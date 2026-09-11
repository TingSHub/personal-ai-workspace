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
- 视觉编排必须把已锁定讲解转成可见的状态变化：建立对象、显示关系、突出比较、呈现边界、收束判断。读取动画 Skill、写入节拍或通过静态检查均不等于动画已经落地。
- 先验证代表性动态样片，再扩展整片。技术可渲染、图表语义正确、运动与讲解同步、视觉美感和混音听感分别验收；不能互相替代。
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
| `media-use` | skill | 条件必选 | workspace installed_ref | 需要新增音效、BGM 或媒体时解析并冻结本地素材与来源记录 |
| `hyperframes-audio` | skill | 条件必选 | workspace installed_ref | 放置音效或 BGM 后执行混音、人声避让和淡入淡出 |

### Input

锁定 episode、真实音频、字幕、account profile、chart intent 和 evidence IDs。

### Output

`podcast/visual-plan/scene-manifest.json`、HyperFrames project、横竖封面和 `phase2-execution.md`。`scene-manifest.json` 按模板 `investment-video-scene-manifest.json.template` 的 v3 契约填写，是唯一的语义运动事实源，统一承载场景、认知变化、讲解状态、衔接和可选声音事件。使用声音素材时同时交付本地资产和来源记录。

### Execution Order

1. **选择视觉语法**：读取 account design、组件契约和已锁定 scene intent。为每段先写 `viewer_question`、`cognitive_change`、`continuity_anchor`，再从账号场景语法中选择模式。优先复用账号级视觉参考与已验证模式；只有出现新的视觉关系时才补参考画面。品牌 token 决定颜色与字体，讲解内容决定布局；同一个图表可跨多个讲解状态持续存在。
2. **编译单一 manifest**：在 `scene-manifest.json` 中把真实 turn / 句内对齐锚点写成 `states`，每个状态指定动作、目标元素、证据和稳定阅读区间；同一场景写入 `transition_out`，需要声音时写入 `audio_cues`。先建立对象，再揭示数据、连接关系、突出比较或反证，最后稳定停留。使用基础生成器时必须传入 `--scene-manifest`，由运行时按全局真实时间执行 state；目标元素不存在时生成失败。
3. **图表能力核对**：根据当前实现逐项验证类型、数据几何、轴域和揭示能力。语义不同的图表不能仅换名称并共用不相符的形状。未知类型、空图、负值失真、系列独立归一化却暗示同轴比较、数据点裁切、无根据的截断均应失败。使用真实兼容组件或修复生成器后重新验收；不能因模板已有相似外观就判定支持。
4. **衔接编排**：调用 `hyperframes-animation`，选择一种主衔接和至多两种强调方式。基础生成器只使用 `push`、`focus-pull`、`crossfade` 或 `cut`，并通过位置、颜色与运动方向维持连续性；收束让证据焦点过渡到结论。默认从 0.35–0.7 秒试作并按叙事调整。共享元素、遮罩或其他复杂转场只有专用 Composition 已真实实现并通过代表段验收后才能扩展模板与门禁。
5. **按需声音编排**：需要强调关键揭示、机制闭合或换章时，调用 `media-use` 选择少量短音效并绑定既有 state；再调用 `hyperframes-audio` 做增益、淡入淡出和人声避让。没有明确叙事用途时保持安静，不创建占位音轨。
6. **代表段验证**：首次使用新的图表、衔接或声音模式时，用真实音频验证一段连续完整解释。样片放在临时工作目录，只把通过/返修结果写进 `phase2-execution.md`，不作为每期正式交付物。已验证模式可直接复用并执行回归抽查。
7. **整片扩展**：只扩展已验收的图表组件、运动方式和声音处理。每个主题继续依据语义编排状态，不能重复套用章节开头的统一 stagger。

Figma 仅作为账号级视觉参考和新模式设计工具。既有视觉语法直接按 `account-profile/design.md` 复用；不要求每期创建、复制或验收 Figma 文件，也不把 Figma 连接设为生产前置依赖。

### Quality Criteria

- 视觉只表达已锁定的机制、比较和证据；
- chart 数字回指 evidence IDs，不能写死事实；
- 口播、图表、B-roll、字幕职责不重复；
- 多步图（折线/多折线/step-line/流程/检查清单/验证看板）必须在 `scene-manifest.json` 中至少有两个直接寻址该图表元素的 state；
- `scene-manifest.json` 必须连同真实 `segments.json` 和 chart spec 通过 `scripts/check_podcast_visual_sync.py --scene-manifest ... --segments ... --charts ...`，检查所有 topic 覆盖、语义 state、真实 turn、时间、动作、图表目标和声音引用；
- state 只能寻址 clip 内部的稳定元素，不能直接动画 `topic-*`、`turn-*`、`caption-*`、`chart-stage-*` 或 `persistent-nav-*` 等由 HyperFrames 管理生命周期的 clip；
- 上述脚本仅证明节拍引用完整，不证明画面同步。所有承担解释的图表（包括条形、差值、贡献与区间图）均需按导演稿抽查实际事件前、中、后的渲染状态，并验证目标元素存在、落点来自真实音频、状态顺序正确。未实现 runtime 消费节拍时明确判定返修。
- 哑铃图必须表达两端及连接差距；发散条形图必须有共同零线与正负方向；瀑布图必须累计并表达起终点；堆叠图必须保留组成关系；阶梯线必须表达离散变化；区间图必须表达上下界。动画最终几何必须对应原始数据，不能用回弹夸大数值。
- 图表主体按数据与讲解需要占据画面，减少重复外框和重复标题。关键数字使用稳定对齐的数字字形；非当前系列适当弱化，当前关系通过位置、注解与颜色共同突出。颜色含义沿本期证据和账号规则明确，不把涨跌自动等同好坏。
- 每个解释段都有可追溯的语义变化及必要阅读停留。长时间不变的读图区间必须有明确阅读目的，不用装饰动画填满时间。
- 连续三个 scene 不得复用同一布局族；含三个及以上 state 的 scene 不得只使用一种动作。标题、字幕、背景动势和进度条不计入语义变化。
- 新模式的代表段通过手机阅读、图表语义、音画落点、连续衔接与听感检查后才能扩展；已验证模式在整片 QA 中抽查。运行成功和单张漂亮截图均不能替代本门禁。
- 视觉按手机观看优先验收：图表、标题、标签、数字和字幕必须在手机适配尺寸下直接可读；有图表的话题使用图表主视觉并覆盖完整数据解释段；
- 字幕按影视字幕习惯在自然标点处生成多个 cue；逗号、句号、分号和冒号只负责切分，不显示在字幕末尾，问号和感叹号保留；一条 cue 默认不超过 28 个汉字，仅在没有可用标点且确实会溢出时兜底切分，并以真实 turn 时长做确定性区间映射；
- 正片不显示说话人姓名或角色 badge；双人身份通过各自稳定的字幕颜色区分，SRT/字幕 manifest 的 viewer-facing text 也不添加角色前缀；
- 不固定三张卡片，卡片数量和版式由内容决定；不在正片画面显示“开场”作为标题或导航标签；
- 封面必须直接复制 `account-profile/cover-reference/cover-template.html` 及其背景资产；不得用独立 CSS 仿写封面风格；
- 所有 scene 使用同一真实音频累计时间轴。

### Known Issues

视觉发现内容逻辑问题时退回表达层，不在 Composition 代码里修主张。

当前 `build_podcast_composition.py` 强制接收完整 `--scene-manifest`；空 manifest 或未覆盖全部 episode topic 会直接失败。基础生成器支持 `push`、`focus-pull`、`crossfade` 和 `cut`，并分别实现六种 state 动作；未知转场不得写入 manifest。基础生成器会拒绝未知图表类型和缺失端点的哑铃图，区间图与多折线使用共享尺度，step-line 使用阶梯几何，瀑布图按累计关系生成；`stacked-bar` 仍需专用组件。默认仍只有旁白音轨；含 `audio_cues` 的 manifest 必须改用已完成混音接入的 Composition，基础生成器会明确拒绝，不能假装声音已经落地。

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

`podcast/renders/draft.mp4`、`final.mp4`、`podcast/qa/episode-qa.md`、`reuse-regression.md`、snapshots 和 `phase3-execution.md`。运动、衔接、图表语义和声音结果写入现有 `episode-qa.md`，不另建审阅文档。

### Quality Criteria

- 成片没有新增事实、口径漂移、直接建议或内容承诺断裂；
- opening canary、关键模块、OUTRO 和第二个变体均通过检查；
- 音画、字幕、图表和转场使用同一时间轴。
- 用 `hyperframes-animation` 的 animation map 审计实际动画分布，再对照导演稿检查语义推进；运动数量和画面变化量不能独立证明讲解质量。
- 每类图表和每种衔接至少审阅一处前、中、后状态；首尾、长解释段、最终数据状态和所有发现异常的位置必查。对同一时刻比较顺播与随机跳转，排查提前曝光、消失、黑帧、叠字和跨章状态污染。
- 抽查最终 MP4 的音效、旁白与字幕落点，记录实际偏差和所用容差；强揭示事件可从约 0.15 秒容差开始校准，需区别于持续解释动画。检查成片而非仅检查源时间轴。
- 有 BGM/音效时试听耳机与扬声器，确认语音清楚、没有双旁白、突然切断或音效掩蔽；测量混音峰值与响度并记录依据。混音更改后只重跑受影响的声音、时间线与最终文件检查。
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
