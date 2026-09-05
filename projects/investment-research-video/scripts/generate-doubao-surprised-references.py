#!/usr/bin/env python3
"""Generate the missing surprised reference clips for the canonical voice assets."""
import importlib.util
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
        "text": "这个结果比我预想的快。刚才还看不出端倪，怎么一下子就变成这样了？",
    },
    "shenyan": {
        "voice_id": "zh_male_liufei_uranus_bigtts",
        "speech_rate": 0,
        "text": "这个结果，确实有点出乎意料。表面上的变化不算小，可它到底意味着什么，还得再往下拆。",
    },
}


def main():
    asset_root = HERE.parents[2] / ".ai" / "assets" / "voices"
    for speaker, config in REFERENCES.items():
        output = asset_root / speaker / "emotion" / "surprised.wav"
        mp3 = output.with_suffix(".mp3")
        output.parent.mkdir(parents=True, exist_ok=True)
        print(f"豆包生成 {speaker}/surprised: {config['text']}", flush=True)
        doubao.synthesize(config["text"], config["voice_id"], mp3, MODEL, speech_rate=config["speech_rate"])
        subprocess.run([
            "ffmpeg", "-y", "-i", str(mp3), "-ac", "1", "-ar", "16000",
            "-c:a", "pcm_s16le", str(output),
        ], check=True, capture_output=True)
        mp3.unlink()
        print(output)


if __name__ == "__main__":
    main()
