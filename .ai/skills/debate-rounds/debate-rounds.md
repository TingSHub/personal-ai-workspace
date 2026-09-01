# debate-rounds

> 管理资产：`.ai/skills/debate-rounds/debate-rounds.md`；安装实体：`.claude/skills/debate-rounds/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | workspace external skill · distilled from reference podcast format |
| installed_ref | local-installed · current `.claude/skills/debate-rounds/SKILL.md` |
| runtime | both |
| 调用入口 | `$debate-rounds` |
| 要求 | Editorial Master；双方可辩证据；speaker-tagged script；number-perception 与 boundary-rewrite companion skills |
| 更新 | 保留本地记录；更新安装实体后重新审阅回合契约和测试提示 |
| 辅助脚本 | — |

## 作用

为双人财经播客生成预编排回合制结构：矛盾立题 → 空方立论 → 多方“你这话没错，但…”反击 → 连环新证据 → 类比降维 → 收束 → 转场 → 双总结 → 互动钩子。

## 调用约束

- 每个话题必须有独立事实矛盾，不能为了制造冲突改写证据。
- 每句话带 `turn_id`、`topic_id`、`speaker`、`evidence_ids`，直接供逐句音频编译器消费。
- 推荐 5–9 个话题；长篇节目默认 8–9 个话题，目标时长由 account-profile 决定。
- 双方均需有可辩证据；若无双向证据，退回单口叙事弧。
- 不生成目标价、评级、买卖建议、仓位或交易策略。

## 已知限制

- 本 Skill 负责预编排，不负责 TTS、音频拼接、字幕对齐或 HyperFrames 渲染。
- 不能把两段长旁白标成“双人播客”；必须由下游逐句编译器执行 speaker turn。
