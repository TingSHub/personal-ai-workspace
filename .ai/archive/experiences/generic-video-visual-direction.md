---
name: generic-video-visual-direction
description: 当 HyperFrames 视频出现静态 deck、拥挤目录或空白结尾时，用 scene manifest、数据动效、紧凑导航和开场 canary 建立通用视觉质量门禁
type: quality-check
status: archived
owner: investagent-podcast-video-by-hyperframes, hyperframes
asset: investagent-podcast-video-by-hyperframes, hyperframes, hyperframes-animation, hyperframes-creative
tags: [video, hyperframes, visual-direction, motion, quality-gate]
---

# Experience: generic-video-visual-direction

## 来源证据

- 项目：`investment-research-video`，东山精密 run `2026-08-23`。
- 产物：`outputs/companies/东山精密/2026-08-23/podcast/visual-plan/scene-manifest.json`、`podcast/project/`、`podcast/opening-test-v4/`。
- 验证：HyperFrames Composition check `ok=True`，runtime errors `0`，layout errors `0`；opening canary `37.066667s`，同时包含 video/audio stream；animation map 记录 `75` 个 tweens。
- 相关资源 installed_ref：`hyperframes` `c32b804`；`hyperframes-animation` 与 `hyperframes-creative` 随 HyperFrames 资源执行。

## 触发场景

- 视频可以渲染，但每个话题只有一张静态页，数据没有变化过程。
- 目录文字挤成一排或长问题被压缩成同尺寸胶囊。
- 结尾只剩空白画面，没有总结性的视觉资产。
- 长片渲染成本较高，需要先快速判断开场是否成立。

## 问题与归属判定

- 问题：仅依赖生成器和默认审美会把研究视频做成静态 deck；技术 check 通过不等于视觉叙事成立。
- 归属（owner）：`investagent-podcast-video-by-hyperframes` Phase 4/5 的视觉质量标准，以及 `hyperframes` 资源记录的调用注意事项。

## 可复用结论（resolution）

1. Composition 生成前必须有公司无关的 `scene-manifest.json`：每个核心话题至少声明立题、数据变化、机制/限制、验证收束四类 beat；数据图至少绑定一种 seek-safe 动效（数字滚动、柱体生长、曲线绘制、瀑布展开、节点出现或重点标注）。
2. 目录使用紧凑章节网格或分组导航，只显示 manifest 的短标签；完整问题留给口播和字幕，不把长文本堆成胶囊。
3. OUTRO/SUMMARY 必须输出验证看板、三道门、结论矩阵或指标卡，并绑定 manifest 的收束文字；空白结尾不能通过视觉门禁。
4. 先用 `animation-map` 检查开场、目录、核心话题和结尾，再抓 snapshots；长片渲染前运行 `build_opening_canary.py` 生成 `COLD_OPEN + INTRO` 短片做视觉审阅。
5. 视觉验收同时看技术证据和人工观感：`check` 负责确定性、媒体流和布局，snapshot/canary 负责判断节奏、层级、数字是否真的被看见。

## 回写目标

- 已回写：`investagent-podcast-video-by-hyperframes` Phase 4/5 Required Resources、Quality Criteria 和 Output。
- 已回写：`hyperframes` 资源记录的经验引用。

## 适用范围

公司研究、财经播客、数据解读和其他使用 HyperFrames 的参数化视频；适用于短开场回归和完整长片渲染。

## 不适用范围

纯静态海报、没有数据叙事的片头片尾，或用户明确要求静态 slide 展示的交付物；不以动效数量替代内容证据和音频时间轴。

## 关联资产

`investagent-podcast-video-by-hyperframes`、`hyperframes`、`hyperframes-animation`、`hyperframes-creative`
