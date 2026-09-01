# workflow-registry

> 管理资产：`.ai/skills/workflow-registry/workflow-registry.md`；安装实体：`.claude/skills/workflow-registry/`

## 元数据

| 字段 | 值 |
|---|---|
| name | workflow-registry |
| kind | skill |
| description | 按统一 Markdown SOP 模板创建、索引、查看、修改和归档 Global/Project Workflow |
| source | internal · `.claude/skills/workflow-registry/` |
| installed_ref | internal |
| runtime | both |
| invocation | `$workflow-registry`；创建、修改、索引或归档 Workflow 时调用 |
| requirements | 读取 `.ai/templates/workflow.md.template`；Required Resources 必须使用 by-name |
| update | internal · 随 workspace 规则更新；验证：六章节、Phase 字段和资源引用解析检查 |
| 辅助脚本 | — |
| 经验引用 | — |

## 调用

Workflow Markdown 是唯一事实源，registry 只维护位置、分类、项目关联和 Required Resources 索引，不解释或替代 SOP。每个 Phase 的资源必须真实执行并留下独立产物。

## 注意事项与踩坑

- Global Workflow 位于 `.ai/workflows/<category>/<name>/workflow.md`，Project Workflow 位于项目仓库。
- SOP 必须包含 Mission、Input、Output、Principles、Phase 和 Evolution Log。
- 归档 Workflow 前先由 Experience Curator 处理仍有复用价值的经验，并取得用户确认。
