#!/usr/bin/env python3
"""Assemble a fresh topic-forward run from validated, sourced lead cards."""
import argparse
import copy
import json
from pathlib import Path


ROUTES = {
    "market_pulse": ("market-companion-editor-agent", "行情陪伴型"),
    "earnings_gap": ("earnings-gap-translator-agent", "账本预期差型"),
    "company_industry": ("company-industry-explainer-agent", "生意拆解型"),
    "valuation_mechanism": ("valuation-mechanism-teacher-agent", "机制翻译型"),
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--leads", required=True, type=Path)
    parser.add_argument("--candidate-pool", required=True, type=Path)
    parser.add_argument("--out-dir", required=True, type=Path)
    args = parser.parse_args()

    leads = json.loads(args.leads.read_text(encoding="utf-8"))
    pool = json.loads(args.candidate_pool.read_text(encoding="utf-8"))
    template = json.loads(
        (Path(__file__).resolve().parents[3] / ".ai/templates/topic-forward-candidate.json.template").read_text(
            encoding="utf-8"
        )
    )
    template_keys = set(template)
    if len(leads) < 10:
        raise SystemExit("at least 10 sourced leads are required")

    cards = []
    matrix_seeds = []
    for lead in leads:
        if set(lead) != template_keys:
            raise SystemExit(f"lead fields must exactly match topic-forward template: {lead.get('candidate_id')}")
        line = lead.get("content_line")
        if line not in ROUTES:
            raise SystemExit(f"invalid content_line: {line}")
        agent, mode = ROUTES[line]
        if lead.get("expression_agent") != agent or lead.get("expression_mode") != mode:
            raise SystemExit(f"route mismatch: {lead.get('candidate_id')}")
        if not str(lead.get("dedup_status", "")).startswith("new"):
            raise SystemExit(f"lead is not marked as new: {lead.get('candidate_id')}")
        card = copy.deepcopy(lead)
        card["status"] = "card"
        card["review_constraints"] = list(card["review_constraints"]) + [
            "适用复盘实验：若采用，只携带 C1（前15–20秒完成冲突—判断—验证条件），不与其他内容实验叠加"
        ]
        cards.append(card)
        matrix_seeds.append(
            {
                "seed_id": lead["candidate_id"],
                "subject": lead["title"],
                "possible_lines": [
                    {
                        "content_line": line,
                        "eligible": True,
                        "reason": "当前来源支持该观众任务；其他主线不在轻量核验阶段硬造",
                        "expression_agent": agent,
                        "expression_mode": mode,
                        "audience_question": lead["audience_question"],
                        "core_tension": lead["core_tension"],
                        "title_options": lead["title_options"],
                        "research_required": lead["research_required"],
                    }
                ],
                "selected_line": line,
                "discarded_lines": [x for x in ROUTES if x != line],
            }
        )

    args.out_dir.mkdir(parents=True, exist_ok=True)
    (args.out_dir / "topic-angle-matrix.json").write_text(
        json.dumps(
            {
                "schema_version": "1",
                "captured_at": pool.get("captured_at"),
                "source_file": str(args.candidate_pool),
                "seeds": matrix_seeds,
                "notes": ["Fresh 2026-09-08 run; each card has one content line and one audience task."],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    (args.out_dir / "topic-forward.json").write_text(
        json.dumps(
            {
                "topic_forward_date": "2026-09-08",
                "run_id": "rerun-01",
                "status": "pending_approval",
                "approved_topic_id": None,
                "approved_at": None,
                "user_note": "",
                "source_files": [args.leads.name, args.candidate_pool.name, "signals.json", "multi-search.json"],
                "cards": cards,
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    lines = [
        "# 2026-09-08 选题前瞻（全新重跑）",
        "",
        "> 状态：`pending_approval`。本目录不是 2026-09-06 候选的复制；本轮重新发现并排除了上一轮的猪周期、软件数据基础设施、黄酒消费、包装和激光设备主题。",
        "",
        "## 执行摘要",
        "",
        f"- 新增有来源 discovery seeds：{len(cards)} 张；行情扫描错误保留在 `signals.json`。",
        "- 本轮 `multi-search` 三组查询均因网络不可用返回空数组；候选事实使用公开原文检索结果并标注研究缺口，不把空结果解释为没有新闻。",
        "- 每张卡只有一条 `content_line`；当前复盘候选只作为可选 C1 实验，不改变研究问题。",
        "",
        "## 新的候选卡",
        "",
        "| 顺位 | 主线 | topic_id | 选题 | 观看任务 |",
        "|---:|---|---|---|---|",
    ]
    for i, card in enumerate(cards, 1):
        lines.append(f"| {i} | `{card['content_line']}` | {card['topic_id']} | {card['title']} | {card['audience_question']} |")
    lines += [
        "",
        "## 审批",
        "",
        "请从 `TOPIC-R2-01` 至 `TOPIC-R2-12` 中选择一个。批准内容是“研究对象 + content_line + 核心问题”；批准前不进入 `topic-research` 和视频生产。",
    ]
    (args.out_dir / "topic-forward.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (args.out_dir / "topic-forward-execution.md").write_text(
        "\n".join(
            [
                "# topic-forward-lead 执行记录：2026-09-08 / rerun-01",
                "",
                "## 运行结论",
                "",
                "- 本轮为全新发现，不复用 2026-09-06-rerun-01 的候选卡。",
                f"- 生成 {len(cards)} 张候选卡，状态为 `pending_approval`；未启动研究、脚本、配音、渲染或发布。",
                "- 旧题去重：猪周期、软件数据基础设施、黄酒消费、包装、激光设备不进入本轮卡片。",
                "",
                "## Required Resources",
                "",
                "| Resource | 执行结果 | 产物 | 降级/边界 |",
                "|---|---|---|---|",
                "| `topic-forward-signal-scanner` | 已执行 | `signals.json` | 涨停池与全量行情均 `ConnectionError`；保留 errors，不把空结果当无热点 |",
                "| `multi-search` | 已执行 | `multi-search.json` | 三组查询均因网络不可用返回空数组；公开原文核验线索另存于 `editorial-leads-2026-09-08.json` |",
                "| `finance-content-engineering` | 已应用 topic-gen 规则 | `editorial-leads-2026-09-08.json`、`topic-forward.json` | 角度先于标题，保留事实/推断边界 |",
                "| `topic-angle-router-agent` | 已执行 | `topic-angle-matrix.json`、`topic-forward.json` | 每卡一条主线、一种深度和一个观众任务 |",
                "| `boundary-rewrite` | 已应用 | `topic-forward.json`、本轮 cards 的 `review_constraints` | 删除交易指令、目标价和收益承诺，保留可验证冲突 |",
                "",
                "## 审批边界",
                "",
                "用户批准前，未批准卡不得进入 `topic-research` 或视频生产。",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"[OK] assembled {len(cards)} cards in {args.out_dir}")


if __name__ == "__main__":
    main()
