#!/usr/bin/env python3
"""Read-only workspace structure scan.

Usage: python3 scan_workspace_structure.py --root PATH [--json]
Exit codes: 0 = no blocker, 1 = blocker found, 2 = usage or scan error.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from pathlib import Path

SECRET_NAMES = {".env", "credentials", "credentials.json"}
SKIP_NAMES = {".git", ".omc", ".omx", "node_modules", "__pycache__"}
DATE_DIRECTORY = re.compile(r"^20\d{2}-\d{2}-\d{2}$")


def finding(level: str, code: str, path: Path, message: str) -> dict[str, str]:
    return {"level": level, "code": code, "path": path.as_posix(), "message": message}


def is_git_ignored(root: Path, path: Path) -> bool:
    result = subprocess.run(
        ["git", "check-ignore", "--quiet", "--", str(path)],
        cwd=root,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def tree_has_files(path: Path) -> bool:
    return any(candidate.is_file() for candidate in path.rglob("*"))


def scan(root: Path) -> list[dict[str, str]]:
    results: list[dict[str, str]] = []
    if not (root / "AGENTS.md").is_file() or not (root / ".ai").is_dir():
        raise ValueError("root is not a personal-ai-workspace checkout")

    legacy_projects = root / ".ai" / "projects"
    if legacy_projects.exists():
        results.append(finding("RECOMMENDED", "legacy-project-registry", legacy_projects.relative_to(root), "Legacy registry duplicates the canonical projects/ tree."))

    active_closeouts = root / ".ai" / "closeouts"
    if active_closeouts.is_dir():
        runs = sorted(path for path in active_closeouts.iterdir() if path.is_dir())
        if runs:
            results.append(finding("RECOMMENDED", "completed-closeout-runs", active_closeouts.relative_to(root), f"Contains {len(runs)} run directories; archive completed compact receipts."))

    projects_root = root / "projects"
    if projects_root.is_dir():
        for project in projects_root.iterdir():
            nested = project / "projects"
            if project.is_dir() and nested.exists():
                results.append(finding("RECOMMENDED", "nested-project-root", nested.relative_to(root), "A project contains another projects/ root; confirm whether this is an accidental duplicate hierarchy."))
            if not project.is_dir():
                continue
            for candidate in project.rglob("*"):
                rel_candidate = candidate.relative_to(root)
                if (
                    candidate.is_dir()
                    and DATE_DIRECTORY.fullmatch(candidate.name)
                    and not is_git_ignored(root, rel_candidate)
                    and not tree_has_files(candidate)
                ):
                    results.append(finding("RECOMMENDED", "empty-date-tree", rel_candidate, "Date-named directory tree contains no files; confirm deletion."))

    allowed_root_directories = {".agents", ".ai", ".claude", ".codex", ".git", "external", "projects"}
    for candidate in root.iterdir():
        if (
            candidate.is_dir()
            and candidate.name not in allowed_root_directories
            and not candidate.name.startswith(".venv")
            and not is_git_ignored(root, candidate.relative_to(root))
            and not tree_has_files(candidate)
        ):
            results.append(finding("OPTIONAL", "empty-root-directory", candidate.relative_to(root), "Root-level directory tree contains no files and has no registered workspace role."))

    for current, dirs, files in os.walk(root):
        current_path = Path(current)
        relative = current_path.relative_to(root)
        if relative.parts[:2] == (".claude", "skills"):
            dirs[:] = []
        else:
            dirs[:] = [
                name
                for name in dirs
                if name not in SKIP_NAMES
                and not name.startswith(".venv")
                and not is_git_ignored(root, (current_path / name).relative_to(root))
            ]
        for name in files:
            rel_path = (current_path / name).relative_to(root)
            if name in SECRET_NAMES and not is_git_ignored(root, rel_path):
                results.append(finding("BLOCKER", "secret-risk-file", rel_path, "Credential-shaped file exists; verify it is ignored and excluded from staging."))
    return sorted(results, key=lambda item: (item["level"], item["code"], item["path"]))


def main() -> int:
    parser = argparse.ArgumentParser(description="Read-only personal AI workspace structure scan")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        root = args.root.expanduser().resolve()
        results = scan(root)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 2
    if args.json:
        print(json.dumps({"root": str(root), "findings": results}, ensure_ascii=False, indent=2))
    else:
        for item in results:
            print(f"{item['level']}\t{item['code']}\t{item['path']}\t{item['message']}")
        print(f"SUMMARY\t{len(results)} finding(s)")
    return 1 if any(item["level"] == "BLOCKER" for item in results) else 0


if __name__ == "__main__":
    raise SystemExit(main())
