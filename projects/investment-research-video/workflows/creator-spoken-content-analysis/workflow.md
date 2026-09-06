# Workflow: creator-spoken-content-analysis

> 位置: Project: projects/investment-research-video/workflows/creator-spoken-content-analysis/

## Mission

把参考博主的一批视频转成可审计的口播分析与可迁移的内容规则：先确认真实口播文本和说话形态，再归纳叙事大类、单期结构、开场钩子、证据推进、语言风格、节奏、互动与收束方式，最后把通过边界审查的规则吸收到本项目的视频生产 Workflow。目标是学习内容机制，不复制博主的人设、原句、具体投资结论或未经核验的事实。

## Input

- 参考视频目录，至少包含视频或音频文件；目录中的标题 `.txt` 只能作为索引，不能自动当作口播稿。
- 博主名称、素材批次日期和可选的账号/发布时间信息。
- 可选：已有字幕、人工转写、视频链接、评论数据；如果已有高质量转写，优先使用并保留来源。
- 本项目当前 `account-profile`、内容政策和现有视频生产 Workflow，作为迁移边界与冲突检查依据。

## Output

正式运行目录为 `outputs/creator-analysis/{creator}/{run_date}/`，至少包括：

- `source-manifest.json`：源文件、时长、转写方法、speaker mode 与缺失项；
- `asr-{model}/`：逐条 `transcript.md`、`transcript.json` 和总 manifest；
- `corpus-catalog.md`：每条视频的题型、时长、开场、结构、收束、证据与不确定项；
- `distillation-report.md`：跨视频归纳、证据引用、置信度、可迁移规则与反例；
- `adoption-candidates.md`：准备吸收到现有视频 Workflow 的规则，逐条标注 owner、适用条件和验证任务；
- `phase*-execution.md`：每个阶段的真实执行回执。

## Principles

- `best_available_resource`：按实际效果、输出质量、稳定性、依赖成本、维护成本和当前项目适配性选择资源；文本优先不等于标题优先。
- 真实来源优先：标题、话题标签和封面用于发现与分类；叙事和风格判断必须尽量引用口播转写及时间戳，关键结论抽查原音频。
- 先判定说话形态：`single-speaker-monologue`、`dialogue_like_single_track`、`multi-speaker` 或 `unknown`。ASR 默认不提供 speaker diarization，不得凭语气猜 speaker 姓名。
- 功能回合优先：拟对话素材先标注“主张/追问/反驳/解释/收束”等功能；只有获得听辨、声纹或分离证据后才命名角色。
- 蒸馏机制，不蒸馏表面：抽取结构、认知推进、节奏和观众价值；不照搬口头禅、辱骂、原句、人设、公司判断或具体数字。
- 规则必须能执行和验证：每条候选规则都要写触发场景、操作步骤、反例、内容边界和一个回归样例。
- 财经边界优先：保留“预期差、估值、证伪条件和风险”的分析价值，但不得生成买卖、仓位、目标价、收益保证或未经证实的荐股表达。
- 失败也要产物：缺少真实转写、speaker 无法判定或 ASR 质量不足时，输出降级报告并阻止把该结论写入生产规则。

## Phase 1: source-and-speech-preflight — 素材与口播形态确认

### Goal

建立可追溯的素材清单，区分标题文本与真实口播，确认音频时长、声道、转写来源和 speaker mode。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| `douyin-blogger-analysis` | skill | 可选 | workspace installed_ref | 适合从抖音采集、下载、截图和外部字幕；已有本地素材时不重复下载 |
| `faster-whisper` | skill | 必选 | workspace installed_ref | 本地中文 ASR；有时间戳但默认没有 speaker diarization，关键术语需回听 |
| `media-use` | skill | 可选 | workspace installed_ref | 已有音频需要统一转写/媒体处理时使用；不以估算字数代替声学证据 |

### Input

参考素材目录和创作者元信息。

### Output

`source-manifest.json`、`asr-{model}/manifest.json`、speaker mode 判定和 `phase1-execution.md`。

### Quality Criteria

- 每个输入条目都有源路径、媒体类型、时长、是否有口播音频、转写来源和状态。
- `.txt` 只有在内容确认为字幕/转写时才进入正文分析；标题/标签单独标为 metadata。
- 记录声道检查；双声道复制不得解释为两个 speaker。
- 若出现多人或拟对话，至少抽查一条音频并把身份判定写成 `confirmed`、`inferred` 或 `unknown`。
- 未有真实口播文本时，Phase 1 只能输出 blocked/degraded，不进入跨视频蒸馏。

### Known Issues

ASR 会把财经专名、数字和人名识别错；本阶段只证明“有可分析文本”，不证明事实正确。GPU 运行库缺失时可切 CPU，但必须记录模型、设备和降级原因。

## Phase 2: corpus-coding — 单条视频编码与叙事分类

### Goal

逐条编码开场、问题、主张、证据、反方/追问、解释、判断、条件和结尾，建立可比较的叙事语料库。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| `cangjie-skill` | skill | 必选 | workspace installed_ref | 把长内容方法论抽成可执行单元；本 Workflow 只借用其验证思想，不自动把博主变成 skill |
| `human-understanding` | skill | 必选 | workspace installed_ref | 将观众问题、认知负担和表达收益转成编码字段 |
| `finance-content-engineering` | skill | 必选 | workspace installed_ref | 检查财经事实边界、口语表达和数字是否需要铺垫 |

### Input

通过 Phase 1 的转写稿、时间戳和 source manifest。

### Output

`corpus-catalog.md`、逐条编码记录、叙事分类及 `phase2-execution.md`。

### Quality Criteria

- 每条视频至少记录：hook、audience question、core claim、evidence sequence、counterpoint、payoff、ending、CTA/disclaimer、speaker mode、confidence。
- 分类采用“主类 + 次类”，不得用题目标签替代叙事结构。
- 记录至少一个具体时间戳证据；无法判断的字段写 `unknown`，不能补全。
- 识别“信息播报”“观点解读”“机制教学”“市场周报”“拟对话解释”等不同节目功能。
- 对同一模式至少找到两条独立样本，才可进入跨视频规则候选。

### Known Issues

同一博主可能把单人脚本写成多角色问答；“你怎么看”不等于真实双人。转写断句也不等于自然停顿，需要保留音频抽查任务。

## Phase 3: narrative-and-style-distillation — 跨视频蒸馏

### Goal

从语料库提取稳定、可迁移、可测试的叙事和口播规则，并把有效机制与高风险表面特征分离。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| `cangjie-skill` | skill | 必选 | workspace installed_ref | 跨样本验证、候选单元筛选和边界记录 |
| `boundary-rewrite` | skill | 必选 | workspace installed_ref | 将冲击性财经表达改成边界内等价表达，不抹平判断力度 |
| `finance-content-engineering` | skill | 必选 | workspace installed_ref | 统一承载口语化、真实双人表达、概念命名意识与趣味表达；本 Workflow 不把它们拆成多个调用 |

### Input

已验收的 `corpus-catalog.md` 和转写证据。

### Output

`distillation-report.md`、`adoption-candidates.md` 和 `phase3-execution.md`。

### Quality Criteria

- 每条候选规则有至少两条样本证据、适用场景、反例、置信度和验证方式。
- 至少覆盖：叙事大类、开场、认知推进、证据顺序、拟对话/回合、口语节奏、幽默与比喻、结尾和 CTA。
- 将“可迁移机制”“仅适合该博主的人设”“不可吸收的风险表达”分栏。
- 不把博主的投资结论当作本项目结论；不把一次性热点或单条金句升格为规则。
- 产出一份本项目可执行的最小规则集，不超过现有 Workflow 能验证的范围。

### Known Issues

28 条视频足以做首轮模式发现，但不足以证明长期效果；不能从本批素材推断播放量、完播率或转化率。没有平台数据时，增长判断只能写成待验证假设。

## Phase 4: adoption-and-regression — 吸收、验证与交接

### Goal

把通过筛选的规则合并到本项目现有视频生产链的合适章节，并用新旧题型样例验证不破坏事实、合规和可复用性。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| `editorial-director-agent` | agent | 必选 | workspace installed_ref | 接收开场、叙事模式与增长承诺规则；不接受博主专属人设复制 |
| `dialogue-director-agent` | agent | 必选 | workspace installed_ref | 接收回合、拟对话和口语节奏规则；speaker 身份仍需证据 |
| `research-quality-gate` | skill | 必选 | workspace installed_ref | 验证研究、脚本、字幕和证据链一致性 |
| `boundary-rewrite` | skill | 必选 | workspace installed_ref | 对吸收后的财经口播做边界扫描 |
| `experience-curator` | skill | 可选 | workspace installed_ref | 只有用户确认要沉淀跨项目经验时才归档 Experience |

### Input

`adoption-candidates.md`、现有视频 Workflow、一个公司/财报题和一个行业/市场题的测试输入。

### Output

现有 Workflow 的最小可审阅补丁、`adoption-review.md`、回归样例和 `phase4-execution.md`。本 Workflow 本身不自动修改生产规则，除非吸收项已通过本阶段验收。

### Quality Criteria

- 每个吸收项只写入一个明确 owner 章节，保留来源引用和适用条件。
- 至少验证一个财报解读题、一个市场轮动/行业题；两者均能保持单一核心判断、证据边界和财经合规。
- 口播规则不要求复制“老灯/韭菜”等特定称呼，不引入买卖、目标价、仓位或收益承诺。
- 运行项目既有脚本/门禁，并留下差异、失败项和未验证项。
- 只有通过的候选进入生产 Workflow；其他候选留在分析报告中，不伪装成项目规范。

### Known Issues

吸收规则属于内容实验，不能直接宣称提升流量。后续必须用播放、留存、完播、评论、收藏、分享和关注等真实数据复盘，再决定是否写入长期账号资产。
