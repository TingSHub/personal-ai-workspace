#!/usr/bin/env python3
"""Known-text Chinese forced alignment for the locked Presentation Notes."""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path


def extract_notes(path: Path) -> list[str]:
    source = path.read_text(encoding="utf-8")
    notes = re.findall(r'<aside\b[^>]*class="[^\"]*\bnotes\b[^\"]*"[^>]*>(.*?)</aside>', source, re.S)
    return [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", item)).strip() for item in notes]


def ts(seconds: float) -> str:
    seconds = max(0.0, seconds)
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    whole = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    if millis == 1000:
        whole += 1
        millis = 0
    return f"{hours:02d}:{minutes:02d}:{whole:02d},{millis:03d}"


def write_srt(chunks: list[dict], path: Path) -> None:
    blocks = []
    for index, item in enumerate(chunks, 1):
        blocks.append(f"{index}\n{ts(item['start'])} --> {ts(item['end'])}\n{item['text']}\n")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(blocks), encoding="utf-8")


def chunk_items(items: list[dict], scene_start: float, scene_end: float) -> list[dict]:
    chunks = []
    current = []
    start = None
    for item in items:
        if start is None:
            start = float(item["start_time"])
        current.append(item)
        text = "".join(x["text"] for x in current)
        elapsed = float(item["end_time"]) - float(start)
        if text.endswith(("。", "！", "？", "；", ".", "!", "?", ";")) or len(text) >= 18 or elapsed >= 4.5:
            chunks.append({
                "start": scene_start + float(start),
                "end": min(scene_end, scene_start + float(item["end_time"])),
                "text": text,
            })
            current = []
            start = None
    if current:
        chunks.append({
            "start": scene_start + float(start),
            "end": min(scene_end, scene_start + float(current[-1]["end_time"])),
            "text": "".join(x["text"] for x in current),
        })
    return [item for item in chunks if item["end"] > item["start"] and item["text"].strip()]


def build_cues(items: list[dict], scene_start: float, scene_end: float, stage_count: int, scene_id: str) -> list[dict]:
    if not items:
        return []
    cues = []
    for stage in range(1, stage_count + 1):
        fraction = stage / (stage_count + 1)
        index = min(len(items) - 1, max(0, int(round(fraction * (len(items) - 1)))))
        item = items[index]
        cues.append({
            "scene_id": scene_id,
            "cue_id": f"{scene_id}-stage-{stage}",
            "stage": stage,
            "timestamp": round(scene_start + float(item["start_time"]), 3),
            "anchor_text": item["text"],
            "source": "aligned-token-order",
        })
    return cues


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", type=Path, required=True)
    ap.add_argument("--segments", type=Path, required=True)
    ap.add_argument("--audio-dir", type=Path, required=True)
    ap.add_argument("--outdir", type=Path, required=True)
    ap.add_argument("--model", default="Qwen/Qwen3-ForcedAligner-0.6B")
    args = ap.parse_args()

    import torch
    from qwen_asr import Qwen3ForcedAligner

    notes = extract_notes(args.html)
    payload = json.loads(args.segments.read_text(encoding="utf-8"))
    segments = payload["segments"]
    if len(notes) != len(segments):
        raise SystemExit(f"notes={len(notes)} segments={len(segments)} mismatch")

    print(f"loading {args.model}")
    model = Qwen3ForcedAligner.from_pretrained(args.model, dtype=torch.bfloat16, device_map="cuda:0")
    all_scenes = []
    all_cues = []
    all_chunks = []
    for index, (note, segment) in enumerate(zip(notes, segments), 1):
        audio = args.audio_dir / "segments" / f"seg-{index:02d}.mp3"
        print(f"align scene-{index:02d}: {audio.name}", flush=True)
        result = model.align(audio=str(audio), text=note, language="Chinese")[0]
        items = [
            {"text": item.text, "start_time": float(item.start_time), "end_time": float(item.end_time)}
            for item in result.items
        ]
        scene_start = float(segment["start"])
        scene_end = float(segment["end"])
        stage_count = 4
        scene_id = f"scene-{index:02d}"
        cues = build_cues(items, scene_start, scene_end, stage_count, scene_id)
        chunks = chunk_items(items, scene_start, scene_end)
        all_cues.extend(cues)
        all_chunks.extend(chunks)
        all_scenes.append({
            "scene_id": scene_id,
            "page": index,
            "audio": str(audio),
            "start": scene_start,
            "duration": float(segment["duration"]),
            "end": scene_end,
            "note_chars": len(note),
            "aligned_items": items,
            "cues": cues,
            "subtitle_chunks": chunks,
        })
        print(f"  items={len(items)} cues={len(cues)} subtitles={len(chunks)}", flush=True)

    args.outdir.mkdir(parents=True, exist_ok=True)
    alignment = {
        "method": "qwen3-forced-aligner",
        "model": args.model,
        "language": "Chinese",
        "total_seconds": payload["total_seconds"],
        "scenes": all_scenes,
    }
    (args.outdir / "alignment.json").write_text(json.dumps(alignment, ensure_ascii=False, indent=2), encoding="utf-8")
    timing_map = {
        "method": "aligned-token-order-stage-cues",
        "total_seconds": payload["total_seconds"],
        "cues": all_cues,
    }
    (args.outdir / "timing-map.json").write_text(json.dumps(timing_map, ensure_ascii=False, indent=2), encoding="utf-8")
    write_srt(all_chunks, args.outdir / "subtitles" / "narration.srt")
    print(f"wrote {args.outdir / 'alignment.json'} · cues={len(all_cues)} · subtitles={len(all_chunks)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
