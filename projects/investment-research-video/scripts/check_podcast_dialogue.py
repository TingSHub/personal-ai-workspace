#!/usr/bin/env python3
"""Validate the podcast editorial dialogue contract.

Usage:
  python3 scripts/check_podcast_dialogue.py \
    --episode outputs/subjects/<subject>/<date>/podcast/script/episode.json \
    --editorial-execution outputs/subjects/<subject>/<date>/editorial/phase1-execution.md \
    --feedback-constraints outputs/subjects/<subject>/<date>/editorial/feedback-constraints.md \
    [--out outputs/subjects/<subject>/<date>/editorial/dialogue-check.json]

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
MONOSYLLABLE_PREFIX = re.compile(r"^[对嗯好](?:[，。；：！？!?]|$)")
BOOKISH_HOOK = re.compile(r"(?:利润|净利|净利润)快涨(?:了)?三倍")
FORBIDDEN_VALUATION = ("目标价", "评级", "买入", "卖出", "持有", "仓位", "交易策略")
FORBIDDEN_DIRECT_ADVICE = re.compile(
    r"(?:建议|可以|应该|适合|值得|不妨|赶紧|立即|马上)\s*(?:买入|卖出|持有)"
    r"|(?:买入|卖出)\s*(?:这只|该股|这家公司|甲公司|乙公司)?"
    r"|(?:逢低|逢高)\s*(?:买入|卖出)"
)
FORBIDDEN_PRODUCTION_META = ("视频里", "画面里", "字幕里", "镜头里", "观众", "必须把", "必须说", "口播稿")
GROWTH_FIELDS = {"click_reason", "watch_promise", "interaction_value", "follow_reason"}
THESIS_FIELDS = {
    "mechanism", "time_horizon", "affected_segment", "strongest_counterargument",
    "invalidation_condition", "evidence_ids",
}

# --- 数字双文本兜底（第三层）：主防线是表达层契约（dialogue-director 实体 §4/§5），
# 这里的检查只兜"硬性缺失"和"百分比不等价"，不追求覆盖全部读法，避免误报淹没门禁。
CN_DIGITS = {"零": 0, "一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5,
             "六": 6, "七": 7, "八": 8, "九": 9}
SPOKEN_PERCENT = re.compile(r"百分之([零一二两三四五六七八九十百千点]+)")
DISPLAY_PERCENT = re.compile(r"(\d+(?:\.\d+)?)\s*[%％]")
# 问句句尾语气颗粒/疑问语尾：TTS 靠语气词和疑问词识别疑问语调，不是靠问号。
# 裸结构问句（“是不是反转了？”“为什么还不反转？”→ 加“呢/吗”收尾），
# 而“怎么看/怎么读/什么”类疑问语汇本身即升调句，允许。2026-09-07 实测。
QUESTION_PARTICLE_OK = re.compile(
    r"(?:吗|呢|吧|么|呀|啊|什么|为什么|怎么看|怎么办|怎么读|怎么算|怎么讲|怎么理解|"
    r"在哪里|哪儿|哪个|哪|谁|啥|对不对|是不是|对吗|在哪|多少)$"
)
NUMERIC_TEXT = re.compile(
    r"\d+(?:\.\d+)?"
    r"|百分之[零一二两三四五六七八九十百千点]+"
    r"|[零一二两三四五六七八九十百千]+(?:点[零一二两三四五六七八九十]+)?"
    r"(?:亿|万|倍|成|块|元|个百分点|点(?!数|子))"
)


def _cn_int(numerals: str) -> int | None:
    """中文整数位值解析：'三千七百八十一' -> 3781；解析失败返回 None。"""
    result, section, number = 0, 0, 0
    for ch in numerals:
        if ch in CN_DIGITS:
            number = CN_DIGITS[ch]
        elif ch == "十":
            section += (number or 1) * 10
            number = 0
        elif ch == "百":
            section += (number or 1) * 100
            number = 0
        elif ch == "千":
            section += (number or 1) * 1000
            number = 0
        elif ch == "万":
            result += (section or number) * 10000
            section, number = 0, 0
        elif ch == "亿":
            result += (section or number) * 100000000
            section, number = 0, 0
        else:
            return None
    return result + section + number


def _cn_percent_value(numerals: str) -> float | None:
    """'六点五' -> 6.5；'一百点八' -> 100.8；纯整数按位值返回。"""
    if "点" in numerals:
        int_part, frac_part = numerals.split("点", 1)
        whole = _cn_int(int_part)
        if whole is None:
            return None
        frac = 0.0
        scale = 0.1
        for ch in frac_part:
            if ch not in CN_DIGITS:
                return None
            frac += CN_DIGITS[ch] * scale
            scale /= 10
        return whole + frac
    value = _cn_int(numerals)
    return float(value) if value is not None else None


def spoken_percent_values(text: str) -> set[float]:
    features = {float(m.group(1)) for m in DISPLAY_PERCENT.finditer(text)}
    for m in SPOKEN_PERCENT.finditer(text):
        value = _cn_percent_value(m.group(1))
        if value is not None:
            features.add(value)
    return features


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episode", type=Path, required=True)
    parser.add_argument("--editorial-execution", "--phase2-execution", dest="editorial_execution", type=Path, required=True)
    parser.add_argument("--feedback-constraints", type=Path, required=True)
    parser.add_argument("--brokerage-dir", type=Path)
    parser.add_argument("--out", type=Path)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        episode = json.loads(args.episode.read_text(encoding="utf-8"))
        editorial_execution = args.editorial_execution.read_text(encoding="utf-8")
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

    if not topic_order or topic_order[0] != "COLD_OPEN":
        findings.append("episode must start with COLD_OPEN")
    if "INTRO" in topic_order and topic_order.index("INTRO") != 1:
        findings.append("optional INTRO must follow COLD_OPEN")
    if "OUTRO" not in topic_order:
        findings.append("episode must contain OUTRO")
    if not episode.get("editorial_thesis"):
        findings.append("episode requires a clear editorial_thesis")
    growth_contract = episode.get("growth_contract") or {}
    for field in sorted(GROWTH_FIELDS):
        if not growth_contract.get(field):
            findings.append(f"growth_contract missing {field}")
    thesis_contract = episode.get("thesis_contract") or {}
    for field in sorted(THESIS_FIELDS):
        if not thesis_contract.get(field):
            findings.append(f"thesis_contract missing {field}")
    cold = [turn for turn in turns if turn.get("topic_id") == "COLD_OPEN"]
    if not cold:
        findings.append("missing COLD_OPEN turns")
    else:
        first = cold[0]
        text = first.get("text", "")
        if first.get("turn_id") != "COLD_OPEN-01":
            findings.append("first cold-open turn must be COLD_OPEN-01")
        if not text.strip():
            findings.append("COLD_OPEN-01 must contain spoken text")
        # A thesis-led opening need not contain a question or contrast word.
        # Evidence strength and audience payoff are reviewed by the editor.
        if BOOKISH_HOOK.search(text):
            findings.append("COLD_OPEN-01 contains bookish profit-growth wording")

    for index, turn in enumerate(turns):
        text = turn.get("text", "")
        if turn.get("speaker") == "shenyan" and MONOSYLLABLE_PREFIX.search(text):
            findings.append(
                f"{turn.get('turn_id')} analyst turn starts with a monosyllable backchannel; "
                "rewrite it as a meaningful phrase instead of relying on punctuation for TTS separation"
            )
        if text.rstrip().endswith(("？", "?")):
            if turn.get("delivery") != "rising_question":
                findings.append(f"{turn.get('turn_id')} question requires delivery=rising_question")
        if text.rstrip().endswith(("？", "?")):
            question_body = text.rstrip().rstrip("？?")
            if not QUESTION_PARTICLE_OK.search(question_body):
                findings.append(
                    f"{turn.get('turn_id')} question lacks a final particle (吗/呢/吧…); "
                    "rewrite with a particle tail so TTS produces a reliable rising contour"
                )
        if NUMERIC_TEXT.search(text):
            if not turn.get("display_text"):
                findings.append(
                    f"{turn.get('turn_id')} numeric turn missing display_text; "
                    "provide viewer-facing arabic numbers so captions do not show Chinese readings"
                )
            elif spoken_percent_values(text) - spoken_percent_values(turn["display_text"]):
                findings.append(
                    f"{turn.get('turn_id')} display_text differs from spoken numbers; "
                    "keep text (reading) and display_text (viewer) numerically equivalent"
                )
        for phrase in FORBIDDEN_PRODUCTION_META:
            if phrase in text:
                findings.append(f"{turn.get('turn_id')} contains production metadata in spoken text: {phrase}")
        if FORBIDDEN_DIRECT_ADVICE.search(text):
            findings.append(f"{turn.get('turn_id')} contains direct investment advice")
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
        if not valuation.get("source_class"):
            findings.append("enabled valuation_context requires source_class")
        if valuation.get("source_class") == "brokerage" and (
            args.brokerage_dir is None or not args.brokerage_dir.is_dir()
        ):
            findings.append("enabled valuation_context requires research-materials/brokerage/")
        if valuation.get("source_class") != "brokerage" and not valuation.get("source_refs"):
            findings.append("non-brokerage valuation_context requires source_refs")
        for turn in turns:
            if any(word in turn.get("text", "") for word in FORBIDDEN_VALUATION):
                findings.append(f"valuation context contains forbidden advice wording: {turn.get('turn_id')}")

    if "finance-content-engineering" not in editorial_execution:
        findings.append("editorial execution receipt missing finance-content-engineering")

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
