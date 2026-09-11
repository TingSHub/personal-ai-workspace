# 账本两面 v1 Design Tokens

```yaml
canvas: 1920x1080
visual_style: 'editorial-paper'
background: '#faf7f1'
surface: '#fffdf8'
ink: '#211d18'
ink_secondary: '#6a6354'
accent_red: '#a6192e'
growth_green: '#1e6b4c'
neutral_amber: '#8a5e15'
hairline: '#e7e0d2'
card_radius: 2px
content_density: mobile-first
speaker_pills: false
topic_navigation: true
visual_priority: chart > table > text
font_display_resource: 'font.noto-serif-sc'
font_candidate_resource: 'font.zhuque-fangsong'
font_license: 'SIL Open Font License 1.1; retain LICENSE with asset'
font_fallback: 'Source Han Serif SC, Songti SC, serif'
font_body: 'Noto Sans SC, Source Han Sans SC, Microsoft YaHei, sans-serif'
persistent_navigator: true
persistent_navigator_background: 'transparent'
persistent_navigator_blur: true
persistent_progress_height: 2px
persistent_progress_opacity: 1
```

## Mobile-first readability gate

- The video remains 1920×1080, but composition decisions are made for phone viewing at fitted width.
- Do not force every topic into three cards. A topic with a valid chart uses a chart-first scene; card count is data-driven and may be zero, one, two or three.
- A chart is the main visual for the full evidence-explanation segment. It must not be reduced to a small footer panel beneath cards.
- Important text must be legible without pausing or zooming: topic headlines, chart titles, chart labels, values and current-turn subtitles all use video-sized type. Decorative metadata and navigation may be smaller, but cannot compete with or replace the evidence.
- `scripts/check_mobile_legibility.py` is a static gate. A final run also requires rendered screenshot inspection at phone-fitted scale; clipping, overlap, or unreadable labels fails the gate.

## Component contract

- `ShowHeader(company, showName, disclaimer)`
- `SpeakerPill(speaker, active)`
- `TopicTitle(index, question)`
- `MetricCard(color, label, value, explanation)` — only when the evidence needs a metric card; never pad the layout with empty cards
- `ChartFrame(type, claim, data, source_ids)`
- `AgendaStrip(items)`
- `TableFallback(rows, unit)`
- `OwnershipRoute(steps)`
- `SubtitleRail(text, speaker)`
- `TopicNavigation(topics, activeTopicId)`
- `PersistentNavigator(chapters, activeChapterId, elapsed, total)` — root-level overlay, independent from page scenes

Each component is driven by account/episode data, not by company-specific selectors or hardcoded text. If a claim has a valid chart spec, render a chart first; use a table only when the relationship is not chartable; use text only for context, caveats and conclusions. The persistent navigator is a root-level layer and must remain visible while page scenes change.

## Visual reference and motion grammar

- 视觉稿是账号级参考，不是每期生产文件。当前参考 `account-motion-study-v1`：<https://www.figma.com/design/T7XPzbAjUpUgsFSejr7BJP>。它用于统一时间区间图、机制拆解和场景衔接的构图方向，不作为待逐帧复刻的成片模板。
- 日常视频从本文件的 token、组件契约和已验证的 HyperFrames 模式直接生成。只有新增一种视觉关系或整体品牌改版时，才补一张参考画面；在同一 Figma 文件内新增 frame，不新建一期一文件。
- 一段讲解应保持一个主视觉，并通过 `scene-manifest.json` 的 `states` 推进：建立对象、揭示数据、连接关系、突出比较、显示反证、收束判断。标题入场和持续背景运动不能代替这些变化。
- 图表几何必须表达数据关系：区间使用上下界，哑铃使用两端与连接差距，发散图共享零线，瀑布图表达累计起终点，系列比较共享可比尺度。组件名称不能替代语义验证。
- 主衔接优先延续上一场的位置、颜色和运动方向；基础生成器使用定向推移、焦点转移、交叉淡化或硬切。更复杂的共享元素或遮罩转场只有专用 Composition 已实现并通过代表段验收后才能启用。音效只绑定关键状态或换章事件，保持少量、短促且不遮挡旁白。

默认视觉旋钮为 `design_variance=6`、`motion_intensity=6`、`visual_density=5`。每期可因题型调整一档，但必须在 scene manifest 中记录；财经可信度、证据清晰度和手机可读性优先于风格强度。

### 场景语法

| 语法 | 观众认知变化 | 首选状态动作 | 典型视觉对象 |
|---|---|---|---|
| `thesis-reveal` | 从问题进入本期唯一判断 | establish → resolve | 冲突标题、关键数字、结论锚点 |
| `evidence-compare` | 看清共同尺度下的差异 | establish → reveal → compare | 条形、哑铃、区间、同轴折线 |
| `mechanism-chain` | 理解原因如何传导到结果 | establish → connect → resolve | 节点、路径、因果回路 |
| `timeline-shift` | 理解事实、预期和价格的先后 | establish → reveal → connect | 时间轴、阶梯线、事件落点 |
| `counterevidence-challenge` | 看到主判断最强反证与边界 | establish → challenge → resolve | 对照层、风险矩阵、证伪条件 |
| `closing-synthesis` | 把分散证据重组为结论 | reveal → compare → resolve | 前文共享对象、结论与推翻条件 |

- 每个 scene 明确 `viewer_question`、`cognitive_change` 和 `continuity_anchor`；缺少认知变化时不进入视觉制作。
- 连续三个 scene 不得复用同一布局族；一个 scene 有三个及以上 state 时不得只有一种动作。
- 背景动势、标题入场和进度条属于支持层，不计入语义 state。每个承担解释的 scene 至少有一次数据、关系、边界或焦点的真实变化。
- `establish` 建立对象，`reveal` 揭示信息，`connect` 形成关系，`compare` 建立共同尺度，`challenge` 引入反证，`resolve` 收束焦点。动作名称必须对应实际几何或视觉变化。

## 平台封面规范（account-fixed, by-name: `account-cover-reference`）

封面是独立平台资产，不属于正片 timeline；固定参考资产与模板见 `account-cover-reference`（`account-profile/cover-reference/`），风格事实源为 `reference-3x4.png`。后续视频封面均按此规则生成，允许 token 内的创意变体，不允许跳出边界。

### 画布与结构

- 竖向 3:4 = 1080×1440（mobile 缩略图）；横向 4:3 = 1440×1080。导出必须是元素全幅 PNG（尺寸精确匹配）。
- 结构自上而下：品牌区（黑红折页 logo + 「账本两面」+ 「看懂数字背后的公司」标签 + 细分隔线）→ 公司行（subject，字号 37px）→ 大字标题两行（墨黑行 + 暗酒红 accent 行）→ 分类行（如「数据基础设施观察」）→ 底部值（如「从订单到现金，逐层验证」）；两侧 154px 账本细线边栏 + 侧注（财报/订单/现金流/产业 · 数据/市场/公司/价值）。
- 背景：米白羊皮纸账本摄影（`assets/background-portrait.png` / `background-landscape.png`），照片子元素（纸、钢笔、酒红折纸）作为氛围层。

### 排版 token

- 字体：Noto Serif SC Bold（`font.noto-serif-sc` 资源，随封面复制 `assets/fonts/NotoSerifSC-{Regular,Bold}.otf`）；ink `#201f1d`，wine `#781923`，paper `#f4eee3`。
- 大字：容器 880px 水平居中，font-size 212px（竖向）/ 163px（横向单行），line-height 1，letter-spacing 4px；主行 `-webkit-text-stroke:1.5px currentColor`、accent 3px（账户仅有 Bold 字重，用 stroke 合成加粗；引入 Black/900 后改回 `font-weight:900` 并删除 stroke）。
- **行尾全角标点规则**：Noto Serif SC Bold 中「？/！」（U+FF1F/FF01）字身宽为全角（≈182px@212px）但墨迹只画在左侧约 0.48em、右侧 0.51em 空字身；text-align:center 按完整字身居中会让整行墨迹视觉左偏 40-50px。必须把行尾标点包进 `<span class="qm">` 并使用 `.headline span.qm{display:inline-block;width:auto;margin-right:-0.521em}`（选择器需压过 `.headline span` 的 `width:100%`；换字体/字重按「墨迹中心=画布中心」重校准）。生成的 cover.html 由 `scripts/build_podcast_composition.py` 自动包裹。

### 内容边界

- 数据唯一来源：`episode-input.json` 的 `cover.title` / `cover.subtitle` / `cover.subject_label` / `cover.large_text`；缺失时 Phase 2 失败，不从历史补值。
- 至多一个冲突主标题 + 一个必要辅助标签；禁止日期、免责声明、研究编号、不可读小字进缩略图；禁止亮红/黄色投流风格、纯色铺底、无语义几何装饰、反色 Logo。
- 创意允许范围：同风格背景摄影替代、纸章/imprint 微调、大字关键词化；保持 `.headline` 两行结构与 token 色相不变。

### 渲染与验收（脚本已固化）

- `scripts/render_cover_4x3.js`（必须带 `?format=landscape` 激活横版布局）→ `cover.png`；`scripts/render_cover_3x4.js` → `cover-3x4.png`；两者均为 `#cover` 元素全幅截图并等待 `document.fonts.ready` + 图片 decode。
- 验收判据：尺寸 1440×1080 / 1080×1440；标题墨迹中心与画布中心偏差 ≤3px；墨迹高度/密度对齐 `reference-3x4.png`（±0.01）。仅生成 cover.html 不算完成。
