#!/usr/bin/env python3
"""Generate stronger, scene-based Doubao emotion references for VoxCPM2."""
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
        "items": {
            "curious": (
                "诶，等一下，这个变化好像比我们刚才想的复杂。表面上看是一个结果，可往下追，"
                "到底是哪一环发生了变化？你有没有觉得，这里面还藏着一个没解释清楚的问题？",
                "用自然、明显好奇的口语语气说，像突然发现了线索，带一点追问和探索感；不要播音腔。",
            ),
            "surprised": (
                "啊？这个结果确实有点出乎意料。刚才还看起来很平稳，怎么一下子就变成这样了？"
                "先别急着往下定论，我得再确认一遍，到底是哪一个数字突然变了。",
                "用克制但真实的惊讶语气说，开头先有一点意外，随后压住情绪继续确认；不要夸张。",
            ),
            "skeptical": (
                "等一下，这也能算好消息吗？收入是涨了，可钱到底回来没有？利润表好看一点，"
                "就能说明公司真的变好了吗？如果客户一直不回款，这个增长到底是谁的增长？",
                "用明显怀疑、克制但有压力的质问语气说。开头先停一下，中间逐步加强，最后连续反问；不要大喊，不要方言。",
            ),
            "cautious": (
                "我觉得这里还是先别急着庆祝。现在看到的只是一个阶段性信号，后面能不能持续，"
                "还没有完全验证。万一下一季度又变回去，我们是不是又得重新解释一遍？",
                "用谨慎、克制、略带担忧的口语语气说，像是在提醒对方不要过早下结论；有停顿但不要拖沓。",
            ),
            "firm": (
                "这一点我想说得明确一点：增长不是答案，回款和现金流才是答案。"
                "如果钱没有真正回到公司账上，再漂亮的收入数字，也不能替它证明经营变好了。",
                "用平静但坚定的语气说，前半句清晰立场，后半句逐步加重；不要喊叫，要有判断力。",
            ),
            "thoughtful": (
                "如果把时间拉长一点看，眼前这个结果可能没有那么简单。一次变化说明不了太多，"
                "真正值得看的，是它能不能在下一阶段重复出现。这个问题，可能得慢一点想。",
                "用放慢一点、边思考边说的口语语气，带自然停顿和回看感；不要像朗读，也不要拖音。",
            ),
        },
    },
    "shenyan": {
        "voice_id": "zh_male_liufei_uranus_bigtts",
        "role": "顾慎言",
        "items": {
            "curious": (
                "这个问题我反而觉得挺有意思。表面看是收入在增长，可往下拆，还有应收、库存和回款几个环节。"
                "到底是哪一部分在真正起作用？我们是不是漏看了什么？",
                "用自然、带探索感的好奇语气说，像在现场拆解线索；有轻微追问，不要播音腔。",
            ),
            "surprised": (
                "这个结果，确实有点意外。收入能涨到这个幅度，本身就不算小，可现金流怎么反而更紧了？"
                "这和我们第一眼看到的情况，完全不是一回事。",
                "用明显但克制的惊讶语气说，先表达意外，再转入理性分析；不要夸张，不要大喊。",
            ),
            "skeptical": (
                "这个地方，我想先停一下。听上去好像都说得通，可越往下看，越有几个地方让我不太踏实。"
                "收入增长了，钱呢？利润增加了，回款呢？如果这些都没有改善，这个结论凭什么成立？",
                "用明显怀疑、克制但有压力的质问语气说。前面先压住不信任，后面逐步加强，结尾要有反问；不要方言。",
            ),
            "cautious": (
                "这个结论，我建议先放一放。现在能确认的只是阶段性变化，还不能直接推成长期趋势。"
                "尤其是现金流，下一期的数据如果接不上，今天这个判断就得重新审视。",
                "用谨慎、低调、略带风险提醒的语气说，像是在给过快的判断踩刹车；语速稍慢，自然停顿。",
            ),
            "firm": (
                "这一点可以明确：增长本身不是答案，能不能形成回款和现金流，才决定这件事有没有真正改善。"
                "账面上的数字，不能替公司把钱收回来。这个顺序不能搞反。",
                "用沉稳、坚定、带结论感的语气说，重点逐句加重；保持克制，不要变成喊话。",
            ),
            "thoughtful": (
                "我更愿意把它放回时间里看。一次变化说明不了太多，真正有价值的，是看它能不能持续出现。"
                "有时候，最容易被忽略的，不是结果，而是结果背后那条慢慢变化的线。",
                "用低沉、放慢、边思考边说的口语语气，带一点停顿和回看感；不要拖音，不要播音腔。",
            ),
        },
    },
}


def convert(mp3: Path, wav: Path) -> float:
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(mp3), "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", str(wav)], check=True)
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(wav)], text=True).strip())


def main() -> None:
    outdir = HERE.parent / "outputs" / "experiments" / "doubao-emotion-library-v2-strong"
    records = []
    for speaker, config in LIBRARY.items():
        speaker_dir = outdir / speaker
        speaker_dir.mkdir(parents=True, exist_ok=True)
        for emotion, (text, instruction) in config["items"].items():
            mp3 = speaker_dir / f"{emotion}.mp3"
            wav = speaker_dir / f"{emotion}.wav"
            print(f"生成 {speaker}/{emotion}", flush=True)
            result = doubao.synthesize(text, config["voice_id"], mp3, model=None, context_texts=[instruction], speech_rate=RATE)
            duration = convert(mp3, wav)
            records.append({"speaker": speaker, "role": config["role"], "emotion": emotion, "voice_id": config["voice_id"], "model": None, "speech_rate": RATE, "context_texts": [instruction], "text": text, "mp3": str(mp3), "wav": str(wav), "duration_seconds": duration, "api_result": result})
    (outdir / "emotion-library.json").write_text(json.dumps({"status": "PASS", "records": records}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"完成: {outdir}", flush=True)


if __name__ == "__main__":
    main()
