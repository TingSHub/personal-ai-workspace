# 模块接口规范

## 1. Serenity Skill 接口

### 输入
```python
{
    "market": "A-share" | "HK" | "US" | "TW" | "JP" | "global",
    "theme": "AI半导体" | "CPO" | "机器人" | "800V直流电" | ...,
    "time_window": "3-12个月" | "6个月" | "1年",
    "depth": "quick_scan" | "full_research"
}
```

### 输出
```python
{
    "value_chain_layers": [
        {"layer": "原材料", "companies": [...], "scarcity_score": 0.8},
        ...
    ],
    "scarce_layers": ["层名1", "层名2"],
    "company_universe": [
        {"ticker": "600519.SH", "name": "贵州茅台", "chain_position": "...", "evidence_count": 5, "priority": "high"},
        ...
    ],
    "evidence_sources": [...],
    "risks": [...],
    "next_steps": [...]
}
```

### 调用方式
- Agent Skill: 读取 SKILL.md 后由Agent按指令执行
- 本地脚本: `python scripts/serenity_scorecard.py --format md company.json`

---

## 2. Buffett Skills 接口

### 输入
```python
{
    "company": "苹果" | "AAPL",
    "mode": "quick_filter" | "deep_analysis" | "topic"
}
```

### 输出（快速筛选）
```python
{
    "verdict": "pass" | "fail",
    "scores": {
        "circle_of_competence": "yes" | "no",
        "durability": "yes" | "no",
        "moat": "yes" | "no",
        "pricing_power": "yes" | "no",
        "earnings_quality": "yes" | "no",
        "debt_safety": "yes" | "no",
        "management_integrity": "yes" | "no",
        "reasonable_price": "yes" | "no"
    },
    "red_flags": ["管理层诚信存疑"],
    "summary": "..."
}
```

### 输出（深度分析）
```python
{
    "conclusion": "...",
    "circle_of_competence": "...",
    "key_assumptions": [...],
    "business_quality": {...},
    "financial_snapshot": {...},
    "valuation": {...},
    "sell_criteria": {...},
    "key_risks": [...],
    "monitoring_metrics": [...],
    "final_assessment": "..."
}
```

### 调用方式
- Agent Skill: 读取 SKILL.md + 按需读取 references/ 下的8个文件
- 无代码接口，纯Agent指令驱动

---

## 3. UZI-Skill 接口

### 输入
```python
{
    "ticker": "600519.SH" | "AAPL" | "00700.HK",
    "mode": "full_analysis" | "quick_scan" | "dcf" | "comps" | "scan_trap"
}
```

### 输出
```
.cache/{ticker}/
├── raw_data.json          # 22维原始数据
├── panel.json             # 65位评审裁决
├── agent_analysis.json    # Agent定性分析
├── institutional/         # 机构建模结果
│   ├── dcf.json
│   ├── comps.json
│   └── lbo.json
├── report.html            # Bloomberg风格HTML报告
└── share_card.png         # 社交分享战报
```

### 调用方式
```bash
# CLI
cd skills/uzi-skill && python run.py <ticker>

# Python API
from lib.pipeline.run import run_pipeline
run_pipeline(ticker="600519.SH", resume=False)
```

---

## 4. TradingAgents 接口

### 输入
```python
{
    "ticker": "NVDA",
    "date": "2026-01-15",
    "provider": "openai" | "google" | "anthropic" | "deepseek",
    "model": "gpt-5.5" | "claude-4" | "gemini-3.1"
}
```

### 输出
```
~/.tradingagents/logs/
├── {ticker}_{date}/
│   ├── fundamentals_analyst_report.md
│   ├── sentiment_analyst_report.md
│   ├── news_analyst_report.md
│   ├── technical_analyst_report.md
│   ├── bull_researcher.md
│   ├── bear_researcher.md
│   ├── trader_decision.md
│   ├── risk_management.md
│   └── portfolio_manager_decision.md
```

### 调用方式
```bash
# CLI
cd skills/TradingAgents && python main.py --ticker NVDA --date 2026-01-15

# Python API
from tradingagents.graph.trading_graph import TradingAgentsGraph
graph = TradingAgentsGraph(debug=False)
graph.propagate("NVDA", "2026-01-15")
```

---

## 5. QuantDinger 接口

### 输入
```python
{
    "strategy_code": "Python策略代码",
    "symbol": "BTCUSDT",
    "interval": "15m",
    "start_date": "2025-01-01",
    "end_date": "2026-01-01",
    "initial_capital": 10000,
    "commission": 0.001
}
```

### 输出
```python
{
    "equity_curve": [...],
    "total_return": 0.42,
    "sharpe_ratio": 1.8,
    "max_drawdown": -0.12,
    "win_rate": 0.65,
    "profit_factor": 2.1,
    "trades": [...]
}
```

### 调用方式
```bash
# Docker
cd skills/QuantDinger && docker-compose up -d

# API
POST http://localhost:5000/api/backtest/run

# MCP (Agent)
通过 quantdinger-mcp 包调用
```
