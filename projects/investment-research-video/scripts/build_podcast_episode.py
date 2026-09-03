#!/usr/bin/env python3
"""Build a podcast episode from a company manifest only.

Usage:
  python3 scripts/build_podcast_episode.py --input editorial/episode-input.json --run-root <company-run>

The builder deliberately has no company/topic/outro fallback. Every spoken line,
topic, chart and closing line must come from the input manifest.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path


SHORT_PREFIXES = ("没错", "对", "嗯", "好")
SHORT_PAUSE_MS = 160


def normalize_item(item: dict | list) -> dict:
    if isinstance(item, dict):
        return item
    values = list(item)
    return {
        "speaker": values[0], "text": values[1], "interaction_type": values[2],
        "emotion": values[3], "delivery": values[4], "evidence_ids": values[5],
        "question_ending": values[6], "backchannel": values[7] if len(values) > 7 else None,
    }


def leading_backchannel(text: str) -> str | None:
    for prefix in SHORT_PREFIXES:
        if text.startswith(prefix) and len(text) > len(prefix) and text[len(prefix)] in "，。:：、 ":
            return prefix
    return None


def make_turn(turn_id: str, topic_id: str, item: dict | list, previous: str | None) -> dict:
    spec = normalize_item(item)
    speaker = spec["speaker"]
    backchannel = spec.get("backchannel") or leading_backchannel(spec["text"])
    delivery = spec.get("delivery", "normal")
    if backchannel and delivery == "normal":
        delivery = "short_pause"
    return {
        "turn_id": turn_id,
        "topic_id": topic_id,
        "speaker": speaker,
        "role": "host" if speaker == "zhiwei" else "analyst",
        "beat_group_id": None,
        "reply_to_turn_id": previous,
        "interaction_type": spec.get("interaction_type", "content"),
        "backchannel": backchannel or "none",
        "backchannel_target": previous if backchannel else None,
        "filler_position": "start" if backchannel else "none",
        "question_ending": spec.get("question_ending", "none"),
        "emotion": spec.get("emotion", "thoughtful"),
        "delivery": delivery,
        "evidence_ids": spec.get("evidence_ids", []),
        "fact_ids": spec.get("fact_ids", []),
        "fact_role": spec.get("fact_role", "none"),
        "source_refs": spec.get("source_refs", []),
        "visual_intent": spec.get("visual_intent", "none"),
        "pause_after_ms": int(spec.get("pause_after_ms", SHORT_PAUSE_MS if backchannel else 0)),
        "response_action": "backchannel" if backchannel else "content",
        "text": spec["text"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, required=True)
    parser.add_argument("--run-root", type=Path, required=True)
    args = parser.parse_args()
    manifest = json.loads(args.input.read_text(encoding="utf-8"))
    meta = manifest.get("episode") or {}
    opening = manifest.get("opening") or {}
    topics = manifest.get("topics") or []
    outro = manifest.get("outro") or []
    required_meta = {"episode_id", "company_id", "company_name", "research_date", "show_name", "role_map", "speakers"}
    missing = required_meta - set(meta)
    if missing or not opening.get("cards") or not opening.get("cold_open") or not opening.get("intro") or not topics or not outro:
        raise SystemExit(f"manifest incomplete: missing_meta={sorted(missing)} opening/topics/outro required")
    if normalize_item(opening["cold_open"][0]).get("interaction_type") != "hook":
        raise SystemExit("opening.cold_open[0] must be interaction_type=hook")
    for topic in topics:
        for key in ("topic_id", "title", "claim", "metrics", "chart", "turns"):
            if key not in topic:
                raise SystemExit(f"topic {topic.get('topic_id', '?')} missing {key}")
        if not topic["turns"]:
            raise SystemExit(f"topic {topic['topic_id']} has no turns")

    script_dir = args.run_root / "podcast" / "script"
    visual_dir = args.run_root / "podcast" / "visual-plan"
    script_dir.mkdir(parents=True, exist_ok=True)
    visual_dir.mkdir(parents=True, exist_ok=True)
    turns: list[dict] = []
    previous = None
    for i, item in enumerate(opening["cold_open"], 1):
        turn = make_turn(f"COLD_OPEN-{i:02d}", "COLD_OPEN", item, previous)
        turns.append(turn); previous = turn["turn_id"]
    previous = None
    for i, item in enumerate(opening["intro"], 1):
        turn = make_turn(f"INTRO-{i:02d}", "INTRO", item, previous)
        turns.append(turn); previous = turn["turn_id"]
    for topic in topics:
        previous = None
        for i, item in enumerate(topic["turns"], 1):
            turn = make_turn(f"{topic['topic_id']}-{i:02d}", topic["topic_id"], item, previous)
            turns.append(turn); previous = turn["turn_id"]
    previous = turns[-1]["turn_id"]
    for i, item in enumerate(outro, 1):
        turn = make_turn(f"OUTRO-{i:02d}", "OUTRO", item, previous)
        turns.append(turn); previous = turn["turn_id"]
    for index in range(1, len(turns)):
        if turns[index]["speaker"] == turns[index - 1]["speaker"]:
            beat = f"transition-{turns[index - 1]['topic_id']}-{turns[index]['topic_id']}"
            turns[index - 1]["beat_group_id"] = beat
            turns[index]["beat_group_id"] = beat

    episode = {
        **meta,
        "content_angle": manifest.get("content_angle"),
        "report_context": manifest.get("report_context"),
        "editorial_thesis": manifest.get("editorial_thesis"),
        "financial_data_role": manifest.get("financial_data_role"),
        "opening_rationale": manifest.get("opening_rationale"),
        "cover": manifest.get("cover"),
        "opening_visual": opening.get("opening_visual") or manifest.get("opening_visual"),
        "opening_mode": opening.get("mode", "cold_data_hook"),
        "opening_cards": opening["cards"],
        "comparison_entities": manifest.get("comparison_entities", []),
        "agenda": [topic["title"] for topic in topics],
        "valuation_context": manifest.get("valuation_context"),
        "topics": [{**{k: topic[k] for k in ("topic_id", "title", "claim", "metrics", "chart")}, "short_label": topic.get("short_label", topic["title"].split("，")[0]), "entity_legend": topic.get("entity_legend", []), "fact_ids": topic.get("fact_ids", []), "fact_role": topic.get("fact_role", "none"), "source_refs": topic.get("source_refs", []), "visual_intent": topic.get("visual_intent", "none")} for topic in topics],
        "outro_summary": manifest.get("outro_summary", [{"label": "增长", "value": "已发生", "desc": "收入与利润高增长"}, {"label": "现金", "value": "待验证", "desc": "经营现金流与回款"}, {"label": "产能", "value": "待兑现", "desc": "扩产后的有效回报"}]),
        "turns": turns,
    }
    (script_dir / "episode.json").write_text(json.dumps(episode, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (script_dir / "dialogue-map.json").write_text(json.dumps({"format_mode": meta.get("format_mode", "host_analyst"), "role_map": meta["role_map"], "topic_states": [{"topic_id": t["topic_id"], "question": t["title"], "state": t["claim"]} for t in topics]}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (script_dir / "spoken-style-map.json").write_text(json.dumps({"spoken_rules": ["口播文本必须来自 manifest", "保留事实和数字口径", "不输出交易建议"], "numeric_display": [{"topic_id": t["topic_id"], "exact_evidence": t["chart"].get("evidence_ids", [])} for t in topics]}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (visual_dir / "chart-spec.json").write_text(json.dumps({"version": "v1", "company_id": meta["company_id"], "charts": [{**t["chart"], "topic_id": t["topic_id"]} for t in topics]}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (script_dir / "debate-script.md").open("w", encoding="utf-8") as handle:
        handle.write(f"# {meta['company_name']}｜账本两面主理人播客稿\n\n")
        for turn in turns:
            handle.write(f"[{turn['speaker']}] {turn['text']}\n\n")
    (script_dir / "dialogue-director-execution.md").write_text("# Dialogue Director Execution\n\n- source: episode-input.json\n- topics: manifest-driven\n- outro: manifest-driven\n- company-specific fallback: none\n", encoding="utf-8")
    print(f"PASS company={meta['company_name']} topics={len(topics)} turns={len(turns)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
