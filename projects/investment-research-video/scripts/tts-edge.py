#!/usr/bin/env python3
"""tts-edge.py — Edge TTS 全量合成（微软 Edge 朗读同款神经语音，非官方接口）

输入：deck HTML（提取 aside.notes）或 notes 文本（P1: 每页一段）
流程：逐页 edge-tts 合成（zh-CN-XiaoxiaoNeural, rate=+8%）
      → seg-NN.mp3 → ffprobe 时长 → 拼接 narration-full.mp3
      → 按累计时长派生 narration.srt（页级字幕，notes 为唯一 SoT）
输出：{outdir}/{deck-name}/（segments/ + narration-full.mp3 + narration.srt + segments.json）

用法：
    python3 tts-edge.py --html <deck.html> [--outdir <dir>]
    python3 tts-edge.py --notes <notes.txt> [--outdir <dir>]

环境：edge-tts 装在 MoneyPrinterTurbo/.venv（7.2.7）——脚本自动探测；可 $EDGE_TTS_PYTHON 指定
商用红线：非官方逆向接口，微软无书面授权，正式发布迁移 Azure（同源音色 XiaoxiaoNeural）
"""
import argparse
import asyncio
import json
import re
import subprocess
import sys
from pathlib import Path

VOICE = "zh-CN-XiaoxiaoNeural"
RATE = "+8%"


def find_edge_env():
    env = __import__("os").environ.get("EDGE_TTS_PYTHON")
    if env:
        return env
    cands = [
        Path.home() / "MoneyPrinterTurbo/.venv/bin/python",
        Path.home() / "personal-ai-workspace/.venv/bin/python",
    ]
    for py in cands:
        if py.is_file():
            try:
                r = subprocess.run([str(py), "-c", "import edge_tts"], capture_output=True, timeout=10)
                if r.returncode == 0:
                    return str(py)
            except Exception:
                pass
    return None


def extract_notes_from_html(html_path: Path):
    src = html_path.read_text(encoding="utf-8")
    notes = re.findall(
        r'<aside\b[^>]*class="[^"]*\bnotes\b[^"]*"[^>]*>(.*?)</aside>',
        src,
        re.S,
    )
    return [re.sub(r"\s+", " ", n).strip() for n in notes]


def extract_notes_from_txt(txt_path: Path):
    paras = [p.strip() for p in txt_path.read_text(encoding="utf-8").split("\n\n") if p.strip()]
    return [re.sub(r"^P\d+:\s*", "", p) for p in paras]


def synth_one(py: str, text: str, out: Path, voice: str, rate: str) -> bool:
    """调用 edge-tts CLI 合成单段。"""
    r = subprocess.run([py, "-m", "edge_tts", "--voice", voice, "--rate", rate,
                        "--text", text, "--write-media", str(out)],
                       capture_output=True, text=True, timeout=180)
    return r.returncode == 0 and out.is_file() and out.stat().st_size > 1000


def duration_ffprobe(mp3: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(mp3)], capture_output=True, text=True)
    return float(r.stdout.strip() or 0)


def fmt_ts(sec: float) -> str:
    h, rem = divmod(int(sec), 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d},{int((sec % 1) * 1000):03d}"


def main() -> int:
    ap = argparse.ArgumentParser(description="Edge TTS 全量合成（Xiaoxiao）")
    ap.add_argument("--html", type=Path)
    ap.add_argument("--notes", type=Path)
    ap.add_argument("--outdir", type=Path, default=Path("videos"))
    ap.add_argument("--flat", action="store_true", help="write directly into --outdir instead of a stem subdirectory")
    ap.add_argument("--voice", default=VOICE)
    ap.add_argument("--rate", default=RATE)
    args = ap.parse_args()

    if not args.html and not args.notes:
        print("用法错误: 需提供 --html 或 --notes", file=sys.stderr)
        return 2
    py = find_edge_env()
    if not py:
        print("用法错误: 找不到 edge-tts 环境（$EDGE_TTS_PYTHON 可指定）", file=sys.stderr)
        return 2

    notes = extract_notes_from_html(args.html) if args.html else extract_notes_from_txt(args.notes)
    if not notes:
        print("用法错误: 未提取到 notes", file=sys.stderr)
        return 2

    deck_name = (args.html or args.notes).stem
    out = args.outdir if args.flat else args.outdir / deck_name
    seg_dir = out / "segments"
    seg_dir.mkdir(parents=True, exist_ok=True)

    print(f"合成 {len(notes)} 段（voice={args.voice} rate={args.rate}）→ {out}")
    segs = []
    for i, text in enumerate(notes, 1):
        mp3 = seg_dir / f"seg-{i:02d}.mp3"
        if mp3.exists():
            print(f"  [{i}/{len(notes)}] 缓存命中 {mp3.name}")
        else:
            if not synth_one(py, text, mp3, args.voice, args.rate):
                print(f"  [{i}/{len(notes)}] 失败: {mp3.name}", file=sys.stderr)
                return 1
            print(f"  [{i}/{len(notes)}] {mp3.name} ({mp3.stat().st_size//1024}KB)")
        segs.append({"page": i, "file": str(mp3), "duration": duration_ffprobe(mp3)})

    concat_file = out / "concat.txt"
    concat_file.write_text("".join(f"file '{Path(s['file']).resolve()}'\n" for s in segs),
                           encoding="utf-8")
    full = out / "narration-full.mp3"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file),
                    "-c", "copy", str(full)], check=True, capture_output=True)

    srt_lines, cursor = [], 0.0
    for s in segs:
        start, end = cursor, cursor + s["duration"]
        srt_lines.append(f"{s['page']}\n{fmt_ts(start)} --> {fmt_ts(end)}\n{notes[s['page']-1]}\n")
        s["start"], s["end"] = start, end
        cursor = end
    (out / "narration.srt").write_text("\n".join(srt_lines), encoding="utf-8")
    (out / "segments.json").write_text(
        json.dumps({"total_seconds": round(cursor, 2), "segments": segs},
                   ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"完成: {full}（{cursor:.1f}s）· narration.srt · segments.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
