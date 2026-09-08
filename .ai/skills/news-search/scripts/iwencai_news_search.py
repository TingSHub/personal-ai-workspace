#!/usr/bin/env python3
"""Query Iwencai SkillHub news search with workspace credentials."""
import argparse
import json
import os
import re
import secrets
import sys
from pathlib import Path

import requests


WORKSPACE_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_BASE_URL = "https://openapi.iwencai.com"


def load_workspace_env():
    env_file = WORKSPACE_ROOT / ".env"
    if not env_file.exists():
        return
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


def search_news(query, max_results=10, retry=False):
    load_workspace_env()
    api_key = os.environ.get("IWENCAI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("IWENCAI_API_KEY is not configured in the process or workspace .env")
    base_url = os.environ.get("IWENCAI_BASE_URL", DEFAULT_BASE_URL).rstrip("/")
    url = f"{base_url}/v1/comprehensive/search"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
        "X-Claw-Call-Type": "retry" if retry else "normal",
        "X-Claw-Skill-Id": "news-search",
        "X-Claw-Skill-Version": "1.0.0",
        "X-Claw-Plugin-Id": "none",
        "X-Claw-Plugin-Version": "none",
        "X-Claw-Trace-Id": secrets.token_hex(32),
    }
    payload = {
        "channels": ["news"],
        "app_id": "AIME_SKILL",
        "query": query,
        "page": "1",
        "limit": str(max_results),
    }
    response = requests.post(url, headers=headers, json=payload, timeout=(5, 30))
    response.raise_for_status()
    data = response.json()
    if data.get("status_code") not in (0, "0", None):
        raise RuntimeError(f"Iwencai status_code={data.get('status_code')}: {data.get('status_msg', '')}")
    results = []
    for item in data.get("data", [])[:max_results]:
        results.append(
            {
                "title": item.get("title", ""),
                "href": item.get("url", ""),
                "body": item.get("summary", ""),
                "source": "iwencai",
                "source_original": item.get("source_original", ""),
                "data_source": item.get("data_source", ""),
                "published_at": " ".join(str(x) for x in [item.get("publish_date", ""), item.get("publish_time", "")] if x),
                "traceability_type": item.get("traceability_type", ""),
            }
        )
    return {"query": query, "source": "iwencai", "total": data.get("total"), "results": results}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--max", type=int, default=10, dest="max_results")
    parser.add_argument("--retry", action="store_true")
    parser.add_argument("--format", choices=["json", "md"], default="json")
    args = parser.parse_args()
    try:
        result = search_news(args.query, max_results=args.max_results, retry=args.retry)
    except Exception as exc:
        print(f"Iwencai news search failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return 2
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"# Iwencai 新闻搜索：{args.query}\n")
        for index, item in enumerate(result["results"], 1):
            print(f"{index}. {item['title']}")
            print(f"   URL: {item['href']}")
            print(f"   来源: {item['source_original'] or item['data_source'] or '未知'} | 时间: {item['published_at'] or '未知'}")
            if item["body"]:
                print(f"   摘要: {item['body']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
