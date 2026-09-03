#!/usr/bin/env python3
"""Render ranked Skill candidates as compact Chinese or English Markdown cards."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from common import load_json


LABELS = {
    "zh": {
        "skill": "Skill", "score": "匹配度", "source": "来源", "updated": "最近更新",
        "security": "安全风险", "dependencies": "额外依赖", "reason": "为什么推荐",
        "notes": "注意事项", "compatibility": "兼容性", "license": "许可证",
        "unknown": "未知", "none": "未声明", "audit": "尚未完成静态审查，不能直接安装",
        "eligible": "已通过所提供的静态审查", "review": "存在中等风险项，需人工复核并明确接受",
        "blocked": "已被结构或安全门禁拦截",
    },
    "en": {
        "skill": "Skill", "score": "Match", "source": "Source", "updated": "Last update",
        "security": "Security", "dependencies": "Extra dependencies", "reason": "Why it fits",
        "notes": "Caveats", "compatibility": "Compatibility", "license": "License",
        "unknown": "Unknown", "none": "Not declared", "audit": "Static audit not completed; do not install yet",
        "eligible": "Passed the supplied static audit", "review": "Medium-risk findings require review and explicit acceptance",
        "blocked": "Blocked by the structure or security gate",
    },
}


def first_reason(item: dict[str, Any], lang: str) -> str:
    if item.get("why_recommended"):
        return str(item["why_recommended"])
    description = str(item.get("description") or "").strip()
    if description:
        return description
    return "名称和检索词相关，需阅读原始 SKILL.md 复核。" if lang == "zh" else "The name matches the query; inspect the original SKILL.md to confirm."


def security_text(item: dict[str, Any], labels: dict[str, str]) -> str:
    status = item.get("recommendation_status")
    if status == "eligible":
        audit = item.get("audit") or {}
        return f"{labels['eligible']}（{audit.get('risk_level', 'low')}）"
    if status == "needs_review":
        return labels["review"]
    if status == "blocked":
        return labels["blocked"]
    return labels["audit"]


def render(item: dict[str, Any], lang: str) -> str:
    labels = LABELS[lang]
    source = item.get("source_url") or item.get("source") or labels["unknown"]
    path = item.get("skill_path")
    if path:
        source = f"{source} · `{path}`"
    dependencies = item.get("dependencies") or labels["none"]
    notes = item.get("limitations") or item.get("notes")
    if not notes:
        notes = "安装前仍应人工复核外部依赖和权限。" if lang == "zh" else "Review external dependencies and permissions before installation."
    lines = [
        f"### {labels['skill']}：{item.get('name') or labels['unknown']}",
        "",
        f"- {labels['score']}：{item.get('score', 0)}/100",
        f"- {labels['source']}：{source}",
        f"- {labels['updated']}：{item.get('updated_at') or labels['unknown']}",
        f"- {labels['security']}：{security_text(item, labels)}",
        f"- {labels['dependencies']}：{dependencies}",
        f"- {labels['reason']}：{first_reason(item, lang)}",
        f"- {labels['notes']}：{notes}",
    ]
    if item.get("compatibility_exception"):
        lines.append(f"- {labels['compatibility']}：{item.get('compatibility') or labels['unknown']}")
    license_info = (item.get("audit") or {}).get("license") or {}
    license_value = license_info.get("id") or item.get("license")
    if license_info.get("needs_display") or str(license_value).casefold() in {"", "missing", "unknown", "none"}:
        lines.append(f"- {labels['license']}：{license_value or labels['unknown']}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True)
    parser.add_argument("--lang", choices=("zh", "en"), default="zh")
    parser.add_argument("--output")
    parser.add_argument("--top", type=int, default=5)
    args = parser.parse_args()
    payload = load_json(args.input)
    candidates = payload.get("candidates", []) if isinstance(payload, dict) else payload
    markdown = "\n\n".join(render(item, args.lang) for item in candidates[:args.top]) + "\n"
    if args.output:
        Path(args.output).write_text(markdown, encoding="utf-8")
    else:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        print(markdown, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
