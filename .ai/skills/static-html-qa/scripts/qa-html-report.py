#!/usr/bin/env python3
"""qa-html-report.py — 静态 HTML 报告前端质检（Playwright 驱动，零安装）

用途：对单文件长文 HTML（企业研究报告/长文页面）做前端质检，覆盖：
  1. 多分辨率截图：桌面(1440) / 移动(390) / 目标视频分辨率(1920x1080)，可自定义
  2. DOM overflow：容器内容超出（scrollWidth > clientWidth）
  3. 卡片内容溢出：同上逐元素 + 文本超出视口宽度（页面截断）
  4. SVG 文字重叠：同 SVG 内 text 元素包围盒相交检测
  5. 图例重叠：.legend / [class*=legend] 元素包围盒相交检测
  6. 字体加载失败：document.fonts.ready 后 status=error 的字体
  7. console error / pageerror
  8. responsive breakpoint 异常：每个视口独立跑全量检查并汇总
  9. 图表文字过小：SVG text 计算字号 < 阈值（默认 9px）
 10. SVG 文字超出画布（被裁剪/出界）

用法：
    python3 qa-html-report.py <report.html> [--viewports 1440x900,390x844,1920x1080]
        [--outdir <dir>] [--min-font 9] [--no-screenshot]

退出码：
    0 = PASS（全部检查无发现）
    1 = 有发现（打印分项汇总与明细，人工裁决；截图仍会生成）
    2 = 用法错误（参数缺失/文件不存在/playwright 不可用）

说明：
    - playwright 库解析顺序：$PLAYWRIGHT_LIB → 已安装的 playwright → npm 全局
      @playwright/cli 内置（Linux ~/.nvm/versions/node/*/lib/node_modules/...）
    - 截图命名：{stem}-{width}x{height}.png（fullPage）；与 check-content-boundary.py、
      check-numbers.py 组成 HTML 质检三件套，建议在 Phase 3/4 全部执行。
"""
import argparse
import json
import os
import subprocess
import sys
import glob
from pathlib import Path


def _venv_candidates() -> list:
    """探测可能装有 playwright 的 venv python（含 $QA_PYTHON 显式指定）。"""
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


def _has_playwright(py: str) -> bool:
    try:
        r = subprocess.run([py, "-c", "import playwright"], capture_output=True,
                           text=True, timeout=15)
        return r.returncode == 0
    except Exception:
        return False


def _ensure_python() -> None:
    """当前解释器无 playwright 时，用探测到的 venv python 重启自身。"""
    try:
        import playwright  # noqa: F401
        return
    except ImportError:
        pass
    for py in _venv_candidates():
        if os.path.isfile(py) and _has_playwright(py):
            os.execv(py, [py] + sys.argv)


def find_playwright() -> str:
    """返回可 import 的 playwright 包路径（目录），找不到返回 None。"""
    import playwright  # noqa: F401  # 此时必有（_ensure_python 已保证）
    return None


# ---- 浏览器内检查脚本（返回 JSON 可序列化结果） ----

JS_OVERFLOW = """
() => {
  const results = [];
  const all = document.querySelectorAll('*');
  for (const el of all) {
    // SVG 元素的 scrollWidth/scrollHeight 无 overflow 语义，由专门 SVG 检查覆盖
    if (el instanceof SVGElement) continue;
    const r = el.getBoundingClientRect();
    if (r.width === 0 || r.height === 0) continue;
    if (el.scrollWidth > r.width + 2 || el.scrollHeight > r.height + 2) {
      results.push({tag: el.tagName.toLowerCase(),
                    cls: String(el.className || '').slice(0, 50),
                    id: el.id || '',
                    sw: el.scrollWidth, cw: Math.round(r.width),
                    sh: el.scrollHeight, ch: Math.round(r.height)});
    }
  }
  return results.slice(0, 40);
}
"""

JS_SVG_TEXT = """
(minSize) => {
  const out = {overlaps: [], outside: [], tiny: []};
  const scope = document.querySelector('.slide.is-active, .slide.active') || document;
  const svgs = [...scope.querySelectorAll('svg')]
    .filter(s => parseFloat(getComputedStyle(s).opacity) > 0);
  svgs.forEach((svg, si) => {
    const srect = svg.getBoundingClientRect();
    if (srect.width === 0) return;
    const texts = [...svg.querySelectorAll('text')];
    for (const t of texts) {
      const fs = parseFloat(getComputedStyle(t).fontSize);
      const txt = (t.textContent || '').trim().slice(0, 24);
      if (fs > 0 && fs < minSize) out.tiny.push({svg: si, fs: fs, text: txt});
      const r = t.getBoundingClientRect();
      if (r.width > 0 && (r.left < srect.left - 4 || r.right > srect.right + 4 ||
                          r.top < srect.top - 4 || r.bottom > srect.bottom + 4)) {
        out.outside.push({svg: si, text: txt,
                          l: Math.round(r.left - srect.left), r: Math.round(r.right - srect.right),
                          t: Math.round(r.top - srect.top), b: Math.round(r.bottom - srect.bottom)});
      }
    }
    for (let i = 0; i < texts.length; i++) for (let j = i + 1; j < texts.length; j++) {
      const a = texts[i].getBoundingClientRect(), b = texts[j].getBoundingClientRect();
      if (a.width === 0 || b.width === 0) continue;
      const ix = Math.min(a.right, b.right) - Math.max(a.left, b.left);
      const iy = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
      if (ix > 1.5 && iy > 1.5) {
        out.overlaps.push({svg: si, a: (texts[i].textContent || '').trim().slice(0, 20),
                           b: (texts[j].textContent || '').trim().slice(0, 20),
                           ix: Math.round(ix), iy: Math.round(iy)});
      }
    }
  });
  out.overlaps = out.overlaps.slice(0, 30);
  out.outside = out.outside.slice(0, 30);
  out.tiny = out.tiny.slice(0, 30);
  return out;
}
"""

JS_LEGEND = """
() => {
  const scope = document.querySelector('.slide.is-active, .slide.active') || document;
  const els = [...scope.querySelectorAll('.legend span, [class*="legend"] span')]
    .filter(el => parseFloat(getComputedStyle(el).opacity) > 0);
  const hits = [];
  for (let i = 0; i < els.length; i++) for (let j = i + 1; j < els.length; j++) {
    const a = els[i].getBoundingClientRect(), b = els[j].getBoundingClientRect();
    if (a.width === 0 || b.width === 0) continue;
    const ix = Math.min(a.right, b.right) - Math.max(a.left, b.left);
    const iy = Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top);
    if (ix > 2 && iy > 2) {
      hits.push({a: (els[i].textContent || '').trim().slice(0, 20),
                 b: (els[j].textContent || '').trim().slice(0, 20),
                 ix: Math.round(ix), iy: Math.round(iy)});
    }
  }
  return hits.slice(0, 30);
}
"""

JS_FONTS = """
async () => {
  await document.fonts.ready;
  const bad = [];
  document.fonts.forEach(f => { if (f.status === 'error') bad.push(f.family); });
  const w = document.documentElement.scrollWidth;
  const cw = document.documentElement.clientWidth;
  return {bad: bad.slice(0, 10), total: document.fonts.size,
          pageOverflowX: w - cw, pageHeight: document.documentElement.scrollHeight};
}
"""

JS_CSS_VARS = """
() => {
  // 未定义 CSS 变量检查：页面样式引用了 var(--x) 但 :root 未定义 → 渲染为无效值（透明/继承）
  const defined = new Set();
  const used = new Set();
  const re = /var\((--[\w-]+)/g;
  for (const sheet of document.styleSheets) {
    let rules;
    try { rules = sheet.cssRules; } catch (e) { continue; }
    for (const rule of rules) {
      let css = '';
      try { css = rule.cssText || ''; } catch (e) { continue; }
      // CSS 变量可定义在任何选择器作用域（:root 或局部作用域）；
      // CSSStyleDeclaration 迭代器不包含自定义属性，用正则扫 cssText
      const reDef = /(--[\w-]+)\s*:/g;
      let dm;
      while ((dm = reDef.exec(css))) defined.add(dm[1]);
      let m;
      while ((m = re.exec(css))) used.add(m[1]);
    }
  }
  // 内联 style 里的 var() 也统计
  for (const el of document.querySelectorAll('[style]')) {
    let m;
    const s = el.getAttribute('style') || '';
    while ((m = re.exec(s))) used.add(m[1]);
  }
  return [...used].filter(v => !defined.has(v));
}
"""

JS_MODE_DETECT = """
() => {
  const hasActive = !!document.querySelector('.slide.is-active, .slide.active');
  const scrollable = document.documentElement.scrollHeight > window.innerHeight + 50;
  return hasActive && !scrollable ? 'paged' : 'longform';
}
"""

JS_PAGED_OVERFLOW = """
() => {
  const act = document.querySelector('.slide.is-active, .slide.active');
  if (!act) return [{err: 'no active slide'}];
  const r = act.getBoundingClientRect();
  const hits = [];
  for (const el of act.querySelectorAll('*')) {
    if (el instanceof SVGElement) continue;
    const er = el.getBoundingClientRect();
    if (er.width > 0 && er.height > 0 &&
        (er.right > r.right + 1 || er.bottom > r.bottom + 1 ||
         er.left < r.left - 1 || er.top < r.top - 1)) {
      hits.push({tag: el.tagName.toLowerCase(),
                 cls: String(el.className || '').slice(0, 40),
                 r: Math.round(er.right - r.right),
                 b: Math.round(er.bottom - r.bottom)});
    }
  }
  return hits.slice(0, 8);
}
"""

JS_CHART_LEGEND = """
() => {
  // 多序列折线图必须有图例（.legend）或线端数值标注——否则读者无法分辨哪条线是什么
  const issues = [];
  const svgs = document.querySelectorAll('svg');
  svgs.forEach((svg, si) => {
    const lines = [...svg.querySelectorAll('polyline, path')].filter(el => {
      const r = el.getBoundingClientRect();
      return el.getAttribute('stroke') !== 'none' && r.width > 20;
    });
    if (lines.length < 2) return;
    let hasLegend = false;
    let p = svg.parentElement;
    for (let i = 0; i < 3 && p; i++) {
      if (p.querySelector && p.querySelector('.legend')) { hasLegend = true; break; }
      p = p.parentElement;
    }
    let allLabeled = true;
    for (const ln of lines) {
      let endX = null, endY = null;
      if (ln.tagName === 'polyline') {
        const pts = (ln.getAttribute('points') || '').trim().split(/[\\s,]+/).map(Number);
        if (pts.length >= 2) { endX = pts[pts.length - 2]; endY = pts[pts.length - 1]; }
      } else {
        const nums = (ln.getAttribute('d') || '').match(/-?\\d+(\\.\\d+)?/g)?.map(Number) || [];
        if (nums.length >= 2) { endX = nums[nums.length - 2]; endY = nums[nums.length - 1]; }
      }
      if (endX == null) continue;
      const near = [...svg.querySelectorAll('text')].some(t => {
        const x = parseFloat(t.getAttribute('x')), y = parseFloat(t.getAttribute('y'));
        return x != null && y != null && Math.abs(x - endX) < 40 && Math.abs(y - endY) < 30;
      });
      if (!near) allLabeled = false;
    }
    if (!hasLegend && !allLabeled) {
      issues.push({svg: si, lines: lines.length, hasLegend, allLabeled});
    }
  });
  return issues.slice(0, 10);
}
"""

JS_PAGED_INDEX = """
() => {
  // 排除 overview 克隆（.mini-slide 容器内），只统计真实 slide
  const slides = [...document.querySelectorAll('.slide')]
    .filter(s => !s.closest('.mini-slide'));
  const act = document.querySelector('.slide.is-active, .slide.active');
  return act ? slides.indexOf(act) : -1;
}
"""

JS_PAGED_TOGGLE = """
(i) => {
  const slides = [...document.querySelectorAll('.slide')];
  slides.forEach((s, k) => {
    s.classList.toggle('is-active', k === i);
    s.classList.toggle('active', k === i);
  });
}
"""


def _goto_slide(page, url, i):
    """翻页到第 i 页：hash 深度链接 → ArrowRight → JS toggle 三级 fallback。"""
    for _ in range(2):
        page.goto(f"{url}#/{i + 1}", wait_until="networkidle")
        page.wait_for_timeout(200)
        if page.evaluate(JS_PAGED_INDEX) == i:
            return
    page.keyboard.press("ArrowRight")
    page.wait_for_timeout(200)
    if page.evaluate(JS_PAGED_INDEX) == i:
        return
    page.evaluate(JS_PAGED_TOGGLE, i)
    page.wait_for_timeout(120)


_ensure_python()


def main() -> int:
    ap = argparse.ArgumentParser(description="静态 HTML 报告前端质检（Playwright）")
    ap.add_argument("html", help="待质检的 HTML 文件路径")
    ap.add_argument("--viewports", default="1440x900,390x844,1920x1080",
                    help="视口列表，逗号分隔 WxH（默认 桌面/移动/视频分辨率）")
    ap.add_argument("--outdir", default=None, help="截图与报告输出目录（默认与 HTML 同目录）")
    ap.add_argument("--min-font", type=float, default=9.0, help="SVG 文字最小字号阈值（默认 9）")
    ap.add_argument("--skip-css-vars", action="store_true",
                    help="跳过未定义 CSS 变量检查（运行时动态注入样式的应用，如 dashi-ppt）")
    ap.add_argument("--no-screenshot", action="store_true", help="跳过截图只做检查")
    ap.add_argument("--mode", choices=["auto", "longform", "paged"], default="auto",
                    help="形态：auto 自动检测（翻页 deck 或长滚动页），longform 强制长文，paged 强制翻页")
    args = ap.parse_args()

    path = Path(args.html)
    if not path.is_file():
        print(f"用法错误: 文件不存在 {path}", file=sys.stderr)
        return 2
    outdir = Path(args.outdir) if args.outdir else path.parent
    outdir.mkdir(parents=True, exist_ok=True)

    lib = find_playwright()
    if lib:
        # 加入 playwright 的父目录（node_modules），使 playwright 与 playwright-core 同时可解析
        sys.path.insert(0, os.path.dirname(lib))
        sys.path.insert(0, lib)
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("用法错误: 找不到 Python playwright 库。可设 $QA_PYTHON 指向装有 "
              "playwright 的 venv python（如 workspace/.venv/bin/python），"
              "或 pip install playwright", file=sys.stderr)
        return 2

    viewports = []
    for vp in args.viewports.split(","):
        try:
            w, h = (int(x) for x in vp.strip().lower().split("x"))
            viewports.append((w, h))
        except ValueError:
            print(f"用法错误: 视口格式应为 WxH: {vp}", file=sys.stderr)
            return 2

    url = "file://" + str(path.resolve())
    findings = {}          # check -> list
    screenshots = []

    with sync_playwright() as p:
        browser = p.chromium.launch()
        for wi, (w, h) in enumerate(viewports):
            page = browser.new_page(viewport={"width": w, "height": h})
            console_errs, page_errs = [], []
            page.on("console", lambda m: console_errs.append(m.text)
                    if m.type in ("error", "warning") else None)
            page.on("pageerror", lambda e: page_errs.append(str(e)))
            page.goto(url, wait_until="networkidle")
            page.wait_for_timeout(400)
            label = f"{w}x{h}"

            mode = args.mode
            if mode == "auto":
                mode = page.evaluate(JS_MODE_DETECT)

            if mode == "paged":
                total = page.evaluate(
                    "[...document.querySelectorAll('.slide')].filter(s => !s.closest('.mini-slide')).length")
                for i in range(total):
                    _goto_slide(page, url, i)
                    o = page.evaluate(JS_PAGED_OVERFLOW)
                    if o:
                        findings.setdefault("翻页页溢出", []).append({f"{label}·p{i + 1}": o})
                    if not args.no_screenshot:
                        shot = outdir / f"{path.stem}-p{i + 1:02d}-{w}x{h}.png"
                        page.screenshot(path=str(shot))
                        screenshots.append(shot.name)
            else:
                overflow = page.evaluate(JS_OVERFLOW)
                if overflow:
                    findings.setdefault("DOM/卡片溢出", []).append({label: overflow})
                if not args.no_screenshot:
                    shot = outdir / f"{path.stem}-{w}x{h}.png"
                    page.screenshot(path=str(shot), full_page=True)
                    screenshots.append(shot.name)

            # 共享检查（两种形态都跑）
            if not args.skip_css_vars:
                css_vars = page.evaluate(JS_CSS_VARS)
                if css_vars:
                    findings.setdefault("未定义 CSS 变量", []).append({label: css_vars})
            chart_legend = page.evaluate(JS_CHART_LEGEND)
            if chart_legend:
                findings.setdefault("多序列图表缺图例/线标注", []).append({label: chart_legend})
            svg = page.evaluate(JS_SVG_TEXT, args.min_font)
            for k in ("overlaps", "outside", "tiny"):
                if svg[k]:
                    findings.setdefault(f"SVG 文字{k}", []).append({label: svg[k]})
            legend = page.evaluate(JS_LEGEND)
            if legend:
                findings.setdefault("图例重叠", []).append({label: legend})
            fonts = page.evaluate(JS_FONTS)
            if fonts["bad"]:
                findings.setdefault("字体加载失败", []).append({label: fonts["bad"]})
            if fonts["pageOverflowX"] > 2:
                findings.setdefault("页面横向溢出/截断", []).append(
                    {label: f"溢出 {fonts['pageOverflowX']}px"})
            if console_errs:
                findings.setdefault("console error/warning", []).append({label: console_errs[:10]})
            if page_errs:
                findings.setdefault("pageerror", []).append({label: page_errs[:5]})
            page.close()
        browser.close()

    report = {"html": str(path), "viewports": viewports,
              "min_font": args.min_font, "findings": findings,
              "screenshots": screenshots}
    (outdir / "qa-report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")

    if not findings:
        print(f"PASS: {len(viewports)} 个视口全量检查无发现（截图: {', '.join(screenshots) or '跳过'}）")
        return 0

    total = sum(len(v) for v in findings.values())
    print(f"FAIL: {len(findings)} 类 / {total} 处发现（完整明细见 qa-report.json，截图仍已生成）")
    for check, groups in findings.items():
        print(f"\n  [{check}]")
        shown = 0
        for g in groups:
            for vp, items in g.items():
                for item in (items if isinstance(items, list) else [items]):
                    if shown >= 12:
                        print(f"    ...（其余见 qa-report.json）")
                        break
                    if isinstance(item, dict):
                        print(f"    {vp}: {json.dumps(item, ensure_ascii=False)[:150]}")
                    else:
                        print(f"    {vp}: {item}")
                    shown += 1
                if shown >= 12:
                    break
            if shown >= 12:
                break
    return 1


if __name__ == "__main__":
    sys.exit(main())
