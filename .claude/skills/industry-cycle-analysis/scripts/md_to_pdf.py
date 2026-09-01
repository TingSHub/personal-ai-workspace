#!/usr/bin/env python3
"""Convert a Markdown report to PDF when local dependencies are available."""

from __future__ import annotations

import argparse
import pathlib
import shutil
import subprocess
import sys
import tempfile


def convert_with_markdown_pdf(input_path: pathlib.Path, output_path: pathlib.Path) -> bool:
    try:
        from markdown_pdf import MarkdownPdf, Section
    except ImportError:
        return False

    text = input_path.read_text(encoding="utf-8")
    pdf = MarkdownPdf(toc_level=2)
    pdf.add_section(Section(text, toc=True))
    pdf.save(str(output_path))
    return True


def find_browser() -> pathlib.Path | None:
    candidates = [
        shutil.which("msedge"),
        shutil.which("msedge.exe"),
        shutil.which("chrome"),
        shutil.which("chrome.exe"),
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    ]
    for candidate in candidates:
        if candidate and pathlib.Path(candidate).is_file():
            return pathlib.Path(candidate)
    return None


def convert_with_pandoc_browser(input_path: pathlib.Path, output_path: pathlib.Path) -> bool:
    pandoc = shutil.which("pandoc")
    browser = find_browser()
    if not pandoc or browser is None:
        return False

    css = """
body { font-family: "Microsoft YaHei", "Noto Sans CJK SC", sans-serif; margin: 36px; line-height: 1.65; color: #171717; }
h1, h2, h3 { page-break-after: avoid; }
table { border-collapse: collapse; width: 100%; font-size: 12px; }
th, td { border: 1px solid #cfd4dc; padding: 6px 8px; vertical-align: top; }
pre, code { white-space: pre-wrap; overflow-wrap: anywhere; }
blockquote { margin-left: 0; padding-left: 14px; border-left: 3px solid #9aa4b2; color: #4b5563; }
@page { size: A4; margin: 14mm; }
""".strip()

    with tempfile.TemporaryDirectory(prefix="industry-report-pdf-") as temp_dir:
        temp = pathlib.Path(temp_dir)
        html_path = temp / "report.html"
        css_path = temp / "report.css"
        profile_path = temp / "browser-profile"
        css_path.write_text(css, encoding="utf-8")

        subprocess.run(
            [
                pandoc,
                str(input_path),
                "--from=gfm",
                "--standalone",
                "--metadata",
                f"title={input_path.stem}",
                "--css",
                str(css_path),
                "--output",
                str(html_path),
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=60,
        )
        subprocess.run(
            [
                str(browser),
                "--headless",
                "--disable-gpu",
                "--no-pdf-header-footer",
                f"--user-data-dir={profile_path}",
                f"--print-to-pdf={output_path}",
                html_path.as_uri(),
            ],
            check=True,
            capture_output=True,
            text=True,
            timeout=90,
        )

    return output_path.is_file() and output_path.stat().st_size > 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert Markdown to PDF.")
    parser.add_argument("input", help="Input Markdown file")
    parser.add_argument("output", help="Output PDF file")
    args = parser.parse_args()

    input_path = pathlib.Path(args.input).resolve()
    output_path = pathlib.Path(args.output).resolve()

    if not input_path.exists():
        print(f"Input file does not exist: {input_path}", file=sys.stderr)
        return 2
    if input_path.suffix.lower() not in {".md", ".markdown"}:
        print(f"Input should be a Markdown file: {input_path}", file=sys.stderr)
        return 2

    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        converted = convert_with_markdown_pdf(input_path, output_path)
        if not converted:
            converted = convert_with_pandoc_browser(input_path, output_path)
    except (OSError, subprocess.SubprocessError) as exc:
        print(f"PDF conversion failed: {exc}", file=sys.stderr)
        return 1

    if not converted:
        print(
            "PDF conversion needs either markdown-pdf, or Pandoc plus Edge/Chrome. "
            "The Markdown report remains the primary deliverable.",
            file=sys.stderr,
        )
        return 1

    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
