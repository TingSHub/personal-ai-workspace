# finance-resentation-agent

> 管理资产：`.ai/agents/finance-resentation-agent/finance-resentation-agent.md`；实体定义：`.agents/finance-resentation-agent.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | agent |
| 来源 | internal · workspace local agent prompt |
| installed_ref | Finance Presentation Agent v0.4 · sha256:22eb057b19ae867f8b44b02f6f8ba2cba0e3f9bb4dbb777a111ec2def590987b |
| runtime | both |
| 调用入口 | 按 Workflow Required Resources 的 by-name `finance-resentation-agent` 调用；加载实体定义执行 |
| 要求 | 已验收 Editorial Master、Editorial Pitch 与冲突/来源记录；hyperframes；html-ppt-skill；static-html-qa；Node/npx、浏览器/Playwright、FFmpeg 渲染环境 |
| 更新 | manual · 修改顶层实体定义后同步 installed_ref；验证：加载 Agent，生成最小 HyperFrames-native Scene/Notes/Reveal HTML，运行 HyperFrames check/snapshot 与语义、数值、HTML QA |
| 辅助脚本 | — |
| 经验引用 | html-ppt-longform-report；presenter-notes-verification；narration-content-lock；multi-source-conflict-check |

## 作用

财经内容视觉导演 Agent：把 Financial Editor 已经讲清楚的企业研究母稿，转化为适合“看、听、逐步理解”的 HyperFrames-native HTML Presentation，并同步生成 Scene Visuals、Composition Structure、Reveal Cues、Final Speaker Notes 与来源锚点，使同一套 Scene 能直接进入视频生产。

## 实体位置

- `.agents/finance-resentation-agent.md`——完整职责、内容边界、Scene/Core Message、Visual Evidence、Notes/Reveal、HyperFrames Composition、输出契约和质量门禁。

## 调用方式

- 输入：已验收 Editorial Master、Editorial Pitch、冲突裁决与必要来源材料。
- 先识别 Editorial Thesis 和 Narrative Arc，再拆分 Scene、确定 Core Message、选择 Visual Evidence、完成 Oral Adaptation，设计 Notes 与 Reveal Semantics。
- 必须从生成阶段调用 `hyperframes`，输出满足 Composition contract 的 HTML；每个 Scene 包含稳定的 Scene/Composition ID、语义一致的 Visual DOM/SVG、`data-cue`、seek-safe 动画语义和 `<aside class="notes">` Final Speaker Notes。
- Preview、Presenter 与 Video 共用同一套 Scene DOM/SVG；Scene duration、start 和 cue timestamps 留给后续 Timing Compile，不在本阶段伪造真实秒数。
- 下游只消费已锁定的 Final Speaker Notes 做 TTS/Alignment；视频 Workflow 不得重新润色或改写 Notes。

## 注意事项与踩坑

- **内容事实源**：Editorial Master 决定事实、数字、因果、Thesis、反证和不确定性；Presentation Agent 不自行重做研究或提高结论强度。
- **Scene First**：章节不等于页面；每个 Scene 只承载一个主要 Core Message。
- **Presentation Completeness**：压缩文字和次要证据，不压缩关键认知过程；重要背景、机制、比较、反证和意义需要多少 Scene，就给多少 Scene。
- **选择而非转录**：优先 1 个主证据、必要时 1–2 个辅助证据；不把研究表和 Evidence Notes 原样搬上页面。
- **Visual / Notes 对齐**：重要口播必须有视觉锚点；Notes 与画面一起设计，并作为 TTS 唯一文本事实源。
- **Reveal 语义**：动画表达认知顺序，不硬编码真实秒数，不做纯装饰动画。
- **Reveal 边界**：Reveal 只展开同一个认知模型，不得作为减少 Scene 数量、合并多个独立机制或比较的工具。
- **HyperFrames-native**：HTML 从生成开始同时是 Presentation 与 Video Composition；不得另做一套 Video HTML，也不得使用 wall-clock、随机数、无限动画或截图后模拟 Reveal。
- **确定性状态**：优先使用 HyperFrames 支持的 paused、seek-safe timeline；Scene / Composition / Cue ID 必须唯一稳定，任意 seek 状态应可复现。
- **Notes 锁定**：`<aside class="notes">` 是 Final Speaker Script 和 TTS 唯一文本 Source of Truth；Presentation Agent 在本阶段完成 Oral Adaptation，后续视频流程只做技术性 TTS/Alignment。
- **投资边界**：视觉、标题、Notes 与动画不得新增目标价、评级、买卖建议、仓位、策略或交易信号。
- **来源与 QA**：关键事实保留轻量来源锚点；交付前必须完成 Semantic QA、HyperFrames Composition QA、内容边界、数值一致性、必要的 snapshot/render 和多视口 HTML QA。
- **范围控制**：不修改 Editorial Master 核心内容，不替代 Financial Editor、Research Agent 或 Audio Timing；负责把内容交付为可被 HyperFrames 确定性渲染的视觉结构。

## 回写条目

- 2026-08-18：实体文档轻度压缩并规范 Markdown；保留 Editorial Master 边界、Scene/Core Message、Visual Evidence、Notes/Reveal、Presentation Handoff 和 QA 契约。
- 2026-08-18：v0.3 增加 Presentation Completeness Principle，明确关键认知步骤优先于 Scene 数量，Reveal 不替代必要 Scene。
- 2026-08-19：v0.4 整合 HyperFrames-native Composition、共享 Scene DOM、Final Speaker Notes 锁定、Reveal Semantics 与 Composition QA；明确 Presentation Agent 在生成阶段完成 Oral Adaptation，后续视频流程不改写 Notes。
