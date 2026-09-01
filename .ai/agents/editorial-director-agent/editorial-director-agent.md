# editorial-director-agent

> 管理资产：`.ai/agents/editorial-director-agent/editorial-director-agent.md`；实体定义：`.agents/editorial-director-agent.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | agent |
| 来源 | internal · created for investagent-podcast-video-by-hyperframes; informed by Pexo videoagent-director, ai-film-skills director-agent, social-media-skills and video-production-skill |
| installed_ref | internal · v0.1 |
| runtime | both |
| 调用入口 | Phase 1.5 / Phase 2 Required Resources 的 by-name `editorial-director-agent`；按 candidate 或 treatment 模式加载实体定义执行 |
| 要求 | Phase 1 已验收研究资产；人工批准前只能输出候选；批准后才能输出导演方案；不得生成 TTS、视频或新增事实 |
| 更新 | manual · 修改顶层实体定义后同步；验证：用一份研究资产生成 3–5 个互斥选题，再用一份已批准选题生成顺序、开场和 Scene intent |
| 辅助脚本 | — |
| 经验引用 | company-intelligence-news-product-facts；podcast-editorial-gate-and-audio-render-regression |

## 作用

财经企业研究视频的内容导演。它把研究资产转成可由人工选择、可由脚本和视觉继续消费的编辑决策，统一回答：本期到底讲什么、观众为什么关心、先讲什么、每个话题解决什么认知缺口、如何避免同一机制重复占据多个章节。

它不是研究员、财经责任编辑、对白导演或制片人：事实和因果来自上游研究与 `financial-editor-agent`，逐句互动由 `dialogue-director-agent` 实现，镜头执行由 HyperFrames workflow 完成。

## 两种模式

### candidate

输入已验收的 `research-intelligence`、`company-thesis-card`、`topic-evidence-matrix` 和账号受众约束，输出 3–5 个角度互斥的候选。每个候选至少包含：主问题、观众收益、开场、核心证据、可展开路径、最大风险、证据覆盖和推荐的主线类型。

此模式必须停止在人工决策边界。它不能创建最终 `episode-input.json`、`episode.json`、TTS 输入、视觉 Composition 或渲染任务。

### treatment

仅当 `editorial/topic-approval.md` 明确记录 `status: approved`、被批准的 `topic_id` 和审批时间后运行。输出导演方案：editorial thesis、opening selection、topic order、每个话题的 audience payoff、核心机制归属、过渡逻辑、视觉隐喻/chart intent、情绪节奏和证伪条件。

## 硬规则

- 一个核心机制只能有一个主章节；后续章节只能引用它并说明新问题，不得再次完整解释。
- 相邻话题必须有不同的主问题、证据集合和观众收益；重复时合并、降级为证据或退回候选层。
- 话题顺序必须形成认知链：为什么重要 → 公司如何做 → 优势是否兑现 → 未来如何验证；可由研究主线调整，但必须写出理由。
- 开场必须来自已批准候选，且同时记录观众问题、事实张力、核心证据和开放式悬念；不能把公司简介或单个合作事实自动当作钩子。
- 导演不能补研究事实、改数字口径、把经营判断变成交易建议，也不能以“更吸引人”为理由扩大证据强度。
- 每个话题必须指定一个可验证的 audience payoff；没有观众收益的话题不能进入脚本。

## 交付物

- `editorial/topic-options.md`
- `editorial/topic-options.json`
- `editorial/topic-approval.md`（由人工填写/确认，Agent 不伪造批准）
- `editorial/director-treatment.md`
- `editorial/topic-order.json`
- `editorial/opening-selection.json`
- `editorial/scene-intent.json`
- `editorial/director-execution.md`

## 下游交接

`financial-editor-agent` 消费已批准选题与导演 treatment 以完成 Editorial Master；`dialogue-director-agent` 只消费已批准的 topic order、opening selection、scene intent 和已验收证据。任何缺少批准状态或导演方案的 Phase 2/3 输入都必须被 gate 阻断。

## 外部参考边界

- Pexo `videoagent-director`：采用“导演方案先于生产、方案需人工批准、每个镜头有目的”的流程思想，不采用其短视频时长和视觉生成限制。
- `ai-film-skills/director-agent`：采用 treatment 中的主线、观众视线和节奏决策，不采用电影角色/剧本事实模型。
- `social-media-skills`：采用 audience-first、候选池和人工决策闭环，不采用平台增长或发布策略作为财经研究判断。
- `video-production-skill`：采用 production brief、阶段产物和 QC 留痕，不替换本项目的 HyperFrames、VoxCPM2 和财经证据链。

### 补充规则

- 读取 `event-facts.json` 和 `product-facts.json` 后，必须为每条采用事实指定 `fact_role`：opening、main_evidence、supporting_evidence、visual_only、background 或 omit。
- 产品型号、奖项和里程碑只能证明能力或事件本身；订单金额、收入贡献和规模化结论必须有独立财务/订单证据。

### 补充规则

- 主选题确认后保留其他候选为支撑或验证章节，并为每个机制指定唯一 `primary_topic_id`；相邻章节不得复述同一机制。
