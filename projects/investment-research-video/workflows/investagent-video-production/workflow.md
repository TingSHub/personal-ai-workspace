# Workflow: investagent-video-production

> Version: 2.2
> 位置: Project: projects/investment-research-video/workflows/investagent-video-production/workflow.md
> Mission: 将已验收的 HyperFrames-native Finance Presentation 编译为真实音频时间，并由 HyperFrames 统一 Video Runtime 直接执行和渲染为旁白视频。

## Mission

本 Workflow 不重新规划内容、不重新设计页面，也不通过截图重建 Presentation。它接收上游 Finance Presentation Agent 已经生成并锁定的：

```text
HyperFrames-native HTML
+
Final Speaker Notes
+
Reveal Cues
+
Seek-safe Animation Semantics
```

完成：

```text
Validate
↓
TTS
↓
Audio Alignment
↓
Timing Compile
↓
HyperFrames Render
↓
Video QA
```

视频只是 Presentation Composition 的音频时间化与确定性执行，不是新的内容层。

**HyperFrames as Video Runtime**：HyperFrames 不只是最终渲染器，而是统一承载 Video Composition、Scene / Sub-composition、动画、视觉媒体、音频轨道、字幕与确定性执行的 Runtime。凡 HyperFrames 已稳定提供且效果满足要求的能力，优先在同一 Composition 中完成；外部 Skill 只用于 HyperFrames 不擅长、质量不足或需要专业能力的环节，例如高质量中文 TTS 和已知文本 Forced Alignment。

## Input

| 字段 | 必填 | 说明 |
|---|---|---|
| company_name | 是 | 公司名称，用于输出目录 |
| research_date | 是 | 研究日期（YYYY-MM-DD） |
| presentation_slug | 是 | 当前 Presentation 的稳定标识 |
| presentation_html | 是 | 上游已验收的 HyperFrames-native Presentation / Composition Skeleton，默认来自 `outputs/companies/{company_name}/{research_date}/investment-report.html` |
| presentation_execution | 是 | 上游 Presentation 执行记录，包含 Scene、Notes、Reveal Cue 和验收状态 |
| tts_provider | 否 | 已配置的 TTS 提供方；Workflow 不绑定具体引擎 |
| speaker | 否 | 固定音色或 speaker 标识；全片必须保持一致 |
| existing_audio | 否 | 已存在且已验收的 Scene 音频或整段旁白，可跳过对应 TTS 工作 |
| existing_alignment | 否 | 已存在且已验收的 transcript / forced alignment，可跳过或复用 Alignment 工作 |

## Output

正式输出位于：

`outputs/companies/{company_name}/{research_date}/video/{presentation_slug}/`

```text
video/{presentation_slug}/
├── audio/
│   ├── scene-01.mp3
│   ├── scene-02.mp3
│   └── narration-full.mp3
├── segments.json
├── alignment.json
├── timing-map.json
├── subtitles/
│   └── narration.srt
├── composition/
│   └── index.html
├── renders/
│   ├── draft.mp4
│   └── final.mp4
├── qa/
│   ├── preflight.md
│   ├── timing-qa.md
│   ├── visual-qa.md
│   ├── audio-qa.md
│   └── content-qa.md
└── video-execution.md
```

产物约定：

- `segments.json`：每个 Scene 的 `scene_id`、`start`、`duration`、音频文件和音频时长。
- `alignment.json`：Final Speaker Notes 与真实语音的词/句级时间信息，以及使用的 Alignment 方法。
- `timing-map.json`：Reveal Cue → 真实 timestamp 的确定性编译结果。
- `subtitles/narration.srt`：从 Final Notes 和 Alignment 派生的字幕，不是独立文案。
- `composition/index.html`：由 Composition Skeleton 写入真实时间后的 Final HyperFrames Composition。
- `video-execution.md`：记录 Workflow 版本、输入、资源 by-name、installed_ref、各 Phase 输出与验收状态。

`timing-map.json` 是确定性编译产物，不是新的内容规划层。

## Principles

- **Content Lock**：每个 Scene 的 `<aside class="notes">` 是最终口播文本唯一 Source of Truth。Video Workflow 不重新润色、不改写事实、不改变表达含义、不生成第二套 Script；只允许 TTS 所需的技术性读音处理。
- **HTML First**：HyperFrames-native Presentation 是 Visual / Semantic Source of Truth，Video Workflow 在不复制视觉内容的前提下，将其 Composition Skeleton 编译为 Final Composition。
- **HyperFrames Runtime First**：HyperFrames 是最终 Video Composition、Scene / Sub-composition、动画、视觉媒体、音频轨道、字幕和确定性执行的统一 Runtime，不只是最后一步的 Renderer。可由 HyperFrames 稳定完成且质量满足要求的能力，不拆到外部工具或第二套 Composition。
- **Scene-oriented Composition**：默认让重要 Scene 对应独立 Composition / Sub-composition，以获得清晰的状态隔离、动画生命周期和 QA 边界；简单 Scene 可以在不损害确定性、可维护性和调试性的情况下共享 Composition。关键不是形式上的 1:1，而是状态隔离、seek-safe、易调试和易返工。Preview、Presenter 和 Video 仍共用同一套 Scene DOM/SVG、Notes 与 Reveal Semantics，不得另做一套 Video HTML。
- **Audio First**：真实时间由音频决定：`Notes → TTS → Scene Duration → Alignment → Cue Timestamp`。Presentation Agent 决定 WHAT / HOW，Video Workflow 决定 WHEN。
- **Deterministic Render**：核心动画必须可以被 HyperFrames seek，并在任意时间点得到可复现状态。
- **No Screenshot Composition**：截图只允许用于 QA 对比、人工审片或回归证据，不得进入正式 Composition 的视觉源链路。
- **No xfade Timeline**：禁止使用多级 FFmpeg `xfade` 作为主时间轴；FFmpeg 只用于编码检查、音视频 mux、抽帧 QA 和必要的最终封装。
- **内容边界**：沿用 `investagent-html-report` 的企业研究边界，旁白、字幕和视频画面不得新增目标价、评级、买卖建议、仓位、交易策略或交易信号。
- **External Skill Boundary**：外部 Skill 只补足 HyperFrames 不擅长、质量不足或需要专业能力的环节；本 Workflow 当前允许外置的主要环节是高质量中文 TTS 和已知文本 Forced Alignment。其余能力优先回到同一 HyperFrames Composition。
- **HyperFrames Capability Adoption**：新增视频能力时，按以下顺序判断与落地：
  1. HyperFrames Composition 原生能力；
  2. HyperFrames 官方动画 / media / audio 能力；
  3. 已验证的外部专业 Skill；
  4. 最后才自建脚本或第二套媒体处理链。
  不得因为已有旧脚本，就绕开 HyperFrames 已经稳定提供的能力。
- **Best available resource**：在允许外置的环节中，按实际效果、输出质量、稳定性、依赖成本、维护成本和当前项目适配性选择 TTS 与 Alignment 资源，不因本地已有脚本而强制绑定。
- **真实执行留痕**：每个 Phase 的 Required Resources 必须真实执行并留下独立产物；未执行资源不得写成已执行。
- **只消费已验收产物**：下游 Phase 只消费通过上游 Quality Criteria 的 HTML、Notes、音频、Alignment 和 Timing Compile 产物。
- **by-name 引用**：Workflow / Skill / Agent / Experience 一律使用 by-name 标识符，不使用相对路径作为资源名称。

## Phase 1: validate — Content Lock 与 Composition Preflight

### Goal

确认上游 Presentation 已达到 Content Lock 和 Composition-ready 状态，可以进入 TTS 与真实时间编译。

如果失败，返回 Finance Presentation Agent；本 Phase 不修正文案、不改设计、不自行补研究。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| hyperframes | skill | 必选 | github · c32b804 | 运行当前安装版本的 Composition `check` / `lint` / 必要 snapshot；验证 Composition contract、稳定 ID 和 seek-safe 结构 |
| static-html-qa | skill | 必选 | internal | 执行内容边界、数值一致性和 HTML/DOM 基础质检；截图仅作为 QA 证据，不进入 Composition |

### Input

- `presentation_html`
- `presentation_execution`
- Phase 3 已验收的 Editorial Master 内容边界与数值期望清单

### Output

- `qa/preflight.md`：Content Lock、Composition-ready、HTML QA 和资源版本的独立检查记录。

### Quality Criteria

- 每个 Scene 有唯一、稳定的 `scene_id` / Composition ID。
- 每个 Scene 有 Final Speaker Notes；Notes 与 Presentation HTML 中的 `<aside class="notes">` 完全一致。
- 每个重要 Reveal Cue 唯一、稳定，顺序可从 Notes / cue anchors 复现。
- Visual、Notes、Reveal 服务同一个 Core Message；不得出现内容漂移。
- Composition 不依赖截图作为正式视觉源，不依赖 `Date.now()`、随机数、wall-clock CSS、`setTimeout()` 驱动核心动画或无限循环。
- HyperFrames `check` / `lint` 与静态 HTML QA 通过；发现问题必须在上游修复后重新验收。

### Known Issues

- HyperFrames 版本升级可能改变 Composition contract；必须记录实际 `installed_ref`，不得只记录命令成功。
- 如果 HTML 仍是普通 Deck、Reveal 没有稳定语义标识或 Notes 尚未锁定，不得在视频阶段临时修补。
- Preview 截图只能证明某个时刻的视觉结果，不能替代 seek-safe Composition 验证。

## Phase 2: tts — Scene Audio Production

### Goal

按照每个 Scene 的 Final Speaker Notes 合成稳定音色旁白，得到真实 Scene 时长和全片 narration。TTS 不改变 Notes 文本。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| video-production-executor | agent | 必选 | workspace internal · internal | 负责按 Scene 执行外部 TTS、音频检查、拼接和执行留痕；不补研究、不改 Notes、不重写内容 |
| edge-tts | skill | 可选 | github · 7.2.8 | 仅作为 HyperFrames 外部 TTS 能力的内部原型/试音实现；非官方逆向接口，不用于正式商业发布，正式项目应使用已配置的合规提供方 |

### Input

- Phase 1 `preflight.md`
- 每个 Scene 的 Final Speaker Notes
- 可选 `tts_provider`、`speaker` 或已验收 `existing_audio`

### Output

- `audio/scene-NN.mp3`：逐 Scene 音频。
- `audio/narration-full.mp3`：按 Scene 顺序拼接的完整旁白。
- `segments.json`：按真实音频时长计算的 Scene 起止时间。
- `qa/tts-execution.md`：provider、speaker、文本 hash、文件、时长和验收记录。

### Quality Criteria

- 全片固定 speaker，不能出现跨 Scene 音色随机漂移。
- 每个音频文件都能通过媒体探针读取，Scene 顺序与 HTML Scene 顺序一致。
- `segments.json` 的 Scene duration 来自真实音频，不使用估时或固定时长。
- 全片音频时长等于各 Scene 时长之和，允许编码级微小误差；拼接不改变语音内容。
- 只允许技术性读音处理，例如 SSML、数字读法映射或停顿参数；不得新增、删除或改写事实与句意。
- TTS provider 可替换，Workflow 不把内容契约绑定到某一个引擎。

### Known Issues

- `edge-tts` 只适合内部原型和试音，正式发布需使用合规的可商用 TTS 提供方。
- 长文本应按 Scene 或稳定文本边界分段；不得为了方便合成长音频后再凭估计切 Scene。
- TTS provider 返回的编码时长可能存在毫秒级差异，必须统一使用媒体探针结果生成 `segments.json`。

## Phase 3: alignment — Audio Alignment 与 Cue 定位

### Goal

把 Final Speaker Notes 中的 narration blocks / Reveal Cue anchors 与真实 Scene 音频建立可靠时间对应，生成 Alignment 和字幕时间信息。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| qwen3-forced-aligner | skill | 必选 | qwen-asr 0.0.6 · Qwen3-ForcedAligner-0.6B | HyperFrames 不足以满足已知文本精确对齐时使用的外部专业能力：Final Notes + Scene Audio → 字/句级时间戳；长音频、GPU 和中文多音字需按资源限制处理 |

### Input

- Phase 2 `audio/scene-NN.mp3`
- Phase 2 `segments.json`
- Final Speaker Notes
- Reveal Cue / narration cue anchors
- 可复用且已验收的 `existing_alignment`

### Output

- `alignment.json`：Scene、narration block、词/句时间戳和对齐方法。
- `timing-map.json`：Reveal Cue 到真实 timestamp 的映射。
- `subtitles/narration.srt`：从 Notes 与 Alignment 派生的字幕。
- `qa/alignment-execution.md`：对齐覆盖率、异常 Cue、人工检查和资源版本。

### Quality Criteria

- 每个重要 Reveal Cue 都能定位到真实音频时间。
- Cue 顺序必须与 Notes / Reveal Semantics 顺序一致。
- 无法稳定匹配的 Cue 必须报错或进入人工检查，不得猜测 timestamp。
- 每个 Scene 的结束时间等于该 Scene 音频 duration；Scene 间不重叠、不产生空洞，除非 Presentation 明确定义了间隔。
- 字幕只从 Final Notes 派生，可断句和加时间，不得另写文案。
- `timing-map.json` 明确记录 scene_id、cue_id、timestamp、来源 block 和异常状态。

### Known Issues

- Qwen3 Forced Aligner 依赖已知文本，且长音频需要分段；超出单次处理范围时按 Scene 或更短片段对齐。
- 对齐质量依赖 TTS 清晰度；带 BGM、混响或压缩失真的音频不得直接作为对齐输入。
- 对齐器不能稳定识别某个 Cue 时，保留异常并回到人工检查，不通过手工 delay 猜测修复。

## Phase 4: timing-compile — Semantic Timing 编译

### Goal

把真实音频时间写入 Presentation Agent 已生成的 HyperFrames Composition Skeleton，生成 Final HyperFrames Composition，完成：

```text
Semantic Timing → Real Timing
```

本 Phase 只编译时间，不重新设计动画、页面、Scene 或叙事。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| hyperframes | skill | 必选 | github · c32b804 | 按当前 Composition contract 写入 `data-start`、`data-duration`、音频轨道和 seek-safe timeline；执行 `check` / `lint` |
| static-html-qa | skill | 必选 | internal | 对编译后的 HTML 运行内容边界、数值和前端结构检查；不生成截图 Composition |

### Input

- Phase 1 已验收的 `presentation_html` Composition Skeleton
- Phase 2 `segments.json` 与 Scene Audio
- Phase 3 `alignment.json`、`timing-map.json`、`subtitles/narration.srt`

### Output

- `composition/index.html`：写入真实时间后的 Final HyperFrames Composition。
- `composition/assets/`：Composition 所需的本地音频、字幕或其他已批准媒体依赖。
- `qa/timing-compile.md`：编译前后 Scene/Cue 映射、总时长和 seek-safe 验收记录。

### Quality Criteria

- 写入 master duration、Scene `data-start`、Scene `data-duration`、audio track timing、Reveal Cue timestamp 和字幕时间。
- 视觉媒体、Scene / Sub-composition、音频轨道和字幕都写入同一 HyperFrames Composition；不得另建外部视频时间轴或截图序列。
- Scene duration 等于对应真实音频时长；master duration 等于全部 Scene 时间范围。
- 编译只改变时间数据与已定义的 timeline 参数，不改变 Visual、Final Notes、事实或 Core Message。
- Cue 顺序与 `timing-map.json` 一致；不允许为了对齐而新增 Reveal、删除 Scene 或改变动画语义。
- GSAP / HyperFrames timeline 在任意 seek 时间点可重复得到同一状态，不依赖上一帧历史状态。
- 编译后的 Composition 通过 HyperFrames `check` / `lint` 和静态 HTML QA。

### Known Issues

- 任何编译后的 Composition 内容变化都必须视为上游 Presentation 变更，不能在 Timing Compile 中偷偷修复。
- 若时间映射不完整，应回到 Alignment；若 Visual 不支持当前 Cue，应回到 Presentation Agent。
- 真实时间可能使页面原有留白或节奏不合理，但只能通过新的 Presentation 版本解决，不通过临时 delay 堆叠解决。

## Phase 5: render — HyperFrames Deterministic Render

### Goal

直接从编译后的 HTML Composition 生成视频。HyperFrames 在本 Phase 作为统一 Video Runtime，执行 Scene / Sub-composition、动画、视觉媒体、音频轨道和字幕，先进行 draft 快验，再生成 standard/final 成片。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| hyperframes | skill | 必选 | github · c32b804 | 从 Composition 进行确定性 frame seek 与 MP4 渲染；使用当前安装版本的 render 参数和输出契约 |

### Input

- Phase 4 `composition/index.html`
- Phase 4 `qa/timing-compile.md`
- 本地化音频、字幕和 Composition assets

### Output

- `renders/draft.mp4`：用于快速发现时长、画面和音频问题。
- `renders/final.mp4`：通过 draft 与必要 QA 后的正式渲染结果。
- `qa/render-execution.md`：渲染命令、HyperFrames installed_ref、参数、输出媒体信息。

### Quality Criteria

- 正式流程为：`HTML Composition → HyperFrames deterministic frame seek → MP4`。
- 正式视频的视觉、动画、音频轨道和字幕均由同一 HyperFrames Composition 执行。
- 不经过 `HTML → PNG → Video` 的截图转视频路径。
- 不使用多级 FFmpeg `xfade` 作为主时间轴。
- FFmpeg 只用于编码检查、音视频 mux、抽帧 QA 或必要的最终封装。
- draft 与 final 使用同一份编译后 Composition；如两者视觉状态不一致，必须定位渲染参数或 seek 问题。
- 输出包含视频流和音频流，分辨率、帧率、编码格式符合项目目标配置。

### Known Issues

- HyperFrames 首次拉取、字体本地化和高质量渲染可能耗时较长；先完成 check/snapshot，再进行 final render。
- 渲染失败时先检查 Composition contract、资源路径、轨道冲突和 seek 状态，不退回截图方案。
- 正式成片必须保留渲染命令、参数和媒体探针结果，临时工作目录不得冒充最终产物。

## Phase 6: qa — Timing / Visual / Audio / Content QA

### Goal

对最终视频、音频、字幕、Timing Map 和 Composition 进行独立验收，确认无累计漂移、重影、状态残留、音画不同步和内容漂移。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| hyperframes | skill | 必选 | github · c32b804 | 在 cue 前/中/后进行 snapshot/seek，对 Composition 状态和可重复渲染进行验证 |
| static-html-qa | skill | 必选 | internal | 对最终 Composition 做 DOM/SVG、console、字体、overflow 和内容边界检查；截图只作为 QA 证据 |
| video-quality-reviewer | agent | 必选 | workspace internal · internal | 对成片、旁白、字幕和 Composition 做独立质量验收；只检查，不改写 Notes、字幕或渲染结果 |

### Input

- `renders/draft.mp4`、`renders/final.mp4`
- `audio/narration-full.mp3` 与 Scene Audio
- `segments.json`
- `alignment.json`
- `timing-map.json`
- `subtitles/narration.srt`
- `composition/index.html`

### Output

- `qa/timing-qa.md`
- `qa/visual-qa.md`
- `qa/audio-qa.md`
- `qa/content-qa.md`
- 更新 `video-execution.md` 的最终验收状态

### Quality Criteria

#### Timing QA

- 视频总时长与 narration 总时长一致，允许明确记录的编码级误差。
- Scene 切换时间与 `segments.json` 一致。
- Reveal 出现时间与 `timing-map.json` 一致。
- 抽查前段、中段、后段和最后一幕，确认无累计漂移。

#### Visual QA

在每个关键 Cue 的以下时间点 seek：

```text
t = cue 前
t = cue 时
t = cue 后
```

确认：

- 元素状态正确；
- 无重影、上一状态残留或重复 timeline；
- SVG / DOM 没有错位、裁剪或异常溢出；
- Reveal 可重复渲染；
- 同一时间多次 render 得到相同视觉状态。

#### Audio QA

- 音色统一；
- 无断裂、爆音、异常静音或 Scene 拼接不自然；
- 音量一致；
- 字幕与语音同步；
- 全片音频可被媒体探针读取并与 `segments.json` 对齐。

#### Content QA

- Final Notes 未被修改；
- 字幕由 Notes 派生，不存在第二套 Script；
- 没有新增研究事实、改变结论强度或引入未经编辑层审议的因果；
- 没有目标价、评级、买卖建议、仓位、交易策略或交易信号漂移。

### Known Issues

- **出现重影**：按 `seek-safe animation → CSS wall-clock animation → DOM 状态复位 → timeline 重复叠加 → transition 历史状态` 顺序排查，不首先退回截图方案。
- **Reveal 不同步**：按 `Notes Cue → Alignment → timing-map → Compiled Timeline → HyperFrames Seek` 顺序定位，不手工调整几十个 delay。
- **单个 Scene 无法稳定渲染**：只降低该 Scene 的动画复杂度或回到 Presentation 修复，不把整条视频降级为静态截图。
- **QA 截图与正式渲染差异**：以 seek 后的 Composition 状态和正式 render 为准，记录 snapshot/render 参数，避免把过渡中的中间帧当作最终状态。
- 未通过的 QA 必须记录证据、归属 Phase 和回退路径；没有证据的“看起来正常”不能作为最终验收。

## Architecture Boundary

完整链路：

```text
Financial Editor
↓
Editorial Master
↓
Finance Presentation Agent
↓
HyperFrames-native Presentation
│
├── Visual / Media Design
├── Scene / Sub-composition
├── Seek-safe Animation Semantics
├── Final Speaker Notes
└── Reveal Semantics
↓
Video Production Workflow
│
├── TTS
├── Audio Alignment
└── Timing Compile
↓
Final HyperFrames Composition
│
├── Visual
├── Animation Timeline
├── Audio Tracks
├── Subtitles
└── Real Timing
↓
HyperFrames Video Runtime
↓
MP4
```

职责边界：

```text
Finance Presentation Agent
→ Composition Skeleton：WHAT / HOW

外部 TTS / Forced Alignment
→ HyperFrames 不足部分的专业能力与 WHEN 音频证据

Timing Compiler
→ 将真实 WHEN 写入 Composition Skeleton，生成 Final Composition

HyperFrames Video Runtime
→ 执行 Final Composition：Scene、动画、视觉媒体、音频轨道、字幕与 deterministic execution

Video QA
→ 验证时间、视觉、音频与内容一致性
```

## Evolution Log

| 日期 | 变更 | 依据 |
|---|---|---|
| 2026-08-17 | v1 创建：notes 口语化 → TTS → 字幕派生 → HyperFrames Composition → 渲染验证；Audio-First 与禁止多级 xfade 链 | 用户指令；27 页 deck → 859.7s 成片实测 |
| 2026-08-19 | v2.0：重构为 Composition Timing & Render Workflow；删除视频阶段 Notes 改写和截图 Composition，新增 Validate、Audio Alignment、Timing Compile、HyperFrames Render、分层 QA 与确定性编译产物 | 用户重构 Spec；HyperFrames-native Finance Presentation 契约 |
| 2026-08-19 | v2.1：明确 HyperFrames 是统一 Video Runtime，统一承载 Composition、Scene/Sub-composition、动画、视觉媒体、音频轨道、字幕与确定性执行；外部 Skill 限定为高质量 TTS 与已知文本 Forced Alignment 等补足能力 | 用户架构边界补充 |
| 2026-08-19 | v2.2：区分 Presentation Composition Skeleton 与 Timing Compile 后的 Final Composition；将 One Scene, One Composition 改为 Scene-oriented Composition，并新增 HyperFrames Capability Adoption 优先级 | 用户架构顺序、Scene 粒度与能力演进补充 |
