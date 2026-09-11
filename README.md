# Personal AI Workspace

个人 AI 能力管理与编排系统 —— **不重复造轮子，让每一次 AI 项目实践成为下一次项目的基础。**

## 系统目标

让 AI Agent 能够：

1. 复用已有 Workflows 和 Skill/Agent 资源
2. 按项目质量要求选择最合适的执行资源
3. 快速创建标准化项目并减少重复配置和排错
4. 在真实项目验证后沉淀可复用经验
5. 让项目随实践积累可封装为 Skill 的方法与材料，在用户需要时快速整理、验证和封装

工作台支持能力从项目实践发展为 Skill，但转换完全可选。项目首先解决真实问题；日常只维护清晰入口、可替换配置、可追溯依赖和最小复跑依据，打包、跨环境适配与独立运行验证在用户决定转换时进行。

本系统**不是** Agent Framework，不替代 Claude / Codex / OMC。Agent 负责执行，本系统负责管理：

- 工作流程（Workflow Markdown SOP）— `.ai/workflows/`、`projects/*/workflows/`
- 执行资源（Skill/Agent）— `.ai/skills/`、`.ai/agents/`
- 可复用经验（Experience 反馈闭环）— `.ai/experiences/` → 归档 `.ai/archive/experiences/`
- 项目资产（Project）— `projects/`

## 目录结构

```
personal-ai-workspace/
├── CLAUDE.md            # Agent 行为规则（Claude Code 入口）
├── AGENTS.md            # Agent 行为规则（Codex 入口）
├── .ai/
│   ├── system.yaml      # workspace 元信息与规则
│   ├── skills/          # Skill 资源说明、注意事项与辅助脚本
│   ├── agents/          # Agent 资源说明、注意事项与辅助脚本
│   ├── archive/         # 归档区（capabilities/experiences/workflows/templates/docs，仅溯源不执行）
│   ├── experiences/     # 在途经验（反馈闭环：回写完成后归档）
│   ├── workflows/       # 流程库（development/task/automation）
│   ├── rules/           # 规则索引
│   └── templates/       # 生成模板（唯一事实源）
├── projects/            # 实际项目（与 workspace 共用一个 Git 仓库）
├── .agents/             # Agent 实体定义（不安装 Skill）
├── .claude/skills/      # Manager 与执行 Skill 的唯一安装根
└── .codex/skills        # 唯一兼容入口（目录软链接 → ../.claude/skills）
```

## Agent 执行规则

当开始一个新任务：

1. **查看已有 Workflow**（`.ai/workflows/`）
2. **优先复用已有 Workflow**
3. **逐 Phase 确认 Required Resources**：明确输入、输出和质量验收标准（by-name 引用 Skill/Agent）
4. **质量优先选择 Skill/Agent**：配置可补齐时先补齐；确实无法使用或验收失败才回退
5. **复用资源说明与脚本**：避免重复研究安装、更新、调用和排错方法

创建新项目一律通过 **Project Registry**，按项目模板生成 README、元数据和基础目录，与顶层共用 Git 仓库。项目默认沿用顶层 Agent 规则，项目级 AGENTS.md / CLAUDE.md 按需添加。`projects/` 是项目入口，不另建重复登记记录。

## 选择、执行与沉淀机制（V0.2.2）

- **默认路径**：Project → Workflow → Skill/Agent。Workflow 是 Markdown SOP，是流程的唯一事实源（Mission/Input/Output/Principles/Phase/Evolution Log）；Phase 的 Required Resources 直接 by-name 列出 Skill/Agent，不再引用已退役的能力契约层
- **真实执行**：Workflow 阶段 Required Resources 必须真实运行并留下独立产物；主 Agent 不得只读方法论后仿写结果
- **中间产物**：下游只消费已经验收的独立产物；最终内容可追溯到具体资源产物
- **质量优先**：采用 `best_available_resource` 而非 `local first`；按实际效果、输出质量、稳定性、依赖成本和维护成本选择（Workflow Phase 所需资源的任务级选择），来源只用于发现与追溯
- **资源可维护**：Resource Manager 记录来源、安装版本、调用、更新方法、注意事项、踩坑和资源目录内的辅助脚本，不修改外部安装实体；Agent 记录只存元信息
- **经验是反馈闭环**：项目日志永不进入资产库；Experience Curator 提炼会改变未来项目行动的结论并判定归属，经用户确认后回写至目标 Workflow SOP 或 Skill/Agent 记录（by-name 回填 `experience_refs[]`），回写完成后归档至 `.ai/archive/experiences/`

## 统一 Git 仓库

- 本仓库（`personal-ai-workspace/.git`）统一管理能力资产、注册元数据和 `projects/*` 项目源码
- `projects/*` 是工作区内的项目目录，不包含独立 `.git`；运行产物、大文件和本地状态按根目录 `.gitignore` 排除

## 技术约束

Markdown + YAML + Git。无数据库、无 Web UI、无评分/状态系统、无 Framework、无 Runtime。

仓库卫生：运行时状态（`.omc/`）永不提交；`.claude/skills` 是唯一 Skill 安装根，`.agents/skills` 禁止存在，`.codex/skills` 必须保持为指向 `../.claude/skills` 的单一目录软链接。
