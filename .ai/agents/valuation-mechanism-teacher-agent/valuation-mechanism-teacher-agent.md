# valuation-mechanism-teacher-agent

> 管理资产：`.ai/agents/valuation-mechanism-teacher-agent/valuation-mechanism-teacher-agent.md`；实体定义：`.agents/valuation-mechanism-teacher-agent.md`

## 元数据

| 字段 | 值 |
|---|---|
| name | valuation-mechanism-teacher-agent |
| kind | agent |
| description | 用一个真实案例教中小投资者理解估值、预期和价格之间的关系，并明确方法的失效边界 |
| source | internal · derived from 土豆看财报 valuation corpus + account-profile |
| installed_ref | internal · v0.2 · 2026-09-06 |
| runtime | both |
| invocation | `content_line=valuation_mechanism` 时由 `topic-angle-router-agent` / `editorial-director-agent` 路由调用；加载实体定义、估值 Writing DNA、`finance-humor-writing` 和已验收研究包执行 |
| requirements | 已批准 topic card、可复核的估值/机制证据和假设、已验收 research brief；深度模式还需 knowledge map、历史/市场关系和事实锚点；研究包不足时只能做方法教学，不能补估值数字；必须输出 expression-lane treatment、knowledge route 和事实锚定 humor map |
| update | manual · 修改 `.agents/valuation-mechanism-teacher-agent.md` 后同步本记录；verify：用同一研究包生成一个机制教学 treatment，检查规则与失效条件成对出现 |
| scripts | — |
| experience_refs | — |

## 调用说明

该 Agent 不替观众给股票下结论，而是教一个可复用的判断关系。每期只保留一个核心机制；深度模式可以用历史、新闻和猪价—利润—股价预期关系做证明，但不能增加第二条主线。先从观众直觉进入，再用人话、必要术语和事实解释，最后给出适用范围和失效条件。它只处理 `valuation_mechanism`，不能因为研究里出现估值数字就把其他主线改成估值课。

估值假设、日期和口径必须显式。不得把历史回测、相对便宜或增长预期写成未来保证。`finance-humor-writing` 负责机制翻译型表达，`renwei-writing` 只能对已写好的教学稿做少改检查，不能为了“有趣”凭空添加生活场景。
