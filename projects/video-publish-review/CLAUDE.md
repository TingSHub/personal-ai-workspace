# video-publish-review — Project Context

## Project

video-publish-review（视频发布复盘）

## Goal

对每支已发布视频执行标准化复盘：流量数据采集 → 漏斗/比率诊断 → 归因 → 改进项 → 回写判定，让下一支视频在发布策略与内容结构上可验证地变好。复盘结果按视频独立成册，沉淀为可跨期对比的账号资产。

## Current Status

in_progress

## Workflow

- publish-review（发布复盘标准流程：登记核对 → 采集 → 诊断 → 归因 → 改进项 → 回写判定）

## Required Resources

- douyin-creator-tools（P1 数据采集，必选）
- experience-curator（P5 回写判定，P5 必选）
- boundary-rewrite（P4 改进项中争议性表达的合规改写，可选）
- video-hook-intro（P4 改进项设计的钩子方法参考，可选）

## Development Rules

- 每支已发布视频一个独立复盘文件夹：`outputs/retrospectives/<published_date>-<slug>/`
- 数据快照 JSON 为唯一流量事实源，归因报告只引用快照数据，不引用记忆中的数字
- 采集走 douyin-creator-tools 登录态自动化，遵守其使用约束（低频、不绕风控、失败即停）
- 复盘报告必须显式标注未验证项；推断与事实分离
- 不在复盘项目内做经验回写决策；回写候选经用户确认后交给 experience-curator
- 字段清单一律从 workspace 的 `.ai/templates/` 读取填充
- 项目执行记录写入 `logs/`，不直接进入资产库；项目结束时将可复用候选交给 Experience Curator

## Known Issues

- 官方导出不含单视频留存曲线与观众画像（仅页面可视化），归因的中段流失定位依赖推断；T+7 复采时人工补截图兜底
