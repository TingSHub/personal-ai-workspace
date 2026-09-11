# Workflow: investment-research-video-create

> 位置: Project: projects/investment-research-video/workflows/investment-research-video-create/

## Mission

财经视频整支生产的单入口编排：按「复盘 → 选题 → 研究 → 表达 → 制作发布 → 复盘闭环」串联本项目子 Workflow。本 Workflow 只编排顺序与进入条件，不复制子 Workflow 的资源表、产物路径或质量门禁——各子 Workflow 的 SOP 是其唯一事实源。

## Input

- 账号 profile、目标平台、目标时长、画幅和可用制作资源；
- 用户给定主题、候选主题或允许自主选题的边界；
- `account-profile/published-works.md` 中待复盘作品及其 review status；
- 研究来源访问边界和真实发布授权状态。

## Output

从获批 topic card、冻结研究包、锁定表达包到最终视频、横竖封面、发布包和复盘记录的完整项目交付链。正式路径分别由各 Child Workflow 的 SOP 定义，本编排 Workflow 不创建平行副本。

## Principles

- by-name 引用：阶段只引用 Workflow 名称，不复制子 SOP 内容
- 只编排顺序：父不复制子 Workflow 的 Required Resources、产物路径与质量门禁
- 行 3–5 由父路由 `investagent-podcast-video-by-hyperframes` 按其 SOP 的交接契约（事实层 → 表达层 → 执行层）串联执行
- 有待复盘视频时从行 1 开始；无待复盘时从行 2 开始

## Phase 1: end-to-end-orchestration — 整支视频编排

### Goal

按进入条件依次执行复盘、选题、研究、表达、制作发布和发布后复盘；每一步只消费已通过子 Workflow 门禁的上游产物。

### Child Workflow

| # | 阶段 | Workflow（by-name） | 进入条件/说明 |
|---|---|---|---|
| 1 | 复盘 | `publish-review` | 有待复盘视频（见 `account-profile/published-works.md` 各条目的 `review_status`）时先复盘 |
| 2 | 话题采集 | `topic-forward-lead` | 唯一选题入口，产出获批 topic card |
| 3 | 话题研究 | `topic-research` | 行 3–5 由父路由 `investagent-podcast-video-by-hyperframes` 按事实层→表达层→执行层顺序执行 |
| 4 | 表达 | `investagent-content-expression` | 同上 |
| 5 | 制作与发布 | `investagent-video-execution` | 同上 |
| 6 | 复盘闭环 | `publish-review` | 发布后按 T+1/T+3/T+7 复盘，回到行 1 |

### Input

本 Workflow 的启动输入，以及上一行 Child Workflow 已验收的正式产物。

### Output

各 Child Workflow 在其 SOP 约定路径留下的正式产物和独立执行回执；最终交付为已通过 QA 的成片与发布包，发布后进入复盘册。

### Quality Criteria

- 所有 Child Workflow 均按 by-name 解析并真实执行；
- 行 3-5 只通过 `investagent-podcast-video-by-hyperframes` 的事实层、表达层和执行层交接，不平行重跑；
- 任一子 Workflow 未通过门禁时停留在对应层返修，不允许下游绕过；
- 未获得发布授权时只生成发布草稿，不创建伪发布结果；
- 发布后真实作品链接和 T+1/T+3/T+7 状态已写入复盘册。

### Known Issues

平台统计可能延迟，发布后复盘允许按时间窗口等待；等待不影响本期成片交付状态。研究改变主体或主问题时返回 `topic-forward-lead`，表达和制作问题不得借此静默改题。
