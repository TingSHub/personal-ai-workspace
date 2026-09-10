# 复盘与选题前瞻

对已发布视频做标准化复盘，并从事件、产业、公司实力、观众问题及可选行情线索生成下一批选题。选题先按 `market_pulse`、`earnings_gap`、`company_industry`、`valuation_mechanism` 四条内容主线分流，再生成候选卡。复盘只提供带适用条件的假设；用户批准的 topic card 先进入 `topic-research`，研究验收后再进入视频生产。

> 本模块原为独立项目 `video-publish-review`，v0.2.4 起并入本项目：Workflow 位于 `workflows/publish-review/` 与 `workflows/topic-forward-lead/`，复盘与选题产物位于本项目 `outputs/`。

## Goal

让账号逐步积累可复用经验，同时保留新选题的自由度：按曝光 → 点击/播放 → 2 秒/5 秒 → 平均观看/完播 → 互动 → 主页访问 → 关注诊断增长漏斗；指标定位现象，内容证据支持归因，单条复盘形成待验证假设，新视频按适用条件选择零或一个主要内容实验。

## Workflows

- publish-review（发布后数据复盘与改进候选，位于 `workflows/publish-review/workflow.md`）
- topic-forward-lead（唯一选题入口：问题发现、轻量核验、增长契约与一次用户审批，位于 `workflows/topic-forward-lead/workflow.md`）

## 依赖资源

- douyin-creator-tools（登录态官方导出 + 解析 + 详情页补充采集 + 评论导出）
- experience-curator（回写判定）
- boundary-rewrite（改进项中争议性表达的合规改写）
- video-hook-intro（改进项的钩子设计参考）
- topic-forward-signal-scanner（选题前瞻的免费市场信号扫描）

## 复盘成果组织

- 每支已发布视频一个独立文件夹：`outputs/retrospectives/<published_date>-<slug>/`
  - `README.md` — 视频身份与复盘状态
  - `metrics-snapshot-YYYY-MM-DD.json` — 每次采集一个快照
  - `attribution-YYYY-MM-DD.md` — 归因报告（T+3 初版，T+7 增量更新终版）
- 每期选题前瞻一个日期文件夹：`outputs/topic-forward/<YYYY-MM-DD>/`，包含 `topic-forward.md`（阅读视图）、`topic-forward.json`（结构化事实源）、`signals.json` 与候选池产物
- 生命周期与复盘进度（已发布视频、复盘册指针、T+1/T+3/T+7 状态与待补队列）：以 `account-profile/published-works.md` 各条目的 `review_status` 与 `review_dir` 为唯一事实源；本文件不维护重复清单。
- 选题前瞻：2026-09-09-run-01 的 `TOPIC-R3-*` 批次中 `TOPIC-R3-06` 已交付；其余 11 张仍为 `card`；`2026-09-08-rerun-01` 的 `TOPIC-R2-*` 批次为历史 pending，不与本轮混用

## 目录说明

- `workflows/publish-review/`、`workflows/topic-forward-lead/`：本模块的工作流 SOP。
- `outputs/account-rules.md`：账号级规律库。
- `outputs/retrospectives/<date>-<slug>/`：每支已发布视频的复盘册。
- `outputs/topic-forward/<date>/`：选题前瞻按日期归档，包含 `topic-forward.md` 阅读视图、`topic-forward.json` 结构化事实源、`signals.json` 与候选池产物。
- `logs/`：运行日志，只保留项目执行证据。

## 运行规则

- 每支已发布视频一个独立复盘文件夹：`outputs/retrospectives/<published_date>-<slug>/`。
- 已验收的结构化数据 JSON 是流量事实源；归因报告只引用已落盘数据，不引用记忆中的数字。
- 采集通过 `douyin-creator-tools` 登录态自动化完成，遵守低频、不绕风控、失败即停的约束。
- 复盘报告必须显式标注未验证项，并分离事实与推断。
- 不在复盘流程内直接做经验回写；候选经用户确认后交给 `experience-curator`。
- 字段清单一律从 workspace 的 `.ai/templates/` 读取。
- 项目执行记录写入 `logs/`，不直接进入资产库。

## 必要资源

- `douyin-creator-tools`：数据采集（publish-review P1/P2，必选）
- `topic-forward-lead`：下一条视频的唯一选题入口，批准后移交 `topic-research`（必选）
- `topic-angle-router-agent`：将 discovery seed 拆成互斥内容主线，并绑定表达 Agent（必选）
- `experience-curator`：用户确认后的 workspace 经验回写（publish-review P7，条件使用）
- `boundary-rewrite`：争议性表达合规改写（可选）
- `video-hook-intro`：改进项的钩子设计参考（可选）
- `topic-forward-signal-scanner`：选题前瞻的免费市场信号扫描

## 已知限制

当前可稳定生成官方详情导出 JSON 及其原始 Excel，覆盖内容吸引力、观众参与度、流量来源、观众分析；章节点击率、搜索关键词、留存曲线等按需通过详情页补充采集，中段流失定位仍依赖原视频对齐。归因、候选、规律库分别是后续条件产物，不要求每次都生成。
