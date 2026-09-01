# hyperframes-animation

> 管理资产：`.ai/skills/hyperframes-animation/hyperframes-animation.md`；安装实体：`.claude/skills/hyperframes-animation/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | github · https://github.com/heygen-com/hyperframes |
| installed_ref | c32b804 · HyperFrames bundled skill |
| runtime | both |
| 调用入口 | 按实体定义选择 2–4 个 motion rules、blueprint 或 runtime adapter；使用 `animation-map.mjs` 做动态审计 |
| 要求 | HyperFrames Composition、可 seek timeline；使用 GSAP/Lottie/Three.js 等 adapter 时遵守实体限制 |
| 更新 | git · 随 HyperFrames 官方技能套件更新；验证：运行 animation map 并对关键时间点 snapshot |
| 辅助脚本 | `scripts/animation-map.mjs`：审计动画实例、时间和 seek-safe 状态 |
| 经验引用 | — |

## 调用说明

负责多节拍 Scene、数据动画、转场、文字动效和可复现 seek 状态。它只执行导演已经确定的 visual intent，不自行新增公司事实或重排话题。
