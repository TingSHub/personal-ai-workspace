---
name: podcast-free-financial-data-fallback
description: 当 Tushare 积分或接口权限不足时，用官方披露作事实主源并以 AkShare/BaoStock 结构化回退且显式映射财务口径
type: resource-lesson
status: in-flight
owner: investagent-podcast-video-by-hyperframes,tushare-connector
asset: investagent-podcast-video-by-hyperframes,tushare-connector
tags: [finance-data,akshare,baostock,tushare,fallback,field-mapping]
---

# Experience: podcast-free-financial-data-fallback

## 来源证据

- 协鑫能科 2026H1 run 的 `research-materials/data-source-ledger.json`：Tushare daily PASS，income/fina_indicator 因 120 积分返回 40203；AkShare 三表返回成功并与官方半年报关键数字一致；BaoStock 季频财务和日线成功。
- `references/global-contract.md` 新增 Free data-source routing and degradation 契约。

## 触发场景

上市公司播客研究需要三表、财务指标和同行统一期数据，但单一数据供应商缺少积分、超时或字段不可用时。

## 问题与归属判定

- 问题：把 Tushare 视为硬依赖，或把结构化接口的合并净利润直接当成归母净利润。
- 归属：研究 Workflow 的数据源路由和质量门禁；连接器记录只保留调用说明。

## 可复用结论（resolution）

官方年报/半年报 PDF 永远是关键事实主源。Tushare 仅在权限可用时优先；AkShare/BaoStock 用于自动化结构化取数和行情回退。每次调用写入 source ledger，记录 API、报告期、单位、复权方式、字段映射、官方复核和降级原因；口径不一致则禁止比较，三层都失败就写缺口。

## 回写目标

已回写 `investagent-podcast-video-by-hyperframes/references/global-contract.md` 与 Workflow Phase 1；将经验名加入 `aitoearn` 资源记录作为研究侧调用注意事项不合适，后续不扩展到发布资源。

## 适用范围

A 股上市公司研究、报告/播客内容工程；本次验证使用 AkShare 1.18.94、BaoStock 0.9.30 和官方 CNINFO PDF。

## 不适用范围

把第三方结构化源当作唯一审计证据、需要实时 Level-2 或未公开数据的交易系统。

## 关联资产

`investagent-podcast-video-by-hyperframes`、`tushare-connector`、`earnings-reader`、`cninfo-connector`
