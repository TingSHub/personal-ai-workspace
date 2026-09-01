# cninfo-connector

> 管理资产：`.ai/skills/cninfo-connector/cninfo-connector.md`；安装实体：`.claude/skills/cninfo-connector/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | internal · workspace internal |
| installed_ref | internal |
| runtime | both |
| 调用入口 | $cninfo-connector |
| 要求 | network |
| 更新 | internal · 在 workspace 源码中评审修改并同步安装实体；验证：本地归档命中测试 + 已知 A 股代码搜索/下载测试 + PDF 正文定位 |
| 辅助脚本 | `scripts/check_archive.py`：下载前检查公司级官方原件缓存和 canonical 文件名 |
| 经验引用 | financial-analysis；financial-report-workflow |

workspace 共享 internal skill：巨潮资讯（cninfo.com.cn）公告/年报获取连接器（动态 orgId）。

## 来源

- internal（workspace 自建，2026-08-09 从 investment-research-system 项目抽离）
- 安装位置：`.claude/skills/cninfo-connector/`（workspace 内，所有项目可见）

## 用途

- 任何项目获取 A股年报/半年报/季报/公告 PDF（法定披露平台，无凭证）
- 规避 cnfinancialscraper 的 orgId 硬编码 bug（动态构造 gssz0<code>/gssh0<code>）

## 公司级归档契约（跨项目通用）

- 官方原件统一归档到 `outputs/companies/{company}/official-information/`，不带研究日期；同行公司使用同级公司目录，不能放进当前公司 run 的子目录。
- 标准文件名：`{ts_code}_{period}_{document_type}_{announcement_date}.pdf`。
- `period` 使用 `YYYYQ1`、`YYYYQ2`、`YYYYH1`、`YYYYFY`；`document_type` 使用 `quarterly-report`、`semiannual-report`、`annual-report` 或固定的公告类型 slug。
- 公告、年报、半年报、季报都进入同一公司级 `official-information/`；研究 run 只保存引用路径和证据定位，不复制原件。
- 下载前必须先运行 `scripts/check_archive.py`，按 `ts_code + period + document_type` 查本地文件和 `download_record.json`；文件非空且公司名、报告期、正文定位可验证时直接复用，禁止重复搜索/下载。
- 新下载记录必须包含：公司名、证券代码、报告期、文件类型、公告日期、公告 ID、来源 URL、本地路径、文件大小和正文校验状态。

## 注意事项与踩坑

- 当前搜索CLI摘要只显示公告ID，下载调用仍需要搜索响应中的 `adjunctUrl`。优先在同一次搜索结果中保留该字段；不得仅凭ID和日期长期依赖人工拼接下载路径。
- 下载返回非空PDF只完成传输验证。后续研究还需确认正文能够检索并定位到页码或段落；运行环境没有PDF文本抽取工具时，应提前选择可解析的官方页面或已有验证的文本抽取路径。
- 历史文件名不符合 canonical 格式时，先在公司级 manifest 建立映射或完成一次可审计迁移，再进入新的 Workflow；不要为同一份报告保留日期 run 副本。

## 辅助脚本

### `scripts/check_archive.py`

- 作用：在搜索和下载前检查公司级官方原件是否已存在。
- 使用：`python3 <skill_dir>/scripts/check_archive.py --companies-root outputs/companies --company 东山精密 --ts-code 002384.SZ --period 2026H1 --document-type semiannual-report`
- 退出码：`0` 已命中可复用文件；`1` 本地缺失，需要进入搜索/下载；`2` 参数或目录错误。

### 补充规则

- 动态 orgId 构造优先（`gssz`/`gssh` + 股票代码），替代旧 cnfinancialscraper 的 orgId 硬编码（如 000938→9900013389 为错误值，正确为 gssz0000938）。
- 东财 search 接口返回非 JSON，公告/年报检索应走巨潮官方接口，不依赖第三方搜索端点。
