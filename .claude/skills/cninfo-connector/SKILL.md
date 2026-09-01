---
name: cninfo-connector
description: 巨潮资讯（cninfo.com.cn）公告/年报数据连接器（workspace 共享 internal skill）——动态 orgId 构造，按代码+关键词搜索法定披露公告并下载 PDF。当任何项目需要获取 A股年报/半年报/季报/公告 PDF 时使用。
---

# cninfo-connector

workspace 级共享数据连接器：巨潮资讯（证监会指定法定披露平台）公告/年报获取，公开接口无需凭证。

## 为什么存在

- cnfinancialscraper 的 cninfo_scraper 存在 orgId 硬编码 bug（部分代码映射错误，如 000938→9900013389）
- 本连接器动态构造 orgId（深市 `gssz0<code>` / 沪市 `gssh0<code>`），规避该 bug
- 跨项目复用：所有项目通过本 skill 获取年报/公告，一处维护

## 用法

CLI：
```bash
python3 <skill_dir>/scripts/cninfo_client.py search <代码> [关键词] [起始日期] [结束日期]
# 例：python3 .../cninfo_client.py search 000938.SZ 年度报告 2025-01-01 2026-08-09
python3 <skill_dir>/scripts/cninfo_client.py download <公告ID> <adjunctUrl> <输出目录> [canonical文件名]
```

库：
```python
import sys; sys.path.insert(0, "<skill_dir>/scripts")
from cninfo_client import search_announcements, download_pdf
items = search_announcements("000938.SZ", keyword="年度报告", start_date="2025-01-01")
path = download_pdf(items[0]["announcementId"], items[0]["adjunctUrl"], "artifacts/data")
```

## 注意

- 巨潮查询 pageSize ≤ 30，调用间隔 ≥ 1.5s（限速要求）
- 关键词用"年度报告"可精确匹配年报（"年报"会命中制度类文件）
- 返回字段：announcementId / announcementTitle / adjunctUrl / publishDate
- PDF 下载为 `static.cninfo.com.cn` + adjunctUrl

## 公司级归档契约

- 官方原件统一放在 `outputs/companies/{company}/official-information/`，不带研究日期；同行公司使用同级公司目录。
- 文件名统一为 `{ts_code}_{period}_{document_type}_{announcement_date}.pdf`。
- `period` 使用 `YYYYQ1`、`YYYYQ2`、`YYYYH1`、`YYYYFY`；`document_type` 使用 `quarterly-report`、`semiannual-report`、`annual-report` 或固定公告 slug。
- 下载前先运行 `scripts/check_archive.py` 检查本地缓存和 `download_record.json`；已存在且正文可验证时直接复用，不重复下载。
- 研究 run 只引用公司级原件，不复制到当前 run 目录；下载记录必须保留公告 ID、来源 URL、路径、大小和文本验证状态。

## Validation（操作后必须执行）

- search 输出含 `announcementId` 且目标报告（年报/半年报）命中
- download 返回的本地文件存在且 > 0 字节
- archive check 对已存在报告返回 exit 0，对缺失报告返回 exit 1
