---
name: podcast-company-specific-opening-and-voice-role-separation
description: 当双人财经播客出现角色名与音色资产混淆或不同公司开场趋同，按逻辑角色与技术音色分离并用公司特征事实重写开场
type: methodology
status: in-flight
owner: investagent-podcast-video-by-hyperframes,editorial-director-agent
asset: investagent-podcast-video-by-hyperframes,editorial-director-agent
tags: [podcast,opening,voice-role,separation,company-specific]
---

# Experience: podcast-company-specific-opening-and-voice-role-separation

## 来源证据

- 用户对协鑫能科 T02 run 的反馈：音色参考与节目角色混淆，且开场与前期公司视频过于相似。
- `outputs/companies/协鑫能科/2026-09-01/editorial/episode-input.json` 与最终 `podcast/script/episode.json`：`display_name=顾慎言`、`logical_speaker=shenyan`、技术资源使用 `voice.luheng`；spoken text 不再暴露音色原主姓名。
- `check_podcast_dialogue.py` 与 `check_editorial_gate.py`：修正后均 PASS。

## 触发场景

生成双人播客的 episode manifest、开场或音色映射时，尤其是克隆音色与公开角色不是同一人的情况。

## 问题与归属判定

- 问题：技术音色名进入节目角色或口播；固定“数字反差+开放问题”让不同公司失去独有入口。
- 归属：节目 Workflow 的 opening/manifest 契约与 editorial-director-agent 的 treatment 规则。

## 可复用结论（resolution）

逻辑角色、公开姓名、音色资源和音色 prompt 必须是四个独立字段。开场保持固定顺序和事实张力门禁，但每家公司必须从自身资产、产品、客户、订单或兑现断点选择 opening mode，并将事实、视觉锚点和问题绑定到本公司 evidence ledger。

## 回写目标

已回写 `investagent-podcast-video-by-hyperframes`、`ACCOUNT_PROFILE` 的开场规则；后续将把经验名加入 `editorial-director-agent` 经验引用。

## 适用范围

双人中文财经播客、HyperFrames manifest；本次验证使用 `podcast-v1-luheng` 与 `gcl-et-002015-20260901-t02-v2`。

## 不适用范围

单人旁白、公开角色与音色原主明确相同的节目，或仅做内部 TTS 技术测试而不产出公开口播文本。

## 关联资产

`investagent-podcast-video-by-hyperframes`、`editorial-director-agent`、`voice.luheng`
