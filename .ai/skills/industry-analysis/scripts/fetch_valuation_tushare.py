#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
估值分位取数脚本（tushare 版，industry-analysis skill 可选增强 · methodology 第七节配套）
=============================================================================
与上游原版 fetch_valuation.py（akshare/东财）功能等价，数据源换为 workspace
共享的 tushare 兼容端点（daily_basic 接口：PE(TTM)/PB/PS(TTM) 日频序列）。
凭证自动加载（.env 向上查找 TUSHARE_TOKEN/TUSHARE_API_URL，与 tushare-connector 一致），
无需安装 akshare，无需额外 token。

位置说明：本脚本是 industry-analysis 的本地辅助脚本，不修改第三方 skill 原文件；
运行时只需 pandas + requests（项目 venv：.venv/bin/python）。

用法（CLI 与原版兼容）：
    python3 fetch_valuation_tushare.py 688017 002050 601689 300124
    python3 fetch_valuation_tushare.py 688017 --years 3        # 改分位回看年数
    python3 fetch_valuation_tushare.py 688017 --md             # 直接输出 markdown 表

设计原则（对齐 methodology 防编造硬约束）：
- 历史 PE/PB/PS 分位 = 可靠输出（真实日频序列算出来的），可直接写进报告。
- PEG：tushare daily_basic 无该字段（东财特有）→ 一律标 ❓ 降级为定性判断，不编造。
- 取不到数据时明确报错，不猜数——宁可留白让用户用 Wind 补。
"""
import sys
import argparse
import datetime as dt
from pathlib import Path

import pandas as pd

# 定位 workspace 共享 tushare 客户端：从脚本目录向上查找 tushare-connector（最多 6 层）
def _find_tushare_client() -> Path:
    d = Path(__file__).resolve().parent
    for _ in range(6):
        cand = d / ".claude" / "skills" / "tushare-connector" / "scripts" / "tushare_client.py"
        if cand.is_file():
            return cand
        if d.parent == d:
            break
        d = d.parent
    raise FileNotFoundError(
        "未找到 tushare-connector/scripts/tushare_client.py——请确认 workspace 结构完整"
    )

sys.path.insert(0, str(_find_tushare_client().parent))
import tushare_client as tc  # noqa: E402


def to_ts_code(code: str) -> str:
    """6 位 A 股代码 → ts_code（带交易所后缀）。"""
    code = code.strip()
    if code.startswith(("6", "9")):
        return f"{code}.SH"
    if code.startswith(("0", "2", "3")):
        return f"{code}.SZ"
    if code.startswith(("4", "8")):
        return f"{code}.BJ"
    return f"{code}.SH"


def pct_rank(series: pd.Series, value: float):
    """value 在 series 中的历史分位（%），0=最低、100=最高。"""
    s = series.dropna()
    if len(s) == 0 or pd.isna(value):
        return None
    return round((s < value).mean() * 100)


def fetch_one(code: str, years: int = 5) -> dict:
    """取单只股票的当前估值 + 历史分位（daily_basic 日频）。返回 dict 或抛异常。"""
    ts_code = to_ts_code(code)
    end = dt.date.today()
    start = end - dt.timedelta(days=365 * years + 30)  # 多留 30 天窗口覆盖交易日偏移
    resp = tc.query(
        "daily_basic",
        {"ts_code": ts_code, "start_date": start.strftime("%Y%m%d"), "end_date": end.strftime("%Y%m%d")},
        "ts_code,trade_date,pe_ttm,pb,ps_ttm",
    )
    # tushare 原始响应结构：{"fields": [...], "items": [[...], ...]}
    if not resp or not resp.get("items"):
        raise ValueError(f"{ts_code} 无估值数据（{start}~{end}）")
    df = pd.DataFrame(resp["items"], columns=resp["fields"])
    df["trade_date"] = pd.to_datetime(df["trade_date"])
    df = df.sort_values("trade_date").reset_index(drop=True)
    cur = df.iloc[-1]
    return {
        "code": code,
        "date": cur["trade_date"].date(),
        "pe": cur["pe_ttm"], "pe_pct": pct_rank(df["pe_ttm"], cur["pe_ttm"]),
        "pb": cur["pb"], "pb_pct": pct_rank(df["pb"], cur["pb"]),
        "ps": cur["ps_ttm"], "ps_pct": pct_rank(df["ps_ttm"], cur["ps_ttm"]),
        "peg": None, "peg_flag": " ❓(tushare 无 PEG 字段，需另取口径)",
        "n": len(df), "years": years,
    }


def fmt(v, nd=1):
    try:
        return f"{float(v):.{nd}f}"
    except (TypeError, ValueError):
        return "—"


def main():
    ap = argparse.ArgumentParser(description="取 A 股历史估值分位（tushare daily_basic，凭证自动加载）")
    ap.add_argument("codes", nargs="+", help="6 位股票代码，如 688017 002050")
    ap.add_argument("--years", type=int, default=5, help="分位回看年数，默认 5")
    ap.add_argument("--md", action="store_true", help="输出 markdown 表格")
    args = ap.parse_args()

    rows = []
    for code in args.codes:
        try:
            rows.append(fetch_one(code, args.years))
        except Exception as e:  # noqa: BLE001
            print(f"[skip] {code}: {type(e).__name__}: {e}", file=sys.stderr)

    if not rows:
        sys.exit("全部取数失败")

    if args.md:
        print("| 标的 | 截至 | PE(TTM) | PE分位({}Y) | PB | PB分位 | PS | PS分位 | PEG |".format(args.years))
        print("|---|---|---|---|---|---|---|---|---|")
        for r in rows:
            print(f"| {r['code']} | {r['date']} | {fmt(r['pe'])} | {r['pe_pct']}% | "
                  f"{fmt(r['pb'],2)} | {r['pb_pct']}% | {fmt(r['ps'])} | {r['ps_pct']}% | "
                  f"{fmt(r['peg'],2)}{r['peg_flag']} |")
    else:
        for r in rows:
            print(f"{r['code']} 截至{r['date']} (近{r['years']}年,{r['n']}日): "
                  f"PE(TTM)={fmt(r['pe'])}[分位{r['pe_pct']}%] "
                  f"PB={fmt(r['pb'],2)}[分位{r['pb_pct']}%] "
                  f"PS={fmt(r['ps'])}[分位{r['ps_pct']}%] "
                  f"PEG={fmt(r['peg'],2)}{r['peg_flag']}")

    print("\n注：PE/PB/PS 历史分位为真实日频序列算出，可直接引用；"
          "PEG 无 tushare 口径，标 ❓ 应降级为定性判断。", file=sys.stderr)


if __name__ == "__main__":
    main()
