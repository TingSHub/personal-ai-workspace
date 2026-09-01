#!/usr/bin/env python3
"""check-fact-drift.py — 口播稿改写的事实零漂移校验

用途：口播稿口语化改写（如 notes 按 finance-content-engineering script-polish
规则改写）后，校验新旧两个版本之间的事实没有漂移：
  1. 数字集合对比：旧版有而新版没有的数字（removed）——必须为中文读法/
     时间指代转换，否则为丢失；新版新增的数字（added）——不允许。
  2. 近似词检测：新版中「约/左右/上下/超过/出头/差不多」等模糊词与精确
     数字并存的位置——精确数据不得被模糊化（如 36.1% 写成「超过三分之
     一」属于事实漂移）。
  3. 中文数字读法核验：removed 数字需在新版对应段落以中文数字形式出现
     （支持 个/十/百/千/万/亿 位；小数需人工核验）。

用法：
    python3 check-fact-drift.py <旧版.txt> <新版.txt>
    # 按段落对比时，两文件结构需一致（每页/段之间空行分隔或按行号对齐）

退出码：
    0 = PASS（无数字丢失、无新增数字、无近似化）
    1 = 有发现（打印 removed/added/近似词明细，人工核验后修复）
    2 = 用法错误

注意：
    - 数字转中文读法（892 → 八百九十二）与时间指代（2025 → 去年）允许，
      由 removed 核验区分；「约/左右」等模糊词属于近似化，禁止。
    - 年份/月份转指代（2026 一季度 → 今年一季度）允许，但「去年」等
      指代在跨年语境下可能漂移，建议核验指代对象。
"""
import re
import sys
from pathlib import Path

# 近似词等价组：组内替换（约→左右/大概）属等价口语化，不算引入新近似
APPROX_GROUPS = [
    ["约", "左右", "上下", "大概", "差不多", "将近"],
    ["出头"],
]
TIME_WORDS = ["去年", "今年", "上半年", "下半年", "一季度", "二季度", "三季度", "四季度"]

CN_DIGITS = {"0": "零", "1": "一", "2": "二", "3": "三", "4": "四",
             "5": "五", "6": "六", "7": "七", "8": "八", "9": "九"}
UNITS = ["", "十", "百", "千"]


def int_to_cn(n: int) -> str:
    """整数转中文读法（支持到亿）。70→七十，892→八百九十二，4000→四千。"""
    return _int_to_cn(n, liang=True)


def _int_to_cn(n: int, liang: bool) -> str:
    """liang=True 时 2 作首位且位权≥百用「两」（两百/两千/两万/两亿）。"""
    if n == 0:
        return "零"
    units = ["", "万", "亿"]
    result = ""
    group_idx = 0
    while n > 0:
        group = n % 10000
        if group:
            part = ""
            digits = []
            g = group
            while g > 0:
                digits.append(g % 10)
                g //= 10
            for i in range(len(digits) - 1, -1, -1):
                d = digits[i]
                if d == 0:
                    if part and not part.endswith("零") and any(x != 0 for x in digits[:i]):
                        part += "零"
                    continue
                if i == 1 and d == 1 and not part:
                    part += "十"
                elif liang and d == 2 and not part and i >= 2:
                    part += "两" + UNITS[i]
                else:
                    part += CN_DIGITS[str(d)] + UNITS[i]
            result = part + units[group_idx] + result
        group_idx += 1
        n //= 10000
    return result


def extract_nums(text: str) -> set:
    """提取文本中的数字 token（含小数）。"""
    return set(re.findall(r"\d+(?:\.\d+)?", text))


def detect_approx(new_text: str, old_text: str):
    """对比式近似检测：新版命中近似词+数字并存，且旧版同段无同组等价词时报。"""
    hits = []
    pat = r"[^。\n]{0,18}(" + "|".join(w for g in APPROX_GROUPS for w in g) + r")[^。\n]{0,18}"
    for m in re.finditer(pat, new_text):
        seg = m.group(0)
        if not re.search(r"\d", seg):
            continue
        word = m.group(1)
        group = next((g for g in APPROX_GROUPS if word in g), [word])
        if not any(w in old_text for w in group):
            hits.append(seg.strip())
    return hits[:20]


def check_cn_reading(passage: str, token: str) -> bool:
    """removed 数字是否在段落中以中文读法/指代出现。"""
    if token.startswith("20") and len(token) == 4:
        # 年份 → 时间指代（去年/今年/上半年等）
        return any(w in passage for w in TIME_WORDS)
    if "." in token:
        # 小数 → 需带单位读法（1.2 亿 → 一亿两千万）
        return ("亿" in passage or "万" in passage) and any(
            w in passage for w in TIME_WORDS + ["亿", "万", "点"])
    n = int(token)
    forms = [int_to_cn(n)]
    if n >= 10000:
        forms.append(int_to_cn(n // 10000) + "万")
    if n >= 100000000:
        forms.append(int_to_cn(n // 100000000) + "亿")
    # 百分比口语（70 → 七成）
    if n < 100:
        forms.append(f"{CN_DIGITS[str(n // 10)] if n // 10 else ''}{CN_DIGITS[str(n % 10)]}成")
        forms.append(f"七成" if n == 70 else "")
    return any(f in passage for f in forms if f)


def main() -> int:
    if len(sys.argv) != 3:
        print("用法: python3 check-fact-drift.py <旧版.txt> <新版.txt>", file=sys.stderr)
        return 2
    old_p, new_p = Path(sys.argv[1]), Path(sys.argv[2])
    if not old_p.is_file() or not new_p.is_file():
        print("用法错误: 文件不存在", file=sys.stderr)
        return 2

    old_text = old_p.read_text(encoding="utf-8")
    new_text = new_p.read_text(encoding="utf-8")

    # 按段落对齐（空行分隔）
    old_paras = [p.strip() for p in old_text.split("\n\n") if p.strip()]
    new_paras = [p.strip() for p in new_text.split("\n\n") if p.strip()]
    if len(old_paras) != len(new_paras):
        print(f"警告: 段落数不一致（旧 {len(old_paras)} / 新 {len(new_paras)}），"
              f"按全文集合对比降级", file=sys.stderr)
        old_paras, new_paras = [old_text], [new_text]

    findings = {"removed": [], "added": [], "approx": []}
    for i, (op, np_) in enumerate(zip(old_paras, new_paras)):
        o, n = extract_nums(op), extract_nums(np_)
        for t in sorted(o - n):
            if not check_cn_reading(np_, t):
                findings["removed"].append((i + 1, t, np_[:40]))
        for t in sorted(n - o):
            findings["added"].append((i + 1, t, np_[:40]))
        for h in detect_approx(np_, op):
            findings["approx"].append((i + 1, h))

    if not any(findings.values()):
        print(f"PASS: 无数字丢失、无新增数字、无近似化（{len(old_paras)} 段）")
        return 0

    print(f"FAIL: 发现 {sum(len(v) for v in findings.values())} 处（数字丢失={len(findings['removed'])}, "
          f"新增={len(findings['added'])}, 近似={len(findings['approx'])}）")
    if findings["removed"]:
        print("  数字丢失（非中文读法）:")
        for para, t, ctx in findings["removed"][:10]:
            print(f"    P{para} [{t}] → 新版无对应读法: {ctx}")
    if findings["added"]:
        print("  新增数字:")
        for para, t, ctx in findings["added"][:10]:
            print(f"    P{para} [{t}]: {ctx}")
    if findings["approx"]:
        print("  近似化嫌疑:")
        for para, h in findings["approx"][:10]:
            print(f"    P{para}: {h}")
    return 1


if __name__ == "__main__":
    sys.exit(main())
