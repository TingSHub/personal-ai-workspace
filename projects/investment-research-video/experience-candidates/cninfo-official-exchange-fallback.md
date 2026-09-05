---
name: cninfo-official-exchange-fallback
description: 当 CNINFO 按代码检索返回空结果时，切换到对应交易所官方公告接口并区分索引成功、PDF 下载成功和正文核验成功
type: resource-lesson
status: in-flight
owner: cninfo-connector,investagent-video-by-hyperframes
asset: cninfo-connector,investagent-video-by-hyperframes
tags: [cninfo, official-disclosure, fallback, pdf-validation, research-evidence]
---

# Experience: cninfo-official-exchange-fallback

## 来源证据

- `TOPIC-07` 实际运行中，CNINFO 对 688435、603138、300663 返回空结果；对应上交所/深交所官方接口分别返回 2026 年半年度报告索引。
- `cninfo-connector` 的 `scripts/cninfo_client.py` 已验证：CNINFO 主路径、SSE 兜底、SZSE 兜底；科蓝软件深交所 PDF 下载通过 `%PDF-` 文件头校验。
- 上交所当前运行环境返回反爬 HTML，连接器已增加拒绝伪 PDF 的保护。
- 验证资源：`cninfo-connector`，`installed_ref: internal`。

## 触发场景

按 A 股代码检索年报、半年报或公告时，CNINFO 请求成功但返回空结果，或 CNINFO 请求不可用。

## 问题与归属判定

- 问题：不能把 CNINFO 空结果误判为公司没有公告，也不能把交易所反爬 HTML 当成已下载 PDF。
- 归属：通用取证规则归入 `cninfo-connector`；视频研究阶段的逐家公司状态记录归入 `investagent-video-by-hyperframes`。

## 可复用结论（resolution）

统一检索入口保持 CNINFO 优先；空结果或请求失败时，按证券市场切换到上交所或深交所官方接口。所有来源统一输出公告 ID、标题、发布日期和官方链接，并记录 `source`。下载阶段必须验证 PDF 文件头；“公告索引成功”“文件下载成功”“正文可检索定位成功”是三个不同状态，不能合并报告。

## 回写目标

将上述规则保留在 `cninfo-connector` 的调用说明与注意事项中，并在 `investagent-video-by-hyperframes` 的研究输入和质量标准中要求逐家公司记录主路径/兜底路径、下载状态和正文定位状态。

## 适用范围

适用于 `cninfo-connector` `installed_ref: internal` 支持的 A 股公告取证，以及以用户批准 topic card 启动的公司或公司对比研究。

## 不适用范围

交易所接口返回的索引不能直接替代 PDF 正文；第三方网页只能作线索或交叉验证，不能作为公司关键事实的唯一来源。交易所反爬未解除时，不得声称已完成官方 PDF 归档或正文核验。

## 关联资产

`cninfo-connector`、`investagent-video-by-hyperframes`、`TOPIC-07`
