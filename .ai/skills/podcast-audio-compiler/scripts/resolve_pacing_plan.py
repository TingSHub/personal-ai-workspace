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

# Turn gaps should support conversation, not make every answer sound like a
# paragraph break. The old resolver used 220–360ms by default and became
# especially slow when a deep episode had many turns.
INTERACTION_PAUSE = {
    "hook": 220,
    "challenge": 180,
    "clarify": 150,
    "question": 180,
    "answer": 150,
    "acknowledge": 100,
    "counter_evidence": 150,
    "summarize": 180,
    "self_introduction": 140,
    "transition": 160,
}


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


def resolve_turn(turn: dict) -> dict:
    result = copy.deepcopy(turn)
    existing = result.get("pacing_plan") or {}
    interaction = str(result.get("interaction_type") or "normal")
    # VoxCPM native timing is the profile baseline. Retiming is allowed only
    # when a director explicitly supplies speech_rate/target_rate_cps.
    rate = float(existing["speech_rate"]) if "speech_rate" in existing else 1.0
    rate = round(clamp(rate, 0.5, 2.0), 3)
    target_rate = None
    if "target_rate_cps" in existing and existing["target_rate_cps"] is not None:
        target_rate = round(clamp(float(existing["target_rate_cps"]), 3.0, 5.5), 2)

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
