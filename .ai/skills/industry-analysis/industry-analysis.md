# industry-analysis

> 管理资产：`.ai/skills/industry-analysis/industry-analysis.md`；安装实体：`.claude/skills/industry-analysis/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | github · https://github.com/bellisji233/industry-analysis-skill |
| installed_ref | tree-sha256:a2a363fca3d9 |
| runtime | both |
| 调用入口 | $industry-analysis |
| 要求 | network for current source verification；TUSHARE_TOKEN and TUSHARE_API_URL for valuation helper script |
| 更新 | git · 从上游仓库获取到临时目录，对比后替换安装实体；保留本地资源说明与 scripts/；验证：完成一次最小行业边界与来源检查，并运行报告校验 |
| 辅助脚本 | scripts/fetch_valuation_tushare.py（使用 Tushare 真实日频数据替代不稳定的 AkShare/东财估值分位路径） |
| 经验引用 | industry-research-methodology |

## 调用

- 入口：`$industry-analysis`
- 适合产业链、高价值环节、细分赛道和 A 股标的映射。
- 联网数据必须标注来源、日期和口径；取不到数据时降级为定性判断，禁止猜数。

## 注意事项与踩坑

- 历史估值分位和 PEG 最容易产生幻觉：有真实序列才输出数值，Tushare 没有 PEG 字段时明确留空。
- 报告需要保留证伪条件、低置信数据和下一步尽调清单。
- 上游 AkShare/东财估值路径可能不稳定；优先使用下面的本地脚本。

## 辅助脚本

### `scripts/fetch_valuation_tushare.py`

- 作用：用 Tushare `daily_basic` 真实日频序列计算 PE(TTM)、PB、PS(TTM) 历史分位。
- 使用条件：A 股行业研究需要真实估值分位，且已配置 `TUSHARE_TOKEN`、`TUSHARE_API_URL`。
- 调用：`.venv/bin/python .ai/skills/industry-analysis/scripts/fetch_valuation_tushare.py 688017 --md`
- 限制：依赖 pandas（项目 .venv）；脚本不可用时降级定性区间（高/中/低），禁止凭空给出具体数值；不提供 PEG；接口无数据时明确失败，不猜测数值。

### 补充规则

- 估值分位优先用脚本取 Tushare 真实数据（`scripts/fetch_valuation_tushare.py`）；脚本不可用时降级定性区间（高/中/低），禁止凭空给出具体数值。实测真实分位可改变实质判断（如识别唯一低分位标的），并对口径异常（如 PE 489x）如实标注待核验。

## 更新

按 `skill.yaml` 从 GitHub 更新安装实体；保留本地说明和 `scripts/`，再执行最小行业分析与报告校验。
