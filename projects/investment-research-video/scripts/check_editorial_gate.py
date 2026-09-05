#!/usr/bin/env python3
"""Validate the approved topic, accepted research, and director handoff.

This gate deliberately reads the upstream approval directly. Production does
not create a second candidate pool or a local approval copy.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


REQUIRED_CARD_FIELDS = {
    "topic_id", "title", "subject_type", "audience_question", "core_tension",
    "evidence", "status",
}
REQUIRED_TREATMENT_FILES = (
    "director-treatment.md",
    "topic-order.json",
    "opening-selection.json",
    "scene-intent.json",
    "director-execution.md",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-root", type=Path, required=True)
    parser.add_argument("--upstream-topic-card", type=Path, required=True)
    parser.add_argument("--research-brief", type=Path, required=True)
    parser.add_argument("--require-approved", action="store_true")
    parser.add_argument("--out", type=Path)
    return parser.parse_args()


def read_json(path: Path, findings: list[str]) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        findings.append(f"cannot read {path.name}: {exc}")
        return {}
    if not isinstance(value, dict):
        findings.append(f"{path.name} must contain a JSON object")
        return {}
    return value


def section(text: str, heading: str) -> str:
    match = re.search(rf"^## {re.escape(heading)}\s*$\n(.*?)(?=^## |\Z)", text, re.MULTILINE | re.DOTALL)
    return match.group(1).strip() if match else ""


def main() -> int:
    args = parse_args()
    findings: list[str] = []
    upstream = read_json(args.upstream_topic_card, findings)
    try:
        research = args.research_brief.read_text(encoding="utf-8")
    except OSError as exc:
        research = ""
        findings.append(f"cannot read research brief: {exc}")

    status = upstream.get("status")
    approved_id = upstream.get("approved_topic_id")
    approved_at = upstream.get("approved_at") or upstream.get("topic_forward_date")
    cards = upstream.get("cards") or []
    matches = [card for card in cards if isinstance(card, dict) and card.get("topic_id") == approved_id]
    approved_card = matches[0] if len(matches) == 1 else {}

    if len(matches) != 1:
        findings.append("upstream must contain exactly one card matching approved_topic_id")
    if approved_card:
        missing = sorted(field for field in REQUIRED_CARD_FIELDS if not approved_card.get(field))
        if missing:
            findings.append(f"approved card missing {','.join(missing)}")
        if approved_card.get("status") != "approved":
            findings.append("matching topic card must have status=approved")

    approved_question = section(research, "Approved Question")
    scope_decision = section(research, "Scope Decision").splitlines()
    decision = scope_decision[0].strip().lower() if scope_decision else ""
    if not approved_question:
        findings.append("research brief missing Approved Question section")
    elif approved_card.get("audience_question") and approved_card.get("audience_question") not in approved_question:
        findings.append("research question differs from the approved topic card")
    if decision != "accepted":
        findings.append("research Scope Decision must be accepted before production")

    if args.require_approved:
        if status != "approved":
            findings.append("upstream topic status must be approved before production")
        if not approved_id:
            findings.append("upstream approval requires approved_topic_id")
        if not approved_at:
            findings.append("upstream approval requires approved_at")
        editorial = args.run_root / "editorial"
        for filename in REQUIRED_TREATMENT_FILES:
            path = editorial / filename
            if not path.is_file() or not path.read_text(encoding="utf-8").strip():
                findings.append(f"missing director artifact: {filename}")
        order = read_json(editorial / "topic-order.json", findings)
        order_items = order.get("topics") or order.get("topic_order") or []
        if not order_items:
            findings.append("topic-order.json must contain topics/topic_order")
        mechanisms: list[str] = []
        for item in order_items:
            if not isinstance(item, dict):
                findings.append("topic order items must be objects")
                continue
            if not item.get("audience_payoff"):
                findings.append(f"topic order item {item.get('topic_id', '?')} missing audience_payoff")
            mechanism = item.get("primary_mechanism")
            if not mechanism:
                findings.append(f"topic order item {item.get('topic_id', '?')} missing primary_mechanism")
            elif mechanism in mechanisms:
                findings.append(f"primary_mechanism repeated across topics: {mechanism}")
            else:
                mechanisms.append(mechanism)
        for previous, current in zip(order_items, order_items[1:]):
            if isinstance(previous, dict) and isinstance(current, dict):
                if previous.get("audience_payoff") == current.get("audience_payoff"):
                    findings.append(f"adjacent topics repeat audience_payoff: {current.get('topic_id', '?')}")

    report = {
        "status": "PASS" if not findings else "FAIL",
        "run_root": str(args.run_root),
        "approval_status": status,
        "approved_topic_id": approved_id,
        "scope_decision": decision,
        "require_approved": args.require_approved,
        "findings": findings,
    }
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
