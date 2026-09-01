---
name: experience-curator
description: 从真实项目证据中筛选、去重和沉淀可复用 Experience，判定归属并回写 Workflow SOP 与 Skill/Agent 记录后归档。当用户说“沉淀经验”“记录踩坑”“项目复盘”“生成 experience candidate”时使用。
---

# Experience Curator

Experience Curator 是 Experience 的唯一维护入口，职责是反馈闭环（提炼 → 判定归属 → 回写 → 归档）。目标不是保存更多内容，而是让下一次项目改变行动、减少重复劳动或提高交付质量。

## 目录与模板

- 原始事实：`projects/<name>/logs/`，永不进入资产库
- 候选：`projects/<name>/experience-candidates/`
- 正式经验（在途）：`.ai/experiences/`，只存未完成回写的在途经验
- 归档经验：`.ai/archive/experiences/`，回写完成后移入
- 候选与正式经验都读取 `.ai/templates/experience.md.template`
- 目录位置区分 Candidate 与正式经验，不增加状态字段

## curate：生成候选

1. 读取项目日志、交付物和实际使用的 Workflow/Skill/Agent。
2. 只保留会改变未来 Workflow、资源选择、调用方法、质量检查或可复用脚本的结论。
3. 排除对话全文、普通命令输出、偶发错误、项目专属事实、无证据建议和可从官方文档直接重建的内容。
4. 搜索已有 Experience，优先合并或修订，不创建重复主题。
5. 按模板生成 Candidate，frontmatter 必填（`name` = 文件名 slug、`description` 一句话摘要 = 触发场景与行动、`type`、`status`、`owner`、`asset`、`tags`，字段清单从模板读取），正文写明适用/不适用范围、证据和验证时的资源 `installed_ref`。
6. 明确建议更新哪个 Workflow SOP 或 Skill/Agent 记录；不要越权直接修改其他资产。
7. **脚本化判定（常设）**：检查结论中是否有可机械化的检查/操作（引用可解析性、格式完整性、数字/禁用项出现、统计分布、口径一致性等）。凡"人工逐条核对"类操作，应生成通用脚本沉淀到对应 Skill/Agent 资源的 `scripts/` 目录（无 scripts 目录则创建），候选的回写目标中注明脚本。

## promote：确认后回写并归档

1. 必须获得用户明确确认。
2. 将 Candidate 追加到 `.ai/experiences/`（在途），并在 `.ai/experiences/README.md` 在途索引表登记一行（by-name / type / description / owner / 加入日期）。
3. 按 by-name 回写目标资产：Workflow SOP 的 Known Issues / Quality Criteria、skill.yaml / agent.yaml 注意事项，并回填 `experience_refs[]`（by-name 引用已归档经验）。
4. 回写条目只追加到目标资产带来源标记的分区（`## 回写条目（来源: {experience by-name}）`）；正文编辑/合并由 resource-manager 执行或复核，curator 与 resource-manager 不得同文件无分区直写。
5. **脚本化沉淀（与回写同步）**：对 curate 第 7 步判定的脚本，生成并保存到对应资源的 `scripts/` 目录。脚本规范：纯标准库、单文件、参数化输入（文件路径/清单）、退出码语义（PASS=0 / 有发现=1 / 用法错误=2）、docstring 含用法与输出说明；在资源描述层「辅助脚本」行登记（用途 + 使用时机）；经验文件的回写目标包含脚本路径。
6. 回写完成后将经验文件移入 `.ai/archive/experiences/`，同步维护索引：从 `.ai/experiences/README.md` 在途表删除该行，在 `.ai/archive/experiences/README.md` 归档映射表登记；`.ai/experiences/` 只存未完成回写的在途经验，不无限堆积。

## review / merge

- 检查经验是否仍能改变未来行动。
- 多条经验结论重复时合并，保留证据和适用边界。
- 外部资源更新后，不自动宣告旧经验失效；通过 `installed_ref` 判断是否需要真实项目复验。
- 删除或大幅改写已确认经验前取得用户确认。

## Validation

- 正式 Experience 有真实项目或交付物证据
- **frontmatter 必填**：`name` / `description` / `type` / `status` / `owner` / `asset` / `tags` 完整且符合模板字段清单；`description` 是检索相关性判断依据，不得空泛
- 在途经验在 `.ai/experiences/README.md` 索引有登记行，与文件 frontmatter（by-name / type / description / owner）一致
- 包含触发场景、可复用结论、未来行动、适用与不适用范围、关联资产
- 关联资源证据包含验证时的 `installed_ref`（能够取得时）
- 不包含 secret、原始日志或无行动价值的叙述
- 所有 experience_refs 使用 by-name 且目标存在
- 归档经验在 `.ai/archive/experiences/README.md` 有回写映射条目
- **脚本化检查**：结论中可机械化的检查/操作已生成脚本（纯标准库、参数化、退出码、docstring）并在资源描述层「辅助脚本」行登记；脚本经真实产物最小验证（至少一次 PASS 或命中场景）
