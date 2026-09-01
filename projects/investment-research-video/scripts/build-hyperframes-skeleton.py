#!/usr/bin/env python3
"""Build a HyperFrames Composition Skeleton from an accepted Presentation HTML.

The source deck remains the visual/content baseline. This adapter removes the
interactive presenter runtime, adds HyperFrames timing contracts to each Scene,
and creates one deterministic paused GSAP timeline. Real durations are supplied
later from segments.json; subtitles are supplied from narration.srt.
"""

from __future__ import annotations

import argparse
import html
import json
import re
from pathlib import Path


def balanced_deck(source: str) -> str:
    start = source.find('<div class="deck">')
    if start < 0:
        raise ValueError("source Presentation has no .deck root")

    tag_re = re.compile(r"</?div\b[^>]*>", re.I)
    depth = 0
    for match in tag_re.finditer(source, start):
        tag = match.group(0)
        if tag.startswith("</"):
            depth -= 1
            if depth == 0:
                return source[start : match.end()]
        elif not tag.rstrip().endswith("/>"):
            depth += 1
    raise ValueError("could not find balanced .deck root")


def first_style(source: str) -> str:
    match = re.search(r"<style\b[^>]*>(.*?)</style>", source, re.I | re.S)
    if not match:
        raise ValueError("source Presentation has no inline style")
    return match.group(1)


def load_segments(path: Path | None, scene_count: int, nominal: float) -> tuple[list[dict], float]:
    if path is None:
        segments = [
            {"page": i, "start": round((i - 1) * nominal, 3), "duration": nominal}
            for i in range(1, scene_count + 1)
        ]
        return segments, round(scene_count * nominal, 3)

    payload = json.loads(path.read_text(encoding="utf-8"))
    segments = payload.get("segments", [])
    if len(segments) != scene_count:
        raise ValueError(f"segments count {len(segments)} != scene count {scene_count}")
    normalized = []
    cursor = 0.0
    for i, item in enumerate(segments, 1):
        duration = float(item["duration"])
        normalized.append({
            "page": int(item.get("page", i)),
            "start": round(cursor, 3),
            "duration": round(duration, 3),
            "end": round(cursor + duration, 3),
        })
        cursor += duration
    return normalized, round(cursor, 3)


def parse_srt(path: Path | None) -> list[dict]:
    if path is None or not path.is_file():
        return []
    blocks = []
    for raw in re.split(r"\n\s*\n", path.read_text(encoding="utf-8").strip()):
        lines = [line.strip("\ufeff") for line in raw.splitlines() if line.strip()]
        if len(lines) < 3 or "-->" not in lines[1]:
            continue
        start, end = [x.strip() for x in lines[1].split("-->", 1)]
        blocks.append({"index": int(lines[0]), "start": srt_time(start), "end": srt_time(end), "text": " ".join(lines[2:])})
    return blocks


def srt_time(value: str) -> float:
    hms, millis = value.replace(",", ".").split(".", 1)
    hours, minutes, seconds = [float(x) for x in hms.split(":")]
    return hours * 3600 + minutes * 60 + seconds + float(f"0.{millis}")


def caption_chunks(text: str, start: float, end: float, max_chars: int = 26) -> list[dict]:
    compact = re.sub(r"\s+", " ", text).strip()
    if not compact:
        return []
    parts = []
    for sentence in re.split(r"(?<=[。！？；])", compact):
        sentence = sentence.strip()
        if not sentence:
            continue
        while len(sentence) > max_chars:
            cut = max_chars
            for boundary in "，、：；, ":
                candidate = sentence.rfind(boundary, 0, max_chars + 1)
                if candidate >= max_chars // 2:
                    cut = candidate + 1
                    break
            parts.append(sentence[:cut].strip())
            sentence = sentence[cut:].strip()
        if sentence:
            parts.append(sentence)
    total_chars = max(1, sum(len(part) for part in parts))
    duration = max(0.1, end - start)
    cursor = start
    chunks = []
    for index, part in enumerate(parts):
        if index == len(parts) - 1:
            chunk_end = end
        else:
            chunk_end = cursor + duration * len(part) / total_chars
        chunks.append({"start": round(cursor, 3), "end": round(chunk_end, 3), "text": part})
        cursor = chunk_end
    return chunks


def transform_slides(deck: str, segments: list[dict]) -> tuple[str, int]:
    section_re = re.compile(
        r'(<section\b(?=[^>]*\bclass="[^"]*\bslide\b[^"]*")[^>]*>)(.*?)(</section>)',
        re.I | re.S,
    )
    count = 0

    def replace(match: re.Match[str]) -> str:
        nonlocal count
        count += 1
        if count > len(segments):
            raise ValueError("more slides than segments")
        segment = segments[count - 1]
        scene_id = f"scene-{count:02d}"
        tag = re.sub(r'class="[^"]*"', 'class="slide"', match.group(1), count=1)
        tag = tag.replace("<section", f'<section id="{scene_id}"', 1)
        body = match.group(2)

        def add_cue(local_match: re.Match[str]) -> str:
            local_tag = local_match.group(0)
            if "data-cue=" in local_tag:
                return local_tag
            stage = re.search(r'data-stage="(\d+)"', local_tag)
            stage_id = stage.group(1) if stage else "0"
            return local_tag[:-1] + f' data-cue="{scene_id}-stage-{stage_id}">'

        body = re.sub(
            r'<(?:p|h1|h2|div|svg|table|section)\b[^>]*data-stage="\d+"[^>]*>',
            add_cue,
            body,
            flags=re.I | re.S,
        )
        body = body.replace(
            '<p class="meta-line"',
            '<p class="meta-line" data-layout-allow-overlap data-layout-allow-occlusion',
            1,
        )
        body = body.replace(
            '<p class="page-sub"',
            '<p class="page-sub" data-layout-allow-occlusion',
            1,
        )
        return (
            f'<div id="{scene_id}-clip" class="clip scene-clip" '
            f'data-start="{segment["start"]:.3f}" data-duration="{segment["duration"]:.3f}" '
            f'data-track-index="{count}">{tag}{body}{match.group(3)}</div>'
        )

    transformed = section_re.sub(replace, deck)
    if count != len(segments):
        raise ValueError(f"slide count {count} != segments count {len(segments)}")

    return transformed, count


def build_html(source: Path, outdir: Path, segments_path: Path | None, srt_path: Path | None, composition_id: str, nominal: float) -> None:
    source_text = source.read_text(encoding="utf-8")
    deck = balanced_deck(source_text)
    style = first_style(source_text)
    slide_count = len(re.findall(r'<section\b[^>]*\bclass="[^"]*\bslide\b[^"]*"', deck, flags=re.I | re.S))
    segments, total = load_segments(segments_path, slide_count, nominal)
    deck, _ = transform_slides(deck, segments)
    srt_blocks = parse_srt(srt_path)
    captions = []
    for block in srt_blocks:
        captions.extend(caption_chunks(block["text"], block["start"], block["end"]))
    caption_html = "\n".join(
        f'<div id="subtitle-{index:03d}" class="clip hf-subtitle" data-layout-allow-overlap data-layout-allow-occlusion '
        f'data-start="{item["start"]:.3f}" '
        f'data-duration="{max(0.05, item["end"] - item["start"]):.3f}" data-track-index="80">'
        f'{html.escape(item["text"])}</div>'
        for index, item in enumerate(captions, 1)
    )
    audio_html = ""
    if segments_path is not None:
        audio_html = (
            f'<audio id="narration" class="clip audio-track" src="assets/narration-full.mp3" '
            f'data-start="0" data-duration="{total:.3f}" data-track-index="90" data-volume="1"></audio>'
        )

    style_extra = f"""
html,body {{ width:1920px; height:1080px; margin:0; overflow:hidden; background:#faf7f1; }}
#root {{ position:relative; width:1920px; height:1080px; overflow:hidden; background:#faf7f1; }}
#root > .deck {{ width:1920px !important; height:1080px !important; position:relative !important; overflow:hidden !important; }}
#root .scene-clip {{ position:absolute; inset:0; overflow:hidden; }}
#root .slide {{ opacity:1; transform:none !important; transition:none !important; pointer-events:auto !important; }}
#root [data-stage] {{ animation:none !important; opacity:1 !important; filter:none !important; clip-path:none !important; transition:none !important; }}
#root .notes, #root .presenter-ui, #root #stage {{ display:none !important; }}
.hf-subtitle {{ position:absolute; left:96px; right:96px; bottom:58px; z-index:200; min-height:42px; padding:6px 24px 7px; border-left:4px solid #a6192e; background:rgba(33,29,24,.90); color:#fffdf8; font:600 20px/1.35 system-ui,-apple-system,"PingFang SC","Microsoft YaHei",sans-serif; text-align:center; letter-spacing:.01em; }}
.slide .callout, .slide .callout-plain {{ margin-bottom:110px; }}
.audio-track {{ display:block; }}
"""
    script = f"""
<script src="node_modules/gsap/dist/gsap.min.js"></script>
<script>
  window.__timelines = window.__timelines || {{}};
  const tl = gsap.timeline({{ paused: true, defaults: {{ ease: 'power2.out' }} }});
  document.querySelectorAll('#root .slide').forEach((scene) => {{
    const sceneClip = scene.closest('.scene-clip');
    const start = Number(sceneClip?.dataset.start || 0);
    scene.querySelectorAll('[data-stage]').forEach((el) => {{
      const stage = Number(el.dataset.stage || 1);
      const local = Math.min(3.2, 0.32 + (stage - 1) * 0.58);
      tl.fromTo(el, {{ opacity: 0 }}, {{ opacity: 1, duration: 0.48 }}, start + local);
    }});
  }});
  window.__timelines['{composition_id}'] = tl;
</script>
"""
    html_doc = f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=1920, height=1080">
<title>贵州茅台 · HyperFrames Composition</title>
<style>{style}\n{style_extra}</style>
</head>
<body>
  <div id="root" data-composition-id="{composition_id}" data-start="0" data-width="1920" data-height="1080" data-duration="{total:.3f}">
    {audio_html}
    {deck}
    {caption_html}
  </div>
  {script}
</body>
</html>
'''
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "index.html").write_text(html_doc, encoding="utf-8")
    manifest = {"composition_id": composition_id, "scene_count": slide_count, "duration": total, "skeleton": segments_path is None, "source": str(source)}
    (outdir / "composition-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {outdir / 'index.html'} · scenes={slide_count} · duration={total:.3f}s · captions={len(captions)}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--presentation-html", type=Path, required=True)
    ap.add_argument("--outdir", type=Path, required=True)
    ap.add_argument("--segments", type=Path)
    ap.add_argument("--srt", type=Path)
    ap.add_argument("--composition-id", default="maotai-report")
    ap.add_argument("--nominal-duration", type=float, default=30.0)
    args = ap.parse_args()
    build_html(args.presentation_html, args.outdir, args.segments, args.srt, args.composition_id, args.nominal_duration)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
