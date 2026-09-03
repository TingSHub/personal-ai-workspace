#!/usr/bin/env python3
"""Report optional commands and standard Skill search roots."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from common import dump_json, find_executable


def default_roots() -> list[Path]:
    roots = [Path.cwd() / ".agents/skills", Path.cwd() / ".codex/skills"]
    home = Path.home()
    roots.extend([home / ".agents/skills", home / ".codex/skills", home / ".claude/skills"])
    return roots


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", help="Write JSON to this path instead of stdout")
    args = parser.parse_args()
    commands = {}
    for name in ("git", "gh", "node", "npx", "skill-scanner"):
        path = find_executable(name)
        commands[name] = {"available": bool(path), "path": path}
    roots = []
    for root in default_roots():
        roots.append({"path": str(root.resolve()), "exists": root.is_dir()})
    result = {
        "platform": os.name,
        "python": os.sys.version.split()[0],
        "commands": commands,
        "search_roots": roots,
        "notes": [
            "Remote providers require network access.",
            "GitHub code search is enabled only when GitHub CLI is available and authenticated.",
            "Static inspection is best-effort and is not a security guarantee.",
        ],
    }
    dump_json(result, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
