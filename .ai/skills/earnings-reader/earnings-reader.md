# earnings-reader

> 管理资产：`.ai/skills/earnings-reader/earnings-reader.md`；安装实体：`.claude/skills/earnings-reader/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | skillhub · pack finance-financial-report-analysis |
| installed_ref | v1.0.0 |
| runtime | both |
| 调用入口 | $earnings-reader |
| 要求 | 真实财务报表输入 |
| 更新 | reinstall · 从原 SkillHub pack 下载到临时目录，对比后替换安装实体；验证：使用一组三表数据完成最小同比解读 |
| 辅助脚本 | — |
| 经验引用 | financial-analysis |

A股财报研读助手：逐表解读利润表（营收增速/毛利率/净利率趋势）、资产负债表（资产结构/负债/流动性）、现金流量表（经营/自由现金流），识别异常波动。

## 来源

- SkillHub pack `finance-financial-report-analysis`（v1.0.0）
