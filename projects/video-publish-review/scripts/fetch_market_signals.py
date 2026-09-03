#!/usr/bin/env python3
"""选题前瞻 P1 信号扫描：免费数据源（akshare）—— 每日市场信号 → JSON。

数据源（免费，无 token）：
- 东财涨停池 stock_zt_pool_em：当日涨停股（题材锚点）
- 新浪全量行情 stock_zh_a_spot：5554 只，用于涨幅/换手/量比筛选
用法：python3 fetch_market_signals.py [--date 2026-09-02] [--out /path/signals.json]
"""
import argparse
import json
import sys
from datetime import datetime


def fetch_zt_pool(date: str):
    import akshare as ak
    df = ak.stock_zt_pool_em(date=date)
    recs = []
    for _, r in df.iterrows():
        recs.append({
            "code": str(r.get("代码", "")),
            "name": str(r.get("名称", "")),
            "price": float(r.get("最新价", 0) or 0),
            "pct_chg": float(r.get("涨跌幅", 0) or 0),
            "turnover": float(r.get("换手率", 0) or 0),
            "industry": str(r.get("所属行业", "")),
        })
    return recs


def fetch_movers(top_n: int = 200):
    import akshare as ak
    df = ak.stock_zh_a_spot()
    cols = list(df.columns)
    name_col = "名称" if "名称" in cols else None
    code_col = "代码" if "代码" in cols else None
    pct_col = "涨跌幅" if "涨跌幅" in cols else None
    turn_col = "换手率" if "换手率" in cols else None
    if not (name_col and pct_col):
        return []
    df = df.dropna(subset=[pct_col])
    # 排除 ST / 退市
    exclude = df[name_col].str.contains("ST|退", na=False)
    df = df[~exclude]
    df = df.sort_values(pct_col, ascending=False).head(top_n)
    recs = []
    for _, r in df.iterrows():
        recs.append({
            "code": str(r.get(code_col, "")),
            "name": str(r.get(name_col, "")),
            "pct_chg": float(r.get(pct_col, 0) or 0),
            "turnover": float(r.get(turn_col, 0) or 0) if turn_col else None,
        })
    return recs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", default=datetime.now().strftime("%Y%m%d"))
    ap.add_argument("--out", default="")
    ap.add_argument("--web-fallback", action="store_true",
                    help="spot 接口失败时追加提示（数据源切换建议），不影响流程")
    args = ap.parse_args()

    signals = {"captured_at": datetime.now().isoformat(timespec="seconds"),
               "trade_date": args.date,
               "zt_pool": [], "movers": []}
    errors = []

    # 1) 涨停池
    try:
        signals["zt_pool"] = fetch_zt_pool(args.date)
        print(f"[OK] 涨停池 {len(signals['zt_pool'])} 只")
    except Exception as e:
        errors.append(f"zt_pool: {str(e)[:120]}")
        print(f"[WARN] 涨停池失败: {e.__class__.__name__}")

    # 2) 全量行情筛选
    try:
        signals["movers"] = fetch_movers()
        print(f"[OK] 涨幅榜 {len(signals['movers'])} 只")
    except Exception as e:
        errors.append(f"movers: {str(e)[:120]}")
        print(f"[WARN] 全量行情失败: {e.__class__.__name__}")

    signals["errors"] = errors

    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            json.dump(signals, f, ensure_ascii=False, indent=1)
        print(f"written: {args.out}")
    else:
        print(json.dumps(signals, ensure_ascii=False, indent=1)[:1500])


if __name__ == "__main__":
    main()
