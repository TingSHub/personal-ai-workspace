---
name: work-for-me
description: 管理可复用 Workflow 并路由执行任务——按模板创建 Global/Project Workflow 的 Markdown SOP、索引元数据、查看修改、归档，以及任务开始时定位项目、匹配 Workflow 并按 SOP 逐 Phase 执行。当用户说“创建 workflow”“修改流程”“归档 workflow”，或开始一项任务需要按 SOP 执行、说“帮我做 X”时使用。
---

# Work For Me

管理服务项目交付的可复用流程，并在任务开始时把任务路由到正确的 Workflow。**Workflow Markdown 是唯一事实源，只索引不解释，路由只导航不决策**：注册侧负责索引 Workflow 元数据（位置/分类/项目关联/搜索/归档）；路由侧只做确定性查找与按 SOP 顺序执行（定位项目 → 匹配 Workflow → 读 SOP → 逐 Phase 真实执行）。不评分、不排序推荐、不调度、不做状态机；不负责资源安装、资源选择或 Experience 沉淀。

## 目录与约束

- Global Workflow：`.ai/workflows/<category>/<name>/workflow.md`
- Project Workflow：`projects/<project>/workflows/<name>/workflow.md`
- category ∈ development / task / automation
- SOP 按 `.ai/templates/workflow.md.template` 生成，字段从模板读取
- 默认路径：Project → Workflow → Skill/Agent
- 每个 Phase 的 Required Resources 按 by-name 直接列出 Skill/Agent
- Phase 的 Required Resources 必须真实执行并留下独立产物；下游步骤只消费已验收的产物
- 归档是显式操作，必须先取得用户确认

## create / create-project-workflow

1. 明确 Workflow 目标、输入、输出、Phase 和依赖。
2. 按 `.ai/templates/workflow.md.template` 生成 SOP，为每个 Phase 写明 Goal、Required Resources（by-name Skill/Agent 表）、Input、Output、Quality Criteria 与 Known Issues。
3. 检查 Required Resources 均可解析到 `.ai/skills/` 或 `.ai/agents/`（by-name）。
4. Project Workflow 创建后回填项目 `project.yaml` 的 workflows[]；Global Workflow 保存到对应类别目录。

索引记录：workflow-name / 位置 / 分类 / 项目 / 最近更新 / 每 SOP 的 Required Resources by-name 列表（索引不解释，内容以 SOP 为准）。

## view / modify

- `view`：读取索引记录：位置、分类、项目、最近更新与每 SOP 的 Required Resources by-name 列表。
- `modify`：只更新索引元数据；SOP 内容由 workflow 作者直接编辑 Markdown，本 Skill 不解释或改写。
- 发现资源问题时转交 Resource Manager；发现可复用经验时转交 Experience Curator。

## route

任务开始时（用户说“帮我做 X”，或主 Agent 判断任务应按 SOP 执行）确定性地把任务路由到正确的 Workflow 并按 SOP 逐 Phase 执行：

1. **定位项目**：读 `projects/README.md`、各项目 `README.md` 与 `project.yaml`，确定任务所属项目；跨项目的通用任务查 `.ai/workflows/README.md` 索引。
2. **匹配 Workflow**：先按名称精确匹配；无精确名时运行 `scripts/find-workflow.py <keywords>` 列出确定性候选（按关键词命中数排序，只列候选不推荐）。
3. **读 SOP**：完整读取 `workflow.md` 的 Mission / Input / Output / Principles / 全部 Phase。
4. **复合 Workflow**：SOP 的 Phase 用 `### Child Workflow` 或编排表逐行引用子 Workflow 时，按顺序进入每个子 Workflow 的 SOP 真实执行；父 Workflow 只编排顺序与交接，不复制子 Workflow 的资源表、产物路径与质量门禁。
5. **逐 Phase 执行**：Required Resources 按 by-name 解析到 `.ai/skills/` 或 `.ai/agents/` 并真实执行、留下独立产物；下游只消费已验收产物；Phase 的 Quality Criteria 逐条验收后再进入下一 Phase。
6. **候选确认**：多候选或无匹配时列出候选交用户确认，不自动选择、不擅自执行。

## archive

取得用户明确确认后删除 Workflow 实体，并同步项目或其他 Workflow 的 by-name 引用。若存在值得保留的方法或教训，先交 Experience Curator 生成 Candidate。

## Validation

- workflow.md 含 Mission/Input/Output/Principles/Phase 五类运行章节；不要求 Evolution Log 历史章节
- 每个 Phase 含 Goal/Required Resources/Input/Output/Quality Criteria/Known Issues
- Phase Output 包含项目相对路径和格式；多个资源并行执行时，产物必须能逐项识别其执行结果
- Required Resources 每项均可解析到 `.ai/skills/` 或 `.ai/agents/`（by-name）
- 索引记录与 SOP 内容一致，且索引不含解释性改写
- SOP 不包含状态或自动化调度字段
- 复合 Workflow 的 `### Child Workflow` 或编排表引用的 by-name 均可解析到对应 SOP
