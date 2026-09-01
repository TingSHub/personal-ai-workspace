# financial-fraud-index

> 管理资产：`.ai/skills/financial-fraud-index/financial-fraud-index.md`；安装实体：`.claude/skills/financial-fraud-index/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | skillhub · pack finance-financial-report-analysis |
| installed_ref | tree-sha256:620e79e02f98 |
| runtime | both |
| 调用入口 | $financial-fraud-index |
| 要求 | 年报 PDF 或抽取文本 |
| 更新 | reinstall · 从原 SkillHub pack 下载到临时目录，对比后替换安装实体；验证：使用一份年报完成最小风险评估并检查证据引用 |
| 辅助脚本 | — |
| 经验引用 | financial-analysis |

财报造假指数分析：基于年报/审计报告/三表（PDF 或抽取文本）做证据驱动的造假风险评估，输出量化风险指数与风险等级、可疑科目标注、证据链。

## 来源

- SkillHub pack `finance-financial-report-analysis`
