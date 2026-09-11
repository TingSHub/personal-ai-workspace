# hithink-finance

> 管理资产：`.ai/skills/hithink-finance/hithink-finance.md`；安装实体：`.claude/skills/hithink-finance/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | github · [HiThink-Tech/Financial-API](https://github.com/HiThink-Tech/Financial-API) |
| installed_ref | 402574a6221d5e255dba47166df8e5abb7149938 |
| runtime | both |
| 调用入口 | `hithink-finance`（自然语言任务路由；通过 CLI、MCP、REST API 或 Python SDK/marketdb 执行） |
| 要求 | 同花顺金融数据服务 API Key（`HITHINK_FINANCE_API_KEY`）；按选定接入方式提供 network、CLI、MCP 或 Python 环境 |
| 更新 | git · 从来源仓库获取新提交到临时目录，替换 `.claude/skills/hithink-finance/` 的完整目录并更新本记录的 commit SHA；验证：检查 `SKILL.md`、`references/` 完整且按仓库入口完成最小离线检查 |
| 辅助脚本 | — |
| 经验引用 | — |

## 调用说明

### 作用

同花顺官方 A 股金融数据服务的统一 Agent 入口。可按任务路由到最新行情、历史 K 线、财务报表、估值、指数、板块、基金、期货、期权、涨跌停/龙虎榜等数据能力，也支持本地 DuckDB 数据库同步、SQL 查询和导出。

### 来源与安装

- 来源仓库：[HiThink-Tech/Financial-API](https://github.com/HiThink-Tech/Financial-API)
- 当前安装实体保留了完整的 `references/` 和 `agents/`，没有只复制主 `SKILL.md`。
- 当前版本为提交 `402574a6221d5e255dba47166df8e5abb7149938`，仓库声明 MIT License。

### 怎么用

直接用自然语言描述任务即可，例如：

- “查询贵州茅台的最新行情。”
- “比较茅台和平安银行近一年的走势，计算涨跌幅、均线和最大回撤。”
- “查询宁德时代最近四期利润表和主要盈利指标，注明报告期与数据来源。”
- “获取沪深 300 当前成分股，并保存为本地文件。”

Skill 会根据任务和当前环境选择接入方式。默认优先使用 CLI；已连接托管 MCP 的对话优先走 MCP；Python/Notebook 或已有 marketdb 场景走 Python；自定义服务端集成走 REST API。

### 配置与注意事项

- API Key 从 `https://fuyao.aicubes.cn/admin` 获取，推荐保存为用户级 `HITHINK_FINANCE_API_KEY` 或用户级 `credentials.env`；本记录不保存密钥。
- 名称或代码取数前先做标的消歧，转换为唯一 `thscode`；结果需注明数据时间、报告期、复权口径和来源。
- 全市场、多年历史或大批量结果必须落盘，只在对话中返回路径、行数、时间范围和摘要，不能把原始全集塞入上下文。
- 当前公开能力不包含分钟 K、tick、海外行情、宏观数据、新闻公告原文和研报；请求超出范围时应明确说明，不使用模拟数据替代。
- 未配置 API Key 时可以阅读和规划调用，但不能宣称已完成线上数据验证；不要在聊天、日志、代码或 Git 中回显或保存 Key。

### 最小验证

离线验证：确认 `.claude/skills/hithink-finance/SKILL.md` 以及 `references/` 存在，并可从 `.codex/skills/hithink-finance/SKILL.md` 解析到同一安装实体。线上验证需要用户已配置有效 API Key，再按选定入口执行一个小范围查询。
