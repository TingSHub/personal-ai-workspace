#!/usr/bin/env python3
"""Build read-only A/B manifests for CosyVoice style-control experiments."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--episode", type=Path, required=True)
    parser.add_argument("--outdir", type=Path, required=True)
    args = parser.parse_args()
    source = json.loads(args.episode.read_text(encoding="utf-8"))
    args.outdir.mkdir(parents=True, exist_ok=True)
    for name, instruction in {
        "02-weak-instruct": "Use a natural, restrained conversational podcast delivery in Mandarin. Keep the pacing calm and avoid exaggerated emotion.<|endofprompt|>",
        "03-current-instruct": None,
    }.items():
        manifest = json.loads(json.dumps(source, ensure_ascii=False))
        if instruction:
            for turn in manifest["turns"]:
                turn["style_instruction"] = instruction
        (args.outdir / f"{name}.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"PASS manifests={args.outdir}")


if __name__ == "__main__":
    main()
