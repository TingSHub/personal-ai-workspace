# Workflow: closeout-and-commit

> 位置: `.ai/workflows/task/closeout-and-commit/`

## Mission

通过显式 `$closeout` 把已完成任务转化为结构清晰、经验可复用、范围可审计的本地 Git 提交。先验收任务与目录结构，再生成逐项审批提案；只有用户批准后才整理目录、回写正式资产或提交。流程服务整个单仓库 workspace，不负责 push、PR、发布或外部消息。

## Input

- 必填：显式 `$closeout` 调用、当前任务目标、正式产物、验收证据和当前工作目录。
- 必填：运行模式；未指定时为 `review`。`apply` 必须带有可映射到稳定提案 ID 的用户批准。
- 可选：任务拥有的文件、排除项、允许保留的结构例外和需要蒸馏的对话或日志。
- `commit-only` 可跳过经验蒸馏；`distill-only` 不执行目录 mutation 或 Git commit。

## Output

- 默认：review、审批提案、验证结果和最终 handoff 直接返回当前对话，不创建 staging 或 receipt 文件。
- 可选：只有用户明确要求审计留痕时，才写入 `baseline.md`、`directory-review.md`、`approval-proposal.md` 或 action receipts。
- apply：只为实际执行且用户要求留痕的动作增加 receipt；canonical asset 和 Git commit 仍按批准写入。
- 不创建未使用阶段的占位文件，不把普通对话输出复制进资产库。

## Principles

- 显式入口：只有 `$closeout` 启动本 Workflow；普通“提交/结束”措辞不能替代显式调用或 mutation 批准。
- 先建议、后批准：review 不移动、删除、归档、写 canonical asset、stage 或 commit。
- 分项授权：提交范围、目录动作、Experience、文档回写和 commit 使用稳定 ID 分别批准；模糊同意不扩大范围。
- 单仓库边界：workspace 顶层 Git 是唯一仓库；`projects/*` 是同一仓库内的子项目，不分别 commit。
- 目录质量是提交门：同时检查归属、生命周期、命名、重复、可发现性和扩展结构；vendor/runtime 体积本身不是重组理由。
- 真实执行留痕：Required Resources 必须真实执行并在对话中给出可核验结果；只有用户要求审计记录时才落盘独立产物。
- 经验只沉淀未来会改变行动的结论；项目事实和普通日志留在项目执行记录。
- by-name 引用：Workflow、Skill、Agent 和 Experience 使用稳定名称。

## Phase 0: baseline-and-completion — 冻结范围并确认任务完成

### Goal

冻结 HEAD、工作树和 task-owned 范围，并在治理与提交前确认请求的工作已经完成。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| closeout | skill | 必选 | internal | 显式路由、模式与审批边界；不替代任务自己的质量门 |

### Input

任务目标、最终产物、验证证据、Git 状态、用户提供的范围与排除项。

### Output

对话中的 baseline 摘要：HEAD、工作树快照、task-owned 候选、pre-existing 修改、排除项、完成度与阻断项；用户要求留痕时才写 `baseline.md`。

### Quality Criteria

- 任务必需产物存在且相应验证已执行；失败或缺失记为 BLOCKER。
- pre-existing 修改与本次任务修改分开记录；未知归属不进入批准清单。
- 本阶段不修改文件、不 stage、不 commit。

### Known Issues

对话上下文不足以判定文件归属时，只生成待确认项；不能以“当前工作树里存在”为依据认领文件。

## Phase 1: structure-and-knowledge-review — 目录审查与按需蒸馏

### Goal

扫描机械结构问题并进行语义目录审查；仅在存在真实可复用反馈时生成 Experience 和文档候选。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| closeout | skill | 必选 | internal | 执行只读扫描与语义结构审查；扫描器不判断业务归属 |
| experience-curator | skill | 按模式 | internal | review/distill 且有真实证据时生成候选；无复用结论时应明确跳过 |
| cangjie-skill | skill | 可选 | internal | 仅用于长对话或长日志蒸馏，不再作为每次提交的固定成本 |

### Input

已验收的 `baseline.md`、任务产物、相关父目录、控制目录、引用和可追溯反馈。

### Output

- 对话中的 directory review：扫描结果和语义审查，分为 BLOCKER、RECOMMENDED、OPTIONAL、ACCEPTED_EXCEPTION；用户要求留痕时才写 `directory-review.md`。
- 可选 Experience candidates 和文档回写候选，各自包含证据、owner、目标资产与未来行动。

### Quality Criteria

- 每个目录建议包含当前位置、建议位置、理由、受影响引用、风险和是否阻断提交。
- 检查归属、source/generated/runtime/archive 生命周期、命名、重复、发现入口和后续同类扩展方式。
- 外部安装实体、虚拟环境、缓存和大型依赖不因体积或深度被误判为应移动。
- 没有会改变未来行动的结论时，不创建 Experience 占位文件。

### Known Issues

确定性扫描只能发现高置信度事实；扩展性和归类准确性必须结合任务语义审阅。

## Phase 2: approval — 生成统一逐项审批提案

### Goal

把任务文件、目录动作、经验、文档回写、延期事项和 commit 授权汇总为可精确批准的清单。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| closeout | skill | 必选 | internal | 生成稳定提案 ID 并阻止模糊授权扩张 |

### Input

通过验收的 baseline、directory review 和可选知识候选。

### Output

对话中的 approval proposal：至少分为文件范围、目录动作、Experience、文档写入、延期与本地 commit 六类；用户要求留痕时才写 `approval-proposal.md`。

### Quality Criteria

- 每个 mutation 都有独立稳定 ID；move、merge、archive、delete 不合并为一个泛化动作。
- 提案明确哪些是阻断项以及不批准的后果。
- review 和 distill-only 到此停止并把选择交给用户。

### Known Issues

“同意”“继续”等无法映射到具体 ID 时，必须请求更精确选择，不能默认全选。

## Phase 3: apply-and-postflight — 应用批准项并重新验证

### Goal

仅执行明确批准的动作，然后从最终状态重新检查目录、引用、测试、secret 和 Git 范围。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| closeout | skill | 必选 | internal | 执行范围保护、结构复扫和 staged diff 门禁 |
| experience-curator | skill | 按批准项 | internal | promote、回写并归档已批准 Experience |
| resource-manager | skill | 按批准项 | internal | Skill/Agent 资源登记、修改、脚本和引用验证 |
| work-for-me | skill | 按批准项 | internal | Workflow SOP/索引与 Required Resources 解析验证 |
| no-negative-echo | skill | 可选 | github · 2dfbefdc41f9f728984096850d90a61e20054923 | 对长迭代后的正式表面做清理；普通小提交无需固定调用 |

### Input

明确批准的提案 ID、上游验收产物和任务质量门。

### Output

`apply-receipt.md` 与 `validation-receipt.md`：逐项结果、最终路径、引用更新、测试、结构复扫、secret 检查和 diff 范围。

### Quality Criteria

- 只执行批准 ID；目录移动使用可恢复方式并同步已识别引用。
- mutation 后重新运行结构扫描、引用检查、任务测试和 `git diff --check`。
- unresolved BLOCKER、secret、测试失败、陈旧引用或范围歧义阻断 commit。
- staged 文件集合必须严格等于批准集合；未批准和 pre-existing 修改保持不动。

### Known Issues

归档和删除不是同一动作；删除仍需独立批准。无法验证的外部状态必须报告为 deferred 或 blocked。

## Phase 4: commit-and-handoff — 本地提交与最终交付

### Goal

仅在明确批准 commit 且 postflight 通过时创建一个本地提交，并交付可读回的最终状态。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| closeout | skill | 必选 | internal | staged 范围、提交授权和最终读回门禁 |

### Input

通过验证的 receipts、批准的 commit ID、冻结的最终提交说明和 staged diff。

### Output

`commit-receipt.md` 与最终 handoff：commit SHA、文件清单、验证证据、延期项、保留的 pre-existing 修改和未执行的外部动作。

### Quality Criteria

- commit subject 使用 `type(scope): imperative summary`，正文只描述最终结果、验证和 task-owned 范围。
- `git diff --cached --check` 通过，staged 文件与批准清单一致。
- commit SHA 可读回；只创建本地 commit，不 push、不建 PR。
- 完成后 workspace 级 closeout 只归档必要收据，不保留空阶段和重复对话副本。

### Known Issues

用户批准目录或知识变更不等于批准 commit；缺少独立 commit 授权时停在已应用、未提交状态。
