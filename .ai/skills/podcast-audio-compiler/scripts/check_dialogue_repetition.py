#!/usr/bin/env python3
"""Check a podcast episode manifest for repeated turn endings and exact lines.

Usage: python check_dialogue_repetition.py <episode.json> [--min-ending-chars 8]
Output: JSON findings to stdout. Exit 0 when no repeated endings/lines are found,
1 when findings exist, and 2 for invalid usage or malformed input.
"""

import argparse
import json
import re
import sys
from collections import defaultdict


def normalize(text: str) -> str:
    return re.sub(r"\s+", "", text).strip("，。！？；：、,.!?;:")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("episode")
    parser.add_argument("--min-ending-chars", type=int, default=8)
    args = parser.parse_args()
    try:
        with open(args.episode, encoding="utf-8") as fh:
            data = json.load(fh)
        turns = data["turns"]
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({"status": "ERROR", "error": str(exc)}, ensure_ascii=False))
        return 2

    exact = defaultdict(list)
    endings = defaultdict(list)
    for turn in turns:
        text = str(turn.get("text", ""))
        tid = turn.get("turn_id")
        norm = normalize(text)
        if norm:
            exact[norm].append(tid)
        ending = normalize(text[-args.min_ending_chars:]) if len(text) >= args.min_ending_chars else ""
        if ending:
            endings[ending].append(tid)

    exact_findings = [{"text": text, "turn_ids": ids} for text, ids in exact.items() if len(ids) > 1]
    ending_findings = [{"ending": ending, "turn_ids": ids} for ending, ids in endings.items() if len(ids) > 1]
    result = {
        "status": "PASS" if not exact_findings and not ending_findings else "FINDINGS",
        "exact_repeats": exact_findings,
        "repeated_endings": ending_findings,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
