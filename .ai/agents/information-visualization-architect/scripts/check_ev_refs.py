#!/usr/bin/env python3
"""check_ev_refs.py — EV 引用可解析性检查（v0.2.1）

检查 visual-brief.md（及 content-thesis.md）中所有「数据引用: EV-xxx」是否在
evidence-reference.md 中存在对应条目（EV-001~EV-0NN）。

用法:
    python3 check_ev_refs.py <visual-brief.md> <evidence-reference.md>
    python3 check_ev_refs.py <visual-brief.md> <evidence-reference.md> --strict

输出:
    缺失引用列表（不可解析的 EV-xxx）、引用统计、退出码（有缺失=1，--strict 时也检查软性注意点）
"""
import re
import sys

EV_REF_RE = re.compile(r"\bEV-(\d{3})\b")


def extract_evs(path: str) -> set[int]:
    """提取文件中所有 EV-xxx 编号。"""
    evs: set[int] = set()
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                for m in EV_REF_RE.finditer(line):
                    evs.add(int(m.group(1)))
    except FileNotFoundError:
        print(f"[ERROR] 文件不存在: {path}")
        sys.exit(2)
    return evs


def main() -> int:
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    brief_path, ev_path = sys.argv[1], sys.argv[2]
    strict = "--strict" in sys.argv[3:]

    refs = extract_evs(brief_path)
    defined = extract_evs(ev_path)
    missing = sorted(refs - defined)

    print(f"visual-brief 引用 EV 编号: {len(refs)} 个去重")
    print(f"evidence-reference 已定义: {len(defined)} 个")
    if missing:
        print(f"[FAIL] 不可解析引用 {len(missing)} 个:")
        for n in missing:
            print(f"  EV-{n:03d} — 在 evidence-reference 中不存在")
        print("处理: 反馈问题并回传上游（visual-brief 不得引用未定义条目）")
        return 1
    print("[PASS] 全部引用可解析（差集为空）")
    if strict:
        unused = sorted(defined - refs)
        print(f"（strict）evidence-reference 未被引用的条目: {len(unused)} 个"
              f"{'（正常，供查询）' if len(unused) <= 5 else ' — 注意 visual-brief 覆盖度'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
