# Capability 审计与资源选择升级

日期：2026-08-13  
范围：`.ai/capabilities/*/capability.yaml`、全局与项目 Workflow、上市公司研究视频真实项目证据、已安装及公开外部资源。

## 结论

- 原有 Capability：27 个。
- 目标 Capability：5 个：`data-acquisition`、`investment-research`、`content-production`、`media-production`、`quality-assurance`。
- 全局 `.ai/workflows/` 当前没有正式 Workflow；实际迁移对象是独立项目 `investment-research-system` 的 3 条 Workflow。
- 资源没有因 Capability 合并而删除。优秀 Skill/Agent 继续作为候选；字幕、配音、渲染、格式生成和打包降级为 Workflow 步骤或资源/工具动作。
- 没有创建 `automation`：扫描结果没有对应的长期专业方法论或多资源真实证据，不能为凑数量新增空 Capability。

## 原 Capability 处理结果

|原 Capability|处理结果|原因|
|---|---|---|
|company-business-analysis|合并到 `investment-research`|商业模式与护城河是投资研究专业模块，不需要独立资源路由层。|
|company-valuation-analysis|合并到 `investment-research`|估值方法专业但与行业、财务和投资逻辑共享输入与资源组合。|
|content-narrative-design|合并到 `content-production`|受众、冲突、Hook和结构是内容生产方法论的一部分。|
|content-quality-gate|合并到 `quality-assurance`|与研究交付、视频质量门共享独立检查、归因和回退语义。|
|financial-fraud-risk-assessment|合并到 `investment-research`|是财务完整性专项分支，且只有一个专用资源。|
|financial-report-generation|降级为 Workflow/Tool|核心是文件生成、图表和DOCX格式，不是长期分析能力。|
|financial-statement-interpretation|合并到 `investment-research`|三表和盈利质量是投资研究专业模块。|
|industry-research|合并到 `investment-research`|方法论完整且资源丰富，保留全部专业验收，但由上位领域统一选择资源。|
|investment-thesis-analysis|合并到 `investment-research`|多空逻辑是研究综合结果，不应再建立一层细粒度路由。|
|investment-video-script-generation|合并到 `content-production`|与长短视频脚本能力重复，且未被当前 Workflow 使用。|
|market-data|合并到 `data-acquisition`|原定义偏连接器调度；与检索、披露和证据治理合并后形成完整来源能力。|
|research-deliverable-validation|合并到 `quality-assurance`|与内容质量门重复，当前 Workflow 未使用。|
|research-evidence-ledger|合并到 `data-acquisition` 与 `investment-research`|来源分级进入底稿，结论映射进入研究结果，不再单设文档生成层。|
|research-master-document-generation|降级为 Workflow 步骤|只是把已验收模块按模板合成唯一母稿。|
|short-video-generation|合并到 `content-production`|与长视频、叙事策略共享事实源、资源和验收边界。|
|subtitle-alignment|降级为 Workflow/Tool|音频到SRT的声学对齐动作；`aligned` 验收保留在媒体生产步骤。|
|subtitle-generation|降级为 Workflow/Tool|脚本到SRT的格式转换；`estimated` 状态保留在内容生产步骤。|
|video-content-planning|合并到 `media-production`|场景、节奏、运动和信息密度属于长期媒体制作方法论。|
|video-material-planning|合并到 `content-production`|素材的叙事作用和证据映射属于内容资产设计。|
|video-publish-package|降级为 Workflow/Tool|目录、封面、文案和文件打包动作。|
|video-quality-check|合并到 `quality-assurance`|保留独立媒体 reviewer 与音视频验收方法。|
|video-rendering|降级为 Workflow/Tool|FFmpeg/Node/HyperFrames 的具体渲染动作。|
|video-script-generation|合并到 `content-production`|与叙事和短视频属于同一内容生产领域。|
|video-subtitle-generation|降级为 Workflow/Tool|与 `subtitle-generation` 重复且未被当前 Workflow 使用。|
|visual-asset-generation|降级为 Workflow/Tool|图表、SVG、PNG生成是媒体生产实现；来源验收保留在步骤。|
|voice-generation|降级为 Workflow/Tool|TTS或人工旁白导入是具体实现。|
|web-search|合并到 `data-acquisition`|搜索工具调度降级，来源核验、时效和主体消歧进入领域能力。|

## 目标 Capability 边界

|Capability|长期职责|不负责|
|---|---|---|
|data-acquisition|主体、市场数据、法定披露、网络来源、证据分级、冲突和降级治理|固定某个连接器或搜索引擎|
|investment-research|行业、商业、财务、估值、多空逻辑、风险、跟踪指标和统一母稿|下载文件、生成DOCX或拼接独立报告|
|content-production|内容策略、长短脚本、字幕初稿、素材叙事规划和事实映射|TTS、声学对齐、最终渲染|
|media-production|场景设计、旁白、原创视觉、正式字幕、成片和发布资产|独立放行自己的成片|
|quality-assurance|研究、内容、媒体的独立只读门禁、问题归属和回退|补研究、生成内容或直接修复上游|

## 资源选择机制

统一原则为 `best_available_resource`，禁止 `local first`。

1. 先按当前任务和 Capability acceptance 判断适配性。
2. 再比较实际效果、输出质量、稳定性、依赖成本和维护成本。
3. 从 workspace、已安装外部 Skill、skill-hub、find-skills 和 agent repository 发现候选；发现顺序不是选择优先级。
4. 可安全补齐的依赖先补齐；首选资源无法执行或结果未通过验收时才回退。
5. 每个候选在 Capability 中记录 `name/source/version/strength/weakness/test_result/recommended_usage`，并补充依赖与维护成本。
6. 未实测候选可以保留在本报告的发现池，但不能宣称优于真实项目已验证资源，也不能在没有资源记录时写入 Capability 引用。

## 上市公司视频案例验证

### investment-research

- `industry-analysis`（外部 GitHub，`tree-sha256:a2a363fca3d9`）在紫光股份及四家公司批量案例中完成六阶段行业研究、HTML交付和真实估值序列，是当前 A股任务的最佳领域适配资源。
- `buffett`（外部 GitHub/investagent，`tree-sha256:51aa7c2823bd`）四家公司均实跑；消费品牌解释力最强，技术公司必须由产业研究校准。
- `earnings-reader` 与 `financial-fraud-index` 完成三表、盈利质量和舞弊风险边界；弱信号没有被写成已证实舞弊。
- `investagent` 是覆盖最广的一体化外部候选，但完整链路依赖模型、数据和 Docker；入口与子 Skill 已验证，五模块端到端尚未完成，因此不以“全能”描述替代实测证据。
- 真实案例结论：A股主路径优先按任务组合 `industry-analysis`、`buffett`、`earnings-reader` 等专长资源；环境齐备时再用 `investagent`/`deep-analysis` 做综合或估值交叉验证。这个顺序来自效果与适配性，不来自本地/外部身份。

### content-production / media-production

- `codex-video-pipeline`（外部 GitHub，commit `aab79717ad692dd0b4d770778be28a2fa2b09a6e`）是发现范围内最完整的视频生产候选，覆盖证据、脚本、旁白、字幕、HyperFrames、封面、发布包和门禁。
- 其本地 unittest 2项通过，FFmpeg/ffprobe 就绪；当前主机缺 HyperFrames 且尚未创建生产配置，`readyForProduction=false`。因此它已从 reference 升为 execution candidate，但不能伪称真实成片端到端已完成。
- `research-content-producer` 在紫光股份内容层实测完成策划、长视频、5个短视频、estimated SRT和18项素材规划，独立质量门0阻断；在事实边界严格的上市公司内容任务上仍是当前稳定选择。
- `video-production-executor` 和 `video-quality-reviewer` 保留为可控本地编排与独立媒体复核资源；资源没有因数量压缩而删除。

## 外部候选发现池

|候选|来源/版本|优势|弱点|决定|
|---|---|---|---|---|
|InvestSkill|https://github.com/yennanliu/InvestSkill，公开 tag v1.11.0|26套prompt-only框架、零运行时、跨模型便携|美股优先、无数据引擎、质量依赖模型和来源|记录为发现候选；未安装、未做A股真实案例，不写入 Capability|
|finance-skills|https://github.com/himself65/finance-skills，公开 tag v9.1.0|社区与维护信号较强、金融工具覆盖广|偏美股与连接器，配置成本高于prompt-only方案|记录为发现候选；先做A股适配与安全验证再考虑注册|
|codex-video-pipeline|https://github.com/zoglmk/codex-video-pipeline，已安装 commit见上|当前发现中唯一与本项目端到端边界高度匹配的视频Skill|依赖多、公共仓库规模小、生产环境未齐|保留并提升为 content/media/QA execution candidate|

没有发现质量、范围和可验证性都明确优于 `codex-video-pipeline` 的公开上市公司视频生产 Skill，因此不为追求“外部参与”安装较弱替代品。

## 迁移与保留

- 3条项目 Workflow 已迁移到5个领域 Capability；每个步骤只声明1个目标能力。
- 原细粒度验收没有删除：来源定位、estimated/aligned、ffprobe、版权、证据映射和发布包完整性均保留在 Workflow acceptance 或新 Capability acceptance。
- 历史 logs、outputs、已确认 Experience 和旧版资源评估文档保留旧 Capability 名称，作为当时执行证据，不回写历史。
- 未触碰项目中已有的未跟踪 experience candidates 与 research-run logs。

## 剩余风险

- `codex-video-pipeline` 仍需安装/配置 HyperFrames 与生产提供方后完成一次真实上市公司端到端成片验证。
- `investagent` 的完整五模块流程仍需在同一公司、同一截止日下执行后，才能与当前专长资源组合做公平比较。
- 已确认 Experience 正文包含旧名称；按 Experience 沉淀规则，本次不静默改写历史知识，未来经用户确认后可补充 V0.2.0 适用映射。
