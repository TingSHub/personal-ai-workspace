# hyperframes-creative

> 管理资产：`.ai/skills/hyperframes-creative/hyperframes-creative.md`；安装实体：`.claude/skills/hyperframes-creative/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | github · https://github.com/heygen-com/hyperframes |
| installed_ref | c32b804 · HyperFrames bundled skill |
| runtime | both |
| 调用入口 | 按实体定义读取 design spec、house style、palette、beat direction、narration 和 composition pattern |
| 要求 | 已确定的内容/导演意图、HyperFrames Composition；动画细节转交 `hyperframes-animation` |
| 更新 | git · 随 HyperFrames 官方技能套件更新；验证：读取实体并完成一条视觉 spec 到 Composition 的 check |
| 辅助脚本 | `scripts/contrast-report.mjs`：审计视觉对比度和颜色可读性 |
| 经验引用 | — |

## 调用说明

负责视觉方向、排版、色板、节奏和品牌一致性。财经播客默认从 account-profile 读取 editorial-paper 视觉 Token；本 Skill 不负责重新选择选题。
