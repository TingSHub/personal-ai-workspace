#!/usr/bin/env python3
"""verify_financial.py — 财务数据一致性验证（RD v0.3 辅助脚本，可选不强制）

用法:
    1. 双值对比（两个来源同指标）:
       python3 verify_financial.py --compare --metric PE --a 20.3 --a-source tushare --b 18.84 --b-source uzi

    2. PE/PB 重算（从 tushare daily_basic JSON，优先权威来源）:
       python3 verify_financial.py --pe --daily-basic data/daily_basic.json --price 1341.99

    3. ROE/净利率重算（从 tushare income/fina_indicator JSON）:
       python3 verify_financial.py --roe --fina data/fina_indicator.json --period 20251231

输出:
    对比/重算结果 + 结论建议（一致/口径差异/需人工核对），退出码 0=一致，1=差异，2=用法错误

说明:
    - 数据优先级（验证时）：财报/法定披露 > tushare 结构化数据 > 其他来源
    - 本脚本只做计算与对比，不替代 RD 的验证判断（口径归属、真值选择由 RD 结合上下文决定）
"""
import argparse
import json
import sys


def compare(metric: str, a: float, a_source: str, b: float, b_source: str) -> int:
    diff = abs(a - b)
    rel = diff / max(abs(a), abs(b), 1e-9) * 100
    print(f"[对比] {metric}: {a} ({a_source}) vs {b} ({b_source})")
    print(f"  绝对差 {diff:.4f}，相对差 {rel:.2f}%")
    if rel < 0.5:
        print(f"  → 结论: 数值一致（差异 {rel:.2f}% < 0.5%，可视为舍入/口径微差）")
        return 0
    if rel < 5:
        print(f"  → 结论: 存在差异（{rel:.2f}%），疑似口径不同——需 RD 按优先级核对口径")
        return 1
    print(f"  → 结论: 显著差异（{rel:.2f}%），需验证——按优先级（财报 > tushare）重算真值")
    return 1


def calc_pe(daily_basic_path: str, price: float) -> int:
    """从 tushare daily_basic JSON 重算 PE(TTM)。JSON 结构: [{ts_code, trade_date, pe_ttm, ...}]"""
    try:
        with open(daily_basic_path, encoding="utf-8") as f:
            rows = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"[ERROR] 读取 daily_basic 失败: {e}")
        return 2
    if not rows:
        print("[ERROR] daily_basic 为空")
        return 2
    # 取最新一条
    latest = max(rows, key=lambda r: r.get("trade_date", ""))
    pe = latest.get("pe_ttm")
    print(f"[重算] PE(TTM) 核对: {latest.get('ts_code')} @ {latest.get('trade_date')}")
    print(f"  tushare pe_ttm = {pe}")
    if pe:
        implied = price / pe
        print(f"  隐含 EPS(TTM) = 价格/PE = {price}/{pe} = {implied:.4f}")
        print(f"  → 验证: 用财报 EPS(TTM) 对照隐含 EPS；口径一致则 PE 可信")
    return 0


def calc_roe(fina_path: str, period: str) -> int:
    """从 tushare fina_indicator JSON 核对 ROE。JSON 结构: [{ts_code, end_date, roe, roe_waa, ...}]"""
    try:
        with open(fina_path, encoding="utf-8") as f:
            rows = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"[ERROR] 读取 fina_indicator 失败: {e}")
        return 2
    matches = [r for r in rows if str(r.get("end_date", "")).startswith(str(period))]
    if not matches:
        print(f"[ERROR] 未找到报告期 {period} 的数据")
        return 2
    for r in matches:
        print(f"[核对] {r.get('ts_code')} @ {r.get('end_date')}: roe={r.get('roe')}, "
              f"roe_waa={r.get('roe_waa')}, netprofit_margin={r.get('netprofit_margin')}")
    # 检查同指标多值
    roes = {r.get("roe") for r in matches if r.get("roe") is not None}
    if len(roes) > 1:
        print(f"  → 发现 ROE 多值: {sorted(roes)}——同源多值需 RD 核对字段口径（加权/摊薄/年化）")
        return 1
    print("  → 同报告期 ROE 单值一致")
    return 0


def main() -> int:
    p = argparse.ArgumentParser(description="财务数据一致性验证（RD v0.3）")
    p.add_argument("--compare", action="store_true", help="双值对比模式")
    p.add_argument("--metric", default="指标")
    p.add_argument("--a", type=float)
    p.add_argument("--a-source", default="来源A")
    p.add_argument("--b", type=float)
    p.add_argument("--b-source", default="来源B")
    p.add_argument("--pe", action="store_true", help="PE(TTM) 重算模式")
    p.add_argument("--daily-basic", help="tushare daily_basic JSON 路径")
    p.add_argument("--price", type=float, help="当前价格（重算隐含 EPS 用）")
    p.add_argument("--roe", action="store_true", help="ROE 核对模式")
    p.add_argument("--fina", help="tushare fina_indicator JSON 路径")
    p.add_argument("--period", default="", help="报告期（如 20251231）")
    args = p.parse_args()

    if args.compare and args.a is not None and args.b is not None:
        return compare(args.metric, args.a, args.a_source, args.b, args.b_source)
    if args.pe and args.daily_basic and args.price:
        return calc_pe(args.daily_basic, args.price)
    if args.roe and args.fina:
        return calc_roe(args.fina, args.period)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
