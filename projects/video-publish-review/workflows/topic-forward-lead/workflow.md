# Workflow: topic-forward-lead

> 位置: Project: projects/video-publish-review/workflows/topic-forward-lead/

## Mission

作为新视频的唯一选题入口：从重大事件、产业变化、公司实力与产品、观众问题、已有研究及可选行情信号中发现值得研究的问题，生成 3–5 张轻量核验的 topic card，并取得一次真实用户批准。批准卡只决定“研究什么”，不预设研究结论或视频结构。

## Input

近期事件与原文、产业/技术变化、公司产品与经营线索、观众评论或直接问题、已有研究发现、已发布作品去重基线、`publish-review` 的条件化改进候选与 `account-rules.md`。行情与热点数据是可选发现源，不能替代事实核验。

候选字段只从 `topic-forward-candidate.json.template` 读取；项目脚本 `build-topic-candidates.py` 负责把可选 signals 与有来源 leads 归一成 discovery seeds。

## Output

`outputs/topic-forward/{date}/` 下：

- `signals.json`：可选行情及抓取缺口；
- `candidate-pool.json`：可追溯 discovery seeds；
- `topic-forward.json`：3–5 张结构化 topic card、批准状态和批准卡；
- `topic-forward.md`：人类阅读视图；
- `topic-forward-execution.md`：实际资源、installed_ref、来源与降级记录。

用户批准后，选中的结构化 topic card 原样交给 `topic-research`。视频生产不直接读取复盘 attribution、候选池或未批准卡。

## Principles

- 流量优先但不牺牲事实：每张卡都回答为什么点开、看完得到什么、为什么愿意讨论/收藏、为什么值得继续关注。
- 选题卡锁定问题，不锁定答案。它可以提出有争议的假设和核心张力，但最终主张由研究和内容导演决定。
- 来源并行：事件、产业、产品实力、观众问题和已有研究与行情同级；没有行情或复盘不阻断选题。
- 轻量核验只确认主体、事件、时效、问题价值和可研究性，不在本 Workflow 做完整研究。
- 复盘只提供有适用条件的假设，不决定排序。每张卡最多携带一个主要内容实验，也可以不采用。
- 候选数量与类型由有效线索决定；公司、行业、新闻、比较是覆盖视角，不是固定配额。
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
| `multi-search` | skill | 必选 | workspace installed_ref | 发现并打开关键原文；摘要不能直接作事实 |
| `topic-forward-signal-scanner` | skill | 可选 | workspace internal v0.1 | 免费行情发现；接口失败只降级该来源 |
| `news-search` | skill | 可选 | workspace installed_ref | 新闻热度聚合；必须回原文核验 |
| `social-trend-monitor` | skill | 可选 | workspace installed_ref | 海外科技与产业风向；需验证本地相关性 |

### Input

用户问题、评论、公开事件、产业与产品资料、已有研究、近期开启的市场/热点信号。

### Output

`outputs/topic-forward/{date}/signals.json`、来源摘要、各资源执行记录和 `candidate-pool.json` 初稿。

### Quality Criteria

- 来源记录事件日、发布日期、主体、原文与待核验点；搜索摘要不进入事实表述。
- 行情记录采集日与实际交易日；涨跌只说明关注线索，不自动生成公司实力或财务结论。
- 观众问题可以证明需求，但不能证明公司事实；两类证据必须分开。
- 无有效线索时宁可少卡，不用旧新闻或空泛公司名补数量。

### Known Issues

免费行情接口可能断连；失败时保留 errors 并继续事件、产业、产品和观众来源。

## Phase 2: candidate-pool — 问题化与去重

### Goal

把原始线索转成不同观众问题的候选池，剔除只是换公司名、没有新增认知价值的重复题。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| `finance-content-engineering` | skill | 必选 | workspace installed_ref | 将研究/线索转成互斥内容角度；不代替事实核验 |

### Input

Phase 1 已验收来源、`published-works.md`、历史复盘册和账号内容范围。

### Output

更新后的 `candidate-pool.json`，记录主体、核心问题、来源、时效、新增价值、去重结果和仍需研究的事项。

### Quality Criteria

- 每个候选都挂来源，并形成一个可验证、与受众有关的问题。
- 公司题说明讲实力、商业化、经营质量还是事件影响；行业题说明利润、瓶颈、供需或竞争格局；比较题先声明共同问题和可比边界。
- 与历史作品按主体 + 核心问题 + 关键证据去重；同主体的新问题必须写清新增价值。
- 不因账号过去偏财报而强迫新题使用财务兑现主线。

### Known Issues

行情天然偏短线；候选是否值得做，取决于问题张力、观众价值和可获得证据，而不是单日涨幅。

## Phase 3: lightweight-verification — 轻量核验与排序

### Goal

确认候选前提真实、问题可研究，并按增长潜力、独特洞察和证据基础排序。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| `multi-search` | skill | 必选 | workspace installed_ref | 打开原文，核验主体、日期与关键前提 |
| `boundary-rewrite` | skill | 必选 | workspace installed_ref | 保留张力，移除直接交易引导 |

### Input

Phase 2 候选池、`account-rules.md` 和历史作品去重基线。

### Output

通过核验的排序候选、选择理由、原文引用、研究缺口和复盘适用性，写入 `topic-forward.md` 与执行记录。

### Quality Criteria

- 排序逐项说明点击理由、时效/长期价值、独特发现、证据基础和可制作性；不使用未经验证的固定权重。
- 核心张力可以有争议，但必须是可由研究支持或推翻的假设，不能把结论写死。
- 无复盘规则命中不降权；每卡最多一个适用内容实验，发布时段等运营实验留给发布环节。
- 前提未核验或证据不可获得的候选留在 pool，不进入可批准卡。

### Known Issues

早期账号规律样本少，复盘更多是实验假设，不是跨题材通用规律。

## Phase 4: topic-card — 增长与研究契约

### Goal

按模板生成 3–5 张可比较、可批准、可直接进入研究的结构化卡片。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| `boundary-rewrite` | skill | 必选 | workspace installed_ref | 卡片表述合规且保留讨论空间 |

### Input

Phase 3 已验收候选与适用的复盘假设。

### Output

`topic-forward.json` 和 `topic-forward.md` 中的 3–5 张 topic card；字段唯一来源为 `topic-forward-candidate.json.template`。

### Quality Criteria

- 每卡明确研究对象与范围、观众问题、核心张力、证据起点、待研究事项和叙事方向。
- 每卡明确点击理由、内容承诺、互动价值和关注理由；四者围绕同一受众问题，正文可兑现。
- 封面方向只给研究对象和大字冲突，不把未研究假设写成已证实结论。
- `narrative_direction` 是方向而非章节模板；财报、行业、事件、技术与公司案例均可成为主线。
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
- 研究和生产复用该批准，不重复询问同一主问题。
- 研究若推翻前提，或必须改变主体/主问题，标记 `scope_change_required` 并返回本 Phase；标题、措辞、章节和叙事模式变化不需要重新批准。
- 未批准卡不得进入研究或视频生产。

### Known Issues

用户全否时记录原因并返回候选池；不要为了推进流程自动选择排名第一的卡。
