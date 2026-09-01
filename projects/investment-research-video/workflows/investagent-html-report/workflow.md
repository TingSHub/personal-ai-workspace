# Workflow: investagent-html-report

> 位置: Project: projects/investment-research-video/workflows/investagent-html-report/workflow.md

## Mission

最短生产链路验证与执行：三个成熟研究 Skill 并行研究（industry-analysis + industry-cycle-analysis + investagent）→ 冲突检查与裁决（无新 Agent）→ Financial Editor 形成 Editorial Master → Finance Presentation Agent 生成 HyperFrames-native 企业研究 HTML。

服务对象：对上市公司研究感兴趣的普通投资者。产出「看懂公司/行业/周期/财务/经营变化/估值分歧/风险」的企业研究内容页——**不是投资推荐**。

核心约束：不创建 Research/Content/Visual Director 等新 Agent；研究 Skill 原生执行、不修改外部 Skill；结构服从信息，不服从模板；Presentation 与 Video 共用同一套 Scene Composition。

## Input

| 字段 | 必填 | 说明 |
|---|---|---|
| company_id | 是 | 公司代码（如 600519） |
| company_name | 是 | 公司名称（如 贵州茅台） |
| research_date | 是 | 运行日期（YYYY-MM-DD），同时是输出目录层级 |
| 已有研究产物 | 否 | 若有当日/近期原生产物，可复用并如实记录，避免重跑 |

## Output

| 产物 | 位置 | 格式 |
|---|---|---|
| 三份研究原生产物 + findings-summary | `outputs/companies/{company_name}/{research_date}/research-materials/{skill}/` | skill 原生格式（HTML/markdown/多文件），不强制转换 |
| Editorial Pitch | `outputs/companies/{company_name}/{research_date}/editorial/01-editorial-pitch.md` | markdown（主命题、读者承诺、关键问题、张力与反证） |
| Editorial Master | `outputs/companies/{company_name}/{research_date}/editorial/02-editorial-master.md` | markdown（供 HTML 生成消费的企业研究母稿） |
| 冲突与编辑决策记录 | `outputs/companies/{company_name}/{research_date}/editorial/unresolved-conflicts.md` | markdown（已裁决 + 未裁决清单；未裁决不得进入 HTML） |
| Phase 2 执行记录 | `outputs/companies/{company_name}/{research_date}/editorial/phase2-execution.md` | markdown（资源、输入、输出与验收状态） |
| 最终 HTML | `outputs/companies/{company_name}/{research_date}/investment-report.html` | 单文件自包含（内联 CSS/SVG，无 CDN） |
| 全页截图 | 同目录 `preview.png` | PNG |

## Principles

- 本 Workflow 只负责研究 → 编辑综合 → HTML 生成 → QA 的项目顺序和产物交接；通用资源纪律由各 Required Resource 的资产记录负责。
- 本项目定位为企业研究内容，不是投资推荐；具体输出边界由 `boundary-rewrite` 与 `finance-content-engineering` 承接，Phase 级验收只检查本项目产物是否越界。
- `<aside class="notes">` 是本项目页面口播文本的唯一 Source of Truth；需要改变核心观点或新增视觉支撑时，回到 Presentation Agent 阶段同步更新。
- 不创建新 Agent 类型，不提前固定章节模板、Hook、Bull-Bear 格式或页面数量。

## Phase 1: research — 并行原生研究

### Goal

三个研究 Skill 按各自原生流程完整执行，产物原格式保留；每份产物附带结构化 findings-summary 作为下游衔接层。研究目标覆盖：公司业务与商业模式、行业与产业链、行业周期、市场地位、核心竞争优势/护城河、财务表现、经营变化、增长驱动、主要风险、长期跟踪变量。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| industry-analysis | skill | 必选 | github · tree-sha256:a2a363fca3d9 | 行业/产业链 6 阶段（产业链图谱/三高矩阵/标的映射）；产出原生 HTML 可视化报告；要求联网检索，估值需真实来源 |
| industry-cycle-analysis | skill | 必选 | github · tree-sha256:9e9b5dd25f8e | 供需周期/资本周期/市场预期阶段；产出深研 markdown + 证据台账；用 skill 自带验证器 strict full 校验 |
| investagent | skill | 必选 | github · tree-sha256:51aa7c2823bd | **内容生产链路只跑「研究+数据」范围**（见 Known Issues）：Buffett 定性 + UZI 22 维 + tushare 采集；跳过 TradingAgents/QuantDinger |

### Input

- 任务参数：company_id / company_name / research_date
- 研究目标清单（见 Goal）
- 环境说明：无用户确认场景下自主执行；tushare 凭证从 workspace 根 `.env` 自动加载

### Output

- `outputs/companies/{company_name}/{research_date}/investment-report/research-materials/industry-analysis/`：原生报告（HTML）+ findings-summary.md
- `outputs/companies/{company_name}/{research_date}/investment-report/research-materials/industry-cycle-analysis/`：原生报告（markdown）+ findings-summary.md
- `outputs/companies/{company_name}/{research_date}/investment-report/research-materials/investagent/`：原生报告 + UZI 产物 + 数据留档 + findings-summary.md
- `outputs/companies/{company_name}/official-information/`：公司级长期年报、中报、季报和公告原件存档，不带研究日期；同行公司使用同级目录
- 官方文件统一命名为 `{ts_code}_{period}_{document_type}_{announcement_date}.pdf`；执行前先检查本地文件和 `download_record.json`，命中且正文可验证时直接复用，不重复获取

- findings-summary 契约：①关键数据点→来源索引（机构/媒体具体名称）；②待验证/存疑数据单列（含口径矛盾标注）；③执行状态如实说明（真实执行 vs 降级 vs 排除）；④不含决策/回测结论；⑤不含具体目标价、买卖评级、操作区间——盈利一致预期（净利/EPS）作为市场预期允许保留

### Quality Criteria

- 每个 Required Resource 真实执行并留下独立产物，可逐项识别执行结果
- findings-summary 满足上述 4 项契约
- 数据来自真实接口/检索，无模型记忆补数；降级路径如实标注，未执行不得写成已执行
- 原生产物保留原生格式，未为 HTML 强行改造

### Known Issues

- **investagent 范围**：完整流水线约 40% 模块（TradingAgents 决策、QuantDinger 回测、买点/卖出清单）产出内容边界禁止内容——启动即限定「研究+数据」，不跑完再裁剪（经验: `investagent-research-only-scope`）。TradingAgents 本环境成功率低且产出对内容无价值。
- 执行预算（实测）：industry-analysis ≈ 8 分钟 / industry-cycle-analysis ≈ 18 分钟 / investagent ≈ 22 分钟（opus）。并行执行，用 `findings-summary.md` 作为衔接层。
- 环境问题：UZI 渲染需 playwright chromium（国内网络下载易超时，数据产物不受影响）；FRED 无 key 诚实降级；雪球端点需登录（腾讯/baostock 兜底）。
- 既有运行时经验：`investagent-module-runtime-issues`（QuantDinger 镜像降级、yfinance 映射、tushare 倒序）、`industry-research-methodology`（环境齐备才编排）。

## Phase 2: editorial-synthesis — Financial Editor Agent 编辑综合

### Goal

由 Financial Editor Agent 接管三份 Phase 1 findings-summary 的编辑综合，而不是只做数字冲突登记。Agent 必须先理解公司、行业与当前变化，再自主形成一个 Editorial Thesis，围绕该主命题决定哪些问题值得讲、哪些资料应删除或压缩，并完成事实核验、口径分层、冲突裁决、同行坐标、反证寻找与企业观点表达。

本 Phase 的交付目标是形成一份可以被 Human Editor 审阅、被 Presentation/HTML Agent 直接消费的 Human-first、Presentation-ready 企业研究母稿。它研究企业状态与经营逻辑，不输出投资观点、买卖建议、目标价或交易策略。无法验证或无法裁决的内容必须留在内部决策记录中，不得进入 Editorial Master 的事实正文。

默认顺序：

```text
三份 findings-summary
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
| financial-editor-agent | agent | 必选 | workspace · installed_ref 以 `phase2-execution.md` 记录 | 负责 Editorial Thesis、Editorial Pitch、Editorial Master、证据链、冲突裁决与企业研究边界；不输出证券交易建议 |

### Input

- Phase 1 三份 findings-summary.md（已验收）
- 必要时可回看 Phase 1 原生产物与其中引用的一手来源，专门用于核验关键冲突；不得把未核验的单源估计伪装成事实
- 任务参数：company_id / company_name / research_date

### Output

- `editorial/01-editorial-pitch.md`：
  - Working Title / Subtitle
  - Editorial Thesis
  - Why Now / Reader Promise
  - Key Questions / Key Tensions
  - Competitive Context
  - Major Evidence / Counter Evidence
- `editorial/02-editorial-master.md`：
  - Final Title / Final Subtitle
  - 以 Editorial Thesis 为中心、结构自由的完整企业研究内容
  - 可追溯的 Sources
  - Editorial Notes：Evidence Decisions / Conflict Decisions / Important Uncertainties
- `editorial/unresolved-conflicts.md`：
  - 已裁决清单：冲突项 / 各方口径 / 裁决结果 / 依据（含口径差异标注）
  - 未裁决清单：冲突项 / 无法裁决原因 / 对 Editorial Master 的排除处理
- `editorial/phase2-execution.md`：
  - financial-editor-agent 的 installed_ref、输入清单、输出清单、执行状态与验收结果

### Quality Criteria

- financial-editor-agent 真实执行并留下上述四份独立产物；`phase2-execution.md` 能按 by-name 识别资源与输入/输出
- Editorial Pitch 有且只有一个可复述的 Editorial Thesis，并明确 Why Now、Reader Promise、Key Questions、Key Tensions、Major Evidence、Counter Evidence
- Editorial Master 不是 findings-summary 的拼接：结构服从公司与问题，正文形成 Evidence Chain，并给出基于证据的企业判断
- 关键事实、数字、因果关系与同行比较均可追溯到来源；Fact / Estimate / Opinion / Inference 不混写
- 冲突项逐条记录，裁决有依据（算术自洽校验、一手来源优先、口径分层）；口径不同但均可靠时并列呈现并明确口径
- 未裁决项不得进入 Editorial Master 的事实正文；如仍需保留上下文，必须改为定性表述并在 Editorial Notes 标明不确定性
- Editorial Master 与所有内部记录均遵守企业研究边界：不得出现买卖建议、目标价、操作区间、仓位、交易策略或投资推荐式结论

### Known Issues

- 多源口径管理是固定成本（实测：裁决 12 项 + 未裁决 6 项，约 15 分钟）——不要压缩，数字可信度是研究内容底线（经验: `multi-source-conflict-check`）。
- Financial Editor Agent 的 Editorial Master 可能比原冲突清单更强地删减材料；删减是编辑判断，不代表 Phase 1 研究丢失，完整研究仍保留在原生产物中。
- Workflow 无 Human Editor 阻塞式确认点；如需人工复核，复核对象是 Editorial Pitch，而不是让 HTML Agent 自行重写 Thesis。
- 常见口径陷阱：营业总收入 vs 营业收入（差其他业务约 32 亿）；全年 vs 单期每股分红；个股 PE vs 指数 PE；A 股上市公司 vs 全国规上统计；机构目标价不同样本差异。
- **算术自洽校验是最强裁决工具**：Q2 单季 = H1 − Q1；分红率 × 净利 ÷ 股本 ≈ 每股分红。
- 无法裁决的处理：风险描述改定性表述，不呈现具体数字（如社会库存规模）。
- 脚本化：Phase 3/4 数值一致性检查用 `static-html-qa` 的 `check-numbers.py`，期望值清单取自本 Phase Editorial Master 与裁决结果。

## Phase 3: presentation-production — Finance Presentation Agent 生成 HyperFrames-native HTML

### Goal

由 finance-resentation-agent 接管 Phase 2 已验收内容的视觉转译，以 Editorial Master 和冲突/编辑决策记录为内容 Source of Truth，Phase 1 原生产物只用于回查来源，不得绕过 Financial Editor Agent 重新引入被删减或未裁决内容。

Agent 负责识别 Editorial Thesis 与 Narrative Arc，按 Scene First 原则重新拆解内容，并为每个 Scene 确定一个 Core Message、少量高解释力 Visual Evidence、Final Speaker Notes、Reveal Cues 与 HyperFrames Composition 结构。

**四资源职责分工模型（v0.4.0）**——内容决策、视觉语言、Composition 运行时和演示工程分层，各司其职：

| 层 | 资源 | 职责 |
|---|---|---|
| 内容导演层 | finance-resentation-agent | 讲哪些 Scene、每 Scene 的 Core Message、认知顺序、Visual Evidence 选择、是否拆页、Reveal Semantics、Notes |
| 视觉语言层 | impeccable | 视觉语言、版式、字体层级、图表美化、信息层级优化、设计系统、细节质感 |
| Composition 运行时层 | hyperframes | Composition contract、seek-safe 动画语义、确定性状态、视频渲染结构 |
| 演示工程层 | html-ppt-skill | HTML Deck、Presenter、Notes、Preview 外壳与工程实现 |

执行顺序与回环：**内容导演层先行**（Scene/Core Message/认知顺序/Reveal Semantics/Final Notes 定稿）→ **视觉语言层**（视觉方向、版式与设计系统，Read 模式克制侧）→ **Composition 与演示工程层**（同一套 DOM/SVG 接入 hyperframes，并由 html-ppt-skill 提供 Preview/Presenter 外壳）。视觉层、Composition 层与工程层发现内容层面问题（事实冲突、核心逻辑缺失、无法支撑视觉表达）时，记录 Content Issue 并返回导演层（即 finance-resentation-agent）；任何下游不得绕过或改写内容决策。impeccable 只做视觉与设计系统；hyperframes 负责确定性 Composition；html-ppt-skill 只做演示工程，均不替代 Agent 的内容选择和视觉导演责任。

每个 Scene 内部先确定薄三元组：**Core Message / Visual Evidence / Narration Expansion**，并定义至少一组阶段信息：**核心结论、主视觉、分阶段呈现步骤、每一步元素变化、Notes/Narration 对应步骤**。Visual 与 Speaker Notes 共同服务 Core Message，但不要求页面逐字复述口播。核心结论、关键数字、关键比较、趋势、因果和经营验证变量原则上必须有视觉锚点；背景、限定条件、过渡和深入解释可以只保留在 Notes。若重要口播无法被画面支持，应修改视觉、拆分 Scene 或弱化口播。HTML 从生成阶段即满足 HyperFrames Composition contract；Scene / Composition ID、Visual DOM/SVG、Final Notes、Reveal Cue 和 seek-safe Animation Semantics 在本阶段确定，真实时长留给后续 Timing Compile。

Presentation is selection, not transcription：每个 Scene 优先 1 个主证据，必要时 1–2 个辅助证据；不得把 Editorial Master、研究表格或 Evidence Notes 原样搬上页面。除非 Human Editor 明确要求，不生成复杂 Blueprint、Slide Spec 或大型 JSON Manifest。

Presentation Completeness Principle：压缩文字和次要证据，不压缩关键认知过程。Editorial Master 中理解 Thesis 所必需的背景、机制、比较、反证和意义，必须获得足够 Scene 空间；重要概念需要多少 Scene，就给多少 Scene。出现多个独立机制、多组重要比较、多个需分别解释的证据，或必须依赖大量卡片/表格才能容纳时，优先拆 Scene。

生成后自检：观众同时听 Speaker Notes、看当前 Slide，能否明确知道每个核心观点对应画面的什么内容？不能通过时不得进入后续 QA。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| finance-resentation-agent | agent | 必选 | workspace internal · Finance Presentation Agent v0.4 · sha256:22eb057b19ae867f8b44b02f6f8ba2cba0e3f9bb4dbb777a111ec2def590987b | 内容导演层：讲哪些 Scene、每 Scene 的 Core Message、认知顺序、Visual Evidence 选择、是否拆页、Reveal Semantics、Final Speaker Notes；从生成阶段确定 HyperFrames Composition 语义；不得修改 Editorial Master 的事实、Thesis、因果和边界 |
| impeccable | skill | 必选 | github · v4.1.1（npm 3.6.0）· f88b2837a7d7c3182e46307bbbb091a1ed547571 | 视觉语言层：视觉方向/版式/字体层级/图表美化/信息层级/设计系统/细节质感；init 生成 PRODUCT.md/DESIGN.md；audit（59 条确定性检测：a11y/对比度/间距，无 LLM）/ detect 作补充门禁；只取克制侧（Read 模式），不用 bolder/overdrive；hook 未安装（`--no-hooks`），纯命令调用；不驱动内容与设计决策 |
| hyperframes | skill | 必选 | github · c32b804 | Composition 运行时层：按当前 Composition contract 生成可 seek 的 DOM/SVG 状态、确定性动画与视频结构；真实 Scene/Cue 时间由后续 Audio Timing Compile 注入；使用前必须遵循当前安装版本的 Skill 指令 |
| html-ppt-skill | skill | 必选 | github · f3a8435d3901697d5ac5e64d356c933637e43107 | 工程实现层：HTML Deck（deck/slide 结构）、Presenter（S 键演讲者视图）、Notes（N 键抽屉）、Stage/runtime（键盘翻页/深链/概览/进度条，runtime.js 内联保持单文件自包含）；长文报告可取设计 token 体系（经验: `html-ppt-longform-report`） |
| static-html-qa | skill | 必选 | internal | 跨生成器质检三件套（内容边界/数值一致性/前端 QA），形态自适应（auto 检测翻页/长文）；所有 HTML 交付前必跑 |
| taste-skill | skill | 可选 | github · v2 experimental · dfb6f9f9e93a39f673b1827c0889cc28326d1800 | 视觉方向参考（editorial 页类 / 反模板纪律，与「结构服从信息」同向）；图表/数据密集页 Out of Scope；「有图像工具必先生成图」指令与单文件自包含约束冲突时以项目约束为准 |

### Input

- Phase 2 Editorial Master（已验收）
- Phase 2 Editorial Pitch（用于核对主命题与内容承诺）
- Phase 2 冲突与编辑决策记录（unresolved-conflicts.md）
- Phase 1 原生产物 + findings-summary（仅用于来源回查，不得绕过 Phase 2 重新取舍内容）

### Output

- `outputs/companies/{company_name}/{research_date}/investment-report.html`
  - HyperFrames-native 单文件 Composition：内联 CSS + 内联 SVG 图表，系统字体栈，无 CDN 依赖，本地可预览并可确定性渲染
- `outputs/companies/{company_name}/{research_date}/presentation-execution.md`
  - finance-resentation-agent by-name、installed_ref、输入/输出、Scene 数、Notes/Reveal 状态和验收结果
- `outputs/companies/{company_name}/{research_date}/expected-numbers.tsv`
  - 从 Editorial Master 与冲突裁决提取的 HTML 数值一致性期望清单
- 一屏一个核心观点；减少大段文字；卡片组织信息；趋势图/对比图表达数据
- 每页具备可执行的分阶段呈现结构；阶段可通过渐显、图表绘制、数字变化、对比高亮、结构切换或其他合适的动画实现，不规定统一动效
  - 无 AI 内部字段 / metadata / 置信度编号 / workflow 信息 / 未解决冲突 / 买卖建议
  - **每页 `<aside class="notes">` speaker script（150-300 字逐字稿）**：由 Presentation Agent 与 Scene Visual 同步产出，HTML 负责视觉压缩，script 可使用研究材料中页面未展示但与该页直接相关的证据/原因/背景（Presenter 模式 S 键可查看）；它是 Final Speaker Script 和 TTS 唯一文本 Source of Truth，后续视频 Workflow 不再重新润色或改写
  - **notes 口语化（朗读友好化）**：由 Presentation Agent 在本阶段完成——百分比直读（「营收负 1.2%」→「营收下降 1.2%」）、大数读法（中文数字/万亿单位）、单句 ≤25 字、书面语→口头语；**事实零漂移**：禁止近似化（「36.1%」不得写成「超过三分之一」）、不得新增/丢失数字（数字转中文读法与时间指代「去年/今年」允许）
  - **Content Lock（2026-08-16）**：口语化完成后 notes 即锁定为该页最终口播文本的唯一 Source of Truth（deck HTML 含 CONTENT LOCK 标记）；TTS 仅允许不改变语义和文字内容的技术性处理；字幕由 notes 派生，可断句但不另写文案

### Quality Criteria

- 内容正确：进入 HTML 的每个数值可追溯至 Phase 2 Editorial Master 与裁决记录
- **Agent 执行留痕**：finance-resentation-agent 真实执行并留下 HTML + `presentation-execution.md`；记录能识别 by-name 资源、输入、输出与验收状态
- **Scene First**：一个 Scene 只有一个主要 Core Message；章节不直接等同页面，拆分/合并均以观众新增认知为依据
- **Presentation Completeness Test**：理解 Thesis 所必需的背景、机制、比较、反证和意义均有足够 Scene 空间；不得为减少 Scene 数量跳过关键认知步骤
- **Cognitive Load Test**：一个 Scene 出现多个独立机制、多组重要比较或过量卡片/表格时必须拆分，不得继续压缩
- **Selection Test**：每个 Scene 只保留最有解释力的主证据和必要辅助证据，不转录 Editorial Master 或证据台账
- **数值一致性**：`static-html-qa/scripts/check-numbers.py <期望清单.tsv> <html>` PASS（期望清单由 Phase 2 裁决结果生成，round/exact/pct 三种模式）
- **内容边界**：`static-html-qa/scripts/check-content-boundary.py <html> --ignore <允许语境词>` PASS（资金流向事实等允许语境用 --ignore 声明；免责声明行自动豁免）。**页面不得出现任何具体目标价**（机构或自研），估值仅呈现 PE/PB/股息率/历史分位/不同增长假设下的 DCF 区间
- **无内部痕迹**：不出现「置信度/证据编号/证据台账/结论状态」类内部研究表述——用户只需要结论与依据，不需要 AI 内部过程
- **措辞克制**：避免「唯一/无懈可击/绝对/最优质」等绝对化、营销化措辞；「企稳确认/压力信号」类基本面验证信号保留，但不得写成「出现信号即买卖」
- 结构自然：行业 → 周期 → 公司的三层叙事为推荐起点（随信息自由调整），无固定模板强制
- A 股财务页面红涨绿跌（`--up: 红 / --down: 绿`）
- **Speaker Script 与 Slide Visual 语义一致原则**：同一次内容规划产出，script 可含页面未展示的相关证据/背景，但不得新增研究事实（仍受内容边界约束：无目标价/买卖建议）；Presentation Agent 完成 Oral Adaptation 后即锁定，若需改变核心观点或增加关键视觉支撑，必须回到该 Agent 同步更新 Scene
- **Core Message 对齐门禁**：口播与页面要求认知一致而非文字一致；重要口播必须有可定位的视觉锚点，不要求逐字上屏，页面不得变成字幕墙
- **分阶段呈现门禁**：每页必须能说明“先呈现什么、再呈现什么、元素如何变化、此时旁白讲什么”；未建立 narration-to-stage 映射的页面不得通过
- **Reveal 语义门禁**：Reveal/Stage 只展开同一个认知模型，不是减少 Scene 数量的工具；Phase 3 不硬编码真实音频秒数，真实时间由 TTS/Alignment 决定
- **HyperFrames Composition 门禁**：Scene / Composition / Cue ID 唯一稳定；Preview、Presenter 与 Video 共用同一套 Scene DOM/SVG；seek 到任意时间状态可复现，不依赖 wall-clock、随机数、无限动画或截图后模拟 Reveal；按当前安装版本完成 HyperFrames check 与必要的 snapshot/render

### Known Issues

- SVG 图表坐标换算是耗时最重、最易错环节——手工完成后必须跑数值一致性检查，禁止跳过（经验: `multi-source-conflict-check`）。
- 红涨绿跌是设计红线；skill 默认蓝涨绿跌为美股惯例，必须显式覆盖（经验: `html-ppt-longform-report`）。
- 不展示未解决冲突（U 编号项）；机构目标价等市场预期需标注「市场预期/样本差异」语境。
- 参考：本流程 HTML 生成前，先通读三份 findings-summary 提炼「核心矛盾」作为 Hero 与各部分结论横幅。
- Finance Presentation Agent 发现事实冲突、核心逻辑缺失或无法支撑视觉表达时，应记录 Content Issue 并返回 Phase 2；不得自行重做研究或提高结论强度。
- **同名类污染（2026-08-19 实测）**：长文版结论横幅 `.deck` 与翻页容器 `.deck` 类名冲突——横幅规则的 `max-width:46em`/`border-top`/`font-size` 会同时匹配容器，把容器宽度压至 46em（883px@1.2rem）并破坏 slide 全屏布局。三资源协作时类名必须全局唯一（横幅用 `.callout`，容器保留 `.deck`）；QA 的「slide 宽不足全屏」是这类污染的典型信号。
- **动画位移污染 QA 测量（2026-08-19 实测）**：stage reveal 用 `translateY` 时，动画未完成（qa 截图后 ~400ms 即检测）的 rect 处于偏移位 → 出界/溢出误报。stage 动画一律用 opacity + clip-path（不动滚动尺寸与 rect），并保留 capture-mode（headless 检测）与 reduced-motion 全显回退。
- **runtime 保留类名冲突（2026-08-19 实测）**：html-ppt-skill runtime 的 counter-up 特性会劫持 `class="counter"` 元素（文本被替换为 NaN）——自定义组件类名避开 `.counter`（如 `.counter-card`）。
- **矮视口（16:10 桌面）溢出（2026-08-19 实测）**：翻页 deck 以 16:9 视频帧（1920x1080）为设计目标；1440x900 等 16:10 视口下内容可能垂直溢出——用 `@media(max-height:940px)` 压缩 padding/标题/图表宽度，不动 16:9 设计。
- **impeccable detect 字号阈值（2026-08-19 实测）**：tiny-text 阈值 ≥11px（预防起点 12px）——移动端降级字号不得低于 12px（`.page-kicker`/`.footnote` 等）。
- **notes 交互方式（翻页 deck）**：notes 不再页面内显示（N 键抽屉 / S 键演讲者视图承载）；逐字稿内容不变，QA 断言需适配。

## Phase 4: qa — 截图与最终检查

### Goal

打开检查最终 HTML（人工/截图），确认渲染正常、图表可读、无边界违规。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| static-html-qa | skill | 必选 | internal | `qa-html-report.py`（形态自适应：翻页 deck 逐页检查/长文 fullPage；自动探测 .venv playwright）+ `check-content-boundary.py` + `check-numbers.py` + `screenshot-fullpage.sh` |
| impeccable | skill | 可选 | github · v4.1.1（npm 3.6.0）· f88b2837a7d7c3182e46307bbbb091a1ed547571 | `audit` 确定性设计检测作补充门禁（a11y/对比度/间距节奏维度，与 static-html-qa 的溢出/SVG/数值维度互补）；发现项人工裁决，不阻塞 PASS 流程 |

### Input

- Phase 3 最终 HTML（已验收）

### Output

- 同目录 `preview.png`（全页截图，默认宽 1440px）
- `qa-html-report.py` 输出：桌面/移动/视频分辨率三张截图 + `qa-report.json`（发现明细）

### Quality Criteria

- **前端质检**：`python3 static-html-qa/scripts/qa-html-report.py <html>` 返回 PASS（0，`--mode auto` 自动识别翻页/长文），覆盖：多视口截图（默认 1440x900 桌面 / 390x844 移动 / 1920x1080 视频）、DOM/卡片溢出、SVG 文字重叠与出界、图例重叠、字体加载失败、console error、responsive 断点、图表文字过小（默认阈值 9px）、页面横向截断
- 发现项须修复后重跑至 PASS（SVG 坐标类问题由 qa 脚本兜底发现，禁止跳检）
- Phase 3 内容边界（check-content-boundary）与数值一致性（check-numbers）检查记录在案（PASS）
- 人工抽查移动端截图（响应式折叠）与视频分辨率截图

### Known Issues

- qa-html-report.py 需 Python playwright：自动探测工作区 `.venv`（`$QA_PYTHON` 可显式指定）；npm 全局 `@playwright/cli` 是 JS 包，不能用于 Python 导入；翻页 deck 的 `.mini-slide` 克隆（overview）与 dashi 克隆页不影响激活页检查
- 截图仅验证渲染，不替代数值一致性与内容边界检查（三脚本需全部执行）
