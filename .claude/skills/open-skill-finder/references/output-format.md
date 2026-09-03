# Recommendation output

Use concise evidence cards. Default to Simplified Chinese; use English when requested or when the user is clearly communicating in English.

## Chinese

```markdown
### Skill：example-skill

- 匹配度：82/100
- 来源：https://github.com/owner/repo · `skills/example-skill`
- 最近更新：2026-06-01
- 安全风险：已通过所提供的静态审查（low）
- 额外依赖：Python 3.10+
- 为什么推荐：实际指令覆盖用户所需的检索和比较流程。
- 注意事项：联网搜索需要 GitHub CLI 登录。
```

## English

```markdown
### Skill: example-skill

- Match: 82/100
- Source: https://github.com/owner/repo · `skills/example-skill`
- Last update: 2026-06-01
- Security: Passed the supplied static audit (low)
- Extra dependencies: Python 3.10+
- Why it fits: Its actual instructions cover the requested discovery and comparison workflow.
- Caveats: GitHub search requires an authenticated GitHub CLI.
```

## Conditional fields

Do not repeat ordinary cross-agent compatibility. Add a compatibility line only for an exception such as a required proprietary tool, operating system, or agent-specific API.

Do not repeat an ordinary permissive license. Add a license line when the license is missing, unclear, restrictive, inconsistent across files, or important to redistribution.

## Uncertainty

Use direct language:

- `未完成安全审查，不能直接安装` / `Static audit not completed; do not install yet`.
- `来源无法独立验证` / `Source could not be independently verified`.
- `这是根据仓库活动作出的推断` / `This is an inference from repository activity`.

Never turn an inference into a verified fact.
