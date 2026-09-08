# Workflow: topic-research

> 位置: Project: projects/investment-research-video/workflows/topic-research/

## Mission

围绕用户已经批准的选题问题做定向研究，并通过 `research-collaboration-agent` 与用户共同检验观点、补充材料和寻找反例。产出可供内容导演直接使用的当前答案、机制、证据、最强反证、时间范围、受影响环节和推翻条件，并按 `content_depth` 区分短机制课与深度解释型视频。深度解释型视频还必须交付面向普通观众的知识地图、历史验证线和必要的市场预期关系。它不重新生成候选、不重复审批，也不默认把财报作为研究主线。

## Input

用户已批准的 `topic-forward-lead` topic card（字段来自 `topic-forward-candidate.json.template`）、研究日期、可用来源与访问边界，以及可选的用户观点、疑问、文章链接/摘录和参考视频章节。公司、行业、事件、技术、政策、宏观和比较议题均可进入；只有问题涉及公司时才要求公司标识，只有问题涉及财务时才要求财报与三表资料。`content_depth` 为 `standard` 或 `deep_explainer`；旧卡缺失时按 `standard` 兼容，但若用户明确要求历史、新闻事实、股价关系和深度科普，必须升级为 `deep_explainer`。

## Output

正式输出位于 `outputs/research/{subject_id}/{research_date}/`：

- `approved-topic.json`：批准卡的只读快照及批准来源；
- `source-ledger.md`：实际采用的一手/结构化/外部来源、日期、定位、口径与缺口；
- `evidence/`：各 Required Resource 的独立执行产物和引用原件；
- `research-brief.md`：按 `topic-research-brief.md.template` 生成的研究结论；
- `content-collaboration.md`：同一期唯一的研究讨论、母稿和口播审核协作稿；每轮追加到同一文件，不创建轮次副本；
- `knowledge-map.md`：深度解释型视频的普通观众知识路径；标准模式记录本期最小解释范围；
- `historical-market-relation.md`：涉及周期/估值/行业轮动时的历史阶段与市场预期关系；不适用时记录原因；
- `research-quality-gate.md`：`research-quality-gate` 的验收结果；
- `research-execution.md`：实际资源、installed_ref、输入、产物与降级记录。

只有 Scope Decision 为 `accepted`、研究讨论已由用户与 Agent 双方同意收敛且质量门禁通过的 `research-brief.md` 才能交给视频生产。`scope_change_required` 必须返回 `topic-forward-lead` 重新确认，不得由研究或制作阶段自行改题。

## Principles

- best_available_resource：按实际效果、输出质量、稳定性、依赖成本、维护成本和当前问题适配性选择资源，禁止 local first。
- 真实执行留痕：被选中的 Required Resource 必须真实运行并在 `evidence/` 留下独立产物；未运行不得写成已执行。
- 只研究批准问题：允许缩小无关资料，但不能改变主体、主问题或内容承诺。研究推翻前提时报告范围变化，不在本阶段另选题。
- 研究讨论没有固定轮数；`research-collaboration-agent` 可以建议收敛，用户也可以提出收敛，但只有双方都确认后才结束。
- 用户提供的材料进入 `content-collaboration.md` 作为线索与讨论记录，必须先核验再进入事实正文。
- 问题决定资源：产品实力核验产品、客户、认证与交付；行业逻辑核验供需、瓶颈与利润分配；重大事件核验时间线与传导；盈利质量才深入三表。不得为了“完整”固定跑一套财报清单。
- 观点先有证据：研究必须给出当前更可信的解释及最强反证。模棱两可只允许作为真实证据不足的结论，并必须说明缺什么证据能改变状态。
- 报告是证据，不是结论：最终要回答利润、权力、瓶颈或竞争优势可能向哪里移动，以及判断能持续多久。
- 深度解释型研究必须形成“人话直觉 → 必要概念 → 历史验证 → 当前事实 → 市场预期/估值含义 → 证伪条件”的知识路径；历史和股价关系用于解释，不得被写成简单因果或精确收益预测。
- 新闻事实不是标题清单：每条进入正文的新闻必须说明事件日、发布主体、采取的动作、它验证或挑战了哪一环机制，以及事实与推断的边界。
- 搜索摘要只做线索；关键事实必须打开原文，记录事件日、发布日期、主体、口径和定位。外部研究中的数字与判断需回到原始来源或可靠结构化数据核验。
- 不输出直接荐股、买卖指令、仓位、交易策略或收益保证；可以给出有条件的竞争力、多空和估值判断。
- by-name 引用：Workflow / Skill / Agent / Experience 一律用名称，不用相对路径。

## Phase 1: evidence-plan — 问题拆解与来源发现

### Goal

冻结批准问题和 `content_depth`，明确需要证明什么、可能被什么推翻、应调用哪些研究资源以及何时停止。若为 `deep_explainer`，同时冻结知识地图、历史锚点、市场关系问题和内容不能越过的证据边界。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| `multi-search` | skill | 必选 | workspace installed_ref | 发现近期原文与交叉来源；摘要不能直接作为证据 |

### Input

批准 topic card、研究日期、可用来源与账号内容边界；旧卡缺失 `content_depth` 时记录兼容推断。

### Output

`outputs/research/{subject_id}/{research_date}/approved-topic.json`、`source-ledger.md` 初稿、`evidence/multi-search-execution.md` 和研究停止条件。

### Quality Criteria

- 原样保留批准对象范围、观众问题、内容承诺和增长字段。
- 研究计划说明核心命题、替代解释、最强可能反证及所需证据；不预设最终结论。
- 每类来源标明用途、时效和一手/结构化/外部属性；搜索摘要不进入事实正文。
- `standard` 只需达到核心答案、关键反证和证据缺口的停止条件；`deep_explainer` 还必须确认概念、历史、当前新闻和市场关系四类解释材料是否已足以让普通观众复述机制，不为固定篇幅堆资料。

### Known Issues

热点与涨跌只能说明关注度，不能直接证明公司实力、行业景气或商业化兑现。

## Phase 2: targeted-evidence — 按问题定向取证

### Goal

只运行能回答批准问题的研究资源，形成可追溯证据、替代解释和缺口。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| `industry-analysis` | skill | 可选 | workspace installed_ref | 产业链、竞争格局和价值分配问题 |
| `industry-cycle-analysis` | skill | 条件必选 | workspace installed_ref | 行业、供需、库存、产能、价格和周期问题；`deep_explainer` 的周期题必须执行并留下历史/机制产物 |
| `marketpulse` | skill | 条件必选 | workspace installed_ref | `deep_explainer` 且批准问题涉及猪股/行业股价与预期关系时，获取可复核的历史行情或板块关系；不要求精确股价叙事，但不接受无来源的“股价跟着猪价涨” |
| `investagent` | skill | 可选 | workspace installed_ref | 单家公司或多公司综合研究；不负责视频写作 |
| `earnings-reader` | skill | 可选 | workspace installed_ref | 财报、盈利质量或三表问题 |
| `cninfo-connector` | skill | 可选 | workspace installed_ref | A 股法定披露、公告和报告原文 |
| `tushare-connector` | skill | 可选 | workspace installed_ref | 结构化公司、财务和行情数据；权限不足需记录降级 |
| `news-search` | skill | 条件必选 | workspace installed_ref | `deep_explainer` 或批准问题明确要求新闻事实时，用于发现事件；必须回到原文核验 |
| `deep-research` | skill | 可选 | workspace installed_ref | 外部行业、技术和竞品补充；不能单独支撑关键事实 |
| `finance-report-analyzer` | skill | 可选 | workspace installed_ref | 已有 PDF/Excel 财务包的批量结构化 |

### Input

Phase 1 已验收的研究计划、批准卡和 source ledger。

### Output

`outputs/research/{subject_id}/{research_date}/evidence/` 下按实际资源区分的执行产物，更新后的 `source-ledger.md`，以及事实、机制、历史、市场关系、反证和缺口的证据映射。`deep_explainer` 额外形成 `knowledge-map.md` 和 `historical-market-relation.md`。

### Quality Criteria

- 只调用与问题有关的资源，并在 `research-execution.md` 说明选择与未选择理由。
- 每个关键事实包含来源、日期、主体、口径、定位和 evidence id；不同报告期或业务口径不得直接排名。
- 产品、订单、技术、政策与事件结论优先由公司、监管、政府、标准组织或权威原文支持。
- `deep_explainer` 至少交付：一张知识地图；一条包含关键阶段、转折原因和统计口径的历史线；一条当前新闻/政策事件线；若问题含股价关系，至少两段有时间窗口和来源的“价格/利润/预期”关系材料。可以用定性趋势，不能省掉事实锚点。
- 每个历史或市场关系叙事必须标明 `fact`、`inference`、`estimate` 或 `opinion`，并说明是否只是相关关系；不得把猪价与猪股的同步变化自动写成单一因果。
- 财务比较才要求同期同口径三表；定性产业位置不因缺财务表被阻断，但要写清比较边界。
- 数据源失败、权限不足或关键原文缺失必须显式降级，不能用二手摘要静默替代。

### Known Issues

资源越多不代表结论越好；互相复制的二手文章不构成独立交叉验证。

## Phase 2.5: collaborative-research — 用户观点与证据协作

### Goal

在首轮定向取证之后，让用户提供的观点、疑问、文章、摘录和参考视频进入研究过程。通过多轮对话查证主张、补充知识、寻找最强反例，并由用户与 `research-collaboration-agent` 双方确认后收敛。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| `research-collaboration-agent` | agent | 必选 | internal · v0.1 | 维护同一期唯一协作稿；每轮只推进一个最高价值问题；不替代研究资源、不单方面结束讨论 |

### Input

Phase 2 已验收的证据映射、source ledger、批准卡，以及用户本轮提供的观点、疑问、链接、摘录或视频章节。没有额外用户材料时，Agent 仍需向用户确认是否有初始判断或关键疑问。

### Output

更新 `outputs/research/{subject_id}/{research_date}/content-collaboration.md`。该文件是本期唯一的人工协作稿，按轮次追加讨论，并在同一文件中维护当前综合、母稿、母稿审核、口播审核和交接状态；不创建每轮独立文件。

### Quality Criteria

- 用户输入与 Agent 的研究事实、推断、表达偏好和未决问题分开记录；
- 用户提供的链接、摘录和视频章节先作为线索，关键事实核验后才能进入 `research-brief.md`；
- 每个重要主张都有支持、反驳、部分支持或未解决状态；
- 当前综合明确当前判断、机制、时间范围、最强反例、推翻条件和证据缺口；
- Agent 可以建议收敛，用户也可以提出收敛，但只有双方都确认后才把讨论标记为 closed；
- 若主体、主问题或 `content_line` 需要改变，写入 `scope_change_required` 并返回 `topic-forward-lead`；
- 只有协作稿已 closed，且后续研究质量门通过，才允许进入母稿与表达层。

### Known Issues

协作稿是人工交互产物，不应由自动流程在用户未回应时伪造“双方同意”；用户暂时离开时保留 active 状态，下一次继续同一个文件。

## Phase 3: synthesis-and-challenge — 判断综合与反证

### Goal

在批准问题内给出明确的当前答案，并用最强替代解释测试其边界。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| `financial-editor-agent` | agent | 必选 | internal installed_ref | 裁决事实、口径、因果强度和结论边界；不决定叙事 |
| `boundary-rewrite` | skill | 必选 | workspace installed_ref | 保留判断力度，同时移除直接交易引导 |

### Input

Phase 2 已验收的证据映射、source ledger、批准卡、账号 content-policy，以及已 closed 的 `content-collaboration.md`。

### Output

按 `topic-research-brief.md.template` 生成 `outputs/research/{subject_id}/{research_date}/research-brief.md`，同步回填 `content-collaboration.md` 的 Current Synthesis，并留下 `knowledge-map.md`、`historical-market-relation.md`（按适用性）、`evidence/financial-editor-execution.md` 与 `evidence/boundary-rewrite-execution.md`。

### Quality Criteria

- Current Answer 是一句明确、可争辩、可证伪的判断，不用“两方面都有可能”替代结论。
- 说明成立机制、适用时间、直接受益/受压或关键环节、最强反证和推翻条件。
- `deep_explainer` 的 `Knowledge Map` 必须让非专业观众知道“先理解什么、为什么、证据在哪、它改变什么”；`Historical And Market Relation` 必须区分历史事实、市场叙事和编辑推断。
- 每个核心判断能回指 evidence id；事实、推断和预测明确分开。
- `content-collaboration.md` 中用户提出的关键疑问已经回应，未采纳的观点保留理由，不能只保留最终结论。
- `check_content_collaboration.py --phase research` 能确认协作稿结构完整；进入母稿前必须改用 `--phase mother` 并通过双方收敛检查。
- 若证据不足，只能降低结论强度并列出缺口；若批准问题本身失效，Scope Decision 必须为 `scope_change_required`。
- 财报、公告或后续数据只作为验证条件，不得成为“以后再看”的空结论。

### Known Issues

鲜明观点不等于绝对化表达。最强反证必须真的能挑战主张，不能用弱风险充数。

## Phase 4: research-acceptance — 研究验收与移交

### Goal

确认研究可以安全、准确地进入内容导演阶段，并冻结范围与证据版本。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| `research-quality-gate` | skill | 必选 | workspace installed_ref | 验收来源、口径、脚本可用性和证据链；不替代人工事实裁决 |

### Input

research brief、source ledger、证据映射、批准卡和各资源执行产物。

### Output

`outputs/research/{subject_id}/{research_date}/research-quality-gate.md`、冻结的 `research-brief.md` 与 `research-execution.md`。

### Quality Criteria

- 批准卡与 research brief 的主体、主问题一致。
- 关键事实可追溯，数字有单位、期间、口径和定位；未裁决冲突不能进入结论。
- Scope Decision 为 `accepted` 才可移交 `investagent-podcast-video-by-hyperframes`。
- 移交包明确当前判断、机制、时间范围、受影响环节、最强反证、推翻条件、证据缺口和可视化线索。
- 若为 `deep_explainer`，移交包还必须明确知识地图、历史锚点、市场关系材料、新闻事件线和可用于幽默的事实锚点；缺任一项则降低为 `standard` 或退回研究计划，不能静默交给表达层补写。
- 质量门禁及每个已调用资源都有独立执行记录。

### Known Issues

研究验收不代表结论永久正确；新证据触发推翻条件时，应重新运行本 Workflow，而不是在制作阶段临时改口径。
