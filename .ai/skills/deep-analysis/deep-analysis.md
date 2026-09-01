# deep-analysis

> 管理资产：`.ai/skills/deep-analysis/deep-analysis.md`；安装实体：`.claude/skills/deep-analysis/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | github · https://github.com/tohnee/investagent |
| installed_ref | tree-sha256:51aa7c2823bd |
| runtime | both |
| 调用入口 | $stock-deep-analyzer:deep-analysis |
| 要求 | network and supported market data environment |
| 更新 | git · 随 investagent 更新，从临时目录核对 uzi-skill/skills/deep-analysis 后替换安装实体并保留本地说明；验证：验证数据契约并生成一次最小估值产物；明确报告未执行的模型 |
| 辅助脚本 | — |
| 经验引用 | — |

- 实体来自 `investagent` 的 `uzi-skill/skills/deep-analysis` 子目录。
- 本系统只在估值需要多模型交叉验证时可选调用，不因功能清单庞大就宣称所有模型已经执行。
- 输出必须报告真实数据源、完成的模型和降级项；未执行的 DCF、Comps 或 panel 不得写入执行记录。
- 更新随 `investagent` 统一进行，更新后核对数据契约与质量清单。
