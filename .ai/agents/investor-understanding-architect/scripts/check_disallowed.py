#!/usr/bin/env python3
"""check_disallowed.py — 禁用数字/表述出现检查（v0.2.1）

检查 content-thesis.md / visual-brief.md / visual-plan/*.md 中禁用数字是否出现。

用法:
    python3 check_disallowed.py <file.md> -- "PEG" "58倍" "57.86" "46%"
    # 或从文件读取禁用清单（每行一个）:
    python3 check_disallowed.py <file.md> --list <disallowed.txt>

输出:
    命中清单（含行号与语境） + 退出码（有命中=1）
注意:
    禁用清单按公司/案例变化，命中需要人工确认是否处于「禁止项说明/处理语境」（此类不算违规）。
"""
import sys


def load_list(args: list[str]) -> list[str]:
    if not args:
        print("用法: check_disallowed.py <file.md> -- '禁用词1' '禁用词2' ... 或 --list <file>")
        sys.exit(2)
    if args[0] == "--list":
        try:
            return [l.strip() for l in open(args[1], encoding="utf-8") if l.strip()]
        except FileNotFoundError:
            print(f"[ERROR] 清单文件不存在: {args[1]}")
            sys.exit(2)
    return [a for a in args if a != "--"]


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    path = sys.argv[1]
    disallowed = load_list(sys.argv[2:])
    try:
        lines = open(path, encoding="utf-8").readlines()
    except FileNotFoundError:
        print(f"[ERROR] 文件不存在: {path}")
        return 2

    hits: list[tuple[int, str, str]] = []
    for i, line in enumerate(lines, 1):
        for d in disallowed:
            if d in line:
                hits.append((i, d, line.strip()[:80]))

    print(f"检查: {path}（禁用项 {len(disallowed)} 个）")
    if not hits:
        print("[PASS] 禁用数字零出现")
        return 0
    print(f"[CHECK] 命中 {len(hits)} 处（需人工确认语境：禁止项说明/处理语境不算违规）:")
    for i, d, ctx in hits:
        print(f"  行 {i} [{d}]: {ctx}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
