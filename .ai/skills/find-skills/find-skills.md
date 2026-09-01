# find-skills

> 管理资产：`.ai/skills/find-skills/find-skills.md`；安装实体：`.claude/skills/find-skills/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | github · https://github.com/vercel-labs/skills/tree/main/skills/find-skills |
| installed_ref | c6f69c631292444cc541ac6d91e2226b0ff247da |
| runtime | both |
| 调用入口 | $find-skills；需要实际搜索时调用 npx skills find |
| 要求 | Node.js 与 npm/npx；network（查询 skills.sh 或使用 Skills CLI 时） |
| 更新 | reinstall · 将 vercel-labs/skills 的 skills/find-skills 获取到临时目录审查，再用 skill-installer 按 commit 替换 .claude/skills/find-skills；验证：校验 SKILL.md frontmatter、确认 npx 可用，并运行 Skills CLI 帮助入口 |
| 辅助脚本 | — |
| 经验引用 | — |

## 作用

用于从开放 Agent Skills 生态发现候选资源，并在推荐前核验安装量、来源信誉和仓库活跃度。安装实体来自 `vercel-labs/skills` 的 `skills/find-skills` 子目录。

## 调用

- 工作流入口：`$find-skills`
- 搜索：`npx skills find <关键词>`
- 上游给出的安装形式：`npx skills add <owner/repo@skill> -g -y`

## Workspace 边界

- 不仅凭搜索排名推荐或安装；需要检查来源、安装量、GitHub 仓库与实际 Skill 内容。
- 本 workspace 的正式注册、安装和更新仍由 `resource-manager` 处理，避免 `npx skills add -g` 绕过 `.ai/skills` 记录和 `.codex/skills` 目录级映射约定。
- 若确需使用 Skills CLI 安装，先确认其目标位置和覆盖行为，再同步登记安装 revision；不要把搜索热度直接写成 Capability 排序。

## 更新与验证

更新时锁定上游 commit，先在 `/tmp` 审查 `SKILL.md`，再重装并确认 `.codex/skills` 目录链接正确、两条入口解析到同一实体。最小验证包括 frontmatter 检查、`npx --version` 和 `npx skills --help`。
