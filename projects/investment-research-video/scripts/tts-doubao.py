#!/usr/bin/env python3
"""tts-doubao.py — 豆包 TTS 全量合成（火山语音技术 v3 API）

输入：notes 文本（P1: ... 每页一段，空行分隔）或 deck HTML（自动提取 aside.notes）
流程：逐页调用 openspeech /api/v3/tts/create（seed-audio-1.0，描述式控制男声）
      → 解 base64 → seg-NN.mp3 → ffprobe 时长 → 拼接 narration-full.mp3
      → 按累计时长派生 narration.srt（页级字幕，notes 为唯一 SoT）
输出目录：{outdir}/{deck-name}/（segments/ + narration-full.mp3 + narration.srt + segments.json）

用法：
    python3 tts-doubao.py --html <deck.html> [--outdir <dir>]
    python3 tts-doubao.py --notes <notes.txt> [--outdir <dir>]

凭证：workspace 根 .env 的 VOLC_API_KEY（X-Api-Key header）
音色：--voice-type zh_male_liufei_uranus_bigtts（seed-audio 下为描述性参考，
      实际音色由 --voice-desc 描述控制；开通 bigtts 语音合成模型后改 --model 即可）

退出码：0=成功 / 1=部分失败 / 2=用法错误
"""
import argparse
import base64
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path
from urllib import request

API_URL = "https://openspeech.bytedance.com/api/v3/tts/unidirectional"
RESOURCE_ID = "seed-tts-2.0"
DEFAULT_VOICE = "zh_male_liufei_uranus_bigtts"
DEFAULT_VOICE_DESC = ""  # seed-tts-2.0 用 speaker 音色 ID，无需描述


def load_key():
    env = Path(__file__).resolve().parents[3] / ".env"
    if env.is_file():
        for line in env.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("VOLC_API_KEY="):
                return line.split("=", 1)[1].strip()
    return os.environ.get("VOLC_API_KEY", "")


def extract_notes_from_html(html_path: Path):
    """从 deck HTML 提取每页 aside.notes（按顺序）。"""
    src = html_path.read_text(encoding="utf-8")
    notes = re.findall(r'<aside class="notes">(.*?)</aside>', src, re.S)
    return [re.sub(r"\s+", " ", n).strip() for n in notes]


def extract_notes_from_txt(txt_path: Path):
    paras = [p.strip() for p in txt_path.read_text(encoding="utf-8").split("\n\n") if p.strip()]
    return [re.sub(r"^P\d+:\s*", "", p) for p in paras]


def tts_synthesize(api_key: str, text: str, model: str, voice: str,
                   voice_desc: str, reqid: str) -> bytes:
    """调用豆包 TTS（seed-tts-2.0 单向流式），返回 mp3 字节。

    响应为 NDJSON 流：每行 {"code":0,"data":"<base64 mp3 块>"}，逐行拼接。
    """
    body = json.dumps({
        "req_params": {
            "text": text,
            "speaker": voice,
            "audio_params": {"format": "mp3", "sample_rate": 24000},
        }
    }).encode("utf-8")
    req = request.Request(API_URL, data=body, method="POST", headers={
        "Content-Type": "application/json",
        "X-Api-Key": api_key,
        "X-Api-Resource-Id": RESOURCE_ID,
        "Connection": "keep-alive",
    })
    chunks = []
    try:
        with request.urlopen(req, timeout=300) as resp:
            for raw in resp:
                line = raw.decode("utf-8").strip()
                if not line:
                    continue
                obj = json.loads(line)
                if obj.get("data"):
                    chunks.append(base64.b64decode(obj["data"]))
    except Exception as e:
        raise RuntimeError(f"API 调用失败: {e}")
    if not chunks:
        raise RuntimeError("API 返回空音频")
    return b"".join(chunks)


def duration_ffprobe(mp3: Path) -> float:
    r = subprocess.run(["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
                        "-of", "csv=p=0", str(mp3)], capture_output=True, text=True)
    return float(r.stdout.strip() or 0)


def fmt_ts(sec: float) -> str:
    h, rem = divmod(int(sec), 3600)
    m, s = divmod(rem, 60)
    return f"{h:02d}:{m:02d}:{s:02d},{int((sec % 1) * 1000):03d}"


def main() -> int:
    ap = argparse.ArgumentParser(description="豆包 TTS 全量合成")
    ap.add_argument("--html", type=Path, help="deck HTML（提取 aside.notes）")
    ap.add_argument("--notes", type=Path, help="notes 文本（P1: 每页一段）")
    ap.add_argument("--outdir", type=Path, default=Path("videos"))
    ap.add_argument("--model", default=RESOURCE_ID, help="X-Api-Resource-Id（seed-tts-2.0）")
    ap.add_argument("--voice-type", default=DEFAULT_VOICE, help="speaker 音色 ID")
    ap.add_argument("--voice-desc", default=DEFAULT_VOICE_DESC)
    ap.add_argument("--sleep", type=float, default=1.0, help="请求间隔秒（限流保护）")
    args = ap.parse_args()

    if not args.html and not args.notes:
        print("用法错误: 需提供 --html 或 --notes", file=sys.stderr)
        return 2

    api_key = load_key()
    if not api_key:
        print("用法错误: .env 中缺少 VOLC_API_KEY", file=sys.stderr)
        return 2

    notes = extract_notes_from_html(args.html) if args.html else extract_notes_from_txt(args.notes)
    if not notes:
        print("用法错误: 未提取到 notes", file=sys.stderr)
        return 2

    deck_name = (args.html or args.notes).stem
    out = args.outdir / deck_name
    seg_dir = out / "segments"
    seg_dir.mkdir(parents=True, exist_ok=True)

    print(f"合成 {len(notes)} 段（resource={args.model} speaker={args.voice_type}）→ {out}")
    segs = []
    for i, text in enumerate(notes, 1):
        mp3 = seg_dir / f"seg-{i:02d}.mp3"
        if mp3.exists():
            print(f"  [{i}/{len(notes)}] 缓存命中 {mp3.name}")
        else:
            try:
                audio = tts_synthesize(api_key, text, args.model, args.voice_type,
                                       args.voice_desc, f"{deck_name}-{i}-{int(time.time())}")
                mp3.write_bytes(audio)
                print(f"  [{i}/{len(notes)}] {mp3.name} ({len(audio)//1024}KB)")
            except Exception as e:
                print(f"  [{i}/{len(notes)}] 失败: {e}", file=sys.stderr)
                return 1
            time.sleep(args.sleep)
        segs.append({"page": i, "file": str(mp3), "duration": duration_ffprobe(mp3)})

    # 拼接（ffmpeg concat demuxer）
    concat_file = out / "concat.txt"
    concat_file.write_text("".join(f"file '{Path(s['file']).resolve()}'\n" for s in segs), encoding="utf-8")
    full = out / "narration-full.mp3"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file),
                    "-c", "copy", str(full)], check=True, capture_output=True)

    # SRT 派生（页级：累计时长，notes 为唯一 SoT，断句不改文案）
    srt_lines = []
    cursor = 0.0
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
