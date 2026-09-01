#!/usr/bin/env python3
"""build-composition.py — 从 deck 截图 + segments 生成 HyperFrames composition

Audio-First：每页 scene 时长 = 该页音频时长（segments.json），根 data-duration =
总音频时长；旁白音频（narration-full.mp3）data-start=0 data-duration=total 由
框架混音；页级字幕由 notes 派生（scene 底部文本，与 narration.srt 一致）。

用法：
    python3 build-composition.py --video-dir <outputs/experiments/video/index> \
        --frames-dir <paged-deck/html-ppt> --outdir <composition 输出目录>

产物：{outdir}/index.html（HyperFrames composition，可直接 npx hyperframes render）
"""
import argparse
import json
from pathlib import Path

GSAP_CDN = "https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"


def main() -> int:
    ap = argparse.ArgumentParser(description="生成 HyperFrames composition")
    ap.add_argument("--video-dir", type=Path, required=True, help="含 segments.json/narration-full.mp3")
    ap.add_argument("--frames-dir", type=Path, required=True, help="deck 截图目录（index-pNN-WxH.png）")
    ap.add_argument("--outdir", type=Path, required=True)
    ap.add_argument("--width", type=int, default=1440)
    ap.add_argument("--height", type=int, default=810)
    args = ap.parse_args()

    segs = json.load(open(args.video_dir / "segments.json"))["segments"]
    total = float(json.load(open(args.video_dir / "segments.json"))["total_seconds"])
    notes = json.load(open(args.video_dir / "segments.json"))  # 重新读 notes? 从 srt 派生
    # notes 从 narration.srt 提取（页级文本）
    srt = (args.video_dir / "narration.srt").read_text(encoding="utf-8")
    notes_by_page = {}
    for block in srt.strip().split("\n\n"):
        lines = block.split("\n")
        if len(lines) >= 3:
            notes_by_page[int(lines[0])] = lines[2]

    args.outdir.mkdir(parents=True, exist_ok=True)
    # 截图复制（composition 内引用）
    frames = []
    for s in segs:
        src = args.frames_dir / f"index-p{s['page']:02d}-{args.width}x{args.height}.png"
        dst = args.outdir / f"frame-{s['page']:02d}.png"
        if src.is_file():
            dst.write_bytes(src.read_bytes())
            frames.append(dst.name)
        else:
            print(f"警告: 缺截图 {src.name}", file=__import__("sys").stderr)
            return 2

    # 音频复制
    audio_src = args.video_dir / "narration-full.mp3"
    audio_dst = args.outdir / "narration-full.mp3"
    if audio_src.is_file():
        audio_dst.write_bytes(audio_src.read_bytes())

    clips = []
    for s in segs:
        p = s["page"]
        start = s["start"]
        dur = s["duration"]
        note = notes_by_page.get(p, "")
        clips.append(f"""    <section class="clip scene" data-start="{start:.3f}" data-duration="{dur:.3f}" data-track-index="{p}">
      <div class="bg" style="background-image:url(frame-{p:02d}.png)"></div>
      <div class="cap">{note}</div>
    </section>""")

    html = f"""<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width={args.width}, height={args.height}">
<title>贵州茅台 · 企业研究（视频版）</title>
<script src="{GSAP_CDN}"></script>
<style>
  body {{ margin: 0; background: #000; }}
  #root {{
    position: relative; width: {args.width}px; height: {args.height}px;
    overflow: hidden; background: #1d1713;
  }}
  .scene {{ position: absolute; inset: 0; }}
  .bg {{ position: absolute; inset: 0; background-size: cover; background-position: center; }}
  .cap {{
    position: absolute; left: 0; right: 0; bottom: 0;
    padding: 22px 56px 26px; background: linear-gradient(transparent, rgba(0,0,0,.82) 40%);
    color: #fff; font-family: "PingFang SC", "Microsoft YaHei", sans-serif;
    font-size: 24px; line-height: 1.5; letter-spacing: .01em;
  }}
</style>
</head>
<body>
  <div id="root" data-composition-id="maotai-report" data-start="0"
       data-width="{args.width}" data-height="{args.height}"
       data-duration="{total + 1:.3f}">
    <audio id="vo" src="narration-full.mp3" data-start="0"
           data-duration="{total:.3f}" data-track-index="99" data-volume="1"></audio>
{chr(10).join(clips)}
  </div>
  <script>
    window.__timelines = window.__timelines || {{}};
    const tl = gsap.timeline({{ paused: true }});
    window.__timelines["maotai-report"] = tl;
  </script>
</body>
</html>
"""
    (args.outdir / "index.html").write_text(html, encoding="utf-8")
    print(f"composition -> {args.outdir}/index.html（{len(clips)} scene · {total + 1:.1f}s · {len(frames)} 帧 · 音频 {audio_dst.name}）")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
