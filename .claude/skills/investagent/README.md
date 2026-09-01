<div align="center">

# InvestAgent · 全栈AI投研Agent

**Your AI Research Co-Pilot for Smarter Investment Decisions**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg?logo=python)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![AI Agent](https://img.shields.io/badge/AI_Agent-Claude%20Code%20Compatible-blueviolet?logo=cursor)](https://github.com/features/preview/copilot-workspace)
[![GitHub issues](https://img.shields.io/github/issues/investagent/investagent)](https://github.com/investagent/investagent/issues)
[![GitHub stars](https://img.shields.io/github/stars/investagent/investagent?style=social)](https://github.com/investagent/investagent/stargazers)
[![Made in China](https://img.shields.io/badge/Made%20in-China-red.svg)](https://github.com/investagent/investagent)

---

</div>

## 🌟 Overview

**InvestAgent** is an open-source, AI-powered investment research agent that consolidates five proven research methodologies into a single, automated workflow. It is built for individual investors, quant enthusiasts, and finance professionals who want *systematic, data-driven research* without the overhead of running a full research team.

### What It Does

When you ask InvestAgent to "研究A股AI半导体" or "深度分析贵州茅台", it orchestrates a six-stage pipeline:

```
┌────────────┐     ┌────────────┐     ┌────────────┐     ┌────────────┐
│  1. Theme  │────▶│ 2. Buffett│────▶│  3. Deep   │────▶│ 4. Trading│
│  Selection │     │  Screen    │     │  Analysis  │     │  Debate    │
└────────────┘     └────────────┘     └────────────┘     └────────────┘
                                                                 │
                       ┌────────────┐     ┌────────────┐        │
                       │ 6. Report  │◀────│ 5. Backtest│◀────────┘
                       │ Generation │     │  / Validate │
                       └────────────┘     └────────────┘
```

Each stage leverages a different open-source research framework — giving you a multi-methodology, multi-angle view of every investment opportunity.

### Target Market

- 🇨🇳 **A-share / HK stocks** (primary focus — research methodologies are built around Chinese market structure)
- 🇺🇸 **US equities** (fully supported via Yahoo Finance + Alpha Vantage)
- 💰 **Crypto** (quant backtesting via QuantDinger)
- 📊 **Sector / Theme analysis** (AI semis, CPO, robotics, 800V inverters, etc.)

---

## 🎯 Key Features

### 1. Five Integrated Research Frameworks

| Framework | Role | Capability |
|-----------|------|------------|
| **Serenity Skill** | 🏭 Industry chain analyst | 8-layer value chain mapping, bottleneck detection, candidate pool generation |
| **Buffett Skills** | 🧠 Value investing filter | 8-question screening, moat evaluation, management quality, margin-of-safety |
| **UZI-Skill** | 📊 Deep stock analyzer | 22-dim data, 65-person panel scoring, Bloomberg-style report |
| **TradingAgents** | ⚖️ Multi-agent debate | Analyst → Researcher → Trader → Risk Manager → Portfolio Manager |
| **QuantDinger** | 🧮 Quant backtest engine | Python strategy → deterministic backtest → PnL curves |

### 2. Smart Request Router

InvestAgent automatically classifies your question and chooses the right execution path:

| Query Pattern | Path | Example |
|--------------|------|---------|
| *"研究XX赛道"* | **Theme research** (Serenity → Buffett → UZI → TradingAgents → QuantDinger) | "研究AI半导体产业链" |
| *"深度分析XXX"* | **Stock deep dive** (Buffett → UZI → TradingAgents → QuantDinger) | "深度分析贵州茅台" |
| *"产业链拆解"* | **Industry-chain only** (Serenity full workflow) | "CPO产业链瓶颈分析" |
| *"巴菲特估值"* | **Value investing filter** (Buffett full framework) | "用巴菲特框架分析苹果" |
| *"多Agent分析"* | **Trading decision** (TradingAgents multi-agent workflow) | "用多Agent决策分析NVDA" |
| *"回测策略"* | **Quant backtest** (QuantDinger) | "写个双均线策略回测BTC" |

### 3. Structured Research Output

Every report includes:
- **Executive summary** — one-line thesis with score (1–10)
- **Industry chain analysis** — value chain layers + bottleneck detection
- **Stock screening** — Buffett 8-question filter with pass/fail verdicts
- **Deep-dive analysis** — financials, valuation, competitive position
- **Bull vs. bear thesis** — two-sided argument
- **Risk inventory** — quantified key risks
- **Verification action items** — what to monitor
- **Disclaimer** — always present, never financial advice

### 4. Automated Daily Research

Built-in scheduler runs your chosen theme every trading day, delivering a fresh report to `output/`.

```
⏰ 08:00 (Mon–Fri) · Asia/Shanghai
├── Scan today's hot sectors and market sentiment
├── Select the most research-worthy theme
├── Run full industry-chain + stock screening pipeline
└── Save report to  →  /workspace/investment-agent/output/daily_theme_20260618.md
```

### 5. Claude Code / Cursor / Codex Native

Designed to be dropped into a `.claude/skills/` folder in your project. The `SKILL.md` orchestration file is consumed natively by AI code editors — no server required.

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **Git** (for cloning the project and submodules)
- **Docker & Docker Compose** (optional, only needed for QuantDinger backtest)
- **LLM API key** (optional, only needed for TradingAgents multi-agent workflow)

### Installation

```bash
# 1. Clone the project with submodules
git clone --recurse-submodules https://github.com/investagent/investagent.git
cd investagent

# 2. Install core dependencies (for the orchestration layer + UZI-Skill)
bash scripts/setup_env.sh

# 3. Verify it works — run a stock analysis
python scripts/run_stock_analysis.py --ticker 600519.SH

# 4. Or run a theme-level research task
python scripts/run_research.py --theme "A股AI半导体" --market A-share
```

### With Claude Code (Recommended)

```bash
# Copy the SKILL orchestration file into your project
cp SKILL.md /your-project/.claude/skills/investagent/

# Then in Claude Code chat, just say:
# "深度分析宁德时代" or "研究A股CPO产业链"
```

That's it. InvestAgent handles the rest.

---

## 📂 Project Structure

```
investagent/
├── SKILL.md                              # ← Core orchestration file
│                                         #   (loaded by Claude Code / Cursor)
├── README.md                             # ← This document (EN)
├── README_CN.md                          # ← Chinese version
├── LICENSE                               # ← MIT
├── .gitmodules                           # ← 5 framework submodules
├── .gitignore                            # ← Standard Python + project ignores
│
├── scripts/
│   ├── run_research.py                   # Theme-level research (CLI entry)
│   ├── run_stock_analysis.py             # Single-stock deep analysis
│   └── setup_env.sh                      # One-command environment setup
│
├── skills/                               # Integrated research frameworks
│   ├── serenity-skill/                   # → Industry chain bottleneck hunter
│   ├── buffett-skills/                   # → Buffett value-investing system
│   ├── uzi-skill/                        # → 22-dim stock deep analyzer
│   ├── TradingAgents/                    # → Multi-agent LLM trading framework
│   └── QuantDinger/                      # → AI quantitative trading platform
│
├── references/
│   ├── architecture.md                   # System architecture doc
│   ├── module-interfaces.md              # Data contract between modules
│   └── prompt-templates.md               # Reusable prompt library
│
└── output/                               # Generated reports (Markdown, 1/day)
    └── .gitkeep
```

---

## 🧠 Architecture

### Design Principles

1. **Progressive disclosure** — Modules are activated only as needed. A simple Buffett screen runs in seconds; a full theme research may run 10–30 minutes.
2. **No data fabrication** — Every number comes from web search, scripts, or public APIs. Hard failure is preferred over hallucinated numbers.
3. **Contrarian by design** — When modules disagree (e.g., Buffett says "overvalued" but TradingAgents says "buy on momentum"), both positions are preserved in the report. The disagreement *itself* is the signal.
4. **Never give investment advice** — The agent's job is research. Output always ends with a disclaimer.

### Data Flow Between Modules

```
[Serenity]      →   candidate_tickers.json
    |                  (tickers, chain_position, scarcity_score)
    |
    v
[Buffett]       →   screening_results.json
    |                  (tickers, verdict, per_question_score, red_flags)
    |
    v
[UZI-Skill]     →   reports/* (22-dim data, 65-person panel, valuation models)
    |
    v
[TradingAgents] →   multi_agent_decision.json
    |                  (analyst_report, bull_vs_bear, trader_position, risk_assessment)
    |
    v
[QuantDinger]   →   backtest_results.json
                       (equity_curve, sharpe, max_drawdown, trade_log)
```

Full architecture document → [references/architecture.md](references/architecture.md)

---

## 📝 Example Output

### Research Report: 江化微 (603078.SH)

> **Summary:** Wet-chemicals leader in a hot semiconductor-supply chain, but PE 154× leaves no margin of safety. **Score 4.7/10 — watch, don't buy.**

| Dimension | Score | Notes |
|-----------|-------|-------|
| Industry outlook | 8/10 | Wet chemicals are semiconductor "blood," domestic substitution space is enormous |
| Company quality | 6/10 | Established domestic leader, but net margin only 8.5% |
| Growth | 7/10 | Semi segment +22% YoY, high-end 8–12 inch products +40% |
| Valuation | 2/10 | PE(TTM) 154 — severe overvaluation |
| Management | 4/10 | Second controller change in 4 years |
| Margin of safety | 1/10 | Virtually none at current price |

**Full sample report** → [output/stock_603078_20260616.md](output/stock_603078_20260616.md)

---

## 🛣️ Roadmap

- [x] **Core orchestration layer** — 5-module integration via SKILL.md
- [x] **CLI entry scripts** — `run_research.py`, `run_stock_analysis.py`
- [x] **Buffett 8-question screening** — value-investing filter
- [x] **22-dim deep analysis** — UZI-Skill pipeline
- [x] **Daily automated research** — scheduled 08:00 every trading day
- [ ] **TradingAgents integration** — LLM multi-agent decision pipeline (in progress)
- [ ] **QuantDinger integration** — dockerized backtest (in progress)
- [ ] **HTML report generator** — Bloomberg-style visualization (next)
- [ ] **Telegram / email notification** — deliver daily reports (next)
- [ ] **Web dashboard** — browser-based report viewer (planned v2)
- [ ] **i18n** — English-language research mode (planned v2)

---

## 🤝 Contributing

InvestAgent is an open, opinionated research framework. We welcome contributions from anyone — especially if you bring:

- **A new research methodology** — e.g., Peter Lynch-style PEG screening, Soros-style reflexivity indicators
- **Better data connectors** — local CSVs, terminal data, WeChat-mini-program scrapers
- **Report visualizations** — pretty HTML output, charts, dashboards
- **i18n** — translate the research prompts and output templates to English / Japanese

**See [CONTRIBUTING.md](#)** (drop a PR, we'll respond within 72 hours).

### Star History

If you find this project useful, a ⭐ on GitHub is the easiest way to say thanks.

---

## ⚠️ Disclaimer

**THIS SOFTWARE IS FOR RESEARCH AND EDUCATIONAL PURPOSES ONLY.**

- ❌ **No investment advice** — Nothing in the generated reports constitutes a recommendation to buy, sell, or hold any security.
- ❌ **No warranty** — The software is provided "as is," without warranty of any kind. Data may be delayed, incomplete, or incorrect.
- ❌ **No backtest guarantee** — Past performance does not guarantee future results. All backtest results are for research purposes.
- ✅ **Do your own research** — Always verify critical data points independently before making any investment decision.

---

## 📄 License

**MIT License** — You are free to use, modify, and distribute this project for any purpose (including commercial), provided you include the license and disclaimer. See [LICENSE](LICENSE) for the full text.

---

<div align="center">

**Made with 🧠 + ☕ in Shanghai**

*An open-source investment research agent — because systematic thinking beats random opinions.*

[![Top Language](https://img.shields.io/github/languages/top/investagent/investagent)](https://github.com/investagent/investagent)
[![Repo size](https://img.shields.io/github/repo-size/investagent/investagent)](https://github.com/investagent/investagent)
[![GitHub commit activity](https://img.shields.io/github/commit-activity/m/investagent/investagent)](https://github.com/investagent/investagent/commits)

</div>
