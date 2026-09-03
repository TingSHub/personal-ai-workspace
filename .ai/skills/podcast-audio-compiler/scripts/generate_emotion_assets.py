#!/usr/bin/env python3
"""Generate one-time reusable emotion reference clips for the account voices."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parents[4]
ASSET_ROOT = WORKSPACE_ROOT / ".ai" / "assets"

VOICE_CONFIG = {
    "zhiwei": {
        "clip": ASSET_ROOT / "voices" / "zhiwei" / "reference.wav",
        "prompt": "大家好，我是林知微。今天我们来聊聊投资这件事。营收九百六十七亿，净利润却只有十六亿，这个反差，值得每一个人认真思考。有人说，这是AI风口上的真龙；也有人说，这不过是一吹就破的泡沫。数据不会说谎，但数据需要被读懂。你，更相信哪一个？欢迎在评论区告诉我。",
    },
    "shenyan": {
        "clip": ASSET_ROOT / "voices" / "shenyan" / "reference.wav",
        "prompt": "欢迎来到账本两面，我是顾慎言。20多年投资经验，经历过2007年牛市，2015年股灾，见过太多看着贵其实不贵，和看着便宜其实是坑的故事。",
    },
    "shenyan": {
        "clip": ASSET_ROOT / "voices" / "shenyan" / "reference.wav",
        "prompt": "大家好，我是陆衡。这里是账本两面。今天我们先把收入、利润和现金流放在一起看。增长是真的，但利润能不能留下，还要继续核对。有人更看重规模，也有人更在意回款，这个问题可能没有一句话答案。",
    },
}

EMOTION_TEXT = {
    "curious": "等等，这里有个问题……为什么收入增长了，利润却没有同步跟上？",
    "skeptical": "先别急着下结论。收入看起来漂亮，但利润和现金流还得继续核对。",
    "firm": "这一点可以明确：增长已经发生，但质量还需要连续数据来验证。",
    "thoughtful": "我更愿意把这件事放回时间里看。下一期数据，可能比今天的结论更重要。",
}


def audio_duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        check=True,
        capture_output=True,
        text=True,
    )
    return float(result.stdout.strip())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--outdir", type=Path)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--speakers", nargs="+", choices=sorted(VOICE_CONFIG), default=sorted(VOICE_CONFIG))
    args = parser.parse_args()

    outdir = args.outdir or ASSET_ROOT / "voices"
    outdir.mkdir(parents=True, exist_ok=True)

    import soundfile as sf
    from voxcpm import VoxCPM

    model = VoxCPM.from_pretrained(
        "openbmb/VoxCPM2",
        load_denoiser=False,
        optimize=False,
        device=args.device,
    )
    records = {}
    report_path = outdir / "emotion-assets.json"
    if report_path.exists():
        try:
            previous = json.loads(report_path.read_text(encoding="utf-8"))
            for item in previous.get("clips", []):
                records[(item.get("speaker"), item.get("emotion"))] = item
        except (OSError, json.JSONDecodeError):
            pass
    for speaker in args.speakers:
        config = VOICE_CONFIG[speaker]
        prompt_wav = Path(config["clip"])
        speaker_dir = outdir / speaker / "emotion"
        speaker_dir.mkdir(parents=True, exist_ok=True)
        for emotion, text in EMOTION_TEXT.items():
            output = speaker_dir / f"{emotion}.wav"
            if not output.exists():
                wav = model.generate(
                    text=text,
                    prompt_wav_path=str(prompt_wav),
                    prompt_text=config["prompt"],
                    cfg_value=2.0,
                    inference_timesteps=15,
                    retry_badcase=True,
                    retry_badcase_max_times=1,
                )
                sf.write(str(output), wav, model.tts_model.sample_rate)
            records[(speaker, emotion)] = {
                "speaker": speaker,
                "emotion": emotion,
                "text": text,
                "file": str(output),
                "duration_seconds": round(audio_duration(output), 3),
                "sha256": hashlib.sha256(output.read_bytes()).hexdigest(),
            }

    report = {
        "status": "PASS",
        "speakers": sorted({speaker for speaker, _ in records}),
        "emotions": sorted(EMOTION_TEXT),
        "clips": sorted(records.values(), key=lambda item: (item["speaker"], item["emotion"])),
    }
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
