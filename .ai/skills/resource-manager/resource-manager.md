# resource-manager

> 管理资产：`.ai/skills/resource-manager/resource-manager.md`；安装实体：`.claude/skills/resource-manager/`

## 元数据

| 字段 | 值 |
|---|---|
| name | resource-manager |
| kind | skill |
| description | 注册、安装、更新、验证和归档 Skill/Agent 以及跨项目复用的媒体与设计资源 |
| source | internal · `.claude/skills/resource-manager/` |
| installed_ref | internal |
| runtime | both |
| invocation | `$resource-manager`；资源新增、更新、注册、验证或归档时调用 |
| requirements | 读取 `.ai/templates/` 字段模板；外部资源先放临时目录审查；不记录密钥 |
| update | internal · 随 workspace 规则更新；验证：读取当前 SKILL.md 并执行对应资源引用检查 |
| 辅助脚本 | — |
| 经验引用 | — |

## 调用

统一维护 `.ai/skills/`、`.ai/agents/`、`.ai/assets/` 和唯一安装树 `.claude/skills/` 的边界、来源、installed_ref、调用方式与验证方法。外部安装实体不直接改写；本地调用说明和辅助脚本放在资源记录中。

## 注意事项与踩坑

- 字段清单必须来自 `.ai/templates/`，不能在 Manager 中自行扩展。
- 资源记录只写技术调用，不写项目专属角色、公司事实或质量评分。
- `.claude/skills` 是 workspace 唯一 Skill 安装根；`.agents/` 只保存 Agent 定义，禁止存在 `.agents/skills`。
- `.codex/skills` 必须保持指向 `../.claude/skills` 的单一目录软链接，不创建逐 Skill 链接。
