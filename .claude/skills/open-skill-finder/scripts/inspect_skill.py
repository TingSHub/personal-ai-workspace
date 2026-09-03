#!/usr/bin/env python3
"""Validate an Agent Skill directory and perform best-effort static inspection."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from common import dump_json, is_probably_text, parse_frontmatter


SEVERITY_ORDER = {"info": 0, "low": 1, "medium": 2, "high": 3, "critical": 4}
ALLOWED_TOP_LEVEL = {"SKILL.md", "agents", "scripts", "references", "assets", "LICENSE", "LICENSE.md", "NOTICE"}
PERMISSIVE_LICENSES = {"MIT", "APACHE-2.0", "BSD-2-CLAUSE", "BSD-3-CLAUSE", "ISC", "CC0-1.0", "UNLICENSE"}

RULES: list[tuple[str, str, re.Pattern[str], str]] = [
    ("instruction_hijack", "critical", re.compile(r"ignore\s+(?:all\s+)?previous\s+instructions|system\s+prompt|developer\s+message", re.I), "Possible instruction hijacking text"),
    ("destructive_delete", "critical", re.compile(r"\b(?:rm\s+-rf|Remove-Item\b[^\n]*(?:-Recurse|-Force)|rmdir\s+/s)\b", re.I), "Potentially destructive recursive deletion"),
    ("credential_access", "critical", re.compile(r"(?:\.ssh[/\\]|\.aws[/\\](?:credentials|config)|\.config[/\\]gh[/\\]hosts\.yml|id_rsa|GITHUB_TOKEN|OPENAI_API_KEY)", re.I), "Sensitive credential or secret access"),
    ("dynamic_execution", "high", re.compile(r"\b(?:eval|exec)\s*\(|shell\s*=\s*True|Invoke-Expression\b", re.I), "Dynamic or shell command execution"),
    ("remote_pipe_shell", "high", re.compile(r"(?:curl|wget|Invoke-WebRequest)[^\n|]{0,240}\|\s*(?:sh|bash|zsh|powershell|pwsh)\b", re.I), "Remote content piped into a shell"),
    ("lifecycle_hook", "high", re.compile(r'"(?:preinstall|install|postinstall|prepare)"\s*:', re.I), "Package lifecycle hook"),
    ("broad_config_write", "high", re.compile(r"(?:\.bashrc|\.zshrc|PowerShell_profile|settings\.json|\.gitconfig)", re.I), "Possible write or instruction involving global configuration"),
    ("network_access", "medium", re.compile(r"\b(?:curl|wget|Invoke-WebRequest|requests\.(?:get|post)|urllib\.request|fetch\s*\(|axios\.)", re.I), "Network access or download"),
    ("package_install", "medium", re.compile(r"\b(?:pipx?|npm|pnpm|yarn|brew|apt(?:-get)?|winget|choco)\s+(?:install|add)\b", re.I), "Package installation instruction"),
    ("long_base64", "medium", re.compile(r"[A-Za-z0-9+/]{500,}={0,2}"), "Large base64-like payload"),
    ("hidden_unicode", "medium", re.compile(r"[\u200b-\u200f\u202a-\u202e\u2060-\u2069\ufeff]"), "Invisible or bidirectional control character"),
    ("external_url", "info", re.compile(r"https?://[^\s<>\])}\"']+", re.I), "External URL"),
]


def add_finding(findings: list[dict[str, Any]], rule: str, severity: str, message: str, path: Path | str, line: int | None = None, evidence: str = "") -> None:
    finding: dict[str, Any] = {"rule": rule, "severity": severity, "message": message, "path": str(path)}
    if line is not None:
        finding["line"] = line
    if evidence:
        finding["evidence"] = evidence[:240]
    findings.append(finding)


def line_number(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def find_license(root: Path) -> tuple[str, str]:
    current = root
    for _ in range(6):
        for name in ("LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING"):
            candidate = current / name
            if candidate.is_file():
                content = candidate.read_text(encoding="utf-8", errors="replace")[:8000]
                upper = content.upper()
                if "MIT LICENSE" in upper or "PERMISSION IS HEREBY GRANTED" in upper:
                    return "MIT", str(candidate)
                if "APACHE LICENSE" in upper and "VERSION 2.0" in upper:
                    return "Apache-2.0", str(candidate)
                if "GNU GENERAL PUBLIC LICENSE" in upper:
                    version = "3.0" if "VERSION 3" in upper else "unknown"
                    return f"GPL-{version}", str(candidate)
                if "BSD" in upper:
                    return "BSD", str(candidate)
                return "detected-unclassified", str(candidate)
        if (current / ".git").exists() or current.parent == current:
            break
        current = current.parent
    return "missing", ""


def inspect_package_json(path: Path, findings: list[dict[str, Any]]) -> None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        add_finding(findings, "invalid_package_json", "medium", f"Cannot parse package.json: {exc}", path)
        return
    scripts = payload.get("scripts") or {}
    for hook in ("preinstall", "install", "postinstall", "prepare"):
        if hook in scripts:
            add_finding(findings, "lifecycle_hook", "high", f"Package lifecycle hook: {hook}", path, evidence=str(scripts[hook]))


def inspect(root: Path, max_file_bytes: int) -> dict[str, Any]:
    root = root.resolve()
    findings: list[dict[str, Any]] = []
    files: list[dict[str, Any]] = []
    manifest = root / "SKILL.md"
    metadata: dict[str, str] = {}
    spec_valid = True

    if not root.is_dir():
        add_finding(findings, "missing_directory", "critical", "Skill directory does not exist", root)
        spec_valid = False
    elif not manifest.is_file():
        add_finding(findings, "missing_manifest", "critical", "SKILL.md is required", manifest)
        spec_valid = False
    else:
        text = manifest.read_text(encoding="utf-8", errors="replace")
        metadata = parse_frontmatter(text)
        if not metadata:
            add_finding(findings, "invalid_frontmatter", "high", "SKILL.md must start with YAML frontmatter", manifest)
            spec_valid = False
        for field in ("name", "description"):
            if not metadata.get(field):
                add_finding(findings, f"missing_{field}", "high", f"Frontmatter field '{field}' is required", manifest)
                spec_valid = False
        if metadata.get("name") and metadata["name"] != root.name:
            add_finding(findings, "name_path_mismatch", "low", "Skill name differs from its directory name", manifest, evidence=f"{metadata['name']} != {root.name}")
        extra = sorted(set(metadata) - {"name", "description", "license", "compatibility", "metadata", "allowed-tools"})
        if extra:
            add_finding(findings, "unusual_frontmatter", "low", "Unrecognized frontmatter fields", manifest, evidence=", ".join(extra))

    if root.is_dir():
        for child in root.iterdir():
            if child.name.startswith(".") and child.name not in {".gitignore"}:
                add_finding(findings, "hidden_top_level", "medium", "Hidden top-level entry requires review", child)
            if child.name not in ALLOWED_TOP_LEVEL and not child.name.startswith("."):
                add_finding(findings, "unusual_top_level", "low", "Unusual top-level entry", child)

        for path in root.rglob("*"):
            relative = path.relative_to(root)
            if ".git" in relative.parts:
                continue
            if path.is_symlink():
                try:
                    resolved = path.resolve()
                    resolved.relative_to(root)
                    severity = "low"
                    message = "Internal symlink requires review"
                except (OSError, ValueError):
                    severity = "high"
                    message = "Symlink escapes the Skill directory"
                add_finding(findings, "symlink", severity, message, relative)
                continue
            if not path.is_file():
                continue
            try:
                size = path.stat().st_size
                digest = hashlib.sha256(path.read_bytes()).hexdigest()
            except OSError as exc:
                add_finding(findings, "unreadable_file", "medium", f"Cannot read file: {exc}", relative)
                continue
            files.append({"path": str(relative).replace("\\", "/"), "bytes": size, "sha256": digest})
            if path.name == "package.json":
                inspect_package_json(path, findings)
            if size > max_file_bytes:
                add_finding(findings, "large_file", "medium", "File exceeds static inspection size limit", relative, evidence=str(size))
                continue
            if not is_probably_text(path):
                if size > 0:
                    add_finding(findings, "opaque_file", "medium", "Non-text file requires manual review", relative, evidence=str(size))
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            for rule, severity, pattern, message in RULES:
                matches = list(pattern.finditer(text))
                for match in matches[:10]:
                    add_finding(
                        findings, rule, severity, message, relative,
                        line_number(text, match.start()), match.group(0).replace("\n", " "),
                    )
                if len(matches) > 10:
                    add_finding(findings, f"{rule}_truncated", severity, f"{len(matches) - 10} additional matches omitted", relative)

    license_id, license_path = find_license(root) if root.is_dir() else ("missing", "")
    if license_id == "missing":
        add_finding(findings, "license_missing", "low", "No repository or Skill license found", root)
    elif license_id.upper() not in PERMISSIVE_LICENSES and not license_id.upper().startswith("BSD"):
        add_finding(findings, "license_review", "low", "License may require redistribution review", license_path, evidence=license_id)

    counts = Counter(finding["severity"] for finding in findings)
    actionable = [finding for finding in findings if finding["severity"] != "info"]
    risk_level = max((finding["severity"] for finding in actionable), key=lambda value: SEVERITY_ORDER[value], default="low")
    install_allowed = spec_valid and not any(SEVERITY_ORDER[finding["severity"]] >= SEVERITY_ORDER["high"] for finding in findings)
    return {
        "skill_root": str(root),
        "metadata": metadata,
        "spec_valid": spec_valid,
        "license": {"id": license_id, "path": license_path, "needs_display": license_id == "missing" or bool([f for f in findings if f["rule"] == "license_review"])},
        "file_count": len(files),
        "total_bytes": sum(item["bytes"] for item in files),
        "files": files,
        "risk_level": risk_level,
        "install_allowed": install_allowed,
        "severity_counts": {level: counts.get(level, 0) for level in SEVERITY_ORDER},
        "findings": findings,
        "disclaimer": "Best-effort static inspection only; a clean result is not a security guarantee.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("skill_directory")
    parser.add_argument("--max-file-bytes", type=int, default=2_000_000)
    parser.add_argument("--fail-on", choices=("low", "medium", "high", "critical"), default="high")
    parser.add_argument("--output")
    args = parser.parse_args()
    report = inspect(Path(args.skill_directory), args.max_file_bytes)
    dump_json(report, args.output)
    threshold = SEVERITY_ORDER[args.fail_on]
    failed = any(SEVERITY_ORDER[item["severity"]] >= threshold for item in report["findings"])
    return 2 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
