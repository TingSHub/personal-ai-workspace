# research-synthesis-agent

> 管理资产：`.ai/agents/research-synthesis-agent/research-synthesis-agent.md`；安装实体：`.agents/research-intelligence-agent.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | agent |
| 来源 | internal · workspace internal agent profile |
| installed_ref | internal |
| runtime | both |
| 调用入口 | 由 listed-company-research-production 在 data-acquisition 通过后调用；只消费已验收来源和实际执行资源产物 |
| 要求 | 已验收的公司主体、证券代码、研究边界、数据截止日和 source_base；至少一个适配任务的外部或 workspace 研究资源真实执行并留下 Capability Result；能处理长文档并保持证据、口径、缺口和资源执行记录一致的模型 |
| 更新 | internal · 只更新本地 Agent 调用说明、输出契约和资源融合规则；不得复制外部 Skill 内容或伪造未执行资源；验证：用一个已完成上市公司案例重新生成 Research Intelligence Document，并通过研究-only质量门和人工抽样证据复核 |
| 辅助脚本 | — |
| 经验引用 | research-master-content-pipeline |

## 作用

Research Synthesis Agent（旧架构资源，v0.3 重命名）：整合已实际执行的研究资源，生成完整、严谨、可复用的 Research Intelligence Document（十章 + Evidence Ledger）。研究阶段只最大化研究价值，不为传播目的压缩内容。

## 实体位置（可加载定义）

- `.agents/research-synthesis-agent.md`——完整职责（定位/输入/执行原则/十章输出契约/验收）

## 调用方式

- 输入：公司主体信息 + 已验收 `source_base` + 实际执行资源产物 + Research Resource Evaluation
- 输出：Research Intelligence Document（十章：概览/行业/竞争/业务/护城河/财务/投资逻辑/风险/估值/跟踪指标）+ Evidence Ledger

## 注意事项与踩坑

- best available resource，不做简单平均；按资源优势组合章节。
- 未实际执行的资源只能作为候选评估，不能声称已运行。
- 每个关键结论必须绑定 Evidence Ledger；无来源数据一律禁止。
- 内容生产只能消费已验收的 RID，不消费本 Agent 私有推理。
