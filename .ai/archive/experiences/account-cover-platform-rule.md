---
name: account-cover-platform-rule
description: 米白账本风格平台封面的固定规范与踩坑——全角行尾标点「？/！」在 Noto Serif SC Bold 中墨迹仅占字身左半需 .qm 负外边距补偿、单 Bold 字重要靠 stroke 合成加粗、横版导出必须 ?format=landscape 且元素全幅截图、验收判据为墨迹中心对齐画布中心 ±3px
type: methodology
status: archived
owner: account-profile-design, account-cover-reference
asset: investagent-podcast-video-by-hyperframes, account-profile-design, account-cover-reference
tags: [封面规范, cover, 字体坑, font-pitfall, playwright, 验收判据]
---

# Experience: account-cover-platform-rule

> Experience 是反馈，不是永久知识库：合格经验先判定归属，回写至 Workflow SOP 或 Skill/Agent 记录（by-name 回填 `experience_refs[]`），**回写完成后归档**至 `.ai/archive/experiences/`；`.ai/experiences/` 只存未完成回写的在途经验，不无限堆积。
> frontmatter 是机器检索层（name/type/status/owner/asset/tags 供 LLM 精确过滤），正文是人读细节；两者以正文为准。

## 来源证据

2026-09-05 数据基础设施封面任务（outputs/companies/数据基础设施/2026-09-05/podcast/project/）：
- 居中诊断：Playwright DOM（Range ink + getComputedStyle）+ 元素截图 numpy 像素分析证明——`.headline` 盒子（width 880/760 + margin auto）与 text-align:center 均生效，墨迹错位来自「真订单？」行尾全角「？」（U+FF1F）：Noto Serif SC Bold 中字身 advance 182px，但墨迹仅 -3..85px（左 48%），右约 0.51em 空字身；text-align:center 按完整字身居中 → 墨迹视觉左偏约 48px（两行错位 44px，诊断时 182px 字号）。
- 修复验证：`<span class="qm">？</span>` + `margin-right:-0.521em` 后两行墨迹中心 536 / 539.5（画布中心 540）；参考封面（1086×1448）对标：字号 182→212px、墨迹高度 168→199/201（参考 204/207）、酒红行密度 0.326（参考 0.32）。
- 渲染管线：render_cover_4x3.js 原来不激活 `?format=landscape`（横版导出呈现竖版布局）；两脚本原来整页截图（含工具栏与缩放留白）。修复后 element 截图 #cover 原生 1440×1080 / 1080×1440。

## 触发场景

任何「账本两面」账户封面（或同风格封面）的生成、调整、排障；修复后对齐参考封面比例；使用 render_cover_3x4/4x3.js 导出 PNG。

## 问题与归属判定

- 问题：CJK 行尾全角标点的字身/墨迹差在 text-align:center 下造成"版面偏移"假象；单 Bold 字重无法实现"更粗"；横版导出布局错配。
- 归属（owner）：`account-profile/design.md` 增加「平台封面规范」章节（固定规范 + 内容边界 + 创意边界）；脚本侧已固化在 `scripts/render_cover_3x4.js` / `render_cover_4x3.js`（workflow by-name 引用）与 `scripts/build_podcast_composition.py`（.qm 自动包裹 + `.title .qm` 规则）。

## 可复用结论（resolution）

1. 全角行尾「？/！」包 `<span class="qm">` + `margin-right:-0.521em`（Noto Serif SC Bold 实测；换字体/字重需按"墨迹中心=画布中心"重校准）。注意选择器必须压过 `.headline span` 的 `width:100%` 污染：`.headline span.qm{display:inline-block;width:auto;...}`。
2. 字重合成：仅有 Bold 字重文件时，`-webkit-text-stroke:1.5px`（主行）/`3px`（accent）近似 Black 900；引入 NotoSerifSC-Black 后移除 stroke 直接 font-weight:900。
3. 渲染管线：横版必须 `?format=landscape`（激活 .landscape 布局）；导出用 element 截图（非整页），先等 `document.fonts.ready` + 图片 decode；导出前调用 `transform:none!important` 抵消预览缩放。
4. 验收判据：PNG 尺寸必须 1440×1080 / 1080×1440；标题墨迹中心与画布中心偏差 ≤3px；墨迹密度对齐参考封面（±0.01）。
5. 参考封面本身就是"账户风格事实源"：米白羊皮纸账本背景 + 两侧 154px 细线边栏 + 黑红折页 logo + 大字两行（墨黑 + 暗酒红 #781923）+ 分类/底部细则；该风格已被用户确认为后续所有视频封面固定风格（允许换背景图与创意变体，但 token 与内容边界不变）。

## 回写目标

- `account-profile-design`：design.md 新增「平台封面规范」章节（本经验回写落地处）
- `investagent-podcast-video-by-hyperframes`：workflow.md / global-contract.md 平台封面小节继续 by-name 引用同一规范（既有分支修改已扩写，无需再改）

## 适用范围

账本两面账户的投资研究视频平台封面（竖版 3:4 + 横版 4:3）；字体 NotoSerifSC-Regular/Bold（SIL OFL，已附 LICENSE）；Chromium/Playwright 1.62。2026-09-05 发布日期版。
