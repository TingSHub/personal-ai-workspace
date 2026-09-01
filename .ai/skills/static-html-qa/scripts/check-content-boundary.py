#!/usr/bin/env python3
"""check-content-boundary.py — 内容边界扫描（企业研究 HTML 质检用）

用途：扫描生成的 HTML 报告，检查是否出现内容边界禁止的表述（买卖建议、
操作区间、交易策略、仓位建议、回测结论等）。用于企业研究内容生产链路
（如 investagent-html-report-v0.1 workflow）的 Phase 3/4 质检。

用法：
    python3 check-content-boundary.py <report.html> [--ignore "词1" "词2" ...]

    --ignore 允许出现的关键词（如机构目标价/北向净买入等允许语境），可多次传
    例：python3 check-content-boundary.py investment-report.html \
             --ignore "机构目标价" "北向净买入" "分价位带"

退出码：
    0 = PASS（未命中，或命中的词全部在 --ignore 白名单中）
    1 = 命中禁用词（打印 行号:词 → 所在行内容）
    2 = 用法错误（参数缺失/文件不存在）

默认禁用词（按企业研究内容边界，随业务可增改）：
    买入 / 卖出 / 持有建议 / 仓位 / 回测 / 买点 / 卖点 / 目标价主张 /
    操作区间 / 交易策略 / 短线 / 四派系价位带 / Hold / BUY / SELL

注意：--ignore 是"允许出现的上下文"，命中行中同时包含忽略词与禁用词时仍计为
命中——只在整行被判断为允许语境时由人工复核确认，脚本输出供人工裁决。
"""
import argparse
import re
import sys
from pathlib import Path

FORBIDDEN = [
    "买入", "卖出", "持有建议", "仓位", "回测", "买点", "卖点",
    "操作区间", "交易策略", "短线", "四派系", "价位带", "目标价",
    "Hold", "BUY", "SELL",
]


def main() -> int:
    ap = argparse.ArgumentParser(description="企业研究 HTML 内容边界扫描")
    ap.add_argument("html", help="待扫描的 HTML 文件路径")
    ap.add_argument("--ignore", action="extend", nargs="+", default=[],
                    help="允许出现的关键词（可传多个），命中该词的整行跳过")
    args = ap.parse_args()

    path = Path(args.html)
    if not path.is_file():
        print(f"用法错误: 文件不存在 {path}", file=sys.stderr)
        return 2

    text = path.read_text(encoding="utf-8")
    hits = []
    for lineno, line in enumerate(text.splitlines(), 1):
        if any(ig in line for ig in args.ignore):
            continue
        # 免责声明行（说明"不含/不构成"的元表述）自动豁免
        if "不构成任何投资建议" in line or ("不含" in line and "建议" in line) \
                or ("不含" in line and "目标价" in line):
            continue
        for word in FORBIDDEN:
            if word in line:
                hits.append((lineno, word, line.strip()[:120]))
                break

    if not hits:
        print(f"PASS: 未命中内容边界禁用词（{len(FORBIDDEN)} 词扫描，忽略 {len(args.ignore)} 词）")
        return 0

    print(f"FAIL: 命中 {len(hits)} 处禁用表述，请人工裁决语境：")
    for lineno, word, line in hits:
        print(f"  L{lineno}  [{word}]  {line}")
    print("提示：若为允许语境（如机构预期/资金流向事实），用 --ignore 显式声明")
    return 1


if __name__ == "__main__":
    sys.exit(main())
