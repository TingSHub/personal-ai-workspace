# Production Contract

本文件只规定视频生产运行目录、共同输入和媒体交付。研究来源、官方资料归档和证据选择由 `topic-research` 负责，不在生产 Workflow 重复维护。

## Run Root

每期使用 `outputs/subjects/{subject_id}/{run_date}/`。`subject_id` 是稳定、可读的研究对象标识；公司、行业、主题、事件、技术、政策、宏观和比较议题使用同一目录形态。历史 `outputs/companies/` 保留追溯，不迁移、不作为新运行默认路径。

## Accepted Inputs

- 用户已批准的 topic card，只读引用上游 `topic-forward-lead` 结构化事实源；
- Scope Decision 为 `accepted` 的 `topic-research` research brief 与 source ledger；
- `account-profile` 的内容、对白、视觉与音色规则；
- 按 `investment-video-episode-input.json.template` 生成的 episode input。

批准卡与 research brief 的主体或主问题不一致时停止。标题、章节和叙事方式的变化不算改题，由内容导演决定。

## Required Production Outputs

```
outputs/subjects/{subject_id}/{run_date}/
├── editorial/
│   ├── director-treatment.md
│   ├── topic-order.json
│   ├── opening-selection.json
│   ├── scene-intent.json
│   ├── feedback-constraints.md
│   ├── episode-input.json
│   └── phase1-execution.md
├── podcast/
│   ├── script/episode.json
│   ├── audio/segments.json
│   ├── audio/narration-full.wav
│   ├── audio/narration-full.mp3
│   ├── qa/captions.json
│   ├── qa/audio-qa.json
│   ├── qa/episode-qa.md
│   ├── visual-plan/scene-manifest.json
│   ├── project/cover.html
│   ├── project/cover.png
│   ├── project/cover-3x4.png
│   └── renders/final.mp4
└── publish/
    ├── metadata.json
    ├── sources.md
    └── platform-results.json
```

未执行真实发布时不创建伪 platform result；未使用可选阶段时不创建占位文件。

## Growth Contract

同一期视频只使用一套增长承诺：

- topic card 提供点击理由、观看承诺、互动价值和关注理由；
- 内容导演明确这些价值分别在封面/标题、前 10 秒、正文段落、结尾何处兑现；
- 成片 QA 检查兑现，不用标题点击替代内容质量；
- 发布后按曝光、点击/播放、2 秒/5 秒、平均观看/完播、互动、主页访问和关注完整漏斗复盘。

## Thesis And Closing Contract

- `editorial_thesis` 是本期唯一核心判断；`thesis_contract` 记录机制、时间范围、受影响环节、最强反证、推翻条件和 evidence ids。
- OUTRO 必须把当前判断说出来，再说明为何成立、适用于什么时间和环节、什么证据会改变判断。
- “继续看财报”“等待数据”“持续关注”“未来可期”只能作为验证动作或过渡，不能单独收束。
- 评论问题应来自本期真实分歧或推翻条件，不使用与内容无关的通用二选一。

## Performance Contract

- manifest 以 `COLD_OPEN` 开始，`INTRO` 可选；逐句音频是唯一时间轴。
- `host_analyst` 是默认角色关系，`debate` 仅显式启用；不要求双方等量发言。
- 每个 turn 保留 speaker、reply、interaction、evidence、fact/source 和 visual intent；短回应要有明确 backchannel 与停顿。
- 数字在研究事实层保留精确口径，口播层优先听觉理解，画面层优先数量级和关系；三层不能改变方向或比较结果。
- 口语化、情绪与停顿在脚本阶段锁定；音频阶段不得临时改观点或数字。

## Visual And Cover Contract

- 视觉样式从 account profile 选择，可按叙事使用 editorial-paper、data-newsroom、dark-terminal、field-notes、timeline-board 或已验证新模式。
- 每个 scene 由内容目的驱动；图表、B-roll、字幕和口播不重复承担同一信息。
- 章节、scene、caption、audio 与进度条共用全局累计时间线。
- 平台封面是独立 HTML/PNG 资产，不进入正片。横版 1440×1080，竖版 1080×1440，分别排版并检查手机可读性。
- 封面只保留研究对象、一个冲突主标题和必要辅助信息；公司名不再是强制元素。缺省副标题为“{subject} 深度解析”。
- OUTRO 视觉读取 manifest 的本期结论，不使用固定“毛利、现金流、产能”文案。

## Reuse And QA

- 生成器不得写死公司、行业、话题、开场、结尾或事实数据。
- 第二个不同 subject/叙事变体应只替换 manifest 即可生成 draft；失败时记录适配边界。
- 音频必须经过反向对齐、独立 ASR 和 artifact consistency；视觉必须经过 HyperFrames check、关键帧审阅、字幕/时间线和 static HTML QA。
- 任何新增事实、口径漂移、未兑现增长承诺或结尾立场缺失都必须退回相应上游阶段。
