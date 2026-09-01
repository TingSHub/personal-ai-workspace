#!/usr/bin/env python3
"""Run Qwen known-text alignment over podcast turn WAVs and flag failed turns."""

import argparse
import json
import re
from pathlib import Path


def normalize(text: str) -> str:
    return re.sub(r"[^\u4e00-\u9fffA-Za-z0-9]", "", text).lower()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episode", type=Path, required=True)
    parser.add_argument("--segments", type=Path, required=True)
    parser.add_argument("--audio-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--model", default="Qwen/Qwen3-ForcedAligner-0.6B")
    args = parser.parse_args()

    import torch
    from qwen_asr import Qwen3ForcedAligner

    episode = json.loads(args.episode.read_text(encoding="utf-8"))
    timeline = json.loads(args.segments.read_text(encoding="utf-8"))
    turns = episode["turns"]
    segments = timeline["segments"]
    if len(turns) != len(segments):
        raise SystemExit(f"turns={len(turns)} segments={len(segments)} mismatch")
    model = Qwen3ForcedAligner.from_pretrained(args.model, dtype=torch.bfloat16, device_map="cuda:0")
    results = []
    for turn, segment in zip(turns, segments):
        audio = args.audio_dir / f"{turn['turn_id']}.wav"
        row = {"turn_id": turn["turn_id"], "audio": str(audio), "expected_text": turn["text"], "duration": segment["duration"], "status": "PASS"}
        try:
            aligned = model.align(audio=str(audio), text=turn["text"], language="Chinese")[0]
            items = [{"text": x.text, "start": float(x.start_time), "end": float(x.end_time)} for x in aligned.items]
            recognized = "".join(x["text"] for x in items)
            row["aligned_items"] = len(items)
            row["aligned_text"] = recognized
            row["alignment_end"] = items[-1]["end"] if items else 0
            if not items or row["alignment_end"] > float(segment["duration"]) + 1.0 or not normalize(recognized):
                row["status"] = "FAIL"
                row["finding"] = "empty or out-of-range alignment"
        except Exception as exc:
            row["status"] = "FAIL"
            row["finding"] = f"{type(exc).__name__}: {exc}"
        results.append(row)
        print(f"{row['status']} {row['turn_id']} items={row.get('aligned_items', 0)}", flush=True)
    report = {"status": "PASS" if all(x["status"] == "PASS" for x in results) else "FAIL", "method": "qwen3-known-text-alignment", "model": args.model, "turn_count": len(results), "anomalies": [x for x in results if x["status"] != "PASS"], "turns": results}
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status": report["status"], "turn_count": len(results), "anomalies": len(report["anomalies"])}))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
