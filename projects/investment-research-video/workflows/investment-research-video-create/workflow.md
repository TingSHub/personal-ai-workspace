# Workflow: investment-research-video-create

> 位置: Project: projects/investment-research-video/workflows/investment-research-video-create/

## Mission

财经视频整支生产的单入口编排：按「复盘 → 选题 → 研究 → 表达 → 制作发布 → 复盘闭环」串联本项目子 Workflow。本 Workflow 只编排顺序与进入条件，不复制子 Workflow 的资源表、产物路径或质量门禁——各子 Workflow 的 SOP 是其唯一事实源。

## Principles

- by-name 引用：阶段只引用 Workflow 名称，不复制子 SOP 内容
- 只编排顺序：父不复制子 Workflow 的 Required Resources、产物路径与质量门禁
- 行 3–5 由父路由 `investagent-podcast-video-by-hyperframes` 按其 SOP 的交接契约（事实层 → 表达层 → 执行层）串联执行
- 有待复盘视频时从行 1 开始；无待复盘时从行 2 开始

## 阶段编排

| # | 阶段 | Workflow（by-name） | 进入条件/说明 |
|---|---|---|---|
| 1 | 复盘 | `publish-review` | 有待复盘视频（见 `account-profile/published-works.md` 各条目的 `review_status`）时先复盘 |
| 2 | 话题采集 | `topic-forward-lead` | 唯一选题入口，产出获批 topic card |
| 3 | 话题研究 | `topic-research` | 行 3–5 由父路由 `investagent-podcast-video-by-hyperframes` 按事实层→表达层→执行层顺序执行 |
| 4 | 表达 | `investagent-content-expression` | 同上 |
| 5 | 制作与发布 | `investagent-video-execution` | 同上 |
| 6 | 复盘闭环 | `publish-review` | 发布后按 T+1/T+3/T+7 复盘，回到行 1 |
