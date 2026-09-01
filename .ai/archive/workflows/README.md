# Archive: Workflows（v0.2.2 归档）

> 本表为溯源/导航信息，不构成执行契约；语义以对应 Workflow SOP 与 skill.yaml/agent.yaml 为准

## 归档清单（2026-08-15，转换人 v0.2.2，Spec: deep-interview-v022-architecture-convergence）

| 原位置（workflow.yaml） | 归档位置 | 转换日期 | 新 SOP 位置 |
|---|---|---|---|
| `projects/investment-research-system/workflows/listed-company-research-production/workflow.yaml` | `.ai/archive/workflows/projects/investment-research-system/listed-company-research-production/workflow.yaml` | 2026-08-15 | `projects/investment-research-system/workflows/listed-company-research-production/workflow.md` |
| `projects/investment-research-system/workflows/listed-company-research-video-production/workflow.yaml` | `.ai/archive/workflows/projects/investment-research-system/listed-company-research-video-production/workflow.yaml` | 2026-08-15 | `projects/investment-research-system/workflows/listed-company-research-video-production/workflow.md` |
| `projects/investment-research-system/workflows/listed-company-video-production/workflow.yaml` | `.ai/archive/workflows/projects/investment-research-system/listed-company-video-production/workflow.yaml` | 2026-08-15 | `projects/investment-research-system/workflows/listed-company-video-production/workflow.md` |

- 转换动作：原 workflow.yaml（YAML DAG 程序流程）转为 Markdown SOP（导演手册），旧文件完整移入归档，无删除无丢失。
- 每个 SOP 的 Phase 结构、Required Resources（by-name）、Input/Output、Quality Criteria、Known Issues 均继承自原 workflow.yaml 与其引用的 capability.yaml 资源字段（archive/capabilities/README.md 有映射）。
- 转换人：v0.2.2（team v022-arch-convergence，worker-1 执行 Phase 0+1）。

## Provenance 注记（deferred M2）

`projects/investment-research-system/CLAUDE.md` 的「Required Capabilities and Resources」清单与「每个 Workflow 步骤先按 Capability 验收」措辞为 **deferred 项**：由项目侧在项目仓库提交 v0.2.2 三层同步（Project → Workflow → Skill/Agent）时另行更新；本计划不跨仓库修改项目文件。在本注记落盘之前，项目 CLAUDE.md 的旧措辞不代表本归档的契约语义。
