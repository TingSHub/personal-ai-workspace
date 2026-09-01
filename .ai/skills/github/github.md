# github

> 管理资产：`.ai/skills/github/github.md`；安装实体：`.claude/skills/github/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | skillhub · community @steipete/github |
| installed_ref | v1.0.0 |
| runtime | both |
| 调用入口 | unavailable |
| 要求 | gh CLI；GitHub authentication |
| 更新 | reinstall · 如需恢复，从原 SkillHub 来源下载到临时目录并重新安装；验证：执行只读 gh auth status 和仓库查询 |
| 辅助脚本 | — |
| 经验引用 | — |

当前安装实体已归档，保留本记录用于避免重复评估。

## 恢复调用

- 从原 SkillHub 来源重新安装后再使用。
- 要求 `gh` CLI 和 GitHub 认证；不得记录认证 token。

## 注意事项

- 仓库创建、推送、PR、Issue 和 CI 操作可能产生外部副作用，应遵循用户授权边界。
- 恢复后先运行只读 `gh auth status` 和仓库查询，再执行写操作。
