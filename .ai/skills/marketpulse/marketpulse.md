# marketpulse

> 管理资产：`.ai/skills/marketpulse/marketpulse.md`；安装实体：`.claude/skills/marketpulse/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | skillhub · pack finance-financial-report-analysis (author: AIsa, MIT) |
| installed_ref | v1.0.2 |
| runtime | both |
| 调用入口 | $marketpulse |
| 要求 | AISA_API_KEY；network |
| 更新 | reinstall · 从原 SkillHub pack 下载到临时目录，对比后替换安装实体；验证：查询一个美股标的的最新行情和一份披露 |
| 辅助脚本 | — |
| 经验引用 | financial-analysis |

美股/全球市场数据：实时股价、新闻、财务报表、分析师评级、内部人交易、SEC 文件、宏观利率。

## 来源

- SkillHub pack `finance-financial-report-analysis`（author: AIsa, v1.0.2, MIT）

## 依赖

- **AISA_API_KEY**（环境变量；primaryEnv）

## 使用

市场数据查询、股票分析、watchlist、组合工作流。

## 回写条目（来源: financial-analysis）

- 无 `AISA_API_KEY` 时降级跳过，不阻塞流程；美股数据缺口需在交付报告中注明。
