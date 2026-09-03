# open-skill-finder

> 管理资产：`.ai/skills/open-skill-finder/open-skill-finder.md`；安装实体：`.claude/skills/open-skill-finder/`

## 元数据

| 字段 | 值 |
|---|---|
| name | open-skill-finder |
| kind | skill |
| description | Skill 发现与安全审计：多源搜索、证据卡片、安装前强制审计与用户批准 |
| source | github · https://github.com/30bewater/open-skill-finder · installed_ref c512648870b7d8db6334578711ea70884fd5bbe0（MIT） |
| runtime | claude / codex（Python 仅标准库，git/gh 可用即可） |
| invocation | 按 SKILL.md 工作流执行：probe → search（≥2 独立源）→ inspect（不执行候选脚本）→ rank → render 证据卡 → 用户批准后安装并验证 |
| requirements | Python 3.12 已验证；git/gh 已确认可用（probe_capabilities.py 输出 ok） |
| update | manual · 重新获取固定 commit 对比后替换安装实体，保留本地说明；verify：`python3 scripts/probe_capabilities.py` + `python3 -m pytest tests/`（或 test_workflow.py 直跑） |
| scripts | 无（自带脚本属安装实体本体，不经本地辅助脚本通道） |
| experience_refs | 无 |

## 调用说明

### 用途

按 workspace 的 best_available_resource 原则做 Skill 选型时，用它替代人工搜索：多源搜索（本地已装 → skills.sh → GitHub → 可配置 registry）、按 repo+path 去重、读真实 SKILL.md 而非标题、审计脚本/隐藏文件/远联、评分排名、证据卡片输出。

### 硬规则（继承上游，与 workspace 红线一致）

- 不虚构 Skill/仓库/版本/许可；发现阶段不执行候选脚本
- 无完成审计或有高危发现不安装；安装前必须用户明确批准
- 安装后必须验证安装副本

### 本 workspace 的适配

- 安装实体落 `.claude/skills/<name>/`、资产文档落 `.ai/skills/<name>/`、登记 installed_ref（commit SHA）——与 resource-manager 流程一致，本 skill 的输出可作为 resource-manager `add` 的输入
- 与既有 `find-skills`、`skill-hub` 并存：需要"证据卡片 + 审计"时用本 skill；简单查找用 find-skills
