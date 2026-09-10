# topic-angle-router-agent

> 管理资产：`.ai/agents/topic-angle-router-agent/topic-angle-router-agent.md`；实体定义：`.agents/topic-angle-router-agent.md`

## 元数据

| 字段 | 值 |
|---|---|
| name | topic-angle-router-agent |
| kind | agent |
| description | 把选题线索拆成互斥的观众问题、内容主线和解释深度，并绑定对应的表达 Agent、表达模式和研究契约 |
| source | internal · investment-research-video |
| installed_ref | internal · v0.2 · 2026-09-06 |
| runtime | both |
| invocation | `topic-forward-lead` Phase 2 调用；对 discovery seeds 生成 content-line angle matrix，并为候选卡绑定后续表达 Agent |
| requirements | 已验收 discovery seeds、轻量来源和账号去重基线；需要判断 `content_depth` 并把深度需求写入研究契约；不能代替完整研究、用户批准或最终标题审定 |
| update | manual · 修改 `.agents/topic-angle-router-agent.md` 后同步本记录；verify：用同一主体生成至少两张主线不同且问题互斥的候选卡，检查映射和证据缺口 |
| scripts | — |
| experience_refs | — |

## 调用说明

这是选题层和表达层之间的路由 Agent。它不写完整脚本，也不提前调用某条表达 Agent 生成成稿；它只把 `content_line`、观众问题、核心张力、标题方向、研究缺口和后续 `expression_agent` 固定下来。

四条映射固定为：`market_pulse → market-companion-editor-agent`、`earnings_gap → earnings-gap-translator-agent`、`company_industry → company-industry-explainer-agent`、`valuation_mechanism → valuation-mechanism-teacher-agent`。行情热度不能自动升级为财报或估值角度；同一公司多角度候选必须有不同观众任务和证据需求。
