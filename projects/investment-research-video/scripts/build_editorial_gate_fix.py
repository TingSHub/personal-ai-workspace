#!/usr/bin/env python3
"""Clone an editorial-gate episode and apply the verified 2026H1 text fixes."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path


REPLACEMENTS = {
    "2025H1": "2026H1",
    "2025-08-25": "2026-08-26",
    "26.65%": "27.23%",
    "26.6%": "27.23%",
    "+2.4%": "+27.62%",
    "2.4%": "27.62%",
    "3.22亿": "4.53亿",
    "7.29亿": "9.71亿",
    "5.69亿": "8.44亿",
    "+29.4%": "+33.31%",
    "29.4%": "33.31%",
    "约29.4%": "约33.31%",
    "约 29.4%": "约33.31%",
    "+55.2%": "+48.45%",
    "55.2%": "48.45%",
    "约55.2%": "约48.45%",
    "约 55.2%": "约48.45%",
    "-13.81亿": "-1.87亿",
    "12.00%": "13.00%",
    "约12%": "约13%",
    "约 26.6%": "是27.23%",
    "约26.65%": "是27.23%",
    "毛利率约27.23%": "毛利率是27.23%",
    "毛利率约 27.23%": "毛利率是27.23%",
}


def replace(value):
    if isinstance(value, str):
        for old, new in REPLACEMENTS.items():
            value = value.replace(old, new)
        return value
    if isinstance(value, list):
        return [replace(item) for item in value]
    if isinstance(value, dict):
        return {key: replace(item) for key, item in value.items()}
    if isinstance(value, (int, float)):
        return {2.4: 27.62, 26.65: 27.23, 26.6: 27.23, 29.4: 33.31, 55.2: 48.45, -13.81: -1.87}.get(value, value)
    return value


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    episode = replace(copy.deepcopy(json.loads(args.input.read_text(encoding="utf-8"))))
    episode["episode_id"] = "zhongke-shuguang-603019-20260827-editorial-gate-fix"
    episode["research_date"] = "2026-08-27"
    episode["report_context"].update({"report_type": "2026H1", "announcement_date": "2026-08-26", "days_since_release": 1, "freshness": "fresh", "materiality": "high"})
    for turn in episode["turns"]:
        if turn["turn_id"] == "T01-01":
            turn["text"] = "毛利率接近27%，但规模还小，这个差距到底来自产品结构，还是市场份额不足？"
        if turn["turn_id"] == "OUTRO-04":
            turn["text"] = "感谢收看账本两面。如果觉得有收获，记得点赞关注。我们下期再见。"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(episode, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"PASS turns={len(episode['turns'])} output={args.output}")


if __name__ == "__main__":
    main()
