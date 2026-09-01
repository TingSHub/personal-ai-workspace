<div align="center">

# InvestAgent · 全栈AI投研Agent

**您的AI投资研究助理 — 从产业洞察到个股深度**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![AI Agent](https://img.shields.io/badge/AI_Agent-Claude%20Code%20兼容-blueviolet?logo=cursor)](https://github.com/features/preview/copilot-workspace)
[![Made in China](https://img.shields.io/badge/Made%20in-Shanghai-red.svg)](https://github.com/investagent/investagent)

[English](README.md) · **简体中文** · [文档](#) · [示例报告](output/stock_603078_20260616.md) · [问题反馈](https://github.com/investagent/investagent/issues)

---

</div>

## 🌟 项目简介

**InvestAgent** 是一个开源的 AI 投资研究助理，将 **5 种成熟的投研方法论** 整合到一个自动化工作流中。它面向**个人投资者、量化爱好者、金融从业者**——让您用系统化、数据驱动的方式做研究，而不用组建一个完整的研究团队。

### 它能做什么

当您让它 "**研究A股AI半导体**" 或 "**深度分析贵州茅台**" 时，InvestAgent 会编排一条**六阶段研究流水线**：

```
┌───────────────┐     ┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│ ① 主题识别    │────▶│ ② 巴菲特筛选 │────▶│ ③ 深度分析    │────▶│ ④ 多空辩论   │
│  行业选择     │     │  价值投资过滤 │     │  22维数据     │     │  TradingAgents│
└───────────────┘     └───────────────┘     └───────────────┘     └───────────────┘
                                                                           │
                                ┌───────────────┐     ┌───────────────┐      │
                                │ ⑥ 生成报告    │◀────│ ⑤ 回测验证    │◀─────┘
                                │  Markdown输出  │     │  QuantDinger  │
                                └───────────────┘     └───────────────┘
```

每个阶段都使用**一套独立的开源研究框架**——为每一个投资机会提供**多方法论、多视角**的研究结果。

### 覆盖市场

- 🇨🇳 **A股 / 港股**（主要研究方向 — 方法论围绕中国市场结构设计）
- 🇺🇸 **美股**（通过 Yahoo Finance + Alpha Vantage 完整支持）
- 💰 **加密货币**（通过 QuantDinger 进行策略回测）
- 📊 **主题/赛道分析**（AI半导体、CPO、机器人、800V、创新药等）

---

## 🎯 核心功能

### 1. 五大投研框架深度整合

| 框架 | 角色 | 能力 |
|------|------|------|
| **Serenity Skill** | 🏭 产业链分析师 | 8层价值链映射、稀缺瓶颈识别、候选标的池生成 |
| **Buffett Skills** | 🧠 价值投资过滤器 | 8问快速筛选、护城河评估、管理层质量、安全边际 |
| **UZI-Skill** | 📊 个股深度分析引擎 | 22维数据采集、65人评委打分、Bloomberg风格报告 |
| **TradingAgents** | ⚖️ 多Agent辩论 | 分析师 → 研究员 → 交易员 → 风控 → 基金经理 的协作决策 |
| **QuantDinger** | 🧮 量化回测引擎 | Python策略 → 确定性回测 → PnL净值曲线 |

### 2. 智能请求路由器

InvestAgent 会**自动判断您的意图**，选择最合适的执行路径：

| 提问方式 | 执行路径 | 示例 |
|---------|---------|------|
| **"研究XX赛道"** | 主题研究全流程（Serenity → Buffett → UZI → TradingAgents → QuantDinger） | "研究A股AI半导体产业链" |
| **"深度分析XXX"** | 个股深度研究（Buffett → UZI → TradingAgents → QuantDinger） | "深度分析贵州茅台" |
| **"产业链拆解"** | 产业链研究（Serenity完整工作流） | "CPO产业链瓶颈分析" |
| **"巴菲特估值"** | 价值投资筛选（Buffett完整框架） | "用巴菲特框架分析苹果" |
| **"多Agent分析"** | 多Agent交易决策（TradingAgents完整流程） | "用多Agent决策分析NVDA" |
| **"回测策略"** | 量化策略回测（QuantDinger） | "写个双均线策略回测BTC" |

### 3. 结构化研究报告

每份报告都包含：
- **一句话结论** — 核心判断 + 综合评分（1–10分）
- **产业链分析** — 价值链图层 + 瓶颈识别
- **标的筛选** — 巴菲特8问筛选表 + 每只标的 pass/fail 判定
- **深度分析** — 财务数据、估值、竞争地位
- **多空逻辑** — 看涨看跌两面对比
- **风险清单** — 关键风险量化打分
- **后续验证动作** — 监控指标与跟踪信号
- **免责声明** — 始终附带，从不提供投资建议

### 4. 每日自动化研究

内置调度器在每个交易日**早上 08:00（北京时间）**自动扫描热门赛道，生成一份完整研究报告并存入 `output/` 目录：

```
⏰ 08:00 (周一–周五) · Asia/Shanghai
├── 扫描今日热门板块与市场情绪
├── 选择最具研究价值的主题
├── 执行产业链拆解 + 标的筛选 + 深度分析全流程
└── 输出报告  →  /workspace/investment-agent/output/daily_theme_20260618.md
```

### 5. Claude Code / Cursor / Codex 原生支持

只需将 `SKILL.md` 放入项目的 `.claude/skills/` 文件夹，AI 编辑器即可**原生识别**并调用整套研究框架。**不需要额外的服务器**。

---

## 🚀 快速开始

### 前置条件

- **Python 3.10+**
- **Git**（用于克隆项目和子模块）
- **Docker & Docker Compose**（可选，仅在使用 QuantDinger 回测时需要）
- **LLM API Key**（可选，仅在使用 TradingAgents 多Agent流程时需要）

### 安装

```bash
# 1. 克隆项目（包含所有子模块）
git clone --recurse-submodules https://github.com/investagent/investagent.git
cd investagent

# 2. 安装核心依赖（编排层 + UZI-Skill）
bash scripts/setup_env.sh

# 3. 验证安装 — 分析一只股票
python scripts/run_stock_analysis.py --ticker 600519.SH

# 4. 或者跑一次主题级别的研究任务
python scripts/run_research.py --theme "A股AI半导体" --market A-share
```

### 在 Claude Code 中使用（推荐）

```bash
# 将 SKILL 编排文件复制到您的项目中
cp SKILL.md /your-project/.claude/skills/investagent/

# 然后在 Claude Code 的对话中直接说：
# "深度分析宁德时代"  或  "研究A股CPO产业链"
```

就这么简单。剩下的交给 InvestAgent。

---

## 📂 项目结构

```
investagent/
├── SKILL.md                              # ← 核心编排文件
│                                         #   （由 Claude Code / Cursor 加载）
├── README.md                             # ← 英文文档
├── README_CN.md                          # ← 中文文档（本文件）
├── LICENSE                               # ← MIT许可证
├── .gitmodules                           # ← 5个框架作为 git submodule
├── .gitignore                            # ← Python + 项目忽略规则
│
├── scripts/
│   ├── run_research.py                   # 主题级研究（CLI入口）
│   ├── run_stock_analysis.py             # 个股深度分析
│   └── setup_env.sh                      # 一键环境配置
│
├── skills/                               # 整合的研究框架
│   ├── serenity-skill/                   # → 产业链瓶颈猎手
│   ├── buffett-skills/                   # → 巴菲特价值投资系统
│   ├── uzi-skill/                        # → 22维个股深度分析
│   ├── TradingAgents/                    # → 多Agent LLM交易框架
│   └── QuantDinger/                      # → AI量化交易平台
│
├── references/
│   ├── architecture.md                   # 系统架构文档
│   ├── module-interfaces.md              # 模块间数据契约
│   └── prompt-templates.md               # 可复用 Prompt 模板库
│
└── output/                               # 生成的研究报告（Markdown，每日一份）
    └── .gitkeep
```

---

## 🧠 架构设计

### 设计原则

1. **渐进式加载** — 模块按需启动。简单的巴菲特筛选只需数秒，完整的主题研究可能运行10–30分钟。
2. **禁止数据编造** — 所有数字必须来自网络搜索、脚本执行或公开API。宁可硬失败也不能容忍幻觉数字。
3. **反共识设计** — 当模块结论不一致（例如 Buffett 说"估值过高"但 TradingAgents 说"动量买入"），**两个观点都会被保留在报告中**——分歧本身就是信号。
4. **永不提供投资建议** — Agent 的唯一角色是研究，所有输出都以**免责声明**结尾。

### 模块间数据流

```
[Serenity]      →   candidate_tickers.json
    |                （股票代码、产业链位置、稀缺度评分）
    |
    v
[Buffett]       →   screening_results.json
    |                （股票代码、判定结果、每问评分、红旗）
    |
    v
[UZI-Skill]     →   reports/* （22维数据、65人评委、估值模型）
    |
    v
[TradingAgents] →   multi_agent_decision.json
    |                （分析师报告、多空辩论、交易员决策、风控评估）
    |
    v
[QuantDinger]   →   backtest_results.json
                     （净值曲线、夏普、最大回撤、交易明细）
```

完整架构文档 → [references/architecture.md](references/architecture.md)

---

## 📝 示例输出

### 研究报告：江化微 (603078.SH)

> **一句话结论**：半导体湿化学龙头，产业逻辑优秀，但 PE 154× 缺乏安全边际。**综合评分 4.7/10 — 观望，不买入。**

| 维度 | 评分 | 说明 |
|------|------|------|
| 行业前景 | 8/10 | 湿电子化学品是半导体"血液"，国产替代空间巨大 |
| 公司质地 | 6/10 | 国产领先者，但净利率仅8.5% |
| 成长性 | 7/10 | 半导体业务同比+22%，8–12寸高端产品+40% |
| 估值 | 2/10 | PE(TTM) 154 — 估值过高 |
| 管理层 | 4/10 | 四年内两次变更实控人 |
| 安全边际 | 1/10 | 当前价格几乎没有 |

**完整示例报告** → [output/stock_603078_20260616.md](output/stock_603078_20260616.md)

---

## 🛣️ 路线图

- [x] **核心编排层** — 5模块集成（通过 SKILL.md）
- [x] **CLI入口脚本** — `run_research.py`、`run_stock_analysis.py`
- [x] **巴菲特8问筛选** — 价值投资过滤器
- [x] **22维深度分析** — UZI-Skill流水线
- [x] **每日自动化研究** — 交易日 08:00 定时执行
- [ ] **TradingAgents 整合** — LLM 多Agent决策流水线（进行中）
- [ ] **QuantDinger 整合** — Docker化回测（进行中）
- [ ] **HTML报告生成器** — Bloomberg风格可视化（下一步）
- [ ] **Telegram / 邮件通知** — 日报自动推送（下一步）
- [ ] **Web 仪表盘** — 浏览器版报告查看器（v2 计划）
- [ ] **i18n** — 英文研究模式（v2 计划）

---

## 🤝 贡献指南

InvestAgent 是一个开放、有明确观点的研究框架。我们欢迎所有人的贡献 — 尤其如果您能带来：

- **新的研究方法论** — 例如彼得·林奇 PEG 筛选、索罗斯反身性指标
- **更好的数据连接器** — 本地CSV、终端数据、小程序爬虫
- **报告可视化** — 漂亮的 HTML 输出、图表、仪表盘
- **i18n** — 将研究 Prompt 和输出模板翻译为英文 / 日文

**提交 PR 后我们会在72小时内回复。**

如果这个项目对您有帮助，请给我们一个 ⭐ — 这是对开源维护者最直接的鼓励。

---

## ⚠️ 免责声明

**本软件仅供研究与教育目的使用。**

- ❌ **不提供任何投资建议** — 报告中的任何内容都不构成买入、卖出或持有任何证券的建议。
- ❌ **不提供任何保证** — 软件"按原样"提供，数据可能延迟、不完整或错误。
- ❌ **不保证回测结果** — 历史表现不代表未来结果，所有回测结果仅供研究使用。
- ✅ **请独立研究** — 在做出任何投资决策前，务必自行核实关键数据。

---

## 📄 许可证

**MIT License** — 您可以自由使用、修改和分发本项目（包括商业用途），只需保留许可证和免责声明。完整条款请见 [LICENSE](LICENSE)。

---

<div align="center">

**Made with 🧠 + ☕ in Shanghai**

*一个开源的投资研究 Agent — 因为系统化的思考胜过随机的观点。*

</div>
