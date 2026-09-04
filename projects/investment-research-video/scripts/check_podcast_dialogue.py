#!/usr/bin/env python3
"""Validate the podcast Phase 2 dialogue contract.

Usage:
  python3 scripts/check_podcast_dialogue.py \
    --episode outputs/companies/<company>/<date>/podcast/script/episode.json \
    --phase2-execution outputs/companies/<company>/<date>/editorial/phase2-execution.md \
    --feedback-constraints outputs/companies/<company>/<date>/editorial/feedback-constraints.md \
    --brokerage-dir outputs/companies/<company>/<date>/research-materials/brokerage \
    [--out outputs/companies/<company>/<date>/editorial/phase2-dialogue-check.json]

Exit codes: 0 = PASS, 1 = findings, 2 = usage or unreadable input error.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


CONTRAST_MARKERS = ("反而", "但", "却", "不过", "只是", "同时")
SHORT_PREFIXES = ("没错", "对", "嗯", "好")
BOOKISH_HOOK = re.compile(r"(?:利润|净利|净利润)快涨(?:了)?三倍")
FORBIDDEN_VALUATION = ("目标价", "评级", "买入", "卖出", "持有", "仓位", "交易策略")
FORBIDDEN_PRODUCTION_META = ("视频里", "画面里", "字幕里", "镜头里", "观众", "必须把", "必须说", "口播稿")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episode", type=Path, required=True)
    parser.add_argument("--phase2-execution", type=Path, required=True)
    parser.add_argument("--feedback-constraints", type=Path, required=True)
    parser.add_argument("--brokerage-dir", type=Path, required=True)
    parser.add_argument("--out", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        episode = json.loads(args.episode.read_text(encoding="utf-8"))
        phase2 = args.phase2_execution.read_text(encoding="utf-8")
        args.feedback_constraints.read_text(encoding="utf-8")
    except (OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: cannot read validation input: {exc}", file=sys.stderr)
        return 2

    findings: list[str] = []
    turns = episode.get("turns") or []
    topic_order = []
    for turn in turns:
        if turn.get("topic_id") not in topic_order:
            topic_order.append(turn.get("topic_id"))

    if topic_order[:2] != ["COLD_OPEN", "INTRO"]:
        findings.append("opening order must be COLD_OPEN -> INTRO")
    cold = [turn for turn in turns if turn.get("topic_id") == "COLD_OPEN"]
    if not cold:
        findings.append("missing COLD_OPEN turns")
    else:
        first = cold[0]
        text = first.get("text", "")
        if first.get("turn_id") != "COLD_OPEN-01":
            findings.append("first cold-open turn must be COLD_OPEN-01")
        if first.get("question_ending") != "question" or "？" not in text:
            findings.append("COLD_OPEN-01 must contain an open question")
        if not any(marker in text for marker in CONTRAST_MARKERS):
            findings.append("COLD_OPEN-01 must contain a fact contrast")
        if BOOKISH_HOOK.search(text):
            findings.append("COLD_OPEN-01 contains bookish profit-growth wording")

    for index, turn in enumerate(turns):
        text = turn.get("text", "")
        for phrase in FORBIDDEN_PRODUCTION_META:
            if phrase in text:
                findings.append(f"{turn.get('turn_id')} contains production metadata in spoken text: {phrase}")
        prefix = next((item for item in SHORT_PREFIXES if any(text.startswith(item + marker) for marker in ("，", "。"))), None)
        if prefix:
            if turn.get("backchannel") != prefix:
                findings.append(f"{turn.get('turn_id')} short response missing backchannel={prefix}")
            if not turn.get("backchannel_target") and index > 0:
                findings.append(f"{turn.get('turn_id')} short response missing backchannel_target")
            if turn.get("filler_position") != "start":
                findings.append(f"{turn.get('turn_id')} short response missing filler_position=start")
            if turn.get("delivery") != "short_pause":
                findings.append(f"{turn.get('turn_id')} short response missing delivery=short_pause")
            if int(turn.get("pause_after_ms", 0)) <= 0:
                findings.append(f"{turn.get('turn_id')} short response missing pause_after_ms")

    valuation = episode.get("valuation_context") or {}
    if valuation.get("enabled"):
        if valuation.get("source_class") != "brokerage":
            findings.append("enabled valuation_context must use source_class=brokerage")
        if not args.brokerage_dir.is_dir():
            findings.append("enabled valuation_context requires research-materials/brokerage/")
        for turn in turns:
            if any(word in turn.get("text", "") for word in FORBIDDEN_VALUATION):
                findings.append(f"valuation context contains forbidden advice wording: {turn.get('turn_id')}")

    for resource in ("human-understanding", "humanizer-zh"):
        if resource not in phase2:
            findings.append(f"phase2 execution receipt missing {resource}")

    # Comparison episodes must name the objects being compared.  Do not infer
    # or ban names from sibling project directories: industry and comparison
    # subjects are explicitly allowed to mention multiple entities.
    comparison_entities = episode.get("comparison_entities") or []
    comparison_signal = any(
        marker in (turn.get("text", "") or "")
        for turn in turns
        for marker in ("三家公司", "几家公司", "多家公司", "三类公司", "三类主体", "多个项目")
    )
    if comparison_signal and len(comparison_entities) < 2:
        findings.append("comparison wording requires comparison_entities[] with at least two named entities")
    if len(comparison_entities) > 1:
        spoken = "\n".join(turn.get("text", "") for turn in turns)
        for entity in comparison_entities:
            name = entity.get("name", "") if isinstance(entity, dict) else str(entity)
            if name and name not in spoken:
                findings.append(f"comparison entity missing from spoken text: {name}")
        for entity in comparison_entities:
            if isinstance(entity, dict):
                for field in ("role", "comparison_axis"):
                    if not entity.get(field):
                        findings.append(f"comparison entity {entity.get('name', '?')} missing {field}")

    report = {
        "status": "PASS" if not findings else "FAIL",
        "episode": str(args.episode),
        "topic_order": topic_order,
        "short_response_count": sum(
            1 for turn in turns if any(turn.get("text", "").startswith(prefix + marker) for prefix in SHORT_PREFIXES for marker in ("，", "。"))
        ),
        "valuation_context_enabled": bool(valuation.get("enabled")),
        "findings": findings,
    }
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
