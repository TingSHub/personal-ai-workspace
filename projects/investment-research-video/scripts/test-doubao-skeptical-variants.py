#!/usr/bin/env python3
"""Generate conversational skeptical variants for a Doubao emotion-reference A/B."""
import importlib.util
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
loader = importlib.util.spec_from_file_location("doubao_ws", HERE / "tts-doubao-v3-ws-test.py")
doubao = importlib.util.module_from_spec(loader)
loader.loader.exec_module(doubao)

VOICE_ID = "zh_male_liufei_uranus_bigtts"
MODEL = "seed-tts-2.0-expressive"
VARIANTS = {
    "formal": "先别急着下结论。数字看起来很漂亮，但利润和现金流的底色，可能没有表面那么简单。我们还得继续核对。",
    "conversational": "等等，这个数字我得先打个问号。收入是涨了没错，可现金流怎么还没跟上？先别急着说业务变好了，利润到底是怎么来的，还得再看一眼。",
    "strong_skeptic": "先等等。这个结论，我现在还不能认。收入看着不错，可现金流没跟上，利润的质量就得打个问号。到底是真改善，还是阶段性波动，数据还没给答案。",
}


def main():
    outdir = HERE.parent / "outputs" / "experiments" / "doubao-shenyan-skeptical-v1"
    outdir.mkdir(parents=True, exist_ok=True)
    records = []
    for name, text in VARIANTS.items():
        mp3 = outdir / f"{name}.mp3"
        wav = outdir / f"{name}.wav"
        print(f"豆包生成 {name}: {text}")
        result = doubao.synthesize(text, VOICE_ID, mp3, MODEL)
        subprocess.run(["ffmpeg", "-y", "-i", str(mp3), "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(wav)], check=True, capture_output=True)
        duration = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(wav)], text=True).strip()
        records.append({"variant": name, "speaker": "shenyan", "voice_id": VOICE_ID, "model": MODEL, "text": text, "wav": str(wav), "duration_seconds": float(duration)})
    (outdir / "manifest.json").write_text(json.dumps({"status": "PASS", "records": records}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(records, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
