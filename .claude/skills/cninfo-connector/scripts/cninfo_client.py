#!/usr/bin/env python3
"""巨潮资讯（cninfo.com.cn）公告/年报轻量客户端（investment-research-system 文本层）。

巨潮为证监会指定法定披露平台，公开接口无需凭证。本客户端为 cnfinancialscraper
cninfo_scraper 的 orgId 硬编码 bug 的适配层（深市 orgId=gssz+代码，沪市 gssh+代码）。

用法（CLI）：
  python3 cninfo_client.py search <代码> [关键词] [起始日期] [结束日期]
     例：python3 cninfo_client.py search 000938 年报 2025-01-01 2026-08-09
  python3 cninfo_client.py download <公告ID> <adjunctUrl> <输出目录> [canonical文件名]

用法（库）：
  from cninfo_client import search_announcements, download_pdf
  items = search_announcements("000938", keyword="年报")
"""
import json
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import requests

CNINFO_QUERY = "http://www.cninfo.com.cn/new/hisAnnouncement/query"
CNINFO_DOWNLOAD = "http://static.cninfo.com.cn/"


def _org_id(ts_code: str) -> str:
    """深市 gssz0000938 / 沪市 gssh600519；代码如 000938.SZ / 600519.SH。"""
    code = ts_code.split(".")[0]
    market = "sz" if ts_code.upper().endswith("SZ") else "sh"
    return f"gs{market}0{code}"


def search_announcements(
    ts_code: str,
    keyword: str = "",
    start_date: str = "2020-01-01",
    end_date: str = "",
    page_size: int = 30,
    max_pages: int = 3,
) -> List[dict]:
    """按股票代码+关键词搜索公告。返回结构化列表（含 announcementId/adjunctUrl/title）。"""
    end_date = end_date or datetime.now().strftime("%Y-%m-%d")
    stock = f"{ts_code.split('.')[0]},{_org_id(ts_code)}"
    results = []
    for page in range(1, max_pages + 1):
        resp = requests.post(
            CNINFO_QUERY,
            data={
                "pageNum": page, "pageSize": page_size,
                "column": "szse" if ts_code.upper().endswith("SZ") else "sse",
                "tabName": "fulltext", "plate": "", "stock": stock,
                "searchkey": keyword, "secid": "", "category": "", "trade": "",
                "seDate": f"{start_date}~{end_date}",
                "sortName": "", "sortType": "", "isHLtitle": "true",
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=30,
        )
        resp.raise_for_status()
        body = resp.json()
        anns = body.get("announcements") or []
        results.extend(anns)
        if not body.get("hasMore") or not anns:
            break
        time.sleep(1.5)  # 巨潮限速要求
    return results


def canonical_filename(ts_code: str, period: str, document_type: str, announcement_date: str) -> str:
    """Return the shared company-level official-information filename."""
    date = announcement_date.replace("-", "")
    return f"{ts_code.upper()}_{period}_{document_type}_{date}.pdf"


def download_pdf(announcement_id: str, adjunct_url: str, output_dir: str, filename: Optional[str] = None) -> Optional[str]:
    """下载公告 PDF 到输出目录；filename 应使用 canonical 文件名。"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    local = Path(output_dir) / (filename or f"{announcement_id}.pdf")
    if local.exists() and local.stat().st_size > 0:
        return str(local)
    url = CNINFO_DOWNLOAD + adjunct_url.lstrip("/")
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    local.write_bytes(resp.content)
    return str(local) if local.stat().st_size > 0 else None


def main() -> None:
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    cmd = sys.argv[1]
    if cmd == "search":
        code = sys.argv[2]
        keyword = sys.argv[3] if len(sys.argv) > 3 else ""
        start = sys.argv[4] if len(sys.argv) > 4 else "2020-01-01"
        end = sys.argv[5] if len(sys.argv) > 5 else ""
        items = search_announcements(code, keyword, start, end)
        print(f"共 {len(items)} 条")
        for ann in items:
            print(f"  [{ann.get('announcementTime','')}] {ann.get('announcementTitle','')[:60]} | id={ann.get('announcementId')}")
    elif cmd == "download":
        aid, url, out = sys.argv[2], sys.argv[3], sys.argv[4]
        filename = sys.argv[5] if len(sys.argv) > 5 else None
        path = download_pdf(aid, url, out, filename)
        print(path or "下载失败")


if __name__ == "__main__":
    main()
