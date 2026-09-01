# 模板归档索引

归档日期：2026-08-15
归档原因：v0.2.2 架构收敛——Workflow 从 YAML DAG 转为 Markdown SOP，Capability 层退役，旧架构模板不再承担生成职责。

## 归档模板

| 文件 | 来源 | 原用途 | 替代 |
|---|---|---|---|
| `workflow.yaml.template` | `.ai/templates/`（V0.1.5 时代创建） | 生成 workflow.yaml（YAML DAG 程序流程：步骤、capabilities by-name、capability_result、acceptance） | `.ai/templates/workflow.md.template`（Markdown SOP：Mission/Input/Output/Principles/Phase/Evolution Log） |
| `capability.yaml.template` | `.ai/templates/`（V0.1.5 时代创建） | 生成 capability.yaml（能力契约：input/output/acceptance/selection/resources/execution_contract） | 无直接替代——Capability 层已退役；其 resources 注记语义由 Workflow SOP 的 Required Resources 表承担 |

## 保留未归档

- `research-resource-evaluation.yaml.template` 保留于 `.ai/templates/` 原位——仍被 research-intelligence-agent 的 AGENT.md 引用，且不含 capability 措辞。

> 本表为溯源/导航信息，不构成执行契约；语义以对应 Workflow SOP 与 skill.yaml/agent.yaml 为准。
