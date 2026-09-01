#!/usr/bin/env python3
"""
投研Agent编排器 - 主题研究全流程
整合 Serenity + Buffett + UZI-Skill + TradingAgents + QuantDinger

用法:
    python run_research.py --theme "A股AI半导体" --market A-share
    python run_research.py --theme "CPO产业链" --market global
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Agent根目录
AGENT_ROOT = Path(__file__).parent.parent
SKILLS_DIR = AGENT_ROOT / "skills"
OUTPUT_DIR = AGENT_ROOT / "output"
CACHE_DIR = AGENT_ROOT / ".cache"


def log_step(step_name: str, status: str = "running"):
    """打印步骤状态"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    symbols = {"running": "▶", "done": "✓", "skip": "○", "error": "✗"}
    print(f"\n[{timestamp}] {symbols.get(status, '▶')} {step_name}")


def check_skill_installed(skill_name: str, skill_path: Path) -> bool:
    """检查skill是否已安装"""
    if not skill_path.exists():
        log_step(f"{skill_name} 未安装", "error")
        print(f"  请先安装: git clone <repo_url> {skill_path}")
        return False
    return True


def step1_serenity_scan(theme: str, market: str) -> dict:
    """
    Step 1: Serenity产业链扫描
    输出: 候选公司列表 + 稀缺层 + 证据链
    """
    log_step("Step 1: Serenity 产业链扫描")
    serenity_dir = SKILLS_DIR / "serenity-skill"

    if not check_skill_installed("Serenity Skill", serenity_dir):
        return {"candidates": [], "error": "Serenity Skill not installed"}

    skill_md = serenity_dir / "SKILL.md"
    if skill_md.exists():
        log_step("  读取 Serenity SKILL.md", "done")

    # Serenity是纯方法论Skill，由Agent执行
    # 这里输出结构化prompt供Agent使用
    result = {
        "module": "serenity",
        "action": "theme_scan",
        "params": {
            "market": market,
            "theme": theme,
            "time_window": "3-12个月",
            "depth": "full_research"
        },
        "skill_path": str(skill_md),
        "references_dir": str(serenity_dir / "references"),
        "instruction": f"""
请按照 Serenity SKILL.md 中的研究工作流执行以下任务：

主题: {theme}
市场: {market}
时间窗口: 3-12个月

执行步骤:
1. 设定范围
2. 将故事转化为系统变化
3. 映射8层价值链
4. 找到稀缺层
5. 构建公司宇宙（≥20家）
6. 收集证据（≥25源）
7. 排序优先级
8. 解释可能出错的地方
9. 给出下一步研究动作

输出格式: JSON，包含 value_chain_layers, scarce_layers, company_universe, evidence_sources, risks, next_steps
"""
    }

    log_step("Step 1: Serenity 产业链扫描", "done")
    return result


def step2_buffett_filter(candidates: list) -> dict:
    """
    Step 2: Buffett快速筛选
    对候选池执行8问检查表
    """
    log_step("Step 2: Buffett 价值投资筛选")
    buffett_dir = SKILLS_DIR / "buffett-skills"

    if not check_skill_installed("Buffett Skills", buffett_dir):
        return {"passed": candidates, "failed": [], "error": "Buffett Skills not installed"}

    skill_md = buffett_dir / "skills" / "buffett" / "SKILL.md"
    if skill_md.exists():
        log_step("  读取 Buffett SKILL.md", "done")

    result = {
        "module": "buffett",
        "action": "quick_filter",
        "params": {
            "candidates": candidates[:5],  # 取Top5
            "mode": "quick_filter"
        },
        "skill_path": str(skill_md),
        "references_dir": str(buffett_dir / "skills" / "buffett" / "references"),
        "instruction": f"""
请按照 Buffett SKILL.md 中的8问快速筛选流程，对以下候选公司逐一评估：

候选公司: {json.dumps(candidates, ensure_ascii=False, indent=2)}

8问检查表:
1. 能力圈: 能用一段话解释它怎么赚钱吗？
2. 持久性: 10年后它还会更有竞争力吗？
3. 护城河: 竞争对手能复制其核心优势吗？
4. 定价权: 能抬价5-10%而不失去大量客户吗？
5. 盈利质量: 利润真实转化为现金了吗？
6. 债务安全: 收入跌30%公司还能活着吗？
7. 管理层诚信: 管理层是否坦诚面对问题？
8. 合理价格: 当前价格与内在价值差距够大吗？

注意: Q7管理层诚信是一票否决项。
输出: passed列表 + failed列表 + 每只股票的评分和理由
"""
    }

    log_step("Step 2: Buffett 价值投资筛选", "done")
    return result


def step3_uzi_analysis(tickers: list) -> dict:
    """
    Step 3: UZI-Skill深度分析
    对筛选通过的标的执行22维数据+65位评审
    """
    log_step("Step 3: UZI-Skill 深度分析")
    uzi_dir = SKILLS_DIR / "uzi-skill"

    if not check_skill_installed("UZI-Skill", uzi_dir):
        return {"reports": [], "error": "UZI-Skill not installed"}

    skill_md = uzi_dir / "skills" / "deep-analysis" / "SKILL.md"
    requirements = uzi_dir / "skills" / "deep-analysis" / "requirements.txt"

    if requirements.exists():
        log_step("  安装 UZI-Skill 依赖...", "running")
        try:
            subprocess.run(
                ["pip", "install", "-r", str(requirements), "--break-system-packages", "-q"],
                check=True, capture_output=True, timeout=300
            )
            log_step("  依赖安装完成", "done")
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
            log_step(f"  依赖安装失败: {e}", "error")

    results = []
    for ticker in tickers[:2]:  # 最多分析2只
        log_step(f"  分析 {ticker}...", "running")
        try:
            result = subprocess.run(
                [sys.executable, "run.py", ticker],
                cwd=str(uzi_dir),
                capture_output=True, text=True, timeout=600
            )
            cache_dir = uzi_dir / ".cache" / ticker
            report_html = cache_dir / "report.html"
            results.append({
                "ticker": ticker,
                "success": result.returncode == 0,
                "report_path": str(report_html) if report_html.exists() else None,
                "cache_dir": str(cache_dir) if cache_dir.exists() else None,
                "stdout": result.stdout[-500:] if result.stdout else "",
                "stderr": result.stderr[-500:] if result.stderr else ""
            })
            log_step(f"  分析 {ticker}", "done" if result.returncode == 0 else "error")
        except subprocess.TimeoutExpired:
            log_step(f"  分析 {ticker} 超时", "error")
            results.append({"ticker": ticker, "success": False, "error": "timeout"})

    return {
        "module": "uzi-skill",
        "action": "deep_analysis",
        "results": results,
        "skill_path": str(skill_md)
    }


def step4_trading_agents(tickers: list, date: str = None) -> dict:
    """
    Step 4: TradingAgents多Agent交易决策
    """
    log_step("Step 4: TradingAgents 多Agent交易决策")
    ta_dir = SKILLS_DIR / "TradingAgents"

    if not check_skill_installed("TradingAgents", ta_dir):
        return {"decisions": [], "error": "TradingAgents not installed"}

    if date is None:
        date = datetime.now().strftime("%Y-%m-%d")

    requirements = ta_dir / "requirements.txt"
    if requirements.exists():
        log_step("  安装 TradingAgents 依赖...", "running")
        try:
            subprocess.run(
                ["pip", "install", "-r", str(requirements), "--break-system-packages", "-q"],
                check=True, capture_output=True, timeout=300
            )
            log_step("  依赖安装完成", "done")
        except (subprocess.TimeoutExpired, subprocess.CalledProcessError) as e:
            log_step(f"  依赖安装失败: {e}", "error")

    results = []
    for ticker in tickers[:2]:
        log_step(f"  多Agent分析 {ticker}...", "running")
        try:
            env = os.environ.copy()
            env["TRADINGAGENTS_OUTPUT_LANGUAGE"] = "zh"
            result = subprocess.run(
                [sys.executable, "main.py", "--ticker", ticker, "--date", date],
                cwd=str(ta_dir),
                capture_output=True, text=True, timeout=900,
                env=env
            )
            results.append({
                "ticker": ticker,
                "success": result.returncode == 0,
                "stdout": result.stdout[-1000:] if result.stdout else "",
                "stderr": result.stderr[-500:] if result.stderr else ""
            })
            log_step(f"  多Agent分析 {ticker}", "done" if result.returncode == 0 else "error")
        except subprocess.TimeoutExpired:
            log_step(f"  多Agent分析 {ticker} 超时", "error")
            results.append({"ticker": ticker, "success": False, "error": "timeout"})

    return {
        "module": "trading-agents",
        "action": "multi_agent_decision",
        "results": results
    }


def step5_quantdinger_backtest(strategy_code: str = None) -> dict:
    """
    Step 5: QuantDinger策略回测
    """
    log_step("Step 5: QuantDinger 策略回测")
    qd_dir = SKILLS_DIR / "QuantDinger"

    if not check_skill_installed("QuantDinger", qd_dir):
        return {"backtest": None, "error": "QuantDinger not installed"}

    docker_compose = qd_dir / "docker-compose.yml"
    if docker_compose.exists():
        log_step("  检查Docker服务状态...", "running")
        try:
            result = subprocess.run(
                ["docker", "compose", "ps"],
                cwd=str(qd_dir),
                capture_output=True, text=True, timeout=30
            )
            if "running" in result.stdout:
                log_step("  QuantDinger 服务运行中", "done")
            else:
                log_step("  QuantDinger 服务未运行，请先启动:", "error")
                print(f"    cd {qd_dir} && docker-compose up -d")
        except FileNotFoundError:
            log_step("  Docker未安装", "error")

    return {
        "module": "quantdinger",
        "action": "backtest",
        "api_url": "http://localhost:5000/api/backtest/run",
        "mcp_package": "quantdinger-mcp",
        "instruction": """
QuantDinger需要Docker环境运行。如果Docker不可用，可以：
1. 在本地Python环境中编写策略代码
2. 使用yfinance获取数据进行简单回测
3. 或跳过此步骤，仅使用前4个模块的分析结果
"""
    }


def generate_report(steps_results: dict, theme: str, output_dir: Path):
    """生成最终研究报告"""
    log_step("生成研究报告")
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = output_dir / f"research_{theme}_{timestamp}.md"

    report = f"""# {theme} 投研报告

> 生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
> Agent: 全栈AI投研Agent v1.0
> 免责声明: 本报告仅供研究参考，不构成任何投资建议。

---

## 研究流程概览

"""

    for step_name, result in steps_results.items():
        status = "✓ 完成" if result.get("success", True) else "✗ 失败"
        if "error" in result and result["error"]:
            status = f"✗ {result['error']}"
        report += f"- {step_name}: {status}\n"

    report += "\n---\n"

    # Serenity结果
    if "serenity" in steps_results:
        r = steps_results["serenity"]
        report += """## 一、产业链分析（Serenity）

> Serenity产业链瓶颈猎手分析结果

"""
        if "instruction" in r:
            report += "**Agent执行指令:**\n```json\n"
            report += json.dumps({"theme": r["params"]["theme"], "market": r["params"]["market"]}, ensure_ascii=False, indent=2)
            report += "\n```\n\n"
        report += "> ⚠️ Serenity为方法论Skill，需由AI Agent执行上述指令完成分析。\n"
        report += "> 请将上述instruction输入到支持Agent Skill的AI编程助手中执行。\n\n"

    # Buffett结果
    if "buffett" in steps_results:
        r = steps_results["buffett"]
        report += """## 二、价值投资筛选（Buffett）

> 巴菲特8问快速筛选结果

"""
        if "instruction" in r:
            report += "**Agent执行指令:**\n\n"
            report += r["instruction"] + "\n\n"
        report += "> ⚠️ Buffett Skills为方法论Skill，需由AI Agent执行上述指令完成分析。\n\n"

    # UZI结果
    if "uzi" in steps_results:
        r = steps_results["uzi"]
        report += """## 三、深度分析（UZI-Skill）

"""
        for item in r.get("results", []):
            ticker = item.get("ticker", "unknown")
            success = item.get("success", False)
            report_path = item.get("report_path")
            report += f"### {ticker}\n"
            report += f"- 状态: {'✓ 成功' if success else '✗ 失败'}\n"
            if report_path:
                report += f"- 报告路径: `{report_path}`\n"
            if item.get("stdout"):
                report += f"- 输出摘要: {item['stdout'][:200]}\n"
            report += "\n"

    # TradingAgents结果
    if "trading_agents" in steps_results:
        r = steps_results["trading_agents"]
        report += """## 四、多Agent交易决策（TradingAgents）

"""
        for item in r.get("results", []):
            ticker = item.get("ticker", "unknown")
            success = item.get("success", False)
            report += f"### {ticker}\n"
            report += f"- 状态: {'✓ 成功' if success else '✗ 失败'}\n"
            if item.get("stdout"):
                report += f"- 输出摘要: {item['stdout'][:300]}\n"
            report += "\n"

    # QuantDinger结果
    if "quantdinger" in steps_results:
        r = steps_results["quantdinger"]
        report += """## 五、策略回测（QuantDinger）

"""
        if r.get("instruction"):
            report += r["instruction"] + "\n"
        if r.get("api_url"):
            report += f"- API地址: `{r['api_url']}`\n"
        report += "\n"

    report += """---

## 六、关键风险

1. **数据风险**: 分析依赖公开数据，可能存在延迟或偏差
2. **模型风险**: AI分析可能存在幻觉或误判
3. **市场风险**: 市场环境变化可能导致分析结论失效
4. **流动性风险**: 部分标的可能流动性不足

## 七、后续验证动作

- [ ] 对Serenity识别的稀缺层进行实地/电话调研验证
- [ ] 跟踪候选公司的最新财报和公告
- [ ] 监控产业链上下游的产能变化
- [ ] 定期更新估值模型参数

## 八、免责声明

本报告由AI投研Agent自动生成，所有分析仅供研究参考，**不构成任何投资建议**。
投资有风险，决策需谨慎。过往业绩不代表未来表现。
"""

    report_file.write_text(report, encoding="utf-8")
    log_step(f"报告已保存: {report_file}", "done")
    return str(report_file)


def main():
    parser = argparse.ArgumentParser(description="全栈AI投研Agent - 主题研究")
    parser.add_argument("--theme", required=True, help="研究主题，如'A股AI半导体'")
    parser.add_argument("--market", default="A-share", help="市场: A-share/HK/US/global")
    parser.add_argument("--date", default=None, help="分析日期 (YYYY-MM-DD)")
    parser.add_argument("--skip-steps", default=[], nargs="+",
                        help="跳过的步骤: serenity/buffett/uzi/trading/quant")
    parser.add_argument("--output", default=None, help="输出目录")

    args = parser.parse_args()

    print(f"""
╔══════════════════════════════════════════╗
║       全栈AI投研Agent v1.0              ║
║       主题: {args.theme:<24s}║
║       市场: {args.market:<24s}║
╚══════════════════════════════════════════╝
""")

    output_dir = Path(args.output) if args.output else OUTPUT_DIR
    steps_results = {}

    # Step 1: Serenity
    if "serenity" not in args.skip_steps:
        steps_results["serenity"] = step1_serenity_scan(args.theme, args.market)

    # Step 2: Buffett (需要Serenity的候选公司列表)
    if "buffett" not in args.skip_steps:
        candidates = steps_results.get("serenity", {}).get("company_universe", [])
        if not candidates:
            candidates = [{"name": args.theme, "ticker": "待定"}]
        steps_results["buffett"] = step2_buffett_filter(candidates)

    # Step 3: UZI (需要Buffett筛选通过的标的)
    if "uzi" not in args.skip_steps:
        passed = steps_results.get("buffett", {}).get("passed", [])
        tickers = [c.get("ticker", "") for c in passed if c.get("ticker")]
        if not tickers:
            tickers = ["600519.SH"]  # 默认示例
        steps_results["uzi"] = step3_uzi_analysis(tickers)

    # Step 4: TradingAgents
    if "trading" not in args.skip_steps:
        tickers = steps_results.get("uzi", {}).get("results", [])
        ta_tickers = [r.get("ticker", "") for r in tickers if r.get("ticker")]
        if not ta_tickers:
            ta_tickers = ["NVDA"]
        steps_results["trading_agents"] = step4_trading_agents(ta_tickers, args.date)

    # Step 5: QuantDinger
    if "quant" not in args.skip_steps:
        steps_results["quantdinger"] = step5_quantdinger_backtest()

    # 生成报告
    report_path = generate_report(steps_results, args.theme, output_dir)

    print(f"""
╔══════════════════════════════════════════╗
║       研究流程完成                        ║
║       报告: {report_path:<30s}║
╚══════════════════════════════════════════╝
""")


if __name__ == "__main__":
    main()
