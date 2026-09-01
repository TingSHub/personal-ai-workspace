---
name: company-intelligence-news-product-facts
description: 当上市公司视频需要呈现近期新闻、奖项、产品型号或项目里程碑时，使用 Tavily 优先发现、原文核验和 fact-card 交接，避免研究事实在脚本或视觉阶段丢失
type: methodology
status: archived
owner: investagent-podcast-video-by-hyperframes, multi-search, editorial-director-agent
asset: investagent-podcast-video-by-hyperframes, multi-search, cninfo-connector, news-search, editorial-director-agent
tags: [company-intelligence, tavily, news, products, provenance, video]
---

# Experience: company-intelligence-news-product-facts

## 来源证据

- 项目：`investment-research-video`，中科曙光 `2026-08-26-editorial-gate-rerun`。
- 产物：`research-materials/company-intelligence/event-facts.json`、`product-facts.json`、`source-ledger.json`、`coverage-report.md`、`podcast/visual-plan/fact-card-manifest.json`。
- 验证：`multi-search` `prefer_quality=True` 实际使用 Tavily；状态为 Tavily 可用，997/1000 配额剩余；最终采用事实均有打开来源。
- 事实样本：科技日报报道曙光8000（登峰）十万卡超集群与应用扩展；公司行动方案页面披露 scaleX640、FlashNexus、ParaStor、C7000-F 等产品事实。

## 触发场景

上市公司研究视频中需要呈现近期新闻、获奖、产品发布、具体型号、签约/中标/交付、标准制定或技术里程碑，且这些事实需要从研究传递到脚本和视觉。

## 问题与归属判定

- 问题：原 Phase 1 只要求财务、行业和护城河证据，没有独立公司动态/产品事实资产；旧视频因此只呈现抽象能力，事实在脚本和画面阶段容易丢失。
- 归属：回写 `investagent-podcast-video-by-hyperframes` Phase 1/1.5/2/4/5；搜索调用补充到 `multi-search`；事实角色交接补充到 `editorial-director-agent`。

## 可复用结论（resolution）

1. Phase 1 增加公司动态与产品事实证据线，统一产出 `event-facts.json`、`product-facts.json`、`source-ledger.json` 和 `coverage-report.md`。
2. 搜索发现使用 `multi-search(prefer_quality=True)`，实际优先 Tavily；`news-search` 只做聚合补充；搜索摘要不得直接进入口播。
3. 每条事实记录 `fact_id`、事件/发布日期、类型、主体、原文 URL、定位、来源级别、相关性和视觉候选。
4. Phase 1.5 由内容导演决定事实属于 opening、main_evidence、supporting_evidence、visual_only、background 或 omit；不能把新闻标题自动升级为主线。
5. Phase 2 manifest 保留 `fact_ids`、`fact_role`、`source_refs` 和 `visual_intent`；Phase 4 用 `fact-card-manifest.json` 生成事件卡、产品卡、型号卡或里程碑时间线。
6. 订单金额、收入贡献、奖项等级和产品性能必须在一手或权威原文核验后使用；找不到时记录缺口而不是用低质量媒体补齐。

## 回写目标

- `investagent-podcast-video-by-hyperframes`：Phase 1/1.5/2/4/5 的 Required Resources、Output、Quality Criteria 和 Known Issues。
- `multi-search`：现有 `prefer_quality=True` / Tavily 调用和来源回指说明。
- `editorial-director-agent`：事实角色分类和产品/新闻到视觉的交接规则。

## 适用范围

上市公司研究、财经播客和 HyperFrames 视频；本次验证资源为 `multi-search` tree-sha256 `6535cb0b3ab7`、`cninfo-connector` internal、`editorial-director-agent` internal v0.1。

## 不适用范围

纯财务报表解读、无需近期事实的历史专题，或需要实时监控而不是单次研究的新闻产品；实时监控应另行配置监控服务和告警策略。

## 关联资产

`investagent-podcast-video-by-hyperframes`、`multi-search`、`cninfo-connector`、`news-search`、`editorial-director-agent`
