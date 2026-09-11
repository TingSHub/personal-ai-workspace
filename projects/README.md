# Projects

实际项目目录。每个子目录由工作区顶层 Git 仓库统一管理，默认包含：

- `README.md`
- `project.yaml`（项目顶层）
- `workflows/` / `docs/` / `outputs/` / `experience-candidates/` / `logs/`

README 是项目说明入口，Agent 行为沿用顶层规则。项目级 CLAUDE.md / AGENTS.md 为可选文件，仅在有专属指令时添加；后续转换 Skill 时再按目标环境补充必要指令。

项目源码、配置和工作流进入顶层仓库；运行产物、大文件和本地状态由根目录 `.gitignore` 排除。`projects/` 是活动项目和子项目的唯一入口，不再维护重复的项目登记索引。

创建新项目：使用 Project Registry skill（`.claude/skills/project-registry/`）。

项目首先服务真实交付，也为未来按需封装 Skill 保留必要材料。新项目 README 从 `.ai/templates/project-readme.md.template` 生成，集中导航入口、输入输出、配置依赖与复跑依据；详细执行方法仍以 Workflow SOP 为准。探索期允许待验证项，主流程跑通后补充一个最小复跑案例。脚本、测试、配置和样例按实际需要添加，不预建 Skill 包。既有项目在相关工作触及时渐进补齐，无需批量迁移。
