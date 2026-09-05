#!/usr/bin/env python3
"""Small, isolated test client for Doubao TTS V3 bidirectional WebSocket."""
import argparse
import base64
import gzip
import json
import os
import struct
import subprocess
import uuid
from pathlib import Path

import websocket

ENDPOINT = "wss://openspeech.bytedance.com/api/v3/tts/bidirection"
RESOURCE_ID = "seed-tts-2.0"


def api_key() -> str:
    env = Path(__file__).resolve().parents[3] / ".env"
    if env.is_file():
        for line in env.read_text(encoding="utf-8").splitlines():
            if line.startswith("VOLC_API_KEY="):
                return line.split("=", 1)[1].strip()
    return os.environ.get("VOLC_API_KEY", "")


def frame(event: int, payload: dict, session_id: str | None = None) -> bytes:
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    # protocol header: 4-byte base header, full-client JSON, event flag
    out = bytearray([0x11, 0x14, 0x10, 0x00])
    out += struct.pack(">I", event)
    if session_id is not None:
        sid = session_id.encode()
        out += struct.pack(">I", len(sid)) + sid
    out += struct.pack(">I", len(body)) + body
    return bytes(out)


def parse(data: bytes):
    if len(data) < 8:
        raise RuntimeError(f"short server frame: {len(data)}")
    header_size = (data[0] & 0x0F) * 4
    message_type = (data[1] >> 4) & 0x0F
    flags = data[1] & 0x0F
    serialization = (data[2] >> 4) & 0x0F
    compression = data[2] & 0x0F
    pos = header_size
    event = None
    if flags & 0x03:
        pos += 4
    if flags & 0x04:
        event = struct.unpack(">I", data[pos:pos + 4])[0]
        pos += 4
        # Server events carry an event-id string.
        if event in {50, 51, 52} or event >= 150:
            n = struct.unpack(">I", data[pos:pos + 4])[0]
            pos += 4 + n
    error_code = None
    if message_type == 0x0F:
        error_code = struct.unpack(">I", data[pos:pos + 4])[0]
        pos += 4
    size = struct.unpack(">I", data[pos:pos + 4])[0]
    pos += 4
    payload = data[pos:pos + size]
    if compression == 1:
        payload = gzip.decompress(payload)
    return message_type, serialization, event, error_code, payload


def synthesize(
    text: str,
    voice_id: str,
    out: Path,
    model: str | None = "seed-tts-2.0-standard",
    context_texts: list[str] | None = None,
    speech_rate: int = 0,
) -> dict:
    key = api_key()
    if not key:
        raise RuntimeError("VOLC_API_KEY missing")
    connect_id = str(uuid.uuid4())
    session_id = uuid.uuid4().hex[:12]
    ws = websocket.create_connection(
        ENDPOINT,
        timeout=60,
        header=[f"X-Api-Key: {key}", f"X-Api-Resource-Id: {RESOURCE_ID}",
                f"X-Api-Connect-Id: {connect_id}"],
    )
    chunks = []
    events = []
    try:
        ws.send(frame(1, {"namespace": "BidirectionalTTS"}), opcode=websocket.ABNF.OPCODE_BINARY)
        while True:
            mt, ser, event, err, payload = parse(ws.recv())
            events.append(event)
            if err:
                raise RuntimeError(f"server error {err}: {payload[:500]!r}")
            if event == 50:
                break

        req_params = {
            "speaker": voice_id,
            "audio_params": {
                "format": "mp3",
                "sample_rate": 24000,
                "speech_rate": speech_rate,
            },
        }
        # Doubao 2.0 native voices support context_texts. The docs warn that
        # explicitly setting model for a cloned voice disables this feature,
        # so instruction-based calls omit model unless the caller needs it.
        if model:
            req_params["model"] = model
        if context_texts:
            req_params["context_texts"] = context_texts
        ws.send(frame(100, {"user": {"uid": "codex-doubao-test"}, "event": 100,
        "req_params": req_params},
                       session_id), opcode=websocket.ABNF.OPCODE_BINARY)
        while True:
            mt, ser, event, err, payload = parse(ws.recv())
            events.append(event)
            if err:
                raise RuntimeError(f"server error {err}: {payload[:500]!r}")
            if event == 150:
                break

        ws.send(frame(200, {"user": {"uid": "codex-doubao-test"}, "event": 200,
                            "req_params": {"text": text}}, session_id),
                opcode=websocket.ABNF.OPCODE_BINARY)
        ws.send(frame(102, {}, session_id), opcode=websocket.ABNF.OPCODE_BINARY)
        while True:
            mt, ser, event, err, payload = parse(ws.recv())
            events.append(event)
            if err:
                raise RuntimeError(f"server error {err}: {payload[:500]!r}")
            if mt == 0x0B or ser == 0:
                if payload:
                    chunks.append(payload)
            elif ser == 1 and payload:
                obj = json.loads(payload)
                if obj.get("data"):
                    chunks.append(base64.b64decode(obj["data"]))
            if event == 152:
                break
        out.write_bytes(b"".join(chunks))
    finally:
        try:
            ws.close()
        except Exception:
            pass
    return {"voice_id": voice_id, "model": model, "context_texts": context_texts,
            "speech_rate": speech_rate, "text": text, "file": str(out),
            "bytes": out.stat().st_size, "events": events}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--episode", type=Path, required=True)
    ap.add_argument("--outdir", type=Path, required=True)
    ap.add_argument("--turns", type=int, default=4)
    ap.add_argument("--model", default="seed-tts-2.0-standard",
                    choices=["seed-tts-2.0-standard", "seed-tts-2.0-expressive"])
    args = ap.parse_args()
    data = json.loads(args.episode.read_text(encoding="utf-8"))
    turns = data["turns"][:args.turns]
    args.outdir.mkdir(parents=True, exist_ok=True)
    results = []
    voice_map = {"zhiwei": "zh_female_xiaohe_uranus_bigtts",
                 "shenyan": "zh_male_liufei_uranus_bigtts"}
    for turn in turns:
        out = args.outdir / f"{turn['turn_id']}-{turn['speaker']}.mp3"
        print(f"合成 {turn['turn_id']} {turn['speaker']} -> {voice_map[turn['speaker']]}")
        results.append({**turn, **synthesize(turn["text"], voice_map[turn["speaker"]], out, args.model)})
    concat = args.outdir / "concat.txt"
    concat.write_text("".join(f"file '{Path(x['file']).resolve()}'\n" for x in results), encoding="utf-8")
    full = args.outdir / "doubao-podcast-sample.mp3"
    subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat), "-c", "copy", str(full)], check=True)
    meta = {"endpoint": ENDPOINT, "resource_id": RESOURCE_ID, "turns": results, "audio": str(full)}
    (args.outdir / "manifest.json").write_text(json.dumps(meta, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"完成: {full}")


if __name__ == "__main__":
    main()
