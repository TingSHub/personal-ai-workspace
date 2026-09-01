#!/usr/bin/env python3
"""apply-timing.py — 用 segments.json 更新 composition 时序(index.html)

用法:
    python3 scripts/apply-timing.py --html <index.html> --segments <segments.json>

Scene 内动画时间按比例缩放(新 Scene 时长 / 旧 Scene 时长),保持动画节奏跟随旁白。
"""
import argparse
import json
import re
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--html", type=Path, required=True)
    ap.add_argument("--segments", type=Path, required=True)
    args = ap.parse_args()

    segs = json.loads(args.segments.read_text(encoding="utf-8"))["segments"]
    total = float(json.loads(args.segments.read_text(encoding="utf-8"))["total_seconds"])
    scenes = [(s["scene"], s["start"], s["end"], s["duration"]) for s in segs]
    NEW = [(s[1], s[2]) for s in scenes]

    # 旧时序:从 index.html 读取当前 scene data-start(顺序)
    src = args.html.read_text(encoding="utf-8")
    old_starts = re.findall(r'<section id="s\d+" class="scene clip" data-start="([\d.]+)" data-duration="([\d.]+)"', src)
    if len(old_starts) != len(NEW):
        print(f"Scene 数不匹配: html={len(old_starts)} segments={len(NEW)}", file=sys.stderr)
        return 2
    OLD = [(float(s), float(s) + float(d)) for s, d in old_starts]

    def map_t(t):
        for i, (os_, oe) in enumerate(OLD):
            if os_ <= t <= oe or i == len(OLD) - 1:
                ns, ne = NEW[i]
                if oe == os_:
                    return ns
                return round(ns + (t - os_) * (ne - ns) / (oe - os_), 2)
        return t

    # 根 duration
    src = re.sub(r'(data-duration=")[\d.]+(")', rf'\g<1>{total}\g<2>', src, count=1)

    # Scene/audio/captions 时序
    for i in range(1, len(NEW) + 1):
        ns, ne = NEW[i - 1]
        src = re.sub(r'(<section id="s%d"[^>]*data-start=")[\d.]+(")' % i, rf'\g<1>{ns}\g<2>', src)
        src = re.sub(r'(<section id="s%d"[^>]*data-duration=")[\d.]+(")' % i, rf'\g<1>{round(ne-ns, 2)}\g<2>', src)
        src = re.sub(r'(<audio id="a%d"[^>]*data-start=")[\d.]+(")' % i, rf'\g<1>{ns}\g<2>', src)
        src = re.sub(r'(<audio id="a%d"[^>]*data-duration=")[\d.]+(")' % i, rf'\g<1>{round(ne-ns, 2)}\g<2>', src)
        src = re.sub(r'(<div id="caps-s%d"[^>]*data-start=")[\d.]+(")' % i, rf'\g<1>{ns}\g<2>', src)
        src = re.sub(r'(<div id="caps-s%d"[^>]*data-duration=")[\d.]+(")' % i, rf'\g<1>{round(ne-ns, 2)}\g<2>', src)

    # GSAP 时间点
    def tl_time(m):
        return f', {map_t(float(m.group(1)))})'

    src = re.sub(r', ([\d.]+)\)', tl_time, src)
    src = re.sub(r'(tl\.to\("#progress-fill", \{[^}]*duration:)[\d.]+', rf'\g<1>{total}', src)
    args.html.write_text(src, encoding="utf-8")
    print(f"时序已更新: {len(NEW)} Scene, 总时长 {total}s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
