# Manager 归档索引

归档日期：2026-08-15

## capability-manager（已弃用）

- 弃用原因：v0.2.2 架构收敛后 Capability 层退役（5 个 capability.yaml 归档至 `.ai/archive/capabilities/`），Workflow 转 Markdown SOP 并直接 by-name 列 Skill/Agent，不再存在「Capability 契约、候选顺序和选择理由」需要管理的实体。capability-manager 的注册/查询职责已由 resource-manager 承接，索引职责由 workflow-registry 承接。
- 归档位置：`.ai/archive/managers/capability-manager/SKILL.md`（原始内容完整保留）
- 恢复方法：如需恢复，执行 `mv .ai/archive/managers/capability-manager .claude/skills/capability-manager` 即可（`.codex/skills` 单一目录软链接自动同步，无需额外操作）。
- 原始位置：`.claude/skills/capability-manager/`（2026-08-15 移除）

> 本表为溯源/导航信息，不构成执行契约；语义以对应 Workflow SOP 与 skill.yaml/agent.yaml 为准。
