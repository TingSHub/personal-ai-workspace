# video-publish-review

对每支已发布视频做标准化发布复盘，并在复盘末端发现下一支视频的选题与叙事方向。发布复盘和选题前瞻分属两条工作流；叙事架构建议由 `topic-forward-lead` 交给 investment-research-video，并根据复盘与新调研结果选择或调整模板。

## Goal

让"下一支视频"从上一支的真实流量数据中变好：诊断漏斗断点（2s/5s/中段/完播）、用类型校准比率判断内容性质、归因到可修改的内容与发布变量（钩子/中段结构/评论触发器/发布时间），并把结论沉淀为可执行的改进项。

## Resources Used

- douyin-creator-tools（登录态指标导出 + 解析 + 评论导出）
- experience-curator（回写判定）
- boundary-rewrite（改进项中争议性表达的合规改写）
- video-hook-intro（改进项的钩子设计参考）
- topic-forward-signal-scanner（选题前瞻的免费市场信号扫描）

## Workflows

- publish-review（本项目核心 SOP，位于 `workflows/publish-review/workflow.md`）
- topic-forward-lead（选题前瞻：复盘后自动发现下一个视频话题，位于 `workflows/topic-forward-lead/workflow.md`）

## 复盘成果组织

- 每支已发布视频一个独立文件夹：`outputs/retrospectives/<published_date>-<slug>/`
  - `README.md` — 视频身份与复盘状态
  - `metrics-snapshot-YYYY-MM-DD.json` — 每次采集一个快照
  - `attribution-YYYY-MM-DD.md` — 归因报告（T+3 初版，T+7 增量更新终版）
- 每期选题前瞻一个日期文件夹：`outputs/topic-forward/<YYYY-MM-DD>/`，包含 `topic-forward.md` 与 `signals.json`
- 已完成复盘：
  - 2026-08-28 中科曙光（迁移自 investment-research-video，见该文件夹内 README）
- 待复盘队列：
  - 星网锐捷（2026-09-01 发布，T+3 = 2026-09-04 采集）

## 注册位置说明

Skill 资源注册在 workspace 的 `.ai/skills/`（如 `.ai/skills/douyin-creator-tools/`），仅作路径说明，引用一律 by-name。

## Project 运行约束

本目录是 `video-publish-review` 子项目，归属于 workspace 顶层 Git 仓库；不再维护独立的 `AGENTS.md`、`CLAUDE.md` 或 `project.yaml`。本 README 是项目目标、工作流、资源和运行约束的唯一项目说明。

### 项目元数据

- 名称：video-publish-review（视频发布复盘）
- 目标：对每支已发布视频执行“流量数据采集 → 漏斗/比率诊断 → 归因 → 改进项 → 回写判定”，让下一支视频在发布策略与内容结构上可验证地变好。
- 复盘结果按视频独立成册，并沉淀为可跨期对比的账号资产。
- 当前状态：持续维护中。

### 运行规则

- 每支已发布视频一个独立复盘文件夹：`outputs/retrospectives/<published_date>-<slug>/`。
- 数据快照 JSON 是唯一流量事实源；归因报告只引用快照数据，不引用记忆中的数字。
- 采集通过 `douyin-creator-tools` 登录态自动化完成，遵守低频、不绕风控、失败即停的约束。
- 复盘报告必须显式标注未验证项，并分离事实与推断。
- 不在复盘项目内直接做经验回写；候选经用户确认后交给 `experience-curator`。
- 字段清单一律从 workspace 的 `.ai/templates/` 读取。
- 项目执行记录写入 `logs/`，不直接进入资产库。

### 必要资源

- `douyin-creator-tools`：数据采集（publish-review P1，必选）
- `experience-curator`：回写判定（publish-review P5，必选）
- `boundary-rewrite`：争议性表达合规改写（可选）
- `video-hook-intro`：改进项的钩子设计参考（可选）
- `topic-forward-signal-scanner`：选题前瞻的免费市场信号扫描

### 已知限制

官方导出不含单视频留存曲线与观众画像（仅页面可视化），中段流失定位依赖推断；T+7 复采时以人工截图作为兜底。
