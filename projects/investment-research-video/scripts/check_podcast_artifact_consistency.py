#!/usr/bin/env python3
"""Check podcast episode, measured segments, captions, and optional audio duration.

Usage:
  python3 scripts/check_podcast_artifact_consistency.py \
    --episode episode.json --segments segments.json --captions captions.json

Exit codes: 0 = PASS, 1 = findings, 2 = usage or unreadable input error.
The check is deterministic and does not assess pronunciation quality; pair it
with an independent ASR receipt for actual spoken-text verification.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


def load(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"cannot read {path}: {exc}") from exc


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--episode", type=Path, required=True)
    parser.add_argument("--segments", type=Path, required=True)
    parser.add_argument("--captions", type=Path, required=True)
    parser.add_argument("--audio", type=Path)
    args = parser.parse_args()
    try:
        episode = load(args.episode)
        segments_doc = load(args.segments)
        captions_doc = load(args.captions)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    turns = episode.get("turns") or []
    segments = segments_doc.get("segments") or []
    cues = captions_doc.get("cues") or []
    findings: list[str] = []
    if len(turns) != len(segments):
        findings.append(f"turn/segment count mismatch: {len(turns)} != {len(segments)}")
    if len(segments) != len(cues):
        findings.append(f"segment/caption count mismatch: {len(segments)} != {len(cues)}")

    for index, (turn, segment) in enumerate(zip(turns, segments), 1):
        if turn.get("turn_id") != segment.get("turn_id"):
            findings.append(f"row {index} turn_id mismatch")
        if turn.get("text") != segment.get("text"):
            findings.append(f"{turn.get('turn_id', index)} text differs from measured segment")
    for index, (segment, cue) in enumerate(zip(segments, cues), 1):
        expected = segment.get('text')
        if cue.get("turn_id") != segment.get("turn_id") or cue.get("text") != expected:
            findings.append(f"caption row {index} differs from measured segment")
        try:
            start = float(cue["start"])
            end = float(cue["end"])
            seg_start = float(segment["start"])
            seg_end = seg_start + float(segment.get("speech_duration", segment["duration"]))
            if abs(start - seg_start) > 0.01 or abs(end - seg_end) > 0.02:
                findings.append(f"caption timing mismatch at {segment.get('turn_id')}")
        except (KeyError, TypeError, ValueError):
            findings.append(f"caption timing unreadable at row {index}")

    previous_end = 0.0
    for segment in segments:
        try:
            start = float(segment["start"])
            end = float(segment["end"])
            if start < previous_end - 0.02:
                findings.append(f"segment timeline overlaps at {segment.get('turn_id')}")
            previous_end = end + float(segment.get("pause_after_ms", 0)) / 1000
        except (KeyError, TypeError, ValueError):
            findings.append(f"segment timing unreadable at {segment.get('turn_id')}")

    audio_duration = None
    if args.audio:
        try:
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(args.audio)],
                check=True, capture_output=True, text=True,
            )
            audio_duration = float(result.stdout.strip())
            declared = float(segments_doc["total_seconds"])
            if abs(audio_duration - declared) > 0.10:
                findings.append(f"audio duration differs from segments total: {audio_duration:.3f} != {declared:.3f}")
        except (OSError, subprocess.CalledProcessError, KeyError, TypeError, ValueError) as exc:
            findings.append(f"audio duration check failed: {exc}")

    status = "PASS" if not findings else "FAIL"
    print(json.dumps({"status": status, "turns": len(turns), "segments": len(segments), "captions": len(cues), "audio_duration": audio_duration, "findings": findings}, ensure_ascii=False))
    return 0 if status == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
