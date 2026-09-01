# Investment Research Video — Project Context

## Project

investment-research-video

## Goal

investagent 研究 → 企业研究 HTML/deck（每页 speaker script，一次内容规划）→ 口语化（Content Lock）→ TTS 配音 → HyperFrames 视频 的完整内容生产链路。

## Current Status

in_progress

## Workflow

- investagent-html-report（研究 → 冲突检查 → HTML/deck 生成）
- investagent-video-production（notes 口语化 → TTS → composition → 渲染）
- investagent-video-by-hyperframes（研究 → 编辑综合 → HyperFrames 全权接管创作与渲染：router → faceless-explainer → creative/core/animation → media-use → CLI render）

## Required Resources

- industry-analysis / industry-cycle-analysis / investagent（研究，P1）
- html-ppt-skill（deck 生成）
- finance-content-engineering（口语化 + 零漂移校验）
- static-html-qa（质检：内容边界/数值/前端/Presenter）
- edge-tts（TTS 配音）
- hyperframes（视频渲染）

## Development Rules

- 内容边界（荐股法律风险红线）：研究/deck/口播/字幕均不得出现目标价/买卖建议/操作区间；表述用中性研究语言
- Content Lock：每页 notes 是最终口播文本唯一 Source of Truth；TTS 仅技术性处理；字幕由 notes 派生
- Audio-First：视频页面时长 = 音频时长；禁多级 xfade 链（累积误差）
- 事实零漂移：口语化改写后 check-fact-drift.py 必跑（禁止近似化）
- 字段清单一律从 workspace 的 `.ai/templates/` 读取填充
- 项目执行记录写入 `logs/`，不直接进入资产库；项目结束时将可复用候选交给 Experience Curator

## Known Issues

- 无
