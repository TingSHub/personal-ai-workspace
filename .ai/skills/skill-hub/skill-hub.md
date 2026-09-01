# skill-hub

> 管理资产：`.ai/skills/skill-hub/skill-hub.md`；安装实体：`.claude/skills/skill-hub/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | github · https://github.com/wanghui2323/skill-hub |
| installed_ref | 3e4601b1479e7cac003d98df1c08759d695a3673 |
| runtime | both |
| 调用入口 | $skill-hub；脚本入口位于安装实体 scripts/ |
| 要求 | Python 3.6+；network（搜索、抓取或从 GitHub 安装时）；Git（使用其安装脚本的 GitHub 克隆路径时） |
| 更新 | reinstall · 将上游最新 revision 获取到临时目录，审查 SKILL.md、scripts、依赖与 LICENSE 后，用 skill-installer 替换 .claude/skills/skill-hub；保留本地资源记录；验证：校验 SKILL.md frontmatter，编译全部 Python 脚本，并运行 search_skills.py 的帮助/最小离线入口 |
| 辅助脚本 | scripts/search_skills.py（从官方、精选社区和 GitHub 来源搜索 Skill）；scripts/fetch_skill.py（获取远程或本地 Skill 内容供审查）；scripts/install_skill.py（将 Skill 安装到用户级 Claude Skills 目录）；scripts/analyze_skill_patterns.py（分析现有 Skill 的结构与可复用构建模式） |
| 经验引用 | — |

## 作用

用于发现第三方 Skill、读取候选内容、做初步质量与安全评估，以及分析 Skill 的构建模式。安装实体来自 `wanghui2323/skill-hub`。

## 调用

- 工作流入口：`$skill-hub`
- 搜索：`python3 .claude/skills/skill-hub/scripts/search_skills.py "<需求>"`
- 获取候选：`python3 .claude/skills/skill-hub/scripts/fetch_skill.py <URL或本地路径>`
- 构建分析：`python3 .claude/skills/skill-hub/scripts/analyze_skill_patterns.py <URL或本地路径>`

## Workspace 边界

- 搜索结果与内置评分只是候选发现信息，不等于 Capability 资源路由或正式安全批准。
- 注册、安装、更新和归档仍由 `resource-manager` 执行；Capability 关系由 `capability-manager` 管理。
- 上游 `install_skill.py` 会写用户级 `~/.claude/skills`，并包含失败清理逻辑。调用前必须核对目标目录，避免覆盖既有资源；本 workspace 优先使用 Codex `skill-installer` 安装到 `.claude/skills` 后再登记。
- 不在资源记录中保存 GitHub token 或其他密钥。

## 更新与验证

更新时先下载到 `/tmp`，检查上游 `SKILL.md`、全部脚本、依赖、LICENSE 和 commit，再替换安装实体。更新后运行 Python 语法编译、入口帮助检查并确认 `.codex/skills` 目录链接正确、两条入口解析到同一实体。
