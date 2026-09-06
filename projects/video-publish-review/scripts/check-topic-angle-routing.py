#!/usr/bin/env python3
"""Validate content-line to expression-agent routing on topic cards."""
import argparse
import json
from pathlib import Path


ROUTES = {
    "market_pulse": ("market-companion-editor-agent", "行情陪伴型"),
    "earnings_gap": ("earnings-gap-translator-agent", "账本预期差型"),
    "company_industry": ("company-industry-explainer-agent", "生意拆解型"),
    "valuation_mechanism": ("valuation-mechanism-teacher-agent", "机制翻译型"),
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, type=Path)
    args = parser.parse_args()
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    cards = payload.get("cards") if isinstance(payload, dict) else payload
    if not isinstance(cards, list) or not cards:
        raise SystemExit("topic input must contain a non-empty cards list")
    errors = []
    for index, card in enumerate(cards):
        line = card.get("content_line")
        if line not in ROUTES:
            errors.append(f"card[{index}] invalid content_line: {line!r}")
            continue
        agent, mode = ROUTES[line]
        if card.get("expression_agent") != agent:
            errors.append(f"card[{index}] expression_agent mismatch: expected {agent}")
        if card.get("expression_mode") != mode:
            errors.append(f"card[{index}] expression_mode mismatch: expected {mode}")
        for field in ("audience_question", "core_tension", "narrative_direction"):
            if not card.get(field):
                errors.append(f"card[{index}] missing {field}")
        title_options = card.get("title_options")
        if not isinstance(title_options, list) or len(title_options) < 2:
            errors.append(f"card[{index}] needs at least two title_options")
    if errors:
        raise SystemExit("\n".join(errors))
    print(f"PASS topic-angle-routing cards={len(cards)}")


if __name__ == "__main__":
    main()
