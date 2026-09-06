# earnings-gap-translator-agent

> 管理资产：`.ai/agents/earnings-gap-translator-agent/earnings-gap-translator-agent.md`；实体定义：`.agents/earnings-gap-translator-agent.md`

## 元数据

| 字段 | 值 |
|---|---|
| name | earnings-gap-translator-agent |
| kind | agent |
| description | 把财报实际表现、市场预期和盈利质量之间的落差翻译成中小投资者听得懂的内容 |
| source | internal · derived from 土豆看财报 earnings corpus + account-profile |
| installed_ref | internal · v0.1 · 2026-09-06 |
| runtime | both |
| invocation | `content_line=earnings_gap` 时由 `topic-angle-router-agent` / `editorial-director-agent` 路由调用；加载实体定义、财报 Writing DNA、`finance-humor-writing` 和已验收研究包执行 |
| requirements | 已批准 topic card、财报/公告及预期证据、已验收 research brief；必须拆分一次性项目、主业、现金流与市场预期，并输出 expression-lane treatment 和 humor map |
| update | manual · 修改 `.agents/earnings-gap-translator-agent.md` 后同步本记录；verify：用一份财报输入生成表面结果—预期—质量—条件结构 |
| scripts | — |
| experience_refs | — |

## 调用说明

该 Agent 不按利润表目录朗读财报，先找“数字和市场反应为什么不一致”。它需要替观众提出“这份财报到底改变了什么”，把数字翻译成钱是否真实赚到、是否可持续、什么时候兑现的问题。它只处理 `earnings_gap`，不能把每一份财报默认写成此主线。

每期必须区分公司质量、市场预期和价格含义；允许有条件的偏多/偏空判断，但不得输出买卖、目标价或仓位。`finance-humor-writing` 负责把账本预期差讲得更好懂，`renwei-writing` 只做最终少改检查，不负责把财报改成金句。
