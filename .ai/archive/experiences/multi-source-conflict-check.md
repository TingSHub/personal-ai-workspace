# Experience: multi-source-conflict-check

## 来源证据

- 项目：investment-research-html-mvp（2026-08-16 运行，贵州茅台 600519）
- 运行记录：`logs/run-20260816-workflow-v1.md`（冲突检查：12 项已裁决、6 项未裁决）；`outputs/companies/贵州茅台/2026-08-16/conflict-check/unresolved-conflicts.md`
- 相关资源 installed_ref：investagent（tree-sha256:51aa7c2823bd）、industry-analysis（tree-sha256:a2a363fca3d9）、industry-cycle-analysis（tree-sha256:9e9b5dd25f8e）

## 触发场景

- 多研究 Skill 并行产出同一公司/行业数据后，进入统一 HTML/内容呈现前
- 任何「多源数据必须合并呈现且不允许编造」的内容生产链路

## 问题与归属判定

- 问题：三个成熟 Skill 独立研究同一对象必然产生口径冲突（本次 12 项），若不做裁决直接拼入页面会出现数字自相矛盾（如 2025 营收 1720.5 vs 1688.4、Q2 单季 367.9 vs 375.75、每股分红 27.993 vs 51.98）；部分冲突（社会库存三种口径、经销商数量 -261 vs -46）无法裁决，若强行入页会误导读者。
- 归属（owner）：investagent-html-report-v0.1 workflow SOP Phase 2（Quality Criteria/Known Issues）；html-ppt-skill 记录辅助脚本（数值一致性检查脚本）

## 可复用结论（resolution）

- **裁决优先级**：一手来源（公司公告/财报/官方统计）> 券商调研 > 媒体转引 > 推算；「已裁决（含口径差异标注）」才允许进入 HTML。
- **算术自洽校验是最强裁决工具**：Q2 单季 = H1 − Q1 减法验证（367.9 与中报合计矛盾 → 采用 375.75）；分红率 × 净利 ÷ 股本 ≈ 每股分红（51.98 三方自洽 → 27.993 判定为单期口径）。
- **口径分层呈现**：营业收入 vs 营业总收入、个股 PE vs 指数 PE、A 股上市公司 vs 全国规上统计、样本不同的机构预期——各自标注口径而非强行统一。
- **无法裁决即不进入 HTML**：记录到 unresolved-conflicts.md，风险描述改定性表述（如社会库存规模不呈现数字）。
- **脚本化**：HTML 生成后必须跑数值一致性检查（`html-ppt-skill/scripts/check-numbers.py`，期望值来自裁决后的数据清单）——手工 SVG 坐标换算必然引入转录错误。

## 回写目标

- investagent-html-report-v0.1 workflow SOP Phase 2 Quality Criteria / Known Issues（已随 v0.1 写入）
- html-ppt-skill 记录「辅助脚本」行登记 check-numbers.py（随脚本沉淀同步完成）

## 适用范围

- 多源研究 → 统一内容呈现的链路（本 workflow 及类似内容生产流程）
- 数据均来自真实接口/披露时；裁决依赖可复算的公开数字

## 不适用范围

- 单源研究链路（无冲突可裁决）
- 数据本身不可复算（无一手来源可查）时——此类数字直接归入未裁决，不强行裁决

## 关联资产

- investagent-html-report-v0.1（Workflow by-name）
- html-ppt-skill（脚本归属资源）
- unresolved-conflicts.md（本项目冲突检查产出物）
