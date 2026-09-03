#!/usr/bin/env python3
"""Search local and remote Agent Skill sources and emit normalized JSON."""

from __future__ import annotations

import argparse
import json
import subprocess
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

from common import dump_json, find_executable, merge_candidates, parse_frontmatter


USER_AGENT = "open-skill-finder/1.0 (+https://github.com/30bewater/open-skill-finder)"


def http_json(url: str, timeout: int) -> Any:
    request = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def default_local_roots() -> list[Path]:
    home = Path.home()
    return [
        Path.cwd() / ".agents/skills",
        Path.cwd() / ".codex/skills",
        home / ".agents/skills",
        home / ".codex/skills",
        home / ".claude/skills",
    ]


def text_matches(query: str, *values: str) -> bool:
    terms = [term.casefold() for term in query.split() if term.strip()]
    haystack = " ".join(values).casefold()
    return not terms or all(term in haystack for term in terms) or any(term in haystack for term in terms)


def search_local(query: str, roots: list[Path], limit: int) -> list[dict[str, Any]]:
    results: list[dict[str, Any]] = []
    seen_files: set[str] = set()
    for root in roots:
        if not root.is_dir():
            continue
        for skill_file in root.glob("*/SKILL.md"):
            resolved = str(skill_file.resolve()).casefold()
            if resolved in seen_files:
                continue
            seen_files.add(resolved)
            try:
                text = skill_file.read_text(encoding="utf-8", errors="replace")
                metadata = parse_frontmatter(text)
            except OSError:
                continue
            name = metadata.get("name") or skill_file.parent.name
            description = metadata.get("description", "")
            if not text_matches(query, name, description, text[:8000]):
                continue
            results.append({
                "id": f"local:{skill_file.parent.resolve()}",
                "name": name,
                "description": description,
                "source": "local",
                "source_url": "",
                "skill_path": skill_file.parent.name,
                "local_path": str(skill_file.parent.resolve()),
                "provider": "local",
                "installed": True,
                "evidence": [{"type": "local_manifest", "value": str(skill_file.resolve())}],
            })
            if len(results) >= limit:
                return results
    return results


def search_skills_sh(query: str, limit: int, timeout: int) -> list[dict[str, Any]]:
    params = urllib.parse.urlencode({"q": query, "limit": limit})
    payload = http_json(f"https://skills.sh/api/search?{params}", timeout)
    rows = payload.get("skills", []) if isinstance(payload, dict) else []
    results = []
    for rank, row in enumerate(rows):
        source = str(row.get("source") or "")
        skill_id = str(row.get("id") or row.get("name") or "")
        source_url = source if source.startswith(("http://", "https://")) else (
            f"https://github.com/{source.strip('/')}" if "/" in source else ""
        )
        results.append({
            "id": f"skills.sh:{skill_id}",
            "name": row.get("name") or skill_id.rsplit("/", 1)[-1],
            "description": row.get("description") or "",
            "source": source,
            "source_url": source_url,
            "listing_url": f"https://skills.sh/{skill_id.strip('/')}",
            "skill_path": row.get("skillPath") or row.get("path") or skill_id.rsplit("/", 1)[-1],
            "provider": "skills.sh",
            "provider_rank": rank + 1,
            "installs": row.get("installs") or 0,
            "evidence": [{"type": "registry_listing", "value": f"https://skills.sh/{skill_id.strip('/')}"}],
        })
    return results


def run_gh(arguments: list[str], timeout: int) -> Any:
    gh = find_executable("gh")
    if not gh:
        raise RuntimeError("GitHub CLI is not available")
    completed = subprocess.run(
        [gh, *arguments], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout
    )
    if completed.returncode != 0:
        message = completed.stderr.strip() or completed.stdout.strip() or "GitHub CLI failed"
        raise RuntimeError(message)
    return json.loads(completed.stdout or "null")


def github_repo_metadata(repo: str, timeout: int) -> dict[str, Any]:
    fields = "nameWithOwner,url,description,stargazerCount,forkCount,updatedAt,isArchived,licenseInfo"
    try:
        data = run_gh(["repo", "view", repo, "--json", fields], timeout)
    except Exception:
        return {}
    license_info = data.get("licenseInfo") or {}
    return {
        "description": data.get("description") or "",
        "stars": data.get("stargazerCount") or 0,
        "forks": data.get("forkCount") or 0,
        "updated_at": data.get("updatedAt"),
        "archived": data.get("isArchived", False),
        "license": license_info.get("spdxId") or license_info.get("name") or "",
    }


def search_github(query: str, limit: int, timeout: int, enrich: int) -> list[dict[str, Any]]:
    rows = run_gh(
        ["search", "code", query, "--filename", "SKILL.md", "--limit", str(limit), "--json", "path,repository,url"],
        timeout,
    )
    results = []
    metadata_cache: dict[str, dict[str, Any]] = {}
    for rank, row in enumerate(rows or []):
        repository = row.get("repository") or {}
        repo = repository.get("nameWithOwner") or ""
        path = row.get("path") or "SKILL.md"
        skill_path = str(Path(path).parent).replace("\\", "/")
        if skill_path == ".":
            skill_path = ""
        metadata: dict[str, Any] = {}
        if repo and rank < enrich:
            metadata = metadata_cache.setdefault(repo, github_repo_metadata(repo, timeout))
        results.append({
            "id": f"github:{repo}:{skill_path or 'root'}",
            "name": Path(skill_path).name if skill_path else repo.rsplit("/", 1)[-1],
            "description": metadata.get("description", ""),
            "source": repo,
            "source_url": repository.get("url") or (f"https://github.com/{repo}" if repo else ""),
            "listing_url": row.get("url") or "",
            "skill_path": skill_path,
            "provider": "github",
            "provider_rank": rank + 1,
            "stars": metadata.get("stars", 0),
            "forks": metadata.get("forks", 0),
            "updated_at": metadata.get("updated_at"),
            "archived": metadata.get("archived", False),
            "license": metadata.get("license", ""),
            "evidence": [{"type": "github_code_result", "value": row.get("url") or ""}],
        })
    return results


def search_registry(spec: str, query: str, limit: int, timeout: int) -> list[dict[str, Any]]:
    if "=" not in spec:
        raise ValueError("Registry must use name=https://example/api/search syntax")
    name, base_url = spec.split("=", 1)
    parsed = urllib.parse.urlsplit(base_url)
    existing = urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
    query_string = urllib.parse.urlencode([*existing, ("q", query), ("limit", str(limit))])
    url = urllib.parse.urlunsplit((parsed.scheme, parsed.netloc, parsed.path, query_string, parsed.fragment))
    payload = http_json(url, timeout)
    if isinstance(payload, list):
        rows = payload
    elif isinstance(payload, dict):
        rows = payload.get("skills") or payload.get("results") or payload.get("items") or []
    else:
        rows = []
    results = []
    for rank, row in enumerate(rows[:limit]):
        if not isinstance(row, dict):
            continue
        source_url = row.get("source_url") or row.get("repository") or row.get("url") or ""
        results.append({
            "id": f"registry:{name}:{row.get('id') or row.get('name') or rank}",
            "name": row.get("name") or row.get("slug") or "unknown",
            "description": row.get("description") or row.get("summary") or "",
            "source": row.get("source") or source_url,
            "source_url": source_url,
            "listing_url": row.get("listing_url") or row.get("url") or "",
            "skill_path": row.get("skill_path") or row.get("path") or row.get("name") or "",
            "provider": name,
            "provider_rank": rank + 1,
            "installs": row.get("installs") or row.get("downloads") or 0,
            "stars": row.get("stars") or 0,
            "forks": row.get("forks") or 0,
            "updated_at": row.get("updated_at") or row.get("updatedAt"),
            "license": row.get("license") or "",
            "evidence": [{"type": "custom_registry", "value": url}],
        })
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", help="Capability or Skill to search for")
    parser.add_argument("--limit", type=int, default=20, help="Maximum results per provider")
    parser.add_argument("--timeout", type=int, default=20, help="Network/command timeout in seconds")
    parser.add_argument("--local-root", action="append", default=[], help="Additional local Skill root")
    parser.add_argument("--registry", action="append", default=[], help="Custom JSON registry as name=URL")
    parser.add_argument("--no-local", action="store_true")
    parser.add_argument("--no-skills-sh", action="store_true")
    parser.add_argument("--no-github", action="store_true")
    parser.add_argument("--github-enrich", type=int, default=5, help="Repositories to enrich with metadata")
    parser.add_argument("--output", help="Write JSON to this path")
    args = parser.parse_args()

    candidates: list[dict[str, Any]] = []
    errors: list[dict[str, str]] = []
    providers: list[str] = []

    if not args.no_local:
        providers.append("local")
        roots = default_local_roots() + [Path(path).expanduser() for path in args.local_root]
        candidates.extend(search_local(args.query, roots, args.limit))
    if not args.no_skills_sh:
        providers.append("skills.sh")
        try:
            candidates.extend(search_skills_sh(args.query, args.limit, args.timeout))
        except (OSError, ValueError, urllib.error.URLError) as exc:
            errors.append({"provider": "skills.sh", "error": str(exc)})
    if not args.no_github:
        providers.append("github")
        try:
            candidates.extend(search_github(args.query, args.limit, args.timeout, args.github_enrich))
        except (RuntimeError, OSError, subprocess.SubprocessError, ValueError) as exc:
            errors.append({"provider": "github", "error": str(exc)})
    for spec in args.registry:
        provider = spec.split("=", 1)[0]
        providers.append(provider)
        try:
            candidates.extend(search_registry(spec, args.query, args.limit, args.timeout))
        except (OSError, ValueError, urllib.error.URLError) as exc:
            errors.append({"provider": provider, "error": str(exc)})

    result = {
        "query": args.query,
        "providers_attempted": providers,
        "errors": errors,
        "count": 0,
        "candidates": merge_candidates(candidates),
    }
    result["count"] = len(result["candidates"])
    dump_json(result, args.output)
    return 0 if result["candidates"] or not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
