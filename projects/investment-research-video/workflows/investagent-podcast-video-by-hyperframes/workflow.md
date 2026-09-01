# Workflow: investagent-podcast-video-by-hyperframes

> 位置: Project: projects/investment-research-video/workflows/investagent-podcast-video-by-hyperframes/workflow.md

## Mission

把上市公司研究转成可复用的长篇双人财经播客视频。账号规格、研究证据、逐句对话、音频时间轴和 HyperFrames 视觉均由 manifest 驱动；公司事实不能写死在模板源码中。

默认节目是 `host_analyst`：主理人追问、承接和转场，分析师回答、展开证据和限定结论。`debate` 只有在 episode manifest 中显式指定时启用。

## Input

| Field | Required | Contract |
|---|---|---|
| `company_id` / `company_name` | yes | 研究对象 |
| `research_date` | yes | 本次运行日期 |
| `account-profile` | yes | 账号、角色、音色、视觉和表达规则 |
| `reference_video` | Phase 0 only | 首次建立账号规格时使用；后续公司运行不需要 |
| `format_mode` | no | 默认继承账号的 `host_analyst`；`debate` 必须显式指定 |
| `target_duration` | no | 默认 18–25 分钟，不能降级为短视频 |

## Output

执行前读取 `references/global-contract.md`。本 Workflow 的账户资产、公司 run 输出、官方资料归档、pacing-plan 和视觉默认契约均在那里集中维护；各 Phase 的独有产物仍在本文件中声明。

### Account and company-run outputs

账号资产、公司 run 输出、官方资料归档、同行目录、券商材料和媒体产物的完整路径契约见 `references/global-contract.md`；本 Workflow 只在各 Phase 声明本阶段必须新增的产物。

## Principles

- Workflow 是流程事实源；资源用 Skill/Agent by-name 引用，不复制外部资源正文。
- Phase 的 Required Resources 必须真实执行并留下可识别产物；下游只消费已验收产物。
- 账号资产先于公司内容；公司名、数字、话题、音频路径和图表数据来自 manifest。
- 研究资料分为四条证据线：官方披露、结构化财务/行情、产业与周期研究、外部深度研究；任何一条线都不能静默替代另一条线。
- 公司研究额外必须覆盖第五条证据线：公司动态与产品事实，包括近期公告/新闻、获奖、产品发布、具体型号、项目签约/中标/交付、标准制定和技术里程碑；没有命中时也必须留下覆盖报告和缺口状态。
- 新闻发现优先使用 `multi-search` 的 `prefer_quality=True`（Tavily）；搜索摘要只做候选发现，最终事实必须打开原文并记录来源、事件日期、发布日期和主体核验。`news-search` 只作热点聚合补充。
- `deep-research` 只作为外部资料补充源；其报告中的数字和判断必须回到原始来源或结构化数据复核后，才能进入 Research Intelligence Document。
- 内容主线按报告新鲜度和经营重要性动态选择：最近 1–2 天发布且有重大经营变化时，财报可作为主线；否则以公司、业务或行业主线为主，财报作为验证或辅助章节。
- 官方资料路径、复用检查、命名和同行归档统一遵循 `references/global-contract.md` 与 cninfo-connector；公司新闻与产品资料统一落到 `research-materials/company-intelligence/`。
- 公司级 `editorial/episode-input.json` 是 Phase 2 生成器的输入事实与表达契约；生成器不得在代码中写死公司专属开场、自我介绍或估值内容。
- Phase 1 与 Phase 2 之间存在不可跳过的人工决策门：先生成 3–5 个互斥选题，人工明确批准一个 `topic_id`，再允许内容导演和脚本继续。
- `editorial-director-agent` 是全局内容导演：它决定主问题、开场、话题顺序、机制归属、观众收益和视觉意图；`financial-editor-agent` 负责证据/因果裁决，`dialogue-director-agent` 负责逐句互动，三者不得越权。
- 公司动态和产品事实必须先进入 `company-intelligence` 资产，再由内容导演决定是 opening、main_evidence、supporting_evidence、visual_only、background 还是 omit；研究员或脚本生成器不得直接把搜索结果写进口播。
- 一个核心机制只能有一个主章节；相邻章节必须有不同主问题、证据集合和观众收益，并在导演方案中留下去重与顺序理由。
- 开场使用独立顺序 `COLD_OPEN → INTRO → T01`：冷开场负责客观数据钩子，INTRO 负责目录和主持人定位；不得用固定自我介绍替代冷开场。
- 冷开场口播采用“事实反差 → 开放问题”：先用两个客观事实形成张力，再以“事实果真如此吗？”或同等开放问句收束；不得只罗列数据、先下结论或使用书面化的“利润快涨三倍”。
- 逐句音频是唯一时间轴来源；不得按性别整段拼接或用字数估时。
- `speaker alternation` 只是顺序门禁；对话关系必须由 `reply_to_turn_id`、`interaction_type`、`emotion` 和 `delivery` 表达。
- 图表优先于表格，表格优先于大段文字；观众不可见内部字段不得进入 HTML。
- Composition 默认使用 editorial-paper 视觉变体：暖纸面、衬线标题、深墨正文、红涨绿跌、细线结构和低圆角；只有 A/B 视觉实验才显式传入其他 --style。
- 音色缺失、身份不匹配或静默 fallback 时，停在音频门禁。
- `references/podcast-v1-luheng.md` 是当前稳定音频版本，使用 VoxCPM2 continuation；CosyVoice3、IndexTTS 和其他 clone mode 只作为独立 A/B。
- **数字口播简化**：亿级金额只说整数（"五十八亿"而非"五十八亿五"），千万级四舍五入到亿（"七个亿"而非"七亿三"），百分比用"X个点"（"十二个点"而非"十二点零零"）。详见 `account-profile/dialogue-policy.md`。
- **英文读法**：CPU 保持英文，GPU 可说"显卡"，ARM 整体发音（不逐字母拼读），NVIDIA 用"英伟达"。
- **字幕基线**：默认一条口播回合对应一条字幕，时间沿用该回合真实音频区间；允许自然换行，不按固定字数机械切碎。只有一个回合确实包含多个独立句群且画面需要分别强调时，才在 manifest 中显式拆 cue。
- **平台封面**：封面是独立 HTML 资产，不属于正片 Composition 时间轴；沿用同一 editorial-paper 背景和字体，显示公司名/栏目 logo、主标题和副标题，封面字号大于正片标题。封面数据来自 `episode-input.json` 的 `cover.title` 与 `cover.subtitle`。
- **官方报告归档**：Phase 1 前必须将公司半年报/年报 PDF 下载到 `outputs/companies/{company}/official-information/`，使用 cninfo-connector 标准文件名。下载前先查本地缓存。

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

## Phase 1: research — 公司与行业研究

### Goal

建立足以支撑 8–9 个话题的事实、正反证据、产业背景、核心优势、护城河、风险和可验证变量，并决定本期最值得讲的公司主线。

### Required Resources

| Resource | Type | Required | Use |
|---|---|---|---|
| `industry-analysis` | skill | yes | 产业链和竞争格局 |
| `industry-cycle-analysis` | skill | yes | 供需、周期和反证 |
| `investagent` | skill | yes | 公司研究和数据范围 |
| `tushare-connector` | skill | yes | 公司与同行的统一财务、三表和行情取数 |
| `earnings-reader` | skill | yes | 三表口径、盈利质量、现金流和同行财报阅读 |
| `multi-search` | skill | yes | `prefer_quality=True` 优先使用 Tavily，发现近期公司新闻、产品发布、型号、奖项、订单和交付线索；搜索摘要不得直接入稿 |
| `cninfo-connector` | skill | conditional | 年报、公告和法定披露 |
| `news-search` | skill | conditional | 多平台新闻聚合补充；只用于发现线索，必须回到原文核验 |
| `finance-report-analyzer` | skill | conditional | 同行 PDF/Excel 财报包的批量结构化和趋势图；有文件包时启用 |
| `deep-research` | skill | conditional | 行业、竞品、技术路线和市场结构的外部补充；出现公开资料缺口时启用 |
| `research-quality-gate` | skill | yes | 研究底稿和证据链验收 |

### Input

公司标识、研究日期、账号 profile、研究边界和初始同行宇宙（证券代码、比较角色、业务环节）。

执行前读取 `references/global-contract.md` 的 Company-run outputs 和 Official-source archive。

### Output

公司级 `outputs/companies/{company}/official-information/` 原件与 manifest、各研究资源的原生产物、`research-materials/peer-comparison/peer-comparison.json`、`research-materials/peer-comparison/peer-comparison.md`、`research-materials/editorial/company-thesis-card.json`、`research-materials/company-intelligence/event-facts.json`、`research-materials/company-intelligence/product-facts.json`、`research-materials/company-intelligence/source-ledger.json`、`research-materials/company-intelligence/coverage-report.md`、可选 `research-materials/deep-research/`、`findings-summary`、`topic-evidence-matrix.md` 和执行记录。

### Quality Criteria

- 至少 8 个候选话题，每个话题有矛盾、正反证据、来源、期间和视觉锚点。
- 必须生成 `company-thesis-card.json`，明确公司身份、核心优势、护城河机制、行业位置、增长驱动、风险、未来利润情景和财报在本期的角色。
- 必须根据最新财报公告日与研究日计算 `days_since_release`，并记录 `freshness`、`materiality`、`content_angle` 和选择理由；不得默认所有公司都使用财报主线。
- `content_angle` 仅可取 `earnings_led`、`company_led`、`industry_led`、`event_led`；最近 1–2 天发布且 `materiality=high` 时优先 `earnings_led`，其余情况优先从公司优势、行业位置或重大事件中选择。
- 必须提供至少两个不同的开场角度，其中至少一个围绕公司优势/护城河；选定角度必须能说明财报是主线、验证、反证还是背景。
- 必须完成公司动态与产品事实扫描，覆盖最近 180 天以及最近 2 年内仍影响当前主线的关键事件；至少查询公告/新闻、产品/型号、奖项/标准、订单/签约/交付四类关键词，并生成 `company-intelligence/coverage-report.md`。
- 每条入选动态/产品事实必须有 `fact_id`、事件日期、发布日期、事实类型、主体、原文 URL、来源级别、定位信息、与主线相关性和视觉候选；搜索摘要不得作为唯一来源。
- 产品型号、性能指标、奖项和项目规模必须优先由公司官网、正式公告、政府/行业组织或权威媒体原文支撑；无法核验的线索写入缺口，不进入事实正文。
- 关键数字有来源、口径、期间和定位；最新报告期与近 12 个月变化单列。
- 同行比较至少覆盖两个业务环节；每个环节至少保留 2 家有明确比较角色的上市公司，并注明业务重合度、并表范围和不可比项。
- `peer-comparison.json` 必须统一记录公司代码、比较角色、报告期、数据类型、单位、收入、归母净利、增速、毛利/净利率、经营现金流、自由现金流、应收、存货、资本开支、债务和估值；取不到的指标写明确缺口，不用空白或估算冒充。
- 同行表必须按同一报告期分组；Q1、H1、全年不得混成一张排名表。缺少同期数据时，降级为产业坐标并写入缺口清单。
- 同行关键数字至少有一手披露或结构化数据源；`deep-research` 只提供候选来源、行业背景和外部交叉线索，不能单独支撑公司事实。
- 同行官方报告必须归档到对应公司级 `outputs/companies/{peer_company}/official-information/`；当前 run 只保存引用路径和证据映射，不复制同行原件。
- 获取前必须执行本地复用检查；下载记录至少包含 `ts_code`、公司名、报告期、类型、公告日期、公告 ID、来源 URL、本地路径、文件大小和文本校验状态。
- 文件名必须符合 `{ts_code}_{period}_{document_type}_{announcement_date}.pdf`；不符合的历史文件在进入新 Workflow 前先建立 canonical manifest 映射。
- 没有足够证据、追问缺口或视觉锚点的话题不得进入 Phase 2。
- 没有完成公司动态与产品事实覆盖报告的话题不得进入 Phase 1.5；覆盖不足时必须标记 `coverage_status=degraded` 和具体缺口。
- 所有关键数字都能回溯到 `official-information/` 中的原始披露或明确标记的结构化行情源；不能只引用 `research-materials/` 二次摘要。

### Known Issues

未裁决的口径冲突不得进入事实正文；旧数据不能冒充当前变化；同行报告期或业务口径无法对齐时不得做简单排名；Phase 1 不生成买卖建议。

## Phase 1.5: topic-selection-and-approval — 候选选题与人工确认

### Goal

将 Phase 1 的研究资产转成 3–5 个角度互斥的选题候选，明确主问题、观众收益、开场、证据和风险，并在人工批准前停止下游生产。

### Required Resources

| Resource | Type | Required | Use |
|---|---|---|---|
| `finance-content-engineering` | skill | yes | 执行 topic-gen，按研究证据生成候选池，不直接决定最终选题 |
| `editorial-director-agent` | agent | yes | 评估候选的观众价值、事实张力、主线适配和互斥性；candidate 模式只能停在审批门 |

### Input

Phase 1 已验收的 `research-materials/editorial/company-thesis-card.json`、`topic-evidence-matrix.md`、`research-materials/company-intelligence/event-facts.json`、`product-facts.json`、`source-ledger.json`、`coverage-report.md`、findings-summary、研究 freshness/materiality、账号 audience/content policy 和可用视觉锚点。

### Output

- `editorial/topic-options.md`：供人工阅读的 3–5 个候选。
- `editorial/topic-options.json`：机器可消费的候选、证据 IDs、风险和互斥关系。
- `editorial/topic-approval.md`：人工审批表，必须明确 `status: pending|approved|rejected`、批准的 `topic_id`、`approved_at` 和备注。
- `editorial/phase1.5-execution.md`：资源 by-name、installed_ref、输入、候选覆盖、停止状态和 gate 结果。

### Quality Criteria

- 候选数量为 3–5 个，角度互斥；不能只是同一个事实换写标题。
- 每个候选必须包含：主问题、观众为什么关心、开场候选、核心证据、可展开路径、最大风险、content_angle 和 evidence coverage。
- 每个候选必须明确是否使用公司动态/产品事实，以及每条事实的 `fact_id`、`fact_role`（opening/main_evidence/supporting_evidence/visual_only/background/omit）和采用理由；不能只把新闻标题贴到选题里。
- 至少一个候选解释公司优势/护城河，至少一个候选解释优势兑现或未来验证；是否采用财报主线由 freshness/materiality 决定。
- 开场候选必须是事实张力加开放问题；公司简介、合作清单或单个技术事实不能自动成为主钩子。
- `topic-options.json` 必须记录候选间的 `mutually_exclusive_with` 和机制覆盖，便于后续去重。
- `topic-approval.md` 在用户确认前必须保持 `status: pending`；pending/rejected 状态不得生成 `director-treatment.md`、`episode-input.json`、`episode.json`、TTS、字幕、视觉或渲染产物。
- gate 必须能识别缺批准、批准 topic_id 不在候选中、批准时间缺失和候选不完整并给出 FAIL。

### Known Issues

人工确认是内容决策硬门，不是质量标准软建议；Agent 不能用默认候选、历史 run 或自己的判断代替批准。

## Phase 2: editorial-dialogue-design — 编辑与对话导演

### Goal

把已验收证据编排成自然的主理人播客逐句稿，并锁定口播、回应关系、情绪、delivery 和画面表达。

### Required Resources

| Resource | Type | Required | Use |
|---|---|---|---|
| `editorial-director-agent` | agent | yes | treatment 模式；读取已批准候选，锁定 editorial thesis、opening、topic order、机制去重和 scene intent |
| `financial-editor-agent` | agent | yes | 主命题、事实核验和冲突裁决 |
| `dialogue-director-agent` | agent | yes | host/analyst 回合、回应关系和表演字段 |
| `information-visualization-architect` | agent | yes | chart-spec，不补数据 |
| `debate-rounds` | skill | conditional | 仅 `format_mode=debate` |
| `finance-content-engineering` | skill | yes | 主口播改写：draft-script → polished-script，事实零漂移 |
| `human-understanding` | skill | yes | 将试听反馈还原为口语、关系和情绪约束；不直接改事实 |
| `humanizer-zh` | skill | yes | 对已改写的实际 episode 文本做二次审校，不只生成风格标签 |
| `boundary-rewrite` | skill | yes | 财经表达边界 |

### Input

Phase 1 已验收证据、已验收的 `company-intelligence` 事实资产、Phase 1.5 已批准的 `topic-approval.md` 与 `topic-options.json`、`research-materials/editorial/company-thesis-card.json`、账号 profile 和导演 treatment。

执行前读取 `references/global-contract.md` 的 Performance contract。

### Output

`editorial/episode-input.json`、`editorial/feedback-constraints.md`、`editorial/phase2-execution.md`、`podcast/script/episode-draft.json`、`podcast/script/episode-polished.json`、`podcast/script/episode.json`、`podcast/script/spoken-polish-diff.json`、`debate-script.md`、`dialogue-map.json`、`spoken-style-map.json` 和 `visual-plan/chart-spec.json`。

同时保留 `editorial/director-treatment.md`、`editorial/topic-order.json`、`editorial/opening-selection.json`、`editorial/scene-intent.json` 和 `editorial/director-execution.md`。

### Quality Criteria

- manifest 写入 `format_mode`、`role_map`、`turn_id`、`topic_id`、`speaker`、`text` 和 `evidence_ids`。
- manifest 的 topic/turn 必须能够回指 `fact_ids`、`fact_role`、`source_refs` 和 `visual_intent`；产品型号、奖项、签约、交付等事实不得只存在于导演私有笔记。
- `episode-input.json` 必须声明 `cover.title`、`cover.subtitle` 和 `outro`；`topics[]` 必须提供 `short_label`，供目录和持久导航使用。
- `episode-input.json` 必须声明 `opening.mode`、`opening.cards`、`opening.cold_open`、`opening.intro`；开场和自我介绍只能从该 manifest 读取。
- `episode-input.json` 必须携带 `content_angle`、`report_context`、`editorial_thesis`、`financial_data_role` 和 `opening_rationale`；Phase 2 不得绕过 Phase 1 的主线决策。
- Phase 2 开始前必须通过 topic approval gate；`topic_id`、opening 和 topic order 必须与批准记录一致。
- 必须消费 `editorial-director-agent` 的 treatment：每个话题有 audience payoff、机制归属、前后依赖、visual intent 和验证/证伪条件；缺少任一项不得生成最终 episode。
- 话题顺序必须有全局去重表：一个核心机制只有一个 `primary_topic_id`；相邻话题不得重复主问题、证据集合和观众收益。
- 开场 manifest 必须包含 `opening_mode`、`opening_cards` 和 `COLD_OPEN/INTRO` turns；冷开场后才出现主持人自我介绍和目录。
- `COLD_OPEN-01` 必须包含至少一组事实反差、一个开放问题和 `question_ending=question`；金额/增速采用自然口播，如“涨了快三倍”“反而下降了”。
- 生成 opening canary 时运行项目脚本 `build_podcast_opening_test.py`；脚本必须对 `COLD_OPEN → INTRO` 顺序、事实反差、开放问题和书面化禁用短语给出 PASS/FAIL。
- 每个话题至少有主理人立题、分析师直接回应、主理人承接/追问、分析师证据、主理人转场。
- 除话题第一句外，每句有 `reply_to_turn_id` 和 `interaction_type`；不能靠交替 speaker 制造对话。
- 情绪和 delivery 与回应关系共同生成；语气词服务于关系，不能机械重复。
- Phase 2 输出 emotion、delivery 和 pause anchors；Phase 3 先运行 resolve_pacing_plan.py，再消费稳定基线的 turn 级 speech_rate、target_rate_cps 和 pause_after_ms，并在 segments.json/audio-qa.json 留痕。
- 句首出现“对/嗯/没错/好”等短回应时，必须同时写入 `response_action=backchannel`、`backchannel`、`backchannel_target`、`filler_position=start`、`delivery=short_pause` 和正值 `pause_after_ms`；不能只把短词拼进普通长句。
- 数字分别锁定事实、自然口播和紧凑画面表达；不改变口径和事实方向。
- `human-understanding` 先把反馈转成约束；`finance-content-engineering` 直接改写 episode-draft；`humanizer-zh` 审校 episode-polished 并写回最终 episode.json。两者不能只更新 spoken-style-map，也不能在 Phase 3 随意改稿。
- `spoken-polish-diff.json` 必须记录每个 changed turn 的 before/after；draft/final 的 speaker、topic_id、evidence_ids 不得变化。存在用户口语化反馈时，运行 `scripts/check_spoken_polish.py --require-change`，无实际文本变化不得写 PASS。
- `check_podcast_dialogue.py` 必须阻断制作元话语（视频里、画面里、字幕里、必须说等）和其他公司名进入 spoken text；`check_spoken_polish.py` 对长篇稿件至少要求 10% turn 有实际 before/after 改写，不能用一两个虚词变化冒充全稿口语化。
- 每个话题有 chart-spec 或明确 no-chart 理由；可选 `valuation_context` 话题只消费官方或券商材料，不出现买卖建议、仓位或目标价。
- 话题排序必须服务于 `editorial_thesis`：至少一个话题解释公司优势/护城河，至少一个话题验证其兑现情况，至少一个话题讨论未来驱动和证伪条件；财报主线也不能把整期变成数字罗列。
- `valuation_context` 必须显式声明 `enabled`；启用时必须有 `topic_id`、`source_class=brokerage`、`source_dir=research-materials/brokerage/`、允许证据类型和禁用表达清单。未启用不阻断整期节目。
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

`episode.json`、项目 `account-profile` 的资源选择和显式 Workflow profile。默认稳定版本见 `references/podcast-v1-luheng.md`。

Phase 2 必须使用项目通用脚本 `scripts/build_podcast_episode.py` 从 `episode-input.json` 生成 episode、dialogue-map、spoken-style-map 和 chart-spec；该脚本不提供公司、话题或 OUTRO fallback，禁止调用带公司专属内容的历史 run 脚本作为新公司生成器。

执行前读取 `references/global-contract.md` 的 Performance contract，并只消费已锁定的 pacing_plan。

### Output

`podcast/audio/segments/`、`segments.json`、`narration-full.wav/mp3`、`subtitles.srt`、`podcast/qa/captions.json`、`audio-qa.json` 和执行记录。

### Quality Criteria

- 每个 turn 独立生成并按 manifest 顺序拼接；speaker 映射严格命中。
- 字幕时间来自真实 WAV；音频和 manifest 的文本、角色、后端、profile 可追溯。
- 编译完成后必须运行 `scripts/build_caption_manifest.py`，从真实 `segments.json` 生成 `podcast/qa/captions.json` 和最终 `subtitles.srt`；Composition 只消费该 caption manifest，不直接把整段 turn 文本当作一条字幕。
- 默认每个 turn 生成一条字幕 cue，起止时间来自该 turn 的真实音频；长文本由字幕容器自然换行，不用固定 20 字/40 字规则强制拆分。
- `references/podcast-v1-luheng.md` 使用 VoxCPM2 continuation、`voice.zhiwei + voice.luheng`、自然停顿和 natural 后处理；不启用 CosyVoice3、IndexTTS 或其他 clone mode。
- 通过音色、发音、尾词残留、杂音、响度、断句和文件可解码检查。
- TTS 完成后必须对最终 narration 或逐句 WAV 执行反向转写/已知文本对齐检查；`audio-qa.json` 必须记录转写文本、异常句、重生成次数和最终 PASS。发现乱码、漏词、重复词或句尾残留时，必须回到 Phase 3 重生成该 turn，不能只改字幕。
- 音频未通过不得进入视觉 Composition。

### Known Issues

v1 暂不解决 VoxCPM2 的高频颗粒、气声和部分末段动态问题；后续 prompt、音量处理或情绪控制优化必须作为新 profile/实验版本，不得静默改变 v1。

## 回写条目（来源: cosyvoice3-production-backend-selection）

- 当前 `podcast-v1-luheng` 的生产后端为 VoxCPM2 continuation；后端切换前必须先通过同一 `COLD_OPEN + INTRO` canary 和人工试听。
- 当前 profile 固定使用自然停顿、natural 后处理和 luheng 情绪参考资产；其他后端和 clone mode 属于独立实验分支。

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
- 每个核心数据图至少使用一种可感知的 seek-safe 动画：数字滚动、柱体生长、曲线绘制、瀑布展开、路径/节点出现或重点标注；动画必须由 `hyperframes-animation` 规则和 `scene-manifest.json` 指定。
- 目录使用紧凑的章节网格或分组导航，不把完整长问题堆成同尺寸胶囊；目录文字必须来自 manifest 的短标签。
- OUTRO/SUMMARY 必须有总结性视觉资产（验证看板、三道门、结论矩阵或指标卡）和一句来自 manifest 的收束文字；不得以空白画面作为结尾状态。
- 字幕、说话人高亮、图表、音频和导航使用同一真实时间轴。
- `COLD_OPEN`、音频和第一条 caption 均从 0 秒开始；`cover.html` 是独立平台封面，不得出现在正片 timeline。
- **字幕密度**：默认一回合一条字幕，贴合沪电股份基线；字幕时间覆盖该回合真实语音区间，长句自然换行，不按固定字数机械截断。字幕数字使用阿拉伯数字（如"58亿""7个亿""12%"），不用中文数字。
- **平台封面**：Phase 4 必须生成独立的 `podcast/project/cover.html`，沿用 Composition 的同一背景、字体和视觉 Token，只展示公司名/栏目标识、引人注目的主标题和副标题，标题字号大于正片标题。封面必须包含账号 logo，并分别使用 `scripts/render_cover_4x3.js` 导出 4:3 的 `cover.png`（推荐 1440×1080）、使用 `scripts/render_cover_3x4.js` 导出 3:4 的 `cover-3x4.png`（推荐 1080×1440）；封面独立于正片时间轴。
- 平台封面默认不进入正片时间轴，不产生音频、字幕或 `segments.json` 时长；正片 `COLD_OPEN` 必须从 0 秒开始。若明确需要片头封面动画，必须将同等时长同步加入音频、字幕和所有 Scene 时间轴，并单独标记为 in-video cover。
- 底部章节导航和进度条是 root-level persistent layer，章节宽度按真实音频时长比例计算。
- 进度条、章节边界和 Scene 区间必须共用同一套全局累计时间线：每个区间记录 `start_ms`、`end_ms`、`duration_ms`，首段从 0 开始，后段 `start_ms` 必须等于前段 `end_ms`；不得为章节重新从 0 计时或用局部比例重算。
- 页面切换、图表插播和 Scene 复用时导航不重置、不消失。
- 图表优先于表格和文字；观众不可见字段不得进入 HTML。
- 采用的公司动态和产品事实必须通过通用 event-card、product-card、server-spec-card 或 milestone-timeline Scene 呈现；不得把搜索摘要、未经核验的产品图或奖项标题直接放进 HTML。
- 运行 `check_public_copy.py` 和 `caption_gate.py verify`。
- 运行全局时间线检查，验证 progress、chapter ranges、Scene、caption 和 audio segments 使用同一累计区间；发现区间断裂、重叠或进度语义不一致时 FAIL。
- 运行字幕密度检查，确认 `podcast/qa/captions.json` 默认每个 turn 只有一条 cue、起止时间覆盖真实语音，且平台封面单独截图、不参与正片时长。
- 运行 `hyperframes-animation/scripts/animation-map.mjs` 并在开场、目录、至少两个核心话题和结尾抓取 snapshots；视觉审阅必须记录结论，不只检查 DOM/媒体流。

### Known Issues

长片优先使用 topic sub-compositions；图表必须支持公司间数字、标题长度和缺失字段变化。当前 delivery 仍主要进入 segments.json 记录；需要实际改变节奏时使用 pacing_plan，不要把 delivery 标签本身误判为已完成的表演控制。

## Phase 5: render-and-regression-qa — 渲染与复用门禁

### Goal

验证成片可播、研究一致、音频同步、视觉达标，并证明第二家公司只替换 manifest 即可复用。

### Required Resources

| Resource | Type | Required | Use |
|---|---|---|---|
| `hyperframes-cli` | skill | yes | check、snapshot、render 和诊断 |
| `hyperframes-animation` | skill | yes | animation-map 和动态节奏审计 |
| `static-html-qa` | skill | yes | HTML、数字、边界和视觉回归 |
| `research-quality-gate` | skill | yes | 研究、脚本、字幕和证据一致性 |

### Input

完整 Composition、最终音频、字幕、episode manifest、账号 profile 和第二家公司最小测试输入。

### Output

`podcast/renders/draft.mp4`、`final.mp4`、可选 `podcast/opening-test-v4/renders/opening-canary-v4.mp4`、`podcast/qa/episode-qa.md`、`reuse-regression.md` 和执行记录。

### Quality Criteria

- 音频逐句交替、音色正确、字幕同步、导航连续、图表状态完整。
- 公共文案、数字一致性、字体、溢出、时长和渲染性能通过门禁。
- 检查 `content_angle` 与 `report_context` 的一致性；非新鲜财报不得无理由使用固定的财务反差开场，跨公司重复开场需回到公司主线卡复核。
- 检查 Phase 1.5 的批准记录与导演 treatment 一致；没有人工批准的 run 不得进入渲染。
- 检查话题全局顺序、机制主章节和相邻话题去重；发现多个章节重复同一机制时，必须退回 Phase 2 重新编排。
- 检查反向转写 QA 已对所有重生成句完成闭环，异常句不能只通过字幕替换掩盖。
- 检查 progress/chapter/scene/audio/caption 的全局累计区间一致。
- 检查所有可见新闻、奖项、产品型号、性能和项目事实均能回指 `fact-card-manifest.json` 与已打开原文；缺来源或只来自搜索摘要时 FAIL。
- 开场回归优先运行 `scripts/build_opening_canary.py`，只截取 `COLD_OPEN + INTRO` 生成短视频，先完成视觉审阅再进入长片渲染。
- 第二家公司只替换 manifest 即可完成 draft render，不改模板源码。
- 所有事实可回溯，财经边界检查通过。

### Known Issues

只在单家公司通过不算 Workflow 完成；必须保留第二家公司复用回归证据。

## Evolution Log

| Date | Change | Basis |
|---|---|---|
| 2026-08-22 | 建立长篇双人账号 Workflow，明确 host_analyst、逐句音频、图表优先和跨公司门禁 | 用户目标、参考节目蒸馏和既有资源 |
| 2026-08-27 | 曾将 `podcast-v1-luheng` 切换为 CosyVoice3 zero-shot 进行 A/B；随后根据完整视频试听反馈恢复 VoxCPM2 continuation 作为当前稳定后端 | 中科曙光 opening canary、完整视频 A/B 与用户试听反馈 |
| 2026-08-23 | Phase 1 增加同行比较资料契约与四条证据线：tushare-connector / earnings-reader / cninfo-connector / industry-analysis / industry-cycle-analysis / finance-report-analyzer / deep-research；同行原件、统一比较表和外部深研资料分目录 | 用户要求补齐同行比较并接入 deep-research；东山精密运行检查发现同行仅有 raw stock_basic/income，缺少统一报告期、三表和口径加工 |
| 2026-08-24 | 历史音频基线曾沿用 VoxCPM2、情绪参考音频和逐句 WAV；当时只补可执行的语速/句内停顿计划 | 用户试听反馈；107 段 segments.json 的字速/停顿统计；podcast-audio-compiler 与 podcast-workflow 资源复核 |
| 2026-08-24 | 固化通用视觉质量门禁：scene manifest、多 beat Scene、数据动效、紧凑目录、非空总结结尾、animation-map、snapshot 和 opening canary | `generic-video-visual-direction` Experience；东山精密 opening canary 与 Composition check 验证 |
| 2026-08-25 | 历史 profile 曾固化 VoxCPM2 音频基线：整句级语速、自然停顿和现有情绪资产 | 用户试听反馈；opening canary A/B；podcast-audio-compiler 与 podcast-workflow 资源复核 |
| 2026-08-26 | 增加基于财报新鲜度与经营重要性的内容主线决策；要求公司主线卡、财报角色和非模板化开场证据 | 用户反馈：财报新发布时可作为重点，其他情况下应服务于公司优势、护城河与未来前景 |
| 2026-08-27 | Phase 1 增加公司动态与产品事实证据线；`multi-search` 质量优先使用 Tavily，`news-search` 仅作聚合补充；新增 event/product facts、source ledger、coverage report 和 fact-card-manifest 交接 | 用户要求补齐中科曙光近期新闻、获奖、产品型号和项目事实；Tavily 实测可用，搜索摘要必须回到原文核验 |

## 回写条目（来源: company-intelligence-news-product-facts）

- 公司动态/产品事实扫描成为 Phase 1 的第五证据线；Phase 1.5 必须把 fact_id 和 fact_role 交给内容导演，Phase 2/4 必须保留来源和视觉交接。

## 回写条目（来源: podcast-editorial-gate-and-audio-render-regression）

- 一次人工 Topic Approval 后，主线与支撑章节关系由导演方案锁定；Phase 3 使用已知文本对齐，Phase 4/5 使用 pause-aware 全局时间线和独立动态事实卡 QA。
