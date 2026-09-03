# Global Contract: investagent-podcast-video-by-hyperframes

本文件承载跨 Phase 的稳定契约。执行任一 Phase 前，先读本文件对应章节；Phase 自己的 Quality Criteria 和 Known Issues 仍是该阶段的最终门禁。

## 1. Account assets

- `account-profile/ACCOUNT_PROFILE.md`
- `account-profile/design.md`
- `account-profile/content-policy.md`
- `account-profile/dialogue-policy.md`
- 顶层 `.ai/assets/` 中由 `resource_key` 选择的通用资源
- 当前 Workflow profile，例如 `references/podcast-v1-shenyan.md`
- 账号图形：`account-profile/account/` 下的横版 logo、mark 和 avatar

账号资产先于公司内容；项目只通过 `resource_key` 和 profile 选择资源，不复制资源本体。

## 2. Company-run outputs

- 长期官方原件：`outputs/companies/{company}/official-information/`
- 本次研究：`outputs/companies/{company}/{run_date}/research-materials/`
- 编辑与视频：`outputs/companies/{company}/{run_date}/editorial/`、`podcast/`
- 券商材料：`research-materials/brokerage/`
- 同行比较：`research-materials/peer-comparison/`
- 外部深研：`research-materials/deep-research/`

同行官方原件使用同级公司目录：`outputs/companies/{peer_company}/official-information/`，不放进当前公司 run。

## 3. Official-source archive

- 下载前先查公司级 `official-information/` 和 `download_record.json`；文件非空且公司、报告期、正文可验证时直接复用。
- 标准文件名：`{ts_code}_{period}_{document_type}_{announcement_date}.pdf`。
- 公告、年报、半年报和季报都归档到公司级 `official-information/`，run 只保存引用路径和证据定位。
- 下载记录至少包含代码、公司名、报告期、类型、公告日期、公告 ID、来源 URL、本地路径、文件大小和文本校验状态。

执行细则以 cninfo-connector Skill 为准；这里保留路径和 Workflow 级门禁，避免跨公司运行时误归档。

## 3.1 Free data-source routing and degradation

结构化数据不再绑定单一供应商。按以下顺序路由，并在本次 run 的 `research-materials/data-source-ledger.json` 留下每次调用、字段口径、报告期、返回状态和复核结果：

| 数据用途 | 首选 | 免费回退 | 事实等级 |
|---|---|---|---|
| 年报/半年报/公告原文 | cninfo-connector / 交易所 | 公司投资者关系页面 | 事实主源；必须归档 PDF 或原文定位 |
| 单家公司三表与财务指标 | Tushare（有权限时） | AkShare；再回退 BaoStock | 结构化辅助源；关键数字必须回查官方披露 |
| A 股历史日线 | Tushare daily（120 分可用） | BaoStock；再回退 AkShare | 行情辅助源；记录复权方式和时间戳 |
| 同行统一期财务数据 | Tushare（有权限时） | AkShare/BaoStock 分别取数后交叉核对 | 只有报告期、单位、并表范围一致才可比较 |

Tushare 无权限、token 失效或接口超时不是研究失败；必须进入下一层回退并标记 `degraded=true`。AkShare/BaoStock 的数字不得静默升级为官方披露；若字段语义不一致（例如合并净利润与归母净利润），必须在 ledger 和 findings-summary 中写明，禁止直接横向比较。若三层均无法取得，写明确缺口，不用估算填补。

## 4. Performance contract

- `episode.json` 是事实、对话和角色的锁定输入；`spoken-style-map.json` 保存情绪、delivery、意图和停顿锚点。
- 需要实际改变语速或停顿时，先由 `resolve_pacing_plan.py` 将 emotion、delivery、interaction_type 和 pause anchors 解析为 turn 级 `pacing_plan`；`delivery` 本身不是声学执行参数。稳定生产基线只执行整句级语速和句间停顿。
- `pacing_plan` 由现有 podcast-audio-compiler 执行并写入 `segments.json`、`audio-qa.json`。
- 使用另一个 voice asset 时，必须同步提供对应的 emotion 目录，禁止 reference 与 emotion 静默串用。

## 5. Visual default and reuse

- 默认视觉变体为 `editorial-paper`：暖纸面、衬线标题、深墨正文、红涨绿跌、细线结构和低圆角。
- 公司事实、数字、话题和图表数据必须来自 manifest；生成器不得写死公司品牌色或公司专属内容。
- 第二家公司只替换 manifest 和研究资产，不改 Composition 模板源码。
- 生成视频、音频、截图、PDF 和 HTML 是 run 产物，不进入通用资源层。
- 平台封面是独立 `cover.html` + 4:3 `cover.png` + 3:4 `cover-3x4.png` 产物：复用正片背景和视觉 Token，展示主标题、副标题、公司名/栏目 logo；推荐 PNG 尺寸分别为 1440×1080 和 1080×1440。除非 manifest 显式声明 in-video cover，否则不得挂入正片 timeline，也不得改变音频、字幕或 Composition 的起始时间。
- `episode-input.json` 的 `cover.title`、`cover.subtitle`、`outro` 和每个 topic 的 `short_label` 是唯一内容来源；不存在这些字段时，Phase 2 直接失败，不从历史公司或模板补值。
- 字幕以 `podcast/qa/captions.json` 为唯一显示来源；它由真实 `segments.json` 生成，默认一回合一条 cue、起止时间覆盖该回合真实语音，平台封面不复用字幕时间轴。
- 内容主线由 Phase 1 的 `research-materials/editorial/company-thesis-card.json` 决定：`earnings_led` 仅适用于研究日前 1–2 天发布且经营变化重大的财报；其他情况使用 `company_led`、`industry_led` 或 `event_led`，财报作为验证或辅助章节。
- `company-thesis-card.json` 至少记录 `content_angle`、`report_context`、`company_identity`、`core_advantages`、`moat_mechanisms`、`growth_drivers`、`profit_scenarios`、`financial_data_role`、`opening_candidates` 和 `selection_reason`。Phase 2 必须原样交接主线决策，不得用模板默认值覆盖。
