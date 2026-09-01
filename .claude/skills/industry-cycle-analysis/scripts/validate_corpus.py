#!/usr/bin/env python3
"""Audit a directory of industry reports as one corpus.

The report validator answers "is this file structurally valid?".  This audit
answers the complementary questions that only become visible across files:
whether prose is being recycled, whether nodes carry enough information, and
whether evidence is sufficiently diverse relative to the semiconductor
benchmark.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from validate_report import (
    extract_node_blocks,
    node_field,
    markdown_tables,
    normalize_text,
    representative_company_rows,
    section,
    table_rows,
    validate,
)


STRUCTURED_FIELDS = ("what", "suppliers", "buyers", "money", "bottleneck", "advanced")
FIXED_PROSE_PREFIXES = (
    "分析日期",
    "地理范围",
    "数据时效",
    "行业边界",
    "免责声明",
    "本报告不构成",
)


@dataclass(frozen=True)
class ReportMetrics:
    nodes: int
    average_node_chars: float
    company_rows: int
    advanced_blocks: int
    evidence_rows: int
    publishers: int
    source_urls: int


def _ledger(text: str) -> str:
    return section(text, "## 附录A 证据台账") or section(text, "## 10. 证据台账")


def report_metrics(text: str) -> ReportMetrics:
    chain = section(text, "## 1. 产业链地图")
    nodes = extract_node_blocks(chain)
    structured_lengths: list[int] = []
    companies = 0
    for _, block in nodes:
        structured_lengths.append(
            sum(len(normalize_text(node_field(block, key))) for key in STRUCTURED_FIELDS)
        )
        companies += len(representative_company_rows(block))

    ledger = _ledger(text)
    rows = table_rows(ledger)
    evidence_rows = len(re.findall(r"^\|\s*E\d+\s*\|", ledger, re.MULTILINE))
    publishers: set[str] = set()
    if rows:
        headers = rows[0]
        publisher_header = "发布方" if "发布方" in headers else "Publisher"
        if publisher_header in headers:
            publisher_index = headers.index(publisher_header)
            publishers = {
                row[publisher_index].strip()
                for row in rows[1:]
                if len(row) > publisher_index and row[publisher_index].strip()
            }

    return ReportMetrics(
        nodes=len(nodes),
        average_node_chars=(sum(structured_lengths) / len(nodes)) if nodes else 0.0,
        company_rows=companies,
        advanced_blocks=len(re.findall(r"\*\*进阶视角\*\*", text)),
        evidence_rows=evidence_rows,
        publishers=len(publishers),
        source_urls=len(set(re.findall(r"https?://[^)\s|>]+", text))),
    )


def reusable_prose(text: str) -> set[str]:
    """Return substantive prose units that should not be identical across reports."""
    prose: set[str] = set()
    for raw in text.splitlines():
        line = raw.strip()
        if (
            not line
            or line.startswith(("#", "|", "```", "- [", "<!--"))
            or any(line.startswith(prefix) for prefix in FIXED_PROSE_PREFIXES)
        ):
            continue
        line = re.sub(r"^[-*+]\s+", "", line)
        line = re.sub(r"\bE\d+\b", "E#", line)
        for sentence in re.split(r"(?<=[。！？；])", line):
            normalized = normalize_text(sentence)
            if len(normalized) >= 36:
                prose.add(normalized)
    return prose


def audit(
    reports: list[Path], benchmark: Path | None, strict: bool
) -> tuple[list[str], list[str], dict[Path, ReportMetrics]]:
    errors: list[str] = []
    warnings: list[str] = []
    metrics: dict[Path, ReportMetrics] = {}
    prose_owners: defaultdict[str, list[Path]] = defaultdict(list)
    timeline_owners: defaultdict[tuple[str, ...], list[Path]] = defaultdict(list)

    benchmark_average = 0.0
    if benchmark:
        benchmark_average = report_metrics(benchmark.read_text(encoding="utf-8")).average_node_chars
        if benchmark_average <= 0:
            errors.append(f"benchmark has no parseable structured nodes: {benchmark}")

    for report in reports:
        text = report.read_text(encoding="utf-8")
        report_errors, report_warnings = validate(text, "full", strict)
        errors.extend(f"{report.name}: {item}" for item in report_errors)
        warnings.extend(f"{report.name}: {item}" for item in report_warnings)

        current = report_metrics(text)
        metrics[report] = current
        if current.average_node_chars < 200:
            errors.append(
                f"{report.name}: average structured node information is "
                f"{current.average_node_chars:.1f} chars; expected at least 200"
            )
        if benchmark_average and current.average_node_chars < benchmark_average * 0.65:
            errors.append(
                f"{report.name}: structured-node depth is only "
                f"{current.average_node_chars / benchmark_average:.0%} of benchmark; expected at least 65%"
            )
        for sentence in reusable_prose(text):
            prose_owners[sentence].append(report)
        cycle = section(text, "## 5. 周期位置与传导")
        timeline_tables = [
            rows for rows in markdown_tables(cycle)
            if rows and any("阶段" in cell or "日期" in cell for cell in rows[0])
        ]
        if timeline_tables:
            periods = tuple(normalize_text(row[0]) for row in timeline_tables[0][1:] if row)
            if periods:
                timeline_owners[periods].append(report)

    for sentence, owners in prose_owners.items():
        unique_owners = sorted({owner.name for owner in owners})
        if len(unique_owners) >= 2:
            errors.append(
                "cross-report repeated prose in "
                f"{', '.join(unique_owners)}: {sentence[:64]}..."
            )

    for periods, owners in timeline_owners.items():
        unique_owners = sorted({owner.name for owner in owners})
        if len(unique_owners) >= 2:
            errors.append(
                "cross-report repeated cycle timeline in "
                f"{', '.join(unique_owners)}: {', '.join(periods)}"
            )

    return errors, warnings, metrics


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("reports_directory", type=Path)
    parser.add_argument("--pattern", default="??_*.md")
    parser.add_argument("--benchmark", type=Path)
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    reports = sorted(args.reports_directory.glob(args.pattern))
    if not reports:
        print(f"ERROR: no reports matched {args.pattern!r} in {args.reports_directory}")
        return 1

    errors, warnings, metrics = audit(reports, args.benchmark, args.strict)
    for report, current in metrics.items():
        print(
            f"METRIC: {report.name}: nodes={current.nodes}, "
            f"avg_node_chars={current.average_node_chars:.1f}, companies={current.company_rows}, "
            f"advanced={current.advanced_blocks}, evidence={current.evidence_rows}, "
            f"publishers={current.publishers}, urls={current.source_urls}"
        )
    for item in warnings:
        print(f"WARNING: {item}")
    for item in errors:
        print(f"ERROR: {item}")

    if errors or (args.strict and warnings):
        print(f"Corpus validation failed: {len(errors)} error(s), {len(warnings)} warning(s).")
        return 1
    print(f"Corpus validation passed: {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
