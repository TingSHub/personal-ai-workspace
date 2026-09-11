#!/usr/bin/env python3
"""Check that charts and scene states reveal against named narration turns.

Usage:
  python3 scripts/check_podcast_visual_sync.py --episode episode.json \
    --scene-manifest scene-manifest.json --segments segments.json [--charts chart-spec.json]

Exit codes: 0 = PASS, 1 = findings, 2 = usage or unreadable input error.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


MULTI_STEP_TYPES = {"line", "multiline", "step-line", "flow", "checklist", "validation-dashboard"}
ALLOWED_ACTIONS = {"establish", "reveal", "connect", "compare", "challenge", "resolve"}
ALLOWED_TRANSITIONS = {"push", "focus-pull", "crossfade", "cut"}
ALLOWED_PURPOSES = {"establish", "explain", "compare", "challenge", "conclude"}


def is_number(value: object) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def dom_id(value: object) -> str:
    return re.sub(r"[^a-zA-Z0-9_-]+", "-", str(value or "chart")).strip("-") or "chart"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episode", type=Path, required=True)
    parser.add_argument("--charts", type=Path)
    parser.add_argument("--scene-manifest", type=Path, required=True)
    parser.add_argument("--segments", type=Path, required=True)
    args = parser.parse_args()
    try:
        episode = json.loads(args.episode.read_text(encoding="utf-8"))
        charts = json.loads(args.charts.read_text(encoding="utf-8")) if args.charts else {"charts": []}
        scene_manifest = json.loads(args.scene_manifest.read_text(encoding="utf-8"))
        segments_payload = json.loads(args.segments.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read validation input: {exc}", file=sys.stderr)
        return 2

    if scene_manifest.get("version") != "v3":
        print(json.dumps({
            "status": "FAIL",
            "findings": ["scene manifest must use investment-video-scene-manifest v3"],
        }, ensure_ascii=False))
        return 1

    turns = {turn.get("turn_id"): turn for turn in episode.get("turns", [])}
    segments = {
        segment.get("turn_id"): segment
        for segment in segments_payload.get("segments", [])
        if segment.get("turn_id")
    }
    findings: list[str] = []
    scenes = scene_manifest.get("scenes", [])
    dials = (scene_manifest.get("visual_system") or {}).get("design_dials") or {}
    for dial in ("design_variance", "motion_intensity", "visual_density"):
        value = dials.get(dial)
        if not is_number(value) or not 1 <= value <= 10:
            findings.append(f"scene manifest has invalid design dial: {dial}")
    scenes_by_topic: dict[str, list[dict]] = {}
    for scene in scenes:
        scenes_by_topic.setdefault(scene.get("topic_id"), []).append(scene)

    rendered_chart_ids: set[str] = set()
    for chart in charts.get("charts", []):
        chart_id = chart.get("chart_id", "?")
        chart_dom_id = dom_id(chart_id)
        if chart_dom_id in rendered_chart_ids:
            findings.append(f"duplicate rendered chart id: {chart_dom_id}")
        rendered_chart_ids.add(chart_dom_id)
        if chart.get("type") not in MULTI_STEP_TYPES:
            continue
        chart_prefixes = (
            f"chart-{chart_dom_id}",
            f"chart-row-{chart_dom_id}-",
            f"chart-bar-{chart_dom_id}-",
            f"chart-series-{chart_dom_id}-",
            f"chart-node-{chart_dom_id}-",
            f"chart-point-{chart_dom_id}-",
            f"chart-connector-{chart_dom_id}-",
        )
        chart_states = [
            state
            for scene in scenes_by_topic.get(chart.get("topic_id"), [])
            for state in scene.get("states", [])
            if any(
                str(target_id).startswith(chart_prefixes)
                for target_id in state.get("target_ids", [])
            )
        ]
        if len(chart_states) < 2:
            findings.append(f"{chart_id} requires at least two scene states targeting the chart")

    state_ids: set[str] = set()
    scene_ids: set[str] = set()
    if not scenes:
        findings.append("scene manifest requires at least one scene")
    expected_topics = {turn.get("topic_id") for turn in turns.values() if turn.get("topic_id")}
    covered_topics = {scene.get("topic_id") for scene in scenes if scene.get("topic_id")}
    for topic_id in sorted(expected_topics - covered_topics):
        findings.append(f"scene manifest does not cover episode topic: {topic_id}")

    previous_scene_start: float | None = None
    for scene in scenes:
        scene_id = scene.get("scene_id", "?")
        scene_topic_id = scene.get("topic_id")
        if scene_id in scene_ids:
            findings.append(f"duplicate scene_id: {scene_id}")
        scene_ids.add(scene_id)
        if scene.get("purpose") not in ALLOWED_PURPOSES:
            findings.append(f"{scene_id} has unsupported purpose: {scene.get('purpose')}")
        for field in ("visual_pattern", "viewer_question", "cognitive_change", "continuity_anchor"):
            if not scene.get(field):
                findings.append(f"{scene_id} is missing {field}")
        scene_start = scene.get("start")
        scene_end = scene.get("end")
        if not is_number(scene_start) or not is_number(scene_end) or scene_end <= scene_start:
            findings.append(f"{scene_id} has invalid start/end")
        else:
            if previous_scene_start is not None and scene_start < previous_scene_start:
                findings.append(f"scenes are not ordered by start time: {scene_id}")
            previous_scene_start = float(scene_start)
        states = scene.get("states") or []
        if not states:
            findings.append(f"{scene_id} requires at least one semantic state")
        elif len(states) >= 3 and len({state.get("action") for state in states}) < 2:
            findings.append(f"{scene_id} repeats one motion action across three or more states")
        previous_at: float | None = None
        scene_state_ids: set[str] = set()
        for state in states:
            state_id = state.get("state_id")
            if not state_id:
                findings.append(f"{scene_id} contains a state without state_id")
                continue
            if state_id in state_ids:
                findings.append(f"duplicate state_id: {state_id}")
            state_ids.add(state_id)
            scene_state_ids.add(state_id)

            turn_id = state.get("turn_id")
            if turn_id not in turns:
                findings.append(f"{state_id} references unknown narration turn: {turn_id}")
            elif scene_topic_id and turns[turn_id].get("topic_id") != scene_topic_id:
                findings.append(f"{state_id} narration turn is outside scene topic: {turn_id}")

            action = state.get("action")
            if action not in ALLOWED_ACTIONS:
                findings.append(f"{state_id} has unsupported action: {action}")
            target_ids = state.get("target_ids") or []
            if not target_ids:
                findings.append(f"{state_id} is missing target_ids")
            for target_id in target_ids:
                if str(target_id).startswith(("topic-", "turn-", "caption-", "chart-stage-", "persistent-nav-")):
                    findings.append(f"{state_id} targets a framework-owned clip: {target_id}")

            at = state.get("at")
            hold_until = state.get("hold_until")
            if not is_number(at):
                findings.append(f"{state_id} has invalid at time")
                continue
            if previous_at is not None and at < previous_at:
                findings.append(f"{scene_id} states are not ordered by at time: {state_id}")
            previous_at = at
            if not is_number(hold_until) or hold_until < at:
                findings.append(f"{state_id} has invalid hold_until")
            elif is_number(scene_end) and hold_until > scene_end:
                findings.append(f"{state_id} hold_until is outside scene")

            if is_number(scene_start) and is_number(scene_end) and not scene_start <= at <= scene_end:
                findings.append(f"{state_id} at time is outside scene")

            segment = segments.get(turn_id)
            if not segment:
                findings.append(f"{state_id} narration turn is missing from segments: {turn_id}")
            elif segment:
                if at < segment.get("start", at) or at > segment.get("end", at):
                    findings.append(f"{state_id} at time is outside narration turn: {turn_id}")

        transition = scene.get("transition_out") or {}
        transition_type = transition.get("type")
        if transition_type not in ALLOWED_TRANSITIONS:
            findings.append(f"{scene_id} has unsupported transition_out.type: {transition_type}")
        duration = transition.get("duration", 0)
        if not is_number(duration) or duration < 0 or duration > 0.8:
            findings.append(f"{scene_id} has invalid transition duration")
        for cue in scene.get("audio_cues") or []:
            cue_id = cue.get("cue_id", "?")
            if cue.get("state_id") not in scene_state_ids:
                findings.append(f"{scene_id} audio cue {cue_id} references unknown state")
            if not cue.get("asset_ref"):
                findings.append(f"{scene_id} audio cue {cue_id} is missing asset_ref")
            if not is_number(cue.get("gain_db")) or not is_number(cue.get("ducking_db")):
                findings.append(f"{scene_id} audio cue {cue_id} has invalid gain/ducking")

    for index in range(2, len(scenes)):
        patterns = [scenes[offset].get("visual_pattern") for offset in range(index - 2, index + 1)]
        if patterns[0] and len(set(patterns)) == 1:
            findings.append(f"three consecutive scenes reuse one visual pattern: {patterns[0]}")

    report = {"status": "PASS" if not findings else "FAIL", "findings": findings}
    print(json.dumps(report, ensure_ascii=False))
    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
