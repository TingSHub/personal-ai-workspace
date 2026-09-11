# Investment Research Video

把公司实力、行业逻辑、重大事件、技术与政策变化，转成有明确判断、可验证证据和增长目标的财经视频。

## 启动与输入输出

从工作区根目录启动 Agent，指定项目 `investment-research-video`。最小请求示例（仅为调用示例，不代表已批准选题或发布）：

> 在 investment-research-video 项目，按 investment-research-video-create 围绕“液冷产业的交付瓶颈”提出选题，面向当前账号制作约 5 分钟的抖音视频，先确认研究问题，最终交付成片与发布草稿。

启动时提供主题或选题授权范围、研究日期、目标平台/时长/画幅，以及是否复用当前账号配置。入口读取待复盘作品后按 SOP 决定起点；已获批选题或已验收研究包可作为交接输入，但仍需核对对应阶段的进入条件。

预期交付为选题卡、研究包、表达包、音频/字幕/画面、成片及发布包。详细输入输出与批准边界以各 Workflow 为准：研究包由 topic-research 管理，制作产物由 investagent-video-execution 管理，发布后数据由 publish-review 管理。

## 配置与依赖

以下位置相对本项目目录，工作区共享资源另行注明。它们是现有配置的导航，不是第二份流程定义。

| 内容 | 位置或资源 | 调用约定 |
|---|---|---|
| 账号定位与表达规则 | `account-profile/ACCOUNT_PROFILE.md`、`content-policy.md`、`dialogue-policy.md` | 明确本次使用哪个账号；更换账号时复核这些规则 |
| 视觉、封面与图表 | `account-profile/design.md`、`cover-reference/`、`charts/chart-spec.md` | 复用当前素材；更换素材时显式指定位置 |
| 已发布作品与复盘入口 | `account-profile/published-works.md`、`docs/publish-review.md` | 用于真实作品追踪，不是通用测试样例 |
| 数据与场景契约 | 工作区 `.ai/templates/` 中的 topic-forward-candidate、topic-research-brief、content-collaboration、investment-video-episode-input、investment-video-scene-manifest 模板 | 字段只从模板读取，不在此复制 |
| 音色、字体等共享资产 | 工作区 `.ai/assets/` | 通过登记的 resource_key 选择；音频使用 voice.zhiwei / voice.shenyan，实际参数以执行 SOP 为准 |
| 项目工具与测试 | `scripts/README.md`、`tests/` | 项目级工具保留在项目；外部资源调用按名称查询管理记录 |

本地回归测试使用 Python 3 标准库。生产依赖按所执行阶段准备：研究需要联网与相应数据访问；音频由 podcast-audio-compiler、voxcpm 的资源记录说明运行环境、模型和 FFmpeg 等要求；渲染环境由 hyperframes-cli 管理；发布与复盘所需登录态按发布资源及 douyin-creator-tools 的记录处理。凭据只记录配置名称和获取条件，不写入项目文档。资源来源、版本、安装与更新方法查询对应 Skill/Agent 管理记录，完整资源清单以各阶段 Required Resources 为准。

当前仍依赖本工作区的模板、资源安装和本地模型环境；画面生成器的账号素材/字体有工作区相对默认位置，可通过 `--account-media-dir`、`--font-dir` 覆盖。其他脚本迁出时需逐项核对路径与依赖，目前未验证独立环境中的整条生产链。

## 最小复跑与验收

在工作区根目录执行现有本地测试：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s projects/investment-research-video/tests -p 'test_*.py'
```

测试自行构造合成输入并使用临时目录，覆盖 episode 输入编译及开场提取、研究/表达协作与编辑门禁、对白和数字检查、场景音频同步、结尾标题等行为。2026-09-11 本次运行 49 项全部通过；预期退出码为 0 且输出 OK，测试数量随维护变化。

其中 `tests/test_build_podcast_episode.py` 提供可复用的行业主题最小输入与编译验收案例。测试中的合成证据和回执仅验证程序行为，不作为正式研究或批准依据。端到端验证需使用新批准的选题、当次有效研究资料、真实音频和渲染结果，逐阶段按 SOP 验收；本次未重跑真实配音、渲染、发布及发布后复盘。

## 主链路

整支视频从单入口编排 Workflow `investment-research-video-create` 进入（阶段编排表：复盘 → 选题 → 研究 → 表达 → 制作发布 → 复盘闭环，见 `workflows/investment-research-video-create/workflow.md`）。各阶段对应 Workflow：

1. `topic-forward-lead`：从事件、产业、公司、观众问题和可选行情线索生成选题卡；用户只确认“研究什么”。
2. `topic-research`：围绕已批准问题定向研究，按 `content_depth` 区分标准机制课与深度解释型视频；后者额外交付知识地图、历史验证线、当前新闻事实和必要的市场预期关系；不重新选题。
3. `investagent-podcast-video-by-hyperframes`：父 Workflow，只负责事实层、表达层和执行层的顺序与交接。
   - `topic-research`：事实层，冻结研究证据与当前判断；
   - `investagent-content-expression`：表达层，锁定主张、知识路径、叙事和真实双人对白；
   - `investagent-video-execution`：执行层，编译音频、视觉、渲染、QA 和发布。
4. `publish-review`：按曝光到关注的完整漏斗复盘，将观察、归因假设和下一轮实验分开；复盘只影响适用的新选题。

研究若推翻选题前提，或必须改变主体范围、主问题，标记 `scope_change_required` 并返回 `topic-forward-lead`。标题、章节、叙事模式和口播措辞的调整由内容导演负责，不触发重复审批。

## 复盘与选题前瞻

`publish-review` 与 `topic-forward-lead` 构成复盘与选题闭环：前者按曝光到关注的完整漏斗复盘已发布视频并沉淀账号规律（`outputs/account-rules.md`），后者把复盘改进候选与多来源信号转为下一批选题。各视频生命周期与复盘状态（复盘册指针、T+1/T+3/T+7 进度与待补队列）以 `account-profile/published-works.md` 为唯一事实源；模块机制与运行规则见 `docs/publish-review.md`。

## 内容原则

- 流量是产品目标：每期都要明确点击理由、观看承诺、互动价值和关注理由，并在正文兑现。
- 每期只有一个核心判断。判断必须有证据、可争辩、可证伪，结论强度不得超过证据。
- 财报只是证据类型，不是固定结构。研究资源由问题决定；没有财务问题时，不强制三表和现金流分析。
- 结尾给出当前判断、机制、适用时间、受影响环节和推翻条件。“继续看后续财报”只能是验证动作，不能充当结论。
- 可以表达明确的多空、竞争力和估值观点；禁止直接荐股、交易指令、仓位建议和收益保证。

## 责任边界

- 选题前瞻：决定什么问题值得研究，并取得真实批准。
- 研究：回答问题，给出证据、替代解释和判断边界。
- `editorial-director-agent`：选择最终主张和讲法，对点击承诺与观看留存负责。
- `financial-editor-agent`：裁决事实、口径和因果强度。
- `dialogue-director-agent`：把导演方案变成自然、可听懂的逐句互动。
- 制作与发布：执行锁定方案，并保证标题、封面、口播、画面和发布文案一致。

## 运行约束

- 下游只消费已验收的上游产物；每个 Required Resource 必须真实执行并留下独立记录。
- 字段清单只从 `.ai/templates/` 读取。
- 历史报告、旧流程与既有输出只作追溯，不作为当前视频链路输入。
- 项目执行记录写入 `logs/`；可复用结论经用户确认后再交 `experience-curator`。
- 稳定方法维护在 SOP，变化的输入、配置与单次产物分开；README 只保留导航与复跑依据。
- Skill 转换完全可选。用户要求时，再由 skill-creator 基于现有 SOP、脚本、模板、依赖记录和测试封装，按目标环境处理路径与资源打包并验证；日常交付不要求预建 Skill 包。
