#!/usr/bin/env python3
"""Generate isolated Doubao emotion references for the local VoxCPM2 voice chain."""
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
TEXTS = {
    "curious": "这里有个问题，先别急着往下看：收入在增长，为什么现金流还没有跟上？这个反差，究竟是怎么形成的？",
    "skeptical": "先别急着下结论。数字看起来很漂亮，但利润和现金流的底色，可能没有表面这么简单。我们还得继续核对。",
    "cautious": "这件事我会把结论压低一点。现在能确认的是阶段性改善，还不能把它直接说成长期趋势。下一期数据很关键。",
    "firm": "这一点可以明确：增长已经发生，但质量必须用连续数据验证。没有回款和现金流，规模本身不能证明生意变好了。",
    "thoughtful": "我更愿意把这件事放回时间里看。真正重要的不是这一期数字，而是下一期、再下一期，它能不能持续留下来。",
}


def main():
    outdir = HERE.parent / "outputs" / "experiments" / "doubao-shenyan-emotion-v1"
    outdir.mkdir(parents=True, exist_ok=True)
    records = []
    for emotion, text in TEXTS.items():
        mp3 = outdir / f"{emotion}.mp3"
        wav = outdir / f"{emotion}.wav"
        print(f"豆包生成 {emotion}: {text}")
        result = doubao.synthesize(text, VOICE_ID, mp3, MODEL)
        subprocess.run([
            "ffmpeg", "-y", "-i", str(mp3), "-ac", "1", "-ar", "16000",
            "-c:a", "pcm_s16le", str(wav)
        ], check=True, capture_output=True)
        duration = subprocess.check_output([
            "ffprobe", "-v", "error", "-show_entries", "format=duration",
            "-of", "csv=p=0", str(wav)], text=True).strip()
        records.append({"speaker": "shenyan", "emotion": emotion,
                        "voice_id": VOICE_ID, "model": MODEL, "text": text,
                        "mp3": str(mp3), "wav": str(wav),
                        "duration_seconds": float(duration)})
    report = {"status": "PASS", "source": "remote_doubao_tts",
              "endpoint": doubao.ENDPOINT, "resource_id": doubao.RESOURCE_ID,
              "records": records}
    (outdir / "manifest.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
