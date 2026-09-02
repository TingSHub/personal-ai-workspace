---
name: podcast-douyin-handoff-and-investor-cover
description: 当 AiToEarn 通过抖音 App Scheme 立即发布时，人工确认封面并用股民信息流优先的大字号高对比封面完成发布闭环
type: methodology
status: archived
owner: investagent-podcast-video-by-hyperframes,aitoearn,social-auto-upload
asset: investagent-podcast-video-by-hyperframes,aitoearn,social-auto-upload
tags: [douyin,aitoearn,cover,thumbnail,publishing,investor-audience]
---

# Experience: podcast-douyin-handoff-and-investor-cover

## 来源证据

- 协鑫能科真实发布任务：AiToEarn Flow `d4dbec23-9b1e-4517-b438-487741641e0f`，任务 `6a983e02fe73016b35812130`，抖音最终作品 `https://www.douyin.com/video/7680961320070873467`。
- AiToEarn 账号/平台接口实测：抖音账号“账本两面”状态正常；立即发布返回 status 8，用户打开短链并确认后变为 published。
- AiToEarn 当前仓库 main 分支的抖音适配实现：App Scheme 组装视频路径、标题、话题和隐私/下载选项；独立 cover URL 没有进入用户接力 Scheme。验证时上游版本为 `v2.5.0`，本地 REST 使用中国版 `https://aitoearn.cn/api`。
- `cover.html`、`cover.png`、`cover-3x4.png`：新版封面以 `6000MW`、大标题和“资产很大，收入在哪？”为首屏信息，横版与竖版分别适配并通过 Playwright 渲染 PASS。

## 触发场景

通过 AiToEarn 将财经视频立即提交抖音，并希望在手机确认时使用独立设计封面、提高股民信息流点击识别度。

## 问题与归属判定

- 问题：请求中虽然带了独立封面，但抖音确认页默认显示视频首帧；需要在手机确认页手动上传封面。旧的“平台封面已传入”判断会误导发布验收。
- 归属：AiToEarn 调用说明与播客 Workflow Phase 6 的抖音人工确认/封面门禁；封面设计规则归入播客视觉与账号发布资产。

## 可复用结论（resolution）

AiToEarn 抖音立即发布应按“提交 → 手机打开 Scheme → 确认页人工检查封面 → 上传最终 3:4 封面 → 确认 → API 轮询作品链接”执行。请求封面与抖音实际采用封面分开记录。面向股民的封面不要使用弱识别的留白报告式版式，应优先把公司名、核心数字、经营矛盾和高对比色放入首屏，并为横版与 3:4 分别重排。抖音话题数量以当前平台校验为准，本次实测上限为 5 个。

## 回写目标

已回写 `investagent-podcast-video-by-hyperframes` Phase 6/Quality Criteria、`aitoearn` 调用说明和 `social-auto-upload` 经验引用；发布结果已回写 `account-profile/published-works.md`。

## 适用范围

AiToEarn 中国版 REST/API Key、抖音 App Scheme 用户接力和财经播客封面；验证使用 `aitoearn` v2.5.0 资源记录与真实抖音发布任务。

## 不适用范围

不能据此断言所有 AiToEarn 平台都忽略独立封面；B站、YouTube 等平台可能由其服务端或官方 API 处理封面。不能把 status 8 或分享 ID 当作已发布作品链接。

## 关联资产

`investagent-podcast-video-by-hyperframes`、`aitoearn`、`social-auto-upload`、`video-agent-publisher`
