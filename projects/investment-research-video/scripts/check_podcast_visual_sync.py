#!/usr/bin/env python3
"""Check that multi-step charts reveal against named narration turns.

Usage:
  python3 scripts/check_podcast_visual_sync.py --episode episode.json --charts chart-spec.json

Exit codes: 0 = PASS, 1 = findings, 2 = usage or unreadable input error.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


MULTI_STEP_TYPES = {"line", "multiline", "step-line", "flow", "checklist", "validation-dashboard"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episode", type=Path, required=True)
    parser.add_argument("--charts", type=Path, required=True)
    args = parser.parse_args()
    try:
        episode = json.loads(args.episode.read_text(encoding="utf-8"))
        charts = json.loads(args.charts.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read validation input: {exc}", file=sys.stderr)
        return 2

    turns = {turn.get("turn_id"): turn for turn in episode.get("turns", [])}
    findings: list[str] = []
    for chart in charts.get("charts", []):
        if chart.get("type") not in MULTI_STEP_TYPES:
            continue
        chart_id = chart.get("chart_id", "?")
        beats = chart.get("narration_beats") or []
        if len(beats) < 2:
            findings.append(f"{chart_id} requires at least two narration_beats")
            continue
        for beat in beats:
            turn_id = beat.get("turn_id")
            if turn_id not in turns:
                findings.append(f"{chart_id} references unknown narration turn: {turn_id}")
                continue
            if turns[turn_id].get("topic_id") != chart.get("topic_id"):
                findings.append(f"{chart_id} narration turn is outside chart topic: {turn_id}")
            if not beat.get("reveal"):
                findings.append(f"{chart_id} narration beat missing reveal: {turn_id}")

    report = {"status": "PASS" if not findings else "FAIL", "findings": findings}
    print(json.dumps(report, ensure_ascii=False))
    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
