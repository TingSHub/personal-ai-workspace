#!/usr/bin/env python3
"""Compile a speaker-tagged episode with IndexTTS-2.5.

This is an adapter beside the account's stable VoxCPM compiler. It deliberately
keeps the episode manifest and timing artifact shape compatible so TTS backends
can be A/B tested without changing dialogue or visuals.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

WORKSPACE_ROOT = Path(__file__).resolve().parents[4]
ASSET_ROOT = WORKSPACE_ROOT / ".ai" / "assets"

VOICE_CONFIG = {
    "zhiwei": {
        "clip": ASSET_ROOT / "voices" / "zhiwei" / "reference.wav",
        "emotion_dir": ASSET_ROOT / "voices" / "zhiwei" / "emotion",
    },
    "shenyan": {
        "clip": ASSET_ROOT / "voices" / "shenyan" / "reference.wav",
        "emotion_dir": ASSET_ROOT / "voices" / "shenyan" / "emotion",
    },
}


def duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
        check=True, capture_output=True, text=True,
    )
    return float(result.stdout.strip())


def srt_time(seconds: float) -> str:
    ms = int(round(seconds * 1000))
    h, ms = divmod(ms, 3600000)
    m, ms = divmod(ms, 60000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episode", type=Path, required=True)
    parser.add_argument("--outdir", type=Path, required=True)
    parser.add_argument("--index-root", type=Path, required=True)
    parser.add_argument("--model-dir", type=Path, required=True)
    parser.add_argument("--use-bf16", action="store_true")
    parser.add_argument("--emo-alpha", type=float, default=0.5)
    args = parser.parse_args()

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
        if i and turn["speaker"] == turns[i - 1]["speaker"]:
            raise SystemExit(f"speaker alternation failed at {turn['turn_id']}")

    sys.path.insert(0, str(args.index_root))
    from indextts.infer_v2_5 import IndexTTS2

    args.outdir.mkdir(parents=True, exist_ok=True)
    segments_dir = args.outdir / "segments"
    segments_dir.mkdir(exist_ok=True)
    tts = IndexTTS2(
        cfg_path=str(args.model_dir / "config.yaml"),
        model_dir=str(args.model_dir),
        use_bf16=args.use_bf16,
        use_cuda_kernel=False,
        use_deepspeed=False,
        use_qwen_emo=False,
    )

    segments = []
    cursor = 0.0
    reused_segments = 0
    for index, turn in enumerate(turns, 1):
        output = segments_dir / f"{turn['turn_id']}.wav"
        if not output.exists():
            cfg = VOICE_CONFIG[turn["speaker"]]
            voice = Path(cfg["clip"])
            emotion = turn.get("emotion")
            emotion_clip = Path(cfg["emotion_dir"]) / f"{emotion}.wav" if emotion else None
            kwargs = {
                "spk_audio_prompt": str(voice),
                "text": turn["text"],
                "lang": "ZH",
                "output_path": str(output),
                "verbose": True,
            }
            if emotion_clip and emotion_clip.exists():
                kwargs.update({"emo_audio_prompt": str(emotion_clip), "emo_alpha": args.emo_alpha})
            tts.infer(**kwargs)
        else:
            reused_segments += 1
        length = duration(output)
        segments.append({
            "index": index,
            "turn_id": turn["turn_id"],
            "topic_id": turn["topic_id"],
            "speaker": turn["speaker"],
            "role": turn.get("role"),
            "backchannel": turn.get("backchannel"),
            "backchannel_target": turn.get("backchannel_target"),
            "filler_position": turn.get("filler_position"),
            "question_ending": turn.get("question_ending"),
            "text": turn["text"],
            "reply_to_turn_id": turn.get("reply_to_turn_id"),
            "interaction_type": turn.get("interaction_type"),
            "emotion": turn.get("emotion"),
            "delivery": turn.get("delivery"),
            "file": str(output),
            "start": round(cursor, 3),
            "end": round(cursor + length, 3),
            "duration": round(length, 3),
        })
        cursor += length

    concat = args.outdir / "concat.txt"
    concat.write_text("".join(f"file '{Path(s['file']).resolve()}'\n" for s in segments), encoding="utf-8")
    full_wav = args.outdir / "narration-full.wav"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(full_wav)], check=True, capture_output=True)
    full_mp3 = args.outdir / "narration-full.mp3"
    subprocess.run(["ffmpeg", "-y", "-i", str(full_wav), "-c:a", "libmp3lame", "-q:a", "2", str(full_mp3)], check=True, capture_output=True)
    (args.outdir / "segments.json").write_text(json.dumps({"backend": "IndexTTS-2.5", "format_mode": format_mode, "role_map": role_map, "reused_segments": reused_segments, "total_seconds": round(cursor, 3), "segments": segments}, ensure_ascii=False, indent=2), encoding="utf-8")
    with (args.outdir / "subtitles.srt").open("w", encoding="utf-8") as srt:
        for i, segment in enumerate(segments, 1):
            srt.write(f"{i}\n{srt_time(segment['start'])} --> {srt_time(segment['end'])}\n{segment['speaker']}：{segment['text']}\n\n")
    report = {"status": "PASS", "backend": "IndexTTS-2.5", "format_mode": format_mode, "role_map": role_map, "speaker_alternation": True, "reused_segments": reused_segments, "turn_count": len(segments), "total_seconds": round(cursor, 3), "voices": sorted({s["speaker"] for s in segments})}
    (args.outdir / "audio-qa.json").write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
