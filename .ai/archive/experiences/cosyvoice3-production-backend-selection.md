---
name: cosyvoice3-production-backend-selection
description: 当双人中文播客比较本地 TTS 后端时，先用同一开场做 zero-shot canary，再将 CosyVoice3 的稳定参数固定为生产 profile。
type: resource-lesson
status: archived
owner: investagent-podcast-video-by-hyperframes,podcast-audio-compiler
asset: podcast-v1-luheng
tags: [tts, cosyvoice3, voxcpm2, podcast-audio, canary]
---

# Experience: cosyvoice3-production-backend-selection

## 来源证据

- 项目：`investment-research-video`。
- 中科曙光开场 canary：`outputs/companies/中科曙光/2026-08-26-editorial-gate-rerun/podcast/audio/cosyvoice-opening-ab-20260827/01-zero-shot-luheng-v2/audio-qa.json`，CosyVoice3-0.5B、4 turns、42.3 秒、QA PASS。
- 公平 VoxCPM2 对照：`outputs/companies/中科曙光/2026-08-26-editorial-gate-rerun/podcast/audio/voxcpm-opening-fair-20260827/`，reference、continuation、ultimate 三路均使用同一开场和基础参考音色；用户试听反馈均不如 CosyVoice3。
- 验证资源：CosyVoice3-0.5B 本地模型、`external/cosyvoice`、项目 `.venv-cosyvoice`；VoxCPM2 为 `openbmb/VoxCPM2`，项目 `.venv-voxcpm`。

## 触发场景

双人中文财经播客需要在多个本地 TTS 后端之间做听感选择，且必须保证后端切换不改变脚本、角色映射和停顿契约。

## 问题与归属判定

- 问题：原稳定 profile 使用 VoxCPM2；在同一开场的公平试听中，CosyVoice3 zero-shot 的情绪收束和整体稳定性更符合当前节目。
- 归属：回写 `podcast-v1-luheng` 与 `investagent-podcast-video-by-hyperframes` 的音频编译阶段。

## 可复用结论（resolution）

- 该次 A/B 实验中，CosyVoice3-0.5B zero-shot 的开场听感优于当时的 VoxCPM2 对照；结论只适用于该次试听与对应模型安装。
- CosyVoice3 的实验调用使用 `.venv-cosyvoice`、`external/cosyvoice`、Fun-CosyVoice3-0.5B、自然停顿、无后处理和 boundary-clean。
- 该次 CosyVoice3 实验使用 `voice.luheng/reference.wav`；后续项目 profile 的生产后端由 Workflow 明确决定，不由本 Experience 静默覆盖。
- 后端切换前先跑同一份 `COLD_OPEN + INTRO` canary；通过音频可解码、角色/顺序、停顿、响度和人工试听后，才扩展整期。
- VoxCPM2 保留为显式 A/B 后端，不作为当前 profile 的静默回退。

## 回写目标

已回写：`podcast-v1-luheng`、`investagent-podcast-video-by-hyperframes`。

## 适用范围

适用于本项目的 `host_analyst` 中文播客和当前 CosyVoice3-0.5B 本地安装；需要保留已登记的 `voice.zhiwei` 与 `voice.luheng` 资源。

## 不适用范围

不自动推导其他项目的后端优先级；不把一次 canary 试听当成所有文本、音色或模型版本的普遍结论。

## 关联资产

`podcast-v1-luheng`、`investagent-podcast-video-by-hyperframes`、`podcast-audio-compiler`、`voice.zhiwei`、`voice.luheng`
