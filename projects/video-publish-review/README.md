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
