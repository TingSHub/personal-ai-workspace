#!/usr/bin/env python3
"""
投研Agent编排器 - 个股深度研究
整合 Buffett + UZI-Skill + TradingAgents + QuantDinger

用法:
    python run_stock_analysis.py --ticker 600519.SH
    python run_stock_analysis.py --ticker AAPL --date 2026-01-15
    python run_stock_analysis.py --ticker 00700.HK --skip quant
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime

AGENT_ROOT = Path(__file__).parent.parent
SKILLS_DIR = AGENT_ROOT / "skills"
OUTPUT_DIR = AGENT_ROOT / "output"


def log_step(step_name: str, status: str = "running"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    symbols = {"running": "▶", "done": "✓", "skip": "○", "error": "✗"}
    print(f"\n[{timestamp}] {symbols.get(status, '▶')} {step_name}")


def step1_buffett_quick_filter(ticker: str) -> dict:
    """巴菲特8问快速筛选"""
    log_step("Step 1: Buffett 8问快速筛选")
    buffett_dir = SKILLS_DIR / "buffett-skills"
    skill_md = buffett_dir / "skills" / "buffett" / "SKILL.md"

    if not skill_md.exists():
        log_step("Buffett Skills 未安装", "error")
        return {"verdict": "unknown", "error": "not installed"}

    log_step("  读取 Buffett SKILL.md", "done")

    return {
        "module": "buffett",
        "action": "quick_filter",
        "ticker": ticker,
        "skill_path": str(skill_md),
        "references_dir": str(buffett_dir / "skills" / "buffett" / "references"),
        "instruction": f"""
请按照 Buffett SKILL.md 中的8问快速筛选流程，评估以下公司：

股票代码: {ticker}

8问检查表:
1. 能力圈: 能用一段话解释它怎么赚钱吗？
2. 持久性: 10年后它还会更有竞争力吗？
3. 护城河: 竞争对手能复制其核心优势吗？
4. 定价权: 能抬价5-10%而不失去大量客户吗？
5. 盈利质量: 利润真实转化为现金了吗？
6. 债务安全: 收入跌30%公司还能活着吗？
7. 管理层诚信: 管理层是否坦诚面对问题？（一票否决）
8. 合理价格: 当前价格与内在价值差距够大吗？

输出: verdict(pass/fail) + 每问评分 + 理由
"""
    }


def step2_uzi_deep_analysis(ticker: str) -> dict:
    """UZI-Skill 22维深度分析"""
    log_step(f"Step 2: UZI-Skill 深度分析 {ticker}")
    uzi_dir = SKILLS_DIR / "uzi-skill"

    if not (uzi_dir / "run.py").exists():
        log_step("UZI-Skill 未安装", "error")
        return {"success": False, "error": "not installed"}

    requirements = uzi_dir / "skills" / "deep-analysis" / "requirements.txt"
    if requirements.exists():
        log_step("  安装依赖...", "running")
        try:
            subprocess.run(
                ["pip", "install", "-r", str(requirements), "--break-system-packages", "-q"],
                check=True, capture_output=True, timeout=300
            )
            log_step("  依赖安装完成", "done")
        except Exception as e:
            log_step(f"  依赖安装失败: {e}", "error")

    log_step(f"  执行深度分析...", "running")
    try:
        result = subprocess.run(
            [sys.executable, "run.py", ticker],
            cwd=str(uzi_dir),
            capture_output=True, text=True, timeout=600
        )
        cache_dir = uzi_dir / ".cache" / ticker
        report_html = cache_dir / "report.html"
        success = result.returncode == 0

        log_step(f"  深度分析 {'完成' if success else '失败'}",
                 "done" if success else "error")

        return {
            "module": "uzi-skill",
            "ticker": ticker,
            "success": success,
            "report_path": str(report_html) if report_html.exists() else None,
            "cache_dir": str(cache_dir) if cache_dir.exists() else None,
            "stdout_tail": result.stdout[-500:] if result.stdout else "",
            "stderr_tail": result.stderr[-300:] if result.stderr else ""
        }
    except subprocess.TimeoutExpired:
        log_step(f"  深度分析超时", "error")
        return {"ticker": ticker, "success": False, "error": "timeout"}


def step3_trading_agents(ticker: str, date: str) -> dict:
    """TradingAgents多Agent交易决策"""
    log_step(f"Step 3: TradingAgents 多Agent分析 {ticker}")
    ta_dir = SKILLS_DIR / "TradingAgents"

    if not (ta_dir / "main.py").exists():
        log_step("TradingAgents 未安装", "error")
        return {"success": False, "error": "not installed"}

    requirements = ta_dir / "requirements.txt"
    if requirements.exists():
        log_step("  安装依赖...", "running")
        try:
            subprocess.run(
                ["pip", "install", "-r", str(requirements), "--break-system-packages", "-q"],
                check=True, capture_output=True, timeout=300
            )
            log_step("  依赖安装完成", "done")
        except Exception as e:
            log_step(f"  依赖安装失败: {e}", "error")

    log_step(f"  执行多Agent分析...", "running")
    try:
        env = os.environ.copy()
        env["TRADINGAGENTS_OUTPUT_LANGUAGE"] = "zh"
        result = subprocess.run(
            [sys.executable, "main.py", "--ticker", ticker, "--date", date],
            cwd=str(ta_dir),
            capture_output=True, text=True, timeout=900,
            env=env
        )
        success = result.returncode == 0
        log_step(f"  多Agent分析 {'完成' if success else '失败'}",
                 "done" if success else "error")

        return {
            "module": "trading-agents",
            "ticker": ticker,
            "success": success,
            "stdout_tail": result.stdout[-1000:] if result.stdout else "",
            "stderr_tail": result.stderr[-500:] if result.stderr else ""
        }
    except subprocess.TimeoutExpired:
        log_step(f"  多Agent分析超时", "error")
        return {"ticker": ticker, "success": False, "error": "timeout"}


def generate_stock_report(steps: dict, ticker: str, output_dir: Path) -> str:
    """生成个股研究报告"""
    log_step("生成个股研究报告")
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = output_dir / f"stock_{ticker}_{timestamp}.md"

    report = f"""# {ticker} 深度研究报告

> 生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
> Agent: 全栈AI投研Agent v1.0
> 免责声明: 本报告仅供研究参考，不构成任何投资建议。

---

## 研究流程概览

| 步骤 | 模块 | 状态 |
|------|------|------|
| 1 | Buffett 快速筛选 | {"✓" if steps.get("buffett", {}).get("verdict") else "✗"} |
| 2 | UZI 深度分析 | {"✓" if steps.get("uzi", {}).get("success") else "✗"} |
| 3 | TradingAgents 多Agent | {"✓" if steps.get("trading", {}).get("success") else "✗"} |

---

## 一、价值投资筛选（Buffett）

"""

    buffett = steps.get("buffett", {})
    if buffett.get("instruction"):
        report += "> ⚠️ 以下指令需由AI Agent执行:\n\n"
        report += buffett["instruction"] + "\n\n"
    if buffett.get("verdict"):
        report += f"**筛选结果**: {'通过 ✓' if buffett['verdict'] == 'pass' else '未通过 ✗'}\n\n"

    report += """---

## 二、深度分析（UZI-Skill）

"""
    uzi = steps.get("uzi", {})
    if uzi.get("success"):
        report += f"- **分析状态**: ✓ 成功\n"
        if uzi.get("report_path"):
            report += f"- **HTML报告**: `{uzi['report_path']}`\n"
        if uzi.get("cache_dir"):
            report += f"- **数据缓存**: `{uzi['cache_dir']}`\n"
        if uzi.get("stdout_tail"):
            report += f"\n**输出摘要**:\n```\n{uzi['stdout_tail']}\n```\n"
    else:
        report += f"- **分析状态**: ✗ 失败\n"
        if uzi.get("error"):
            report += f"- **错误**: {uzi['error']}\n"

    report += """---

## 三、多Agent交易决策（TradingAgents）

"""
    ta = steps.get("trading", {})
    if ta.get("success"):
        report += f"- **分析状态**: ✓ 成功\n"
        if ta.get("stdout_tail"):
            report += f"\n**输出摘要**:\n```\n{ta['stdout_tail']}\n```\n"
    else:
        report += f"- **分析状态**: ✗ 失败\n"
        if ta.get("error"):
            report += f"- **错误**: {ta['error']}\n"

    report += """---

## 四、关键风险

1. **数据时效性**: 分析数据可能存在延迟
2. **AI幻觉风险**: AI生成内容可能包含不准确信息
3. **市场风险**: 市场环境变化可能导致结论失效
4. **流动性风险**: 标的流动性可能不足

## 五、监控指标

- [ ] 定期更新估值模型
- [ ] 跟踪财报和公告
- [ ] 监控行业政策变化
- [ ] 关注大股东增减持

## 六、免责声明

本报告由AI投研Agent自动生成，所有分析仅供研究参考，**不构成任何投资建议**。
投资有风险，决策需谨慎。
"""

    report_file.write_text(report, encoding="utf-8")
    log_step(f"报告已保存: {report_file}", "done")
    return str(report_file)


def main():
    parser = argparse.ArgumentParser(description="全栈AI投研Agent - 个股深度研究")
    parser.add_argument("--ticker", required=True, help="股票代码，如 600519.SH / AAPL / 00700.HK")
    parser.add_argument("--date", default=None, help="分析日期 (YYYY-MM-DD)")
    parser.add_argument("--skip-steps", default=[], nargs="+",
                        help="跳过的步骤: buffett/uzi/trading")
    parser.add_argument("--output", default=None, help="输出目录")

    args = parser.parse_args()
    date = args.date or datetime.now().strftime("%Y-%m-%d")

    print(f"""
╔══════════════════════════════════════════╗
║       全栈AI投研Agent v1.0              ║
║       个股: {args.ticker:<28s}║
║       日期: {date:<28s}║
╚══════════════════════════════════════════╝
""")

    output_dir = Path(args.output) if args.output else OUTPUT_DIR
    steps = {}

    if "buffett" not in args.skip_steps:
        steps["buffett"] = step1_buffett_quick_filter(args.ticker)

    if "uzi" not in args.skip_steps:
        steps["uzi"] = step2_uzi_deep_analysis(args.ticker)

    if "trading" not in args.skip_steps:
        steps["trading"] = step3_trading_agents(args.ticker, date)

    report_path = generate_stock_report(steps, args.ticker, output_dir)

    print(f"""
╔══════════════════════════════════════════╗
║       研究流程完成                        ║
║       报告: {report_path:<30s}║
╚══════════════════════════════════════════╝
""")


if __name__ == "__main__":
    main()
