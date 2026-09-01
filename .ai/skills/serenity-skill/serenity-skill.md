# serenity-skill

> 管理资产：`.ai/skills/serenity-skill/serenity-skill.md`；安装实体：`.claude/skills/serenity-skill/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | github · https://github.com/tohnee/investagent |
| installed_ref | tree-sha256:51aa7c2823bd |
| runtime | both |
| 调用入口 | $serenity-skill |
| 要求 | network for source-backed research |
| 更新 | git · 随 investagent 更新，从临时目录核对子 Skill 后替换安装实体并保留本地说明；验证：运行内置 validate_skill.py，并完成一次来源支持的瓶颈分析 |
| 辅助脚本 | — |
| 经验引用 | — |

- 实体来自 `investagent` 的 `serenity-skill` 子目录。
- 适合补充产业链瓶颈、价值捕获、反方证伪和证据阶梯；不替代 `industry-analysis` 的完整六阶段结果。
- 只有实际调用并形成独立结果时才能记为 execution；仅读取其框架时标为 reference。
- 更新随 `investagent` 统一进行，更新后运行其自带验证脚本。
