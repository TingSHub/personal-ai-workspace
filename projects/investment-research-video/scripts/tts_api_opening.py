#!/usr/bin/env python3
"""Generate a locked opening canary with GLM-TTS and MiMo-TTS."""

from __future__ import annotations

import argparse
import base64
import json
import os
import subprocess
import urllib.error
import urllib.request
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
DEFAULT_EPISODE = ROOT / "projects/investment-research-video/outputs/companies/中科曙光/2026-08-26-editorial-gate-rerun/podcast/script/episode.json"


def load_env(path: Path) -> None:
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key.strip(), value)


def post_json(url: str, headers: dict[str, str], payload: dict) -> tuple[bytes, str]:
    request = urllib.request.Request(
        url,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={**headers, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=180) as response:
            return response.read(), response.headers.get("Content-Type", "")
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code} from {url}: {detail[:1000]}") from exc


def glm(text: str, voice: str, out: Path) -> None:
    key = os.environ.get("GLM_API_KEY")
    base = os.environ.get("GLM_OPENAI_COMPATIBLE_URL", "https://open.bigmodel.cn/api/paas/v4/").rstrip("/")
    model = os.environ.get("GLM_TTS_MODEL", "glm-tts")
    if not key:
        raise RuntimeError("GLM_API_KEY is not set")
    body, content_type = post_json(
        f"{base}/audio/speech",
        {"Authorization": f"Bearer {key}"},
        {"model": model, "input": text, "voice": voice, "speed": 1.0, "volume": 1.0, "response_format": "wav"},
    )
    if "audio" in content_type or body[:4] == b"RIFF":
        out.write_bytes(body)
        return
    data = json.loads(body)
    encoded = data.get("data") or data.get("audio")
    if isinstance(encoded, dict):
        encoded = encoded.get("data")
    if not encoded:
        raise RuntimeError(f"GLM returned no audio: {body[:500]!r}")
    out.write_bytes(base64.b64decode(encoded))


def mimo(text: str, voice: str, out: Path) -> None:
    key = os.environ.get("MIMO_API_KEY")
    model = os.environ.get("MIMO_TTS_MODEL", "mimo-v2.5-tts")
    if not key:
        raise RuntimeError("MIMO_API_KEY is not set")
    body, _ = post_json(
        "https://api.xiaomimimo.com/v1/chat/completions",
        {"Authorization": f"Bearer {key}"},
        {
            "model": model,
            "messages": [
                {"role": "user", "content": "专业财经播客开场，中文普通话，沉稳、自然、有好奇心；事实反差处适度强调，问句结尾上扬。"},
                {"role": "assistant", "content": text},
            ],
            "audio": {"format": "wav", "voice": voice},
        },
    )
    data = json.loads(body)
    try:
        encoded = data["choices"][0]["message"]["audio"]["data"]
    except (KeyError, IndexError, TypeError) as exc:
        raise RuntimeError(f"MiMo returned no audio: {body[:1000]!r}") from exc
    out.write_bytes(base64.b64decode(encoded))


def duration(path: Path) -> float:
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "default=nw=1:nk=1", str(path)],
        check=True, capture_output=True, text=True,
    )
    return float(result.stdout.strip())


def concat(files: list[Path], out: Path, pause_ms: int = 350) -> None:
    concat_file = out.with_suffix(".concat.txt")
    lines: list[str] = []
    for index, path in enumerate(files):
        lines.append(f"file '{path.resolve()}'\n")
        if index < len(files) - 1:
            lines.append(f"file '{(out.parent / f'pause-{pause_ms}ms.wav').resolve()}'\n")
    pause = out.parent / f"pause-{pause_ms}ms.wav"
    if not pause.exists():
        subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono", "-t", str(pause_ms / 1000), "-c:a", "pcm_s16le", str(pause)], check=True, capture_output=True)
    concat_file.write_text("".join(lines), encoding="utf-8")
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file), "-c:a", "pcm_s16le", str(out)], check=True, capture_output=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episode", type=Path, default=DEFAULT_EPISODE)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    load_env(ROOT / ".env")
    episode = json.loads(args.episode.read_text(encoding="utf-8"))
    turns = [t for t in episode["turns"] if t["topic_id"] in {"COLD_OPEN", "INTRO"}]
    args.out.mkdir(parents=True, exist_ok=True)
    configs = {
        "glm": (lambda text, speaker, path: glm(text, "female" if speaker == "zhiwei" else "male", path)),
        "mimo": (lambda text, speaker, path: mimo(text, "冰糖" if speaker == "zhiwei" else "苏打", path)),
    }
    manifest = {"episode": episode["episode_id"], "turns": [], "backends": {}}
    for backend, synth in configs.items():
        backend_dir = args.out / backend
        backend_dir.mkdir(parents=True, exist_ok=True)
        files = []
        try:
            for turn in turns:
                target = backend_dir / f"{turn['turn_id']}.wav"
                synth(turn["text"], turn["speaker"], target)
                files.append(target)
        except Exception as exc:
            manifest["backends"][backend] = {"status": "ERROR", "error": str(exc)}
            continue
        full = backend_dir / "opening.wav"
        concat(files, full)
        manifest["backends"][backend] = {"status": "PASS", "files": [p.name for p in files], "durations": [round(duration(p), 3) for p in files], "total_seconds": round(duration(full), 3)}
    manifest["turns"] = [{"turn_id": t["turn_id"], "speaker": t["speaker"], "text": t["text"]} for t in turns]
    (args.out / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
