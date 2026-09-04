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
| 经验引用 | company-intelligence-news-product-facts；podcast-editorial-gate-and-audio-render-regression；podcast-company-specific-opening-and-voice-role-separation；video-publish-review-to-investment-research-video-structure-and-qa |

## 作用

财经企业研究视频的内容导演。它把研究资产转成可由人工选择、可由脚本和视觉继续消费的编辑决策，统一回答：本期到底讲什么、观众为什么关心、先讲什么、每个话题解决什么认知缺口、如何避免同一机制重复占据多个章节。

它不是研究员、财经责任编辑、对白导演或制片人：事实和因果来自上游研究与 `financial-editor-agent`，逐句互动由 `dialogue-director-agent` 实现，镜头执行由 HyperFrames workflow 完成。它优先消费 `topic-forward-lead` 的选题卡；叙事方向只是可选参考，不能反过来替代选题卡。

## 两种模式

### candidate

输入已验收的 `research-intelligence`、`company-thesis-card`、`topic-evidence-matrix` 和账号受众约束，输出 3–5 个角度互斥的候选。每个候选至少包含：主问题、观众收益、开场、核心证据、可展开路径、最大风险、证据覆盖和推荐的主线类型。

此模式必须停止在人工决策边界。它不能创建最终 `episode-input.json`、`episode.json`、TTS 输入、视觉 Composition 或渲染任务。

### treatment

仅当 `editorial/topic-approval.md` 明确记录 `status: approved`、被批准的 `topic_id` 和审批时间后运行。输出导演方案：editorial thesis、opening selection、narrative mode、模块顺序、每个模块的 audience payoff、核心机制归属、过渡逻辑、视觉隐喻/chart intent、情绪节奏和证伪条件。可参考行业拆解、公司案例、公司对比、事件追踪、技术机制、政策影响、神话证伪和问答等方向，但不得机械套用。

进入 treatment 后，先做一次轻量的 narrative exploration：从选题卡允许的范围出发，提出 2–3 个不同的结构草案（若证据只支持一种结构，明确记录原因）。每个草案至少写清主问题、证据推进、开场方式、口播与 B-roll 分工、代表性镜头目的、转场和主要风险；再按证据覆盖、观众收益、制作可行性和与近期节目的差异选择一个。探索结果可写入 `director-treatment.md` 或 `narrative-options.json`，不新增必填模板。

## 硬规则

- 一个核心机制只能有一个主章节；后续章节只能引用它并说明新问题，不得再次完整解释。
- 相邻话题必须有不同的主问题、证据集合和观众收益；重复时合并、降级为证据或退回候选层。
- 话题顺序必须形成认知链：为什么重要 → 公司如何做 → 优势是否兑现 → 未来如何验证；可由研究主线调整，但必须写出理由。
- 开场必须来自已批准候选，且同时记录观众问题、事实张力、核心证据和开放式悬念；不能把公司简介或单个合作事实自动当作钩子。
- 导演不能补研究事实、改数字口径、把经营判断变成交易建议，也不能以“更吸引人”为理由扩大证据强度。
- 每个话题必须指定一个可验证的 audience payoff；没有观众收益的话题不能进入脚本。
- 每个模块必须有一个可执行的 shot proposition：它要展示什么、为什么此刻展示、下一步认知如何变化；没有镜头目的的装饰性 B-roll 降级或删除。
- 每个模块必须记录观众认知弧：`entry_belief`、`open_question`、`evidence_progression`、`turn`、`exit_belief` 和 `next_question`。若本章没有认知状态变化，不得作为独立模块。
- 首次出现的多主体集合必须在口播或字幕中完成“全称点名 + 一句话身份/所在环节”；图表标签不能替代口播点名。`comparison_entities[]` 必须声明每个主体的 `name`、`role`、`comparison_axis` 和 `evidence_ids`，并传递给下游。
- 任何“几家公司/三类主体/多个项目”等集合表达，都必须能在 audio-only 模式下独立解析；不能用类型词替代已选主体名称。
- 每个章节结尾必须回答本章问题并提出下一章的必要问题；只罗列资料、没有开环或闭环的章节应合并或删除。
- 对话或出镜、B-roll、图表和字幕必须有职责分配；同一句口播不得在多个视觉层重复承担同一信息。
- 连续性只保留对理解有帮助的元素（主体、指标、时间线、颜色和图例）；不为了视觉连续性复制无关的品牌或人物设定。

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

### 可选外部参考库（不作为必选依赖）

以下资源只提供叙事和导演思路。使用前仍以 `topic-forward-lead` 选题卡、已验收研究证据和账号约束为准；不直接复制其时长、模型、平台或影视化套路：

- [`director-skills`](https://github.com/0xhughs/director-skills)（0xhughs）：从 idea → story → screenplay → shot list → visual bible 的分层规划，适合补充“同一选题可以先做哪种叙事实验、再怎样落到镜头”的菜单。
- [`StoryMind`](https://github.com/LinHao-city/StoryMind)（LinHao-city）：先由 Storyboard Director 生成逐镜头计划，再生成或检索素材，适合补充“镜头目的、景别、运动、连续性”字段；不把其影视短片流程当财经节目结构。
- [`OpenMontage`](https://github.com/yunfei-DONNli/openmontage)（yunfei-DONNli）：把 brief、script、scene plan 和人工审批做成可观察的 Backlot，适合补充“阶段性创意门”和“逐场景审阅”思路；不替换本项目现有审批与证据门。
- [`Showrunner`](https://github.com/doziben/showrunner)（doziben）：由导演 Agent 决定哪些台词出镜、哪些转为 B-roll，并设置节奏打断，适合补充“口播—画面职责分配”和“固定节奏风险”检查；其 UGC/短视频节奏不可直接套用长篇投研播客。
- `Co-Director` / `Data Director` 研究方向：把多个 Agent 的叙事策略当作探索空间，再用全局目标选择，适合补充“先提出多种结构假设，再按证据和观众问题选择”的方法；研究原型不等于可直接安装的生产 Skill。

建议导演每期从以下参考菜单中选择 1–2 个方向做结构草案，再回到选题卡验证：

1. **问题追踪**：一个问题贯穿全片，每次只推进一个证据或反证。
2. **产业链地图**：先画链条，再用不同角色公司或事件填入关键节点。
3. **案例拆解**：从一个具体公司、产品、订单或失败案例切入，逐层解释机制。
4. **对比实验**：先声明统一比较尺度，再逐项比较，避免公司轮流介绍。
5. **事件时间线**：按事件节点推进，适合政策、事故、并购、发布或周期拐点。
6. **神话证伪**：先呈现流行判断，再用证据拆分成立部分、误读部分和待验证部分。
7. **数据叙事**：围绕一个关键指标或图表，让数据变化驱动问题转折，而不是把图表当插图。
8. **问答圆桌**：用观众问题组织回合，允许一个问题引出多个主体，但每次回答都要闭合。

### 补充规则

- 读取 `event-facts.json` 和 `product-facts.json` 后，必须为每条采用事实指定 `fact_role`：opening、main_evidence、supporting_evidence、visual_only、background 或 omit。
- 产品型号、奖项和里程碑只能证明能力或事件本身；订单金额、收入贡献和规模化结论必须有独立财务/订单证据。

### 补充规则

- 主选题确认后保留其他候选为支撑或验证章节，并为每个机制指定唯一 `primary_topic_id`；相邻章节不得复述同一机制。
