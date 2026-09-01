#!/usr/bin/env python3
"""check-em-dash.py - 检查静态 HTML 可见文本中的 em-dash / en-dash（taste-skill 零破折号规则）

用法:
    python3 check-em-dash.py <html文件...>

行为:
    - 剥离 <style>/<script> 与标签后检查可见文本
    - 命中任一 em-dash（—）或 en-dash（–，用作分隔符）即报出文件名与上下文片段
    - 中文规范连字符（-）、减号（-）与数字范围（0.5-1）不在检查范围

退出码:
    0 = PASS（无命中）
    1 = 有命中（需人工重写）
    2 = 用法错误（缺参数/文件不存在）
"""
import re
import sys


def visible_text(path: str) -> list[str]:
    """返回文件中可见文本的行列表（剥离 style/script/标签）。"""
    try:
        with open(path, encoding="utf-8") as f:
            html = f.read()
    except OSError as e:
        print(f"error: 无法读取 {path}: {e}", file=sys.stderr)
        sys.exit(2)
    # 剥离 style/script 块（其内容不属于可见文本）
    html = re.sub(r"<style[^>]*>.*?</style>", "", html, flags=re.S | re.I)
    html = re.sub(r"<script[^>]*>.*?</script>", "", html, flags=re.S | re.I)
    # 剥离注释
    html = re.sub(r"<!--.*?-->", "", html, flags=re.S)
    # 剥离标签，保留文本
    text = re.sub(r"<[^>]+>", "", html)
    return [ln for ln in text.splitlines() if ln.strip()]


def main(argv: list[str]) -> int:
    if not argv:
        print(__doc__)
        return 2
    bad_dash = re.compile(r"[—–]")
    found = 0
    for path in argv:
        for lineno, line in enumerate(visible_text(path), 1):
            for m in bad_dash.finditer(line):
                start = max(0, m.start() - 18)
                ctx = line[start : m.start() + 18]
                print(f"{path}:{lineno}: 命中 {m.group()!r} -> ...{ctx}...")
                found += 1
    if found:
        print(f"FAIL: {found} 处 em/en-dash（重写为句号/逗号/括号或连字符 -）")
        return 1
    print("PASS: 无 em-dash / en-dash（taste-skill 零破折号规则）")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
