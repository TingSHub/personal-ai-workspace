# financial-report-analysis

> 管理资产：`.ai/skills/financial-report-analysis/financial-report-analysis.md`；安装实体：`.claude/skills/financial-report-analysis/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | skillhub · pack finance-financial-report-analysis |
| installed_ref | v1.0.0 |
| runtime | both |
| 调用入口 | unavailable |
| 要求 | — |
| 更新 | reinstall · 如需恢复，从原 SkillHub pack 下载到临时目录并先移除模拟数据依赖；验证：注入真实三表数据并与原始报表复核指标 |
| 辅助脚本 | — |
| 经验引用 | financial-analysis |

当前安装实体已归档。原资源包含模拟数据和硬编码公司信息，不能直接用于真实项目；已验证的计算思路由 `financial-report-generator` 承接。

如需恢复，按 `skill.yaml` 重装后必须注入真实三表数据，并把核心指标与原始报表复核；不得使用内置样例生成正式交付物。
