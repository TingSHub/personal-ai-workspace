---
name: podcast-composition-input-contract
description: 用 build_podcast_composition.py 生成播客合成时，episode/cover 的四个结构约束不满足会崩溃或静默产出空白图表区；按契约填输入即可一次通过
type: resource-lesson
status: archived
owner: investagent-podcast-video-by-hyperframes
asset: investagent-podcast-video-by-hyperframes
tags: [podcast, hyperframes, composition, chart, input-contract]
---

# Experience: podcast-composition-input-contract

> Experience 是反馈，不是永久知识库：合格经验先判定归属，回写至 Workflow SOP 或 Skill/Agent 记录（by-name 回填 `experience_refs[]`），**回写完成后归档**至 `.ai/archive/experiences/`；`.ai/experiences/` 只存未完成回写的在途经验，不无限堆积。
> frontmatter 是机器检索层（name/type/status/owner/asset/tags 供 LLM 精确过滤），正文是人读细节；两者以正文为准。

## 来源证据

- 项目：`projects/investment-research-video`，厄尔尼诺农业行情（2026-09-10）真实成片。
- 证据：`outputs/subjects/厄尔尼诺农业行情/2026-09-10/podcast/phase2-execution.md`、`podcast/qa/episode-qa.md`；首轮成片图表区空白，修正后重渲才通过。
- 验证时资源：`build_podcast_composition.py`（项目脚本）、`hyperframes` 0.8.33、`check_podcast_visual_sync.py`。

## 触发场景

用 `build_podcast_composition.py` 从 episode + segments + chart-spec + visual-plan 生成 HyperFrames 合成时。

## 问题与归属判定

- 问题：输入 JSON 的四个结构约束不满足时，脚本要么抛 `TypeError/AttributeError/ValueError`，要么**静默产出空白图表区且 `hyperframes check` 不报错**——后者最危险，会渲染出一条内容缺失的成片。
- 归属（owner）：项目运行契约，回写 `investagent-podcast-video-by-hyperframes` 的 Phase 3 Known Issues。

## 可复用结论（resolution）

1. `episode.topics` 必须是**对象列表**（含 `topic_id`/`title`/`claim`/`metrics`），不能是字符串列表；`metrics` 元素形如 `{label, display_value, display_desc, color}`。
2. `episode.opening_visual` 必须是**对象**（`headline`/`subheadline`/`cards`），不能是字符串；COLD_OPEN 场景读它取标题与卡片。
3. `episode.outro_summary` 必须是**对象列表**（`{label, headline, detail}`），字符串列表会在 `summary_markup` 抛 `too many values to unpack`。
4. `cover.large_text` 用 `\n` 分行，每行 ≤4 字（212px 字号下 880px 容器上限），第二行自动加 accent 酒红样式；单行标题不符合 `design.md` 的两行结构要求。
5. **图表类型必须落在渲染器白名单内**：`dumbbell`/`diverging-bar`/`horizontal-bar`/`bar`/`line`/`multiline`/`step-line`/`waterfall`/`stacked-bar`，以及映射型 `flow→flow-map`、`checklist/progression/funnel/milestone→validation-dashboard`。**`compare`/`timeline` 不在白名单**，会产出空白图表区且门禁不报错。
6. 多步图（`line`/`multiline`/`step-line`/`flow`/`checklist`/`validation-dashboard`）必须补 `narration_beats`（≥2 条，绑定同 topic 的真实 turn 且带 `reveal`），否则 `check_podcast_visual_sync.py` FAIL。
7. 合成产物的 `index.html` 与 `assets/` 必须同目录（相对路径 `assets/...`），否则 `hyperframes check` 报 `audio_src_not_found` / `missing_local_asset`。

## 回写目标

`investagent-podcast-video-by-hyperframes` 的 Phase 3 Known Issues（已合并，不新增章节）。

## 适用范围

`build_podcast_composition.py` 当前版本 + HyperFrames 0.8.x；`editorial-paper` 与 `default` 两种 style 均适用。

## 不适用范围

不适用于其他合成器或手写 Composition；白名单随脚本更新可能变化，改脚本后应重新核对而非套用本条。

## 关联资产

`investagent-podcast-video-by-hyperframes`、`hyperframes`、`hyperframes-cli`
