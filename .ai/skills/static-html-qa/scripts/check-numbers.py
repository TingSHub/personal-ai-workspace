#!/usr/bin/env python3
"""check-numbers.py — HTML 数值一致性校验（多源研究 → 统一 HTML 质检用）

用途：把裁决后的期望数值清单（TSV）与生成的 HTML 逐一比对，确认手工 SVG
坐标换算 / 转录没有引入错误。用于 investagent-html-report-v0.1 workflow
Phase 3/4 质检——所有数字必须与裁决结果一致才允许交付。

期望清单格式（TSV，UTF-8，无表头）：
    <数值>\t<标签>[\t<模式>]
    模式：round = 允许四舍五入到整数（默认，如 1720.5 匹配 1721 或 1720.5）
          exact = 必须精确匹配（如 51.98）
          pct   = 百分数，允许 1 位小数差异（如 3.88 匹配 3.88 或 3.9）
    例：
    1720.5\t2025营业总收入\tround
    51.98\tFY2025每股分红\texact
    3.88\t股息率\tpct

用法：
    python3 check-numbers.py <expected.tsv> <report.html>

退出码：
    0 = PASS（全部数值在 HTML 中找到）
    1 = 有数值未命中（打印 标签 + 期望值 + 模式）
    2 = 用法错误（参数缺失/文件不存在/清单格式错误）

说明：数值以字符串形式在 HTML 中查找（含千分位分隔与全角/半角差异由
round 模式兜底）；命中即通过，不统计出现次数。
"""
import argparse
import sys
from pathlib import Path


def norm(v: str) -> str:
    return v.replace(",", "").replace("，", "").replace(" ", "").strip()


def main() -> int:
    ap = argparse.ArgumentParser(description="HTML 数值一致性校验")
    ap.add_argument("expected", help="期望数值 TSV 清单路径")
    ap.add_argument("html", help="待校验 HTML 路径")
    args = ap.parse_args()

    exp_path, html_path = Path(args.expected), Path(args.html)
    if not exp_path.is_file() or not html_path.is_file():
        print("用法错误: 清单或 HTML 文件不存在", file=sys.stderr)
        return 2

    html = norm(html_path.read_text(encoding="utf-8"))
    missing = []
    with exp_path.open(encoding="utf-8") as f:
        for lineno, raw in enumerate(f, 1):
            raw = raw.strip()
            if not raw or raw.startswith("#"):
                continue
            parts = raw.split("\t")
            if len(parts) < 2:
                print(f"用法错误: 清单 L{lineno} 格式不符（需 数值<TAB>标签[<TAB>模式]）", file=sys.stderr)
                return 2
            value, label = parts[0].strip(), parts[1].strip()
            mode = parts[2].strip() if len(parts) > 2 else "round"

            v = norm(value)
            found = v in html
            if not found and mode == "round":
                try:
                    found = str(round(float(v))) in html
                except ValueError:
                    pass
            if not found and mode == "pct":
                try:
                    fv = float(v)
                    candidates = [f"{fv:.1f}", f"{round(fv, 1)}", f"{fv}"]
                    found = any(c in html for c in candidates)
                    # 同时容忍 1 位小数差（3.88 与 3.9）
                    if not found:
                        found = f"{round(fv, 1)}" in html
                except ValueError:
                    pass
            if not found:
                missing.append((label, value, mode))

    if not missing:
        print("PASS: 期望清单全部数值已找到")
        return 0

    print(f"FAIL: {len(missing)} 项数值未在 HTML 中找到：")
    for label, value, mode in missing:
        print(f"  [{mode}] {label}: 期望 {value}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
