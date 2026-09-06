# Workflow: investagent-podcast-video-by-hyperframes

> 位置: Project: projects/investment-research-video/workflows/investagent-podcast-video-by-hyperframes/

## Mission

作为项目级总路由，按“事实层 → 表达层 → 执行层”串联财经视频生产链。父 Workflow 只负责子 Workflow 的顺序、输入输出交接和退回条件，不在这里重复研究、写对白或执行媒体制作。

## Input

- 用户批准的 `topic-forward-lead` topic card；
- 研究日期、账号 profile、目标平台和制作参数；
- 可用来源与访问边界。

## Output

从 `outputs/research/{subject_id}/{research_date}/` 到 `outputs/subjects/{subject_id}/{run_date}/` 的完整交付链：冻结研究包、锁定表达包、音频、字幕、Composition、成片 QA 和发布回执。

## Principles

- `topic-research` 是事实层必经 Workflow；没有 `Scope Decision: accepted` 的研究包不能进入表达层。
- 表达层只消费冻结的 `research-brief.md`、`source-ledger.md` 和 evidence IDs，不补研究、不改事实口径。
- 执行层只消费锁定的表达包，不重新判断主张、不改写对白、不从字幕反推内容。
- 内容问题向表达层退回，事实问题向 `topic-research` 退回，音频/视觉/渲染/发布问题留在执行层处理。
- 子 Workflow 各自拥有 Required Resources、执行产物和质量门禁；父 Workflow 不复制子 Workflow 的资源表。
- `references/global-contract.md` 是三层共用的项目生产契约；音频后端和音色参数属于 `investagent-video-execution` 的子 Workflow，不放在父路由中。

## Phase 1: fact-layer — 事实研究子 Workflow

### Goal

冻结批准问题、证据、当前判断、最强反证、推翻条件和研究缺口。

### Child Workflow

`topic-research`

### Input

批准 topic card、研究日期、来源边界和账号内容政策。

### Output

`outputs/research/{subject_id}/{research_date}/` 下的 `approved-topic.json`、`source-ledger.md`、`evidence/`、`research-brief.md`、`research-quality-gate.md` 和 `research-execution.md`。

### Quality Criteria

- `Scope Decision` 必须为 `accepted`；
- 关键事实有来源、日期、主体、口径、定位和 evidence ID；
- `investagent` 按 `topic-research` 的问题适配规则执行并留下原生产物；公司/多公司综合研究题不得静默跳过；
- 当前判断、机制、最强反证、时间范围和推翻条件均已冻结；
- 研究包不包含交易指令、目标价或仓位建议。

### Known Issues

事实层资源由 `topic-research` 按问题选择；行业题不强行跑公司研究，非财务问题不强行补三表。研究发现主体或主问题变化时退回选题层。

## Phase 2: content-expression — 表达层子 Workflow

### Goal

把冻结研究转成唯一主张、清晰叙事和真实 `host_analyst` 双人对白，锁定后才能进入媒体执行。

### Child Workflow

`investagent-content-expression`

### Input

Phase 1 已验收的 research package、账号 profile、目标平台和时长。

### Output

导演锁定包、`episode-input.json`、锁定 `episode.json`、`dialogue-map.json`、口播表达记录和表达层执行回执。

### Quality Criteria

- 唯一核心主张、增长承诺、模块顺序和结尾判断已锁定；
- `host_analyst` 中主理人负责观众问题与承接，分析师负责回答、证据和边界；
- 每个事实、数字和判断均来自冻结研究包；
- 口语、概念记忆点、幽默和节奏只改变表达，不改变事实与结论强度；
- `check_editorial_gate.py` 与 `check_podcast_dialogue.py` 通过。

### Known Issues

如果事实或研究证据不足，不在表达层补写；如果只是内容不好听，退回表达层内部的导演锁定或对白锁定，不退回执行层。

## Phase 3: video-execution — 执行层子 Workflow

### Goal

把表达层已经锁定的双人播客内容编译成音频、字幕、视觉、HyperFrames 成片和发布包，并验证音画与内容一致。

### Child Workflow

`investagent-video-execution`

### Input

Phase 2 已锁定的 `episode.json`、dialogue map、account profile、音色、视觉规则、目标平台和发布授权。

### Output

逐句音频、字幕、视觉计划、HyperFrames Composition、封面、最终视频、QA 报告和发布回执。

### Quality Criteria

- 只消费锁定文本和 evidence IDs；
- 音频、字幕和画面均从同一 manifest/真实音频时间轴派生；
- 执行层发现内容事实、主张或对白问题时退回 Phase 2，不在执行层临时改稿；
- 通过音频、视觉、证据、时间线和平台发布门禁。

### Known Issues

音色、TTS、HyperFrames、平台接口和渲染失败属于执行层问题；不要通过修改主张或口播文本来绕过技术故障。
