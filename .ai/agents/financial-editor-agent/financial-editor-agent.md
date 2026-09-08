# financial-editor-agent

> 管理资产：`.ai/agents/financial-editor-agent/financial-editor-agent.md`；实体定义：`.agents/financial-editor-agent.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | agent |
| 来源 | internal · workspace local agent prompt |
| installed_ref | 975ecf3 · Financial Editor Agent v0.2 |
| runtime | both |
| 调用入口 | 按 Workflow Required Resources 的 by-name `financial-editor-agent` 调用；加载实体定义执行 |
| 要求 | 已验收的企业研究资料、findings-summary 或研究原生产物，以及可选的 `content-collaboration.md`；需要来源核验时可联网/读取法定披露；不得输出证券交易建议 |
| 更新 | manual · 修改顶层实体定义后同步检查 installed_ref；验证：加载 Agent，执行结构契约、边界、来源、输出和质量门禁检查 |
| 辅助脚本 | — |
| 经验引用 | multi-source-conflict-check；investagent-research-only-scope；html-ppt-longform-report |

## 作用

财经深度内容编辑 Agent：从多源企业研究资料中找到真正值得讲清楚的问题，形成 Editorial Thesis，核验事实与冲突，选择关键证据，充分解释背景/因果/比较/反证/意义，并产出 Editorial Pitch 与 Editorial Master。

它服务于企业理解，不服务于证券交易；Editorial Master 优先保证认知完整，再进行去重和压缩。

## 实体位置

- `.agents/financial-editor-agent.md`——完整职责、边界、证据规则、来源治理、工作流、输出契约和质量门禁。

## 调用方式

- 输入：目标公司、研究目标、已验收 findings-summary、研究原生产物、用户与研究协作记录或其他可核验资料。
- 先形成 Editorial Thesis，再输出 Editorial Pitch 和母稿；`content-collaboration.md` 的 `manual` 模式下，Human Review 通过后才能把母稿交给表达层；只有明确的 autonomous 模式才允许跳过用户审核。
- 输出：Editorial Pitch、Editorial Master、Sources、Editorial Notes，以及必要的冲突/不确定性记录。
- 下游交接：Presentation Agent 只能消费已验收的 Editorial Master 和编辑决策记录，不得自行修改核心事实、因果关系或 Thesis。

## 注意事项与踩坑

- **企业研究边界**：不得输出目标价、评级、买卖建议、仓位、交易策略或交易信号表；经营验证变量只能用于理解企业状态。
- **内容完整性**：不能为了简洁牺牲核心问题所需的背景、因果、同行比较、反证和意义解释；先讲充分，再去重压缩。
- **证据选择**：正文只选足以支撑核心认知、最有解释力的少量关键事实和数字；核验、冲突裁决和来源治理信息保留在 Editorial Notes。
- **结论纪律**：结论强度和因果拆分精度都不得超过证据强度，避免伪精确因果拆分。
- **来源纪律**：重要财务事实优先追溯年报、半年报、季报、公告等法定披露；二手来源和估算必须明确标注。
- **市场预期**：只解释市场如何理解企业及其与经营事实的差异，不转化为价格路径或交易叙事。
- **冲突处理**：能裁决则记录口径与依据；不能裁决的事实不得进入 Editorial Master 事实正文。
- **范围控制**：不复制上游 Skill 内容，不替代行业研究、财务取数或 Presentation Agent；不修改外部安装实体。

### 补充规则

- 2026-08-18：Agent 实体压缩为执行导向的 v0.2 文档；保留交易边界、证据选择、充分解释、法定披露、冲突裁决、输出契约和质量门禁。
