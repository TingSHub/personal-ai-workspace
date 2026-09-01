# Experience: narration-content-lock

## 来源证据

- 项目：investment-research-html-mvp（2026-08-16，Content Lock 落地：deck HTML 含 CONTENT LOCK 标记）
- 运行记录：`logs/run-20260816-workflow-v1.md`（SOP v0.1.4）
- 相关资源 installed_ref：html-ppt-skill（f3a8435）

## 触发场景

- 口播内容（speaker script/notes）进入 TTS/视频制作前需要锁定文本时
- 多环节接力（规划 → 口语化 → TTS → 字幕）中防止文本被多次改写漂移

## 问题与归属判定

- 问题：口播文本经 TTS、字幕、视频多环节接力时，若每环节都"顺手改写"，最终文本与页面/研究事实脱节；字幕另写一套文案会与旁白不一致（用户原则：字幕由旁白派生）。
- 归属（owner）：investagent-html-report-v0.1 workflow SOP（P3 Content Lock 原则）；html-ppt-skill 记录（notes 作为 speaker script 的锁定语义）

## 可复用结论（resolution）

- **每页 `<aside class="notes">` 是该页最终口播文本的唯一 Source of Truth**（deck HTML 落 CONTENT LOCK 标记，锁定日期记录）。
- 口语化/数字读法/缩写展开/句长与停顿优化**直接更新 notes**——TTS 不得另行改写口播内容，只允许不改变语义和文字内容的技术性处理（断句/标点）。
- **字幕由 notes 派生**：可断句但不另写一套文案。
- Speaker Script 与 Slide Visual 保持语义一致：允许 TTS 前独立迭代润色，但修改核心观点或需要新视觉支撑时同步更新 Slide（纯表达层修改无需）。
- 锁定后回归验证：`static-html-qa/scripts/check-notes-presenter.py`（S 键 presenter 窗口抽查期望片段）。

## 回写目标

- investagent-html-report-v0.1 workflow SOP P3（Content Lock 已随 v0.1.4 写入，本经验作追溯）
- html-ppt-skill 记录注意事项（notes 即最终口播文本 SoT 的语义）

## 适用范围

- 口播 → TTS → 字幕 → 视频的多环节内容链路
- 需要"单一事实源 + 锁定"的内容交付流程

## 不适用范围

- 无 TTS/视频环节的纯阅读页面（notes 仅演讲辅助时无需锁定）
- 多语言配音（每语言需独立锁定版本）

## 关联资产

- investagent-html-report-v0.1（Workflow by-name）；static-html-qa（验证脚本归属资源）
