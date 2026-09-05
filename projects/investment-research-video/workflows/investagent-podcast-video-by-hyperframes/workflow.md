# Workflow: investagent-podcast-video-by-hyperframes

> 位置: Project: projects/investment-research-video/workflows/investagent-podcast-video-by-hyperframes/workflow.md

## Mission

把经过研究的财经、产业与商业议题转成可复用的双人播客视频。账号规格、研究证据、逐句对话、音频时间轴和 HyperFrames 视觉均由 manifest 驱动；公司事实不能写死在模板源码中。公司财报只是输入类型之一，不能作为默认叙事模板。

默认节目是 `host_analyst`：主理人追问、承接和转场，分析师回答、展开证据和限定结论。`debate` 只有在 episode manifest 中显式指定时启用。

## Input

| Field | Required | Contract |
|---|---|---|
| `subject_type` / `subject_id` / `subject_name` | yes | 研究对象类型与标识；`subject_type` 可为 `company`、`industry`、`theme`、`event`、`technology`、`policy`、`macro` 或 `comparison` |
| `topic_card` | yes | 用户已批准的 `topic-forward-lead` 结构化选题卡；这是本 Workflow 的唯一视频输入，包含主题范围、观众问题、内容承诺、证据线索、叙事方向和 `review_constraints[]`；Markdown 交接摘要仅作阅读视图 |
| `research_date` | yes | 本次运行日期 |
| `account-profile` | yes | 账号、角色、音色、视觉和表达规则 |
| `input_mode` | no | `approved_topic`、`topic_discovery`、`research_revision`；默认按上游输入判断 |
| `source_bundle` | yes | 已验收的研究资料集合；可由财报、公告、产业链资料、新闻事件、政策原文、访谈/案例和结构化数据组成，按 subject_type 选择 |
| `company_id` / `company_name` | conditional | 只有 subject_type 涉及公司时必填；行业、主题、事件和技术议题不强制绑定单家公司 |
| `reference_video` | Phase 0 only | 首次建立账号规格时使用；后续公司运行不需要 |
| `format_mode` | no | 默认继承账号的 `host_analyst`；`debate` 必须显式指定 |
| `target_duration` | no | 由选题复杂度、证据量和平台目标决定；不得为了凑固定时长硬加话题 |

## Output

执行前读取 `references/global-contract.md`。本 Workflow 的账户资产、公司 run 输出、官方资料归档、pacing-plan 和视觉默认契约均在那里集中维护；各 Phase 的独有产物仍在本文件中声明。

### Account and subject-run outputs

账号资产、subject run 输出、官方资料归档、比较目录、券商材料和媒体产物的完整路径契约见 `references/global-contract.md`；本 Workflow 只在各 Phase 声明本阶段必须新增的产物。

## Principles

- 本账号面向中小投资者，在法律及适用平台规则边界内，以流量、粉丝积累和长期收益转化为首要产品目标；按 content-policy 执行。每期有一个明确、有依据、可争辩的主张；多空研究供导演取舍，不要求将全部正反观点搬进节目，不直接荐股或给交易指令。

- 本 Workflow 只负责账号规格 → 研究 → 编辑 → 对话 → 音频 → Composition → 渲染/QA 的项目顺序、运行参数和交接；资源通用调用规则由对应 Skill/Agent 资产记录负责。
- Required Resources 仍按 by-name 引用；各 Phase 只消费已验收的上游产物，并在项目执行记录中留下本项目所需的资源和结果证据。
- 账号资产先于公司内容；公司名、数字、话题、音频路径和图表数据来自 manifest。
- 研究资料分为四条证据线：官方披露、结构化财务/行情、产业与周期研究、外部深度研究；任何一条线都不能静默替代另一条线。结构化数据采用 Tushare → AkShare → BaoStock 的可降级路由，但官方披露始终是关键数字的事实主源。
- 公司研究额外必须覆盖第五条证据线：公司动态与产品事实，包括近期公告/新闻、获奖、产品发布、具体型号、项目签约/中标/交付、标准制定和技术里程碑；没有命中时也必须留下覆盖报告和缺口状态。
- 新闻发现优先使用 `multi-search` 的 `prefer_quality=True`（Tavily）；搜索摘要只做候选发现，最终事实必须打开原文并记录来源、事件日期、发布日期和主体核验。`news-search` 只作热点聚合补充。
- `deep-research` 只作为外部资料补充源；其报告中的数字和判断必须回到原始来源或结构化数据复核后，才能进入 Research Intelligence Document。
- 内容主线按 subject_type、观众问题、证据新鲜度和产业/经营重要性动态选择：财报、行业机制、公司案例、重大事件、技术路线和政策变化都可以成为主线；财报只在证据和问题确实支持时作为主线。
- `topic_card` 必须来自用户批准的 `topic-forward-lead` 结构化产物；其中的 `review_constraints[]` 只是验证约束，导演必须判断其是否适用于本期选题，适用时翻译为本期叙事中的具体动作，不适用时记录理由，不得改变研究事实或强行套用结构。任何行业→公司→特殊公司的路径都只是可选参考。
- 每期先从选题卡提炼一个观众问题和内容承诺，再决定主叙事形态与模块数量；不默认从“若干个话题”开始，也不默认每期都走公司介绍 → 财报 → 风险的顺序。
- 比较或行业→公司叙事必须在 manifest 声明 `comparison_entities[]`（每项含 `name`、`role`、`source_refs`）以及相关 topic 的 `entity_legend`；口播首次提到“几家公司/几类主体”时，必须在同一回合或前一回合说出具体名称。质量检查不得通过扫描项目目录来禁止其他公司名，跨主体比较是受支持的输入形态。
- 允许轮换行业拆解、公司案例、公司对比、事件追踪、技术机制、政策影响、神话证伪、产业链地图和问答型节目；轮换必须服从证据和观众问题。
- 官方资料路径、复用检查、命名和同行归档统一遵循 `references/global-contract.md` 与 cninfo-connector；公司新闻与产品资料统一落到 `research-materials/company-intelligence/`。
- `editorial/episode-input.json` 是 Phase 2 生成器的输入事实与表达契约；生成器不得在代码中写死公司、行业或事件专属开场、自我介绍、估值内容或固定话题数量。
- Phase 1 与 Phase 2 之间存在人工决策门：`topic_discovery` 先生成 3–5 个互斥选题并批准一个 `topic_id`；`approved_topic` 与 `research_revision` 验证已有主问题或修订范围后再继续。
- `editorial-director-agent` 是全局内容导演：它决定主问题、开场、话题顺序、机制归属、观众收益和视觉意图；`financial-editor-agent` 负责证据/因果裁决，`dialogue-director-agent` 负责逐句互动，三者不得越权。
- 公司动态和产品事实必须先进入结构化事实资产；行业、事件、政策和技术资料也必须先记录来源、日期、主体和证据角色，再由内容导演决定是 opening、main_evidence、supporting_evidence、visual_only、background 还是 omit；研究员或脚本生成器不得直接把搜索结果写进口播。
- 一个核心机制只能有一个主章节；相邻章节必须有不同主问题、证据集合和观众收益，并在导演方案中留下去重与顺序理由。
- 开场使用 `COLD_OPEN → INTRO` 或直接问题式开场；顺序由 narrative_mode 和平台目标决定，不能用固定自我介绍替代主问题。
- 开场必须在前 10 秒让观众知道本期要回答什么，可采用事实反差、现场问题、争议说法、事件节点、技术演示或产业链冲突；事实、视觉锚点和问题必须来自对应 subject 的证据 brief。
- 逐句音频是唯一时间轴来源；不得按性别整段拼接或用字数估时。
- **Script-first pause**：需要明显句内停顿时，优先在 Phase 2 改写为自然短句、真实追问或独立回应，让 TTS 依据上下文表达；句号只是软性韵律提示，不是确定的静音指令。
- `target_rate_cps` 只允许作为单个 turn 的明确语速实验字段，不能作为全片或整段停顿的默认实现；局部固定停顿优先使用 `intra_turn_breaks`，且不同时改变该 turn 的自然语速。
- `speaker alternation` 只是顺序门禁；对话关系必须由 `reply_to_turn_id`、`interaction_type`、`emotion` 和 `delivery` 表达。
- 图表优先于表格，表格优先于大段文字；观众不可见内部字段不得进入 HTML。
- Composition 使用 account-profile 允许的视觉变体；editorial-paper 是稳定基线，不是每期强制样式。`visual_mode` 可按内容选择 editorial-paper、data-newsroom、dark-terminal、field-notes、timeline-board 或其他已验证变体，并记录选择理由。
- 音色缺失、身份不匹配或静默 fallback 时，停在音频门禁。
- `references/podcast-v1-shenyan.md` 是当前稳定音频版本，使用 VoxCPM2 continuation；CosyVoice3、IndexTTS 和其他 clone mode 只作为独立 A/B。
- **数字口播简化**：亿级金额只说整数（"五十八亿"而非"五十八亿五"），千万级四舍五入到亿（"七个亿"而非"七亿三"），百分比用"X个点"（"十二个点"而非"十二点零零"）。详见 `account-profile/dialogue-policy.md`。
- **英文读法**：CPU 保持英文，GPU 可说"显卡"，ARM 整体发音（不逐字母拼读），NVIDIA 用"英伟达"。
- **字幕基线**：默认一条口播回合对应一条字幕，时间沿用该回合真实音频区间；允许自然换行，不按固定字数机械切碎。只有一个回合确实包含多个独立句群且画面需要分别强调时，才在 manifest 中显式拆 cue。
- **平台封面**：封面是独立 HTML 资产，不属于正片 Composition 时间轴；必须先生成 HTML，再按实际平台尺寸截图为横版与竖版 PNG。封面继承“账本两面”横幅的克制、沉稳、财经出版物气质：深黑蓝—暖棕—灰黑柔和渐变，低透明度纸张噪点、暗角和账本方格纹理；禁止纯色铺底、亮红顶部横条、鲜红标签、黄色强调字、无语义圆环和斜切色块。品牌强调色统一使用 Logo 的暗酒红，右侧主视觉使用 Logo 的黑红折页图形并保持低透明度。标题使用财经出版物/研究机构气质的衬线显示字体，避免普通 PPT 粗黑体；公司名置于标题上方，主标题和底部细线表达由 `episode-input.json` 的 `cover.subject_label`、`cover.large_text`、`cover.subtitle` 驱动。封面不得添加小字免责声明、日期、研究编号或不可读的信息层。
- **官方资料归档**：公司 subject 在 Phase 1 前归档适用的半年报/年报与公告；其他 subject 按来源类型归档政策、事件、技术或产业原文。下载前先查本地缓存。

## Phase 0: reference-replication — 建立账号规格

### Goal

从参考节目和蒸馏成果中提取公司无关的账号定位、主持人关系、节目结构、视觉语法、字体、音色和质量规则。完成后，后续公司不再依赖参考视频。

### Required Resources

| Resource | Type | Required | Use |
|---|---|---|---|
| `hyperframes` | skill | yes | 抽象可复用视觉和时间轴约束 |
| `podcast-workflow` | skill | optional | 借鉴自然对话和分段 TTS 方法 |

### Input

授权参考视频、既有蒸馏成果、目标画幅和账号定位。

### Output

`account-profile/` 下的账号规格、视觉 Token、内容/对话规则、音色资产和 `phase0-execution.md`。

### Quality Criteria

- 覆盖参考节目完整结构，固定元素与变化元素分离。
- 明确 `host_analyst` 默认模式、`debate` 显式覆盖规则、两位主持人身份和发言职责。
- 字体、颜色、字幕、持久导航、图表优先级和时长规则公司无关。
- 音色参考有来源、授权状态、prompt 文本、格式和验证记录。
- 账号 avatar/logo 必须有可渲染的本地文件；Phase 4 Composition 复制并显示账号横版 logo 与头像，缺失时停在账号资产门禁。

### Known Issues

参考视频的原文、原声和品牌资产不进入生产；只能复用结构和视觉语法。音色资产必须使用已授权或自建资产。

## Phase 1: research — 研究对象与证据建模

### Goal

围绕 subject_type 建立足以回答观众问题的事实、正反证据、背景、机制、风险和可验证变量，并决定本期最值得讲的主线。模块数量由问题和证据决定，不以固定话题数为验收目标。

### Required Resources

| Resource | Type | Required | Use |
|---|---|---|---|
| `industry-analysis` | skill | yes | 产业链和竞争格局 |
| `industry-cycle-analysis` | skill | yes | 供需、周期和反证 |
| `investagent` | skill | conditional | subject_type 涉及公司时启用公司研究；行业/主题/事件类输入按研究对象选择对应资源 |
| `tushare-connector` | skill | conditional | 有权限时获取公司与同行统一财务、三表和行情；无权限按数据源路由降级 |
| `earnings-reader` | skill | conditional | 有财报或财务问题时启用；无财报主线时不强制 |
| `multi-search` | skill | yes | `prefer_quality=True` 优先使用 Tavily，发现近期公司新闻、产品发布、型号、奖项、订单和交付线索；搜索摘要不得直接入稿 |
| `cninfo-connector` | skill | conditional | 年报、公告和法定披露 |
| `news-search` | skill | conditional | 多平台新闻聚合补充；只用于发现线索，必须回到原文核验 |
| `finance-report-analyzer` | skill | conditional | 同行 PDF/Excel 财报包的批量结构化和趋势图；有文件包时启用 |
| `deep-research` | skill | conditional | 行业、竞品、技术路线和市场结构的外部补充；出现公开资料缺口时启用 |
| `research-quality-gate` | skill | yes | 研究底稿和证据链验收 |

### Input

subject_type、subject_id/subject_name、研究日期、账号 profile、研究边界和可用 source_bundle；涉及公司时再提供证券代码、比较角色和业务环节。

执行前读取 `references/global-contract.md` 的适用输出契约；公司 subject 使用 Company-run outputs，行业/主题/事件 subject 使用对应的 topic run 目录和来源归档。

### Output

按 subject_type 落盘相应的研究原件、来源 ledger、事实卡、比较材料、findings-summary、topic-evidence-matrix 和执行记录；公司 subject 额外生成 company-thesis-card、company-intelligence 与同行财报归档，行业/主题/事件 subject 生成对应的 industry/theme/event evidence brief，不强制生成公司专属文件。

### Quality Criteria

- 至少形成一个清晰主问题和一组可回答它的内容模块；模块数量按选题复杂度和证据量决定，不要求每期固定 8–9 个话题。
- subject_type 涉及公司时必须生成 `company-thesis-card.json`；其他 subject_type 生成等价的 subject-thesis brief，明确主问题、机制、证据边界、风险和可验证变量。
- 只有有财报输入时才计算 `days_since_release`；所有 subject_type 都必须记录 `freshness`、`materiality`、`content_angle` 和选择理由。
- `content_angle` 可按 subject_type 取 `earnings_led`、`company_led`、`industry_led`、`event_led`、`technology_led`、`policy_led`、`comparison_led` 或 `myth_busting`；不得默认财报主线。
- 至少提供两个不同的开场角度（若选题天然只有一个入口，记录原因）；角度必须体现本 subject 的独特冲突或机制，不能只是套用上一期句式。
- 公司 subject 必须完成公司动态与产品事实扫描；其他 subject_type 按主题性质完成政策、事件、技术、供需或案例覆盖报告，不强制查询公司产品四类关键词。
- 每条入选动态/产品事实必须有 `fact_id`、事件日期、发布日期、事实类型、主体、原文 URL、来源级别、定位信息、与主线相关性和视觉候选；搜索摘要不得作为唯一来源。
- 产品型号、性能指标、奖项和项目规模必须优先由公司官网、正式公告、政府/行业组织或权威媒体原文支撑；无法核验的线索写入缺口，不进入事实正文。
- 关键数字有来源、口径、期间和定位；最新报告期与近 12 个月变化单列。
- 必须生成 `research-materials/data-source-ledger.json`：记录数据源顺序、调用状态、API/函数、报告期、字段映射、单位、复权方式、是否回查官方原文和降级原因；Tushare 无权限时必须留下 AkShare/BaoStock 的真实调用结果或明确缺口。
- 只有选择 comparison 或行业产业链叙事时才要求同行/角色比较；比较对象数量由问题和证据决定，并注明角色、可比边界和不可比项。
- 公司对照可介绍产业位置、技术、产品、客户、渠道、认证、交付和细分优势，须有来源与比较边界；不因缺财务表阻断有证据的定性介绍。只有实际进行财务比较时才生成相应 `peer-comparison.json`，记录使用的指标、报告期、口径与单位；所需指标缺失则标明缺口，不强制收集无关三表字段。
- 同行表必须按同一报告期分组；Q1、H1、全年不得混成一张排名表。缺少同期数据时，降级为产业坐标并写入缺口清单。
- 同行关键数字至少有一手披露或结构化数据源；`deep-research` 只提供候选来源、行业背景和外部交叉线索，不能单独支撑公司事实。
- AkShare/BaoStock 可支撑结构化辅助取数，但不能替代官方 PDF；合并净利润、归母净利润、扣非净利润等字段必须显式映射，口径不一致时不得比较。
- 同行官方报告必须归档到对应公司级 `outputs/companies/{peer_company}/official-information/`；当前 run 只保存引用路径和证据映射，不复制同行原件。
- 获取前必须执行本地复用检查；下载记录至少包含 `ts_code`、公司名、报告期、类型、公告日期、公告 ID、来源 URL、本地路径、文件大小和文本校验状态。
- 文件名必须符合 `{ts_code}_{period}_{document_type}_{announcement_date}.pdf`；不符合的历史文件在进入新 Workflow 前先建立 canonical manifest 映射。
- 没有足够证据、追问缺口或视觉锚点的话题不得进入 Phase 2。
- findings-summary 与 topic-evidence-matrix 保留 investagent、industry-analysis 等已验收研究中的关键多空解释、细分公司优势及可改变判断的证据，供导演选择；不得把研究模型意见伪称为真实机构共识。
- 没有完成公司动态与产品事实覆盖报告的话题不得进入 Phase 1.5；覆盖不足时必须标记 `coverage_status=degraded` 和具体缺口。
- 所有关键数字都能回溯到 `official-information/` 中的原始披露或明确标记的结构化行情源；不能只引用 `research-materials/` 二次摘要。

### Known Issues

未裁决的口径冲突不得进入事实正文；旧数据不能冒充当前变化；同行报告期或业务口径无法对齐时不得做简单排名；Phase 1 不生成买卖建议。

## Phase 1.5: topic-selection-and-approval — 候选选题与人工确认

### Goal

根据 `input_mode` 处理选题：`topic_discovery` 才生成 3–5 个互斥候选；`approved_topic` 直接验证用户已给出的主问题；`research_revision` 针对既有视频或脚本提出结构修订。所有模式都明确主问题、观众收益、证据和风险，并在人工批准前停止下游生产。

### Required Resources

| Resource | Type | Required | Use |
|---|---|---|---|
| `finance-content-engineering` | skill | yes | 执行 topic-gen，按研究证据生成候选池，不直接决定最终选题 |
| `editorial-director-agent` | agent | yes | 评估候选的观众价值、事实张力、主线适配和互斥性；candidate 模式只能停在审批门 |

### Input

Phase 1 已验收的 subject-thesis brief、topic-evidence-matrix、适用的事实卡/来源 ledger/coverage report、findings-summary、研究 freshness/materiality、账号 audience/content policy 和可用视觉锚点；必选读取用户批准的 `topic-forward-lead` topic card。

### Output

- `editorial/topic-options.md` / `.json`：`topic_discovery` 模式的 3–5 个候选；其他模式记录已批准主问题或修订范围。
- `editorial/topic-approval.md`：人工审批表，必须明确 `status: pending|approved|rejected`、批准的 `topic_id`、`approved_at` 和备注。
- `editorial/phase1.5-execution.md`：资源 by-name、installed_ref、输入、候选覆盖、停止状态和 gate 结果。

### Quality Criteria

- `topic_discovery` 候选数量为 3–5 个且角度互斥；其他模式不强制生成候选池，不能为了满足数量制造无效角度。
- 每个候选必须包含：主问题、观众为什么关心、开场候选、核心证据、可展开路径、最大风险、content_angle 和 evidence coverage；用自然语言明确拟主张什么、与何种看法存在分歧、为何值得中小投资者关注。
- 每个候选必须明确是否使用公司动态/产品事实，以及每条事实的 `fact_id`、`fact_role`（opening/main_evidence/supporting_evidence/visual_only/background/omit）和采用理由；不能只把新闻标题贴到选题里。
- 候选或已批准主问题必须覆盖本 subject 最关键的机制、证据冲突或验证路径；是否采用财报主线由 subject_type、freshness 和 materiality 决定。
- 开场候选可直接提出有证据的主张，也可用公司特征事实、案例或问题切入；前 10 秒明确本期要回答什么及观看价值。不同公司允许不同入口，选择理由写入 `opening-selection.json`，标题与开场承诺须由正文兑现。
- `topic-options.json` 必须记录候选间的 `mutually_exclusive_with` 和机制覆盖，便于后续去重。
- `topic-approval.md` 在用户确认前必须保持 `status: pending`；pending/rejected 状态不得生成 `director-treatment.md`、`episode-input.json`、`episode.json`、TTS、字幕、视觉或渲染产物。
- gate 必须能识别缺批准、批准 topic_id 不在候选中、批准时间缺失和候选不完整并给出 FAIL。

### Known Issues

人工确认是内容决策硬门，不是质量标准软建议；Agent 不能用默认候选、历史 run 或自己的判断代替批准。

## Phase 2: editorial-dialogue-design — 编辑与对话导演

### Goal

把已验收证据编排成自然的主理人播客逐句稿，并锁定口播、回应关系、情绪、delivery 和画面表达。先选定 `narrative_mode`，再按该模式组织内容模块，不默认每期使用同一套话题顺序。

### Narrative modes

- `industry_map`：行业问题 → 产业链/机制 → 公司或案例角色 → 兑现与风险
- `company_case`：一个公司问题 → 业务机制 → 证据冲突 → 验证条件
- `comparison`：统一比较问题 → 多对象逐项对照 → 差异来源 → 边界
- `event_tracker`：事件发生了什么 → 谁受影响 → 机制与证据 → 后续观察点
- `technology_explainer`：技术到底解决什么 → 链条和约束 → 商业化案例 → 未解问题
- `policy_impact`：政策目标 → 传导链条 → 受影响主体 → 可能的副作用与观察指标
- `myth_busting`：流行说法 → 事实核验 → 为什么会误判 → 更准确的判断框架
- `qa_roundtable`：观众问题 → 快速回答 → 证据展开 → 追问与结论

可扩展新模式，但必须在 manifest 中声明模式、适用理由和模块顺序；模式只是编排工具，不替代研究判断。

### Required Resources

| Resource | Type | Required | Use |
|---|---|---|---|
| `editorial-director-agent` | agent | yes | treatment 模式；读取已批准选题卡，锁定 editorial thesis、opening、narrative mode、模块顺序、机制去重和 scene intent |
| `financial-editor-agent` | agent | yes | 主命题、事实核验和冲突裁决 |
| `dialogue-director-agent` | agent | yes | host/analyst 回合、回应关系和表演字段 |
| `information-visualization-architect` | agent | yes | chart-spec，不补数据 |
| `debate-rounds` | skill | conditional | 仅 `format_mode=debate` |
| `finance-content-engineering` | skill | yes | 主口播改写：draft-script → polished-script，事实零漂移 |
| `human-understanding` | skill | yes | 将试听反馈还原为口语、关系和情绪约束；不直接改事实 |
| `humanizer-zh` | skill | yes | 对已改写的实际 episode 文本做二次审校，不只生成风格标签 |
| `boundary-rewrite` | skill | yes | 财经表达边界 |

### Input

Phase 1 已验收证据与适用事实资产、Phase 1.5 的批准记录或修订范围、subject-thesis brief、账号 profile、导演 treatment 和已批准的 `topic_card`。

执行前读取 `references/global-contract.md` 的 Performance contract。

### Output

`editorial/episode-input.json`、`editorial/feedback-constraints.md`、`editorial/phase2-execution.md`、`podcast/script/episode-draft.json`、`podcast/script/episode-polished.json`、`podcast/script/episode.json`、`podcast/script/spoken-polish-diff.json`、`debate-script.md`、`dialogue-map.json`、`spoken-style-map.json` 和 `visual-plan/chart-spec.json`。

同时必须保留 `editorial/director-treatment.md`、`editorial/topic-order.json`、`editorial/opening-selection.json`、`editorial/scene-intent.json` 和 `editorial/director-execution.md`；当选题存在两种以上可行讲法时，另保留 `editorial/narrative-options.json`。`editorial/feedback-constraints.md` 必须记录 topic card 携带的复盘候选适用性、具体实现、观察指标和未采用理由。这些是 Phase 2 的硬交接产物。

### Quality Criteria

- manifest 写入 `format_mode`、`role_map`、`turn_id`、`topic_id`、`speaker`、`text` 和 `evidence_ids`。
- manifest 的 topic/turn 必须能够回指 `fact_ids`、`fact_role`、`source_refs` 和 `visual_intent`；产品型号、奖项、签约、交付等事实不得只存在于导演私有笔记。
- `episode-input.json` 必须声明 `cover.title`、`cover.subtitle` 和 `outro`；`topics[]` 必须提供 `short_label`，供目录和持久导航使用。
- `cover.title` 必须突出本期最引人注目的行业、产业链或公司主角；封面只保留手机缩略图可读的大字和必要图形，日期、全称和研究注释不进入封面主视觉。
- `episode-input.json` 必须声明 `opening.mode`、`opening.cards`、`opening.cold_open`、`opening.intro`；开场和自我介绍只能从该 manifest 读取。
- `episode-input.json` 必须携带 `content_angle`、`report_context`、`editorial_thesis`、`opening_rationale` 和 `narrative_mode`；`financial_data_role` 仅在存在财报/财务证据时填写，Phase 2 不得绕过 Phase 1 的主线决策。
- `comparison_entities[]` 在标题、口播或选题卡涉及多家公司/多类主体时为强制字段；每个对象必须有 `name`、`role`、`comparison_axis` 和 `evidence_ids`，且所有主体必须在 spoken text 或字幕中首次点名。任何“几家公司/三类主体”而不点名的稿件必须 FAIL。
- Phase 2 开始前必须通过适用的 topic approval gate；`topic_id`、opening 和模块顺序必须与批准记录或用户已批准主问题一致。
- 必须消费 `editorial-director-agent` 的 treatment：每个内容模块有 audience payoff、机制归属、前后依赖、visual intent 和验证/证伪条件；缺少任一项不得生成最终 episode。
- 每个内容模块还必须写入 `entry_belief`、`open_question`、`evidence_progression`、`turn`、`exit_belief` 和 `next_question`；缺少认知弧、无法说明章节前后判断变化的模块不得生成最终 episode。
- 若选题卡允许多种讲法，导演必须先提交 2–3 个轻量叙事草案并记录选择理由；若证据或平台目标只支持一种，记录不做多方案的原因即可。草案不要求新增模板，写入 treatment 或可选 `narrative-options.json`。
- 话题顺序必须有全局去重表：一个核心机制只有一个 `primary_topic_id`；相邻话题不得重复主问题、证据集合和观众收益。
- 开场 manifest 必须包含 `opening_mode`、`opening_cards` 和 `COLD_OPEN/INTRO` turns；冷开场后才出现主持人自我介绍和目录。
- `COLD_OPEN-01` 或等价的首个主问题回合必须包含 subject 特征事实/争议、一个开放问题和 `question_ending=question`；金额/增速采用自然口播。不得仅因上一期使用过某种钩子，就复制其事实组合、句式或视觉卡布局。
- 生成 opening canary 时运行项目脚本 `build_podcast_opening_test.py`；脚本必须对 `COLD_OPEN → INTRO` 顺序、事实反差、开放问题和书面化禁用短语给出 PASS/FAIL。
- 每个内容模块至少有立题、直接回应、证据展开和推进/收束；是否由分析师承担证据，要按 narrative_mode 和角色设定决定。
- 每个内容模块至少指定一个 shot proposition，并说明口播、出镜、B-roll、图表和字幕各自承担什么信息；无功能的装饰性画面不得进入 Composition。
- 除话题第一句外，每句有 `reply_to_turn_id` 和 `interaction_type`；不能靠交替 speaker 制造对话。
- 情绪和 delivery 与回应关系共同生成；语气词服务于关系，不能机械重复。
- 每个角色的段首、段尾和总结句必须跨话题去重；禁止用固定结论句或口头禅填充每一节。生产前运行 `podcast-audio-compiler` 的 `check_dialogue_repetition.py`，发现重复先回到 Phase 2 改稿。
- Phase 2 输出 emotion、delivery 和 pause anchors；Phase 3 先运行 resolve_pacing_plan.py，再消费稳定基线的 turn 级 speech_rate、target_rate_cps 和 pause_after_ms，并在 segments.json/audio-qa.json 留痕。
- Phase 2 对明显停顿必须先完成脚本表达设计：长句拆分、问答回合或自然承接优先；不得把“画面里、口播、字幕”等制作元话语写入 spoken text。若确需固定静音，才在受影响 turn 上声明 `intra_turn_breaks`。
- 句首出现“对/嗯/没错/好”等短回应时，必须同时写入 `response_action=backchannel`、`backchannel`、`backchannel_target`、`filler_position=start`、`delivery=short_pause` 和正值 `pause_after_ms`；不能只把短词拼进普通长句。
- 数字分别锁定事实、自然口播和紧凑画面表达；不改变口径和事实方向。
- 口播稿不得直接出现未经自然化的金额小数（如 `7307.06万元`、`2498.99万元`）或带两位小数的百分比；精确值必须留在 evidence/chart 字段，口播使用“约/接近/超过”和整数级别表达。若仍出现此类 token，Phase 2 直接退回，不得进入 TTS。
- 每个视觉指标卡必须有语义完整的 `label`、`value`、`desc`；同一 topic 的三张卡不得全部使用“观察/指标/数据/待填写”等占位值。页面标签应回答“谁/什么指标/处于什么阶段”，不能只重复状态词。
- `human-understanding` 先把反馈转成约束；`finance-content-engineering` 直接改写 episode-draft；`humanizer-zh` 审校 episode-polished 并写回最终 episode.json。两者不能只更新 spoken-style-map，也不能在 Phase 3 随意改稿。
- `spoken-polish-diff.json` 必须记录每个 changed turn 的 before/after；draft/final 的 speaker、topic_id、evidence_ids 不得变化。存在用户口语化反馈时，运行 `scripts/check_spoken_polish.py --require-change`，无实际文本变化不得写 PASS。
- 明显停顿的脚本改写必须落在 `episode-draft`/`episode-polished`/最终 `episode.json` 的文本中；只修改 `spoken-style-map`、delivery 或口头说明而未改变实际 spoken text，不得写 PASS。
- `check_podcast_dialogue.py` 必须阻断制作元话语（视频里、画面里、字幕里、必须说等）进入 spoken text；允许已声明并有证据的同行介绍与比较。`check_spoken_polish.py` 对长篇稿件至少要求 10% turn 有实际 before/after 改写，不能用一两个虚词变化冒充全稿口语化。
- 每个内容模块有 chart-spec 或明确 no-chart 理由；定性同行介绍可采用产业地图、产品或公司身份卡。估值可消费官方披露、可靠行情、券商材料及可复核条件计算，允许明确多空观点，不出现直接荐股、交易指令或收益保证。
- 内容模块排序必须服务于 `editorial_thesis`：至少一个模块解释核心机制，至少一个模块呈现证据或反证，至少一个模块讨论验证条件、风险或下一步观察；财报主线也不能把整期变成数字罗列。
- `valuation_context` 必须显式声明 `enabled`；启用时使用现有 source_refs 指向已验收研究来源，声明 topic_id、source_class 及适用 source_dir。券商来源继续使用 research-materials/brokerage/；其他来源不强制券商目录。日期、口径、假设和敏感性在研究材料中说明，由 financial-editor-agent 实际复核；未启用不阻断节目。
- director-treatment.md 按 editorial-director-agent 输出主张、标题/开场选择、问题承接、公司定位及术语铺垫；director-execution.md 留下具体段落的只听稿审阅证据。检验明确立场、最强挑战、及时的信息回报和结尾兑现，不按多空条数或财务表数量验收。
- Phase 2 必须留下三个独立执行证据：`feedback-constraints.md`（human-understanding）、`spoken-polish-diff.json`（finance-content-engineering + humanizer-zh 实际改写）和 `phase2-execution.md` 中的资源 installed_ref；缺少任一证据不得写 PASS。
- 运行项目脚本 `scripts/check_podcast_dialogue.py`，对开场、短回应、估值资料边界和两个口语化资源执行证据给出 PASS/FAIL。
- 运行项目脚本 `scripts/check_editorial_gate.py --run-root <company-run> --require-approved`，对批准状态、候选一致性和导演交接产物给出 PASS/FAIL。

### Known Issues

不能把多个段落当作回合；不能在 Phase 3 临时改写数字、添加语气词或改变观点。短确认词如“对”“嗯”必须有 `interaction_type`、`response_action`、`backchannel_target`、`emotion`、`delivery` 和合理停顿，不能当普通句首文本批量生成。当前历史 run 的 humanizer PASS 只有风格映射、没有逐句 before/after，不能作为新 run 的合格证据。导演 treatment 不是研究补充层，证据缺口必须退回 Phase 1。

## Phase 3: podcast-audio-compile — 逐句音频编译

### Goal

把锁定的 episode manifest 编译为真实交替、可追溯、可对齐的逐句音频和字幕。

### Required Resources

| Resource | Type | Required | Use |
|---|---|---|---|
| `podcast-audio-compiler` | skill | yes | 默认 VoxCPM2 continuation adapter、逐句 WAV、SRT 和 QA |
| `media-use` | skill | yes | 音频媒体接入和资产记录 |
| `hyperframes-audio` | skill | optional | 已有音频的混音处理 |

### Input

`episode.json`、项目 `account-profile` 的资源选择和显式 Workflow profile。默认稳定版本见 `references/podcast-v1-shenyan.md`。

Phase 2 必须使用项目通用脚本 `scripts/build_podcast_episode.py` 从 `episode-input.json` 生成 episode、dialogue-map、spoken-style-map 和 chart-spec；该脚本不提供公司、话题或 OUTRO fallback，禁止调用带公司专属内容的历史 run 脚本作为新公司生成器。

执行前读取 `references/global-contract.md` 的 Performance contract，并只消费已锁定的 pacing_plan。

### Output

`podcast/audio/segments/`、`segments.json`、`narration-full.wav/mp3`、`subtitles.srt`、`podcast/qa/captions.json`、`audio-qa.json` 和执行记录。

### Quality Criteria

- 每个 turn 独立生成并按 manifest 顺序拼接；speaker 映射严格命中。
- 字幕时间来自真实 WAV；音频和 manifest 的文本、角色、后端、profile 可追溯。
- 编译完成后必须运行 `scripts/build_caption_manifest.py`，从真实 `segments.json` 生成 `podcast/qa/captions.json` 和最终 `subtitles.srt`；Composition 只消费该 caption manifest，不直接把整段 turn 文本当作一条字幕。
- 默认每个 turn 生成一条字幕 cue，起止时间来自该 turn 的真实音频；长文本由字幕容器自然换行，不用固定 20 字/40 字规则强制拆分。
- `references/podcast-v1-shenyan.md` 使用 VoxCPM2 continuation、`voice.zhiwei + voice.shenyan`、自然停顿和 natural 后处理；不启用 CosyVoice3、IndexTTS 或其他 clone mode。
- **缓存失效门禁**：音频缓存不得只按 `turn_id` 和 WAV 文件存在性复用。文本、speaker、voice/reference、emotion、prompt、TTS 参数或 pacing 变化时，必须使用内容寻址缓存或全新音频目录；`reused_segments` 必须能解释为同一 manifest 的安全复用。
- 通过音色、发音、尾词残留、杂音、响度、断句和文件可解码检查。
- TTS 完成后必须对最终 narration 或逐句 WAV 执行反向转写/已知文本对齐检查；`audio-qa.json` 必须记录转写文本、异常句、重生成次数和最终 PASS。发现乱码、漏词、重复词或句尾残留时，必须回到 Phase 3 重生成该 turn，不能只改字幕。
- TTS 完成后必须追加独立 ASR（未知文本转写）检查；forced alignment 只能证明已知文本可对齐，不能证明实际音频说的是最终稿。独立 ASR、episode/segments/captions 文本比对和真实音频时长比对未完成时，不得进入视觉 Composition。
- Phase 3/5 必须运行 `scripts/check_podcast_artifact_consistency.py`，检查 episode → segments → captions 的回合、文本、时间和可选音频时长一致性；该脚本不能替代独立 ASR。
- 音频未通过不得进入视觉 Composition。

### Known Issues

v1 暂不解决 VoxCPM2 的高频颗粒、气声和部分末段动态问题；后续 prompt、音量处理或情绪控制优化必须作为新 profile/实验版本，不得静默改变 v1。

局部停顿实验曾因将 `target_rate_cps` 注入全部 turn 而把整片语速降低；TTS 对句号的停顿解释不具备确定性，脚本先行改写和独立 ASR 是当前更稳妥的质量路径。

### Phase 3 profile constraints

- 当前 `podcast-v1-shenyan` 的生产后端为 VoxCPM2 continuation；后端切换前必须先通过同一 `COLD_OPEN + INTRO` canary 和人工试听。
- 当前 profile 固定使用自然停顿、natural 后处理和 shenyan 情绪参考资产；其他后端和 clone mode 属于独立实验分支。

## Phase 4: podcast-composition — 参数化视觉

### Goal

将 account profile、episode manifest、chart-spec、segments 和字幕编译为公司无关的 HyperFrames Composition。

### Required Resources

| Resource | Type | Required | Use |
|---|---|---|---|
| `hyperframes` | skill | yes | Composition、动画和渲染入口 |
| `hyperframes-core` | skill | yes | tracks、timing、sub-composition 和确定性 |
| `hyperframes-animation` | skill | yes | 多节拍 Scene、数据动画、转场和 seek-safe timeline |
| `hyperframes-creative` | skill | yes | 视觉 Token、排版和图表呈现 |
| `information-visualization-architect` | agent | yes | chart-spec 到 Scene 的映射 |
| `static-html-qa` | skill | yes | HTML、数字、溢出和公共文案检查 |

### Input

账号 profile、episode、chart-spec、segments、`podcast/qa/captions.json`、字幕和最终音频。

执行前读取 `references/global-contract.md` 的 Visual default and reuse。

### Output

`podcast/visual-plan/scene-manifest.json`、`podcast/project/`、`podcast/project/cover.html`、4:3 `cover.png` 和 3:4 `cover-3x4.png`（独立平台封面）、Composition 执行记录和可检查的 HTML。

若导演采用公司动态或产品事实，同时输出 `podcast/visual-plan/fact-card-manifest.json`，记录 event-card/product-card/server-spec-card/milestone-timeline 的 fact_id、source_ref、展示文字和画面来源。

### Quality Criteria

- 同一 Composition 只消费 manifest/variables，不能写死公司事实。
- 每个核心话题必须有公司无关的 Scene archetype 和至少 3 个 visual beats：立题/数据变化/机制或限制/验证收束；不能把一个话题压缩成单一静态页。
- 默认视觉 Token 从 account-profile/design.md 读取；不得在生成器中为单家公司写死品牌色，editorial-paper 只提供公司无关的财经编辑语法。
- `visual_mode` 必须与 narrative_mode 和观众问题匹配；连续节目不得无理由复用同一开场卡、目录布局和章节模板。
- 关键转折处应有可感知的视觉或对话变化（图表状态、证据类型、镜头尺度、主持人职责或 B-roll 角色至少变化一项）；变化服务于认知推进，不为制造噪声而切换。
- `scene-intent` 中的每个 scene 都要能回答“展示什么、为什么现在展示、展示后观众多知道什么”；无法回答时降级为背景或删除。
- 每个核心数据图至少使用一种可感知的 seek-safe 动画：数字滚动、柱体生长、曲线绘制、瀑布展开、路径/节点出现或重点标注；动画必须由 `hyperframes-animation` 规则和 `scene-manifest.json` 指定。
- 目录使用紧凑的章节网格或分组导航，不把完整长问题堆成同尺寸胶囊；目录文字必须来自 manifest 的短标签。
- OUTRO/SUMMARY 必须有总结性视觉资产（验证看板、三道门、结论矩阵或指标卡）和一句来自 manifest 的收束文字；不得以空白画面作为结尾状态。
- 字幕、说话人高亮、图表、音频和导航使用同一真实时间轴。
- `COLD_OPEN`、音频和第一条 caption 均从 0 秒开始；`cover.html` 是独立平台封面，不得出现在正片 timeline。
- **字幕密度**：默认一回合一条字幕，贴合沪电股份基线；字幕时间覆盖该回合真实语音区间，长句自然换行，不按固定字数机械截断。字幕数字使用阿拉伯数字（如"58亿""7个亿""12%"），不用中文数字。
- **平台封面**：Phase 4 必须生成独立的 `podcast/project/cover.html`，沿用 Composition 的同一背景、字体和视觉 Token，只展示栏目标识、subject 主角和一组手机端可读的大字；标题字号大于正片标题，副标题可省略。封面主角从行业、产业链、公司、事件或技术中择一，由 evidence brief 说明选择理由。封面必须包含账号 logo，并分别使用 `scripts/render_cover_4x3.js` 导出 4:3 的 `cover.png`（推荐 1440×1080）、使用 `scripts/render_cover_3x4.js` 导出 3:4 的 `cover-3x4.png`（推荐 1080×1440）；封面独立于正片时间轴。
- 封面不得以“生成了 cover.html”作为完成标志：必须在同一 Phase 实际导出两个 PNG，并用图像信息检查确认尺寸分别为 1440×1080 与 1080×1440。封面主视觉最多保留一个冲突主标题和一个必要辅助标签，禁止底部免责声明、日期、研究注释和不可读的小字进入缩略图。
- 平台封面默认不进入正片时间轴，不产生音频、字幕或 `segments.json` 时长；正片 `COLD_OPEN` 必须从 0 秒开始。若明确需要片头封面动画，必须将同等时长同步加入音频、字幕和所有 Scene 时间轴，并单独标记为 in-video cover。
- 底部章节导航和进度条是 root-level persistent layer，章节宽度按真实音频时长比例计算。
- 进度条、章节边界和 Scene 区间必须共用同一套全局累计时间线：每个区间记录 `start_ms`、`end_ms`、`duration_ms`，首段从 0 开始，后段 `start_ms` 必须等于前段 `end_ms`；不得为章节重新从 0 计时或用局部比例重算。
- 页面切换、图表插播和 Scene 复用时导航不重置、不消失。
- 图表优先于表格和文字；观众不可见字段不得进入 HTML。
- 采用的公司动态和产品事实必须通过通用 event-card、product-card、server-spec-card 或 milestone-timeline Scene 呈现；不得把搜索摘要、未经核验的产品图或奖项标题直接放进 HTML。
- 运行 `check_public_copy.py` 和 `caption_gate.py verify`。
- 运行全局时间线检查，验证 progress、chapter ranges、Scene、caption 和 audio segments 使用同一累计区间；发现区间断裂、重叠或进度语义不一致时 FAIL。
- 运行字幕密度检查，确认 `podcast/qa/captions.json` 默认每个 turn 只有一条 cue、起止时间覆盖真实语音，且平台封面单独截图、不参与正片时长。
- 运行 `hyperframes-animation/scripts/animation-map.mjs` 并在开场、主要导航/转场、代表性核心模块和结尾抓取 snapshots；代表性模块数量按 manifest 声明，不强制每期固定两段。

### Known Issues

长片优先使用 topic sub-compositions；图表必须支持公司间数字、标题长度和缺失字段变化。当前 delivery 仍主要进入 segments.json 记录；需要实际改变节奏时使用 pacing_plan，不要把 delivery 标签本身误判为已完成的表演控制。

## Phase 5: render-and-regression-qa — 渲染与复用门禁

### Goal

验证成片可播、研究一致、音频同步、视觉达标，并证明同一模板可在适用的第二个 subject 或视觉/叙事变体上复用。

### Required Resources

| Resource | Type | Required | Use |
|---|---|---|---|
| `hyperframes-cli` | skill | yes | check、snapshot、render 和诊断 |
| `hyperframes-animation` | skill | yes | animation-map 和动态节奏审计 |
| `static-html-qa` | skill | yes | HTML、数字、边界和视觉回归 |
| `research-quality-gate` | skill | yes | 研究、脚本、字幕和证据一致性 |

### Input

完整 Composition、最终音频、字幕、episode manifest、账号 profile 和第二个 subject 或变体的最小测试输入。

### Output

`podcast/renders/draft.mp4`、`final.mp4`、可选 `podcast/opening-test-v4/renders/opening-canary-v4.mp4`、`podcast/qa/episode-qa.md`、`reuse-regression.md` 和执行记录。

### Quality Criteria

- 音频逐句交替、音色正确、字幕同步、导航连续、图表状态完整。
- 公共文案、数字一致性、字体、溢出、时长和渲染性能通过门禁。
- 检查 `subject_type`、`content_angle` 与 `report_context` 的一致性；无财报主线时不得硬套财务反差开场，跨期重复开场需回到 subject brief 复核。
- 检查 Phase 1.5 的批准记录与导演 treatment 一致；没有人工批准的 run 不得进入渲染。
- 检查话题全局顺序、机制主章节和相邻话题去重；发现多个章节重复同一机制时，必须退回 Phase 2 重新编排。
- 检查反向转写 QA 已对所有重生成句完成闭环，异常句不能只通过字幕替换掩盖。
- 检查 progress/chapter/scene/audio/caption 的全局累计区间一致。
- 检查所有可见新闻、奖项、产品型号、性能和项目事实均能回指 `fact-card-manifest.json` 与已打开原文；缺来源或只来自搜索摘要时 FAIL。
- 开场回归优先运行 `scripts/build_opening_canary.py`，只截取 `COLD_OPEN + INTRO` 生成短视频，先完成视觉审阅再进入长片渲染。
- 第二个 subject 或变体只替换 manifest/variables 即可完成 draft render，不改模板源码；若模板不适用，记录原因并新增适配模式。
- 所有事实可回溯，财经边界检查通过。

### Known Issues

只在单一 subject 通过不算 Workflow 完成；必须保留第二个 subject 或变体的复用回归证据。

## Phase 6: publish-and-closeout — 多平台发布与结果回写

### Goal

将已通过成片 QA 的视频、封面和平台差异化元数据，提交到已授权的多平台账号；跟踪每个平台的最终状态和作品链接，并把可审计结果回写到发布包与账号记录。

### Required Resources

| Resource | Type | Required | Use |
|---|---|---|---|
| `aitoearn` | skill | yes | Open Platform/MCP 多平台素材上传、Flow 创建、状态轮询和作品链接回传 |
| `social-auto-upload` | skill/tool resource | conditional | AiToEarn 不支持、明确失败或必须使用浏览器自动化时的国内平台回退 |
| `video-agent-publisher` | skill | yes | 生成平台差异化标题、描述、标签和引用出处 |
| `douyin-creator-tools` | skill | conditional | 发布后抖音作品列表、数据采集和评论运营，不代替发布接口 |

### Input

最终 `podcast/renders/final.mp4`、`podcast/project/cover.png`、`podcast/project/cover-3x4.png`、已验收 `episode.json`、研究来源清单、账号 profile 和用户明确指定的平台/排期。

### Output

`publish/metadata.json`、`publish/sources.md`、`publish/aitoearn-request.json`（不含 API Key）、`publish/aitoearn-result.json`、`publish/platform-results.json`、`publish/publish-execution.md`，以及确认成功后追加的 `account-profile/published-works.md` 记录。

### Execution contract

1. 先运行 `video-agent-publisher`，为抖音、B站、视频号、小红书、快手、YouTube 等分别生成平台适配文案；原始研究事实和平台字数限制不能被发布工具改写。
2. 先通过 AiToEarn 获取平台元数据和账号列表，按 `accountId` 建立本次请求映射；不从本地猜账号 ID。
3. 通过 AiToEarn 签名 URL 上传 MP4 和对应封面，确认资源完成后再创建多平台 Flow；资源 URL 必须属于与 API Key 匹配的中国版或国际版域名。
4. 一个 Flow 可包含多个平台 item；每个 item 允许独立标题、正文、标签、封面和平台选项。默认创建草稿或排期任务，只有用户明确要求立即发布时才提交即时任务。
5. 轮询 Flow/record 状态：成功写入作品链接；失败写入平台错误；抖音进入用户操作状态时输出短链/手机确认提醒。抖音确认页必须人工复核封面：AiToEarn 当前 App Scheme 可能只带视频路径，不保证独立 cover URL 已传入；收到完成状态后继续轮询。
6. 只有 AiToEarn 明确返回不支持或明确失败，且不存在“可能已提交”的不确定状态时，才调用 `social-auto-upload` 回退；回退平台必须逐个平台记录，禁止两套工具并发提交同一账号同一内容。
7. 发布成功后回写 `published-works.md`；没有平台 URL 时留空并标记待确认，禁止编造 URL。发布后的播放/互动数据继续由 `douyin-creator-tools` 或平台后台采集。

### Quality Criteria

- `metadata.json` 为平台差异化版本，不是同一段文案机械复制；每个平台的标题、描述、标签、封面和排期可追溯。
- `aitoearn-request.json` 只保存账号别名/ID、平台、资源引用、请求时间和 Flow 关联，不保存密钥、Cookie 或短期授权信息。
- `aitoearn-result.json` 与 `platform-results.json` 必须逐平台记录 `status`、`record_id`、`published_at`、`platform_url`、`error` 和 `needs_user_action`。
- 轮询失败、超时或状态未知不得直接切换回退工具；必须先查询记录或停在人工恢复状态。
- 抖音需要手机确认时，必须留下用户操作状态和后续确认结果；未确认不能写 `published`。
- 抖音封面必须保留“请求封面”和“确认页实际选择”两个状态；AiToEarn Scheme 未携带 cover 时，发布前从相册上传 3:4 封面，不能把接口请求中的 cover URL 当作已生效。
- 面向股民的信息流封面优先使用大字号公司名/核心数字/事实矛盾和高对比色；横版与 3:4 版分别重排，不做简单裁切。
- 账号级发布记录只接受明确成功的真实作品链接；不得把 Flow ID、任务 ID 或 AiToEarn 控制台链接当平台作品 URL。
- 运行发布前 dry-run/草稿检查；运行发布后结果校验和 `git diff --check`。真实发布属于外部生产动作，必须由用户在调用时明确指定平台、账号和立即/排期模式。

### Known Issues

- 国内平台个人账号上传接口和页面规则可能变化；浏览器回退不是 API 稳定性承诺。
- AiToEarn 的平台授权、API Key 和资源上传属于第三方服务边界；中国版 Key 必须使用 `aitoearn.cn` 端点，国际版 Key 必须使用 `aitoearn.ai` 端点。
- “创建 Flow 成功”不等于所有平台发布成功；必须逐平台追踪最终状态。
