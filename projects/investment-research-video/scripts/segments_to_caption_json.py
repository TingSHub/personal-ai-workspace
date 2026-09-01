#!/usr/bin/env python3
"""Convert measured segments.json into caption_gate.py's acoustic-alignment JSON."""
import argparse, json
from pathlib import Path

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("segments",type=Path); ap.add_argument("output",type=Path); args=ap.parse_args()
    data=json.loads(args.segments.read_text(encoding="utf-8"))
    items=[{"text":f"{s['speaker']}：{s['text']}","start":s['start'],"end":s['end']} for s in data["segments"]]
    args.output.write_text(json.dumps({"items":items},ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"captions={len(items)} duration={data['total_seconds']}")

if __name__ == "__main__": main()
