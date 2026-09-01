# hyperframes-core

> 管理资产：`.ai/skills/hyperframes-core/hyperframes-core.md`；安装实体：`.claude/skills/hyperframes-core/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | github · https://github.com/heygen-com/hyperframes |
| installed_ref | c32b804 · HyperFrames bundled skill |
| runtime | both |
| 调用入口 | 编写或审查 HyperFrames Composition 前读取；按实体契约使用 `data-*`、tracks、clips、sub-compositions、variables 和 deterministic render |
| 要求 | HyperFrames 项目、Node.js 22+、可 seek 的 Composition DOM；需要时使用浏览器和 FFmpeg |
| 更新 | git · 随 HyperFrames 官方技能套件更新；验证：`npx hyperframes check` 与最小 Composition snapshot |
| 辅助脚本 | — |
| 经验引用 | — |

## 调用说明

提供 Composition 的结构、时间、媒体归属和确定性渲染契约。财经播客中它是 Scene、音频、字幕、章节和全局累计时间线的技术边界，不承担内容主线判断。

## 跨 Workflow 使用边界

- 使用 `data-*` 时序、tracks、clips 和 sub-compositions 表达正式时间轴；不得用截图或第二套 HTML 代替正式 Composition。
- 真实时间应由已验收音频或上游明确的 timing contract 注入；内容、事实和章节顺序由上游编辑/导演产物决定。
