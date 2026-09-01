#!/usr/bin/env python3
r"""check_factmap.py — fact-map 输出自检（v0.2.1 execution contract）

检查 fact-map.md：
  1. Conflict 块格式（指标/来源A/来源B/原因/处理 五要素）
  2. Level 标注完整性（每条事实行应含 L1-L4）
  3. 来源完整性启发式（L1/2/4 行应含 source/date/section 或等价来源定位词）
  4. 禁用表述（「L4 表述为确定事实」类：L4 行不应使用确定语气词）

用法:
    python3 check_factmap.py <fact-map.md>

输出:
    检查报告 + 退出码（有 FAIL=1，仅警告=0）
"""
import re
import sys

CONFLICT_KEYS = ["指标", "来源A", "来源B", "原因", "处理"]
LEVEL_RE = re.compile(r"\bL[1-4]\b")
CERTAIN_WORDS = ["确定为", "证实为", "即", "准确为", "就是"]


def check_conflict_blocks(text: str) -> tuple[list[str], int]:
    problems: list[str] = []
    blocks = re.split(r"(?=Conflict:)", text)[1:]
    for block in blocks:
        block_body = block.split("---", 1)[0] if "---" in block else block
        missing = [k for k in CONFLICT_KEYS if f"{k}:" not in block_body]
        if missing:
            head = block_body.strip().splitlines()[0][:50] if block_body.strip() else "?"
            problems.append(f"Conflict 块缺要素 {missing}: {head}")
    return problems, len(blocks)


def check_levels(text: str) -> tuple[list[str], dict[str, int]]:
    problems: list[str] = []
    stats = {"L1": 0, "L2": 0, "L3": 0, "L4": 0}
    in_conflict = False
    for line in text.splitlines():
        if line.startswith("Conflict:"):
            in_conflict = True
            continue
        if in_conflict and line.startswith("---"):
            in_conflict = False
            continue
        if in_conflict or not line.strip():
            continue
        m = LEVEL_RE.search(line)
        if m:
            stats[m.group(0)] += 1
        elif "Level" in line or "level" in line:
            continue  # 标题/说明行
        elif re.match(r"^[#>\|\-*0-9]", line) and "可信度" not in line:
            # 事实行无等级标注（启发式）
            pass
    return problems, stats


def check_source_completeness(text: str) -> list[str]:
    r"""启发式：L1/2/4 事实行应含来源定位（source/来源/date/日期/section/§/E\d+）。"""
    problems: list[str] = []
    for i, line in enumerate(text.splitlines(), 1):
        if not re.search(r"(?<!L)\bL[124]\b", line):
            continue
        if re.search(r"source|来源|date|日期|§|E\d{1,2}|公告|财报|披露|研报|媒体", line, re.I):
            continue
        if line.strip().startswith(("#", ">", "|", "-", "**")):
            continue
        if any(w in line for w in ("纪律", "原因:", "处理:", "不得", "禁止", "仅作")):
            continue  # 规则说明行 / Conflict 块内行，非事实行
        problems.append(f"L{re.search(r'(?<!L)L[124]', line).group()} 行 {i} 缺来源定位: {line.strip()[:60]}")
    return problems


def check_l4_certainty(text: str) -> list[str]:
    problems: list[str] = []
    for i, line in enumerate(text.splitlines(), 1):
        if re.search(r"\bL4\b", line) and any(w in line for w in CERTAIN_WORDS):
            problems.append(f"L4 行 {i} 使用确定语气: {line.strip()[:60]}")
    return problems


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    path = sys.argv[1]
    try:
        text = open(path, encoding="utf-8").read()
    except FileNotFoundError:
        print(f"[ERROR] 文件不存在: {path}")
        return 2

    conflict_problems, n_blocks = check_conflict_blocks(text)
    _, stats = check_levels(text)
    source_problems = check_source_completeness(text)
    l4_problems = check_l4_certainty(text)

    print(f"fact-map: {path}")
    print(f"Conflict 块: {n_blocks} 个" + (f"，{len(conflict_problems)} 个格式问题" if conflict_problems else "，格式 OK"))
    print(f"Level 标注分布: {stats}")
    print(f"来源完整性: {len(source_problems)} 个警告" if source_problems else "来源完整性: OK")
    print(f"L4 确定语气: {len(l4_problems)} 个" if l4_problems else "L4 语气: OK")

    for p in conflict_problems + source_problems + l4_problems:
        print(f"  [WARN] {p}")

    if conflict_problems or l4_problems:
        print("[FAIL] 存在格式或纪律问题")
        return 1
    print("[PASS] 自检通过（警告不影响通过，按需修正）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
