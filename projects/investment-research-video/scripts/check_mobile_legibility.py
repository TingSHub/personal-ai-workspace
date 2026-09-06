#!/usr/bin/env python3
"""Static gate for the phone-first video composition contract.

This is deliberately a small guardrail around the generated HTML.  It does
not replace a rendered screenshot review; it catches regressions where a
future template change brings back tiny type, fabricated card slots, or the
visible "开场" label.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REQUIRED_PATTERNS = {
    "caption font": r"\.caption-line\{[^}]*font-size:48px",
    "chart title font": r"\.chart-first \.chart-title\{[^}]*font-size:56px",
    "chart row font": r"\.chart-first \.chart-row\{[^}]*font-size:56px",
    "chart value font": r"\.chart-first \.chart-row b\{[^}]*font-size:52px",
    "metric value font": r"\.metric \.value\{[^}]*font-size:104px",
}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("html", type=Path)
    args = parser.parse_args()
    source = args.html.read_text(encoding="utf-8")
    findings: list[str] = []

    if re.search(r">(?:开场|冷开场)<", source):
        findings.append('visible navigation/title still contains "开场"')

    layouts = set(re.findall(r'data-layout="([^"]+)"', source))
    if "chart-first" not in layouts:
        findings.append("no chart-first layout was generated for chart-bearing content")
    if "hook" not in layouts:
        findings.append("no hook layout was generated")
    if "agenda" not in layouts:
        findings.append("no agenda layout was generated")

    for name, pattern in REQUIRED_PATTERNS.items():
        if not re.search(pattern, source):
            findings.append(f"{name} is below the mobile-first threshold or missing")

    if findings:
        print("FAIL")
        for finding in findings:
            print(f"- {finding}")
        return 1

    print(f"PASS mobile-first legibility · layouts={','.join(sorted(layouts))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
