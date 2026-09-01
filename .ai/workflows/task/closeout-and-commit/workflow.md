# Workflow: closeout-and-commit

> 位置: `.ai/workflows/task/closeout-and-commit/`

## Mission

把“收尾 / 提交 / 结束 / wrap up”从一句口头指令变成可复用的交付流程：先从本轮对话、日志和产物中提炼可改变未来行动的经验，再由用户确认，随后回写正式文档、清理交付表面、验证任务边界，最后按模板为每个受影响仓库创建本地 Git 提交。流程服务所有项目，不绑定公司、视频或单一 Workflow。

## Input

- 触发意图：用户表达收尾、提交、结束、交付或等价意图；若只是询问状态，不启动提交分支。
- 当前工作范围：项目或顶层仓库、任务目标、正式产物、验收证据、使用过的 Workflow/Skill/Agent、当前 Git 仓库边界。
- 可追溯材料：本轮对话文本或转写稿、项目日志、已验收产物、用户已明确接受的决定。
- 用户选择：Phase 1 生成候选后，必须明确确认要回写的经验、文档变更和提交范围；未确认时只保留 closeout staging bundle，不改正式资产、不提交。
- 可选：本轮排除项或必须保留的审计事实。没有提供时由资源规则从最终状态判定，不凭空补写。

## Output

每次运行先在当前仓库产生一个可审计的 staging bundle：

- 项目仓库：`projects/<project>/logs/closeout/<run-id>/`
- 顶层仓库：`.ai/closeouts/<run-id>/`

Bundle 至少包含：`baseline.md`、`conversation-distill.md`、`experience-candidates/`、`doc-change-proposals.md`、`commit-plan.md`、`validation-receipt.md`、`final-delivery.md`。原始对话只可留在 staging/evidence，不得直接进入资产库。

用户确认后，正式输出为：已回写并归档的 Experience、更新后的 Workflow/Skill/Agent 文档、验证收据、每个仓库一个符合模板的本地 commit，以及最终交付说明。默认不 push、不发 PR、不发送外部消息。

## Principles

- best_available_resource：按实际效果、输出质量、稳定性、依赖成本、维护成本和当前项目适配性选择资源，禁止 local first。
- 先候选、后确认：蒸馏结论和文档计划可以自动生成，正式资产回写和提交必须经过用户确认。
- 只沉淀可改变未来行动的经验：项目专属事实、普通命令输出、对话全文和无证据建议留在日志或 staging。
- 正式文档是最终状态叙述：只保留读者理解结果所需的事实，不把被否决方案、纠正过程或内部约束当成标题和交付内容。
- 保护边界：先记录 pre-existing 修改，按文件清单提交；多个仓库分别验证、分别提交。
- 不把验证替代事实：质量门只能检查已定义的要求，不能把一次通过当成通用能力证明。
- 不自动扩张外部动作：本 Workflow 只提交本地 Git；push、PR、发布和删除属于另一个明确授权。
- by-name 引用：Workflow/Skill/Agent/Experience 使用稳定名称，不使用相对路径作为资源身份。

## Phase 0: inventory — 固定范围与权威基线

### Goal

确定本轮哪些内容属于任务、哪些是 pre-existing 修改，冻结各仓库基线，避免收尾时把无关变更带入文档或提交。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| resource-manager | skill | 必选 | internal | 解析当前资源说明、确认资源身份和 installed_ref；不负责经验回写 |

### Input

触发意图、当前工作目录、任务目标、Git 仓库列表、正式产物和已有验证记录。

### Output

`baseline.md`：仓库绝对路径、HEAD、工作树状态、任务拥有的文件范围、pre-existing 修改、待验证产物、是否存在未完成 closeout。

### Quality Criteria

- 每个受影响仓库都记录 HEAD 与 `git status --short` 快照。
- 明确 task-owned 文件候选和保护清单；未知归属不得默认纳入提交。
- 找到并读取当前任务使用的 Workflow SOP；没有 Workflow 时记录为流程缺口，不在本阶段临时创造隐含规则。
- 不修改正式资产、不 stage、不 commit。

### Known Issues

Git 工作树可能包含其他任务的修改；以 baseline 快照和用户确认范围为准。无法区分归属时只提出候选，不执行提交。

## Phase 1: distill — 对话蒸馏与经验候选

### Goal

把本轮反馈压缩为可复用的正向结论、质量规则、资源调用教训和脚本化机会，形成候选而不是直接写入正式文档。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| cangjie-skill | skill | 必选 | internal | 用 RIA-TV++ 的结构/原则/反例/应用视角蒸馏长对话或转写；需要可追溯文本源，不凭记忆补写 |
| experience-curator | skill | 必选 | internal | 筛选会改变未来 Workflow、资源调用、质量检查或脚本的结论；负责归属，不越权回写 |

### Input

`baseline.md`、对话/日志文本、已验收交付物、当前 Workflow/Skill/Agent 说明和验证证据。

### Output

- `conversation-distill.md`：主题骨架、已接受结论、证据、适用边界、未决项。
- `experience-candidates/*.md`：按 Experience 模板生成的候选，明确 owner、asset、证据和未来行动。
- `doc-change-proposals.md`：每项候选建议回写到哪个 Workflow/Skill/Agent，以及理由。
- `commit-plan.md`：按仓库拆分的拟提交文件、提交类型和最终状态摘要。

### Quality Criteria

- 对话蒸馏有实际文本来源和元信息，不把私有推理当证据。
- 每个候选都能回答“下次具体改变什么行动”；否则留在 `conversation-distill.md`，不创建 Experience。
- 同主题候选先搜索已有 Experience，重复结论合并而不是新增。
- 项目专属事实、未验证建议、被否决方案和原始对话不进入候选正文。
- 可机械化的人工检查被标记为脚本候选，并写明目标资源。
- 本阶段不改 canonical docs、不移动 Experience、不提交 Git。

### Known Issues

cangjie-skill 原生定位是长内容→skills；本 Workflow 只使用其蒸馏方法生成候选，不在没有用户确认时自动创建或安装新 Skill。Experience Curator 的正式 promote 必须延后到 Phase 2。

## Phase 2: approval-and-apply — 用户确认后回写正式文档

### Goal

让用户对“哪些经验成立、回写哪里、哪些文件提交”作出明确确认，然后只应用被确认的变更。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| experience-curator | skill | 必选 | internal | 按确认结果 promote，回写带来源标记的条目并归档；必须保留 by-name 追溯 |
| workflow-registry | skill | 必选 | internal | 维护 Workflow 索引；SOP 内容仍由作者按模板直接修改 |
| resource-manager | skill | 必选 | internal | 修改 Skill/Agent 资源说明或注册新资源；不直接承担 Workflow 知识回写 |

### Input

Phase 1 的候选、文档计划、提交计划和用户明确确认。

### Output

已确认的 Experience 被 promote、回写并归档；批准的 Workflow/Skill/Agent 文档变更已落盘；`apply-receipt.md` 记录每项候选的 accepted/rejected/deferred 及目标文件。

### Quality Criteria

- 用户确认前不写正式资产；确认后只应用明确批准的条目。
- Experience frontmatter 和索引符合模板，回写目标存在，`experience_refs[]` 使用 by-name。
- Workflow 至少保持 Mission/Input/Output/Principles/Phase 运行结构；Required Resources 均可解析。
- 不把通用规则写进某家公司或某个项目的专属 profile；项目事实留在项目记录。
- 变更后立即记录受影响文件和原因，便于 Phase 3 读回。

### Known Issues

“同意”必须能映射到候选或文件范围；模糊同意只能继续生成更小的确认清单，不能扩大写入范围。归档是可追溯变更，删除资产仍需单独确认。

## Phase 3: sanitize-and-verify — 最终表面清理与验证

### Goal

从最终状态重新生成文档、提交说明和交付文案，清除会暴露工作过程的残留，并验证任务事实、路径、资源和测试均未被破坏。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| no-negative-echo | skill | 必选 | github · 2dfbefdc41f9f728984096850d90a61e20054923 | 后置清理和表面质量门；不能保证宿主自动激活，必须显式调用并读回 |
| research-quality-gate | skill | 按任务类型 | internal | 只在研究/视频/脚本等有对应冻结研究底稿时调用；不补研究 |

### Input

已应用的文档变更、`apply-receipt.md`、baseline、提交计划、验证命令、用户确认的必要事实。

### Output

- `validation-receipt.md`：结构、引用、测试、质量门、scanner、Git diff 的结果。
- `final-delivery.md`：从读回最终状态生成的交付说明。
- 冻结的 `commit-message.txt`，仅描述 task-owned 最终状态。

### Quality Criteria

- 先 preflight、冻结表面，再进行 mutation；mutation 后读回并 postflight。
- 使用 no-negative-echo scanner 扫描文档、commit message、handoff 和相关路径；scanner 通过后仍做语义审阅。
- 保留安全、准确、兼容、迁移、审计和实际外部事件等必要事实。
- 研究/视频产物如有对应质量门，必须读取其独立验收结果；不能只写“已检查”。
- 测试失败、未读回或无法扫描的表面必须阻断提交或明确进入 deferred。

### Known Issues

scanner 是精确项扫描，不识别所有语义改写；commit 和 handoff 必须由最终读回状态生成。无法观察宿主是否激活 Skill 时，只能声明“文件安装与脚本验证通过”，不能声称本轮自动激活。

## Phase 4: commit — 按范围创建本地提交

### Goal

只提交用户确认且验证通过的 task-owned 文件，为每个 Git 仓库生成可读、可复现、无会话残留的本地提交。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| no-negative-echo | skill | 必选 | github · 2dfbefdc41f9f728984096850d90a61e20054923 | 冻结并检查 commit message 与提交交付文案；不替代 Git diff 审查 |

### Input

用户确认的文件清单、通过验证的 `validation-receipt.md`、冻结的 `commit-message.txt`、baseline 和各仓库 Git 状态。

### Output

每个受影响仓库一个本地 commit；`commit-receipt.md` 记录仓库、commit SHA、提交文件、验证命令、保留的 pre-existing 修改和未执行的外部动作。

### Quality Criteria

- 只按批准文件清单 stage；提交前检查 staged diff 和 staged 文件名。
- commit subject 使用 Conventional Commits：`type(scope): imperative summary`。
- commit body 使用以下固定结构，内容来自最终状态：

  ```text
  Summary:
  - <accepted result>

  Validation:
  - <command or independent receipt>

  Scope:
  - <task-owned boundary>
  ```

- 不写“经过几轮修改”“没有采用某方案”等会话过程；只有真实 baseline 行为变化、迁移或审计需要时才说明变化。
- 不提交 `.omc/`、临时 staging、密钥、未确认文件或其他仓库文件。
- 本 Phase 只执行本地 Git commit，不 push、不建 PR。

### Known Issues

一个任务可能跨顶层仓库和项目仓库；必须分别 commit，不能在顶层仓库越界 stage `projects/*` 项目代码。提交失败时保留已生成的 receipt，报告准确状态，不重写用户已有修改。

## Phase 5: handoff — 交付与经验闭环

### Goal

把实际读回的最终状态交付给用户，并明确哪些经验已经沉淀、哪些候选延期、哪些仓库修改仍属于用户原有工作。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| no-negative-echo | skill | 必选 | github · 2dfbefdc41f9f728984096850d90a61e20054923 | 对最终 handoff 再做一次正向状态检查；不得隐藏实际外部事件或失败 |
| experience-curator | skill | 必选 | internal | 确认已归档 Experience 的回写目标和适用范围 |

### Input

`commit-receipt.md`、`final-delivery.md`、验证收据、归档 Experience 索引和各仓库最终状态。

### Output

用户可读的最终 handoff：结果、关键文件、commit SHA、验证证据、延期候选、仍保留的用户修改、未执行的外部动作。`final-delivery.md` 必须与实际读回一致。

### Quality Criteria

- 只报告最终状态和必要事实，不把内部草稿当成果。
- 每个 commit SHA 都能由对应仓库读回；文件链接/路径可解析。
- 明确 PASS、WARNING、DEFERRED 和 BLOCKED，不能用模糊的“基本完成”。
- Experience 只有在完成回写并登记归档后才报告为已沉淀；否则报告为候选。

### Known Issues

宿主可能需要新会话才能发现刚安装的外部 Skill；这不阻止使用已验证的本地 scanner，但必须如实说明“激活未观测”。
