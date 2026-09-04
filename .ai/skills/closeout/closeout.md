# Skill: closeout

> 位置: `.ai/skills/closeout/`

## 元数据

| 字段 | 值 |
|---|---|
| name | closeout |
| kind | skill |
| description | 显式执行任务收尾、目录结构审查、经验候选、批准后应用与本地提交 |
| source | internal · personal-ai-workspace |
| installed_ref | internal |
| runtime | both |
| invocation | 显式调用 `$closeout`；默认 review，结果直接返回对话，批准后再 apply |
| requirements | Git；Python 3.10+；读取 closeout-and-commit、当前任务产物和 `.ai/templates/` |
| update | internal · 修改安装实体与本记录后运行 quick_validate、结构扫描器自测及 Workflow by-name 检查 |
| 辅助脚本 | `.claude/skills/closeout/scripts/scan_workspace_structure.py`：一方 Skill 实体内的提交前只读扫描器；review/apply postflight 时使用 |
| experience_refs[] | — |

## 调用说明

这是 `closeout-and-commit` 的显式入口。Workflow 保持单一编排事实源；本 Skill 负责稳定触发、审批边界和 workspace 目录扫描。由于它是 workspace 一方 Skill，辅助脚本与可执行实体同置于 `.claude/skills/closeout/`；外部 Skill 仍按 Resource Manager 规则将本地调用辅助放在 `.ai/skills/<name>/`。

- `review` 只在对话中返回基线、目录审查和审批提案；除非用户明确要求审计记录，否则不生成文件。
- `apply` 只执行用户按提案 ID 批准的目录、经验、文档和提交动作。
- `commit-only` 可跳过经验蒸馏，但不能跳过完成度、目录、密钥、范围和 staged diff 检查。
- `distill-only` 只处理经验与文档候选。

目录扫描器只报告事实和高置信度候选；“归属是否准确、结构是否可扩展”仍需结合任务语义审阅。外部安装实体、虚拟环境、运行缓存和大型依赖目录不能仅因体积或层级被建议重组。
