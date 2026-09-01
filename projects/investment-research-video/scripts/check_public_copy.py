#!/usr/bin/env python3
"""Fail if internal workflow/build metadata leaks into audience-visible HTML."""
import argparse
from pathlib import Path

FORBIDDEN = [
    "reference-podcast", "show-profile", "account-profile", "episode_id", "topic_id", "turn_id",
    "segments.json", "audio timeline", "音频时间轴", "workflow", "installed_ref",
    "source of truth", "metadata", "internal confidence", "evidence ledger",
]

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("html",type=Path); args=ap.parse_args()
    text=args.html.read_text(encoding="utf-8",errors="replace").lower()
    hits=[term for term in FORBIDDEN if term.lower() in text]
    if hits:
        print("FAIL: " + ", ".join(sorted(set(hits))))
        return 1
    print("PASS: no internal metadata terms found")
    return 0

if __name__ == "__main__": raise SystemExit(main())
