#!/usr/bin/env python3
"""Validate that bounded spoken-polish review changed the actual episode text safely."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


IMMUTABLE_FIELDS = ("speaker", "topic_id", "evidence_ids")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--draft", type=Path, required=True)
    parser.add_argument("--final", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--require-change", action="store_true")
    parser.add_argument("--min-change-ratio", type=float, default=0.0, help="minimum changed-turn ratio, e.g. 0.08")
    args = parser.parse_args()
    draft = json.loads(args.draft.read_text(encoding="utf-8"))
    final = json.loads(args.final.read_text(encoding="utf-8"))
    draft_turns = {turn["turn_id"]: turn for turn in draft.get("turns", [])}
    final_turns = {turn["turn_id"]: turn for turn in final.get("turns", [])}
    findings = []
    diff = []

    if set(draft_turns) != set(final_turns):
        findings.append("draft/final turn_id sets differ")
    for turn_id in sorted(set(draft_turns) & set(final_turns)):
        before = draft_turns[turn_id]
        after = final_turns[turn_id]
        for field in IMMUTABLE_FIELDS:
            if before.get(field) != after.get(field):
                findings.append(f"{turn_id} immutable field changed: {field}")
        before_text = before.get("text", "")
        after_text = after.get("text", "")
        if before_text != after_text:
            diff.append({"turn_id": turn_id, "before": before_text, "after": after_text})
        if not after_text.strip():
            findings.append(f"{turn_id} final text is empty")

    if args.require_change and not diff:
        findings.append("spoken-polish produced no text changes")
    if args.min_change_ratio > 0:
        ratio = len(diff) / max(len(draft_turns), 1)
        if ratio < args.min_change_ratio:
            findings.append(f"spoken-polish changed-turn ratio {ratio:.3f} below minimum {args.min_change_ratio:.3f}")
    report = {
        "status": "PASS" if not findings else "FAIL",
        "draft": str(args.draft),
        "final": str(args.final),
        "changed_turn_count": len(diff),
        "diff": diff,
        "findings": findings,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0 if not findings else 1


if __name__ == "__main__":
    raise SystemExit(main())
