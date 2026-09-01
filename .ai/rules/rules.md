# Workspace 规则索引（V0.2.2）

本文件是规则层的可读索引。权威关系：`CLAUDE.md`（Claude Code 入口）= `AGENTS.md`（Codex 入口镜像）> `.ai/system.yaml`（机器可读镜像）> 本索引。

## 核心规则

1. 执行任务前优先寻找并复用已有 Workflow（Markdown SOP）。
2. 不重复创建已有 Skill/Agent；使用 Resource Manager 管理资源。
3. 创建新项目使用 Project Registry。
4. 字段清单一律从 `.ai/templates/` 读取，禁止在 Manager 中复制字段定义。
5. Workflow / Skill / Agent / Experience 一律使用 by-name 引用，不用相对路径。
6. 顶层仓库与 `projects/*` 物理隔离；项目代码永不提交到本仓库。
7. 运行时状态不提交；`.codex/skills` 是指向 `../.claude/skills` 的单一目录软链接，禁止逐 Skill 建链或复制。

## 默认调用路径

`Project → Workflow → Skill/Agent`

- Workflow 是 Markdown SOP，是流程的唯一事实源：描述项目目标、输入/输出、原则和每个 Phase 的 Goal、Required Resources、Input、Output、Quality Criteria、Known Issues。
- Workflow Phase 的 Required Resources 直接 by-name 列出 Skill/Agent，不再引用已退役的能力契约层；workflow-registry 只索引元数据，不解释流程。
- Skill/Agent 是执行资源，只记录可靠调用所需信息和辅助脚本。
- Workflow 阶段 Required Resources 必须真实执行并留下独立产物；下游只消费已验收产物，主 Agent 不得只读方法论后仿写结果。
- 产物边界：下游步骤只消费已验收的独立产物，不消费私有推理或各资源自行生成的平行报告。

## 收尾与提交触发

- 用户说“收尾”“提交”“结束”“交付”“wrap up”或等价表达时，优先调用 Global Workflow `closeout-and-commit`。
- 收尾第一轮只生成 staging bundle、对话蒸馏和 Experience/文档/提交候选，不直接改正式资产或提交。
- 只有用户明确确认候选和文件范围后，才允许回写文档、运行最终交付质量门和创建本地 Git commit。
- 收尾默认不 push、不发 PR、不发布外部内容；实际外部事件和失败必须在 handoff 中保留。

## 质量优先选择

1. 采用 `best_available_resource`，不采用 `local first`；按实际效果、输出质量、稳定性、依赖成本和维护成本选择（Workflow Phase 所需资源的任务级选择）。
2. 候选发现覆盖 workspace、已安装外部 Skill、skill-hub、find-skills 和 agent repository；来源只用于发现与追溯，不决定优先级。
3. 缺少依赖或配置但能够安全补齐时，先按资源说明补齐，不因一次配置选择低质量资源。
4. 资源客观无法使用，或输出未通过验收时，才回退到下一适配候选。
5. 每个候选记录来源、版本、优势、劣势、实测结果、推荐用法及依赖/维护成本；未实测不得宣称优于已验证资源。
6. 候选调整必须由真实项目证据支持；不维护综合评分、可用状态、配置成本模型、生命周期或使用次数。

## Resource

- Resource Manager 统一管理 Skill 和 Agent（注册/查询/验证/归档）。
- 外部资源记录来源、当前安装 ref、调用方法、稳定要求、更新方式和更新后验证；资源重命名/删除时同步全量 Workflow SOP 的 Required Resources by-name 引用。
- `latest_version` 不进入资产；普通更新历史由 Git 提供。
- 调用注意事项、踩坑和脚本用法写在资源说明中。
- 辅助脚本放在对应资源的 `scripts/`，不再细分 Helper/Adapter/Wrapper。
- 本地增强不得直接修改外部安装实体。

## Experience 反馈闭环

1. 普通执行记录留在项目 `logs/`，永不进入资产库。
2. Experience Curator 在项目完成时判断经验是否会改变未来 Workflow SOP、资源调用、质量检查或可复用脚本，并判定归属（优先归入对应 Skill/Agent 的原则、调用说明或注意事项；确属项目运行契约时才归入 Workflow 现有章节）。
3. 合格内容按模板生成 Candidate，暂存于项目 `experience-candidates/`。
4. 用户确认后执行回写：将结论合并进目标 Skill/Agent 的现有原则、调用说明或注意事项，或项目 Workflow 已有的 Principles、Quality Criteria、Known Issues 等章节；按 by-name 回填 `experience_refs[]`，不得新增“回写条目”章节。
5. 回写完成后将经验文件移入 `.ai/archive/experiences/`；`.ai/experiences/` 只存未完成回写的在途经验，不无限堆积。
6. Experience 记录适用边界、证据和验证时的资源 `installed_ref`；不保存对话全文、偶发错误或无证据建议。

## 明确不实现

- Agent Runtime、DAG 调度或任务队列。
- 数字评分、状态机、成本模型或自动推荐系统。
- Helper / Adapter / Wrapper 分类体系。
- 数据库、向量库、Web UI、多用户、权限、云同步或 Marketplace。
- Experience 自动无限生成。
