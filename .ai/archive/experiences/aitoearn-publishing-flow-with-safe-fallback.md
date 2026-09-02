---
name: aitoearn-publishing-flow-with-safe-fallback
description: 当视频已完成且需要多平台发布时，先用 AiToEarn Flow 追踪各平台结果，只有明确失败且未提交才回退浏览器自动化
type: methodology
status: in-flight
owner: investagent-podcast-video-by-hyperframes,aitoearn,social-auto-upload
asset: investagent-podcast-video-by-hyperframes,aitoearn,social-auto-upload
tags: [publishing,aitoearn,multi-platform,fallback,idempotency,workflow]
---

# Experience: aitoearn-publishing-flow-with-safe-fallback

## 来源证据

- AiToEarn Open Platform 文档：账号列表、签名 URL 上传、确认资源、创建多平台 Flow、发布记录查询和抖音用户操作信息接口。
- `aitoearn` 资源记录：已记录中国版/国际版端点匹配、状态机和 API Key 不入库规则。
- 播客 Workflow Phase 6：已写入逐平台结果、作品链接、抖音人工确认和状态不明禁止回退规则；本次尚未执行真实平台发布。

## 触发场景

视频、封面、平台差异化 metadata 和来源清单已经通过 QA，需要一次提交到多个已授权账号时。

## 问题与归属判定

- 问题：多平台逐个手工发布耗时；一个平台超时后盲目切换另一套工具会造成重复发布。
- 归属：发布 Workflow 与 AiToEarn/social-auto-upload 调用说明。

## 可复用结论（resolution）

发布顺序固定为 metadata → 账号/平台规则 → 资源上传确认 → Flow → 逐平台轮询 → 作品链接回写。AiToEarn 明确不支持或明确失败且无“可能已提交”状态时，才调用 social-auto-upload；状态未知必须先查记录或停在恢复状态。默认草稿/排期，真实立即发布仍需用户明确指定。

## 回写目标

已回写 `investagent-podcast-video-by-hyperframes` Phase 6、`.ai/skills/aitoearn/aitoearn.md` 和 `.ai/skills/social-auto-upload/social-auto-upload.md`。

## 适用范围

AiToEarn Open Platform 中国版 REST/MCP、国内平台浏览器回退；资源版本 `aitoearn v2.5.0`、`social-auto-upload 1c66b7db4b30585bbb40c58eb0aa572ffa3cce97`。

## 不适用范围

没有用户明确授权的真实发布、状态未决的失败恢复、或需要平台官方 API 审核能力的企业级发布系统。

## 关联资产

`investagent-podcast-video-by-hyperframes`、`aitoearn`、`social-auto-upload`、`video-agent-publisher`
