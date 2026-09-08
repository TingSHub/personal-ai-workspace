# Workflow: topic-forward-lead

> 位置: Project: projects/video-publish-review/workflows/topic-forward-lead/

## Mission

作为新视频的唯一选题入口：从重大事件、产业变化、公司实力与产品、观众问题、已有研究及可选行情信号中发现值得研究的问题，先按内容主线和内容深度拆成互斥的观众任务，再生成至少 10 张轻量核验的 topic card，并取得一次真实用户批准。批准卡决定“研究什么、以哪条内容主线研究、需要达到什么解释深度”，不预设研究结论或逐句视频结构。

## Input

近期事件与原文、产业/技术变化、公司产品与经营线索、观众评论或直接问题、已有研究发现、已发布作品去重基线、`publish-review` 的条件化改进候选与 `account-rules.md`。行情与热点数据是可选发现源，不能替代事实核验。内容主线由 `topic-angle-router-agent` 按 `market_pulse`、`earnings_gap`、`company_industry`、`valuation_mechanism` 四种任务执行。

候选字段只从 `topic-forward-candidate.json.template` 读取；项目脚本 `build-topic-candidates.py` 负责把可选 signals 与有来源 leads 归一成 discovery seeds；`topic-angle-router-agent` 负责在候选池阶段补齐内容主线与表达 Agent 映射。

## Output

`outputs/topic-forward/{date}/` 下：

- `signals.json`：可选行情及抓取缺口；
- `candidate-pool.json`：可追溯 discovery seeds；
- `topic-angle-matrix.json`：每条 seed 可支持的内容主线、淘汰主线与路由理由；
- `topic-forward.json`：默认至少 10 张结构化 topic card、批准状态和批准卡；
- `topic-forward.md`：人类阅读视图；
- `topic-forward-execution.md`：实际资源、installed_ref、来源与降级记录。

Phase 4 在交付前运行项目脚本 `check-topic-angle-routing.py`，确保每张卡的 `content_line`、`expression_agent` 和 `expression_mode` 映射一致。

用户批准后，选中的结构化 topic card 原样交给 `topic-research`。视频生产不直接读取复盘 attribution、候选池或未批准卡。

## Principles

- 流量优先但不牺牲事实：每张卡都回答为什么点开、看完得到什么、为什么愿意讨论/收藏、为什么值得继续关注。
- `content_line` 是一级字段，必须在标题定稿前锁定；标题是内容主线锁定后的包装，不得用标题倒推主问题。
- `content_depth` 是研究复杂度和观众学习承诺，不是单纯时长字段：`standard` 适合单一机制的最小充分解释，`deep_explainer` 适合明确要求历史、新闻、产业链、市场预期或多阶段因果的题目。
- 四条主线分别服务行情陪伴、财报预期差、公司/产业链、生意/估值机制教学；一条视频只选择一条主线。
- 同一主体可以生成多张候选卡，但必须改变观众问题、证据需求和观看承诺，不能只换标题。
- 选题卡锁定问题，不锁定答案。它可以提出有争议的假设和核心张力，但最终主张由研究和内容导演决定。
- 来源并行：事件、产业、产品实力、观众问题和已有研究与行情同级；没有行情或复盘不阻断选题。
- 轻量核验只确认主体、事件、时效、问题价值和可研究性，不在本 Workflow 做完整研究。
- 复盘只提供有适用条件的假设，不决定排序。每张卡最多携带一个主要内容实验，也可以不采用。
- 每轮默认至少输出 10 张候选卡，给用户足够选择空间；公司、行业、新闻、比较是覆盖视角，不是固定配额。
- 10 张是候选数量下限，不是四条主线的机械配额；应优先扩大来源、拆分不同观众任务和补充可研究问题，不能用同一问题只换标题凑数。若经过来源扩展仍不足 10 张，必须在执行记录中列明缺口与未入卡 seeds，不得伪造证据。
- 候选池追求主线覆盖，不设机械四等分配额；当本轮证据只支持某些主线时，少生成也不凑数。
- 相同主体出现新问题、新证据或新阶段可以再讲，但必须说明新增观看价值。
- 禁止直接荐股、目标价、交易指令和收益保证；允许提出待研究的多空、竞争力、估值与产业受益假设。
- Required Resources 必须真实执行并留下独立产物；下游只消费已验收结果。
- by-name 引用：Workflow / Skill / Agent / Experience 一律用名称，不用相对路径。

## Phase 1: lead-discovery — 多来源问题发现

### Goal

并行发现近期有关注度、认知差或长期价值的问题，并保留来源、日期和待核验状态。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| `multi-search` | skill | 必选 | workspace installed_ref | 先通过 workspace `.env` 注入入口调用，默认 Tavily-first；失败再降级到当前会话原生 Web 搜索，摘要不能直接作事实 |
| `topic-forward-signal-scanner` | skill | 可选 | workspace internal v0.1 | 免费行情发现；接口失败只降级该来源 |
| `news-search` | skill | 可选/降级 | workspace installed_ref | `multi-search` 与原生 Web 均不可用时走 Iwencai API；也可用浏览器聚合新闻；必须回原文核验 |
| `social-trend-monitor` | skill | 可选 | workspace installed_ref | 海外科技与产业风向；需验证本地相关性 |

### Input

用户问题、评论、公开事件、产业与产品资料、已有研究、近期开启的市场/热点信号，以及用于判断 `content_depth` 的解释需求线索。

### Output

`outputs/topic-forward/{date}/signals.json`、来源摘要、各资源执行记录和 `candidate-pool.json` 初稿。

### Quality Criteria

- 来源记录事件日、发布日期、主体、原文与待核验点；搜索摘要不进入事实表述。
- 行情记录采集日与实际交易日；涨跌只说明关注线索，不自动生成公司实力或财务结论。
- 观众问题可以证明需求，但不能证明公司事实；两类证据必须分开。
- 无有效线索时宁可少卡，不用旧新闻或空泛公司名补数量。

### Known Issues

免费行情接口可能断连；失败时保留 errors 并继续事件、产业、产品和观众来源。搜索路由按“本地 `multi-search`（默认 Tavily-first）→ 当前会话原生 Web → Iwencai API（`news-search`）”降级；每一层失败都保留错误，只有全部不可用才记录网络阻断。

## Phase 2: candidate-pool — 问题化与去重

### Goal

把原始线索转成不同内容主线和观众问题的候选池，剔除只是换公司名、只换标题或没有新增认知价值的重复题。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| `finance-content-engineering` | skill | 必选 | workspace installed_ref | 将研究/线索转成互斥内容角度；不代替事实核验 |
| `topic-angle-router-agent` | agent | 必选 | internal v0.1 | 把同一线索拆成内容主线候选，并绑定后续表达 Agent；不代替完整研究或审批 |

### Input

Phase 1 已验收来源、`published-works.md`、历史复盘册和账号内容范围。

### Output

更新后的 `candidate-pool.json`、`topic-angle-matrix.json`，记录主体、`content_line`、对应 `expression_agent`、核心问题、来源、时效、新增价值、去重结果和仍需研究的事项。

### Quality Criteria

- 每个候选都挂来源，并形成一个可验证、与受众有关的问题。
- 每个候选必须有且只有一个 `content_line`，并绑定匹配的 `expression_agent` 与 `expression_mode`；原始 seed 可以暂时为空，但进入 topic card 前不得为空。
- 每个候选必须判断 `content_depth`；若观众问题包含“为什么形成/历史上如何/这次和以前有什么不同/股价与基本面为何错位”等学习需求，默认路由为 `deep_explainer`，不能用 `standard` 的短结构承接。
- 同一主体的不同主线候选必须提供不同观看理由，例如“利润与预期落差”不能和“公司如何赚钱”只换标题。
- 公司题说明讲实力、商业化、经营质量还是事件影响；行业题说明利润、瓶颈、供需或竞争格局；比较题先声明共同问题和可比边界。
- 与历史作品按主体 + 核心问题 + 关键证据去重；同主体的新问题必须写清新增价值。
- 不因账号过去偏财报而强迫新题使用财务兑现主线。
- 不把“公司/行业”这种对象类型误当成内容主线；公司题也可以是行情、财报、产业链或估值题。

### Known Issues

行情天然偏短线；候选是否值得做，取决于问题张力、观众价值和可获得证据，而不是单日涨幅。

## Phase 3: lightweight-verification — 轻量核验与排序

### Goal

确认候选前提真实、问题可研究，并按增长潜力、独特洞察和证据基础排序。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| `multi-search` | skill | 必选 | workspace installed_ref | 默认 Tavily-first 打开原文；本地适配器失败时转当前会话原生 Web，核验主体、日期与关键前提 |
| `boundary-rewrite` | skill | 必选 | workspace installed_ref | 保留张力，移除直接交易引导 |

### Input

Phase 2 候选池、`account-rules.md` 和历史作品去重基线。

### Output

通过核验的排序候选、选择理由、原文引用、研究缺口、主线适配和复盘适用性，写入 `topic-forward.md` 与执行记录。

### Quality Criteria

- 排序逐项说明点击理由、时效/长期价值、独特发现、证据基础和可制作性；不使用未经验证的固定权重。
- 排序先在同一 `content_line` 内比较，再做跨主线比较；不能因为行情信号强就自动压过高价值的机制教学题。
- 核心张力可以有争议，但必须是可由研究支持或推翻的假设，不能把结论写死。
- 无复盘规则命中不降权；每卡最多一个适用内容实验，发布时段等运营实验留给发布环节。
- 前提未核验或证据不可获得的候选留在 pool，不进入可批准卡。

### Known Issues

早期账号规律样本少，复盘更多是实验假设，不是跨题材通用规律。

## Phase 4: topic-card — 增长与研究契约

### Goal

按模板生成至少 10 张可比较、可批准、可直接进入研究的结构化卡片。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| `boundary-rewrite` | skill | 必选 | workspace installed_ref | 卡片表述合规且保留讨论空间 |

### Input

Phase 3 已验收候选与适用的复盘假设。

### Output

`topic-forward.json` 和 `topic-forward.md` 中默认不少于 10 张 topic card；字段唯一来源为 `topic-forward-candidate.json.template`。

### Quality Criteria

- 每卡明确研究对象与范围、观众问题、核心张力、证据起点、待研究事项和叙事方向。
- 每卡明确 `content_line`、`expression_agent` 和 `expression_mode`；三者必须匹配，并原样移交下游研究与表达层。
- 每卡明确 `content_depth`，并在 `research_required` 里列出深度模式所需的历史、当前新闻或市场关系证据；该字段必须原样移交下游。
- 每卡明确点击理由、内容承诺、互动价值和关注理由；四者围绕同一受众问题，正文可兑现。
- 每轮至少 10 张卡；同一主体可以跨主线出现，但必须改变观众问题、证据需求和观看承诺，并在 `topic-angle-matrix.json` 中说明差异。
- 封面方向只给研究对象和大字冲突，不把未研究假设写成已证实结论。
- `narrative_direction` 是方向而非章节模板；财报、行业、事件、技术与公司案例均可成为主线。
- 标题必须从已锁定的观众问题和核心冲突生成；至少提供一个事实型标题和一个问题/反差型标题，不能只输出公司名加报告类型。
- 卡片说明复盘候选是否适用、原因、实现和观察指标；没有适用项时可以为空。
- 表述不含买卖建议、目标价、点位预测或收益保证。

### Known Issues

topic card 是研究问题与增长假设，不是研究报告。证据不足或反证成立时，`topic-research` 可以返回 scope change。

## Phase 5: approve-and-handoff — 一次批准与研究移交

### Goal

取得用户对研究对象与主问题的一次真实确认，并把批准卡原样交给 `topic-research`。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| `finance-content-engineering` | skill | 可选 | workspace installed_ref | 仅在用户要求改写卡片问题时调用；不重建候选池 |

### Input

Phase 4 topic cards 与用户选择/备注。

### Output

`topic-forward.json` 中的 approved status、approved topic id、批准日期与用户备注；选中卡写为 approved，并连同来源与执行记录移交 `topic-research`。

### Quality Criteria

- 批准必须来自用户，不用 Agent 推荐或历史选择代替。
- 用户批准的是“研究对象 + content_line + 核心问题”；后续标题、章节和逐句表达可以在同一主线内优化，但不能静默换成另一条主线。
- 研究和生产复用该批准，不重复询问同一主问题。
- 研究若推翻前提，或必须改变主体/主问题，标记 `scope_change_required` 并返回本 Phase；标题、措辞、章节和叙事模式变化不需要重新批准。
- 未批准卡不得进入研究或视频生产。

### Known Issues

用户全否时记录原因并返回候选池；不要为了推进流程自动选择排名第一的卡。
