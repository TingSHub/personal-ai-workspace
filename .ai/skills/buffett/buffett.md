# buffett

> 管理资产：`.ai/skills/buffett/buffett.md`；安装实体：`.claude/skills/buffett/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | github · https://github.com/tohnee/investagent |
| installed_ref | tree-sha256:51aa7c2823bd |
| runtime | both |
| 调用入口 | $buffett |
| 要求 | 公司财报、公告和已验收行业背景 |
| 更新 | git · 随 investagent 更新，从临时目录核对 buffett 子 Skill 后替换安装实体并保留本地说明；验证：完成一次公司 Quick Filter，并按任务类型实际读取规定 reference 后输出商业质量分析 |
| 辅助脚本 | — |
| 经验引用 | — |

- 实体来自 `investagent` 的 `buffett-skills/skills/buffett` 子目录。
- 完整公司分析必须按其 Reading Protocol 实际读取护城河、管理层、财务与资本配置 reference，不能只引用“巴菲特方法论”。
- 原 Skill 的标准输出含买卖判断和建议价格；用于本 workspace 时只保留商业质量、治理、资本配置和风险判断，不输出直接投资建议。
- 更新随 `investagent` 统一进行，更新后重新验证 reference 路径和必填输出。
