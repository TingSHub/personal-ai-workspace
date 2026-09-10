# work-for-me

> 管理资产：`.ai/skills/work-for-me/work-for-me.md`；安装实体：`.claude/skills/work-for-me/`

## 元数据

| 字段 | 值 |
|---|---|
| name | work-for-me |
| kind | skill |
| description | 按统一 Markdown SOP 模板创建、索引、查看、修改和归档 Global/Project Workflow，并路由执行任务：定位项目 → 匹配 Workflow → 读 SOP → 逐 Phase 真实执行 |
| source | internal · `.claude/skills/work-for-me/` |
| installed_ref | internal |
| runtime | both |
| invocation | `$work-for-me`；创建、修改、索引、归档 Workflow，或任务开始时定位并按 SOP 执行时调用 |
| requirements | 读取 `.ai/templates/workflow.md.template`；Required Resources 必须使用 by-name |
| update | internal · 随 workspace 规则更新；验证：Workflow 运行章节、Phase 字段、资源引用解析与复合 Workflow 子引用检查 |
| 辅助脚本 | `scripts/find-workflow.py`（关键词确定性查找 Workflow 候选，只列不推荐） |
| 经验引用 | — |

## 调用

Workflow Markdown 是唯一事实源：本 Skill 只维护位置、分类、项目关联和 Required Resources 索引，不解释或替代 SOP；路由只做确定性查找与按 SOP 顺序执行，不评分、不自动推荐、不调度。每个 Phase 的资源必须真实执行并留下独立产物。

## 注意事项与踩坑

- Global Workflow 位于 `.ai/workflows/<category>/<name>/workflow.md`，Project Workflow 位于 `projects/<project>/workflows/<name>/workflow.md`。
- SOP 必须包含 Mission、Input、Output、Principles 和 Phase；不要求历史变更章节，当前规则应直接写入对应运行章节。
- 归档 Workflow 前先由 Experience Curator 处理仍有复用价值的经验，并取得用户确认。
- route 是 Agent 按 SOP 的确定性查找与顺序执行（真实执行留痕），不是 DAG 调度器、状态机或自动推荐系统；多候选时交用户确认。
