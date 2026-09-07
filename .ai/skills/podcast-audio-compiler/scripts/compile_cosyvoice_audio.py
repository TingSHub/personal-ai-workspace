#!/usr/bin/env python3
"""Compile the shared podcast manifest with Fun-CosyVoice 3 zero-shot voices."""
from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path

import numpy as np

WORKSPACE_ROOT = Path(__file__).resolve().parents[4]
ASSET_ROOT = WORKSPACE_ROOT / ".ai" / "assets"

BACKEND_NAME = "CosyVoice3-0.5B"
VOICE_CONFIG = {
    "zhiwei": {
        "ref": ASSET_ROOT / "voices" / "zhiwei" / "reference.wav",
        "prompt": "大家好，我是林知微。今天我们来聊聊投资这件事。营收九百六十七亿，净利润却只有十六亿，这个反差，值得每一个人认真思考。有人说，这是AI风口上的真龙；也有人说，这不过是一吹就破的泡沫。数据不会说谎，但数据需要被读懂。你，更相信哪一个？欢迎在评论区告诉我。",
    },
    "shenyan": {
        "ref": ASSET_ROOT / "voices" / "shenyan" / "reference.wav",
        "prompt": "欢迎来到账本两面，我是顾慎言。20多年投资经验，经历过2007年牛市，2015年股灾，见过太多看着贵其实不贵，和看着便宜其实是坑的故事。",
    },
}

PAUSES_MS = {"acknowledge": 120, "clarify": 180, "challenge": 220, "counter_evidence": 160, "interrupt": 70, "summarize": 280}

EMOTION_INSTRUCTIONS = {
    "curious": "请用自然、好奇、带一点追问感的播客语气表达，不要夸张。",
    "skeptical": "请用审慎、略带质疑但克制的播客语气表达。",
    "cautious": "请用谨慎、留有余地、像真人交流一样的播客语气表达。",
    "firm": "请用坚定、清晰、自然的分析语气表达。",
    "thoughtful": "请用思考、克制、稍慢一点的播客语气表达。",
}

DELIVERY_INSTRUCTIONS = {
    "stress_contrast": "把前后对比说清楚，重点自然突出。",
    "pause_before_number": "遇到关键数字前稍作停顿，再自然说出数字。",
    "short_pause": "句中保留一个很短的自然停顿。",
}


def build_style_instruction(turn: dict) -> str:
    parts = []
    emotion = turn.get("emotion")
    delivery = turn.get("delivery")
    if emotion in EMOTION_INSTRUCTIONS:
        parts.append(EMOTION_INSTRUCTIONS[emotion])
    if delivery in DELIVERY_INSTRUCTIONS:
        parts.append(DELIVERY_INSTRUCTIONS[delivery])
    parts.append("整体像两位主持人在真实播客中交流，不要像新闻播报，也不要机械添加语气词。")
    return "You are a helpful assistant. " + "".join(parts) + "<|endofprompt|>"


def duration(path: Path) -> float:
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)], check=True, capture_output=True, text=True)
    return float(result.stdout.strip())


def srt_time(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def make_pause(path: Path, milliseconds: int, sample_rate: int = 24000) -> None:
    subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", f"anullsrc=r={sample_rate}:cl=mono", "-t", f"{milliseconds / 1000:.3f}", "-c:a", "pcm_s16le", str(path)], check=True, capture_output=True)


def clean_segment_boundary(path: Path, threshold_db: float = -45.0, min_quiet_ms: int = 40, fade_ms: int = 8) -> dict:
    """Conservatively remove only quiet edge padding and fade every segment edge."""
    import soundfile as sf

    audio, sample_rate = sf.read(str(path), dtype="float32")
    if audio.ndim > 1:
        audio = audio.mean(axis=1)
    if audio.size == 0:
        return {"trimmed_start_ms": 0, "trimmed_end_ms": 0, "leading_quiet_ms": 0, "trailing_quiet_ms": 0, "fade_ms": 0}

    original_len = len(audio)
    window = max(1, int(sample_rate * 0.01))
    frame_count = int(math.ceil(len(audio) / window))
    rms = np.array([
        np.sqrt(np.mean(np.square(audio[i * window:min((i + 1) * window, len(audio))])))
        for i in range(frame_count)
    ])
    threshold = 10 ** (threshold_db / 20.0)
    active = np.flatnonzero(rms > threshold)
    if active.size == 0:
        return {"trimmed_start_ms": 0, "trimmed_end_ms": 0, "leading_quiet_ms": round(len(audio) / sample_rate * 1000, 1), "trailing_quiet_ms": 0, "fade_ms": 0}

    first_active = int(active[0] * window)
    last_active = min(len(audio), int((active[-1] + 1) * window))
    leading_quiet_ms = first_active / sample_rate * 1000
    trailing_quiet_ms = (len(audio) - last_active) / sample_rate * 1000
    start = first_active if leading_quiet_ms >= min_quiet_ms else 0
    end = last_active if trailing_quiet_ms >= min_quiet_ms else len(audio)
    # Keep a small natural margin after trimming; do not hard-cut the first phoneme.
    margin = int(sample_rate * 0.01)
    start = max(0, start - margin)
    end = min(len(audio), end + margin)
    audio = audio[start:end].copy()
    fade = min(int(sample_rate * fade_ms / 1000), len(audio) // 2)
    if fade:
        audio[:fade] *= np.linspace(0.0, 1.0, fade, dtype=np.float32)
        audio[-fade:] *= np.linspace(1.0, 0.0, fade, dtype=np.float32)
    sf.write(str(path), audio, sample_rate, subtype="PCM_16")
    return {
        "trimmed_start_ms": round(start / sample_rate * 1000, 1),
        "trimmed_end_ms": round((original_len - end) / sample_rate * 1000, 1),
        "leading_quiet_ms": round(leading_quiet_ms, 1),
        "trailing_quiet_ms": round(trailing_quiet_ms, 1),
        "fade_ms": fade_ms if fade else 0,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episode", type=Path, required=True)
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--repo-root", type=Path, required=True)
    parser.add_argument("--model-dir", type=Path, required=True)
    parser.add_argument("--natural-pauses", action="store_true")
    parser.add_argument("--post-process", choices=("none", "light", "natural"), default="none")
    parser.add_argument("--style-control", choices=("none", "instruct"), default="none")
    parser.add_argument("--boundary-clean", action="store_true", help="trim quiet edges conservatively and apply short fades")
    parser.add_argument("--voice-override", action="append", default=[], metavar="SPEAKER=PATH")
    parser.add_argument("--voice-prompt", action="append", default=[], metavar="SPEAKER=TEXT")
    args = parser.parse_args()

    episode = json.loads(args.episode.read_text(encoding="utf-8"))
    mode = episode.get("format_mode")
    role_map = episode.get("role_map") or {}
    if mode not in {"host_analyst", "debate"}:
        raise SystemExit("episode.json must declare format_mode: host_analyst or debate")
    if set(role_map) != {"host", "analyst"}:
        raise SystemExit("episode.json must declare role_map with host and analyst")
    turns = episode.get("turns", [])
    voice_overrides = dict(item.split("=", 1) for item in args.voice_override)
    voice_prompts = dict(item.split("=", 1) for item in args.voice_prompt)
    if not turns:
        raise SystemExit("episode.json has no turns")
    for i, turn in enumerate(turns):
        required = {"turn_id", "topic_id", "speaker", "text"}
        missing = required - set(turn)
        if missing:
            raise SystemExit(f"turn {i} missing: {sorted(missing)}")
        if turn["speaker"] not in VOICE_CONFIG:
            raise SystemExit(f"unregistered speaker voice: {turn['speaker']}")
        same_beat = bool(turn.get("beat_group_id") and turn.get("beat_group_id") == turns[i - 1].get("beat_group_id")) if i else False
        if i and turn["speaker"] == turns[i - 1]["speaker"] and not (mode == "host_analyst" and same_beat):
            raise SystemExit(f"speaker alternation failed at {turn['turn_id']}")

    sys.path.insert(0, str(args.repo_root / "third_party" / "Matcha-TTS"))
    sys.path.insert(0, str(args.repo_root))
    import torch
    import torchaudio
    from cosyvoice.cli.cosyvoice import AutoModel

    args.outdir.mkdir(parents=True, exist_ok=True)
    segments_dir = args.outdir / "segments"
    segments_dir.mkdir(exist_ok=True)
    model = AutoModel(model_dir=str(args.model_dir), load_trt=False, fp16=False)
    segments = []
    cursor = 0.0
    pause_files: list[str] = []
    pause_total = 0.0
    reused_segments = 0
    for index, turn in enumerate(turns, 1):
        output = segments_dir / f"{turn['turn_id']}.wav"
        if not output.exists():
            cfg = VOICE_CONFIG[turn["speaker"]]
            ref = Path(voice_overrides.get(turn["speaker"], cfg["ref"]))
            prompt_text = voice_prompts.get(turn["speaker"], cfg["prompt"])
            prompt = f"You are a helpful assistant.<|endofprompt|>{prompt_text}"
            chunks = []
            if args.style_control == "instruct" or turn.get("style_instruction"):
                instruction = turn.get("style_instruction") or build_style_instruction(turn)
                for item in model.inference_instruct2(turn["text"], instruction, str(ref), stream=False):
                    chunks.append(item["tts_speech"])
            else:
                for item in model.inference_zero_shot(turn["text"], prompt, str(ref), stream=False):
                    chunks.append(item["tts_speech"])
            if not chunks:
                raise SystemExit(f"CosyVoice produced no audio for {turn['turn_id']}")
            wav = torch.cat(chunks, dim=1)
            torchaudio.save(str(output), wav.cpu(), model.sample_rate)
            boundary_info = clean_segment_boundary(output) if args.boundary_clean else {}
        else:
            reused_segments += 1
            boundary_info = {"reused": True}
        length = duration(output)
        start, end = cursor, cursor + length
        pause_ms = int(turn.get("pause_after_ms", 0))
        if args.natural_pauses and pause_ms <= 0 and index < len(turns):
            pause_ms = PAUSES_MS.get(turn.get("interaction_type"), 140)
        if index == len(turns):
            pause_ms = 0
        segments.append({"index": index, "turn_id": turn["turn_id"], "topic_id": turn["topic_id"], "speaker": turn["speaker"], "role": turn.get("role"), "beat_group_id": turn.get("beat_group_id"), "text": turn["text"], "reply_to_turn_id": turn.get("reply_to_turn_id"), "interaction_type": turn.get("interaction_type"), "backchannel": turn.get("backchannel"), "backchannel_target": turn.get("backchannel_target"), "filler_position": turn.get("filler_position"), "question_ending": turn.get("question_ending"), "emotion": turn.get("emotion"), "delivery": turn.get("delivery"), "boundary": boundary_info, "pause_after_ms": pause_ms, "file": str(output), "start": round(start, 3), "end": round(end, 3), "duration": round(length, 3)})
        if pause_ms:
            pause_file = segments_dir / f"pause-{index:02d}.wav"
            if not pause_file.exists():
                make_pause(pause_file, pause_ms, model.sample_rate)
            pause_files.append(str(pause_file.resolve()))
            pause_total += pause_ms / 1000
        else:
            pause_files.append("")
        cursor = end + pause_ms / 1000

    concat = args.outdir / "concat.txt"
    lines = []
    for index, segment in enumerate(segments):
        lines.append(f"file '{Path(segment['file']).resolve()}'\n")
        if pause_files[index]:
            lines.append(f"file '{pause_files[index]}'\n")
    concat.write_text("".join(lines), encoding="utf-8")
    concat_wav = args.outdir / "narration-concat.wav"
    full_wav = args.outdir / "narration-full.wav"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(concat_wav)], check=True, capture_output=True)
    if args.post_process == "light":
        subprocess.run(["ffmpeg", "-y", "-i", str(concat_wav), "-af", "loudnorm=I=-18:TP=-2:LRA=11:linear=true", "-c:a", "pcm_s16le", str(full_wav)], check=True, capture_output=True)
    elif args.post_process == "natural":
        subprocess.run(["ffmpeg", "-y", "-i", str(concat_wav), "-af", "acompressor=threshold=0.10:ratio=2.0:attack=20:release=180:makeup=1.0,volume=4dB,alimiter=limit=0.95", "-c:a", "pcm_s16le", str(full_wav)], check=True, capture_output=True)
    else:
        concat_wav.replace(full_wav)
    full_mp3 = args.outdir / "narration-full.mp3"
    subprocess.run(["ffmpeg", "-y", "-i", str(full_wav), "-c:a", "libmp3lame", "-q:a", "2", str(full_mp3)], check=True, capture_output=True)
    report = {"status": "PASS", "backend": BACKEND_NAME, "format_mode": mode, "role_map": role_map, "style_control": args.style_control, "boundary_clean": args.boundary_clean, "natural_pauses": args.natural_pauses, "post_process": args.post_process, "voice_overrides": voice_overrides, "voice_prompts": voice_prompts, "pause_total_seconds": round(pause_total, 3), "reused_segments": reused_segments, "turn_count": len(segments), "total_seconds": round(cursor, 3), "voices": sorted({s["speaker"] for s in segments})}
    (args.outdir / "segments.json").write_text(json.dumps({**report, "segments": segments}, ensure_ascii=False, indent=2), encoding="utf-8")
    with (args.outdir / "subtitles.srt").open("w", encoding="utf-8") as srt:
        for i, segment in enumerate(segments, 1):
            srt.write(f"{i}\n{srt_time(segment['start'])} --> {srt_time(segment['end'])}\n{segment['text']}\n\n")
    (args.outdir / "audio-qa.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
