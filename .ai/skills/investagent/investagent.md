# investagent

> 管理资产：`.ai/skills/investagent/investagent.md`；安装实体：`.claude/skills/investagent/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | github · https://github.com/tohnee/investagent |
| installed_ref | tree-sha256:51aa7c2823bd |
| runtime | both |
| 调用入口 | $investment-agent |
| 要求 | network and market data configuration；LLM API configuration for multi-agent debate；Docker for complete backtest workflow |
| 更新 | git · 从上游仓库获取到临时目录，对比各子模块后替换安装实体；验证：验证主题扫描入口并逐项报告五个模块的实际可用结果 |
| 辅助脚本 | — |
| 经验引用 | industry-research-methodology；investagent-module-runtime-issues；investagent-research-only-scope |

## 调用

- 入口：`$investment-agent`
- 适合环境齐备时组合产业链研究、价值分析、个股深度、多空辩论和量化回测。
- **A 股个股研究默认走 QuantDinger 降级路径**（透明 Python 脚本 + tushare 真实数据等价回测，产物标注「非原生产物」）：两轮实测均卡在 frontend 私有 GHCR 镜像与 compose 兼容问题（backend 可构建、frontend `invalid tag format` / 镜像不可拉取），降级产物证据强度对研究采集已足够；**仅当明确需要原生完整回测（如多策略横向验证）时才去解决镜像与 compose**——默认不再折腾原生部署，节省时间和 token。

## 要求

- 市场数据和联网配置。
- 多 Agent 辩论所需 LLM API 配置。
- 完整量化回测所需 Docker 环境。

## 注意事项与踩坑

- 各模块必须报告真实完成度，不能把环境降级后的结果描述为完整执行。
- 所有数字来自脚本或真实来源，禁止用模型记忆补数。
- 多模块输出应交叉验证并保留冲突，不能为了形成单一结论抹平分歧。
- 上游由多个子模块组成，更新时逐项检查入口、依赖和调用路径。
- UZI 模块 HTML 渲染依赖 playwright chromium（约 184MB 下载，国内网络易超时）；渲染受限时数据产物仍可保留，报告渲染单独记录降级。

## 更新

按 `skill.yaml` 从 GitHub 更新安装实体；至少验证主题扫描入口，并逐项报告五个模块的实际可用结果。

### 补充规则

- 环境齐备才编排：前置评估环境三件套（项目 .venv 依赖、外部 LLM key（如 DEEPSEEK_API_KEY）、Docker）可得性；实测打通前真实执行率约 40%，打通后约 90%。无 Docker/LLM key 时降级为真实数据 + 等效脚本的可复现输出，不得伪装完整执行。

### 补充规则

- QuantDinger：完整模块依赖 Docker 全栈 + 私有 GHCR 镜像，镜像不可拉取时以透明 Python 脚本 + 真实数据等价执行回测并标注「非原生产物」；tushare daily 返回倒序，回测前须升序重排。
- TradingAgents：yfinance 不识别 A 股代码需映射 .SS（如 600519.SH→600519.SS）；FRED_API_KEY 缺失时宏数据诚实降级为显式不可用，不伪造；StockTwits 403 / Reddit 429 属常见社交源限流。
- UZI-Skill：`--depth lite --no-browser` 档可真实跑通 21 维数据采集（akshare 东财接口不可达时自动走东财历史 + 腾讯 + baostock 兜底）；雪球端点需登录导致部分字段 partial。
- 关键历史财务数据不得用模型记忆，必须联网核实（实测初稿「2013-2015 净利下滑」为错误记忆，2025 年才是首次年度负增长）。

### 补充规则

- **内容生产链路（企业研究/内容页面为最终产物）只跑「研究+数据」范围**：Buffett 定性评估 + UZI 22 维数据采集 + tushare 财务/行情采集；**跳过 TradingAgents 多Agent决策与 QuantDinger 回测**——完整流水线约 40% 模块产出的是内容边界禁止的持有建议/目标价/交易策略，启动时即明确范围，不跑完再裁剪（实测中途裁剪已浪费约 30 分钟执行预算，4 次 TradingAgents 尝试均无内容价值）。
- findings-summary 同步收敛：不写决策/回测结论，执行状态如实标注「按项目内容边界排除」。
- 若项目确需决策结论（投资决策类），再单独以完整模式运行——范围选择是项目属性，不是 skill 缺陷。

> 用户边界修正补充（2026-08-16）：研究交付物（findings-summary）同步收紧——**不输出具体目标价（机构或自研）与买卖评级（含机构评级分布）**；盈利一致预期（净利/EPS）作为「市场预期差异」允许保留；「基本面验证指标/风险证伪条件」允许（如批价站稳、连续两季净利正增长等验证信号）。
