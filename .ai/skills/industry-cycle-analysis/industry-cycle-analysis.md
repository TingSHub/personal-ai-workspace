# industry-cycle-analysis

> 管理资产：`.ai/skills/industry-cycle-analysis/industry-cycle-analysis.md`；安装实体：`.claude/skills/industry-cycle-analysis/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | github · https://github.com/YE-coding/industry-cycle-analysis |
| installed_ref | tree-sha256:9e9b5dd25f8e |
| runtime | both |
| 调用入口 | $industry-cycle-analysis |
| 要求 | network for source-backed research |
| 更新 | git · 从上游仓库获取到临时目录，对比后替换安装实体；验证：运行最小报告并通过 validate_report.py 严格校验 |
| 辅助脚本 | — |
| 经验引用 | industry-research-methodology |

## 调用

- 入口：`$industry-cycle-analysis`
- 适合需求、供给、价格、库存、利润、资本开支和市场预期阶段分析。

## 注意事项与踩坑

- 搜索摘要和转述不能升级为事实，关键证据必须实际打开原始来源。
- 周期阶段、结论状态和置信度应分开表达；证据不足时结论保持暂定。
- 时间敏感结论先确认系统时间和披露状态。
- `validate_report.py --mode full --strict` 只验证结构纪律，校验通过不等于内容可信。

## 更新

按 `skill.yaml` 从 GitHub 更新，随后运行严格报告校验和最小证据账本验证。
