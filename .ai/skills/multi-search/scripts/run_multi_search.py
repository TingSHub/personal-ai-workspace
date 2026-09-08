#!/usr/bin/env python3
"""Run the installed multi-search implementation with workspace .env loaded."""
import argparse
import os
import re
import sys
from pathlib import Path


WORKSPACE_ROOT = Path(__file__).resolve().parents[4]
INSTALLED_ROOT = WORKSPACE_ROOT / ".claude/skills/multi-search"


def load_workspace_env():
    """Load simple KEY=value entries without printing or persisting secret values."""
    env_file = WORKSPACE_ROOT / ".env"
    if not env_file.exists():
        return False
    pattern = re.compile(r"^(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)=(.*)$")
    for raw in env_file.read_text(encoding="utf-8").splitlines():
        match = pattern.match(raw.strip())
        if not match:
            continue
        key, value = match.groups()
        value = value.strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        os.environ.setdefault(key, value)
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query", nargs="?", help="search query")
    parser.add_argument("--max-results", type=int, default=5)
    parser.add_argument("--balanced", action="store_true", help="disable Tavily-first quality routing")
    parser.add_argument("--force-network-check", action="store_true")
    parser.add_argument("--status", action="store_true")
    args = parser.parse_args()

    if not INSTALLED_ROOT.exists():
        raise SystemExit(f"installed multi-search not found: {INSTALLED_ROOT}")
    load_workspace_env()
    sys.path.insert(0, str(INSTALLED_ROOT))
    from multi_search import get_status, search

    if args.status:
        status = get_status(force_network_check=args.force_network_check)
        print("TAVILY_API_KEY configured:", bool(os.environ.get("TAVILY_API_KEY")))
        print("BING_API_KEY configured:", bool(os.environ.get("BING_API_KEY")))
        return 0 if status else 1
    if not args.query:
        parser.error("query is required unless --status is used")
    search(
        args.query,
        max_results=args.max_results,
        prefer_quality=not args.balanced,
        force_network_check=args.force_network_check,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
