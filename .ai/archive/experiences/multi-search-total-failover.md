# Experience: multi-search-total-failover

> 仅沉淀会改变未来项目流程、资源选择、调用方法、质量检查或可复用脚本的经验证结论。

## 来源证据

项目：investment-research-system；运行：research-collection v0.3 贵州茅台实测（2026-08-15，industry-cycle-analysis 执行）。证据：`outputs/companies/贵州茅台/2026-08-15/research-materials/industry-cycle-analysis/` 报告执行记录（multi-search 三引擎全挂 → 降级 WebSearch/WebFetch 直连，质量未受损，证据台账 19/25 条 opened）。相关资源 installed_ref：multi-search（tree-sha256:6535cb0b3ab7）。

## 触发场景

通过 multi-search 执行关键证据检索，而环境出现多引擎同时不可用（DuckDuckGo/Tavily 检测不可用 + Bing 爬虫缺 beautifulsoup4 依赖）。

## 问题与归属判定

- 问题：multi-search 可能三个引擎同时全挂（网络检测失败 + 依赖缺失），此时"等它恢复"会阻塞研究；直接降级为内置 WebSearch/WebFetch 是可行的替代路径。
- 归属（owner）：`multi-search` 注意事项与踩坑（补充现有网络影响条目之下的全挂降级路径）。

## 可复用结论（resolution）

- 三引擎全挂时不必阻塞：降级为 WebSearch/WebFetch 直连可完成同等质量的证据检索（本轮 7 个原始来源实际打开、证据台账质量未受损）。
- 判定顺序：先确认依赖（`pip show beautifulsoup4` 等）与网络检测结果，再决定是修复还是降级；修复超过约 5 分钟即切换直连。
- 降级是研究执行层面的自主行为，属于资源内部职责，不需要上层 Workflow 干预（验证 research-collection v0.3 设计）。

## 回写目标

- `multi-search`（SKILL.md 注意事项与踩坑，追加条目）

## 适用范围

multi-search（tree-sha256:6535cb0b3ab7）在真实项目中的检索任务，特别是证据要求高的研究任务。

## 不适用范围

- 需要多引擎聚合去重场景的批量舆情扫描（直连检索无聚合去重能力）。

## 关联资产

- Skill: `multi-search`
- Workflow: `research-collection`
