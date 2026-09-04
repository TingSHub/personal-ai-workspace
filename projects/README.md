# Projects

实际项目目录。每个子目录由工作区顶层 Git 仓库统一管理，并拥有五件套：

- `README.md`
- `CLAUDE.md` / `AGENTS.md`
- `project.yaml`（项目顶层）
- `workflows/` / `docs/` / `outputs/` / `experience-candidates/` / `logs/`

项目源码、配置和工作流进入顶层仓库；运行产物、大文件和本地状态由根目录 `.gitignore` 排除。`projects/` 是活动项目和子项目的唯一入口，不再维护重复的项目登记索引。

创建新项目：使用 Project Registry skill（`.claude/skills/project-registry/`）。
