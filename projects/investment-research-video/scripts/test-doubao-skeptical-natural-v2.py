#!/usr/bin/env python3
"""Generate a generic, conversational skeptical performance reference."""
import importlib.util
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
loader = importlib.util.spec_from_file_location("doubao_ws", HERE / "tts-doubao-v3-ws-test.py")
doubao = importlib.util.module_from_spec(loader)
loader.loader.exec_module(doubao)

TEXT = "这个地方，我想先停一下。听上去好像都说得通，可越往下看，越有几个地方让我不太踏实。先别急着下结论，我们把细节一项一项对清楚，再判断这个说法到底站不站得住。"
OUTDIR = HERE.parent / "outputs" / "experiments" / "doubao-shenyan-skeptical-v2"


def main():
    OUTDIR.mkdir(parents=True, exist_ok=True)
    mp3 = OUTDIR / "skeptical-natural.mp3"
    wav = OUTDIR / "skeptical-natural.wav"
    doubao.synthesize(TEXT, "zh_male_liufei_uranus_bigtts", mp3, "seed-tts-2.0-expressive")
    subprocess.run(["ffmpeg", "-y", "-i", str(mp3), "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(wav)], check=True, capture_output=True)
    print(wav)
    print(TEXT)


if __name__ == "__main__":
    main()
