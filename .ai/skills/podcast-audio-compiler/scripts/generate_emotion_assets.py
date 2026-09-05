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
        "prompt": "我先说一个直觉啊，这个数字看起来挺亮眼，可是往下拆，现金流好像没有一起跟上。那这个增长，到底是真的变好了，还是只是表面看起来热闹？",
    },
    "shenyan": {
        "clip": ASSET_ROOT / "voices" / "shenyan" / "reference.wav",
        "prompt": "等等，这个数字我得先打个问号。收入是涨了没错，可现金流怎么还没跟上？先别急着说业务变好了，利润到底是怎么来的，还得再看一眼。",
    },
}

EMOTION_TEXT = {
    "curious": "等等，这里有个问题——如果收入真的在增长，为什么现金流还没有跟上？这个反差到底从哪里来？",
    "surprised": "这个结果比我预想的快。刚才还看不出端倪，怎么一下子就变成这样了？",
    "skeptical": "先别急着下结论。数字看起来很漂亮，但利润和现金流的底色，可能没有表面那么简单。",
    "cautious": "这件事我会把结论压低一点。现在能确认的是阶段性改善，还不能把它直接说成长期趋势。",
    "firm": "这一点可以明确：增长已经发生，但质量必须用连续数据验证。没有回款和现金流，规模本身不能证明生意变好了。",
    "thoughtful": "我更愿意把这件事放回时间里看。真正重要的不是这一期数字，而是下一期、再下一期，它能不能持续留下来。",
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
