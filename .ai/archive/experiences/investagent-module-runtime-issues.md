# Experience: investagent-module-runtime-issues

> 仅沉淀会改变未来项目流程、资源选择、调用方法、质量检查或可复用脚本的经验证结论。

## 来源证据

项目：investment-research-system；运行：research-collection v0.3 贵州茅台实测（2026-08-15，investagent 执行，约 23 分钟/150 次工具调用）。证据：`outputs/companies/贵州茅台/2026-08-15/research-materials/investagent/`（主报告 + data/ 子模块 JSON）。相关资源 installed_ref：investagent（tree-sha256:51aa7c2823bd）。

## 触发场景

编排 investagent 对个股执行综合研究（Buffett/UZI/TradingAgents/QuantDinger/Serenity 五模块）时。

## 问题与归属判定

- 问题：investagent 子模块存在多个仅在真实运行才暴露的坑：QuantDinger 私有 GHCR 镜像不可拉取、TradingAgents yfinance 不识别 A 股代码、FRED_API_KEY 缺失中断、社交源 403/429、UZI 雪球端点需登录。
- 归属（owner）：`investagent` 注意事项与踩坑（补充现有环境三件套条目之下的子模块细节）。

## 可复用结论（resolution）

- **QuantDinger**：完整模块需 Docker 全栈（PostgreSQL/Flask + 私有 GHCR 镜像），镜像不可拉取时以透明 Python 脚本 + tushare 真实数据等价执行回测，产物必须标注"非原生产物"；tushare `daily` 返回倒序，回测前须升序重排。
- **TradingAgents**：yfinance 不识别 `600519.SH`，需映射为 `600519.SS`；FRED_API_KEY 缺失时宏数据诚实降级为显式不可用（不伪造）；StockTwits 403 / Reddit 429 属常见社交源限流。
- **UZI-Skill**：`--depth lite --no-browser` 档可真实跑通 21 维数据采集（akshare 东财接口不可达时自动走东财历史+腾讯+baostock 兜底）；雪球端点需登录导致部分字段 partial；HTML 渲染依赖 playwright（国内网络易超时，可跳过渲染保留数据产物）。
- **通用**：关键历史财务数据不得用模型记忆，必须联网核实（本轮初稿"2013-2015 净利下滑"为错误记忆，经核实为真实正增长，2025 年才是首次年度负增长）。

## 回写目标

- `investagent`（SKILL.md 注意事项与踩坑，追加子模块条目）

## 适用范围

investagent（tree-sha256:51aa7c2823bd）对 A 股个股的编排执行；环境为 workspace .venv + DEEPSEEK_API_KEY + docker 可用。

## 不适用范围

- 非个股研究场景（如仅产业链扫描）；
- 上游更新后子模块行为可能变化，需按新 installed_ref 复验。

## 关联资产

- Skill: `investagent`、`deep-analysis`
- Workflow: `research-collection`
- Experience: [[industry-research-methodology]]
