# media-use

> 管理资产：`.ai/skills/media-use/media-use.md`；安装实体：`~/.agents/skills/media-use/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | github · https://github.com/heygen-com/hyperframes |
| installed_ref | c32b804 · HyperFrames bundled skill |
| runtime | both |
| 调用入口 | 按实体定义使用 `resolve` / `generate` / `operate`；HyperFrames 项目中负责媒体解析、配音、字幕和媒体记录 |
| 要求 | Node.js、项目目录、对应媒体 provider；需要 provider 凭据时只读取配置名，不记录密钥 |
| 更新 | git · 随 HyperFrames 官方技能套件更新；审查入口、provider 和输出契约后替换安装实体；验证：运行 `resolve.mjs --doctor` |
| 辅助脚本 | `scripts/resolve.mjs`：解析或生成媒体并写入项目媒体记录；仅按实体说明调用 |
| 经验引用 | — |

## 调用说明

统一处理 HyperFrames 的音频、图片、图标、品牌素材、字幕和媒体复用。当前财经播客 Workflow 只把它用于已锁定音频的媒体接入和资产留痕，不让它重新决定内容或脚本。

本地实体位于用户级 Agent Skills 安装树，`.codex/skills` 已通过目录级链接映射；不要复制或修改外部实体。

## 跨 Workflow 使用边界

- 只消费已锁定的脚本、音频或媒体意图；不得重新决定研究内容、章节主线或事实表达。
- provider 缺失、身份不匹配或静默 fallback 时必须停在媒体门禁并记录降级，不得静默替换正式资源。
