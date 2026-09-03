#!/usr/bin/env python3
"""Apply an explainable, safety-aware quality score to normalized candidates."""

from __future__ import annotations

import argparse
import math
import re
from datetime import datetime, timezone
from typing import Any

from common import dump_json, load_json


WEIGHTS = {
    "relevance": 30,
    "github_quality": 20,
    "provenance": 15,
    "maintenance": 10,
    "usage": 10,
    "community": 5,
    "docs_tests_portability": 10,
}


def tokens(value: str) -> set[str]:
    value = value.casefold()
    result = set(re.findall(r"[a-z0-9][a-z0-9_+.#-]*", value))
    for token in list(result):
        result.update(part for part in re.split(r"[_+.#-]+", token) if part)
    cjk = "".join(re.findall(r"[\u3400-\u9fff]", value))
    result.update(cjk)
    result.update(cjk[index:index + 2] for index in range(max(0, len(cjk) - 1)))
    return {item for item in result if item}


def overlap(query: str, candidate: str) -> float:
    wanted = tokens(query)
    if not wanted:
        return 0.0
    present = tokens(candidate)
    return len(wanted & present) / len(wanted)


def logarithmic(value: Any, practical_max: int) -> float:
    try:
        number = max(0, int(value or 0))
    except (TypeError, ValueError):
        number = 0
    return min(1.0, math.log1p(number) / math.log1p(practical_max))


def recency(updated_at: Any) -> float:
    if not updated_at:
        return 0.25
    try:
        value = str(updated_at).replace("Z", "+00:00")
        updated = datetime.fromisoformat(value)
        if updated.tzinfo is None:
            updated = updated.replace(tzinfo=timezone.utc)
        days = max(0.0, (datetime.now(timezone.utc) - updated).total_seconds() / 86400)
        return max(0.0, min(1.0, math.exp(-days / 730)))
    except ValueError:
        return 0.25


def score_candidate(query: str, item: dict[str, Any]) -> dict[str, Any]:
    audit = item.get("audit") if isinstance(item.get("audit"), dict) else None
    if audit and (not audit.get("spec_valid", False) or audit.get("risk_level") in {"high", "critical"} or not audit.get("install_allowed", False)):
        status = "blocked"
    elif audit and (audit.get("severity_counts") or {}).get("medium", 0) and not audit.get("medium_findings_accepted", False):
        status = "needs_review"
    elif not audit:
        status = "needs_audit"
    else:
        status = "eligible"

    name_match = overlap(query, str(item.get("name") or ""))
    full_match = overlap(query, " ".join(str(item.get(field) or "") for field in ("name", "description", "skill_path")))
    relevance = WEIGHTS["relevance"] * min(1.0, 0.65 * name_match + 0.35 * full_match)
    if relevance < 4 and status != "blocked":
        status = "low_relevance"

    stars = logarithmic(item.get("stars"), 50_000)
    forks = logarithmic(item.get("forks"), 5_000)
    has_github = "github.com/" in str(item.get("source_url") or "").casefold()
    github_quality = WEIGHTS["github_quality"] * min(1.0, 0.6 * stars + 0.15 * forks + (0.1 if has_github else 0) + (0.15 if not item.get("archived") else 0))

    evidence_count = len(item.get("evidence") or [])
    providers_count = len(item.get("providers") or ([item.get("provider")] if item.get("provider") else []))
    provenance_ratio = 0.3 * bool(item.get("source_url")) + 0.2 * bool(item.get("skill_path") is not None) + 0.2 * bool(item.get("commit")) + 0.2 * min(1, evidence_count / 2) + 0.1 * min(1, providers_count / 2)
    provenance = WEIGHTS["provenance"] * provenance_ratio

    maintenance = WEIGHTS["maintenance"] * recency(item.get("updated_at"))
    usage = WEIGHTS["usage"] * logarithmic(item.get("installs"), 1_000_000)
    community = WEIGHTS["community"] * min(1.0, logarithmic(item.get("community_mentions"), 100) * 0.6 + min(1.0, float(item.get("independent_mentions") or 0) / 3) * 0.4)

    docs_ratio = 0.2 * bool(item.get("description")) + 0.2 * bool(item.get("has_examples")) + 0.2 * bool(item.get("has_tests")) + 0.2 * bool(audit and audit.get("spec_valid")) + 0.2 * (not item.get("compatibility_exception", False))
    docs = WEIGHTS["docs_tests_portability"] * docs_ratio

    components = {
        "relevance": round(relevance, 2),
        "github_quality": round(github_quality, 2),
        "provenance": round(provenance, 2),
        "maintenance": round(maintenance, 2),
        "usage": round(usage, 2),
        "community": round(community, 2),
        "docs_tests_portability": round(docs, 2),
    }
    result = dict(item)
    result["score"] = round(sum(components.values()), 1)
    result["score_components"] = components
    result["recommendation_status"] = status
    result["eligible_for_install"] = status == "eligible"
    result["score_explanation"] = [
        f"relevance {components['relevance']}/{WEIGHTS['relevance']}",
        f"project quality {components['github_quality']}/{WEIGHTS['github_quality']}",
        f"provenance {components['provenance']}/{WEIGHTS['provenance']}",
    ]
    if status == "needs_audit":
        result["score_explanation"].append("static audit required before installation")
    elif status == "needs_review":
        result["score_explanation"].append("medium findings require explicit review before installation")
    elif status == "low_relevance":
        result["score_explanation"].append("filtered because relevance evidence is too weak")
    elif status == "blocked":
        result["score_explanation"].append("blocked by structure or security gate")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--query", required=True)
    parser.add_argument("--input", required=True, help="JSON from search_skills.py or a candidate array")
    parser.add_argument("--output")
    parser.add_argument("--top", type=int, default=10)
    parser.add_argument("--include-low-relevance", action="store_true", help="Keep candidates that fail the relevance gate")
    args = parser.parse_args()
    payload = load_json(args.input)
    candidates = payload.get("candidates", []) if isinstance(payload, dict) else payload
    ranked = [score_candidate(args.query, item) for item in candidates]
    if not args.include_low_relevance:
        ranked = [item for item in ranked if item["recommendation_status"] != "low_relevance"]
    status_order = {"eligible": 0, "needs_review": 1, "needs_audit": 2, "blocked": 3, "low_relevance": 4}
    ranked.sort(key=lambda item: (status_order.get(item["recommendation_status"], 9), -item["score"], str(item.get("name") or "")))
    result = {
        "query": args.query,
        "weights": WEIGHTS,
        "count": min(len(ranked), args.top),
        "candidates": ranked[:args.top],
        "warning": "Popularity and score never override the security gate.",
    }
    dump_json(result, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
