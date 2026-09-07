# Workflow: investagent-video-execution

> 位置: Project: projects/investment-research-video/workflows/investagent-video-execution/

## Mission

把表达层已经锁定的双人播客内容编译成音频、字幕、视觉、HyperFrames 成片和发布包。执行层不重新研究、不重写主张、不改变锁定对白。

## Input

- `investagent-content-expression` 已通过的 `episode.json`、dialogue map、表达差异和执行回执；
- account profile、音色资源、视觉规则、目标平台、画幅、时长和发布授权；
- 可视化所需的 evidence IDs、chart intent 和研究包只读引用。

## Output

运行目录下的 `podcast/audio/`、`podcast/visual-plan/`、`podcast/project/`、`podcast/renders/`、`podcast/qa/` 和 `publish/` 产物。

## Principles

- `episode.json` 是锁定文本和角色关系的唯一事实源；执行层不得从字幕、画面或音频反推并改写内容。
- 所有时序以真实音频为准；字幕和画面跟随音频，不估算替代真实时长。
- 任何事实、主张、对白或数字问题都退回表达层；TTS、音频、视觉、渲染和发布问题留在执行层。
- 原始研究材料不在执行层重新研究；只使用已锁定 evidence IDs 和来源引用。
- 音频阶段固定使用 VoxCPM2 continuation、`--natural-pauses`、`--post-process natural` 和 inference timesteps 10；voice override 只作用于当前运行，父 Workflow 不提供执行参数。默认保留 TTS 原生语速，不能由通用 baseline 自动把所有 turn 变速；任何 atempo 必须来自明确 pacing_plan，并在 QA 中同时比较 raw/paced 字速。

## Phase 1: audio-compile — 音频与字幕编译

### Goal

从锁定 episode manifest 生成逐句音频、字幕和音频质量回执。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| `podcast-audio-compiler` | skill | 必选 | workspace installed_ref | 逐句 TTS、拼接、字幕和音频 QA |
| `media-use` | skill | 必选 | workspace installed_ref | 音频媒体接入与资产记录 |
| `hyperframes-audio` | skill | 可选 | workspace installed_ref | 已有音频需要混音时使用 |

### Input

锁定 episode、音色资源和 pacing plan。

执行参数：`format=host_analyst`、`host=zhiwei`、`analyst=shenyan`；使用 `voice.zhiwei` 与 `voice.shenyan`，必要时通过运行时 override 指定参考音频和 emotion 资源。VoxCPM2 continuation 使用 inference timesteps 10、`--natural-pauses` 和 `--post-process natural`。CosyVoice3、IndexTTS 和其他 clone mode 属于独立 A/B，不得静默混入当前生产 profile。

### Output

`podcast/audio/segments/`、`segments.json`、完整音频、`subtitles.srt`、`audio-qa.json` 和 `phase1-execution.md`。

### Quality Criteria

- 文本、speaker、voice/profile 和 pacing 可追溯；
- 文本或 speaker 变化会使缓存失效；
- 字幕来自真实音频；
- `pause_anchors` 必须在实际需要的句内位置落地，逗号不能只依赖 TTS 自行解释；单字回应要在完整短语中生成并抽查首字可辨识度；
- 问句 turn 必须基于 `voice.zhiwei` 的问句 canary 抽查升调（canary 未做或失败时，`rising_question` 不能作为已依赖的生产能力，问句须改写为不依赖升调的表达）；
- 反向对齐、独立 ASR 和 artifact consistency 通过。
- `audio-qa.json` 记录 backend、voice override、停顿、后处理和复用片段数；参考音频、emotion 和 prompt_text 必须与登记的 voice asset 一致。

### Known Issues

停顿优先回到表达层脚本解决；音频层不改观点和数字。

## Phase 2: visual-and-composition — 视觉与时间轴

### Goal

把锁定对白、真实音频、字幕和 evidence IDs 转成可渲染的 HyperFrames Composition、图表和封面。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| `hyperframes` | skill | 必选 | workspace installed_ref | Composition 与渲染入口 |
| `hyperframes-core` | skill | 必选 | workspace installed_ref | tracks、timing 与确定性契约 |
| `hyperframes-animation` | skill | 必选 | workspace installed_ref | seek-safe 动画与节拍 |
| `hyperframes-creative` | skill | 必选 | workspace installed_ref | 视觉方向与排版 |
| `information-visualization-architect` | agent | 必选 | internal installed_ref | evidence IDs 到 chart/scene 的映射；不补数据 |
| `static-html-qa` | skill | 必选 | workspace installed_ref | HTML、溢出、数字和公开文案检查 |

### Input

锁定 episode、真实音频、字幕、account profile、chart intent 和 evidence IDs。

### Output

`podcast/visual-plan/scene-manifest.json`、HyperFrames project、横竖封面和 `phase2-execution.md`。

### Quality Criteria

- 视觉只表达已锁定的机制、比较和证据；
- chart 数字回指 evidence IDs，不能写死事实；
- 口播、图表、B-roll、字幕职责不重复；
- 多步图（折线/多折线/step-line/流程/检查清单/验证看板）必须提供绑定真实 turn 的 `narration_beats`，并通过 `scripts/check_podcast_visual_sync.py`（兜底验证；契约源头在 `information-visualization-architect` 实体 §3）；在 Composition 实现按真实 segment start 逐点 reveal 之前，多步图一律不得通过本门禁；
- 视觉按手机观看优先验收：图表、标题、标签、数字和字幕必须在手机适配尺寸下直接可读；有图表的话题使用图表主视觉并覆盖完整数据解释段；
- 字幕按影视字幕习惯在自然标点处生成多个 cue；逗号、句号、分号和冒号只负责切分，不显示在字幕末尾，问号和感叹号保留；一条 cue 默认不超过 28 个汉字，仅在没有可用标点且确实会溢出时兜底切分，并以真实 turn 时长做确定性区间映射；
- 正片不显示说话人姓名或角色 badge；双人身份通过各自稳定的字幕颜色区分，SRT/字幕 manifest 的 viewer-facing text 也不添加角色前缀；
- 不固定三张卡片，卡片数量和版式由内容决定；不在正片画面显示“开场”作为标题或导航标签；
- 封面必须直接复制 `account-profile/cover-reference/cover-template.html` 及其背景资产；不得用独立 CSS 仿写封面风格；
- 所有 scene 使用同一真实音频累计时间轴。

### Known Issues

视觉发现内容逻辑问题时退回表达层，不在 Composition 代码里修主张。

## Phase 3: render-and-regression-qa — 渲染与回归门禁

### Goal

证明成片内容、音频、字幕、视觉、时间线和模板复用均通过验收。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| `hyperframes-cli` | skill | 必选 | workspace installed_ref | check、snapshot 与 render |
| `hyperframes-animation` | skill | 必选 | workspace installed_ref | 动画与节奏审计 |
| `static-html-qa` | skill | 必选 | workspace installed_ref | 公开文案、数字、字体和布局回归 |
| `research-quality-gate` | skill | 必选 | workspace installed_ref | 研究、脚本、字幕和证据一致性 |

### Input

完整 Composition、最终音频、字幕、episode、研究包和第二个 subject/变体。

### Output

`podcast/renders/draft.mp4`、`final.mp4`、`podcast/qa/episode-qa.md`、`reuse-regression.md`、snapshots 和 `phase3-execution.md`。

### Quality Criteria

- 成片没有新增事实、口径漂移、直接建议或内容承诺断裂；
- opening canary、关键模块、OUTRO 和第二个变体均通过检查；
- 音画、字幕、图表和转场使用同一时间轴。
- 手机缩小截图通过 `scripts/check_mobile_legibility.py`，且人工检查无文字裁切、图表拥挤和小字不可辨。

### Known Issues

单一 subject 通过不能证明复用性；第二变体失败时记录适配边界，不修改表达层主张。

## Phase 4: publish — 发布与复盘移交

### Goal

生成发布包，在用户授权后完成发布，并把真实作品与增长数据移交复盘。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| `video-agent-publisher` | skill | 必选 | workspace installed_ref | 平台差异化标题、描述、标签和来源 |
| `aitoearn` | skill | 可选 | workspace installed_ref | 用户授权的平台上传与状态回传 |
| `social-auto-upload` | skill | 可选 | workspace installed_ref | 主通道明确失败且无重复提交风险时回退 |
| `douyin-creator-tools` | skill | 可选 | workspace installed_ref | 发布后作品与评论采集 |

### Input

通过 QA 的 final.mp4、封面、episode、来源清单、增长 contract、目标平台和明确发布授权。

### Output

`publish/metadata.json`、`sources.md`、平台结果和 `phase4-execution.md`。

### Quality Criteria

- 未获得真实发布授权时只生成草稿；
- 任务 ID 不当作作品 URL；
- 发布状态、错误、作品链接和用户操作可追溯。

### Known Issues

平台任务创建不等于成功发布，必须追踪最终状态。
