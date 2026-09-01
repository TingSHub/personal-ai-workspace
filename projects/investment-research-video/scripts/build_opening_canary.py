#!/usr/bin/env python3
"""Build a reusable COLD_OPEN + INTRO canary project input.

Usage:
  python3 scripts/build_opening_canary.py \
    --episode <episode.json> --segments <segments.json> --out <canary-dir>

The script copies only the opening WAV segments, writes a trimmed segments
manifest, and creates a matching narration-full.mp3 with ffmpeg.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episode", type=Path, required=True)
    parser.add_argument("--segments", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--turns", type=int, default=4)
    args = parser.parse_args()

    episode = json.loads(args.episode.read_text(encoding="utf-8"))
    timeline = json.loads(args.segments.read_text(encoding="utf-8"))
    opening_ids = {"COLD_OPEN", "INTRO"}
    opening = [s for s in timeline["segments"] if s["topic_id"] in opening_ids][: args.turns]
    if not opening or {s["topic_id"] for s in opening} != opening_ids:
        raise SystemExit("segments must contain COLD_OPEN and INTRO")

    out_audio = args.out / "audio"
    out_segments = out_audio / "segments"
    out_segments.mkdir(parents=True, exist_ok=True)
    source_segments = args.segments.parent / "segments"
    pause_files = []
    concat_lines = []
    cursor = 0.0
    normalized = []
    for index, segment in enumerate(opening, 1):
        source = source_segments / f"{segment['turn_id']}.wav"
        target = out_segments / source.name
        shutil.copy2(source, target)
        length = float(segment["duration"])
        normalized_segment = dict(segment)
        normalized_segment["index"] = index
        normalized_segment["start"] = round(cursor, 3)
        normalized_segment["end"] = round(cursor + length, 3)
        normalized.append(normalized_segment)
        concat_lines.append(f"file '{target.resolve()}'\n")
        pause_ms = int(segment.get("pause_after_ms", 0))
        if index < len(opening) and pause_ms:
            pause_source = source_segments / f"pause-{segment['index']:02d}.wav"
            pause_target = out_segments / pause_source.name
            if pause_source.exists():
                shutil.copy2(pause_source, pause_target)
                concat_lines.append(f"file '{pause_target.resolve()}'\n")
                pause_files.append(pause_target)
                cursor += pause_ms / 1000
        cursor += length

    (out_audio / "concat.txt").write_text("".join(concat_lines), encoding="utf-8")
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(out_audio / "concat.txt"), "-c", "copy", str(out_audio / "narration-full.wav")],
        check=True,
        capture_output=True,
    )
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(out_audio / "narration-full.wav"), "-c:a", "libmp3lame", "-q:a", "2", str(out_audio / "narration-full.mp3")],
        check=True,
        capture_output=True,
    )
    (out_audio / "segments.json").write_text(
        json.dumps({"total_seconds": round(cursor, 3), "segments": normalized}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"PASS opening_turns={len(normalized)} duration={cursor:.3f}s out={args.out}")


if __name__ == "__main__":
    main()
