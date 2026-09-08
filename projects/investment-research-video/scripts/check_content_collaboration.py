#!/usr/bin/env python3
"""Validate the single human-facing content collaboration packet."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


PHASES = ("research", "mother", "spoken")
REQUIRED_HEADINGS = {
    "research": ("## Topic Research Discussion", "## Current Synthesis"),
    "mother": ("## Topic Research Discussion", "## Current Synthesis", "## Mother Draft", "## Mother Draft Review"),
    "spoken": (
        "## Topic Research Discussion",
        "## Current Synthesis",
        "## Mother Draft",
        "## Mother Draft Review",
        "## Spoken Draft And Review",
    ),
}


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    values: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        match = re.match(r"^([a-z_]+):\s*(?:\"([^\"]*)\"|'([^']*)'|(.*))$", line)
        if match:
            values[match.group(1)] = next(value for value in match.groups()[1:] if value is not None).strip()
    return values


def validate(path: Path, phase: str) -> dict[str, object]:
    findings: list[str] = []
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        return {"status": "FAIL", "file": str(path), "phase": phase, "findings": [str(exc)]}

    frontmatter = parse_frontmatter(text)
    for key in ("topic_id", "discussion_status", "assistant_ready", "user_ready", "mother_review", "spoken_review"):
        if key not in frontmatter:
            findings.append(f"frontmatter missing {key}")

    for heading in REQUIRED_HEADINGS[phase]:
        if heading not in text:
            findings.append(f"missing heading: {heading}")

    discussion_closed = (
        frontmatter.get("discussion_status") == "closed"
        and frontmatter.get("assistant_ready", "").lower() == "true"
        and frontmatter.get("user_ready", "").lower() == "true"
    )
    if phase in ("mother", "spoken") and not discussion_closed:
        findings.append("research discussion requires discussion_status=closed with assistant_ready=true and user_ready=true")
    if phase == "spoken" and frontmatter.get("mother_review") != "approved":
        findings.append("mother_review must be approved before spoken review")
    if phase == "spoken" and frontmatter.get("spoken_review") != "approved":
        findings.append("spoken_review must be approved before execution")

    return {
        "status": "PASS" if not findings else "FAIL",
        "file": str(path),
        "phase": phase,
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--collaboration", type=Path, required=True)
    parser.add_argument("--phase", choices=PHASES, required=True)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    report = validate(args.collaboration, args.phase)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
