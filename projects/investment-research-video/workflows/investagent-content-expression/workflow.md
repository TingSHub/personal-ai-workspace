# Workflow: investagent-content-expression

> 位置: Project: projects/investment-research-video/workflows/investagent-content-expression/

## Mission

把已验收的事实研究包变成有明确判断、自然双人播客表达和增长承诺的锁定内容包。只做编辑判断与表达编排，不补研究、不执行音频或视觉制作。

## Input

- `topic-research` 已验收的 `research-brief.md`、`source-ledger.md`、evidence map 和 `research-quality-gate.md`；
- 用户批准的 topic card，且必须包含 `content_line`、`expression_agent` 和 `expression_mode`；
- `account-profile`、内容政策、对白政策、目标平台和目标时长。

## Output

运行目录为 `outputs/subjects/{subject_id}/{run_date}/`：

- `editorial/director-treatment.md`
- `editorial/expression-lane-treatment.md`
- `editorial/humor-map.md`
- `editorial/topic-order.json`
- `editorial/opening-selection.json`
- `editorial/scene-intent.json`（只记录内容意图，不制作 chart）
- `editorial/feedback-constraints.md`
- `editorial/episode-input.json`
- `editorial/director-execution.md`
- `editorial/phase1-execution.md`
- `podcast/script/episode.json`
- `podcast/script/dialogue-map.json`
- `podcast/script/spoken-style-map.json`
- `podcast/script/spoken-polish-diff.json`
- `podcast/script/dialogue-director-execution.md`

## Principles

- 研究包是本 Workflow 的事实唯一来源；不重新搜索、不补数字、不改变 evidence ID。
- `content_line` 是表达层的路由契约：`market_pulse`、`earnings_gap`、`company_industry`、`valuation_mechanism` 只能选择一个；不能在导演阶段把财报题静默改成行情题，或把公司题改成估值题。
- 先锁定内容判断，再编排对白；不能先写漂亮对白再反推主张。
- 默认真实 `host_analyst`：主理人提出观众问题并承接，分析师先回答再给证据和限制；`debate` 只有显式指定时启用。
- 听觉理解、对话连续性、概念命名意识、幽默、节奏和 AI 腔清理统一由 `finance-content-engineering` 处理；真实 speaker、turn、reply 和共同注意关系由 `dialogue-director-agent` 处理。
- 内容清晰优先于表达花样；任何表达改动都不得改变事实、数字口径、判断强度和边界。

## Stage Boundary

```text
research-brief + evidence IDs
        ↓
editorial-lock：决定讲什么、为什么讲、观众最终记住什么
        ↓ 通过后才可写逐句对白
dialogue-lock：决定两个人怎么问、怎么答、怎么让观众听懂并愿意继续听
        ↓ 锁定后不得在执行层改写
audio / visual / render
```

`editorial-lock` 的失败是内容问题；`dialogue-lock` 的失败是表达/对白问题；两者都不能由执行层补救。

## Phase 1: editorial-lock — 导演与内容锁定

### Goal

从冻结研究包中选择唯一核心主张、叙事模式、开场、模块顺序、增长承诺和结尾条件。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| `editorial-director-agent` | agent | 必选 | internal v0.3 | 选择主张、叙事、开场、模块和结尾；不补研究 |
| `market-companion-editor-agent` | agent | 条件必选 | internal v0.1 | 仅 `content_line=market_pulse` 执行；提供行情陪伴主线的 viewer contract、证据顺序和观察变量 |
| `earnings-gap-translator-agent` | agent | 条件必选 | internal v0.1 | 仅 `content_line=earnings_gap` 执行；提供财报预期差主线的经营与预期落差结构 |
| `company-industry-explainer-agent` | agent | 条件必选 | internal v0.1 | 仅 `content_line=company_industry` 执行；提供价值链、商业化和兑现条件结构 |
| `valuation-mechanism-teacher-agent` | agent | 条件必选 | internal v0.1 | 仅 `content_line=valuation_mechanism` 执行；提供单一机制、案例和失效条件结构 |
| `finance-humor-writing` | skill | 必选 | workspace internal | 将已选主线转成中小投资者可理解的财经幽默表达；不得改变事实和判断强度 |

### Input

批准 topic card、已验收 research brief/source ledger/evidence map、account profile、目标平台和时长。

### Output

导演方案、topic order、opening selection、scene intent、episode input、director execution 和 `editorial-lock` 回执。

### Quality Criteria

- `editorial_thesis` 明确回答批准问题，包含机制、时间范围、受影响环节、最强反证、推翻条件和 evidence IDs；
- 只有一个核心判断；每个模块有不同问题、证据推进和 audience payoff；
- 开场在前 10 秒交付观看价值，结尾说出当前判断而不是把答案推给未来；
- `episode-input.json` 完全引用研究包，不产生新事实；
- 只执行与 `content_line` 匹配的一个主线 Agent，并在 `director-execution.md` 记录路由结果；其他三个不应并行生成相互竞争的主张。
- 主线 Agent 的 viewer contract、主张结构和兑现条件进入导演方案；`finance-humor-writing` 只负责表达层增味，不重新决定主线。
- `check_editorial_gate.py` 通过后才进入 Phase 2。
- `editorial-lock` 回执必须列出：采用的核心主张、放弃的候选讲法、每个模块的观众认知收益、证据 IDs 和结尾判断；不能只写“导演方案已完成”。

### Known Issues

本阶段不做逐句口语化，不做双人 turn，不制作图表；发现证据不足时退回 `topic-research`。

## Phase 2: dialogue-lock — 双人对白与表达锁定

### Goal

把已锁定的主张和模块编排成真实 `host_analyst` 双人播客逐句稿，并完成统一财经表达工程。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| `dialogue-director-agent` | agent | 必选 | internal installed_ref | 真实 speaker、Conversation State、reply、interaction、emotion 和 delivery |
| `finance-content-engineering` | skill | 必选 | workspace installed_ref | 听觉理解、口语、概念命名意识、适度趣味和事实零漂移 |
| `finance-humor-writing` | skill | 必选 | workspace internal | 按 `content_line` 选择财经幽默模式，输出 humor map 和 fact preservation check |
| `boundary-rewrite` | skill | 可选 | workspace installed_ref | 只在表达边界扫描发现争议措辞时启用 |
| `debate-rounds` | skill | 可选 | workspace installed_ref | 仅 `format_mode=debate` 时启用 |

### Input

通过 Phase 1 验收的 episode input、director treatment、topic order、研究包和 account profile。

### Output

锁定 `episode.json`、dialogue map、spoken style map、spoken polish diff 和 dialogue director execution。

### Quality Criteria

- 每个 turn 明确 speaker、reply_to_turn_id、interaction_type、emotion、delivery、evidence_ids 和 text；
- 每个话题有共同问题、直接回答、真实反应/追问和自然落点；动作按认知需要选择，不为满足固定数量制造废话；
- 每个话题都能指出上一句触发了什么反应或推进，回合长短和回应方式不能机械重复；
- 术语先解释再使用，必要概念不被幽默遮盖；
- 口播使用与 `content_line` 匹配的 `expression_mode`；幽默点必须能回指事实或观众情绪，并在笑点后回到判断、观察变量或验证窗口；
- 概念命名只有在能降低记忆负担时才使用，可以输出“不命名”；
- `host_analyst` 不被误写成双方等量辩论；
- `check_podcast_dialogue.py` 通过后，文本、speaker、数字和 evidence IDs 冻结。
- `dialogue-director-execution.md` 必须记录 `finance-content-engineering` 的统一表达执行，以及每个表达改动如何保持事实零漂移；不得再要求或伪造已下沉的旧表达资源回执。

### Known Issues

如果删除 speaker 姓名后仍像两篇单口稿，必须重写对白；如果需要新事实，退回 `topic-research`，不能由对白导演补写。

## Handoff

只有 `editorial-lock` 和 `dialogue-lock` 都通过，才移交 `investagent-video-execution`。执行层不得消费 draft，只消费锁定的 `episode.json` 和交接回执。
