#!/usr/bin/env python3
"""Check the company-level official-information cache before CNINFO download.

Usage:
  python3 check_archive.py --companies-root outputs/companies \
    --company 东山精密 --ts-code 002384.SZ \
    --period 2026H1 --document-type semiannual-report

Exit codes: 0 = reusable file found, 1 = missing, 2 = usage/path error.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--companies-root", type=Path, required=True)
    parser.add_argument("--company", required=True)
    parser.add_argument("--ts-code", required=True)
    parser.add_argument("--period", required=True)
    parser.add_argument("--document-type", required=True)
    args = parser.parse_args()

    company_dir = args.companies_root / args.company / "official-information"
    if not args.companies_root.is_dir():
        print(f"ERROR companies root not found: {args.companies_root}", file=sys.stderr)
        return 2
    if not company_dir.is_dir():
        print(json.dumps({"status": "missing", "directory": str(company_dir)}, ensure_ascii=False))
        return 1

    prefix = f"{args.ts_code}_{args.period}_{args.document_type}_"
    matches = sorted(
        path for path in company_dir.glob(f"{prefix}*.pdf")
        if path.is_file() and path.stat().st_size > 0
    )
    if matches:
        print(json.dumps({"status": "reusable", "path": str(matches[0]), "size": matches[0].stat().st_size}, ensure_ascii=False))
        return 0

    record = company_dir / "download_record.json"
    if record.is_file():
        try:
            data = json.loads(record.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            print(f"ERROR invalid download_record.json: {exc}", file=sys.stderr)
            return 2
        for document in data.get("documents", []):
            if document.get("stock_code") != args.ts_code or document.get("report_period") != args.period:
                continue
            filename = document.get("local_filename", "")
            if args.document_type not in filename:
                continue
            candidate = company_dir / filename
            if candidate.is_file() and candidate.stat().st_size > 0:
                print(json.dumps({"status": "reusable", "path": str(candidate), "size": candidate.stat().st_size, "source": "download_record.json"}, ensure_ascii=False))
                return 0

    print(json.dumps({"status": "missing", "directory": str(company_dir), "expected_prefix": prefix}, ensure_ascii=False))
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
