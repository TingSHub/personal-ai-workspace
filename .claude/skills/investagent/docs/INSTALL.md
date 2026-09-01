# Installation Guide

This guide covers three ways to use InvestAgent:

1. **Quick Start** — for one-off research tasks
2. **Full Installation** — for daily automated use
3. **Claude Code / Cursor** — for AI-editor native use

---

## Option 1: Quick Start (1–2 minutes)

Use InvestAgent as a drop-in SKILL for your AI editor. No installation required.

```bash
# 1. Clone just the core files
git clone https://github.com/investagent/investagent.git
cd investagent

# 2. Copy the orchestration file to your project
cp SKILL.md /your-project/.claude/skills/investagent/

# 3. Start using it in Claude Code chat:
#    "深度分析贵州茅台"  or  "研究A股AI半导体产业链"
```

This gives you the full research methodology framework — the AI agent reads `SKILL.md` and follows its instructions.

---

## Option 2: Full Installation (10–15 minutes)

### Prerequisites

| Component | Minimum | Recommended | Notes |
|-----------|---------|-------------|-------|
| Python | 3.10 | 3.11+ | Required |
| pip | latest | latest | Use `python -m pip install --upgrade pip` |
| Git | 2.30 | latest | Required for submodules |
| Disk space | 200 MB | 1 GB | Includes 5 submodule repositories |
| Memory | 256 MB | 1 GB | Most research is text/LLM-based |
| Docker Engine | 20.10 | 25+ | *Optional* — only for QuantDinger backtest |

### Step-by-Step

```bash
# ── 1. Clone the project with all submodules ──────────────────
git clone --recurse-submodules https://github.com/investagent/investagent.git
cd investagent

# (If you already cloned without submodules:)
# git submodule update --init --recursive

# ── 2. Install Python dependencies ─────────────────────────────
# Option A: One-command setup
bash scripts/setup_env.sh

# Option B: Manual, if you prefer more control
python -m venv .venv
source .venv/bin/activate              # On Windows: .venv\Scripts\activate
pip install -r skills/uzi-skill/skills/deep-analysis/requirements.txt
pip install -r skills/TradingAgents/requirements.txt

# ── 3. Configure environment variables (optional) ──────────────
# Copy the example file and fill in your API keys
cp .env.example .env

# Edit the file with your preferred editor:
# LLM_PROVIDER=openai               # or anthropic, deepseek, google
# LLM_API_KEY=sk-...                # needed for TradingAgents
# ALPHA_VANTAGE_API_KEY=...         # optional, for US equity data

# ── 4. Verify installation ─────────────────────────────────────
# Run a quick stock analysis to confirm the pipeline works:
python scripts/run_stock_analysis.py --ticker 600519.SH

# Check output directory:
ls -la output/
# You should see: stock_603078_20260616.md (or similar filename)
```

### Step 5: Docker Setup for QuantDinger (Optional)

If you want to run quant backtests:

```bash
cd skills/QuantDinger
docker-compose up -d

# Verify the service is running
curl http://localhost:5000/health
```

The QuantDinger backtest API will be available at `http://localhost:5000`.

---

## Option 3: Claude Code / Cursor / Codex Native

This is the **recommended approach** for most users — InvestAgent was designed from the ground up as a "SKILL" (a concept used by Claude Code / Cursor-style AI editors).

```bash
# 1. Clone into a skills directory in your project
mkdir -p /your-project/.claude/skills
cp SKILL.md /your-project/.claude/skills/investagent/

# 2. Start chatting with the agent
# In Claude Code / Cursor, say things like:
#
#   "帮我分析A股新能源汽车产业链"
#   "用巴菲特的标准筛选一下宁德时代"
#   "做一份贵州茅台的深度研究报告"
#
# The AI will follow the instructions in SKILL.md and produce
# a structured, multi-methodology research report.
```

### Why this approach is powerful

- **No server** — everything runs within the AI editor context
- **Methodology-first** — the agent follows documented research methods, not its own guesses
- **Transparent** — you can inspect and modify every step in SKILL.md
- **Zero cost** to get started (aside from your AI editor subscription)

---

## Troubleshooting

### "`git submodule update` fails with permission denied"

Check that you have network access to GitHub. Some frameworks are hosted on GitCode mirrors for better mainland-China access.

```bash
# Retry with increased verbosity to diagnose:
git submodule update --init --recursive --verbose
```

### "ModuleNotFoundError: No module named 'requests'"

```bash
pip install requests
# or re-run the setup script:
bash scripts/setup_env.sh
```

### "Script runs but report has no numbers"

This is expected when UZI-Skill fails to connect to a data source. InvestAgent is designed to avoid fabricating data — if a data source is unreachable, the report will say "data unavailable" for that dimension. You can:

1. Check your network connectivity to Chinese finance sites (akshare data sources)
2. Run with `--skip uzi` to skip the deep-analysis stage and get a text-only report
3. Add alternative data sources (see the Contributing Guide)

### "The report is too verbose / too short"

Adjust the `--depth` parameter:

```bash
python scripts/run_research.py --theme "AI半导体" --depth quick     # ~1 page
python scripts/run_research.py --theme "AI半导体" --depth normal    # ~5 pages (default)
python scripts/run_research.py --theme "AI半导体" --depth deep      # ~15 pages
```

---

## Uninstall

```bash
# Just delete the directory — InvestAgent doesn't install anything globally
cd ..
rm -rf investagent

# If you created a virtual environment, it's inside the project folder
# (hidden folder .venv), so it's already gone.
```

---

## Next Steps

- 📖 [Usage Examples](../README.md#quick-start) — common research patterns
- 🏗️ [Architecture](../references/architecture.md) — understand how modules interact
- ➕ [Contributing](CONTRIBUTING.md) — improve the project
