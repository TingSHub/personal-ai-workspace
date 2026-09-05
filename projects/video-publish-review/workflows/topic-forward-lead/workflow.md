# Workflow: topic-forward-lead

> 位置: Project: projects/video-publish-review/workflows/topic-forward-lead/

## Mission

作为下一条视频的唯一上游输入：用免费市场信号（涨停池/涨幅异动/财经热点）+ 账号规律库（account-rules.md）+ 上一轮复盘候选，为不同范围的选题自动匹配适合验证的改进方向，生成多样化候选池和 6–8 张可直接交给生产 Workflow 的选题卡，让"发布 → 复盘 → 选题前瞻 → 生产"形成完整飞轮。

## Input

- 市场信号：`topic-forward-signal-scanner` 产物（`outputs/topic-forward/YYYY-MM-DD/signals.json`：涨停池+涨幅榜）
- 财经热点：news-search / multi-search 当日/近 2 日关键词热度；social-trend-monitor 海外风向（可选）
- 复盘候选：上一轮 `publish-review` 复盘册中的 `attribution-<日期>.md` 改进候选池；首次运行没有历史候选时显式记录为空
- 账号规律：`outputs/account-rules.md`（publish-review P7 产物，已验证规律权重高于假设中）
- 去重基线：源项目 `published-works.md` + 全部复盘册（已做过的选题剔除）

## Output

`outputs/topic-forward/YYYY-MM-DD/topic-forward.md`（人类阅读视图）+ `topic-forward.json`（结构化事实源）：
- 信号摘要节：涨停行业聚集度 Top、涨幅榜异常、热点主题
- 候选池节：公司/题材候选（每个含信号证据：涨停/涨幅/换手/热点来源）
- 规律匹配节：候选 × account-rules 打分明细
- 选题卡节：6–8 张，每张含重点范围、研究对象、观众问题、内容承诺、核心冲突、证据线索、叙事方向、封面方向和结构化复盘约束
- `topic-forward.json` 中每张卡是生产 Workflow 的唯一机器可读输入；Markdown 中的交接摘要只是阅读视图，不是事实源
- 审批节：用户只确认 topic card；确认后该 topic card 成为 investment-research-video 的唯一视频输入

## Principles

- best_available_resource：按实际效果、输出质量、稳定性、依赖成本、维护成本和当前项目适配性选择资源，禁止 local first；来源不构成优先级
- 真实执行留痕：Required Resources 必须真实执行并留下独立产物（含资源 by-name 与 installed_ref）；未执行不得写成已执行
- 免费优先：市场数据源用 akshare（免费无token，已实测），不引入收费源
- 信号要可追溯：每个选题卡的证据引用信号 JSON 的具体字段与新闻来源，不引用记忆
- 合规前置：选题卡表述过 boundary-rewrite 约定边界（不荐股、不预测点位）；选题本身倾向研究视角（财报可验证/证据链可展示）
- by-name 引用：Workflow / Skill / Agent / Experience 一律用 by-name 标识符
- 选题先定范围：明确本期讲行业、产业链、单家公司或公司对比，再生成结构化 topic card；不让行业标题在生产时无理由收缩成单家公司
- 选题卡是生产主输入；其中的差异化角度、内容范围和复盘约束提供方向，investment-research-video 再结合调研结果决定叙事与视觉实现
- 每张选题卡必须自行判断哪些复盘候选适用于该选题；候选可以不采纳，也可以携带一个或多个适配候选，但不再设置独立的候选用户审批步骤
- 生产 Workflow 只接收用户批准的 topic card，不直接读取 publish-review 的 attribution 或候选池
- 多样性配额：每轮默认生成 6–8 张卡，至少包含 2 张公司重点型、1 张行业重点型、1 张重大新闻重点型、1 张公司对比型；数量不足时说明缺口，不用低质量卡硬凑。
- 公司落点约束：行业重点型和新闻重点型必须指定 2–4 家待研究公司或公司角色；公司重点型可以围绕一家展开，但必须交代其行业位置、事件背景和可比对象；公司对比型必须围绕同一个问题横向比较。
- 重点范围与涉及公司数分开记录：前者决定叙事重心，后者由证据决定。

## Phase 1: signal-scan — 市场信号扫描

### Goal

跑行情信号脚本（涨停池+涨幅榜）并补热点新闻，产出信号摘要。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| topic-forward-signal-scanner | skill | 必选 | workspace · `.ai/skills/topic-forward-signal-scanner/` · internal v0.1 | 涨停池东财、全量行情新浪；接口偶发断连，输出 errors 并由本 Workflow 标注降级 |
| news-search | skill | 必选 | workspace · .ai/skills/news-search | 财经热点关键词热度 |
| build-topic-candidates.py | script | 必选 | project · `projects/video-publish-review/scripts/` | 把信号 JSON 归一为公司/行业种子；不替代研究判断 |
| multi-search | skill | 可选 | workspace · .ai/skills/multi-search | 交叉验证 |
| social-trend-monitor | skill | 可选 | workspace · .ai/skills/social-trend-monitor | 海外 AI/科技风向（映射国产题材） |

### Input

无（Skill 自取当日数据；交易时段后跑，数据最全）。

### Output

`outputs/topic-forward/YYYY-MM-DD/signals.json`（Skill 产物）+ `candidate-pool.json`（脚本归一结果）+ 信号摘要（涨停行业聚集度、涨幅榜异常、热点主题列表）。

### Quality Criteria

- 信号 JSON 含 captured_at/trade_date/errors（errors 非空必须标注降级）
- 涨停池行业分布统计完成；热点主题 ≥3 个（来自 news-search，含来源与时间）
- 非交易日运行要明确标注"非交易数据"，不得当有效信号

### Known Issues

- akshare 接口均为第三方免费源，偶发断连/变动；脚本有错误捕获与降级提示，失败该路即标注
- 新浪全量行情 + 东财涨停池是主通道；板块资金流是备选，不阻塞流程

## Phase 2: candidate-pool — 候选池构建

### Goal

从信号映射为分层候选池：公司重点、行业重点、重大新闻重点、公司对比重点。涨停行业聚集生成行业候选，涨幅异动生成公司候选，热点新闻生成新闻驱动候选，同一产业链或问题下的多个公司生成对比候选。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| 信号 JSON + 热点摘要 | input | 必选 | Phase 1 | — |
| build-topic-candidates.py | script | 必选 | project · `projects/video-publish-review/scripts/` | 生成可追溯的种子池 |
| finance-content-engineering（topic-gen 方法） | skill | 必选 | workspace · .ai/skills/finance-content-engineering | 角度互斥性检查；研究资产可用后整理深层角度 |

### Input

Phase 1 产物。

### Output

候选池表：候选（公司/行业/新闻/对比）× 信号证据（涨停/涨幅/换手/新闻）→ 归一为 12–20 个原始候选，并标注重点范围、待研究公司角色和去重状态。

### Quality Criteria

- 每个候选必须挂信号证据（无证据不放候选池）
- 公司重点型必须有具体公司；行业重点型、重大新闻重点型必须列出 2–4 家待研究公司或角色；公司对比型必须列出至少 2 家公司及共同比较问题
- 行业聚集度 >2 的涨停行业必入候选（这是"市场当前在奖励什么"的最直接信号）
- 与投研赛道的映射要显式说明（如汽车零部件涨停 → 映射智能制造/出海链）

### Known Issues

- 涨停行业分布偏向短线情绪，不是所有映射都适合研究型视频——P3 规律匹配会过滤

## Phase 3: rule-match — 规律匹配与去重

### Goal

候选池 × account-rules 规律打分，并与上一轮复盘候选做适配判断（已验证规律权重高），剔除已做选题与不符合的。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| account-rules.md | input | 必选 | 本项目 outputs/ | 规律权重：已验证>假设中 |
| published-works.md + 复盘册 | input | 必选 | 源项目 + 本项目 | 去重 |

### Input

候选池 + 规律库 + 去重基线。

### Output

排名后候选（至少 8 个，覆盖四类重点范围）+ 每候选的规律匹配明细（命中哪条规律、证据什么）。

### Quality Criteria

- 已有选题（published-works/复盘册出现过的公司或同题材）必须剔除或明确标注"已在做"
- 排序依据：规律匹配优先于信号强度（信号强度是必要不充分条件）
- 无规律命中的候选必须标注 0 命中（经验性候选，权重低格）

### Known Issues

- 规律库还只有 1 支视频的数据（R1–R4 全"假设中"），初期匹配更多是方向性不是硬性

## Phase 4: topic-card — 结构化选题卡生成

### Goal

从四类重点范围中生成 6–8 张结构化选题卡。卡片优先按证据质量排序，不以单日涨幅机械排序；需要给人看的交接摘要可以从结构化字段渲染，但不再把长提示词作为必交产物。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| boundary-rewrite | skill | 必选 | workspace · .ai/skills/boundary-rewrite | 选题卡表述合规（不荐股不预测） |
| video-hook-intro | skill | 可选 | workspace · .ai/skills/video-hook-intro | 卡内钩子方向线索 |

### Input

Phase 3 排名候选 + 上一轮复盘改进候选池。

### Output

选题卡（6–8 张）。每张卡结构：

```
### 卡 N｜重点范围｜公司/题材
- `focus_type`：company / industry / news / comparison
- `subject_type`：company / industry / theme / event / comparison
- 观众问题：本期要回答的可验证问题
- 内容承诺：观众看完能理解什么
- 核心冲突：市场叙事与待核验事实之间的张力
- 研究对象：公司或公司角色列表；行业/新闻卡必须有 2–4 家
- 证据线索：信号 JSON / 新闻 / 公告待核验引用
- 复盘约束：`candidate_id`、适用性、具体实现、观察指标、阈值；不适用也要写原因
- 叙事方向：可选原型与自由度，不固定章节
- 封面方向：主标题与副标题
- `handoff_view`：可选的人类阅读交接摘要；不作为生产事实源
```

### Quality Criteria

- 每张结构化卡必须含研究起点（公司/公司角色 + 数据来源提示）与内容方向；不再强制生成独立生产提示词
- 每张卡必须列出适用的复盘候选、适配理由和在本选题中的实现方式；没有适配候选时写明原因
- 表述不涉及买卖建议/目标价/预测点位（boundary-rewrite 边界）
- 与已做过的视频角度不同（去重已在 P3）
- 结构化卡必须写明内容范围、公司角色和结论落点；行业/产业链卡优先考虑“行业问题 → 几家公司 → 特殊公司”，但公司数量由证据决定
- 选题卡必须给出封面主角与大字方向：行业、产业链或公司三者择一，封面只保留手机缩略图可读的大字
- 选题卡必须标注 `focus_type`：`company`（公司重点）、`industry`（行业重点）、`news`（重大新闻重点）或 `comparison`（公司对比重点）
- 审批区必须给出四类卡片数量，并说明缺失类别的具体原因

### Known Issues

- 提示词段是选题方向，不是研究结论；研究工作仍由 production 链路完成

## Phase 5: approve — 用户审批与移交

### Goal

用户审批选题卡 → 移交 investment-research-video（topic-gen 或直接进入研究期）。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| 用户确认 | input | 必选 | — | 唯一审批人 |
| finance-content-engineering | skill | 移交后必选 | workspace · .ai/skills/ | 接收 topic-gen |

### Input

Phase 4 选题卡 + 用户选择。

### Output

选定选题卡（≥1 张），登记"移交"记录到该卡与 `logs/`；该批准 topic card 连同其中的复盘候选适配内容，作为生产 Workflow 的唯一视频输入。

### Quality Criteria

- 审批记录含日期、选卡编号、用户备注
- 移交后 production 项目只消费批准 topic card；本 Workflow 不越级决定研究事实、最终叙事结构或渲染实现

### Known Issues

- 若用户全否，记录原因回馈 P2（信号映射盲区），下周期调参与
