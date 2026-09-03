# Workflow: topic-forward-lead

> 位置: Project: projects/video-publish-review/workflows/topic-forward-lead/

## Mission

在复盘闭环的末端发现下一个视频话题：用免费市场信号（涨停池/涨幅异动/财经热点）+ 账号规律库（account-rules.md）自动生成 2–4 个选题卡，每张卡的提示词段可直接作为 investment-research-video 生产工作流的输入，让"发布 → 复盘 → 选题前瞻 → 生产"形成完整飞轮。

## Input

- 市场信号：`scripts/fetch_market_signals.py` 产物（`outputs/topic-signals-YYYY-MM-DD.json`：涨停池+涨幅榜）
- 财经热点：news-search / multi-search 当日/近 2 日关键词热度；social-trend-monitor 海外风向（可选）
- 账号规律：`outputs/account-rules.md`（P6 产物，已验证规律权重高于假设中）
- 去重基线：源项目 `published-works.md` + 全部复盘册（已做过的选题剔除）

## Output

`outputs/topic-forward-YYYY-MM-DD.md`：
- 信号摘要节：涨停行业聚集度 Top、涨幅榜异常、热点主题
- 候选池节：公司/题材候选（每个含信号证据：涨停/涨幅/换手/热点来源）
- 规律匹配节：候选 × account-rules 打分明细
- 选题卡节：2–4 张，每张含 公司/题材、信号证据、规律匹配、差异化角度线索、**生产提示词段**（可直接投喂 production workflow）
- 审批节：待用户确认；确认后移交 investment-research-video 的 topic-gen

## Principles

- best_available_resource：按实际效果、输出质量、稳定性、依赖成本、维护成本和当前项目适配性选择资源，禁止 local first；来源不构成优先级
- 真实执行留痕：Required Resources 必须真实执行并留下独立产物（含资源 by-name 与 installed_ref）；未执行不得写成已执行
- 免费优先：市场数据源用 akshare（免费无token，已实测），不引入收费源
- 信号要可追溯：每个选题卡的证据引用信号 JSON 的具体字段与新闻来源，不引用记忆
- 合规前置：选题卡表述过 boundary-rewrite 约定边界（不荐股、不预测点位）；选题本身倾向研究视角（财报可验证/证据链可展示）
- by-name 引用：Workflow / Skill / Agent / Experience 一律用 by-name 标识符

## Phase 1: signal-scan — 市场信号扫描

### Goal

跑行情信号脚本（涨停池+涨幅榜）并补热点新闻，产出信号摘要。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| fetch_market_signals.py | 脚本 | 必选 | 本项目 scripts/（akshare 免费接口封装） | 涨停池东财、全量行情新浪；板块资金流接口偶发断连，用涨停行业分布替代 |
| news-search | skill | 必选 | workspace · .ai/skills/news-search | 财经热点关键词热度 |
| multi-search | skill | 可选 | workspace · .ai/skills/multi-search | 交叉验证 |
| social-trend-monitor | skill | 可选 | workspace · .ai/skills/social-trend-monitor | 海外 AI/科技风向（映射国产题材） |

### Input

无（脚本自取当日数据；交易时段后跑，数据最全）。

### Output

`outputs/topic-signals-YYYY-MM-DD.json`（脚本产物）+ 信号摘要（涨停行业聚集度、涨幅榜异常、热点主题列表）。

### Quality Criteria

- 信号 JSON 含 captured_at/trade_date/errors（errors 非空必须标注降级）
- 涨停池行业分布统计完成；热点主题 ≥3 个（来自 news-search，含来源与时间）
- 非交易日运行要明确标注"非交易数据"，不得当有效信号

### Known Issues

- akshare 接口均为第三方免费源，偶发断连/变动；脚本有错误捕获与降级提示，失败该路即标注
- 新浪全量行情 + 东财涨停池是主通道；板块资金流是备选，不阻塞流程

## Phase 2: candidate-pool — 候选池构建

### Goal

从信号映射为公司/题材候选池（涨停行业聚集 → 映射 A 股投研题材；涨幅异动 → 与账号已做主题交叉）。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| 信号 JSON + 热点摘要 | input | 必选 | Phase 1 | — |
| finance-content-engineering（topic-gen 方法） | skill | 可选 | workspace · .ai/skills/finance-content-engineering | 角度互斥性检查 |

### Input

Phase 1 产物。

### Output

候选池表：候选（公司/题材）× 信号证据（涨停/涨幅/换手/新闻）→ 归一为 8–12 个原始候选。

### Quality Criteria

- 每个候选必须挂信号证据（无证据不放候选池）
- 行业聚集度 >2 的涨停行业必入候选（这是"市场当前在奖励什么"的最直接信号）
- 与投研赛道的映射要显式说明（如汽车零部件涨停 → 映射智能制造/出海链）

### Known Issues

- 涨停行业分布偏向短线情绪，不是所有映射都适合研究型视频——P3 规律匹配会过滤

## Phase 3: rule-match — 规律匹配与去重

### Goal

候选池 × account-rules 规律打分（已验证规律权重高），剔除已做选题与不符合的。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| account-rules.md | input | 必选 | 本项目 outputs/ | 规律权重：已验证>假设中 |
| published-works.md + 复盘册 | input | 必选 | 源项目 + 本项目 | 去重 |

### Input

候选池 + 规律库 + 去重基线。

### Output

排名后候选（3–6 个）+ 每候选的规律匹配明细（命中哪条规律、证据什么）。

### Quality Criteria

- 已有选题（published-works/复盘册出现过的公司或同题材）必须剔除或明确标注"已在做"
- 排序依据：规律匹配优先于信号强度（信号强度是必要不充分条件）
- 无规律命中的候选必须标注 0 命中（经验性候选，权重低格）

### Known Issues

- 规律库还只有 1 支视频的数据（R1–R4 全"假设中"），初期匹配更多是方向性不是硬性

## Phase 4: topic-card — 选题卡生成（含生产提示词段）

### Goal

为 Top 候选生成 2–4 张选题卡，每张含生产提示词段（可直接投喂 production workflow）。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| boundary-rewrite | skill | 必选 | workspace · .ai/skills/boundary-rewrite | 选题卡表述合规（不荐股不预测） |
| video-hook-intro | skill | 可选 | workspace · .ai/skills/video-hook-intro | 卡内钩子方向线索 |

### Input

Phase 3 排名候选。

### Output

选题卡（2–4 张）。每张卡结构：

```
### 卡 N｜公司/题材
- 市场信号：涨停 ×N / 涨幅 X% / 热点来源（日期）
- 规律匹配：命中 R-K（假设中）→ 价值点
- 差异化角度：只讲上涨→我们讲风险/验证现金流；只下结论→我们展示证据链
- 生产提示词段（可直接复制给 production workflow）：
  <提示词>
```

### Quality Criteria

- 每张卡生产提示词段 ≥80 字、包含研究起点（公司+数据来源提示）与内容方向
- 表述不涉及买卖建议/目标价/预测点位（boundary-rewrite 边界）
- 与已做过的视频角度不同（去重已在 P3）

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

选定选题卡（≥1 张），登记"移交"记录到该卡与 `logs/`，提示词段进入生产链路。

### Quality Criteria

- 审批记录含日期、选卡编号、用户备注
- 移交后 production 项目按正常 topic-gen 流程吸收，本 workflow 不越级干预生产过程

### Known Issues

- 若用户全否，记录原因回馈 P2（信号映射盲区），下周期调参与

## Evolution Log

| 日期 | 变更 | 依据 |
|---|---|---|
| 2026-09-02 | 初版：复盘飞轮的选题前端（免费数据源 akshare 替代 tushare 收费） | 用户需求：复盘后自动寻找下一视频话题；tushare 收费改 akshare（已实测跑通） |
