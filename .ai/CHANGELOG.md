# Changelog

## v0.2.4

**项目合并与 Workflow 路由**：`video-publish-review` 并入 `investment-research-video`（Workflow 迁至 `projects/investment-research-video/workflows/`，复盘册/选题前瞻产物并入本项目 `outputs/`，复盘队列迁至 `docs/publish-review.md`；历史归档 `.ai/archive/**` 不动）。新增单入口编排 Workflow `investment-research-video-create`（阶段编排表：复盘 → 选题 → 研究 → 表达 → 制作发布 → 复盘闭环，只编排顺序不复制子 SOP）。`workflow-registry` 更名 `work-for-me` 并新增 route 能力（定位项目 → 匹配 Workflow → 读 SOP → 逐 Phase 真实执行；只索引与导航，不评分、不自动推荐），新增辅助脚本 `find-workflow.py`；全部引用与规则层同步。

## v0.2.3

**资产管理单文件化（Markdown 文档格式）**：Skill/Agent 描述层从 skill.yaml + SKILL.md 双文件合并为单文件 `.ai/skills/<name>/<name>.md`——纯 Markdown 文档（`# 标题` + `> 位置引用` + `## 元数据` 表格 + 调用说明正文），非 frontmatter 拼接；Agent 实体层补齐至顶层 `.agents/<name>.md`；resource-manager 与模板同步更新为 md 文档流程。

## v0.2.2

**架构收敛（四层 → 三层）**：Project → Workflow → Skill/Agent；Workflow 从 YAML DAG 转为 Markdown SOP（导演手册），Capability 层退役归档，新增按源定位的 Agent 层，Manager 瘦身，Experience 转反馈闭环。

**Changed:**

- Workflow 转 Markdown SOP：项目 3 个 workflow 全部转为 `workflow.md`（Mission/Input/Output/Principles/Phase[Goal/Required Resources/Input/Output/Quality Criteria/Known Issues]/Evolution Log）；旧 `workflow.yaml` 归档至 `.ai/archive/workflows/`（无删除）。新增 `.ai/templates/workflow.md.template`，旧 `workflow.yaml.template`/`capability.yaml.template` 归档至 `.ai/archive/templates/`。
- Capability 退役归档：5 个 capability.yaml 移入 `.ai/archive/capabilities/`；`.ai/capabilities/` 目录移除，不再承担执行层；capability-manager 从 `.claude/skills/` 卸载（SKILL.md 归档于 `.ai/archive/managers/capability-manager/`）；Workflow Required Resources 直接 by-name 列 Skill/Agent，零 Capability 引用。
- Agent 层按源定位登记：harness-100（源仓库为 agent harness 集合）由 `.ai/skills/` 随迁登记为 `.ai/agents/harness-100`（agent.yaml 元信息 + AGENT.md 调用说明）；investagent / claude-youtube / video-agent-skills 源为 skills 形态，保持 Skill 注册零改动。agent.yaml 只记录元信息，不复制 Agent 内部内容。
- Manager 职责：resource-manager 保留（Skill+Agent 注册/查询/验证/归档）；workflow-registry 保留简化（只索引元数据，Workflow Markdown 是唯一事实源）；experience-curator 改为反馈闭环（提炼→判定归属→回写→归档）；capability-manager 卸载。
- Experience 反馈闭环：`.ai/experiences/` 不再无限堆积；4 个经验文件（financial-analysis / financial-report-workflow / industry-research-methodology / research-master-content-pipeline）经回写判定后归档至 `.ai/archive/experiences/`（回写映射表见该目录 README）；`experience.md.template` 改为反馈闭环字段；回写条目标记 `## 回写条目（来源: {experience by-name}）`。
- 模板与规则同步：skill.yaml.template / agent.yaml.template 版本注释升至 V0.2.2；`rules.md` / `system.yaml` / 根 CLAUDE.md / AGENTS.md / README.md 同步三层规则；根 `capability-review.md` 归档至 `.ai/archive/docs/`。
- 版本统一：`.ai/VERSION` 0.1.5 → 0.2.2（与 CHANGELOG、system.yaml 对齐）。

**Decisions:**

- `.ai/system/` 目录不创建（M7 裁决）：`.ai/system.yaml` 已承担机器可读镜像（v0.2.2 更新后仍足够）；manager 职责说明存在于各 manager SKILL.md（唯一事实源）；新增空目录违反「不新增抽象层」。备选 `.ai/system/managers.md` 仅保留为文档化 fallback，未来若出现 manager 索引需求再建。

**Deferred（项目侧同步项）:**

- `projects/investment-research-system/CLAUDE.md` 的「Required Capabilities and Resources」清单与「每个 Workflow 步骤先按 Capability 验收」措辞，由项目侧在项目仓库提交 v0.2.2 三层同步（本版本不跨仓库修改项目文件）。

## v0.2.1

- 新增 `research-intelligence-agent`，在 `investment-research` Capability 内负责专业资源编排、证据冲突消解与完整研究综合，不新增 Capability 或 Manager。
- 将研究交付从面向内容派生的 Research Master Document 升级为十章 Full Research Intelligence Document，并强制独立 Base Case 与 `claim/source/date/confidence/notes` Evidence Ledger。
- 将 `research-content-producer` 收窄为 Content Production 资源；研究阶段不再考虑视频时长、阅读时间或传播压缩。
- Resource Evaluation 明确区分 executed、reference 与 not-run；优秀外部候选保留，不因未本地化而删除或伪报已测试。

## v0.2.0

- 将 27 个细粒度 Capability 收敛为 5 个长期领域能力：数据获取、投资研究、内容生产、媒体生产和质量保证。
- 文件生成、格式转换、字幕、配音、渲染和打包下沉为 Workflow 步骤或 Resource/Tool 动作。
- 资源选择改为 `best_available_resource`，按实际效果、输出质量、稳定性、依赖成本、维护成本和任务适配性选择，不采用 local first。
- Capability 候选新增来源、版本、优势、劣势、实测结果、推荐用法及依赖/维护成本记录；仍不引入综合评分或状态系统。

## v0.1.5

- 为 Capability 增加轻量 `execution_contract`，区分 execution 与 reference 资源，并强制 required resource 真实执行。
- 为 Workflow 步骤增加独立 `capability_result`，让研究模块先落盘、验收，再进入母稿与内容生产。
- 新增 `research-quality-gate`，以确定性检查验收研究完整性、证据、数字一致性、风险保留、SRT 和素材引用。
- 不增加评分、可用状态、配置成本或状态机。

## v0.1.4

**项目交付导向**：将资产管理从 Skill 直接调用升级为 Workflow → Capability → Skill/Agent 的质量契约与资源复用闭环，同时保持 Markdown + YAML + Git 的轻量实现。

**Added:**

- Capability 输入、输出、验收标准、资源适用场景与选择理由
- Agent 资源目录与模板
- Resource Manager、Capability Manager、Experience Curator 三个单一职责管理入口
- 外部 Skill/Agent 的安装 ref、更新方法与更新后验证约定
- 资源目录内辅助脚本机制
- Experience 模板与项目价值准入门槛

**Changed:**

- 默认路径改为 Project → Workflow → Capability → Skill/Agent
- Workflow 改为步骤级声明 Capability 与 acceptance
- 资源选择改为质量优先：配置可补齐时先补齐，确实不可用或验收失败才回退
- Experience 维护从多个 Registry 收敛到 Experience Curator

**Not included:**

- 评分、可用状态、配置成本或生命周期机制
- Helper / Adapter / Wrapper 分类
- Agent Runtime、数据库、Web UI、Marketplace 或自动推荐系统

---

## v0.1.3

**架构简化**：降低长期维护成本，避免资产数量膨胀。核心原则：默认简单，需要抽象时再增加复杂度。

**Removed:**

- Capability 强制层级——降为可选抽象层（默认路径 Project → Workflow → Skill）
- 项目级 Experience 记录（`projects/{name}/experiences/`）——改为 Experience Knowledge
- 4 个无竞争 capability（financial-analysis / report-generation / pdf-processing / github-operations——仅保留 market-data）
- skill.yaml 的 experiences 字段（经验统一进入 Experience Knowledge）

**Added:**

- Experience Knowledge：`.ai/experiences/{name}.md`（跨项目复用、经筛选、持续追加）
- Experience Candidate 暂存目录：`projects/{name}/experience-candidates/`
- `experience_refs[]`（skill.yaml / workflow.yaml，by-name 引用经验）

**Changed:**

- workflow.yaml 字段：`skills[]` 默认直接调用；`capabilities[]` 可选（仅多实现竞争）；恢复 goal/input/output；新增 experience_refs[]
- Experience 沉淀流程：Project Log → Candidate（暂存 experience-candidates/）→ 用户确认 → 追加 .ai/experiences/；Experience 不由 Manager 直接维护，由 Project 结束流程触发
- 项目目录集：experiences/ → experience-candidates/
- registry / 规则层 / 模板同步更新

**Not included:**

- Agent system（执行引擎/DAG/自动编排——由 Agent 负责执行）
- 平台化（多用户/权限/云同步/Marketplace）
- 自动推荐系统
- Experience 自动无限生成（必经用户确认）

---

## v0.1.2

**Removed:**

- Skill / Workflow lifecycle state machines (lifecycle status, evaluation scoring, usage statistics)
- Selection Rule / New Skill Rule（状态优先级依赖）
- Demo workflows（example-project、lifecycle-demo）
- Archived skill entities（cnfinancialscraper、financial-report-analysis——记录保留，实体删除）

**Added:**

- Capability 解耦层：`.ai/capabilities/` 5 个初始能力（financial-analysis / report-generation / pdf-processing / market-data / github-operations）+ 维护三规则（无专用 Manager）
- Experience 沉淀机制：Project Log（`logs/`，永不进资产库）→ Experience Candidate → 用户确认 → `experiences/` 七字段单份记录 + 引用回填（by-name + 日期）
- `capability.yaml.template`；`.ai/rules/` 规则索引
- workflows 分类：development / task / automation

**Changed:**

- 字段精简：skill.yaml（去 status/evaluation/usage_count/last_used，增 usage[]）、workflow.yaml（去 status/lessons 等，增 capabilities[]）、project.yaml（name/description/workflows[]）
- `.ai/skills/` 元数据文档 README.md → SKILL.md（11 个 active skill 内容随迁）
- project.yaml 上移项目顶层（`.ai/` → 项目根）；artifacts/ → outputs/ + docs/
- 归档语义：删除 skill 实体、保留记录（无状态标记）
- registry 三件套指令重写（无状态机/评分，含 Capability 维护规则与 Experience 流程）
- 规则层对齐：CLAUDE.md / AGENTS.md / system.yaml / README（Capability 选择机制 + Experience 沉淀流程）

**Not included:**

- Agent system（执行引擎/DAG/自动编排——由 Agent 负责执行）
- 平台化（多用户/权限/云同步/Marketplace）
- 自动推荐系统

---

## v0.1.1

**Added:**

- Skill lifecycle management
- Workflow lifecycle management
- Skill evaluation
- Asset status tracking

**Changed:**

- Registry upgraded from simple registration to lifecycle management

**Not included:**

- Agent system
- Capability system
