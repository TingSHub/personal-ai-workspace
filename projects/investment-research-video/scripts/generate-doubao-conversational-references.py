#!/usr/bin/env python3
"""Generate clean conversational Doubao expressive references for both voices."""
import importlib.util
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
loader = importlib.util.spec_from_file_location("doubao_ws", HERE / "tts-doubao-v3-ws-test.py")
doubao = importlib.util.module_from_spec(loader)
loader.loader.exec_module(doubao)

MODEL = "seed-tts-2.0-expressive"
REFERENCES = {
    "zhiwei": {
        "voice_id": "zh_female_xiaohe_uranus_bigtts",
        "speech_rate": -10,
        "text": "我先说一个直觉啊，这个数字看起来挺亮眼，可是往下拆，现金流好像没有一起跟上。那这个增长，到底是真的变好了，还是只是表面看起来热闹？",
    },
    "shenyan": {
        "voice_id": "zh_male_liufei_uranus_bigtts",
        "speech_rate": 0,
        "text": "等等，这个数字我得先打个问号。收入是涨了没错，可现金流怎么还没跟上？先别急着说业务变好了，利润到底是怎么来的，还得再看一眼。",
    },
}


def main():
    outdir = HERE.parent / "outputs" / "experiments" / "doubao-conversational-references-mixed-v1"
    outdir.mkdir(parents=True, exist_ok=True)
    records = []
    for speaker, config in REFERENCES.items():
        mp3 = outdir / f"{speaker}.mp3"
        wav = outdir / f"{speaker}.wav"
        print(f"豆包生成 {speaker}: {config['text']}", flush=True)
        doubao.synthesize(config["text"], config["voice_id"], mp3, MODEL, speech_rate=config["speech_rate"])
        subprocess.run([
            "ffmpeg", "-y", "-i", str(mp3), "-ac", "1", "-ar", "16000",
            "-c:a", "pcm_s16le", str(wav),
        ], check=True, capture_output=True)
        duration = subprocess.check_output([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "csv=p=0", str(wav),
        ], text=True).strip()
        records.append({
            "speaker": speaker,
            "voice_id": config["voice_id"],
            "model": MODEL,
            "context_texts": None,
            "speech_rate": config["speech_rate"],
            "text": config["text"],
            "mp3": str(mp3),
            "wav": str(wav),
            "duration_seconds": float(duration),
        })
    (outdir / "manifest.json").write_text(
        json.dumps({"status": "PASS", "records": records}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(records, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
