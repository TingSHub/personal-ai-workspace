# docx

> 管理资产：`.ai/skills/docx/docx.md`；安装实体：`.claude/skills/docx/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | github · https://github.com/anthropics/skills (skills/docx) |
| installed_ref | tree-sha256:3fa56fe41065 |
| runtime | both |
| 调用入口 | $docx |
| 要求 | Skill 声明的文档处理依赖 |
| 更新 | git · 从上游仓库获取 skills/docx 到临时目录，对比后替换安装实体；验证：创建并重新读取一个最小 docx |
| 辅助脚本 | — |
| 经验引用 | — |

创建、读取、编辑、分析 Word 文档（.docx / .dotx），含目录、页眉、页码、表格、邮件合并等格式能力。

## 来源

- 仓库：https://github.com/anthropics/skills（官方）`skills/docx`
- 由 Resource Manager 管理

## 安装说明（licensing 注记）

- 已安装到本 workspace：`.claude/skills/docx/`（含 SKILL.md、LICENSE.txt、scripts/）
- Codex 入口：`.codex/skills/docx`（由 `.codex/skills` 目录级映射自动提供）
- **License：Proprietary（source-available）**——LICENSE.txt 含完整条款；个人/私有使用无碍，**避免公开再分发安装副本**
- 安装实体自带的 `scripts/` 属于第三方内容；本地辅助脚本如有新增，放入资源资产目录而不修改安装实体

## 使用

触发场景：创建/编辑 Word 文档、处理 .docx 文件。实现方式：`docx`(npm) 脚本创建、`unzip`→编辑→`zip` 编辑已有文档、`pandoc -t markdown` 读取内容。
