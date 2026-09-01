# Contributing to InvestAgent

Thank you for your interest in improving this project. We welcome contributions from researchers, developers, investors, and anyone who finds this work useful.

---

## 🌱 Ways to Contribute

You don't need to write code to contribute:

| Type | Examples | Effort |
|------|----------|--------|
| 🐛 **Bug reports** | Found a mistake in a research report? A script that crashes? File an issue. | 15 min |
| 💡 **Feature ideas** | Have an idea for a new research methodology? A better data source? Open a discussion. | 10 min |
| 📖 **Documentation** | Fix a typo, clarify a section, translate to English / Japanese. | 30 min |
| 🔬 **New methodology** | Add a Peter Lynch-style PEG screen, a Soros reflexivity indicator, a momentum filter. | 2–4 hrs |
| 🔌 **Data connectors** | Add support for a new data source (terminal data, local CSVs, APIs). | 1–3 hrs |
| 📊 **Report visualization** | Build an HTML report generator with charts and visualizations. | 3–6 hrs |

---

## 📦 Setting Up a Development Environment

```bash
# 1. Fork on GitHub, then clone your fork
git clone --recurse-submodules https://github.com/[YOUR_USERNAME]/investagent.git
cd investagent

# 2. Create a branch for your work
git checkout -b feature/my-new-feature
# or:
git checkout -b fix/bug-in-stock-parser

# 3. Install dependencies
bash scripts/setup_env.sh

# 4. Test that everything works before you change anything
python scripts/run_stock_analysis.py --ticker 600519.SH --skip trading quant
```

---

## 🏗️ Code Structure & Where to Look

```
investagent/
├── SKILL.md                  ← EDIT if you change the research methodology
│                             (this is the main orchestration file)
│
├── scripts/
│   ├── run_research.py       ← CLI entry point for theme-level research
│   ├── run_stock_analysis.py ← CLI entry point for single-stock analysis
│   └── setup_env.sh          ← Environment setup script
│
├── references/
│   ├── architecture.md       ← Architecture document
│   ├── module-interfaces.md  ← Data contracts between modules
│   └── prompt-templates.md   ← Reusable prompt library
│
├── skills/                   ← Git submodules — do NOT edit directly
│   ├── serenity-skill/       ← Read-only; send PRs to the upstream repository
│   ├── buffett-skills/       ← Read-only; send PRs to the upstream repository
│   ├── uzi-skill/            ← Read-only; send PRs to the upstream repository
│   ├── TradingAgents/        ← Read-only; send PRs to the upstream repository
│   └── QuantDinger/          ← Read-only; send PRs to the upstream repository
│
├── output/                   ← Generated reports (gitignored)
│
├── README.md                 ← English project page
└── README_CN.md              ← Chinese project page (keep in sync!)
```

> **Important:** The `skills/` directory contains git **submodules** — pointers to other open-source projects. Don't edit them directly. If you need to improve a submodule, send a pull request to that upstream project.

---

## ✅ Pull Request Checklist

Before you open a pull request, please make sure:

- [ ] **Your code runs** — Test the affected entry script
- [ ] **Both READMEs are in sync** — Update `README.md` AND `README_CN.md`
- [ ] **SKILL.md is updated** — If you changed the research methodology
- [ ] **No hardcoded API keys or tokens** — Use environment variables
- [ ] **No fabricated data** — Every numeric claim must be sourced or flagged as illustrative
- [ ] **Disclaimer is present** — Any research output template must include the disclaimer

### Example PR description

```markdown
## Summary

Add support for "Magic Formula" (Joel Greenblatt) screening — a new
research module that ranks stocks by (EBIT/Enterprise Value) and
(Return on Invested Capital).

## Changes

- `SKILL.md`: Added "Magic Formula screening" as a new execution path
- `scripts/run_research.py`: Added --magic-formula CLI flag
- `references/architecture.md`: Updated module interaction diagram

## Tested

- Tested on A-share top 50 stocks: produces sensible rankings
- Tested edge case: stocks with negative EBIT are correctly excluded
```

---

## 🧪 Testing Method

Because the project produces *research reports* (not deterministic output), we don't run traditional unit tests. Instead, verify your changes with:

### 1. Smoke Test

```bash
# Does the CLI still work?
python scripts/run_stock_analysis.py --ticker 600036.SS --skip uzi trading quant

# Expected: A Markdown report in output/ with non-zero file size
```

### 2. Methodology Review

```bash
# After editing SKILL.md, ask Claude Code:
# "Run a research task on 贵州茅台 using the updated SKILL file.
#  Did the research methodology execute correctly? Any missing steps?"
```

### 3. Sanity Check

If your change affects numerical output, the generated report's numbers should:
- **Be internally consistent** — PE × EPS ≈ price
- **Be directionally sensible** — A loss-making stock should not score "10/10" on profitability
- **Flag uncertainty** — When data is missing, say "data unavailable" rather than guessing

---

## 📜 Commit Message Convention

```
feat: add magic formula screening
↑     ↑
│     └── Short description in present tense
│
└── Type: feat / fix / docs / style / refactor / test / chore
```

Examples:

- `feat: add magic formula screening module`
- `fix: Buffett screen missing the management-quality question`
- `docs: improve installation guide for Windows users`
- `refactor: consolidate request-router logic`
- `chore: update submodule references to latest versions`

---

## 📖 Documentation Contributions

When you edit `README.md`, also update `README_CN.md`. Both files should cover the same content in their respective languages.

- Short bullet points and code snippets should match between the two files
- The Chinese file can have *additional* context relevant to the Chinese market (e.g., a list of mainland-friendly data sources)

---

## 🔎 Reporting Bugs

When filing an issue, please include:

```
**Environment:**
- Python version: `python --version`
- Operating system: (e.g., macOS 14.4, Ubuntu 22.04, Windows 11)
- InvestAgent commit hash: `git rev-parse --short HEAD`

**What I ran:**
```
python scripts/run_stock_analysis.py --ticker 600519.SH
```

**What I expected:**
A research report with valuation numbers.

**What I got:**
[Paste error message, or a screenshot description]

**Relevant context:**
- Was this the first time running the script?
- Have you modified any files?
- Network connectivity to Chinese data sources? (yes / behind VPN / unsure)
```

---

## 🎛️ Adding a New Research Module

InvestAgent is designed to be extensible. To add a new research methodology:

1. **Document it in `SKILL.md`** — add a new "execution path" section describing what the new module does, what inputs it expects, and what output it produces
2. **Add a submodule** — if it depends on an external tool: `git submodule add https://.../my-new-module.git skills/my-module/`
3. **Add an entry script** — create a small Python script in `scripts/` that serves as the CLI entry point
4. **Update documentation** — mention the new module in both README files
5. **Send the PR** — we'll review within 72 hours

---

## 📄 Contributor License Agreement

By submitting a pull request, you agree to release your contribution under the **MIT License** (same as the project). Your name will be credited in the CONTRIBUTORS file.

---

## 🤔 Still Have Questions?

- **Open a GitHub discussion** — good for design questions and feature proposals
- **File an issue** — for bugs and technical problems
- **Read the existing docs** — [references/architecture.md](../references/architecture.md) covers how modules interact

---

<div align="center">

*Thank you for helping make systematic investment research accessible to everyone.*

</div>
