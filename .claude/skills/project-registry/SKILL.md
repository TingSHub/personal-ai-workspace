---
name: project-registry
description: 创建标准化项目——目录 + git init + 五件套（README/CLAUDE.md/AGENTS.md/project.yaml 顶层）+ 完整目录集 + 登记记录。当用户说"创建项目"、"新建项目"、"开一个新项目"时使用。
---

# Project Registry

创建标准化项目，让每个项目拥有统一入口与元数据。

> 本文同样受模板唯一事实源规则约束：project.yaml/CLAUDE.md/AGENTS.md 字段一律从 `.ai/templates/` 填充，禁止内联字段定义。

## 能力 1：create-project（创建项目）

输入：项目名称、描述

执行：

1. 创建目录 `projects/<project-name>/`
2. `git init`（独立仓库，与顶层仓库物理分离）
3. 从模板生成文件：
   - `README.md` —— 结构由本文定义（见下），不复制 README 模板
   - `CLAUDE.md` —— 从 `.ai/templates/CLAUDE.md.template` 填充
   - `AGENTS.md` —— 从 `.ai/templates/AGENTS.md.template` 填充
   - `project.yaml` —— 从 `.ai/templates/project.yaml.template` 填充（**项目顶层**，非 `.ai/` 下）
4. 初始化目录集：`workflows/` `docs/` `outputs/` `experience-candidates/` `logs/`
5. 写入登记记录 `.ai/projects/<project-name>.yaml` —— 从 `.ai/templates/project-registration.yaml.template` 填充，含 `registered:` 时间戳

## 能力 2：init-directories（补齐目录集）

对既有项目补齐缺失目录：`workflows/` `docs/` `outputs/` `experience-candidates/` `logs/`（项目结束时可将日志交给 Experience Curator；Project Registry 不生成或提升 Experience）

## 能力 3：create-project.yaml（创建/更新 project.yaml）

- 项目顶层 project.yaml，字段从模板读取：name/description/workflows[]
- `workflows[]` 用 by-name 引用

## 能力 4：create-project-workflow（创建项目 Workflow）

- 保存到 `projects/<project-name>/workflows/`
- 每个执行步骤引用 Global/Project Workflow 的 Phase 与其 Required Resources（by-name）
- 回填 project.yaml 的 `workflows[]`

## 能力 5：associate-global-workflow（关联 Global Workflow）

- 项目需要通用能力时，by-name 关联 `.ai/workflows/` 下的 Global Workflow
- 关联记录写入 project.yaml 的 `workflows[]`

## 项目 README.md 结构（散文文档，由本文定义）

- 项目名称与一句话描述
- `Goal`
- `## Resources Used` 小节：by-name 列出 Workflow Phase 实际使用的 Skill/Agent，**不用相对路径**
- `Workflows`：引用的 workflow by-name
- 文末可以说明 skill 的注册位置（如 `.ai/skills/docx/`）——该路径**仅作说明，不作为引用**

## Validation（操作后必须执行）

- `test -f projects/<name>/project.yaml`（**顶层**）且 `test -f projects/<name>/README.md` 且 `test -f projects/<name>/CLAUDE.md` 且 `test -f projects/<name>/AGENTS.md`
- 目录集存在：`test -d projects/<name>/workflows` 且 `test -d projects/<name>/docs` 且 `test -d projects/<name>/outputs` 且 `test -d projects/<name>/experience-candidates` 且 `test -d projects/<name>/logs`
- `test -f .ai/projects/<name>.yaml` 且含 `registered:`
- `grep -q "Resources Used" projects/<name>/README.md`
- `git -C projects/<name> rev-parse --is-inside-work-tree` 输出 true
