# 选题标题与文稿能力审计（2026-09-06）

## 结论

当前 `topic-forward` 的标题质量问题不是“少一个更会写标题的 Agent”，而是把三种不同产物混在了一个 `title` 字段里：

1. **研究标题**：准确锁定对象、范围和待回答问题，供 `topic-research` 交接。
2. **平台包装标题**：让陌生观众产生点击理由，允许同一研究问题生成多个角度。
3. **开场/文稿钩子**：把标题承诺在前 3–30 秒兑现，必须依赖已核验事实。

现有标题如“英方软件：数据保护需求，能否变成持续订单？”作为研究问题是合格的，但作为抖音标题偏平：主体前置、抽象名词多、`能否/还是/哪些指标`句式重复、没有具体冲突锚点，也没有告诉观众看完能判别什么。

## 当前 workspace 资源

| Resource | 最适合的环节 | 能解决什么 | 不能替代什么 |
|---|---|---|---|
| `topic-forward-lead` | 选题入口 | 多来源发现、去重、轻量核验、用户批准 | 不负责高点击标题变体 |
| `finance-content-engineering` | topic-gen / script-polish | 生成角度互斥候选；事实零漂移；口播传播检查 | 不做最终内容决策；当前模板没有 title-pack 输出 |
| `video-hook-intro` | 标题/开场/Scene 立题 | 2–4 个真实对比数字 + A/B 悬念；事实矛盾优先 | 没有研究事实时不能凭空造冲突 |
| `number-perception` | 研究后标题与开场 | 把利润率、倍数、规模差翻译成可感锚点 | 不负责内部数据核对 |
| `debate-rounds` | 有真实分歧的选题 | 多空、产品力/订单、价格/利润等双视角交锋 | 事实没有两面时不能硬造辩论 |
| `editorial-director-agent` | 批准+研究之后 | 把唯一主张、点击承诺、观看承诺、模块顺序、结尾条件统一起来 | 不生成候选、不批准选题、不新增事实 |
| `video-agent-writer` | 大纲之后 | 反常识/故事/问题开头，生成逐字稿和节奏 | 不是标题优化器 |
| `claude-youtube` | 标题/Hook/Metadata 辅助 | 5 种 Hook 机制、Search/Browse/Hybrid 标题思路、Retention Risk Map | YouTube 机制不能直接当作抖音基准；需财经合规包裹 |
| `marketing-content-creator` | 泛平台文案备选 | 多平台内容表达和故事包装 | 不是事实源，也不是财经边界裁决器 |

## 外部调研结果

### 1. 平台官方方向

- YouTube 官方把标题分为“可搜索”和“引发好奇”两类，同时要求标题准确、简洁、重要词靠前，并建议用受众实际观看和 CTR 数据迭代。[YouTube 标题与缩略图建议](https://support.google.com/youtube/answer/12340300?hl=en-GB)
- TikTok 官方创意指南强调：前 3 秒交代内容命题，前 6 秒完成 Hook，并用悬念、惊讶或情绪建立注意力；同时建议持续测试明显不同的创意版本。[TikTok Creative Best Practices](https://ads.tiktok.com/resources/help/article/creative-best-practices)
- 这两条对本账号的共同启发是：标题不能只描述研究对象，必须预告一个可兑现的认知收益；标题、封面和开场要共同兑现同一个承诺。

### 2. 外部 Agent Skill

- `sergebulaev/youtube-skills`：包含 Title Optimizer、Hook Scripter、Thumbnail Brief、Audience Insights 等 9 个 Skill；Title Optimizer 输出 3–5 个按目标标注的标题变体，Hook Scripter 写长视频前 30 秒。它适合作为标题变体生成器的外部参考，但必须接 `finance-content-engineering` 和 `boundary-rewrite`。[GitHub](https://github.com/sergebulaev/youtube-skills)
- `vyralcontent/content-skills`：包含 `viral-hooks`、`viral-short-form-ideas`、`viral-tiktok-content` 等，强调多版本 Hook、视觉/口播/屏幕文字三层钩子和评论/趋势挖掘。它更适合抖音短切和开头实验，不适合作为财经研究长视频的事实和标题主引擎。[GitHub](https://github.com/vyralcontent/content-skills)
- 这两个外部资源都值得“参考或隔离试用”，暂不建议直接纳入主 SOP：前者偏 YouTube 包装，后者偏通用短视频；它们都没有本地财经事实分级、合规和研究批准闸门。

### 3. 标题心理机制

关于 curiosity gap 的研究说明，具体指代、比较级和强化词可以让观众意识到“我知道对象，但不知道关键关系”，从而产生信息缺口；但如果标题只制造缺口、不提供对应事实兑现，就会变成 clickbait。[Clickbait、relevance 与 curiosity gap 研究](https://www.sciencedirect.com/science/article/pii/S0378216621000229)

因此本账号需要的是“有边界的好奇”：让观众知道要验证哪个机制，而不是用“真相”“万万没想到”一类空泛词吊胃口。

## 建议的标题工程

### A. 把一个 `title` 拆成 `research_title` 与 `title_pack`

建议未来模板增加：

```json
{
  "research_title": "英方软件：数据保护需求能否穿透到持续订单？",
  "title_pack": [
    {
      "title": "英方软件涨了12%，订单真的跟上了吗？",
      "mode": "signal-to-proof",
      "anchor": "行情信号 + 订单兑现",
      "viewer_payoff": "看懂需求、订单、回款三者的验证顺序",
      "evidence_status": "signal_only",
      "risk": "正式发布前必须核验涨幅日期和口径"
    }
  ],
  "cover_pack": ["涨的是订单？", "需求在哪兑现？"],
  "opening_promise": "前5秒说清当前能确认什么、还缺哪一张证据",
  "title_body_match": "pending_research"
}
```

`research_title` 进入研究交接；`title_pack` 先做候选包装，研究完成后再生成最终版；`opening_promise` 交给 `editorial-director-agent` 和 `video-hook-intro`；封面短句单独控制，避免与标题重复。

### B. 每张卡强制生成 5 种不同机制

1. **信号→证据**：`英方软件涨了12%，订单真的跟上了吗？`
2. **事实矛盾**：`数据保护很热，为什么还要等订单证明？`
3. **具体判别**：`英方软件要过关，先看订单、回款还是利润？`
4. **机制悬念**：`一笔数据安全订单，怎样才算真的兑现？`
5. **双视角**：`涨的是数据保护，还是订单兑现预期？`

候选必须标注证据状态：`signal_only`、`lightly_verified`、`research_verified`。没有研究证据时不能把推测写成事实。

### C. 标题评审门槛

每个候选标题按 0–2 分检查，不做机械总分替代判断：

- **一眼懂对象**：观众是否知道讲谁/什么机制？
- **冲突具体**：是否有两个事实方向相撞，而不是只有“能否/如何/为什么”？
- **锚点可感**：是否有数字、订单、回款、价格、库存、客户或一个明确动作？
- **收益明确**：看完能解决哪个判断问题？
- **好奇有边界**：缺口是否能被正文兑现？
- **移动端可读**：重要词是否靠前，是否需要读两遍？
- **标题—封面互补**：封面是否提供第二个信息，不是把标题再抄一遍？
- **财经合规**：没有荐股、目标价、收益保证和把行情写成基本面结论。

任一标题若“冲突具体”和“收益明确”均为 0，直接淘汰；得分高也必须经过 `boundary-rewrite` 和事实核对。

## 推荐调用链

### 选题阶段（当前最需要补强）

`topic-forward-lead` → `finance-content-engineering(topic-gen)` → `video-hook-intro` → `number-perception(有数字时)` → `boundary-rewrite` → 用户批准

产物增加 `title-pack.md/json`，不改变用户只批准一个 topic 的闸门。

### 研究之后

`topic-research` → `research-intelligence-agent` → `editorial-director-agent` → `video-hook-intro` + `number-perception` → `finance-content-engineering(script-polish)` → `video-agent-writer`

这时才把 `signal_only` 标题升级为 `research_verified`，并锁定标题、封面、开场和正文的同一增长承诺。

## 对当前 TOPIC-01 的示例

以下只是包装假设，不是最终发布标题：

| 机制 | 示例 | 风险 |
|---|---|---|
| 信号→证据 | 英方软件涨了12%，订单真的跟上了吗？ | 需核验信号日期和涨幅口径 |
| 事实矛盾 | 数据保护很热，订单为什么还没成为答案？ | “很热”需有来源支撑 |
| 判别问题 | 英方软件要过关，先看订单、回款还是利润？ | 更稳，但冲击力较弱 |
| 机制悬念 | 一笔数据安全订单，怎样才算真正兑现？ | 需正文明确兑现条件 |
| 双视角 | 涨的是数据保护，还是订单兑现预期？ | 不能暗示任何交易判断 |

## 最终建议

优先做一个本地轻量的 `finance-title-packaging` Skill，而不是马上安装一堆外部 Agent。它只做标题/封面/开场候选和淘汰记录，调用现有 `video-hook-intro`、`number-perception`、`boundary-rewrite`，并把 `editorial-director-agent` 留在研究之后。

外部 `youtube-skills` 可作为标题变体生成器的 A/B 参考；`vyralcontent/content-skills` 作为短视频 Hook 参考。若后续要做实时关键词和竞品标题数据，再单独评估 vidIQ 类外部工具，不让它替代研究事实或用户批准。
