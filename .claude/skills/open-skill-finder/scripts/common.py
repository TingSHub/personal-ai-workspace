"""Shared, dependency-free helpers for Open Skill Finder."""

from __future__ import annotations

import json
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Any, Iterable


TEXT_EXTENSIONS = {
    ".md", ".txt", ".json", ".jsonc", ".yaml", ".yml", ".toml", ".ini",
    ".cfg", ".conf", ".py", ".js", ".mjs", ".cjs", ".ts", ".tsx", ".jsx",
    ".sh", ".bash", ".zsh", ".fish", ".ps1", ".bat", ".cmd", ".rb", ".go",
    ".rs", ".java", ".xml", ".html", ".css", ".sql", ".env", ".properties",
}


def find_executable(name: str) -> str | None:
    found = shutil.which(name)
    if found:
        return found
    if os.name == "nt":
        known = {
            "gh": [Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "GitHub CLI/gh.exe"],
            "git": [Path(os.environ.get("ProgramFiles", "C:/Program Files")) / "Git/cmd/git.exe"],
        }
        for candidate in known.get(name, []):
            if candidate.is_file():
                return str(candidate)
    return None


def load_json(path: str | Path) -> Any:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def dump_json(data: Any, path: str | Path | None = None) -> None:
    text = json.dumps(data, ensure_ascii=False, indent=2)
    if path:
        Path(path).write_text(text + "\n", encoding="utf-8")
    else:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        print(text)


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.lstrip("\ufeff").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}
    result: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return result
        match = re.match(r"^([A-Za-z0-9_-]+):\s*(.*)$", line)
        if match:
            value = match.group(2).strip()
            if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
                value = value[1:-1]
            result[match.group(1)] = value
    return {}


def canonical_source(source: str | None) -> str:
    if not source:
        return ""
    value = source.strip().replace("\\", "/").rstrip("/")
    value = re.sub(r"\.git$", "", value, flags=re.IGNORECASE)
    value = re.sub(r"^git@github\.com:", "https://github.com/", value, flags=re.IGNORECASE)
    value = re.sub(r"^https?://(?:www\.)?github\.com/", "github.com/", value, flags=re.IGNORECASE)
    return value.lower()


def candidate_key(candidate: dict[str, Any]) -> str:
    source = canonical_source(candidate.get("source_url") or candidate.get("source"))
    path = str(candidate.get("skill_path") or candidate.get("name") or "").replace("\\", "/").strip("/").lower()
    return f"{source}::{path}"


def merge_candidates(candidates: Iterable[dict[str, Any]]) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for item in candidates:
        key = candidate_key(item)
        if not key.strip(":"):
            continue
        if key not in merged:
            merged[key] = dict(item)
            merged[key]["evidence"] = list(item.get("evidence") or [])
            continue
        current = merged[key]
        for field, value in item.items():
            if field == "evidence":
                for evidence in value or []:
                    if evidence not in current["evidence"]:
                        current["evidence"].append(evidence)
            elif value not in (None, "", [], {}) and current.get(field) in (None, "", [], {}):
                current[field] = value
        providers = set(current.get("providers") or [current.get("provider")])
        providers.add(item.get("provider"))
        current["providers"] = sorted(p for p in providers if p)
    return list(merged.values())


def is_probably_text(path: Path) -> bool:
    return path.suffix.lower() in TEXT_EXTENSIONS or path.name.lower() in {
        "skill.md", "license", "notice", "dockerfile", "makefile", ".gitignore",
    }
