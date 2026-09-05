#!/usr/bin/env python3
"""Generate an A/B library for Doubao expressive vs voice instructions."""
import importlib.util
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
loader = importlib.util.spec_from_file_location("doubao_ws", HERE / "tts-doubao-v3-ws-test.py")
doubao = importlib.util.module_from_spec(loader)
loader.loader.exec_module(doubao)

RATE = -10
LIBRARY = {
    "zhiwei": {
        "voice_id": "zh_female_xiaohe_uranus_bigtts",
        "role": "林知微",
        "texts": {
            "curious": "这个地方挺有意思的。我原本以为答案很简单，可顺着往下看，问题反而越来越多。到底是哪一环，出了变化？",
            "surprised": "这个变化比我预想得快。刚才还看不出端倪，转眼之间，结果已经完全不一样了。",
            "skeptical": "先别急着把它说成好消息。表面看起来确实不错，但我想知道，真正发生变化的到底是什么？",
            "cautious": "我觉得这里可以先保留一点判断。现在看到的是一个信号，但它能不能持续，还需要更多数据来验证。",
            "firm": "这一点我们可以先说清楚：事实已经发生，结论还不能提前下。两件事要分开看。",
            "thoughtful": "如果把时间拉长一点看，这件事可能没有那么简单。眼前的变化值得关注，但真正重要的是它能不能延续。",
        },
    },
    "shenyan": {
        "voice_id": "zh_male_liufei_uranus_bigtts",
        "role": "顾慎言",
        "texts": {
            "curious": "这个问题值得拆开看。表面上是一个结果，往下追，其实还牵涉到几个不同的环节。究竟是哪一部分在起作用？",
            "surprised": "这个结果，确实有点出乎意料。表面上的变化不算小，但它到底意味着什么，还要再往下拆。",
            "skeptical": "这个地方，我想先停一下。听上去好像都说得通，可越往下看，越有几个地方让我不太踏实。先别急着下结论，我们把细节一项一项对清楚，再判断这个说法到底站不站得住。",
            "cautious": "这个结论，我建议先放一放。现在能确认的是阶段性变化，还不能直接推成长期趋势。后面的数据，才是关键。",
            "firm": "这一点可以明确：增长本身不是答案，能不能形成回款和现金流，才决定这件事有没有真正改善。",
            "thoughtful": "我更愿意把它放回时间里看。一次变化说明不了太多，真正有价值的，是看它能不能在下一阶段持续出现。",
        },
    },
}

INSTRUCTIONS = {
    "curious": "用自然的口语表达好奇，带一点追问和探索感，不要像朗读稿。",
    "surprised": "用克制的惊讶语气说，先有一点意外，再把情绪收住，不要夸张。",
    "skeptical": "用带一点怀疑、犹豫和反问的语气说，先停顿一下，再逐步拆解；语气克制，不要生硬。",
    "cautious": "用谨慎、克制的口语语气说，像是在提醒对方先别下结论；可以有轻微犹豫。",
    "firm": "用平静但坚定的语气说，重点清楚，收尾有判断力，不要喊出来。",
    "thoughtful": "用放慢一点、边思考边说的语气，带一点停顿和回看感，但不要拖沓。",
}


def convert(mp3: Path, wav: Path) -> float:
    subprocess.run([
        "ffmpeg", "-y", "-v", "error", "-i", str(mp3), "-ac", "1", "-ar", "16000",
        "-c:a", "pcm_s16le", str(wav),
    ], check=True)
    duration = subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(wav)
    ], text=True).strip()
    return float(duration)


def main() -> None:
    outdir = HERE.parent / "outputs" / "experiments" / "doubao-emotion-ab-v1"
    records = []
    for variant in ("A-expressive", "B-context"):
        for speaker, config in LIBRARY.items():
            speaker_dir = outdir / variant / speaker
            speaker_dir.mkdir(parents=True, exist_ok=True)
            for emotion, text in config["texts"].items():
                mp3 = speaker_dir / f"{emotion}.mp3"
                wav = speaker_dir / f"{emotion}.wav"
                context = [INSTRUCTIONS[emotion]] if variant == "B-context" else None
                model = "seed-tts-2.0-expressive" if variant == "A-expressive" else None
                print(f"{variant} {speaker}/{emotion}", flush=True)
                result = doubao.synthesize(
                    text, config["voice_id"], mp3, model=model,
                    context_texts=context, speech_rate=RATE,
                )
                duration = convert(mp3, wav)
                records.append({
                    "variant": variant,
                    "speaker": speaker,
                    "role": config["role"],
                    "emotion": emotion,
                    "voice_id": config["voice_id"],
                    "model": model,
                    "context_texts": context,
                    "speech_rate": RATE,
                    "text": text,
                    "mp3": str(mp3),
                    "wav": str(wav),
                    "duration_seconds": duration,
                })
    (outdir / "manifest.json").write_text(
        json.dumps({"status": "PASS", "speech_rate": RATE, "records": records}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"完成: {outdir}", flush=True)


if __name__ == "__main__":
    main()
