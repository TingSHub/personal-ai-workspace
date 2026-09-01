# Experience: content-director-validation

> 仅沉淀会改变未来项目流程、资源选择、调用方法、质量检查或可复用脚本的经验证结论。

## 来源证据

项目：investment-research-system；运行：research-content-direction Phase 2 首轮正式实测（2026-08-15，investor-understanding-architect v0.1，贵州茅台案例）。证据：`outputs/companies/贵州茅台/2026-08-15/content-assets/content-thesis/content-thesis.md`（174 行）+ `content-assets/execution-log.md`。相关资源 installed_ref：investor-understanding-architect（internal）。

## 触发场景

investor-understanding-architect 执行 Phase 2（研究资产 → 内容观点方案）时；或后续优化该 Agent 工作流与输出契约时。

## 问题与归属判定

- 问题：首轮实测验证了工作流设计的四个有效机制，同时暴露两个输出层短板——需要记录为 Agent 后续优化的依据。
- 归属（owner）：`investor-understanding-architect`（记录为优化依据；本轮不修改 Agent 行为）。

## 可复用结论（resolution）

1. **多视角提案有效**：用 content-opportunity 的多条故事线各自提案再整合，产出高质量叙事（本轮悬念线主骨架 + 对比线 + 历史纵深线）；素材不足的视角（人物线）如实降级为冲突呈现载体，不虚构。→ 保留该机制。
2. **冲突保留有效**：分歧最大的冲突（C2 周期 vs 结构）保留两组叙事候选不合并，C1-C6 全部原样保留不裁决——叙事张力与可信度兼得，无依据合并反而损害内容。→ 保留该纪律。
3. **fact-map 约束有效**：信息取舍按可信度分层（必用/慎用/禁用）严格执行，数字逐一回指、零事实漂移；禁用清单（PEG/失真分位/已证伪记忆/代理数据/未落地政策）有效拦截了高风险数字。→ 保留该约束。
4. **输出偏重**：content-thesis.md 174 行对「内容观点方案」偏重——下游（脚本层/Visual Director）需要的是决策摘要而非长文档。→ 后续优化方向：输出压缩为决策摘要（受众/核心叙事/信息取舍三要素），细节下放引用或附录。
5. **visual brief 需要增强**：输出契约缺少面向 Visual Director 的视觉简报字段（视觉风格/分镜方向/素材策略）——Phase 3 输入将断层。→ 后续优化方向：content-thesis 增加 visual-brief 字段或独立输出，保证 Phase 3 可消费。

## 回写目标

- `investor-understanding-architect`（描述层与实体在后续优化时应用上述结论；本轮仅归档记录，不修改 Agent）

## 适用范围

investor-understanding-architect（internal）的 Phase 2 执行与后续迭代；同类"研究资产 → 内容观点"任务。

## 不适用范围

- 其他 Director 角色（Research Director 的资产理解、Visual Director 的视觉方案各有独立契约）；
- Agent 行为已随版本变化时，需按新版本复验。

## 关联资产

- Agent: `investor-understanding-architect`、`research-intelligence-agent`
- Workflow: `research-content-direction`
- Skill: `zimeiti-persona-skills`、`finance-content-engineering`
