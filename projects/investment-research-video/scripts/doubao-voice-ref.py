#!/usr/bin/env python3
"""doubao-voice-ref.py — 豆包 TTS 合成克隆参考音频(专为 VoxCPM 克隆设计)

用法:
    python3 scripts/doubao-voice-ref.py --voice zh_female_xiaohe_uranus_bigtts --out <wav>

参考文本设计:覆盖陈述/数据强调/对比张力/哲理/疑问收尾,结尾干净完整句。
凭证:workspace 根 .env 的 VOLC_API_KEY。
"""
import argparse
import base64
import json
import sys
from pathlib import Path
from urllib import request

API_URL = "https://openspeech.bytedance.com/api/v3/tts/unidirectional"
RESOURCE_ID = "seed-tts-2.0"
DEFAULT_TEXT = (
    "大家好,我是林知微。今天我们来聊聊投资这件事。"
    "营收九百六十七亿,净利润却只有十六亿,这个反差,值得每一个人认真思考。"
    "有人说,这是AI风口上的真龙;也有人说,这不过是一吹就破的泡沫。"
    "数据不会说谎,但数据需要被读懂。"
    "你,更相信哪一个?欢迎在评论区告诉我。"
)


def load_key():
    env = Path(__file__).resolve().parents[3] / ".env"
    if env.is_file():
        for line in env.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line.startswith("VOLC_API_KEY="):
                return line.split("=", 1)[1].strip()
    import os
    return os.environ.get("VOLC_API_KEY", "")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--voice", default="zh_female_xiaohe_uranus_bigtts")
    ap.add_argument("--text", default=DEFAULT_TEXT)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    key = load_key()
    if not key:
        print("用法错误: 缺少 VOLC_API_KEY", file=sys.stderr)
        return 2

    body = json.dumps({
        "req_params": {
            "text": args.text,
            "speaker": args.voice,
            "audio_params": {"format": "mp3", "sample_rate": 24000},
        }
    }).encode("utf-8")
    req = request.Request(API_URL, data=body, method="POST", headers={
        "Content-Type": "application/json",
        "X-Api-Key": key,
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
                elif obj.get("code") not in (0, 20000000) and "message" in obj:
                    print(f"API 事件: {obj.get('message')}", file=sys.stderr)
    except Exception as e:
        print(f"API 调用失败: {e}", file=sys.stderr)
        return 1

    if not chunks:
        print("无音频返回", file=sys.stderr)
        return 1

    mp3 = Path(str(args.out) + ".mp3")
    mp3.write_bytes(b"".join(chunks))
    import subprocess
    r = subprocess.run(["ffmpeg", "-y", "-v", "quiet", "-i", str(mp3), "-ac", "1",
                        "-ar", "16000", str(args.out)], check=True)
    r2 = subprocess.run(["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
                         "-of", "csv=p=0", str(args.out)], capture_output=True, text=True)
    print(f"完成: {args.out} ({float(r2.stdout.strip()):.1f}s, voice={args.voice})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
