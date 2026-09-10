# Workflow: publish-review

> 位置: Project: projects/investment-research-video/workflows/publish-review/

## Mission

对每支已发布视频执行证据驱动复盘：平台详情数据采集 → 漏斗/比率诊断 → 与原视频内容对齐 → 归因 → 生成改进候选 → 将候选交给 `topic-forward-lead` 按选题适配 → 多期规律沉淀。复盘不直接决定下一条视频选题，也不把单条视频结构升级为全局模板。

## Input

- 发布登记：本项目 `account-profile/published-works.md`（workspace 相对路径 `projects/investment-research-video/account-profile/published-works.md`；本 Workflow 与源项目同库，多账号扩展时按账号对应各自源项目），取其发布条目（实际发布标题/平台/发布时间/视频路径/时长）
- 生命周期状态单一事实源：各视频的复盘进度与待补队列以 `account-profile/published-works.md` 各条目的 `review_status`/`review_dir` 为准；本 SOP 不维护独立队列清单
- 复盘触发时点：T+3 首次归因，T+7 增量复采出终版
- 账号规律先验：本项目 `outputs/account-rules.md`（Phase 7 维护；首次运行时可为空文件）
- 原视频证据：最终成片、旁白稿/字幕、场景或章节 manifest、封面与发布标题（历史视频缺失时显式标注）
- 创作前叙事决策记录：选题问题、核心冲突、叙事原型、opening promise 与预期风险（新视频必填，历史视频可回溯补录）
- 可选输入：评论区导出、单视频详情页截图（详情采集的补充证据）

## Output

- 采集阶段必生成：`outputs/retrospectives/<published_date>-<slug>/README.md`、官方导出解析后的 `detail-exports-<采集日期>.json`
- 原视频证据齐全并完成归因后生成：`attribution-<采集日期>.md`（其中包含诊断和改进候选池）
- 采集阶段同时保留：`detail-exports-<采集日期>/` 原始 Excel 与 `export-manifest.json`
- 详情页补充采集成功时才生成：`detail-snapshot-<采集日期>.json`；页面证据需要留痕时生成 `detail-page-<采集日期>.png`
- 账号已有作品列表基线时可生成：`metrics-snapshot-<采集日期>.json`（用于跨视频比较，不替代单作品详情导出）
- 归因报告内含改进候选池，供必选的 `topic-forward-lead` 按每个选题自由适配；本 Workflow 不生成单独的候选选择文件
- `outputs/account-rules.md` 只在跨视频规律满足证据条件并决定沉淀时更新，不是每条视频必更新

## Principles

- best_available_resource：按实际效果、输出质量、稳定性、依赖成本、维护成本和当前项目适配性选择资源，禁止 local first；来源不构成优先级
- 真实执行留痕：Phase 的 Required Resources 必须真实执行并留下独立产物（含资源 by-name 与 installed_ref）；未执行不得写成已执行
- 只消费已验收产物：下游 Phase 只引用已落盘的快照 JSON，不引用记忆中的数字
- by-name 引用：Workflow / Skill / Agent / Experience 一律用 by-name 标识符
- 推断与事实分离：归因报告必须显式标注未验证项
- 结构开放、功能稳定：叙事原型、章节数量、信息顺序可以变化；验证对象是开头承诺、冲突建立、证据兑现等叙事功能，不是固定章节模板
- 候选不等于规则：单条复盘只形成假设；下一条按适用条件选择零或一个主要内容实验。多次相似表现增加支持度，但不能仅凭两条视频证明因果
- 增长按完整漏斗诊断：曝光 → 点击/播放 → 2 秒/5 秒 → 平均观看/完播 → 点赞/评论/收藏/分享 → 主页访问 → 关注。某一层的数据不能替代其他层；收藏分享和关注转化对研究型账号通常比单一点赞更接近长期价值，但仍须按题材、时长、来源和样本量解释。
- 内容与数据必须合并：平台指标只定位现象，归因必须尽量对照原视频、字幕、manifest、封面或评论证据

## Phase 0: registration-check — 建册与登记核对

### Goal

建立该视频的复盘册，核对发布登记完整性，列出登记缺口（platform_url / 实际标题 / 发布时间）。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| `douyin-creator-tools` | skill | 可选 | workspace installed_ref | 需要补充作品身份时使用；已有登记则不重复采集 |

### Input

本项目 `account-profile/published-works.md` 的目标条目。

### Output

`outputs/retrospectives/<published_date>-<slug>/README.md`（视频身份 + 复盘状态 + 登记缺口）。

### Quality Criteria

- 视频身份四要素齐全：实际发布标题、平台、发布时间、时长
- 登记缺口显式列出
- 文件夹命名与 published-works.md 可互相索引

### Known Issues

- 发布标题与工作标题不一致是常态（中科曙光案例），以创作者中心实际为准

## Phase 1: collection — 流量数据采集

### Goal

登录态自动化导出作品列表 Excel，解析为快照 JSON 落盘到复盘册。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| douyin-creator-tools | skill | 必选 | github · wenyg/douyin-creator-tools · e35dbe2 | 指标导出+解析辅助脚本；有改版风险（踩坑见资源文档） |

### Input

复盘册 README 的视频身份；douyin-creator-tools 登录态有效。

### Output

`metrics-snapshot-<采集日期>.json`：播放/完播率/5s完播率/2s跳出率/封面点击率/平均播放时长/赞/评/藏/转/主页访问/粉丝增量 + captured_at。

本文件是作品列表导出的跨视频基线；单条视频详情复盘以 Phase 2 的官方详情导出 JSON 为主。

### Quality Criteria

- 快照含 captured_at 与 source_file
- 比率字段已 ×100
- 快照 JSON 可独立解读，不需要回看 Excel

### Known Issues

- 官方导出上限约 30 天/100 条；导出不含留存曲线与画像
- 合规约束：每日 ≤ 2 次全量导出；不绕登录/验证码/风控；出现滑块立即停，交人工

## Phase 2: detail-collection — 单作品详情页官方导出与补充采集

### Goal

优先点击创作者中心单作品详情页的官方“导出”按钮，获取结构化 Excel；再用详情页采集补充导出文件没有的数据与页面证据。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| douyin-creator-tools | skill | 必选 | github · wenyg/douyin-creator-tools · e35dbe2；详情采集脚本已在 workspace 资源中登记 | 复用本人账号登录态；采集总览、趋势、章节、搜索词等页面可见数据；页面改版时截图作为兜底 |

### Input

复盘册 README 的 `item_id` 或可定位的作品标题；创作者中心登录态。

### Output

- `detail-exports-<采集日期>/`：官方导出的原始 Excel 与下载清单
- `detail-exports-<采集日期>.json`：内容吸引力、观众参与度、流量来源、观众分析的统一 JSON
- `detail-snapshot-<采集日期>.json`：章节、搜索关键词、趋势等补充结构化数据
- `detail-page-<采集日期>.png`：需要页面证据或补充采集时保留的详情页截图

### Quality Criteria

- 官方导出文件至少覆盖内容吸引力、观众参与度、流量来源、观众分析四类中的可用项，并保存 `export-manifest.json`
- 解析 JSON 含 item_id、captured_at、原始文件路径与结构化 rows
- 比率字段统一为百分数；导出趋势保留时间点和值；章节保留时间点、说明与点击率
- 请求 URL 不保存 `msToken`、`a_bogus`、Cookie 或其他鉴权参数
- 某一导出模块或补充标签失败时，记录 errors，缺失字段写 null/空数组并保留已下载文件，不用 0 猜测

### Known Issues

- 详情页必须使用 `/creator-micro/work-management/work-detail/<作品ID>`，不能用投稿分析汇总页替代
- 导出表头和页面请求参数可能随抖音改版变化；先保存原始 Excel/页面证据，再更新解析逻辑
- 详情页数据是本人账号可见数据，只用于内部复盘，不采集他人后台

## Phase 3: diagnostics — 漏斗与比率诊断

### Goal

从快照 JSON 计算漏斗分层与类型校准比率，形成内容性质判断。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| video-agent-operator | skill | 必选 | workspace · `.claude/skills/video-agent-skills/video-agent-operator/` | 计算指标、跨视频对照与候选诊断；基准区间只作辅助，不替代账号自身历史基线 |

### Input

Phase 1 已验收快照 JSON（有则用于跨视频比较）+ Phase 2 已验收官方详情导出 JSON；详情页补充 JSON 有则引用。

### Output

诊断段（attribution 前两节）：完整漏斗（曝光→点击/播放→2s→5s→平均观看→完播→点赞/评论/收藏/分享→主页访问→关注）+ 类型校准比率表（藏赞比/转赞比/评赞比/互动率 vs 同题材历史基线）+ 关注漏斗分解（主页访问 → 粉丝增量的转化率，快照含两字段）。缺失层必须显式标记，不得从播放量直接推断封面点击或关注意愿。

### Quality Criteria

- 漏斗分母统一用播放量
- 曝光与点击数据可得时单列点击/播放转化；不可得时标记缺口，不用播放量倒推曝光。
- 比率表四项齐全且标注基准来源
- 关注漏斗分解：主页访问→关注转化率 = follower_delta / profile_visits
- 内容性质判断明确（干货收藏型/情感共鸣型/争议讨论型/信息差科普型）

### Known Issues

- 基准区间样本量小，跨期同类型对比比绝对值更有意义

## Phase 4: attribution — 原视频对齐与证据包归因

### Goal

组装六源证据包（指标快照 + 完整文稿 + manifest 话题时序 + 评论区 + 关键帧 + 市场事件），一次多模态归因。同一留存数字可能有完全不同的成因（开头空泛 / 未出现公司名 / 开场寒暄 / 结论太晚 / 画面与标题承诺不一致 / TTS 节奏 / 选题本身无关注度），仅凭指标无法区分——归因必须把平台现象对齐到原视频的文本、时间轴、画面或评论证据，不得只凭指标推断。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| `douyin-creator-tools` | skill | 可选 | workspace installed_ref | 采集评论或详情补充；零评论本身即证据 |
| `multi-search` | skill | 可选 | workspace installed_ref | 核验发布日前后事件；搜索结果必须回到原文 |

### Input

Phase 3 诊断 + account-rules.md（账号规律先验）+ detail exports、完整文稿、manifest 话题时序、评论、关键帧、市场事件与可选竞品数据组成的证据包。

### Output

`attribution-<采集日期>.md`：数据快照节 → 诊断节 → 证据包清单节（六源逐一列明，缺失源显式标注）→ 归因节（1–3 个）→ 改进候选池 → 回写候选节。

attribution 归因节规范：每个归因引用 ≥2 类证据（文稿原文 / 帧图 / 评论原文），并做评论区校验——归因点若评论区无人提及则降权并注明（作者得意之笔 ≠ 观众驱动）。

attribution 抽帧参数：场景切换+均匀采样双轨并行不可互替，场景阈值 0.15；密度按时长分档 ≤10s→4fps / 10–30s→2fps / 30–120s→1fps / >120s→0.5fps；首帧末帧必读；资源紧张只减中段均匀密度。长视频不逐帧全读：按 manifest 话题边界选 10–20 帧 + 首末帧。

### Quality Criteria

- 六源证据包组装齐全，缺失源在证据包清单节显式标注
- 归因 1–3 个，不并列堆砌；每个归因引用 ≥2 类证据
- 评论区校验必做；零评论时归因必须引用文稿/帧图证据
- 未验证项显式标注

### Known Issues

- 留存曲线不在官方导出中，话题级对照靠 manifest 时序推断，T+7 补验证

## Phase 5: improvement-candidates — 改进候选池

### Goal

从归因中生成 3–5 个改进候选。候选必须区分“跨结构叙事功能”与“本条视频的具体实现”，并标明适用的叙事原型；本 Phase 不自动选择、不直接回写正式规则。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| boundary-rewrite | skill | 可选 | workspace · .ai/skills/boundary-rewrite | 争议性表达合规化 |
| finance-content-engineering | skill | 可选 | workspace installed_ref | 把归因转成可执行叙事动作；不自动升级为规则 |

### Input

Phase 3 归因报告 + account-rules.md。账号规律是输入事实，不是 Required Resource。

### Input 补充（可证伪假设格式）

每条改进项说明适用题材、受众、时长和观察窗口；在适配视频中观察支持或反驳信号，不能把下一支视频的变化视为因果证明：

```
假设：<成因，引用归因证据>
改动：<适配视频中的具体动作；可不采用>
观察指标：<指标名>（快照字段）
判定阈值：<数值或方向>（对照 account-rules.md 基线）
```

示例：假设——用户流失因前 8 秒在讲行业背景、未回答标题问题；改动——下条视频前 3 秒直接给反常识结论再补证据；观察指标——finish_rate_5s；判定阈值——≥45%（当前基线 38.08%）。

### Output

改进候选池写入 `attribution-<采集日期>.md`，不额外生成独立文件。每条含假设、证据、适用结构、实现方式、观察指标与判定阈值。

### Quality Criteria

- 改进候选必须是可执行动作，不接受"继续优化"式空话
- 改进候选必须可证伪：必须指明观察指标与判定阈值
- 候选必须说明适用条件和不同叙事结构下的实现方式；发布时间、封面等发布实验交对应环节，不强制进入剧情
- 归因区分观察、假设、行动；同时改动多个变量时明确无法单独归因。均值不能推断具体流失时间；无评论不能证明观众不在意某问题
- 争议性表达经 boundary-rewrite 合规校验
- 本 Phase 只生成候选，不在本 Phase 内选择正式规则

### Known Issues

- 无

## Phase 6: write-back-decision — 回写判定

### Goal

回写候选经用户确认后，判定归属（账号级规则/workflow SOP/资源踩坑/发布 SOP）并执行回写。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| experience-curator | skill | 条件使用 | workspace · .claude/skills/experience-curator | 用户确认后进行归属判定与回写 |

### Input

Phase 5 回写候选 + 用户确认。

### Output

仅在用户确认需要沉淀 workspace 级经验时生成回写判定结果：每条候选 → 归属 + 证据 + by-name 回填 experience_refs[]，完成后归档至 `.ai/archive/experiences/`。

### Quality Criteria

- 洞见符合回写标准（能改变未来 Workflow/资源调用/质量检查/可复用脚本）
- 不回写项目日志本身

### Known Issues

- 无

## Phase 7: rule-distillation — 账号规律沉淀

### Goal

把本期复盘结论与历史规律库对照，增量更新 `outputs/account-rules.md`，沉淀"账本两面"自己的条件规律（如某类选题更适合某类叙事原型，或某类开头功能在不同结构中均有效），让规律成为下期归因与候选生成的先验。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| account-rules.md | input/output | 必选 | 本项目 outputs/account-rules.md | 账号级规律库，唯一事实源 |

### Input

本期 attribution + 全部历史复盘册 + 既有 account-rules.md。

### Output

满足跨视频可比性、记录混杂因素且决定沉淀时，才更新 `outputs/account-rules.md`；每条规律含：规律表述 / 证据视频列表（引用复盘册路径）/ 置信度 / 状态（假设中 → 有条件支持 → 待复核/不支持）/ 最近复核日期。

### Quality Criteria

- 两支可比视频只能增加支持度；须记录题材、时长、流量来源、观察窗口及其他变化，排除明显替代解释后才可标为有条件支持。观察性数据不标因果已验证
- 新数据支持或反驳时保留适用范围和证据链；冲突样本记为待复核，不删除历史证据
- 规律表述可操作且带适用条件（能指导选题/结构/时长决策），不写无条件万能模板

### Known Issues

- 规律库只沉淀账号内容规律；workspace 级结论（能改变 Workflow/资源的）仍走 Phase 6 experience-curator
