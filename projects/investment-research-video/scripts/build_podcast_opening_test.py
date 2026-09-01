#!/usr/bin/env python3
"""Extract a short, manifest-driven COLD_OPEN + INTRO canary from an episode."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


CONTRAST_MARKERS = ("反而", "但", "却", "不过", "只是", "同时")
BOOKISH_HOOK_PATTERNS = (
    re.compile(r"(?:利润|净利|净利润)快涨(?:了)?三倍"),
)


def validate_cold_open(turns: list[dict]) -> None:
    """Validate the reusable hook contract before writing the canary manifest.

    The check is deliberately narrow: it catches the regression discussed in
    the user review (data listing or bookish phrasing) while leaving topic-
    specific wording to the editor.
    """
    cold_turns = [turn for turn in turns if turn["topic_id"] == "COLD_OPEN"]
    if not cold_turns:
        raise SystemExit("episode must contain COLD_OPEN turns")

    first = cold_turns[0]
    text = str(first.get("text", ""))
    if first.get("turn_id") != "COLD_OPEN-01":
        raise SystemExit("first COLD_OPEN turn must be COLD_OPEN-01")
    if first.get("question_ending") != "question" or "？" not in text:
        raise SystemExit("COLD_OPEN-01 must end with an open question")
    if not any(marker in text for marker in CONTRAST_MARKERS):
        raise SystemExit("COLD_OPEN-01 must contain an explicit fact contrast")
    for pattern in BOOKISH_HOOK_PATTERNS:
        if pattern.search(text):
            raise SystemExit(
                "COLD_OPEN-01 uses bookish hook wording; prefer natural spoken phrasing"
            )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episode", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    episode = json.loads(args.episode.read_text(encoding="utf-8"))
    opening_ids = {"COLD_OPEN", "INTRO"}
    turns = [turn for turn in episode["turns"] if turn["topic_id"] in opening_ids]
    if not turns or {turn["topic_id"] for turn in turns} != opening_ids:
        raise SystemExit("episode must contain both COLD_OPEN and INTRO turns")
    topic_order = []
    for turn in turns:
        if turn["topic_id"] not in topic_order:
            topic_order.append(turn["topic_id"])
    if topic_order[:2] != ["COLD_OPEN", "INTRO"]:
        raise SystemExit("opening order must be COLD_OPEN -> INTRO")
    validate_cold_open(turns)

    opening = {
        "episode_id": f"{episode['episode_id']}-opening-canary",
        "company_id": episode.get("company_id"),
        "company_name": episode.get("company_name"),
        "research_date": episode.get("research_date"),
        "show_name": episode.get("show_name"),
        "opening_mode": episode.get("opening_mode", "cold_data_hook"),
        "opening_cards": episode.get("opening_cards", []),
        "format_mode": episode.get("format_mode", "host_analyst"),
        "role_map": episode.get("role_map", {}),
        "speakers": episode.get("speakers", {}),
        "agenda": episode.get("agenda", []),
        "topics": [],
        "turns": turns,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(
        json.dumps(opening, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"PASS opening_turns={len(turns)} out={args.out}")


if __name__ == "__main__":
    main()
