# tushare-data

> 管理资产：`.ai/skills/tushare-data/tushare-data.md`；安装实体：`.claude/skills/tushare-data/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | skillhub · pack finance-financial-report-analysis (author: tushare.pro) |
| installed_ref | v1.1.16 |
| runtime | both |
| 调用入口 | $tushare |
| 要求 | Tushare-compatible token and endpoint；network |
| 更新 | reinstall · 从原 SkillHub pack 下载到临时目录，对比后替换安装实体；验证：用一个 A 股代码完成最小行情查询和字段检查 |
| 辅助脚本 | — |
| 经验引用 | financial-analysis |

面向中文自然语言的 Tushare 数据研究技能：A股/指数/ETF 行情、财务、估值、资金流、公告、宏观数据获取与清洗。

## 来源

- SkillHub pack `finance-financial-report-analysis`（author: tushare.pro, v1.1.16）

## 依赖

- **TUSHARE_TOKEN**（环境变量，https://tushare.pro/register 获取）
- 安装位置：`personal-ai-workspace/.claude/skills/tushare-data/`（workspace 内，随 Git 版本化）；Codex 入口 `.codex/skills/tushare-data`

## 使用

将自然语言请求转为数据获取/清洗/对比/筛选/导出流程；适用 A股研究场景。
