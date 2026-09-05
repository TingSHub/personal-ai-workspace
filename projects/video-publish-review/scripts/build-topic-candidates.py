#!/usr/bin/env python3
"""Normalize market signals into auditable topic seeds.

This creates company and industry seeds only. News and comparison cards need
human/LLM grouping after news-search review; the script must not invent them.
"""
import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--signals", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    source = Path(args.signals)
    data = json.loads(source.read_text(encoding="utf-8"))
    captured = data.get("captured_at", datetime.now().isoformat(timespec="seconds"))
    seeds, industries, members = [], Counter(), defaultdict(list)
    for item in data.get("zt_pool", []):
        industry = item.get("industry") or "未分类"
        industries[industry] += 1
        members[industry].append(item.get("name"))

    def company_seed(item, field, prefix, question):
        name, code = item.get("name", ""), item.get("code", "unknown")
        industry = item.get("industry") or "未分类"
        seeds.append({
            "candidate_id": f"{prefix}-{code}", "focus_type": "company",
            "title": name, "scope": "company", "companies_or_roles": [name],
            "core_question": question,
            "evidence": [{"source": "signals.json", "field": field, "code": code,
                          "industry": industry, "pct_chg": item.get("pct_chg"),
                          "turnover": item.get("turnover")}],
            "review_candidates": [], "dedup_status": "new",
            "research_required": ["公告/财报", "异动原因", "可比公司"],
            "status": "seed"
        })

    zt_pool = sorted(data.get("zt_pool", []), key=lambda x: x.get("pct_chg") or 0, reverse=True)[:6]
    movers = sorted(data.get("movers", []), key=lambda x: x.get("pct_chg") or 0, reverse=True)[:6]
    for item in zt_pool:
        company_seed(item, "zt_pool", "COMPANY", "异动背后的业务、财务与事件是否可验证？")
    for item in movers:
        company_seed(item, "movers", "MOVER", "涨幅是否对应订单、利润或现金流的兑现？")
    for industry, count in industries.items():
        if count >= 2:
            seeds.append({
                "candidate_id": f"INDUSTRY-{industry}", "focus_type": "industry",
                "title": f"{industry}：上涨信号能否被行业基本面验证？", "scope": "industry",
                "companies_or_roles": [x for x in members[industry] if x][:4],
                "core_question": f"{industry}的短期异动，最终要由哪些公司数据验证？",
                "evidence": [{"source": "signals.json", "field": "zt_pool",
                              "industry": industry, "count": count}],
                "review_candidates": [], "dedup_status": "new",
                "research_required": ["行业供需", "代表公司财报", "事件与政策"],
                "status": "seed"
            })
    result = {
        "captured_at": captured, "trade_date": data.get("trade_date"),
        "errors": data.get("errors", []), "source_file": str(source),
        "counts": {"company": sum(x["focus_type"] == "company" for x in seeds),
                    "industry": sum(x["focus_type"] == "industry" for x in seeds),
                    "news": 0, "comparison": 0},
        "seeds": seeds,
        "notes": ["news and comparison seeds require news-search review and analyst grouping"]
    }
    out = Path(args.out)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] wrote {out}: {len(seeds)} seeds")


if __name__ == "__main__":
    main()
