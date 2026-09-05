# Workflow: investagent-video-by-hyperframes

> 位置: Project: projects/investment-research-video/workflows/investagent-video-by-hyperframes/workflow.md

## Mission

企业研究内容视频的纯 HyperFrames 生产链路：Phase 1 按批准问题选择研究资源 → Phase 2 Financial Editor Agent 编辑综合（Editorial Master）→ **Phase 3 起由 HyperFrames 技能体系接管**（router 意图捕获与创作路由 → creative/core/animation 创作 → media-use 配音与媒体 → CLI 确定性渲染）→ 最终 MP4。

服务对象：对上市公司研究感兴趣的普通投资者。产出「看懂公司/行业/周期/财务/经营变化/估值分歧/风险」的企业研究内容视频——**不是投资推荐**。

核心约束：Phase 2 之后不经过 Finance Presentation Agent / html-ppt-skill 中间层，不依赖外部 TTS / Forced Alignment 资源；Composition、动画、媒体、音频轨道、字幕与确定性执行全部由 HyperFrames 原生能力在同一 Composition 内完成。

**形态选择（2026-08-22 起,播客为默认）**：

| 形态 | 适用 | Phase 3 SCRIPT | Phase 4 Composition |
|---|---|---|---|
| **播客形态(默认)** | 双人对话/交锋/争议性选题 | 双人对话稿(`[林知微]`/`[顾慎言]` 标记,回合式) | 双人卡片视觉 + 版式系统 + 双音色 |
| 解说形态(可选) | 单口解说/深度研究 | 单口旁白 | 数据视觉 + 单音色 |

两种形态共享 Phase 1/2(研究/编辑)、Phase 5/6(渲染/QA)与全部边界原则。形态在 Phase 3 入口决策,记录于 routing-decision.md。

与 `investagent-video-production` 的边界：后者接收已验收的 HyperFrames-native Presentation（Finance Presentation Agent 产物）做音频时间化编译；本 Workflow 从 Editorial Master 直接进入 HyperFrames 创作，中间层全部由 HyperFrames 技能体系承担。

## Input

| 字段 | 必填 | 说明 |
|---|---|---|
| company_id | 是 | 公司代码（如 600519） |
| company_name | 是 | 公司名称（如 贵州茅台） |
| research_date | 是 | 运行日期（YYYY-MM-DD），同时是输出目录层级 |
| topic_card | 是 | 用户已批准的 `topic-forward-lead` 结构化选题卡；这是本 Workflow 的唯一视频输入，包含主题范围、观众问题、内容承诺、证据线索、叙事方向和 `review_constraints[]`；Markdown 交接摘要仅作阅读视图 |
| 已有研究产物 | 否 | 若有当日/近期原生产物，可复用并如实记录，避免重跑 |

## Output

| 产物 | 位置 | 格式 |
|---|---|---|
| 本期选用的研究原生产物 + findings-summary | `outputs/companies/{company_name}/{research_date}/research-materials/{skill}/` | skill 原生格式（HTML/markdown/多文件），不强制转换 |
| Editorial Pitch | `outputs/companies/{company_name}/{research_date}/editorial/01-editorial-pitch.md` | markdown（主命题、读者承诺、关键问题、张力与反证） |
| Editorial Master | `outputs/companies/{company_name}/{research_date}/editorial/02-editorial-master.md` | markdown（视频创作消费的企业研究母稿） |
| 冲突与编辑决策记录 | `outputs/companies/{company_name}/{research_date}/editorial/unresolved-conflicts.md` | markdown（已裁决 + 未裁决清单；未裁决不得进入视频） |
| Phase 2 执行记录 | `outputs/companies/{company_name}/{research_date}/editorial/phase2-execution.md` | markdown（资源、输入、输出与验收状态） |
| HyperFrames Brief | `outputs/companies/{company_name}/{research_date}/video/brief/BRIEF.md` | markdown（意图捕获与创作路由确认） |
| Narration 锁稿 | `outputs/companies/{company_name}/{research_date}/video/script/SCRIPT.md` | markdown（由 Editorial Master 派生的最终口播文本，唯一文本 Source of Truth） |
| Composition 项目 | `outputs/companies/{company_name}/{research_date}/video/project/` | HyperFrames 项目（`hyperframes init` scaffold：index.html、assets、hyperframes.json） |
| 最终视频 | `outputs/companies/{company_name}/{research_date}/video/renders/final.mp4` | MP4 |
| 视频 QA | `outputs/companies/{company_name}/{research_date}/video/qa/video-qa.md` | markdown |
| 执行记录 | `outputs/companies/{company_name}/{research_date}/video/hyperframes-execution.md` | markdown（资源 by-name、installed_ref、各 Phase 产物与验收状态） |

## Principles

- 本 Workflow 只负责研究 → 编辑 → HyperFrames 路由/创作 → 渲染 → QA 的项目顺序与交接；通用执行纪律由所列 Skill/Agent 资产记录负责。
- 项目产出仍是企业研究内容，不是投资推荐；Phase QA 必须检查目标价、评级、买卖建议、未解决冲突和内部执行信息没有进入公开产物。
- `SCRIPT.md` 由 Editorial Master 派生并锁定，是全片口播文本唯一 Source of Truth；字幕只能从它派生。
- 时长和形态由 HyperFrames router 根据 Editorial Thesis 与项目输入裁决；不在 Workflow 中写死内容模板。
- 不创建新 Agent 类型；内容结构服从 Editorial Master，不服从固定页面或章节模板。
- `topic_card` 必须来自用户批准的 `topic-forward-lead` 结构化产物；其中的 `review_constraints[]` 是待验证建议。编辑研究后可不采用，最多保留一个主要内容实验；发布时间等发布实验交发布环节。

## Phase 1: research — 按问题选择研究

### Goal

按已批准问题选择研究资源，产物原格式保留；必要时由 `cninfo-connector` 补充一手披露取证。产品实力核验能力、采用与替代难度，周期题核验供需、库存与产能，盈利质量题再深入三表。研究交付核心答案、最强反证、证据缺口和停止条件。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| industry-analysis | skill | 条件使用 | github · tree-sha256:a2a363fca3d9 | 行业/产业链 6 阶段（产业链图谱/三高矩阵/标的映射）；产出原生 HTML 可视化报告；要求联网检索，估值需真实来源 |
| industry-cycle-analysis | skill | 条件使用 | github · tree-sha256:9e9b5dd25f8e | 供需周期/资本周期/市场预期阶段；产出深研 markdown + 证据台账；用 skill 自带验证器 strict full 校验 |
| investagent | skill | 条件使用 | github · tree-sha256:51aa7c2823bd | **内容生产链路只跑「研究+数据」范围**（见 Known Issues）：Buffett 定性 + UZI 22 维 + tushare 采集；跳过 TradingAgents/QuantDinger |
| cninfo-connector | skill | 条件性必选 | internal · installed_ref: internal | A 股年报/半年报/季报/公告的一手披露取证；当关键财务、经营或口径冲突需要官方核验时启用；下载 PDF 并保存到 `official-information/`，不得把仅下载成功当作正文已核验 |

### Input

- 任务参数：company_id / company_name / research_date
- 必选：用户批准的 `topic-forward-lead` topic card；不得直接以 publish-review 的 attribution 或候选池启动视频生产
- 若 topic card 含 `announcement_evidence`，研究阶段必须先读取该结构化公告索引，再按其中的 `official-information` 归档要求下载、校验并定位正文；该索引是取证入口，不是正文事实源
- 研究目标清单（见 Goal）
- 环境说明：无用户确认场景下自主执行；tushare 凭证从 workspace 根 `.env` 自动加载
- 一手取证触发条件：关键财务/经营数字、披露口径冲突、或研究结论依赖公司公告时，启用 `cninfo-connector`；无需官方核验时记录为未触发及原因

### Output

- `outputs/companies/{company_name}/{research_date}/research-materials/industry-analysis/`：原生报告（HTML）+ findings-summary.md
- `outputs/companies/{company_name}/{research_date}/research-materials/industry-cycle-analysis/`：原生报告（markdown）+ findings-summary.md
- `outputs/companies/{company_name}/{research_date}/research-materials/investagent/`：原生报告 + UZI 产物 + 数据留档 + findings-summary.md
- `outputs/companies/{company_name}/official-information/`：`cninfo-connector` 获取到的年报、中报、季报、公告等公司级长期官方资料存档，不带研究日期；同行公司使用同级目录，不放进当前公司 run
- 官方文件统一命名为 `{ts_code}_{period}_{document_type}_{announcement_date}.pdf`；获取前先检查本地文件和 `download_record.json`，命中且正文可验证时直接复用，不重复搜索或下载

- findings-summary 契约：①关键数据点→来源索引（机构/媒体具体名称）；②待验证/存疑数据单列（含口径矛盾标注）；③执行状态如实说明（真实执行 vs 降级 vs 排除）；④不含决策/回测结论；⑤不含具体目标价、买卖评级、操作区间——盈利一致预期（净利/EPS）作为市场预期允许保留

### Quality Criteria

- 每个被选用 Resource 真实执行并留下独立产物；未选用资源记录与本期问题无关的理由。若触发 `cninfo-connector`，必须逐项记录搜索与下载结果、官方文件存档及正文定位；若 topic card 提供公告索引，必须逐家公司记录主路径/兜底路径和下载状态
- findings-summary 满足上述 5 项契约
- 数据来自真实接口/检索，无模型记忆补数；关键财务/经营事实优先回指公司官方披露；降级路径如实标注，未执行不得写成已执行
- 原生产物保留原生格式，未为视频强行改造

### Known Issues

- **investagent 范围**：完整流水线约 40% 模块（TradingAgents 决策、QuantDinger 回测、买点/卖出清单）产出内容边界禁止内容——启动即限定「研究+数据」，不跑完再裁剪（经验: `investagent-research-only-scope`）
- **cninfo-connector 使用边界**：它是官方资料取证连接器，不是第四份独立研究报告；只在关键事实核验或口径冲突时启用。搜索结果需保留 `announcementId` 与 `adjunctUrl`，下载成功后还要确认 PDF 正文可检索并记录页码/段落定位（资源: `cninfo-connector`）
- 执行预算（实测）：industry-analysis ≈ 8 分钟 / industry-cycle-analysis ≈ 18 分钟 / investagent ≈ 22 分钟（opus）。并行执行，用 `findings-summary.md` 作为衔接层
- 环境问题：UZI 渲染需 playwright chromium（国内网络下载易超时，数据产物不受影响）；FRED 无 key 诚实降级；雪球端点需登录（腾讯/baostock 兜底）

## Phase 2: editorial-synthesis — Financial Editor Agent 编辑综合

### Goal

由 Financial Editor Agent 接管 Phase 1 已选研究的 findings-summary。Agent 必须先理解主体、行业与当前变化，再自主形成一个 Editorial Thesis，围绕该主命题决定哪些问题值得讲、哪些资料应删除或压缩，并完成事实核验、口径分层、冲突裁决、同行坐标、反证寻找与企业观点表达。

本 Phase 的交付目标是形成一份可以被 Human Editor 审阅、被 HyperFrames 创作链路直接消费的 Human-first、Presentation-ready 企业研究母稿。它研究企业状态与经营逻辑，不输出投资观点、买卖建议、目标价或交易策略。无法验证或无法裁决的内容必须留在内部决策记录中，不得进入 Editorial Master 的事实正文。

默认顺序：

```text
已选 findings-summary
↓
理解公司与当前变化
↓
形成 Editorial Thesis
↓
建立 Evidence Chain
↓
主动寻找反证
↓
核验与裁决关键冲突
↓
生成 Editorial Pitch
↓
生成 Editorial Master
↓
标记未裁决项与重要不确定性
```

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| financial-editor-agent | agent | 必选 | workspace internal · installed_ref 以 `phase2-execution.md` 记录 | 负责 Editorial Thesis、Editorial Pitch、Editorial Master、证据链、冲突裁决与企业研究边界；不输出证券交易建议 |

### Input

- Phase 1 本期选用且已验收的 findings-summary.md
- 必要时可回看 Phase 1 原生产物与其中引用的一手来源，专门用于核验关键冲突；不得把未核验的单源估计伪装成事实
- 任务参数：company_id / company_name / research_date

### Output

- `editorial/01-editorial-pitch.md`：Working Title / Subtitle、Editorial Thesis、Why Now / Reader Promise、Key Questions / Key Tensions、Competitive Context、Major Evidence / Counter Evidence
- `editorial/02-editorial-master.md`：Final Title / Final Subtitle、以 Editorial Thesis 为中心、结构自由的完整企业研究内容、可追溯的 Sources、Editorial Notes（Evidence Decisions / Conflict Decisions / Important Uncertainties）
- `editorial/unresolved-conflicts.md`：已裁决清单（冲突项/各方口径/裁决结果/依据）与未裁决清单（冲突项/无法裁决原因/对 Editorial Master 的排除处理）
- `editorial/phase2-execution.md`：financial-editor-agent 的 installed_ref、输入清单、输出清单、执行状态与验收结果

### Quality Criteria

- financial-editor-agent 真实执行并留下上述四份独立产物；`phase2-execution.md` 能按 by-name 识别资源与输入/输出
- Editorial Pitch 有且只有一个可复述的 Editorial Thesis，并明确 Why Now、Reader Promise、Key Questions、Key Tensions、Major Evidence、Counter Evidence
- Editorial Master 不是 findings-summary 的拼接：结构服从公司与问题，正文形成 Evidence Chain，并给出基于证据的企业判断
- 关键事实、数字、因果关系与同行比较均可追溯到来源；Fact / Estimate / Opinion / Inference 不混写
- 冲突项逐条记录，裁决有依据（算术自洽校验、一手来源优先、口径分层）；口径不同但均可靠时并列呈现并明确口径
- 未裁决项不得进入 Editorial Master 的事实正文；如仍需保留上下文，必须改为定性表述并在 Editorial Notes 标明不确定性
- Editorial Master 与所有内部记录均遵守企业研究边界：不得出现买卖建议、目标价、操作区间、仓位、交易策略或投资推荐式结论

### Known Issues

- 多源口径管理是固定成本（实测：裁决 12 项 + 未裁决 6 项，约 15 分钟）——不要压缩，数字可信度是研究内容底线（经验: `multi-source-conflict-check`）
- Financial Editor Agent 的 Editorial Master 可能比原冲突清单更强地删减材料；删减是编辑判断，不代表 Phase 1 研究丢失，完整研究仍保留在原生产物中
- Workflow 无 Human Editor 阻塞式确认点；如需人工复核，复核对象是 Editorial Pitch，而不是让下游自行重写 Thesis
- 常见口径陷阱：营业总收入 vs 营业收入；全年 vs 单期每股分红；个股 PE vs 指数 PE；A 股上市公司 vs 全国规上统计；机构目标价不同样本差异
- **算术自洽校验是最强裁决工具**：Q2 单季 = H1 − Q1；分红率 × 净利 ÷ 股本 ≈ 每股分红
- 无法裁决的处理：风险描述改定性表述，不呈现具体数字（如社会库存规模）

## Phase 3: hyperframes-intake — Router 接管与创作路由

### Goal

hyperframes 主技能入口接管 Phase 2 已验收的 Editorial Master，完成意图捕获与创作路由：按主技能入口的状态机与意图层确认 angle / length / destination，建立 BRIEF.md，默认路由到官方 `/faceless-explainer` 创作 workflow（router 保留最终裁决权，可因内容体量、叙事形态或用户偏好改路由），并将 Editorial Master 派生为口语化、锁定版 narration（SCRIPT.md / VO_MODE 逐字稿）。

**时长纪律在本 Phase 落地**：以 Editorial Thesis 的最短完整叙事为目标规划长度；超出 faceless-explainer 硬上限（约 3 分钟）时，router 必须裁决拆分方案（按 Scene 分批 / 多 Composition 序列 / 换 slideshow 或 general-video 路由），裁决记录在案，不得无裁决堆时长。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| hyperframes | skill | 必选 | github · c32b804 | Phase 3 起的统一接管入口：意图捕获、BRIEF.md、创作路由（默认 `/faceless-explainer`）；领域子技能（hyperframes-core / -creative / -animation / -audio / -cli / -registry、media-use）与 CLI 按入口指令随用随载，不单列为独立资源 |
| finance-content-engineering | skill | 可选 | internal | narration 口语化规则与零漂移校验（百分比直读/大数读法/单句 ≤25 字/书面语→口头语；禁止近似化、不得新增/丢失数字）；只作规则与校验来源，不改写链 |

### Input

- Phase 2 Editorial Master（已验收）
- 必选：已批准的 `topic_card` 及其来源文件
- Phase 2 Editorial Pitch（用于核对主命题与内容承诺）
- Phase 2 冲突与编辑决策记录（unresolved-conflicts.md）
- 任务参数：company_id / company_name / research_date
- 可选：destination（YouTube 16:9 为默认）、speaker 偏好、已有 narration 音频

### Output

- `video/brief/BRIEF.md`：意图确认文档（angle / length / destination / 内容来源），后续每个创作阶段只读此文件
- `video/review-constraint.md`：从 topic card 的 `review_constraints[]` 读取复盘候选，记录本期适用性判断、具体实现、观察指标与不采用理由（如不适用）
- `video/script/SCRIPT.md`：由 Editorial Master 派生的最终口播文本（口语化已完成、事实零漂移已校验），锁定为全片唯一文本 Source of Truth
- `video/routing-decision.md`：路由裁决记录（选中的创作 workflow、超长拆分方案或路由变更依据）
- 更新 `video/hyperframes-execution.md`（本 Phase 执行状态）

### Quality Criteria

- hyperframes 主技能真实执行并留下 BRIEF.md、SCRIPT.md、routing-decision.md 独立产物；execution 记录能按 by-name 识别资源与 installed_ref
- BRIEF.md 覆盖 angle / length / destination 三要素；angle 由 Editorial Master 自身结构推导，不是模板套话
- SCRIPT.md 遵守 Editorial Lock：不新增研究事实、不改变结论强度、不引入未经编辑层审议的因果；数字、因果、比较与 Editorial Master 可追溯一致；违反内容边界（目标价/评级/买卖建议）零出现
- narration 口语化完成且事实零漂移：禁止近似化（「36.1%」不得写成「超过三分之一」）、不得新增/丢失数字（数字转中文读法与时间指代「去年/今年」允许）
- 路由裁决与时长规划有依据：目标长度落在所选 workflow 的合理区间；超长内容有明确拆分或路由方案，不遗留「先做出来再看」的悬浮决策
- 视频计划中的每个 Scene 有一个核心观点，重要口播必须有可实现的视觉锚点

### Phase 3 project constraints

- **开场门禁**：前 10 秒说明观看价值，可用观点、案例、事件、技术演示、事实反差或问题；正文必须兑现，不用关键词或固定数字数量代替内容审阅。
- **理解门禁**：只对理解关键的数字做数量级、生活参照或对比翻译；没有必要数字的 Scene 不强制插入数据类比。
- **引述式表达(补回冲击)**：允许引述券商目标价/机构预测作为市场预期(标注「市场预期」+来源,口径一致),禁止自创目标价/评级/买卖建议(`boundary-rewrite` 三分类判定)
- **多空局可选形态**：争议性选题(双方都有可辩护证据)可切换 `debate-rounds` 预编排——SCRIPT 写死双方论点 + 双音色 TTS 分饰 + 画面双方卡片交替;默认形态仍是叙事弧(企业研究定位)

### Phase 3 podcast format constraints

- **播客形态(默认)全流程设计**:
  - **Phase 3 双人对话稿**:按 `debate-rounds` skill 预编排——矛盾立题 → 回合交锋(「你这话没错,但…」/连环新证据/类比降维)→ 收束 → 双总结 → 互动钩子;每句带说话人标记(`[林知微]`/`[顾慎言]`),口语化规则不变
  - **Phase 4 双人视觉**:左右双人卡片(名字+立场标签「多/空」)、当前说话者高亮、数据卡片随对话弹出、说话人切换=高亮切换;字幕带说话人前缀
  - **Phase 4 版式系统**(账号资产定稿,见 `account-profile/design.md`):①左上角说话人胶囊(林知微粉/顾慎言黄);②顶部账号标识+右上角两行免责声明;③页标题=大编号+蓝色提问式;④内容区优先使用图表，其次指标卡/表格，最后才是文字;⑤字幕=当前说话人颜色的粗体字幕;⑥底部导航条(话题列表,当前话题高亮)。每页固定元素不侵入内容区
  - **TTS 双音色交替**:按 `[标记]` 分段合成(林知微/顾慎言,资源见顶层 `.ai/assets/voices/`),交替拼接,segments.json 记录每句时长
  - **时长纪律放宽**:播客形态对话节奏可适当延长(参考 22 分钟多空局),仍保持 Audio First(Scene 时长 = 音频时长)
- **引用通用 Workflow**:音色克隆 → `voice-clone-from-tts`(Global);参考视频解析(转写/抽帧/视觉分析)→ `video-content-extraction`(Global);本工作流只消费其产物

### Phase 3 podcast profile constraints

- **形态变更:双人播客为默认形态(2026-08-21 起)**——从头到尾两位主持人对话(顾慎言=风险/反证视角 + 林知微=数据/趋势视角),替代单口解说叙事弧;`debate-rounds` 从"可选形态"升级为默认(叙事弧仍可选用)
- **品牌音色资源(2026-08-22 定稿)**:林知微(女声)= 数据/趋势方,顾慎言(男声)= 风险/反证方;资源 key 和配方见顶层 `.ai/assets/voices/`;账号共享环境为 `/home/henry/personal-ai-workspace/.venv-voxcpm/`
- **TTS 双音色合成**:Phase 4 按 SCRIPT 说话人标记(`[林知微]`/`[顾慎言]`)分段合成、交替拼接;使用 workspace 根目录 VoxCPM 环境;VoxCPM2 终极克隆 API:`generate(text, prompt_wav_path=克隆参考, prompt_text=片段文本)`;克隆参考片段规范见顶层 `.ai/assets/voices/*/ASSET.md`
- **SCRIPT 双人对话稿规范**:Phase 3 产出对话格式(每句带说话人标记、回合式「你这话没错,但…」、连环新证据、类比降维),非单口旁白;口语化规则不变(单句 ≤25 字、数字零漂移)
- **双人视觉规范**:Phase 4 composition 左右双人卡片(名字+立场标签「空/多」)、当前说话者高亮、数据卡片随对话弹出、说话人切换=高亮切换;字幕带说话人前缀
- **TTS 选型升级**:VoxCPM2(本地 GPU,Apache-2.0)替代 edge-tts 为首选,豆包 TTS(seed-tts-2.0)作为克隆参考合成源(`scripts/doubao-voice-ref.py`,VOLC_API_KEY);edge-tts 降级路径保留

### Known Issues

- 本机未预装 hyperframes CLI：首次 `npx hyperframes init` 拉取较慢（实测 auth 8m10s），耐心等待或预拉取；init 时项目自动 pin CLI 版本，后续渲染按 pin 执行，保持可复现（资产记录: hyperframes）
- HeyGen key 缺失时官方 TTS/BGM 能力不可用——media-use 提供 HeyGen free-usage 路径与本地 Kokoro 备选；无 key 场景在 Phase 4 如实降级并记录
- faceless-explainer 上限约 3 分钟：企业研究内容体量超过时，宁可拆 Scene/分批，不要压缩关键认知过程（继承 Presentation Completeness 思想）；压缩文字和次要证据，不压缩理解 Thesis 必需的背景、机制、比较、反证
- 口语化与零漂移校验是固定成本，不要跳过（经验: `notes-spoken-polish`、`narration-content-lock`）
- 中文 TTS 发音（多音字、数字读法）需在 Phase 4 试音验证；voiceover 与字幕时间基准一律来自真实音频时长，不估时
- **HeyGen 可选升级路径（2026-08-20 决策：暂不安装，先记入工作流）**：media-use 的 HeyGen free-usage path 是配音/BGM/素材的**默认优先路径**，未安装/未 auth 时按经验 `video-pilot-media-degradation` 降级（edge-tts + 无 BGM）。升级方式：安装官方 HeyGen CLI（developers.heygen.com/cli，需 ≥v0.3.0）+ 用户执行 `heygen auth login --oauth`（浏览器授权一次，**免费订阅额度**；`--api-key` 计费不推荐）。收益：专业 TTS 音色、BGM/SFX/图片素材库检索、avatar 视频。升级后 `media-use scripts/resolve.mjs --doctor` 验证，并回归一条样片。成本：需注册 HeyGen 账号；免费额度有月度上限

## Phase 4: hyperframes-authoring — Creative、Composition 与 Media

### Goal

按 BRIEF.md 与 SCRIPT.md 创作 HyperFrames Composition：hyperframes-creative 定设计方向（设计 spec / 色板 / 排版 / beat 规划）→ hyperframes-core 建立 Composition 项目（STORYBOARD → index.html，Scene 以 `data-*` 声明时序、seek-safe）→ hyperframes-animation 实现确定性动画 → media-use 解决 voiceover TTS、BGM、素材 resolve 与字幕派生。所有视觉、动画、音频轨道、字幕与媒体写入**同一 Composition**。

Audio First：先按 SCRIPT.md 逐 Scene 合成配音，用真实音频时长确定 Scene 起止，再写画面时序；不得先设计画面后配音。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| hyperframes | skill | 必选 | github · c32b804 | 统一创作层：hyperframes-creative（设计 spec/beats）、hyperframes-core（composition 契约/`data-*` 时序/tracks/sub-compositions）、hyperframes-animation（seek-safe 动画）、hyperframes-audio（混音）、hyperframes-registry（catalog/add 复用 blocks）、media-use（voiceover TTS、BGM、SFX、字幕、素材 resolve）按入口指令加载 |
| static-html-qa | skill | 可选 | internal | 创作中期对 Composition HTML 的内容边界与数值一致性抽检（check-content-boundary / check-numbers），发现问题早于渲染暴露 |

### Input

- Phase 3 BRIEF.md、SCRIPT.md（已验收）
- Phase 2 Editorial Master（事实与数值回查来源）
- Phase 3 routing-decision.md（选中的创作 workflow 与拆分方案）

### Output

- `video/project/`：HyperFrames 项目（`hyperframes init` scaffold：index.html、assets、hyperframes.json）
- `video/project/STORYBOARD.md`：Scene 级计划（每 Scene 核心观点、视觉、动画、时长来源）
- `video/design/frame.md`：设计 spec（色板/字体/风格 token）
- `video/audio/`：voiceover 音频（逐 Scene + 全片）、BGM/SFX
- `video/project/assets/`：Composition 本地化媒体依赖
- `video/subtitles/`：由 SCRIPT.md 派生的字幕
- 更新 `video/hyperframes-execution.md`（资源 by-name、installed_ref、各产物与验收状态）

### Quality Criteria

- 每个 Scene 有唯一、稳定的 Composition/Scene ID；`data-start` / `data-duration` / audio track timing 写入同一 Composition；不另建外部视频时间轴或截图序列
- 每个 Scene 有一个核心观点；重要 narration 有可定位的视觉锚点；画面不是字幕墙
- seek 到任意时间状态可复现：不依赖 wall-clock、随机数、`setTimeout` 驱动核心动画或无限循环；动画按 hyperframes 确定性规则实现
- 配音与 SCRIPT.md 一致：只允许技术性读音处理（SSML、数字读法映射、停顿参数），不得新增/删除/改写事实与句意；全片音色统一；Scene 时长来自真实音频探针，不估时
- 字幕由 SCRIPT.md 派生，可断句加时间，不另写文案
- 每 Scene 时间范围无重叠、无空洞（除非 BRIEF 明确定义间隔）；master duration 等于全部 Scene 时间范围
- 视觉媒体、音频轨道、字幕与动画均可被 Composition 直接执行；不使用 HTML → PNG → Video 截图转视频路径
- Composition 通过 hyperframes `lint`；数值与内容边界抽检无新增违规

### Known Issues

- 大字号元素与标签间距、track 重叠、对比度是高频 check 失败点；以 `npx hyperframes check` 报错（元素 id + 时间戳 + 修复建议）为准迭代，15 分钟一轮「去装饰+加信息」级修改（资产记录: hyperframes）
- 动画一律用「数据动作」（条生长、线描画、数字逐位滚动、对比翻转）+ 硬切转场（数据新闻标准），禁止淡入淡出装饰；同屏数字峰值 ≤3，大数字 220-240px + 标签层级
- 图表用手写 SVG + 确定性动画，精确比例，不引入 ECharts 类重框架
- 中文语音对齐质量依赖 TTS 清晰度；带 BGM 混音的 voiceover 不得作为对齐基准，先干音对齐再加 BGM
- media-use 的 TTS 生成后必须探针验证时长与可解码性；无法稳定生成时如实降级并记录，不伪装已生成
- 旧实验参考实现：`projects/investment-research-system/experiments/listed-company-video-production/outputs/web/hyperframes/`（v1/v2 全源文件，Audio First + 手工插入音频的方法可复用）

### Phase 4 media fallback constraints

- **配音降级路径（2026-08-20 试点实测）**：media-use `resolve.mjs --doctor` 显示 heygen 缺失时，用项目已验证的 `scripts/tts-edge.py --notes <txt> --outdir video/audio --flat` + 08-19 的 `.venv-edge-tts`（EDGE_TTS_PYTHON 指定）；doctor 证据留痕，不伪装已生成
- **tts-edge.py 按空行分段**：`--notes` 模式按 `\n\n` 分段，段间无空行会把全部旁白合成 1 段（实测 9 段 → 1 段 207.9s）——每 Scene 一段、段间必留空行，前缀 `P\d+:` 会被剥离
- **时长裁决**：实测超路由裁决点 <4%（202.7 vs 195s）不拆分、记录裁决即可；叙事完整性优先于硬上限的轻微越界
- **Audio First 验证**：视频总时长 == narration 总时长（ffprobe 双向核对）即 Scene 时长分配正确；分段响度 -19~-20dB 一致为通过

### Phase 4 CLI constraints

- **init 首次拉取 ~15 分钟**（onnxruntime-node postinstall 大体积运行时）；`--example=data-chart` 有缺陷（缺 index.html）但不影响项目骨架；预留时间或提前预拉取
- **check/渲染命令在项目根运行**：主 composition 放根 `index.html`（`compositions/` 是 registry 子项）；传文件路径报 "Not a directory"
- **timed 视觉元素必须 `class="clip"`**：带 `data-start`/`data-duration` 的元素不加 class，runtime 不按时间控制显隐（首轮 18 个错误）；`<audio>` 媒体元素除外

## Phase 5: render — HyperFrames Deterministic Render

### Goal

从 Phase 4 已验收的 Composition 直接确定性渲染视频：先 draft 快验（时长/画面/音频问题），再 standard/final 成片。渲染命令、参数与输出契约按当前安装版本的 hyperframes CLI 执行。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| hyperframes | skill | 必选 | github · c32b804 | 从 Composition 进行确定性 frame seek 与 MP4 渲染（`npx hyperframes render`，draft → final；`check` 为渲染前质量门） |

### Input

- Phase 4 `video/project/`（已验收 Composition：index.html + assets + audio + subtitles）
- Phase 4 execution 记录与验收状态

### Output

- `video/renders/draft.mp4`：快速发现时长、画面与音频问题
- `video/renders/final.mp4`：通过 draft 与必要 QA 后的正式渲染结果
- `video/qa/render-execution.md`：渲染命令、hyperframes installed_ref（含项目 pin 版本）、参数与输出媒体信息（探针）

### Quality Criteria

- 正式流程为：`HTML Composition → HyperFrames deterministic frame seek → MP4`；不经过截图转视频路径
- 正式视频的视觉、动画、音频轨道与字幕均由同一 HyperFrames Composition 执行
- 渲染前 `npx hyperframes check` 通过（含 lint）；检查失败必须修复后重跑，不得带错渲染
- draft 与 final 使用同一份 Composition；两者视觉状态不一致时定位渲染参数或 seek 问题，不换 Composition
- 输出包含视频流和音频流；分辨率、帧率、编码格式符合项目目标配置
- FFmpeg 只用于编码检查、mux 与必要的最终封装；禁止多级 xfade 作为主时间轴
- 正式成片必须保留渲染命令、参数和媒体探针结果；临时工作目录不得冒充最终产物

### Known Issues

- 首次拉取、字体本地化（Google Fonts CJK 分片 render 期自动嵌入）与高质量渲染耗时较长；先 `check`/`snapshot` 再 final render（资产记录: hyperframes，实测 84.17s 中文财经视频 high quality 渲染 1m36s）
- 渲染失败时先检查 Composition contract、资源路径、track 冲突与 seek 状态，不退回截图方案
- 项目 pin 的 CLI 版本不会自动前进；恢复项目时按 hyperframes 主技能指引探测 `upgrade --check`，升级后必须 `check` 验证

### Phase 5 render constraints

- **中文字体需 `@font-face { src: local(...) }` 声明**：Noto Sans SC / PingFang SC / Microsoft YaHei 不在渲染器自动解析列表，不声明会回退泛型字体（check 报 font_family_without_font_face）
- **对比度警告低成本修复**：ink-faint #9A9A9A→#8F8F8F（2.63:1→3:1+）、gold 上文字 #B08D57→#AC8A55（2.89:1→3:1+）
- **确定性渲染验证方法**：draft 与 final 同时间点抽帧像素对比，差异 0.0% 即确认可重复渲染（实测 5 帧全 0.0%）

## Phase 6: video-qa — Snapshot 验证与内容复核

### Goal

对最终视频、配音、字幕与 Composition 做独立验收：确认无重影、状态残留、音画不同步、内容漂移与边界违规。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| hyperframes | skill | 必选 | github · c32b804 | 在关键 Cue 前/中/后 `snapshot`/seek，验证 Composition 状态与可重复渲染；`check` 复跑 |
| static-html-qa | skill | 必选 | internal | 对最终 Composition 与字幕做内容边界（check-content-boundary）与数值一致性（check-numbers，期望清单来自 Editorial Master 与裁决记录）检查；截图只作为 QA 证据 |

### Input

- `video/renders/draft.mp4`、`video/renders/final.mp4`
- `video/audio/`（voiceover 全片与逐 Scene）
- `video/subtitles/`、`video/script/SCRIPT.md`
- `video/project/`（Composition）
- Phase 2 Editorial Master 与裁决记录（期望清单来源）

### Output

- `video/qa/video-qa.md`：视觉 / 音频 / 内容三维验收记录（含 seek 时间点、检查项、证据与结论）
- 更新 `video/hyperframes-execution.md` 最终验收状态

### Quality Criteria

#### 视觉

- 在每个关键 Cue 的 t = 前/时/后 seek：元素状态正确、无重影/上一状态残留/重复 timeline、SVG/DOM 无错位裁剪溢出、同一时间多次渲染相同视觉状态
- Scene 切换时间与音频时间一致；抽查前段、中段、后段与最后一幕，无累计漂移

#### 音频

- 音色统一；无断裂、爆音、异常静音或 Scene 拼接不自然；音量一致；全片音频可被媒体探针读取
- 视频总时长与 narration 总时长一致（允许明确记录的编码级误差）；字幕与语音同步

#### 内容

- SCRIPT.md 未被修改；字幕由 SCRIPT.md 派生，不存在第二套文案
- 没有新增研究事实、改变结论强度或引入未经编辑层审议的因果
- 没有目标价、评级、买卖建议、仓位、交易策略或交易信号漂移
- 不出现「唯一/无懈可击/绝对/最优质」等绝对化、营销化措辞；「企稳确认/压力信号」类基本面验证信号保留，但不得写成「出现信号即买卖」
- 未解决的冲突项不出现在画面、配音或字幕

### Known Issues

- **重影**：按 `seek-safe animation → CSS wall-clock animation → DOM 状态复位 → timeline 重复叠加 → transition 历史状态` 顺序排查，不首先退回截图方案
- **Cue 不同步**：按 `SCRIPT → 音频时间 → Scene duration → Composition timeline → snapshot` 顺序定位，不手工调整几十个 delay
- **单个 Scene 无法稳定渲染**：只降低该 Scene 的动画复杂度或回到 Phase 4 修复，不把整条视频降级为静态截图
- QA 截图与正式渲染差异：以 seek 后的 Composition 状态与正式 render 为准，记录 snapshot/render 参数，避免把过渡中间帧当作最终状态
- 未通过的 QA 必须记录证据、归属 Phase 与回退路径；没有证据的「看起来正常」不能作为最终验收

## Architecture Boundary

完整链路：

```text
industry-analysis + industry-cycle-analysis + investagent（并行研究）
↓
findings-summary × 3
↓
Financial Editor Agent
↓
Editorial Master
↓
hyperframes 技能体系接管
│
├── Router：BRIEF.md → /faceless-explainer（默认）
├── Creative：设计 spec / beats
├── Core：Composition / Scene / data-* 时序
├── Animation：seek-safe 确定性动画
├── Media（media-use）：voiceover TTS、BGM、字幕
└── CLI：lint → check → preview → render
↓
Final HyperFrames Composition
↓
MP4
```

职责边界：

```text
研究 Skill × 3 / Financial Editor Agent
→ 内容：WHAT（事实、Thesis、边界）
↓
hyperframes router
→ 意图与路由：WHY THIS VIDEO / 时长与形态裁决
↓
hyperframes creative + core + animation + media-use
→ 视觉与运行时：HOW（设计、Composition、动画、媒体、配音、字幕）
↓
hyperframes CLI
→ 执行：WHEN 的真实时间落地与确定性渲染
↓
Video QA
→ 验证：视觉、音频与内容一致性
```
