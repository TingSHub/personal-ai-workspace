# Workflow: publish-review

> 位置: Project: projects/video-publish-review/workflows/publish-review/

## Mission

对每支已发布视频执行标准化复盘：流量数据采集 → 漏斗/比率诊断 → 归因 → 改进项 → 回写判定。让"下一支视频"从上一支的真实流量数据中变好，复盘项目按视频独立成册、跨期可对比。

## Input

- 源项目 `account-profile/published-works.md` 的发布条目（实际发布标题/平台/发布时间/视频路径/时长）
- 复盘触发时点：T+3 首次归因，T+7 增量复采出终版
- 可选输入：评论区导出、单视频详情页截图（留存曲线/观众画像）

## Output

- `outputs/retrospectives/<published_date>-<slug>/`：
  - `README.md` — 视频身份 + 复盘状态
  - `metrics-snapshot-<采集日期>.json` — 每次采集一个快照（唯一流量事实源）
  - `attribution-<采集日期>.md` — 归因报告（T+3 初版 / T+7 终版）
- 改进项清单（attribution 第四节），回写候选经用户确认后交 experience-curator

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
| published-works.md 条目 | input | 必选 | 源项目 account-profile/ | 发布标题可能与工作标题不一致，以实际发布为准 |

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

诊断段（attribution 前两节）：漏斗（2s→5s→平均观看→完播）+ 类型校准比率表（藏赞比/转赞比/评赞比/互动率 vs 干货型基准 1:3–1:15 / 1:15–1:40 / 1:30–1:80 / ≥3%）。

### Quality Criteria

- 漏斗分母统一用播放量
- 比率表四项齐全且标注基准来源
- 内容性质判断明确（干货收藏型/情感共鸣型/争议讨论型/信息差科普型）

### Known Issues

- 基准区间样本量小，跨期同类型对比比绝对值更有意义

## Phase 3: attribution — 归因分析

### Goal

把诊断结果归因到可修改的内容与发布变量（钩子/中段结构/评论触发器/发布时间），每个归因带证据链，显式标注未验证项。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| 评论区导出 | input | 可选 | douyin-creator-tools comments:export | 归因校验关键；零评论本身即证据 |
| 视频脚本话题表 | input | 可选 | 源项目 manifest/SCRIPT | 话题级留存对照（留存曲线需人工补） |

### Input

Phase 2 诊断 + 评论区数据 + 视频结构（脚本话题表）。

### Output

`attribution-<采集日期>.md`：数据快照节 → 诊断节 → 归因节（1–3 个，按证据强度排序）+ 改进项节 + 回写候选节。

### Quality Criteria

- 归因 1–3 个，不并列堆砌
- 每个归因有证据链（快照数据 + 评论区/结构证据）
- 未验证项显式标注

### Known Issues

- 留存曲线不在官方导出中，中段归因是推断，T+7 补验证

## Phase 4: improvements — 改进项与回写候选

### Goal

改进项按预期收益排序，每条落到可执行动作；观点表达合规；列回写候选待用户确认。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| boundary-rewrite | skill | 可选 | workspace · .ai/skills/boundary-rewrite | 争议性表达合规化 |
| video-hook-intro | skill | 可选 | workspace · .ai/skills/video-hook-intro | 改进项的钩子设计参考 |

### Input

Phase 3 归因报告。

### Output

改进项清单（内容动作/运营动作/发布参数三类，按预期收益排序）+ 回写候选清单。

### Quality Criteria

- 改进项必须是可执行动作，不接受"继续优化"式空话
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

回写判定结果：每条候选 → 归属 + 依据 + by-name 回填 experience_refs[]，完成后归档至 `.ai/archive/experiences/`。

### Quality Criteria

- 洞见符合回写标准（能改变未来 Workflow/资源调用/质量检查/可复用脚本）
- 不回写项目日志本身

### Known Issues

- 无

## Evolution Log

| 日期 | 变更 | 依据 |
|---|---|---|
| 2026-09-01 | 初版：基于 2026-08-31 中科曙光首次闭环实战固化 | 中科曙光 T+3 复盘（中科曙光复盘册 attribution-2026-08-31.md） |
