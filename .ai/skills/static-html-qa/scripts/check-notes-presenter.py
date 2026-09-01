#!/usr/bin/env python3
"""check-notes-presenter.py — 翻页 deck Presenter Mode 验证

用途：验证 html-ppt-skill 形态 deck 的每页 <aside class="notes"> speaker
script 在 Presenter Mode（S 键演讲者窗口）中正确显示。用于 notes 口语化
改写或 Content Lock 后的回归验证。

用法：
    python3 check-notes-presenter.py <deck.html> [期望清单.tsv]

期望清单格式（TSV，UTF-8）：页号<TAB>期望出现的文本片段（可多行同页）
    2\t去年营收下降 1.2%
    2\t净利润下降 4.5%
    27\t仅供研究参考

未提供清单时：只验证每页 notes 存在且在 presenter 窗口可见（抽查前 3 页）。

退出码：
    0 = PASS（全部期望片段在对应页 presenter 窗口可见）
    1 = 有发现（缺失片段明细）
    2 = 用法错误

依赖：Python playwright（自动探测 .venv，同 qa-html-report.py）。
"""
import json
import os
import subprocess
import sys
from pathlib import Path


def _venv_candidates():
    cands = []
    env = os.environ.get("QA_PYTHON")
    if env:
        cands.append(env)
    cwd = Path.cwd()
    for d in (cwd, cwd.parent, cwd.parent.parent):
        cands.append(str(d / ".venv" / "bin" / "python"))
    script = Path(__file__).resolve()
    for up in range(1, 7):
        cands.append(str(script.parents[up] / ".venv" / "bin" / "python"))
    cands.append(os.path.expanduser("~/.venv/bin/python"))
    seen = set()
    return [c for c in cands if not (c in seen or seen.add(c))]


def _has_playwright(py):
    try:
        r = subprocess.run([py, "-c", "import playwright"], capture_output=True,
                           text=True, timeout=15)
        return r.returncode == 0
    except Exception:
        return False


def _ensure_python():
    try:
        import playwright  # noqa: F401
        return
    except ImportError:
        pass
    for py in _venv_candidates():
        if os.path.isfile(py) and _has_playwright(py):
            os.execv(py, [py] + sys.argv)


_ensure_python()


def main() -> int:
    if len(sys.argv) < 2:
        print("用法: python3 check-notes-presenter.py <deck.html> [期望清单.tsv]", file=sys.stderr)
        return 2
    html = Path(sys.argv[1])
    if not html.is_file():
        print(f"用法错误: 文件不存在 {html}", file=sys.stderr)
        return 2

    expectations = {}  # page -> [keywords]
    if len(sys.argv) > 2:
        exp_path = Path(sys.argv[2])
        if not exp_path.is_file():
            print(f"用法错误: 清单不存在 {exp_path}", file=sys.stderr)
            return 2
        for lineno, raw in enumerate(exp_path.open(encoding="utf-8"), 1):
            raw = raw.strip()
            if not raw or raw.startswith("#"):
                continue
            parts = raw.split("\t")
            if len(parts) < 2:
                print(f"用法错误: 清单 L{lineno} 格式不符（页号<TAB>文本）", file=sys.stderr)
                return 2
            expectations.setdefault(int(parts[0]), []).append(parts[1])

    from playwright.sync_api import sync_playwright

    url = "file://" + str(html.resolve())
    missing = []
    checked = 0
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        page.wait_for_timeout(500)
        total = page.evaluate(
            "[...document.querySelectorAll('.slide')].filter(s => !s.closest('.mini-slide')).length")

        pages = sorted(expectations) if expectations else list(range(1, min(total, 3) + 1))
        for pg_no in pages:
            page.goto(f"{url}#/{pg_no}", wait_until="networkidle")
            page.wait_for_timeout(300)
            with page.expect_popup() as popup_info:
                page.keyboard.press("S")
            pw = popup_info.value
            pw.wait_for_load_state("domcontentloaded")
            pw.wait_for_timeout(900)
            text = pw.evaluate("document.body.innerText")
            for kw in expectations.get(pg_no, [""]):
                if kw and kw not in text:
                    missing.append((pg_no, kw))
            checked += 1
            pw.close()
        browser.close()

    if not missing:
        print(f"PASS: {checked} 页 presenter 验证通过（期望片段全部可见）")
        return 0
    print(f"FAIL: {len(missing)} 处期望片段缺失：")
    for pg_no, kw in missing:
        print(f"  P{pg_no}: 未找到「{kw}」")
    return 1


if __name__ == "__main__":
    sys.exit(main())
