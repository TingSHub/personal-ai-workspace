---
name: podcast-editorial-gate-and-audio-render-regression
description: 当财经播客需要验证新选题流程时，先用一次人工 topic approval 锁定主线，再用导演去重、已知文本对齐和全局时间线完成端到端回归
type: quality-check
status: archived
owner: investagent-podcast-video-by-hyperframes, editorial-director-agent
asset: investagent-podcast-video-by-hyperframes, editorial-director-agent, podcast-audio-compiler, hyperframes-cli
tags: [editorial-gate, podcast, audio-qa, hyperframes, timeline]
---

# Experience: podcast-editorial-gate-and-audio-render-regression

## 来源证据

- 项目：`investment-research-video`，中科曙光 `2026-08-26-editorial-gate-rerun`。
- 用户确认一次 `TOPIC-B` 后，Phase 2 生成 8 个支撑关系明确的话题；Phase 1.5 gate PASS。
- Phase 3：48 个 VoxCPM2 turn、406.86 秒、`reused_segments=0`；Qwen known-text alignment 48/48 PASS。
- Phase 5：12,206 帧 HyperFrames high render artifact validated；视频 406.866667 秒，与音频误差小于 0.01 秒。

## 触发场景

需要验证“候选选题—人工确认—内容导演—脚本—音频—视觉—渲染”完整链路，且旧 run 已有相似主题或音频，容易误复用。

## 问题与归属判定

- 问题：只有内容检查而没有状态 gate 时，旧主线、旧脚本和旧音频会混入新 run；只有 TTS 成功而没有反向对齐时，异常句可能进入成片；局部 Scene 时间与全局进度线可能不一致。
- 归属：回写 `investagent-podcast-video-by-hyperframes` Phase 1.5/3/4/5；保留 `check_editorial_gate.py`、`align_podcast_known_text.py` 为可复用脚本。

## 可复用结论（resolution）

1. Phase 1.5 产出 3–5 个互斥候选并保持 `pending`；只有人工批准的 `topic_id` 才允许 Phase 2。
2. 其他候选不必删除，应在导演方案中标记为支撑章节、验证章节或背景，并为每个主机制指定唯一 `primary_topic_id`。
3. TTS 后执行已知文本对齐，QA 记录 turn 数、异常句、对齐模型和重生成闭环。
4. 进度、章节、Scene、字幕和音频使用同一累计时间线；turn 之间的停顿应作为已记录 pause gap 验证，而不是误判为断裂。
5. 长片渲染前必须运行 HyperFrames check、animation map、关键快照和高质量 render；静态 HTML 检测告警必须保留在 QA，不以静默忽略替代解释。

## 回写目标

- `investagent-podcast-video-by-hyperframes`：Phase 1.5/3/4/5 的 gate、反向对齐和全局时间线规则。
- `editorial-director-agent`：主线/支撑章节与机制去重规则。
- `podcast-audio-compiler`：已知文本对齐和异常句重生成记录。

## 适用范围

双人财经播客、HyperFrames 长片和 manifest 驱动的 TTS 视频；本次验证 VoxCPM2、Qwen3-ForcedAligner 0.6B 和 HyperFrames 0.8.15。

## 不适用范围

没有已知脚本文本的自由录音转写、纯音乐视频，或不需要人工选题的单次短片。

## 关联资产

`investagent-podcast-video-by-hyperframes`、`editorial-director-agent`、`podcast-audio-compiler`、`qwen3-forced-aligner`、`hyperframes-cli`
