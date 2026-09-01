# hyperframes-cli

> 管理资产：`.ai/skills/hyperframes-cli/hyperframes-cli.md`；安装实体：`.claude/skills/hyperframes-cli/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | github · https://github.com/heygen-com/hyperframes |
| installed_ref | c32b804 · HyperFrames bundled skill |
| runtime | both |
| 调用入口 | `npx hyperframes check|snapshot|preview|render|catalog|add|doctor`；`validate`、`inspect`、`layout` 只视为历史别名 |
| 要求 | Node.js 22+、FFmpeg、Google Chrome；首次运行可能需要网络和项目依赖 |
| 更新 | git · 随 HyperFrames 官方技能套件更新；验证：`npx hyperframes doctor --json` 与项目 `npx hyperframes check` |
| 辅助脚本 | — |
| 经验引用 | — |

## 调用说明

提供 HyperFrames 的开发、检查、快照、预览、渲染、批量渲染和诊断循环。必须在上游内容、音频和 Composition 通过各自门禁后执行 render；不能用 CLI 代替研究或内容导演。

## 跨 Workflow 使用边界

- 默认顺序为 `lint → check → snapshot/preview → render`；render 只能消费已验收的 Composition 和媒体。
- FFmpeg 仅用于编码检查、mux、抽帧 QA 和必要封装；不得用多级 `xfade` 重建主时间轴。
