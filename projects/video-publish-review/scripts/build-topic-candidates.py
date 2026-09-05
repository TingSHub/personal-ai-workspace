#!/usr/bin/env python3
"""Normalize optional market signals and sourced leads into auditable seeds.

The output is a discovery pool. It deliberately leaves the audience question
blank for raw market seeds so a price move cannot silently become a thesis.
"""
import argparse
import copy
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--signals", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--leads", type=Path, help="Optional JSON list of sourced news, product, industry or audience leads")
    args = parser.parse_args()
    source = Path(args.signals)
    data = json.loads(source.read_text(encoding="utf-8"))
    captured = data.get("captured_at", datetime.now().isoformat(timespec="seconds"))
    seeds, industries, members = [], Counter(), defaultdict(list)
    template_path = Path(__file__).resolve().parents[3] / ".ai/templates/topic-forward-candidate.json.template"
    template = json.loads(template_path.read_text(encoding="utf-8"))

    def seed(**values):
        result = copy.deepcopy(template)
        result.update(values)
        return result
    for item in data.get("zt_pool", []):
        industry = item.get("industry") or "未分类"
        industries[industry] += 1
        members[industry].append(item.get("name"))

    def company_seed(item, field, prefix):
        name, code = item.get("name", ""), item.get("code", "unknown")
        industry = item.get("industry") or "未分类"
        seeds.append(seed(**{
            "candidate_id": f"{prefix}-{code}", "focus_type": "company",
            "title": name, "scope": "company", "companies_or_roles": [name],
            "subject_type": "company", "audience_question": "",
            "evidence": [{"source": "signals.json", "field": field, "code": code,
                          "industry": industry, "pct_chg": item.get("pct_chg"),
                          "turnover": item.get("turnover")}],
            "review_constraints": [], "dedup_status": "new",
            "research_required": ["核验信号日期与主体", "查找相关事件、产品或业务变化；策划据此提出观众问题"],
            "status": "seed"
        }))

    zt_pool = sorted(data.get("zt_pool", []), key=lambda x: x.get("pct_chg") or 0, reverse=True)[:6]
    movers = sorted(data.get("movers", []), key=lambda x: x.get("pct_chg") or 0, reverse=True)[:6]
    for item in zt_pool:
        company_seed(item, "zt_pool", "COMPANY")
    for item in movers:
        company_seed(item, "movers", "MOVER")
    for industry, count in industries.items():
        if count >= 2:
            seeds.append(seed(**{
                "candidate_id": f"INDUSTRY-{industry}", "focus_type": "industry",
                "title": industry, "scope": "industry", "subject_type": "industry",
                "companies_or_roles": [x for x in members[industry] if x][:4],
                "audience_question": "",
                "evidence": [{"source": "signals.json", "field": "zt_pool",
                              "industry": industry, "count": count}],
                "review_constraints": [], "dedup_status": "new",
                "research_required": ["核验行业聚集信号", "查找产业变化与受众问题"],
                "status": "seed"
            }))
    if args.leads:
        leads = json.loads(args.leads.read_text(encoding="utf-8"))
        if not isinstance(leads, list):
            raise SystemExit("--leads must contain a JSON list using the topic-forward candidate template")
        for lead in leads:
            if not isinstance(lead, dict) or not lead.get("candidate_id") or not lead.get("title") or not lead.get("evidence"):
                raise SystemExit("each lead requires candidate_id, title and evidence")
            if lead.get("focus_type") not in {"company", "industry", "news", "comparison"}:
                raise SystemExit("invalid lead focus_type")
            if set(lead) - set(template):
                raise SystemExit("lead fields must come from topic-forward-candidate.json.template")
            seeds.append(seed(**{**lead, "status": "seed", "review_constraints": []}))
    unique = {}
    for item in seeds:
        key = item["candidate_id"]
        if key in unique:
            raise SystemExit(f"duplicate candidate_id: {key}")
        unique[key] = item
    result = {
        "captured_at": captured, "trade_date": data.get("trade_date"),
        "errors": data.get("errors", []), "source_file": str(source),
        "counts": {"company": sum(x["focus_type"] == "company" for x in seeds),
                    "industry": sum(x["focus_type"] == "industry" for x in seeds),
                    "news": sum(x["focus_type"] == "news" for x in seeds),
                    "comparison": sum(x["focus_type"] == "comparison" for x in seeds)},
        "seeds": seeds,
        "notes": ["Seeds are discovery leads, not approved topics or verified research. Blank questions require editorial work; market moves do not imply a financial thesis."]
    }
    out = Path(args.out)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[OK] wrote {out}: {len(seeds)} seeds")


if __name__ == "__main__":
    main()
