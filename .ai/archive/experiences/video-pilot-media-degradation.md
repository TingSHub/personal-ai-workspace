---
name: video-pilot-media-degradation
description: HyperFrames 配音降级路径与 Audio First 验证——media-use HeyGen 不可用时用项目已验证的 edge-tts(按空行分段,勿整段合成),视频时长=narration 即验证通过
type: quality-check
status: in-flight
owner: investagent-video-by-hyperframes
asset: media-use
tags: [tts, degradation, audio-first, edge-tts]
---

# Experience: video-pilot-media-degradation

## 来源证据

- 项目：investment-research-video · 2026-08-20 试点(贵州茅台 600519,9 Scene 配音)
- 运行记录：`outputs/companies/贵州茅台/2026-08-20/video/hyperframes-execution.md`(Phase 4 降级记录);`video/audio/segments.json`(202.7s)
- 资源 installed_ref：media-use(随 hyperframes 套件);edge-tts 7.2.8(08-19 venv)

## 触发场景

- HyperFrames 创作链路需要 voiceover,但 HeyGen CLI 未安装/未 auth(media-use `resolve.mjs --doctor` 显示 heygen not found)

## 问题与归属判定

- 问题：①media-use 的 HeyGen free-usage 路径依赖 heygen CLI + OAuth 登录,缺失时配音不可用——按工作流原则如实降级,用项目已验证的 edge-tts(zh-CN-XiaoxiaoNeural, rate +8%,`scripts/tts-edge.py` + 08-19 的 .venv-edge-tts);②`tts-edge.py` 的 `--notes` 模式**按空行分段**,段间无空行会把全部旁白合成 1 段(实测 9 段合成 1 段 207.9s)——必须每段间留空行;③降级是常态而非异常:无 HeyGen 时 doctor 证据留痕 + 记录降级原因,不伪装已生成
- 归属（owner）：investagent-video-by-hyperframes workflow SOP Phase 4 Known Issues

## 可复用结论（resolution）

- 降级路径:media-use doctor 失败 → `scripts/tts-edge.py --notes <txt> --outdir video/audio --flat`,EDGE_TTS_PYTHON 指向已有 .venv-edge-tts
- notes.txt 每 Scene 一段、**段间空行分隔**(extract_notes_from_txt 按 \n\n 分段,去 P\d+: 前缀)
- Audio First 验证:视频总时长 == narration 总时长(ffprobe 双向核对)即 Scene 时长分配正确;响度分段一致(-19~-20dB)无爆音/静音
- 时长裁决:实测超路由裁决点 <4%(202.7 vs 195s)不拆分,记录裁决即可;叙事完整性优先于硬上限的轻微越界

## 回写目标

- investagent-video-by-hyperframes workflow SOP Phase 4 Known Issues(降级路径 + 空行分段坑 + 时长裁决)

## 适用范围

- 本项目视频链路(HyperFrames + 中文配音);任何需要批量 TTS 的中文内容生产

## 不适用范围

- 正式商业发布的 TTS 合规选型(edge-tts 为非官方逆向接口,商用需迁移 Azure 等合规提供方)

## 关联资产

- media-use、hyperframes、investagent-video-by-hyperframes、tts-edge.py
