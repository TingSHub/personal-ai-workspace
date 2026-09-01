# experience-curator

> 管理资产：`.ai/skills/experience-curator/experience-curator.md`；安装实体：`.claude/skills/experience-curator/`

## 元数据

| 字段 | 值 |
|---|---|
| name | experience-curator |
| kind | skill |
| description | 从真实项目证据中筛选、去重和沉淀可复用 Experience，并在用户确认后回写目标 Workflow/Skill/Agent |
| source | internal · `.claude/skills/experience-curator/` |
| installed_ref | internal |
| runtime | both |
| invocation | `$experience-curator`；项目复盘、经验候选、沉淀踩坑和文档回写时调用 |
| requirements | 项目日志/交付物/验证证据；字段读取 `.ai/templates/experience.md.template`；回写必须获得用户明确确认 |
| update | internal · 随 workspace 规则更新；验证：候选 frontmatter、owner、证据、回写和归档索引检查 |
| 辅助脚本 | — |
| 经验引用 | — |

## 调用

先生成 Candidate，判定它是否会改变未来 Workflow、资源调用、质量检查或脚本；用户确认后再 promote、回写目标资产、回填 `experience_refs[]` 并归档。

## 注意事项与踩坑

- 原始日志不进入资产库；普通命令输出和无证据建议不构成 Experience。
- 正式回写追加带来源标记的条目，不与资源 Manager 在同一文件无分区直写。
- 可机械化的人工检查应沉淀为参数化、纯标准库脚本并做最小验证。
