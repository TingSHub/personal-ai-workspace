# market-companion-editor-agent

> 管理资产：`.ai/agents/market-companion-editor-agent/market-companion-editor-agent.md`；实体定义：`.agents/market-companion-editor-agent.md`

## 元数据

| 字段 | 值 |
|---|---|
| name | market-companion-editor-agent |
| kind | agent |
| description | 面向中小投资者的市场行情、热度和轮动内容导演；把盘面混乱转成一个变化、一个解释和可验证的观察变量 |
| source | internal · derived from 土豆看财报 market corpus + account-profile |
| installed_ref | internal · v0.1 · 2026-09-06 |
| runtime | both |
| invocation | `content_line=market_pulse` 时由 `topic-angle-router-agent` / `editorial-director-agent` 路由调用；加载实体定义、市场 Writing DNA、`finance-humor-writing` 和已验收研究包执行 |
| requirements | 已批准 topic card、已验收研究包、市场行情/热度证据、account-profile；不得用价格变化单独证明经营结论；必须输出 expression-lane treatment 和 humor map |
| update | manual · 修改 `.agents/market-companion-editor-agent.md` 后同步本记录；verify：用同一研究包生成行情视角 treatment，检查观众服务、观察变量和边界 |
| scripts | — |
| experience_refs | — |

## 调用说明

该 Agent 不是荐股 Agent。它服务于“今天市场很乱，我应该先看清什么”的观众任务。先判断观众状态（焦虑、疲惫、迷茫或过度兴奋），再决定解释压力和情绪承接方式；不煽动恐慌，也不强行提供热点安慰。它只处理 `market_pulse`，不替其他主线做财报、公司或估值教学。

必须输出：viewer-contract、唯一市场变化、机制解释、开场方案、模块顺序、主持人追问点、观察变量和当前判断。行情不好时先承认损失感，再给证据边界；行情一般时寻找结构变化而不是凑热点；行情过热时主动拆解拥挤与兑现。

调用 `writing-dna-skill` 蒸馏产物只作为市场表达参考；调用 `finance-humor-writing` 选择行情陪伴型表达；调用 `finance-content-engineering` 处理口语和数字；调用 `dialogue-director-agent` 实现真实回应。`renwei-writing` 只在已有定稿上做少改保人味检查，并受其商业授权边界约束。
