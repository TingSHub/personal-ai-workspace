# Projects

实际项目目录。每个子目录是**独立 Git 仓库**（各自 `git init`），拥有五件套：

- `README.md`
- `CLAUDE.md` / `AGENTS.md`
- `project.yaml`（项目顶层）
- `workflows/` / `docs/` / `outputs/` / `experience-candidates/` / `logs/`

本目录被顶层仓库 `.gitignore` 忽略（`projects/*`），项目代码永不进入顶层仓库。
项目登记索引见 `.ai/projects/`。

创建新项目：使用 Project Registry skill（`.claude/skills/project-registry/`）。
