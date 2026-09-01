---
name: podcast-audio-pacing-contract
description: 试听发现播客语速和停顿过于统一时，优先复用现有 VoxCPM2 与情绪参考音频，把 delivery 转成可执行的语速、句内停顿和开场悬停计划
type: quality-check
status: archived
owner: investagent-podcast-video-by-hyperframes, podcast-audio-compiler
asset: podcast-audio-compiler, podcast-workflow, human-understanding
tags: [podcast, audio, pacing, prosody, tts, quality-gate]
---

# Experience: podcast-audio-pacing-contract

## 来源证据

- 项目：investment-research-video，东山精密 run 2026-08-23。
- 证据：podcast/audio/podcast-v1-luheng-corrected/segments.json 与 audio-qa.json。
- 统计：107 段音频；林知微约 4.79 字/秒，顾慎言约 4.50 字/秒；冷开场林知微约 4.39 字/秒，顾慎言约 4.00 字/秒。
- 开场四个 turn 的 turn 间停顿全部为 140ms；episode manifest 的 pause_after_ms 为 0，由 natural-pauses 回填。
- 编译器现状：delivery 写入 segments 元数据；natural-pauses 按 interaction_type 生成 turn 间静音；没有 speech rate 或句内 break 的执行参数。

## 触发场景

- 用户试听反馈“有点快”“每个人都像一个速度”“关键地方没有停下来”。
- 开场事实反差或开放问题需要悬停，但现有 TTS 只依赖标点和统一默认停顿。

## 问题与归属判定

- 问题：当前 delivery 是描述性字段，不是完整的声学控制；开场 hook、answer、self_introduction 没有专门的停顿档位。
- 归属：investagent-podcast-video-by-hyperframes Phase 3，以及 podcast-audio-compiler 的通用编译契约。

## 可复用结论（resolution）

1. 保留 VoxCPM2、逐句 WAV、emotion 参考音频、natural-pauses 和现有 QA；不要为这一问题先更换 TTS 后端。
2. 在同一 episode manifest 中补充可执行的 speech_rate、pause_plan 和 intra_turn_breaks；由现有逐句编译器消费并写回 segments/SRT/QA。
3. 开场单独设定更长的 turn 间停顿，并在事实反差后、开放问题前声明句内停顿；普通说明句沿用正常节奏。
4. 用同一 manifest 做 A/B，只比较节奏字段，避免把音色、文案和事实变化混入试听判断。
5. HyperFrames Audio 只承担混音、EQ、压缩和音量自动化，不承担口播语速或语义停顿控制。

## 回写目标

- 已回写：investagent-podcast-video-by-hyperframes Phase 3 Known Issues/Evolution Log。
- 已回写：podcast-audio-compiler 节奏控制现状与复用路径。

## 适用范围

VoxCPM2 主播/分析师逐句播客；适用于开场、话题转折、关键数字和结论句。

## 不适用范围

需要全新声线、强烈表演型配音或音乐节拍驱动的项目；这些情况仍应单独建立音频 profile 或选择相应 Workflow。

## 关联资产

investagent-podcast-video-by-hyperframes、podcast-audio-compiler、podcast-workflow、human-understanding
