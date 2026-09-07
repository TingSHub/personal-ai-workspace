#!/usr/bin/env python3
"""Build short caption cues from measured segments.json.

Usage: python3 scripts/build_caption_manifest.py <segments.json> <captions.json> <subtitles.srt>
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

def srt_time(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main() -> int:
    if len(sys.argv) != 4:
        print(__doc__, file=sys.stderr)
        return 2
    source, captions_path, srt_path = map(Path, sys.argv[1:])
    data = json.loads(source.read_text(encoding="utf-8"))
    cues = []
    for segment in data.get("segments", []):
        start = float(segment["start"])
        speech_duration = float(segment.get("speech_duration", segment["duration"]))
        end = start + speech_duration
        # Speaker identity is carried by the caption color in the video.  Keep
        # the machine-readable speaker field, but never put a role/name label
        # into the viewer-facing subtitle text.
        # `text` is the pronunciation-safe TTS source. `display_text` may use
        # Arabic numerals and compact financial notation without changing what
        # the voice model receives.
        display = segment.get('display_text', segment['text'])
        cues.append({"index": len(cues) + 1, "turn_id": segment["turn_id"], "speaker": segment["speaker"], "start": round(start, 3), "end": round(end, 3), "text": display})
    captions_path.parent.mkdir(parents=True, exist_ok=True)
    captions_path.write_text(json.dumps({"schema": "caption-manifest-v2", "cue_policy": "one_per_turn_no_speaker_label", "cues": cues}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with srt_path.open("w", encoding="utf-8") as handle:
        for cue in cues:
            handle.write(f"{cue['index']}\n{srt_time(cue['start'])} --> {srt_time(cue['end'])}\n{cue['text']}\n\n")
    print(f"PASS cues={len(cues)} cue_policy=one_per_turn max_display_chars={max((len(c['text']) for c in cues), default=0)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
