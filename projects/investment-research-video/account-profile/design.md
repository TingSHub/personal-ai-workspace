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
