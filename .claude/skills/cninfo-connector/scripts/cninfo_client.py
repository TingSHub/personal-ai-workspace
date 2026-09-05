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
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Optional

import requests

CNINFO_QUERY = "http://www.cninfo.com.cn/new/hisAnnouncement/query"
CNINFO_DOWNLOAD = "http://static.cninfo.com.cn/"
SSE_QUERY = "https://query.sse.com.cn/security/stock/queryCompanyBulletin.do"
SSE_DOWNLOAD = "https://www.sse.com.cn"
SZSE_QUERY = "https://www.szse.cn/api/disc/announcement/annList"
SZSE_DOWNLOAD = "https://disc.static.szse.cn/download"


def _org_id(ts_code: str) -> str:
    """深市 gssz0000938 / 沪市 gssh600519；代码如 000938.SZ / 600519.SH。"""
    code = ts_code.split(".")[0]
    market = "sz" if ts_code.upper().endswith("SZ") else "sh"
    return f"gs{market}0{code}"


def _search_cninfo(
    ts_code: str,
    keyword: str = "",
    start_date: str = "2020-01-01",
    end_date: str = "",
    page_size: int = 30,
    max_pages: int = 3,
) -> List[dict]:
    """Primary CNINFO query."""
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
        for ann in anns:
            ann.setdefault("source", "cninfo")
        results.extend(anns)
        if not body.get("hasMore") or not anns:
            break
        time.sleep(1.5)  # 巨潮限速要求
    return results


def _clean_title(value: str) -> str:
    return re.sub(r"<[^>]+>", "", value or "").strip()


def _search_sse(ts_code: str, keyword: str, start_date: str, end_date: str) -> List[dict]:
    """Official SSE fallback for Shanghai-listed securities."""
    code = ts_code.split(".")[0]
    params = {
        "jsonCallBack": "jsonpCallback", "isPagination": "true", "productId": code,
        "keyWord": keyword, "securityType": "0101,120100,020100,020200,120200",
        "reportType2": "", "reportType": "ALL", "beginDate": start_date,
        "endDate": end_date, "pageHelp.pageSize": "30", "pageHelp.pageCount": "50",
        "pageHelp.pageNo": "1", "pageHelp.beginPage": "1", "pageHelp.cacheSize": "1",
        "pageHelp.endPage": "5", "_": str(int(time.time() * 1000)),
    }
    resp = requests.get(SSE_QUERY, params=params,
                        headers={"Referer": "https://www.sse.com.cn/"}, timeout=30)
    resp.raise_for_status()
    raw = resp.text
    payload = raw[raw.find("(") + 1:raw.rfind(")")]
    body = json.loads(payload)
    rows = (body.get("pageHelp") or {}).get("data") or []
    results = []
    for row in rows:
        title = _clean_title(row.get("TITLE") or row.get("title") or "")
        publish_date = (row.get("SSEDATE") or row.get("ADDDATE") or "")[:10]
        url = row.get("URL") or ""
        if keyword and keyword.lower() not in title.lower():
            continue
        stable_id = row.get("file_Serial") or url.rsplit("/", 1)[-1] or f"{code}-{publish_date}-{title}"
        results.append({
            "announcementId": f"sse:{stable_id}", "announcementTitle": title,
            "adjunctUrl": SSE_DOWNLOAD + url if url.startswith("/") else url,
            "publishDate": publish_date, "announcementTime": row.get("ADDDATE", ""),
            "source": "sse", "exchange": "SSE", "stockCode": code,
        })
    return results


def _search_szse(ts_code: str, keyword: str, start_date: str, end_date: str,
                 max_pages: int = 5) -> List[dict]:
    """Official SZSE fallback for Shenzhen-listed securities."""
    code = ts_code.split(".")[0]
    results = []
    for page in range(1, max_pages + 1):
        resp = requests.post(
            SZSE_QUERY,
            json={"channelCode": ["listedNotice_disc"], "pageSize": 20,
                  "pageNum": page, "stock": [code]},
            headers={"Content-Type": "application/json", "Referer": "https://www.szse.cn/"},
            timeout=30,
        )
        resp.raise_for_status()
        rows = resp.json().get("data") or []
        if not rows:
            break
        for row in rows:
            title = _clean_title(row.get("title") or "")
            publish_date = (row.get("publishTime") or "")[:10]
            if publish_date and (publish_date < start_date or publish_date > end_date):
                continue
            if keyword and keyword.lower() not in title.lower():
                continue
            attach_path = row.get("attachPath") or ""
            results.append({
                "announcementId": f"szse:{row.get('annId') or row.get('id') or attach_path}",
                "announcementTitle": title,
                "adjunctUrl": SZSE_DOWNLOAD + attach_path if attach_path.startswith("/") else attach_path,
                "publishDate": publish_date, "announcementTime": row.get("publishTime", ""),
                "source": "szse", "exchange": "SZSE", "stockCode": code,
            })
        if len(rows) < 20:
            break
    return results


def search_announcements(
    ts_code: str, keyword: str = "", start_date: str = "2020-01-01",
    end_date: str = "", page_size: int = 30, max_pages: int = 3,
) -> List[dict]:
    """Search CNINFO first, then the corresponding official exchange endpoint if empty."""
    end_date = end_date or datetime.now().strftime("%Y-%m-%d")
    try:
        results = _search_cninfo(ts_code, keyword, start_date, end_date, page_size, max_pages)
    except requests.RequestException:
        results = []
    if results:
        return results
    if ts_code.upper().endswith("SZ"):
        return _search_szse(ts_code, keyword, start_date, end_date)
    return _search_sse(ts_code, keyword, start_date, end_date)


def canonical_filename(ts_code: str, period: str, document_type: str, announcement_date: str) -> str:
    """Return the shared company-level official-information filename."""
    date = announcement_date.replace("-", "")
    return f"{ts_code.upper()}_{period}_{document_type}_{date}.pdf"


def download_pdf(announcement_id: str, adjunct_url: str, output_dir: str, filename: Optional[str] = None) -> Optional[str]:
    """下载公告 PDF 到输出目录；filename 应使用 canonical 文件名。"""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    safe_id = re.sub(r"[^A-Za-z0-9._-]+", "_", announcement_id)
    local = Path(output_dir) / (filename or f"{safe_id}.pdf")
    if local.exists() and local.stat().st_size > 0:
        return str(local)
    url = adjunct_url if adjunct_url.startswith(("http://", "https://")) else CNINFO_DOWNLOAD + adjunct_url.lstrip("/")
    resp = requests.get(url, timeout=60)
    resp.raise_for_status()
    if not resp.content.startswith(b"%PDF-"):
        raise ValueError(f"下载内容不是 PDF，可能触发交易所反爬页面: {url}")
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
        source = items[0].get("source", "cninfo") if items else "none"
        print(f"共 {len(items)} 条（来源: {source}）")
        for ann in items:
            print(f"  [{ann.get('announcementTime','')}] {ann.get('announcementTitle','')[:60]} | id={ann.get('announcementId')} | url={ann.get('adjunctUrl','')}")
    elif cmd == "download":
        aid, url, out = sys.argv[2], sys.argv[3], sys.argv[4]
        filename = sys.argv[5] if len(sys.argv) > 5 else None
        path = download_pdf(aid, url, out, filename)
        print(path or "下载失败")


if __name__ == "__main__":
    main()
