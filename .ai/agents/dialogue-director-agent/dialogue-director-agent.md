# dialogue-director-agent

> 管理资产：`.ai/agents/dialogue-director-agent/dialogue-director-agent.md`；实体定义：`.agents/dialogue-director-agent.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | agent |
| 来源 | internal · created for investagent-podcast-video-by-hyperframes |
| installed_ref | internal · v0.2 |
| runtime | both |
| 调用入口 | Phase 2 Required Resources 的 by-name `dialogue-director-agent`；加载实体定义执行 |
| 要求 | 已验收母稿或 Editorial Master、同一期 `content-collaboration.md`、topic-evidence-matrix、account-profile、content_line treatment、content_depth、knowledge route 和事实锚定 humor map；默认执行 `host_analyst`，仅显式 `debate` 时加载 debate-rounds；输出必须包含 format/role/reply/interaction/emotion/delivery 字段 |
| 更新 | manual · 修改顶层实体定义后同步；验证：用一个话题生成 6–8 个交替 turn，检查回应关系、证据引用和企业研究边界 |
| 辅助脚本 | — |
| 经验引用 | published-video-dialogue-caption-visual-sync |

## 作用

双人财经播客对话导演：把已审核母稿和研究证据编排成语义互相回应的回合制对话，同时共同决定口播文本、情绪和 delivery。它解决的是“speaker alternation 通过、但两个人各念各的”问题；在 `manual` 模式下，先把口播草案和审核请求写入同一份 `content-collaboration.md`，审核通过后才锁定 episode。

## 实体位置

- `.agents/dialogue-director-agent.md`——完整职责、生成模型、字段契约、边界和下游交接。

## 调用方式

- 输入：已验收母稿、研究资产、账号主持人 profile、话题顺序、证据矩阵、批准卡的 `content_line`、表达层 humor map 和 `content-collaboration.md` 中的人工反馈。
- 输出：口播审核通过后的 episode.json、debate-script.md、dialogue-map.json、执行记录；口播草案和审核意见先原位写入 `content-collaboration.md`。
- 调用顺序：Financial Editor 之后，podcast-audio-compiler 之前。

## 注意事项与踩坑

- 不把“两个 speaker 交替”当成对话完成；必须有语义回指和回应动作。
- 不跨越批准的 `content_line`；幽默只作为观众承接和机制解释，不产生新的研究主张。
- 不把情绪标签当作情绪音频保证；TTS 需要消费 account-profile 的情绪参考资产或明确的 style adapter。
- 不新增研究事实，不自行改数字口径，不把自然口播舍入变成事实舍入。
- 不使用上游短视频的时长、平台钩子或恐惧叙事作为长篇财经播客规则。
- 踩坑（2026-09-07 猪周期）：顾慎言句首单音节会被吞音/黏连，标点无法稳定制造停顿——已在实体定义 §4/§5/§6 写入“不得以对/嗯/好起句”；问号句必须 `delivery=rising_question`（问号不保证升调）；含数字 turn 必须同时给 `text`/`display_text` 且数值等价。
