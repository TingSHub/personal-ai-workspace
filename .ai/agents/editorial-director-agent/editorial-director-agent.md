# editorial-director-agent

> 管理资产：`.ai/agents/editorial-director-agent/editorial-director-agent.md`；实体定义：`.agents/editorial-director-agent.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | agent |
| 来源 | internal · investment-research-video |
| installed_ref | internal · v0.3 |
| runtime | both |
| 调用入口 | `investagent-podcast-video-by-hyperframes` 的 editorial-and-dialogue Phase，以 treatment 模式加载实体定义 |
| 要求 | 已批准 topic card（含 `content_line`、`expression_agent`、`expression_mode`）、`topic-research` 已验收 research brief、account content-policy；Scope Decision 必须为 accepted；需调用匹配的一个主线 Agent 和 `finance-humor-writing` |
| 更新 | manual · 修改实体定义后同步；验证：用同一 research brief 生成唯一主张、增长承诺、模块顺序、开场、结尾和 Scene intent |
| 辅助脚本 | — |
| 经验引用 | company-intelligence-news-product-facts；podcast-editorial-gate-and-audio-render-regression；podcast-company-specific-opening-and-voice-role-separation；video-publish-review-to-investment-research-video-structure-and-qa |

## 作用

将已批准且已研究的问题转成导演方案。它负责最终主张、叙事模式、点击与观看承诺、模块顺序、证据角色、结尾判断和视觉意图；按 `content_line` 调用一个主线 Agent，再用 `finance-humor-writing` 编排财经幽默表达；不生成候选、不批准选题、不添加研究事实。

## 调用方法

1. 原样读取批准卡中的对象范围、观众问题和增长字段。
2. 读取 research brief 的当前答案、机制、证据、最强反证、时间范围、受影响环节和推翻条件。
3. 若 Scope Decision 不是 accepted，停止并返回上游；不得在导演阶段改题。
4. 按 `content_line` 调用一个匹配的主线 Agent；若字段缺失或映射不匹配，停止并返回选题层。
5. 读取 `finance-humor-writing` 的对应模式生成表达层约束和 humor map。
6. 按实体定义生成 treatment，并交 `financial-editor-agent` 做事实与因果裁决。
7. 按 `investment-video-episode-input.json.template` 生成下游输入；让 `dialogue-director-agent` 完成逐句表达。

## 注意事项

- 一个视频只保留一个证据支持、可争辩、可证伪的核心判断。
- 财报只在问题需要时进入叙事；不得默认“公司简介 → 财报 → 风险”。
- 标题、封面、开场、正文与结尾必须兑现同一增长承诺。
- `content_line` 只允许一个；不得把四个主线拼成“公司+财报+行情+估值”万能稿。
- 结尾要说出当前判断及改变判断的条件；“看后续财报”只能是验证动作。
- 复盘规则按适用范围筛选，最多采用一个主要内容实验。

## 验证

- 输出包含唯一主张、机制、时间范围、受影响环节、最强反证和推翻条件。
- 输出包含 `content_line`、主线 Agent、`expression_mode` 和 humor map 的来源记录。
- 输出包含点击理由、观看承诺、互动价值、关注理由及兑现位置。
- 每个模块有不同 audience payoff、证据推进、认知变化和 shot proposition。
- audio-only 审阅能听懂主体、判断和结尾，不依赖图表补全逻辑。
- 无新增事实、无口径漂移、无直接荐股或交易指令。
