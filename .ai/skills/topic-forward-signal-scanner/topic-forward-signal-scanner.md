# topic-forward-signal-scanner

> 管理资产：`.ai/skills/topic-forward-signal-scanner/topic-forward-signal-scanner.md`；安装实体：`.claude/skills/topic-forward-signal-scanner/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| name | topic-forward-signal-scanner |
| kind | skill |
| description | 使用 AkShare 免费接口扫描涨停池与涨幅异动，为选题前瞻生成可追溯市场信号 JSON |
| source | internal · 从 video-publish-review 项目脚本沉淀 |
| installed_ref | internal · v0.1 |
| runtime | both |
| invocation | `python3 .ai/skills/topic-forward-signal-scanner/scripts/fetch_market_signals.py --date YYYYMMDD --out <signals.json>` |
| requirements | Python 3、akshare、网络；接口失败必须保留 errors |
| update | internal · 修改脚本后用一个交易日运行验证 zt_pool/movers/errors 字段 |
| scripts | `scripts/fetch_market_signals.py`：涨停池与涨幅榜扫描；选题前瞻 Phase 1 使用 |
| experience_refs | — |

## 调用说明

该 Skill 只负责采集市场信号，不判断选题、不生成投资结论。输出包含 `captured_at`、`trade_date`、`zt_pool`、`movers` 和 `errors`，下游必须引用具体字段并保留降级状态。

数据源为 AkShare 的东财涨停池和新浪 A 股行情。涨停池适合题材锚点，涨幅榜适合异常筛选；两路均失败时仍输出 JSON，并由上游工作流决定是否停止。

## 注意事项

- 交易日期使用 `YYYYMMDD`；非交易日运行必须在上游报告中标注。
- 免费接口可能断连或字段变动；不得把空结果解释为市场没有信号。
- 该 Skill 不替代新闻原文、公告或研究证据；信号只用于候选发现。
