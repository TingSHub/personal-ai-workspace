#!/usr/bin/env python3
"""Compile speaker-tagged episode.json into alternating VoxCPM audio and timing artifacts."""
from __future__ import annotations

import argparse
import json
import inspect
import subprocess
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parents[4]
ASSET_ROOT = WORKSPACE_ROOT / ".ai" / "assets"

VOICE_CONFIG = {
    "zhiwei": {
        "clip": ASSET_ROOT / "voices" / "zhiwei" / "reference.wav",
        "emotion_dir": ASSET_ROOT / "voices" / "zhiwei" / "emotion",
        "prompt": "我先说一个直觉啊，这个数字看起来挺亮眼，可是往下拆，现金流好像没有一起跟上。那这个增长，到底是真的变好了，还是只是表面看起来热闹？",
    },
    "shenyan": {
        "clip": ASSET_ROOT / "voices" / "shenyan" / "reference.wav",
        "emotion_dir": ASSET_ROOT / "voices" / "shenyan" / "emotion",
        "prompt": "等等，这个数字我得先打个问号。收入是涨了没错，可现金流怎么还没跟上？先别急着说业务变好了，利润到底是怎么来的，还得再看一眼。",
    },
}

EMOTION_PROMPTS = {
    "curious": "等等，这里有个问题……为什么收入增长了，利润却没有同步跟上？",
    "surprised": "这个结果，确实有点出乎意料。表面上的变化不算小，可它到底意味着什么，还得再往下拆。",
    "skeptical": "先别急着下结论。收入看起来漂亮，但利润和现金流还得继续核对。",
    "cautious": "这件事我会把结论压低一点。现在能确认的是阶段性改善，还不能把它直接说成长期趋势。",
    "firm": "这一点可以明确：增长已经发生，但质量还需要连续数据来验证。",
    "thoughtful": "我更愿意把这件事放回时间里看。下一期数据，可能比今天的结论更重要。",
    # 问句专用（2026-09-07）：curious 参考结尾升调不明显，
    # delivery=rising_question 时改用 questioning 参考；音频与文案来自豆包生成。
    "questioning": "先别急着说好事。价格是回来了，可这次的回暖，真的能站得住吗？我顺着你的逻辑再问一句：如果利润还留在低位，那现在这组价格，是不是已经提前预支了反弹呢？",
}

BACKEND_NAME = "VoxCPM2"


def clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


NATURAL_PAUSES_MS = {
    "acknowledge": 120,
    "clarify": 180,
    "challenge": 220,
    "counter_evidence": 160,
    "interrupt": 70,
    "summarize": 280,
}


def duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        check=True, capture_output=True, text=True,
    )
    return float(result.stdout.strip())


def speech_chars(text: str) -> int:
    return sum(1 for char in text if char.isalnum() or "\u4e00" <= char <= "\u9fff")


def srt_time(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def make_pause(path: Path, milliseconds: int, sample_rate: int = 48000) -> None:
    subprocess.run(
        [
            "ffmpeg", "-y", "-f", "lavfi", "-i",
            f"anullsrc=r={sample_rate}:cl=mono", "-t", f"{milliseconds / 1000:.3f}",
            "-c:a", "pcm_s16le", str(path),
        ],
        check=True, capture_output=True,
    )


def pacing_plan(turn: dict) -> dict:
    plan = turn.get("pacing_plan") or {}
    rate = float(plan.get("speech_rate", 1.0))
    target = plan.get("target_rate_cps")
    if target is not None:
        target = float(target)
        if not 3.0 <= target <= 5.5:
            raise SystemExit(f"{turn['turn_id']} pacing_plan.target_rate_cps must be between 3.0 and 5.5")
    if not 0.5 <= rate <= 2.0:
        raise SystemExit(f"{turn['turn_id']} pacing_plan.speech_rate must be between 0.5 and 2.0")
    breaks = plan.get("intra_turn_breaks") or []
    if not isinstance(breaks, list):
        raise SystemExit(f"{turn['turn_id']} pacing_plan.intra_turn_breaks must be a list")
    return {"speech_rate": rate, "target_rate_cps": target, "intra_turn_breaks": breaks, "pause_after_ms": plan.get("pause_after_ms")}


def split_pacing_text(turn: dict) -> list[tuple[str, int]]:
    plan = pacing_plan(turn)
    text = turn["text"]
    chunks = []
    cursor = 0
    for item in plan["intra_turn_breaks"]:
        marker = str(item.get("after", ""))
        pause_ms = int(item.get("pause_ms", item.get("duration_ms", 0)))
        if not marker or pause_ms <= 0:
            raise SystemExit(f"{turn['turn_id']} has an invalid intra_turn_break")
        position = text.find(marker, cursor)
        if position < 0:
            raise SystemExit(f"{turn['turn_id']} pacing break marker not found: {marker}")
        end = position + len(marker)
        chunks.append((text[cursor:end], pause_ms))
        cursor = end
    if cursor < len(text):
        chunks.append((text[cursor:], 0))
    return chunks or [(text, 0)]


def concat_audio(files: list[Path], output: Path) -> None:
    concat = output.with_suffix(".concat.txt")
    concat.write_text("".join(f"file '{path.resolve()}'\n" for path in files), encoding="utf-8")
    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(output)],
        check=True,
        capture_output=True,
    )


def apply_speech_rate(source: Path, output: Path, rate: float) -> None:
    if abs(rate - 1.0) < 0.001:
        if source.resolve() != output.resolve():
            source.replace(output)
        return
    subprocess.run(
        ["ffmpeg", "-y", "-i", str(source), "-filter:a", f"atempo={rate:.4f}", "-c:a", "pcm_s16le", str(output)],
        check=True,
        capture_output=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episode", type=Path, required=True)
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--device", default=None)
    parser.add_argument("--natural-pauses", action="store_true", help="insert turn-aware variable pauses")
    parser.add_argument("--post-process", choices=("none", "natural"), default="none")
    parser.add_argument("--inference-timesteps", type=int, default=10)
    parser.add_argument("--cfg-value", type=float, default=2.0)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument(
        "--clone-mode",
        choices=("continuation", "ultimate", "reference"),
        default="continuation",
        help="VoxCPM clone path; continuation preserves legacy behavior",
    )
    parser.add_argument("--voice-override", action="append", default=[], metavar="SPEAKER=PATH")
    parser.add_argument("--emotion-override", action="append", default=[], metavar="SPEAKER=DIR")
    parser.add_argument("--reference-override", action="append", default=[], metavar="SPEAKER=PATH")
    parser.add_argument("--voice-prompt", action="append", default=[], metavar="SPEAKER=TEXT")
    parser.add_argument("--emotion-prompt-file", type=Path, default=None,
                        help="JSON mapping of speaker -> emotion -> exact reference text")
    args = parser.parse_args()
    voice_overrides = dict(item.split("=", 1) for item in args.voice_override)
    emotion_overrides = dict(item.split("=", 1) for item in args.emotion_override)
    reference_overrides = dict(item.split("=", 1) for item in args.reference_override)
    voice_prompts = dict(item.split("=", 1) for item in args.voice_prompt)
    emotion_prompts = {}
    if args.emotion_prompt_file:
        emotion_prompts = json.loads(args.emotion_prompt_file.read_text(encoding="utf-8"))
    episode = json.loads(args.episode.read_text(encoding="utf-8"))
    format_mode = episode.get("format_mode")
    role_map = episode.get("role_map") or {}
    if format_mode not in {"host_analyst", "debate"}:
        raise SystemExit("episode.json must declare format_mode: host_analyst or debate")
    if set(role_map) != {"host", "analyst"}:
        raise SystemExit("episode.json must declare role_map with host and analyst")
    turns = episode.get("turns", [])
    if not turns:
        raise SystemExit("episode.json has no turns")
    for i, turn in enumerate(turns):
        required = {"turn_id", "topic_id", "speaker", "text"}
        missing = required - set(turn)
        if missing:
            raise SystemExit(f"turn {i} missing: {sorted(missing)}")
        if turn["speaker"] not in VOICE_CONFIG:
            raise SystemExit(f"unregistered speaker voice: {turn['speaker']}")
        if turn.get("role") and turn["role"] in role_map and role_map[turn["role"]] != turn["speaker"]:
            raise SystemExit(f"role_map mismatch at {turn['turn_id']}")
        same_beat = bool(turn.get("beat_group_id") and turn.get("beat_group_id") == turns[i - 1].get("beat_group_id"))
        if i and turn["speaker"] == turns[i - 1]["speaker"] and not (format_mode == "host_analyst" and same_beat):
            raise SystemExit(f"speaker alternation failed at {turn['turn_id']}")

    args.outdir.mkdir(parents=True, exist_ok=True)
    segments_dir = args.outdir / "segments"
    segments_dir.mkdir(exist_ok=True)

    import soundfile as sf
    from voxcpm import VoxCPM

    device = args.device or __import__("os").environ.get("VOXCPM_DEVICE", "cuda")
    model = VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False, optimize=False, device=device)
    seed_supported = "seed" in inspect.signature(model._generate).parameters
    segments = []
    cursor = 0.0
    pause_files = []
    pause_total = 0.0
    reused_segments = 0
    for index, turn in enumerate(turns, 1):
        output = segments_dir / f"{turn['turn_id']}.wav"
        plan = pacing_plan(turn)
        has_pacing = plan["target_rate_cps"] is not None or plan["speech_rate"] != 1.0 or bool(plan["intra_turn_breaks"])
        raw_output = segments_dir / f"{turn['turn_id']}.raw.wav" if has_pacing else output
        if not output.exists():
            cfg = VOICE_CONFIG[turn["speaker"]]
            emotion = turn.get("emotion")
            emotion_dir = Path(emotion_overrides.get(turn["speaker"], cfg["emotion_dir"]))
            # 问句升调用专用参考：问号只表达语义，不保证 TTS 升调；
            # 门禁要求 delivery=rising_question 后，这里换成 questioning 情绪参考。
            if turn.get("delivery") == "rising_question" and (emotion_dir / "questioning.wav").exists():
                emotion = "questioning"
            emotion_clip = emotion_dir / f"{emotion}.wav" if emotion else None
            if turn["speaker"] in emotion_overrides and emotion_clip and emotion_clip.exists():
                prompt_wav_path = emotion_clip
                prompt_text = emotion_prompts.get(turn["speaker"], {}).get(emotion, EMOTION_PROMPTS.get(emotion, cfg["prompt"]))
            elif turn["speaker"] in voice_overrides:
                prompt_wav_path = Path(voice_overrides[turn["speaker"]])
                prompt_text = voice_prompts.get(turn["speaker"], cfg["prompt"])
            elif emotion_clip and emotion_clip.exists():
                prompt_wav_path = emotion_clip
                prompt_text = emotion_prompts.get(turn["speaker"], {}).get(emotion, EMOTION_PROMPTS.get(emotion, cfg["prompt"]))
            else:
                prompt_wav_path = Path(cfg["clip"])
                prompt_text = EMOTION_PROMPTS.get(emotion, cfg["prompt"])
            reference_wav_path = None
            if args.clone_mode in {"ultimate", "reference"}:
                reference_wav_path = Path(reference_overrides.get(turn["speaker"], cfg["clip"]))
            if args.clone_mode == "reference":
                prompt_wav_path = None
                prompt_text = None
            chunks = split_pacing_text(turn) if has_pacing else [(turn["text"], 0)]
            assembled_parts = []
            speech_parts = []
            for part_index, (part_text, intra_pause_ms) in enumerate(chunks, 1):
                part_output = raw_output if len(chunks) == 1 else segments_dir / f"{turn['turn_id']}.part-{part_index:02d}.wav"
                if not part_output.exists():
                    # VoxCPM's built-in badcase retry can spend several minutes
                    # on one long sentence. Keep the retry bounded; each part
                    # remains resumable and the audio QA report is the final gate.
                    generate_kwargs = {
                        "text": part_text,
                        "prompt_wav_path": str(prompt_wav_path) if prompt_wav_path else None,
                        "prompt_text": prompt_text,
                        "reference_wav_path": str(reference_wav_path) if reference_wav_path else None,
                        "cfg_value": args.cfg_value,
                        "inference_timesteps": args.inference_timesteps,
                        "retry_badcase": True,
                        "retry_badcase_max_times": 1,
                    }
                    if args.seed is not None and seed_supported:
                        generate_kwargs["seed"] = args.seed
                    wav = model.generate(**generate_kwargs)
                    sf.write(str(part_output), wav, model.tts_model.sample_rate)
                final_part = part_output
                if plan["target_rate_cps"] is not None:
                    actual_rate = speech_chars(part_text) / max(duration(part_output), 0.001)
                    factor = clamp(plan["target_rate_cps"] / max(actual_rate, 0.001), 0.5, 2.0)
                    final_part = segments_dir / f"{turn['turn_id']}.paced-{part_index:02d}.wav"
                    if not final_part.exists():
                        apply_speech_rate(part_output, final_part, factor)
                speech_parts.append(final_part)
                assembled_parts.append(final_part)
                if intra_pause_ms:
                    pause_file = segments_dir / f"{turn['turn_id']}.intra-pause-{part_index:02d}.wav"
                    if not pause_file.exists():
                        make_pause(pause_file, intra_pause_ms)
                    assembled_parts.append(pause_file)
            speech_duration = sum(duration(path) for path in speech_parts)
            if plan["target_rate_cps"] is not None:
                concat_audio(assembled_parts, output)
            else:
                if len(assembled_parts) > 1:
                    concat_audio(assembled_parts, raw_output)
                apply_speech_rate(raw_output, output, plan["speech_rate"])
        else:
            reused_segments += 1
            speech_duration = duration(output)
        length = duration(output)
        start = cursor
        end = cursor + length
        pause_ms = int(plan["pause_after_ms"] if plan["pause_after_ms"] is not None else turn.get("pause_after_ms", 0))
        if args.natural_pauses and pause_ms <= 0 and index < len(turns):
            pause_ms = NATURAL_PAUSES_MS.get(turn.get("interaction_type"), 140)
        if index == len(turns):
            pause_ms = 0
        realized_rate = round(speech_chars(turn["text"]) / max(speech_duration, 0.001), 3)
        segments.append({"index": index, "turn_id": turn["turn_id"], "topic_id": turn["topic_id"], "speaker": turn["speaker"], "role": turn.get("role"), "beat_group_id": turn.get("beat_group_id"), "text": turn["text"], "display_text": turn.get("display_text", turn["text"]), "reply_to_turn_id": turn.get("reply_to_turn_id"), "interaction_type": turn.get("interaction_type"), "backchannel": turn.get("backchannel"), "backchannel_target": turn.get("backchannel_target"), "filler_position": turn.get("filler_position"), "question_ending": turn.get("question_ending"), "emotion": turn.get("emotion"), "delivery": turn.get("delivery"), "pacing_plan": turn.get("pacing_plan"), "target_rate_cps": plan["target_rate_cps"], "realized_rate_cps": realized_rate, "speech_duration": round(speech_duration, 3), "pause_after_ms": pause_ms, "file": str(output), "start": round(start, 3), "end": round(end, 3), "duration": round(length, 3)})
        if pause_ms:
            pause_file = segments_dir / f"pause-{index:02d}.wav"
            if not pause_file.exists():
                make_pause(pause_file, pause_ms)
            pause_files.append(str(pause_file.resolve()))
            pause_total += pause_ms / 1000
        else:
            pause_files.append("")
        cursor = end + pause_ms / 1000

    concat = args.outdir / "concat.txt"
    concat_lines = []
    for index, segment in enumerate(segments):
        concat_lines.append(f"file '{Path(segment['file']).resolve()}'\n")
        if index <= len(pause_files) and pause_files[index - 1]:
            concat_lines.append(f"file '{pause_files[index - 1]}'\n")
    concat.write_text("".join(concat_lines), encoding="utf-8")
    full_wav = args.outdir / "narration-full.wav"
    concat_wav = args.outdir / "narration-concat.wav"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(concat_wav)], check=True, capture_output=True)
    if args.post_process == "natural":
        subprocess.run(["ffmpeg", "-y", "-i", str(concat_wav), "-af", "acompressor=threshold=0.10:ratio=2.0:attack=20:release=180:makeup=1.0,volume=4dB,alimiter=limit=0.95", "-c:a", "pcm_s16le", str(full_wav)], check=True, capture_output=True)
    else:
        concat_wav.replace(full_wav)
    full_mp3 = args.outdir / "narration-full.mp3"
    subprocess.run(["ffmpeg", "-y", "-i", str(full_wav), "-c:a", "libmp3lame", "-q:a", "2", str(full_mp3)], check=True, capture_output=True)
    (args.outdir / "segments.json").write_text(json.dumps({"backend": BACKEND_NAME, "format_mode": format_mode, "role_map": role_map, "clone_mode": args.clone_mode, "cfg_value": args.cfg_value, "seed_requested": args.seed, "seed_applied": bool(args.seed is not None and seed_supported), "voice_overrides": voice_overrides, "voice_prompts": voice_prompts, "emotion_prompts": emotion_prompts, "emotion_overrides": emotion_overrides, "reference_overrides": reference_overrides, "inference_timesteps": args.inference_timesteps, "natural_pauses": args.natural_pauses, "post_process": args.post_process, "pause_total_seconds": round(pause_total, 3), "reused_segments": reused_segments, "total_seconds": round(cursor, 3), "segments": segments}, ensure_ascii=False, indent=2), encoding="utf-8")
    with (args.outdir / "subtitles.srt").open("w", encoding="utf-8") as srt:
        for i, segment in enumerate(segments, 1):
            srt.write(f"{i}\n{srt_time(segment['start'])} --> {srt_time(segment['end'])}\n{segment['display_text']}\n\n")
    report = {"status": "PASS", "backend": BACKEND_NAME, "format_mode": format_mode, "role_map": role_map, "clone_mode": args.clone_mode, "cfg_value": args.cfg_value, "seed_requested": args.seed, "seed_applied": bool(args.seed is not None and seed_supported), "voice_overrides": voice_overrides, "voice_prompts": voice_prompts, "emotion_prompts": emotion_prompts, "emotion_overrides": emotion_overrides, "reference_overrides": reference_overrides, "inference_timesteps": args.inference_timesteps, "speaker_alternation": True, "natural_pauses": args.natural_pauses, "post_process": args.post_process, "pause_total_seconds": round(pause_total, 3), "reused_segments": reused_segments, "turn_count": len(segments), "total_seconds": round(cursor, 3), "voices": sorted({s["speaker"] for s in segments})}
    (args.outdir / "audio-qa.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
