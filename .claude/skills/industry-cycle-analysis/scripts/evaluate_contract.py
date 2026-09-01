#!/usr/bin/env python3
"""Compare v1.6 report-contract assertions against baseline and candidate corpora."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from validate_report import extract_node_blocks, markdown_tables, section, table_rows


PREFIXES = ("03_", "12_", "16_", "13_")


def find_report(root: Path, prefix: str) -> Path:
    matches = sorted(root.glob(f"{prefix}*.md"))
    if len(matches) != 1:
        raise ValueError(f"expected one {prefix} report in {root}, found {len(matches)}")
    return matches[0]


def table_by_header(block: str, required: set[str]) -> list[list[str]]:
    return next((rows for rows in markdown_tables(block) if rows and required.issubset(set(rows[0]))), [])


def assertions(text: str) -> dict[str, bool]:
    overview = section(text, "## 0. 一页看懂")
    chain = section(text, "## 1. 产业链地图")
    cycle = section(text, "## 5. 周期位置与传导")
    capital = section(text, "## 6. 资金动向")
    future = section(text, "## 7. 未来资金可能流向")
    ledger = section(text, "## 附录A 证据台账")
    nodes = extract_node_blocks(chain)
    cycle_rows = next((rows for rows in markdown_tables(cycle) if rows and "性质" in rows[0]), [])
    proxy_rows = table_by_header(capital, {"工具/主体", "覆盖节点", "指标与期间", "来源", "结论", "局限"})
    future_rows = table_by_header(future, {"情景", "触发条件", "利润池往哪个环节移动", "先受益的环节", "后受益/受损的环节", "需要盯的证据"})
    intro = re.search(r"###\s*这个行业是做什么的\s*(.*?)(?=\n###|\Z)", overview, re.DOTALL)
    return {
        "four_nodes": len(nodes) >= 4,
        "two_companies_per_node": all(len(re.findall(r"^\|[^-].*\bE\d+\b.*\|$", block, re.MULTILINE)) >= 2 for _, block in nodes),
        "eight_evidence_rows": len(re.findall(r"^\|\s*E\d+\s*\|", ledger, re.MULTILINE)) >= 8,
        "independent_stage_status": all(re.search(rf"{field}[：:]\s*\S+", overview) for field in ("周期阶段", "结论状态", "置信度", "证据截至时间", "上调条件", "下调条件")),
        "intro_status_clean": not intro or "结论状态" not in intro.group(1),
        "four_to_six_timeline_rows": 5 <= len(cycle_rows) <= 7,
        "timeline_types": bool(cycle_rows) and all(len(row) > 1 and row[1] for row in cycle_rows[1:]),
        "two_market_proxies": len(proxy_rows) >= 3,
        "usable_market_metric": len(proxy_rows) >= 3 and all(re.search(r"\d{4}|\d+(?:\.\d+)?%|\d+(?:\.\d+)?倍", row[3]) for row in proxy_rows[1:]),
        "complete_future_scenarios": len(future_rows) == 4 and all(len(row) >= 6 and all(row[:6]) for row in future_rows[1:]),
        "priced_and_unpriced": "已定价" in capital and "未定价" in capital,
        "no_advice_disclaimer": bool(re.search(r"不构成.{0,16}买卖建议", future)),
    }


def evaluate(root: Path) -> dict:
    reports = []
    passed = 0
    total = 0
    for prefix in PREFIXES:
        path = find_report(root, prefix)
        checks = assertions(path.read_text(encoding="utf-8"))
        reports.append({"file": path.name, "assertions": checks})
        passed += sum(checks.values())
        total += len(checks)
    return {"passed": passed, "total": total, "pass_rate": round(passed / total * 100, 1), "reports": reports}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("baseline", type=Path)
    parser.add_argument("candidate", type=Path)
    args = parser.parse_args()
    baseline = evaluate(args.baseline)
    candidate = evaluate(args.candidate)
    result = {
        "industries": ["AI算力", "液冷", "光伏", "铜"],
        "baseline": baseline,
        "candidate": candidate,
        "improvement_percentage_points": round(candidate["pass_rate"] - baseline["pass_rate"], 1),
        "threshold_percentage_points": 20.0,
        "passed": candidate["pass_rate"] == 100.0 and candidate["pass_rate"] - baseline["pass_rate"] >= 20.0,
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
