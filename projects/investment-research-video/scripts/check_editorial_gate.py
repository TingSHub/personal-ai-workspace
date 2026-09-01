#!/usr/bin/env python3
"""Validate the topic approval and editorial-director handoff contract.

Usage:
  python3 scripts/check_editorial_gate.py --run-root <company-run> --require-approved

Exit codes: 0 = PASS, 1 = findings, 2 = unreadable input/usage error.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


REQUIRED_CANDIDATE_FIELDS = {
    "topic_id", "title", "main_question", "audience_value", "opening_candidate",
    "evidence_ids", "expansion_path", "max_risk", "content_angle",
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


def main() -> int:
    args = parse_args()
    editorial = args.run_root / "editorial"
    findings: list[str] = []
    options_path = editorial / "topic-options.json"
    approval_path = editorial / "topic-approval.md"
    options = read_json(options_path, findings)
    try:
        approval = approval_path.read_text(encoding="utf-8")
    except OSError as exc:
        approval = ""
        findings.append(f"cannot read topic-approval.md: {exc}")

    candidates = options.get("candidates") or options.get("topics") or []
    if not isinstance(candidates, list) or not 3 <= len(candidates) <= 5:
        findings.append("topic-options.json must contain 3-5 candidates")
        candidates = candidates if isinstance(candidates, list) else []
    candidate_ids: list[str] = []
    for candidate in candidates:
        if not isinstance(candidate, dict):
            findings.append("each candidate must be an object")
            continue
        candidate_id = candidate.get("topic_id")
        if candidate_id:
            candidate_ids.append(candidate_id)
        missing = sorted(REQUIRED_CANDIDATE_FIELDS - set(candidate))
        if missing:
            findings.append(f"candidate {candidate_id or '?'} missing {','.join(missing)}")
        if not candidate.get("evidence_ids"):
            findings.append(f"candidate {candidate_id or '?'} has no evidence_ids")
    if len(set(candidate_ids)) != len(candidate_ids):
        findings.append("candidate topic_id values must be unique")

    status = "approved" if "status: approved" in approval else "pending" if "status: pending" in approval else "rejected" if "status: rejected" in approval else "missing"
    approved_id = None
    for line in approval.splitlines():
        if line.startswith("topic_id:"):
            approved_id = line.split(":", 1)[1].strip()
            break
    approved_at = any(line.startswith("approved_at:") and line.split(":", 1)[1].strip() for line in approval.splitlines())
    if args.require_approved:
        if status != "approved":
            findings.append("topic approval status must be approved before downstream production")
        if not approved_id or approved_id not in candidate_ids:
            findings.append("approved topic_id must match one candidate")
        if not approved_at:
            findings.append("approved topic requires approved_at")
        for filename in REQUIRED_TREATMENT_FILES:
            path = editorial / filename
            if not path.is_file() or not path.read_text(encoding="utf-8").strip():
                findings.append(f"missing approved treatment artifact: {filename}")
        order = read_json(editorial / "topic-order.json", findings)
        order_items = order.get("topics") or order.get("topic_order") or []
        if not order_items:
            findings.append("topic-order.json must contain topics/topic_order")
        mechanisms: list[str] = []
        for item in order_items:
            if isinstance(item, dict):
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
        "candidate_count": len(candidates),
        "candidate_ids": candidate_ids,
        "approval_status": status,
        "approved_topic_id": approved_id,
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
