---
name: project-registry
description: 创建或补齐标准化项目的 README、元数据与基础目录，使用工作区统一 Git 仓库，并为可选 Skill 封装保留必要材料。当用户说“创建项目”“新建项目”“开一个新项目”或要求调整项目创建规范时使用。
---

# Project Registry

创建标准化项目，让每个项目拥有统一入口与元数据，在真实交付中逐步积累未来可封装为 Skill 的方法与验证材料。转换完全可选，由用户按需发起。

> README.md/project.yaml 的结构和字段一律从 `.ai/templates/` 填充，不在本 Skill 另定义一份。项目默认以 README 为说明入口，沿用顶层 Agent 规则。

## 能力 1：create-project（创建项目）

输入：项目名称、描述

执行：

1. 检查 `projects/` 是否已有目标项目；存在则读取其说明并增量补齐，不覆盖已有内容。
2. 新项目创建目录 `projects/<project-name>/`，由工作区顶层 Git 仓库统一管理，不运行项目级 `git init`，不创建嵌套 `.git`。
3. 从模板生成文件：
   - `README.md` —— 从 `.ai/templates/project-readme.md.template` 填充
   - `project.yaml` —— 从 `.ai/templates/project.yaml.template` 填充（**项目顶层**，非 `.ai/` 下）
4. 初始化目录集：`workflows/` `docs/` `outputs/` `experience-candidates/` `logs/`
5. 按已知信息填充说明；未知项注明待验证，不伪造 Workflow、依赖或执行结果。脚本、测试、配置与样例按实际需要添加。
6. `projects/` 是项目入口，不另写 `.ai/projects/` 登记记录。仅在实际创建项目 Workflow 后回填项目元数据；尚无项目 Workflow 时按模板使用空列表。
7. 默认不生成项目级 AGENTS.md / CLAUDE.md。仅在用户要求或确有项目专属 Agent 指令时，按对应可选模板补充差异；现有文件保留，不自动删除。未来转换 Skill 时由 skill-creator 按目标环境补充真正需要的指令文件。

## 能力 2：init-directories（补齐目录集）

对用户要求补齐的既有项目，按实际缺项补齐基础目录并保留原内容。新约定在相关工作触及时渐进采用，不批量重写既有项目。Project Registry 不生成或提升 Experience。

## 能力 3：create-project.yaml（创建/更新 project.yaml）

- 项目顶层 project.yaml，字段从 `.ai/templates/project.yaml.template` 读取。
- Workflow 清单仅登记本项目实际存在的 Project Workflow，使用 by-name 引用。

## 能力 4：create-project-workflow（创建项目 Workflow）

- 交给 work-for-me 按 Workflow 模板创建 SOP、检查 by-name 资源引用，并回填项目元数据。
- 项目 README 标明入口；具体阶段、输入输出和验收标准保留在 SOP，不在 README 复制。

## 能力 5：associate-global-workflow（关联 Global Workflow）

- 项目需要通用流程时，在 README 或调用它的 SOP 中按名称引用实际存在的 Global Workflow。
- 项目元数据中的 Workflow 清单按模板仅登记 Project Workflow，不混入 Global Workflow。

## 日常维护与可选封装

- 以项目 README 模板为导航约定，创建时轻量填写，随真实任务补齐；主流程跑通后关联一个最小复跑案例，优先利用已有测试和验收材料。
- 稳定执行方法以 Workflow SOP 为唯一事实源；资源来源、安装版本与更新方法由 Resource Manager 的资源记录维护，项目按名称引用。
- 项目无需预建 Skill 包、转换状态、通用框架或跨环境安装器，也无需拆成多个 Skill。可选封装的交接方式见 README 模板，Project Registry 不自动启动转换。

## Validation（操作后必须执行）

- `test -f projects/<name>/project.yaml`（**顶层**）且 `test -f projects/<name>/README.md`；AGENTS.md / CLAUDE.md 不作为必备文件检查。
- 目录集存在：`test -d projects/<name>/workflows` 且 `test -d projects/<name>/docs` 且 `test -d projects/<name>/outputs` 且 `test -d projects/<name>/experience-candidates` 且 `test -d projects/<name>/logs`
- README 按项目 README 模板提供导航；创建时允许明确的待验证项，已声称跑通的主流程应有可定位的复跑与验收依据。
- 元数据中的 Project Workflow 均实际存在；README/SOP 中的 Global Workflow 与 Skill/Agent 引用可按名称解析。
- `git -C projects/<name> rev-parse --show-toplevel` 与工作区顶层一致，且项目内无 `.git` 目录或文件；不新建重复登记记录。遇到已有嵌套仓库时报告冲突，不自动删除或迁移。
