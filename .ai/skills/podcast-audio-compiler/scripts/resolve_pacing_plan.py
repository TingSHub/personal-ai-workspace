#!/usr/bin/env python3
"""Resolve semantic performance fields into deterministic pacing_plan values."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path


EMOTION_RATE = {
    "curious": 1.00,
    "firm": 0.98,
    "skeptical": 0.95,
    "cautious": 0.95,
    "thoughtful": 0.93,
}

SPEAKER_BASELINE_CPS = {
    "zhiwei": 3.9,
    "shenyan": 3.9,
}

DELIVERY_RATE = {
    "normal": 1.00,
    "stress_contrast": 0.96,
    "pause_before_number": 0.98,
    "short_pause": 0.98,
}

INTERACTION_PAUSE = {
    "hook": 360,
    "challenge": 300,
    "clarify": 240,
    "question": 300,
    "answer": 240,
    "acknowledge": 160,
    "counter_evidence": 220,
    "summarize": 320,
    "self_introduction": 200,
    "transition": 260,
}


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def resolve_turn(turn: dict) -> dict:
    result = copy.deepcopy(turn)
    existing = result.get("pacing_plan") or {}
    emotion = str(result.get("emotion") or "neutral")
    delivery = str(result.get("delivery") or "normal")
    interaction = str(result.get("interaction_type") or "normal")
    rate = float(existing.get("speech_rate", EMOTION_RATE.get(emotion, 1.0)))
    if "speech_rate" not in existing:
        rate *= DELIVERY_RATE.get(delivery, 1.0)
    rate = round(clamp(rate, 0.88, 1.04), 3)
    target_rate = float(existing.get("target_rate_cps", SPEAKER_BASELINE_CPS.get(result.get("speaker"), 3.9)))
    if "target_rate_cps" not in existing:
        target_rate *= EMOTION_RATE.get(emotion, 1.0) * DELIVERY_RATE.get(delivery, 1.0)
    target_rate = round(clamp(target_rate, 3.2, 4.3), 2)

    pause_after = existing.get("pause_after_ms")
    if pause_after is None:
        pause_after = INTERACTION_PAUSE.get(interaction, 180)

    anchors = result.get("pause_anchors") or result.get("performance_direction", {}).get("pause_anchors") or []
    breaks = list(existing.get("intra_turn_breaks") or [])
    known = {item.get("after") for item in breaks}
    for anchor in anchors:
        marker = str(anchor.get("after", anchor) if isinstance(anchor, dict) else anchor)
        if marker and marker not in known and marker in result["text"]:
            duration = int(anchor.get("pause_ms", 320) if isinstance(anchor, dict) else 320)
            breaks.append({"after": marker, "pause_ms": max(120, min(800, duration))})

    result["pacing_plan"] = {
        "speech_rate": rate,
        "target_rate_cps": target_rate,
        "pause_after_ms": int(pause_after),
        "intra_turn_breaks": breaks,
        "resolved_by": "resolve_pacing_plan.py",
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episode", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--plan-out", type=Path)
    args = parser.parse_args()
    episode = json.loads(args.episode.read_text(encoding="utf-8"))
    resolved = copy.deepcopy(episode)
    resolved["turns"] = [resolve_turn(turn) for turn in episode.get("turns", [])]
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(resolved, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    plan = {
        "resolver": "resolve_pacing_plan.py",
        "turns": [
            {"turn_id": turn["turn_id"], "pacing_plan": turn["pacing_plan"]}
            for turn in resolved["turns"]
        ],
    }
    plan_out = args.plan_out or args.out.with_name("pacing-plan.json")
    plan_out.write_text(json.dumps(plan, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"PASS resolved_turns={len(resolved['turns'])} out={args.out} plan={plan_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
