#!/usr/bin/env python3
"""Generate Doubao question-intonation references for voice.zhiwei.

The 2026-09-07 investigation found host questions were generated with the
`curious` emotion reference, whose ending question contour is too subtle for
VoxCPM continuation to reproduce a reliable rising.  This job synthesizes a
dedicated `questioning` reference whose final sentences clearly end in 吗/呢,
and merges them into one 16 kHz mono WAV plus a manifest.
"""
import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
loader = importlib.util.spec_from_file_location("doubao_ws", HERE / "tts-doubao-v3-ws-test.py")
doubao = importlib.util.module_from_spec(loader)
loader.loader.exec_module(doubao)

MODEL = "seed-tts-2.0-expressive"
VOICE_ID = "zh_female_xiaohe_uranus_bigtts"
SPEECH_RATE = -10
OUTDIR = HERE.parent / "outputs" / "experiments" / "doubao-question-reference-v1"

# One clip per final particle, then concatenated as the `questioning` asset.
CLIPS = {
    "zhiwei-ma": "先别急着说好事。价格是回来了，可这次的回暖，真的能站得住吗？",
    "zhiwei-ne": "我顺着你的逻辑再问一句：如果利润还留在低位，那现在这组价格，是不是已经提前预支了反弹呢？",
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    OUTDIR.mkdir(parents=True, exist_ok=True)
    records = []
    parts = []
    for name, text in CLIPS.items():
        mp3 = OUTDIR / f"{name}.mp3"
        wav = OUTDIR / f"{name}.wav"
        print(f"豆包生成 {name}: {text}", flush=True)
        doubao.synthesize(text, VOICE_ID, mp3, MODEL, speech_rate=SPEECH_RATE)
        subprocess.run([
            "ffmpeg", "-y", "-i", str(mp3), "-ac", "1", "-ar", "16000",
            "-c:a", "pcm_s16le", str(wav),
        ], check=True, capture_output=True)
        duration = float(subprocess.check_output([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "csv=p=0", str(wav),
        ], text=True).strip())
        records.append({"name": name, "voice_id": VOICE_ID, "model": MODEL,
                        "speech_rate": SPEECH_RATE, "text": text, "file": str(wav),
                        "duration_seconds": duration, "sha256": sha256(wav)})
        parts.append(wav)

    combined = OUTDIR / "questioning.wav"
    listfile = OUTDIR / "concat.txt"
    listfile.write_text("".join(f"file '{p}'\n" for p in parts), encoding="utf-8")
    subprocess.run([
        "ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(listfile),
        "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(combined),
    ], check=True, capture_output=True)
    combined_text = "".join(CLIPS.values())
    combined_duration = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration",
        "-of", "csv=p=0", str(combined),
    ], text=True).strip())
    records.append({"name": "zhiwei-questioning", "voice_id": VOICE_ID, "model": MODEL,
                    "speech_rate": SPEECH_RATE, "text": combined_text, "file": str(combined),
                    "duration_seconds": combined_duration, "sha256": sha256(combined)})
    (OUTDIR / "manifest.json").write_text(
        json.dumps({"status": "PASS", "records": records}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(records, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
