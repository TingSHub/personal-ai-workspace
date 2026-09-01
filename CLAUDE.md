# Personal AI Workspace

## Purpose

这是一个服务项目交付的个人 AI 能力管理与编排系统：管理 Workflow（Markdown SOP）、Skill/Agent 资源和经验证的 Experience，让真实项目质量更高、执行更快、重复利用更多。Claude、Codex 或其他 Agent 负责执行，本仓库不是 Agent Runtime。

## Rules

- 执行任务前优先寻找已有 Workflow（`.ai/workflows/`）
- 不重复创建已有 Skill/Agent 资源（`.ai/skills/`、`.ai/agents/`）
- Skill/Agent 使用 Resource Manager 管理（`.claude/skills/resource-manager/`）
- Workflow 使用 Workflow Registry 索引（`.claude/skills/workflow-registry/`）
- 创建新项目用 Project Registry（`.claude/skills/project-registry/`）
- 字段清单一律从 `.ai/templates/` 模板读取填充，禁止内联字段定义
- 顶层仓库与 `projects/*` 物理隔离：不将项目代码提交到本仓库
- 引用 Workflow / Skill / Agent / Experience 一律用 by-name 标识符，不用相对路径
- 运行时状态（`.omc/`）永不提交；`.codex/skills` 是唯一目录级软链接，固定指向 `../.claude/skills`，禁止创建逐 Skill 二级链接
- **默认调用路径**：Project → Workflow → Skill/Agent。Workflow 是 Markdown SOP 唯一事实源；阶段 Required Resources 必须真实执行并留下独立产物；下游只消费已验收产物。
- **最佳可用资源选择**：禁止 local first。按实际效果、输出质量、稳定性、依赖成本、维护成本和当前项目适配性选择；从 workspace、已安装外部 Skill、skill-hub、find-skills 和 agent repository 发现候选，来源不构成优先级。依赖可安全补齐时先补齐，确实无法使用或验收失败才回退；不维护综合评分、可用状态或配置成本模型。
- **资源边界**：Skill/Agent 只记录来源、已安装版本、调用、要求、更新方式、注意事项、踩坑和可选辅助脚本。本地增强放在资源资产内，不修改外部安装实体。
- **Experience 反馈闭环**：项目日志永不进入资产库。项目结束时由 Experience Curator 提炼能改变未来 Workflow、资源调用、质量检查或可复用脚本的结论并判定归属；Candidate 暂存于项目，经用户确认后回写至目标 Workflow SOP 或 Skill/Agent 记录（by-name 回填 `experience_refs[]`），回写完成后归档至 `.ai/archive/experiences/`。

## Structure

- `.ai/skills` — Skill 资源说明、调用注意事项与本地辅助脚本
- `.ai/agents` — Agent 资源说明、调用注意事项与本地辅助脚本
- `.ai/archive/capabilities` — 已退役 Capability 层归档（历史质量契约，仅溯源不执行）
- `.ai/experiences` — 在途经验（反馈闭环：回写完成后归档至 `.ai/archive/experiences/`）
- `.ai/workflows` — 流程库（development / task / automation）
- `.ai/templates` — 生成模板（唯一事实源）
- `.ai/rules` — 规则索引
- `.claude/skills` — Registry Skills
- `projects` — 实际项目（独立 Git）
