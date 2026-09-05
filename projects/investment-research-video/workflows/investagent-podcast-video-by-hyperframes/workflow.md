# Workflow: investagent-podcast-video-by-hyperframes

> 位置: Project: projects/investment-research-video/workflows/investagent-podcast-video-by-hyperframes/

## Mission

把用户已批准、且经 `topic-research` 验收的财经议题，制作成有明确观点、自然双人表达、可追溯证据和完整增长承诺的 HyperFrames 视频。公司财报只是可选证据，不是默认叙事模板；本 Workflow 不重新选题、不补研究。

默认节目形态是 `host_analyst`：主理人承担观众问题与节奏，分析师承担主要证据与判断。只有导演显式选择且证据支持时才使用 `debate`。

## Input

- 用户已批准的 topic card，字段来自 `topic-forward-candidate.json.template`；
- `topic-research` 已验收、Scope Decision 为 `accepted` 的 `research-brief.md` 与 source ledger；
- `account-profile` 账号、角色、音色、视觉和内容规范；
- 目标平台、画幅、期望时长与发布方式。

结构化 `editorial/episode-input.json` 必须按 `investment-video-episode-input.json.template` 生成。研究对象可为公司、行业、主题、事件、技术、政策、宏观或比较；非公司议题不得被强制补成公司财报视频。

## Output

正式运行目录为 `outputs/subjects/{subject_id}/{run_date}/`，完整路径约定见 `references/global-contract.md`。主要产物包括导演方案、锁定逐句稿、音频与字幕、HyperFrames Composition、横竖封面、最终视频、QA 报告和可选发布回执。

## Principles

- 下游只消费已批准 topic card 与已验收 research brief；研究推翻前提或主体/主问题变化时返回 `topic-forward-lead`，不在生产中二次选题。
- 内容导演负责最终主张、叙事模式、开场、证据顺序和结尾；财经责任编辑负责事实与因果；对白导演负责自然互动；制作只执行锁定方案。
- 每期只有一个明确、有依据、可争辩、可证伪的主张。必须说清机制、时间范围、受影响环节、最强反证和推翻条件。
- 流量是产品目标，但增长承诺必须一致：选题给点击理由，封面与标题承接点击，开场与章节承担留存，正文提供收藏/分享价值，结尾给互动与关注理由。
- 财报、现金流和估值只在问题需要时进入内容；不得默认公司介绍 → 财报 → 风险，也不得把“看后续财报”当结论。
- 开场可用观点、事件、案例、产业冲突、技术演示、问题或数字；不强制问号、反差词、数据卡或 INTRO。
- 一个核心机制只有一个主章节。每个模块必须带来答案、新证据或认知变化；不推进判断的资料合并或删除。
- 允许明确讨论多空、竞争力、估值和受益顺序；禁止直接荐股、交易指令、仓位和收益保证。
- episode manifest 是音频、字幕、视觉和封面的共同事实源；逐句真实音频是唯一时间轴。
- Required Resources 按 by-name 引用，必须真实执行并留下独立产物；下游只消费已验收结果。

## Phase 1: editorial-and-dialogue — 主张、叙事与逐句稿

### Goal

从批准卡与研究结论中选定唯一主张和讲法，锁定增长承诺、模块顺序、逐句回应关系、结尾判断和视觉意图。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| `editorial-director-agent` | agent | 必选 | internal v0.3 | 选择主张、叙事、开场、模块与结尾；不补研究 |
| `financial-editor-agent` | agent | 必选 | internal installed_ref | 裁决事实、口径与因果强度 |
| `dialogue-director-agent` | agent | 必选 | internal installed_ref | 逐句互动、角色关系与听觉节奏 |
| `information-visualization-architect` | agent | 必选 | internal installed_ref | 把证据需求转成 chart/scene intent，不补数据 |
| `finance-content-engineering` | skill | 必选 | workspace installed_ref | 口语化与事实零漂移 |
| `human-understanding` | skill | 必选 | workspace installed_ref | 将试听与受众反馈转成表达约束 |
| `humanizer-zh` | skill | 必选 | workspace installed_ref | 对实际逐句稿做中文自然度审校 |
| `boundary-rewrite` | skill | 必选 | workspace installed_ref | 保留观点力度并守住财经表达边界 |
| `debate-rounds` | skill | 可选 | workspace installed_ref | 仅 `format_mode=debate` 时使用 |

### Input

批准 topic card、已验收 research brief/source ledger、account profile、目标平台与时长。执行前读取 `references/global-contract.md` 和 `content-policy.md`。

### Output

`outputs/subjects/{subject_id}/{run_date}/editorial/` 下的 `director-treatment.md`、`topic-order.json`、`opening-selection.json`、`scene-intent.json`、`feedback-constraints.md`、`episode-input.json`、`director-execution.md` 与 `phase1-execution.md`；`podcast/script/` 下的 draft、polished、最终 `episode.json`、对白图、口语化差异和 chart spec。

### Quality Criteria

- 运行 `check_editorial_gate.py`，直接核验上游批准卡、accepted research brief 和导演交接；不得创建本地候选池或伪造第二次批准。
- `episode-input.json` 使用 `investment-video-episode-input.json.template`，包含同一组点击理由、观看承诺、互动价值和关注理由。
- `editorial_thesis` 明确回答批准问题；thesis contract 包含机制、时间范围、受影响环节、最强反证、推翻条件和证据引用。
- 导演先比较 2–3 个轻量叙事/开场方案；证据只支持一种时记录原因。可选模式包括行业地图、公司案例、比较、事件追踪、技术解释、政策影响、神话证伪和问答。
- 每个模块有不同 audience payoff、认知弧、证据推进、机制归属和 shot proposition；相邻模块不得重复同一答案。
- `COLD_OPEN` 从 0 开始，INTRO 可选；前 10 秒说明为什么值得继续看，正文标明兑现位置。
- OUTRO 必须口头表达当前判断、机制、时间范围、受影响环节和推翻条件，并给出与内容有关的讨论/关注理由；“看后续财报”不能单独收束。
- `build_podcast_episode.py` 只消费 manifest，不提供公司、话题或结尾 fallback。
- 运行 `check_podcast_dialogue.py` 和口语化/重复检查；具体台词不得包含制作元话语或直接交易建议。
- `director-execution.md` 做 audio-only 语义验收，引用具体台词证明开场、主张、反证、结尾和增长承诺已兑现。

### Known Issues

字段齐全不等于内容好看。若观点仍是“两边都有可能”或结尾把答案推给未来报告，必须退回导演重写；证据不足则退回 `topic-research`，不能在脚本阶段补事实。

## Phase 2: podcast-audio-compile — 逐句音频与字幕

### Goal

把锁定的 episode manifest 编译成角色正确、自然可听、可反向核验的逐句音频和字幕。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| `podcast-audio-compiler` | skill | 必选 | workspace installed_ref | 逐句 TTS、拼接、字幕和音频 QA |
| `media-use` | skill | 必选 | workspace installed_ref | 音频媒体接入与资产记录 |
| `hyperframes-audio` | skill | 可选 | workspace installed_ref | 已有音频需要混音时使用 |

### Input

已锁定 `episode.json`、账号音色资源和 pacing plan；稳定音频 profile 见 `references/podcast-v1-shenyan.md`。

### Output

`podcast/audio/segments/`、`segments.json`、`narration-full.wav/mp3`、`subtitles.srt`、`podcast/qa/captions.json`、`audio-qa.json` 和 `phase2-execution.md`。

### Quality Criteria

- 每个 turn 独立生成并按 manifest 顺序拼接；文本、角色、voice/profile 与参数可追溯。
- 文本、speaker、参考音色或 pacing 变化时使缓存失效，不能只凭同名 WAV 复用。
- 字幕时间来自真实音频；默认每个 turn 一条 cue，必要时由 manifest 显式拆分。
- 执行反向对齐与独立 ASR；漏词、重复、乱码、尾词或角色错误必须重生成对应 turn。
- 运行 artifact consistency 检查，episode、segments、captions、字幕和真实时长一致后才可进入视觉阶段。

### Known Issues

停顿优先在脚本中通过短句和真实回合解决；固定静音只用于局部明确需求。后端切换必须先通过同一 opening canary 和人工试听。

## Phase 3: podcast-composition — 视觉、封面与时间轴

### Goal

把锁定脚本、图表、音频和字幕编译成与叙事匹配的 HyperFrames Composition 和独立平台封面。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| `hyperframes` | skill | 必选 | workspace installed_ref | Composition 与渲染入口 |
| `hyperframes-core` | skill | 必选 | workspace installed_ref | tracks、timing 与确定性契约 |
| `hyperframes-animation` | skill | 必选 | workspace installed_ref | seek-safe 动画与节拍 |
| `hyperframes-creative` | skill | 必选 | workspace installed_ref | 视觉方向与排版 |
| `information-visualization-architect` | agent | 必选 | internal installed_ref | chart spec 到 scene 的映射 |
| `static-html-qa` | skill | 必选 | workspace installed_ref | HTML、溢出、数字和公开文案检查 |

### Input

account profile、episode、chart spec、segments、captions、最终音频与 Phase 1 scene intent。

### Output

`podcast/visual-plan/scene-manifest.json`、`podcast/project/`、独立 `cover.html`、1440×1080 `cover.png`、1080×1440 `cover-3x4.png`、可检查 HTML 和 `phase3-execution.md`。

### Quality Criteria

- 模板只消费 manifest/variables；公司、行业、事件、数字和结论不得写死在源码。
- 视觉模式服从 narrative mode。每个关键 scene 说明展示什么、为何此刻展示、观众多知道什么。
- 口播、图表、B-roll、字幕各有职责，不重复堆同一句信息；图表优先表达比较、趋势和机制。
- 章节、scene、caption、audio 和进度条使用同一累计时间轴；`COLD_OPEN` 从 0 秒开始。
- 封面只承接本期点击理由和研究对象，横竖版分别排版，不进入正片时间轴；生成后实际核对尺寸与手机可读性。
- 默认副标题 fallback 为“{subject} 深度解析”，不得把非财报题自动写成“财报解读”。
- OUTRO 有与当前判断相匹配的总结视觉，不使用固定现金流/财报文案替代本期结论。

### Known Issues

视觉变化服务于认知推进，不为避免重复而制造噪声。长片可使用 topic sub-compositions，但全局导航和音频时间线不得重置。

## Phase 4: render-and-regression-qa — 渲染与成片门禁

### Goal

证明成片可播、事实一致、音画同步、增长承诺兑现，并验证模板不依赖单一公司或财报题。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| `hyperframes-cli` | skill | 必选 | workspace installed_ref | check、snapshot 与 render |
| `hyperframes-animation` | skill | 必选 | workspace installed_ref | 动画与节奏审计 |
| `static-html-qa` | skill | 必选 | workspace installed_ref | 公开文案、数字、字体和布局回归 |
| `research-quality-gate` | skill | 必选 | workspace installed_ref | 研究、脚本、字幕和证据一致性 |

### Input

完整 Composition、最终音频与字幕、episode、批准卡、research brief、account profile 和第二个 subject/变体的最小测试输入。

### Output

`podcast/renders/draft.mp4`、`final.mp4`、`podcast/qa/episode-qa.md`、`reuse-regression.md`、代表性 snapshots 和 `phase4-execution.md`。

### Quality Criteria

- 标题/封面、开场、正文和结尾兑现同一点击与观看承诺；不可用标题党掩盖正文偏题。
- 主张、机制、最强反证和推翻条件与 research brief 一致；新增事实或口径漂移 FAIL。
- 音色、字幕、章节、图表、进度和转场按同一真实时间轴运行。
- opening canary 先通过，再渲染长片；关键模块和 OUTRO 均抓取 snapshot 审阅。
- 第二个非同类 subject 或视觉/叙事变体只替换 manifest 即可完成 draft，不修改模板源码。

### Known Issues

单一 subject 成功不能证明复用性；第二个变体失败时应新增明确适配模式，而不是写入某家公司特例。

## Phase 5: publish-and-handoff — 发布与复盘移交

### Goal

为目标平台生成一致但非机械复制的标题、封面和文案；在用户明确授权后发布，并把真实作品与增长假设交给 `publish-review`。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| `video-agent-publisher` | skill | 必选 | workspace installed_ref | 平台差异化标题、描述、标签和来源 |
| `aitoearn` | skill | 可选 | workspace installed_ref | 用户授权的平台上传、排期和状态回传 |
| `social-auto-upload` | skill | 可选 | workspace installed_ref | 主发布通道明确失败且无重复提交风险时回退 |
| `douyin-creator-tools` | skill | 可选 | workspace installed_ref | 发布后作品与评论采集，不替代发布接口 |

### Input

通过 QA 的 final.mp4、横竖封面、episode、来源清单、增长 contract、目标平台和用户明确的发布/排期授权。

### Output

`publish/metadata.json`、`sources.md`、平台请求与结果、`publish-execution.md`；成功后更新真实作品记录，并向 `publish-review` 移交作品链接、发布时间、题材、时长、增长承诺和本期唯一内容实验。

### Quality Criteria

- 标题、封面与描述准确承接点击理由，平台版本可不同但不得改变事实与主张。
- 未获得真实发布授权时只生成草稿；状态未知时不得切换工具重复提交。
- 逐平台记录状态、作品链接、错误和用户操作；不得把任务 ID 当作品 URL。
- 复盘按曝光 → 点击/播放 → 2 秒/5 秒 → 平均观看/完播 → 点赞/评论/收藏/分享 → 主页访问 → 关注的漏斗接收数据。

### Known Issues

平台接口、授权和确认流程可能变化；创建发布任务不等于作品发布成功，必须追踪最终状态。
