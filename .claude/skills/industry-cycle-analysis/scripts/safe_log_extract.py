#!/usr/bin/env python3
"""Extract a bounded slice from logs or JSONL files without loading everything."""

from __future__ import annotations

import argparse
import collections
import pathlib
import re
import sys


def read_tail(path: pathlib.Path, line_count: int) -> list[str]:
    tail: collections.deque[str] = collections.deque(maxlen=line_count)
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        for line in handle:
            tail.append(line.rstrip("\n"))
    return list(tail)


def main() -> int:
    parser = argparse.ArgumentParser(description="Safely extract recent or filtered log lines.")
    parser.add_argument("path", help="Log, JSONL, or text file")
    parser.add_argument("--tail", type=int, default=120, help="Maximum recent lines to read")
    parser.add_argument("--filter", nargs="*", default=[], help="Case-insensitive terms to keep")
    args = parser.parse_args()

    path = pathlib.Path(args.path).resolve()
    if not path.exists():
        print(f"File does not exist: {path}", file=sys.stderr)
        return 2
    if args.tail < 1 or args.tail > 500:
        print("--tail must be between 1 and 500", file=sys.stderr)
        return 2

    lines = read_tail(path, args.tail)

    if args.filter:
        pattern = re.compile("|".join(re.escape(term) for term in args.filter), re.IGNORECASE)
        lines = [line for line in lines if pattern.search(line)]

    for line in lines:
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
