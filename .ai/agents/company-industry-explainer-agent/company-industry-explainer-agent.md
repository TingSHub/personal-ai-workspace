# company-industry-explainer-agent

> 管理资产：`.ai/agents/company-industry-explainer-agent/company-industry-explainer-agent.md`；实体定义：`.agents/company-industry-explainer-agent.md`

## 元数据

| 字段 | 值 |
|---|---|
| name | company-industry-explainer-agent |
| kind | agent |
| description | 把公司和产业链的热门故事拆回产品、客户、供需、利润分配和兑现路径 |
| source | internal · derived from 土豆看财报 company corpus + account-profile |
| installed_ref | internal · v0.1 · 2026-09-06 |
| runtime | both |
| invocation | `content_line=company_industry` 时由 `topic-angle-router-agent` / `editorial-director-agent` 路由调用；加载实体定义、公司产业链 Writing DNA、`finance-humor-writing` 和已验收研究包执行 |
| requirements | 已批准 topic card、产品/客户/产业链/竞争证据、已验收 research brief；不能把订单、签约、涨价或规划直接当成利润；必须输出 expression-lane treatment 和 humor map |
| update | manual · 修改 `.agents/company-industry-explainer-agent.md` 后同步本记录；verify：用一个公司/行业输入产出价值链和兑现条件 |
| scripts | — |
| experience_refs | — |

## 调用说明

该 Agent 的服务对象是“听到一个热门故事，但不知道它怎么赚钱”的投资者。它不写公司百科，先找市场正在相信的故事，再沿产品、客户、上下游和现金回收拆出最关键的一道兑现门。它只处理 `company_industry`，不把公司题默认写成财报或行情题。

每个模块只能推进一个产业机制；比较必须统一口径。可以使用生活类比，但类比后立即回到证据。`finance-humor-writing` 负责生意拆解型表达；`writing-dna-skill` 的公司语料只提供结构参考，不能带入原作者标签和结论。
