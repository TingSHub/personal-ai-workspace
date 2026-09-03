# Workflow: publish-review

> 位置: Project: projects/video-publish-review/workflows/publish-review/

## Mission

对每支已发布视频执行标准化复盘：流量数据采集 → 漏斗/比率诊断 → 证据包归因 → 改进项 → 回写判定 → 规律沉淀。让"下一支视频"从上一支的真实流量数据中变好，复盘项目按视频独立成册、跨期可对比。

## Input

- 源项目发布登记：`projects/<source-project>/account-profile/published-works.md`（workspace 相对路径；当前源项目为 investment-research-video，多账号扩展时按账号对应各自源项目），取其发布条目（实际发布标题/平台/发布时间/视频路径/时长）
- 复盘触发时点：T+3 首次归因，T+7 增量复采出终版
- 账号规律先验：本项目 `outputs/account-rules.md`（Phase 6 维护；首次运行时可为空文件）
- 可选输入：评论区导出、单视频详情页截图（留存曲线/观众画像）

## Output

- `outputs/retrospectives/<published_date>-<slug>/`：
  - `README.md` — 视频身份 + 复盘状态
  - `metrics-snapshot-<采集日期>.json` — 每次采集一个快照（唯一流量事实源）
  - `attribution-<采集日期>.md` — 归因报告（T+3 初版 / T+7 终版）
- 改进项清单（attribution 节），回写候选经用户确认后交 experience-curator
- `outputs/account-rules.md` — 账号规律库（Phase 6 增量更新，长期内容资产）

## Principles

- best_available_resource：按实际效果、输出质量、稳定性、依赖成本、维护成本和当前项目适配性选择资源，禁止 local first；来源不构成优先级
- 真实执行留痕：Phase 的 Required Resources 必须真实执行并留下独立产物（含资源 by-name 与 installed_ref）；未执行不得写成已执行
- 只消费已验收产物：下游 Phase 只引用已落盘的快照 JSON，不引用记忆中的数字
- by-name 引用：Workflow / Skill / Agent / Experience 一律用 by-name 标识符
- 推断与事实分离：归因报告必须显式标注未验证项

## Phase 0: registration-check — 建册与登记核对

### Goal

建立该视频的复盘册，核对发布登记完整性，列出登记缺口（platform_url / 实际标题 / 发布时间）。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| published-works.md 条目 | input | 必选 | projects/&lt;source-project&gt;/account-profile/（workspace 相对路径，当前 investment-research-video） | 发布标题可能与工作标题不一致，以实际发布为准 |

### Input

源项目 published-works.md 的目标条目。

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

### Quality Criteria

- 快照含 captured_at 与 source_file
- 比率字段已 ×100
- 快照 JSON 可独立解读，不需要回看 Excel

### Known Issues

- 官方导出上限约 30 天/100 条；导出不含留存曲线与画像
- 合规约束：每日 ≤ 2 次全量导出；不绕登录/验证码/风控；出现滑块立即停，交人工

## Phase 2: diagnostics — 漏斗与比率诊断

### Goal

从快照 JSON 计算漏斗分层与类型校准比率，形成内容性质判断。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| douyin-viral-analyzer 基准表 | 方法参考 | 必选 | 未注册资源，方法论来自调研结论 | 类型校准比率基准；样本量小，跨期对比优于绝对值 |

### Input

Phase 1 已验收快照 JSON。

### Output

诊断段（attribution 前两节）：漏斗（2s→5s→平均观看→完播）+ 类型校准比率表（藏赞比/转赞比/评赞比/互动率 vs 干货型基准 1:3–1:15 / 1:15–1:40 / 1:30–1:80 / ≥3%）+ 关注漏斗分解（主页访问 → 粉丝增量的转化率，快照含两字段）。

### Quality Criteria

- 漏斗分母统一用播放量
- 比率表四项齐全且标注基准来源
- 关注漏斗分解：主页访问→关注转化率 = follower_delta / profile_visits
- 内容性质判断明确（干货收藏型/情感共鸣型/争议讨论型/信息差科普型）

### Known Issues

- 基准区间样本量小，跨期同类型对比比绝对值更有意义

## Phase 3: attribution — 证据包归因

### Goal

组装六源证据包（指标快照 + 完整文稿 + manifest 话题时序 + 评论区 + 关键帧 + 市场事件），一次多模态归因。同一留存数字可能有完全不同的成因（开头空泛 / 未出现公司名 / 开场寒暄 / 结论太晚 / 画面与标题承诺不一致 / TTS 节奏 / 选题本身无关注度），仅凭指标无法区分——归因必须引用证据包内容，不得只凭指标推断。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| metrics-snapshot | input | 必选 | Phase 1 快照 JSON | 指标事实源 |
| 完整文稿 | input | 必选 | projects/&lt;source-project&gt;/SCRIPT（Content Lock 唯一事实源，自制视频不需 ASR） | 与 manifest 时序对齐 |
| manifest 话题时序 | input | 必选 | projects/&lt;source-project&gt;/manifest（话题编号+起止时间） | 话题级流失对照 |
| 评论区导出 | input | 可选 | douyin-creator-tools comments:export | 归因校验关键；零评论本身即证据 |
| 关键帧 | input | 可选 | ffmpeg 场景切换+均匀采样双轨，Claude 直接读帧图 | 抽帧参数见 Output |
| 市场事件 | input | 可选 | news-search / multi-search（发布日±2 天公司与行业事件） | 解释选题关注度与大盘波动 |
| 竞品数据 | input | 可选 | douyin-blogger-analysis（CDP 挂接用户 Chrome 采集对标账号公开数据） | 竞品三问数据层；未联调，首次使用需用户 Chrome CDP 配合 |

### Input

Phase 2 诊断 + account-rules.md（账号规律先验）+ 上列证据包。

### Output

`attribution-<采集日期>.md`：数据快照节 → 诊断节 → 证据包清单节（六源逐一列明，缺失源显式标注）→ 归因节（1–3 个）+ 改进项节 + 回写候选节。

attribution 归因节规范：每个归因引用 ≥2 类证据（文稿原文 / 帧图 / 评论原文），并做评论区校验——归因点若评论区无人提及则降权并注明（作者得意之笔 ≠ 观众驱动）。

attribution 抽帧参数（继承 douyin-viral-analyzer 方法论）：场景切换+均匀采样双轨并行不可互替，场景阈值 0.15；密度按时长分档 ≤10s→4fps / 10–30s→2fps / 30–120s→1fps / >120s→0.5fps；首帧末帧必读；资源紧张只减中段均匀密度。长视频不逐帧全读：按 manifest 话题边界选 10–20 帧 + 首末帧。

### Quality Criteria

- 六源证据包组装齐全，缺失源在证据包清单节显式标注
- 归因 1–3 个，不并列堆砌；每个归因引用 ≥2 类证据
- 评论区校验必做；零评论时归因必须引用文稿/帧图证据
- 未验证项显式标注

### Known Issues

- 留存曲线不在官方导出中，话题级对照靠 manifest 时序推断，T+7 补验证

## Phase 4: improvements — 改进项与回写候选

### Goal

改进项按预期收益排序，每条以**可证伪假设**表述并落到可执行动作；观点表达合规；列回写候选待用户确认。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| boundary-rewrite | skill | 可选 | workspace · .ai/skills/boundary-rewrite | 争议性表达合规化 |
| video-hook-intro | skill | 可选 | workspace · .ai/skills/video-hook-intro | 改进项的钩子设计参考 |
| account-rules.md | input | 必选 | 本项目 outputs/account-rules.md | 改进项不与已验证规律冲突；新改进项即新假设 |

### Input

Phase 3 归因报告。

### Input 补充（可证伪假设格式）

每条改进项必须能被下一支视频证伪或证实：

```
假设：<成因，引用归因证据>
改动：<下条视频的具体动作>
观察指标：<指标名>（快照字段）
判定阈值：<数值或方向>（对照 account-rules.md 基线）
```

示例：假设——用户流失因前 8 秒在讲行业背景、未回答标题问题；改动——下条视频前 3 秒直接给反常识结论再补证据；观察指标——finish_rate_5s；判定阈值——≥45%（当前基线 38.08%）。

### Output

改进项清单（内容动作/运营动作/发布参数三类，按预期收益排序），每条含假设/改动/观察指标/判定阈值四元组 + 回写候选清单。

### Quality Criteria

- 改进项必须是可执行动作，不接受"继续优化"式空话
- 改进项必须可证伪：不接受"开头更吸引人"式表述；必须指明观察指标与判定阈值
- 争议性表达经 boundary-rewrite 合规校验
- 回写候选不在本项目内决策，经用户确认后交 experience-curator

### Known Issues

- 无

## Phase 5: write-back-decision — 回写判定

### Goal

回写候选经用户确认后，判定归属（账号级规则/workflow SOP/资源踩坑/发布 SOP）并执行回写。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| experience-curator | skill | P5 必选 | workspace · .claude/skills/experience-curator | 归属判定与回写执行 |

### Input

Phase 4 回写候选 + 用户确认。

### Output

回写判定结果：每条候选 → 归属 + 证据 + by-name 回填 experience_refs[]，完成后归档至 `.ai/archive/experiences/`。

### Quality Criteria

- 洞见符合回写标准（能改变未来 Workflow/资源调用/质量检查/可复用脚本）
- 不回写项目日志本身

### Known Issues

- 无

## Phase 6: rule-distillation — 账号规律沉淀

### Goal

把本期复盘结论与历史规律库对照，增量更新 `outputs/account-rules.md`，沉淀"账本两面"自己的规律（如"热门公司+财报证伪留存最好""先结论后解释优于先背景"），让规律成为下期归因与改进项的先验。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| account-rules.md | input/output | 必选 | 本项目 outputs/account-rules.md | 账号级规律库，唯一事实源 |

### Input

本期 attribution + 全部历史复盘册 + 既有 account-rules.md。

### Output

更新后的 `outputs/account-rules.md`，每条规律含：规律表述 / 证据视频列表（引用复盘册路径）/ 置信度 / 状态（假设中 → 已验证 → 已证伪）/ 最近复核日期。

### Quality Criteria

- 新规律 ≥2 支视频证据才能脱离"假设中"状态（单视频结论只能标"假设中"）
- 已有规律被新数据支持时提升置信度；被证伪时显式标记并保留证据链
- 规律表述可操作（能指导选题/结构/时长决策），不写空话

### Known Issues

- 规律库只沉淀账号内容规律；workspace 级结论（能改变 Workflow/资源的）仍走 Phase 5 experience-curator
