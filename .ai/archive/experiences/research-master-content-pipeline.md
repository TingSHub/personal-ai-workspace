# Experience: research-master-content-pipeline

> 仅沉淀会改变未来项目流程、资源选择、调用方法、质量检查或可复用脚本的经验证结论。

## 来源项目与证据

- 项目：`investment-research-system`
- 运行记录：`logs/listed-company-research-video-production-ziguang-20260812.md`、`logs/listed-company-research-video-production-ziguang-v0.1.5-20260812.md`
- 交付证据：`outputs/紫光股份-Research-Master-Document.md`、`outputs/紫光股份-长短视频脚本.md`、`outputs/紫光股份-长视频字幕.srt`、`outputs/紫光股份-视频素材需求清单.md`
- V0.1.5 中间产物证据：`outputs/research_modules/industry-research-result.md`、`business-analysis-result.md`、`financial-analysis-result.md`、`valuation-result.md`、`investment-thesis.md`、`evidence-ledger.md`
- 验证资源：`industry-analysis@tree-sha256:a2a363fca3d9`、`buffett@investagent-tree-sha256:51aa7c2823bd`、`earnings-reader@v1.0.0`、`financial-fraud-index@tree-sha256:620e79e02f98`、`research-content-producer@internal`、`research-quality-gate@internal`
- 实测结果：20条证据记录被融合进单一母稿；脚本、65条SRT字幕和18项素材需求由母稿派生；V0.1.5 的六个研究模块均留下独立 Capability Result；门禁确认脚本55个、字幕51个关键数字存在于母稿，并用注入 `999.99亿元` 的反例夹具验证能够拦截母稿外新增数字。

## 触发场景

一个项目需要组合多个研究Skill/Agent，并在研究结果之上继续生成视频、文章、字幕、图表或其他内容产品时。

## 可复用结论

1. 多资源输出应被当作待验收的研究模块和证据，不应把各资源生成的完整报告直接拼接。独立报告通常具有不同章节、口径和事实截止日，拼接会制造重复与冲突。
2. 先完成证据台账并冻结 Research Master Document，再开始内容派生，能形成明确的事实边界。脚本需要新增事实时，应先回写并重新验收母稿，而不是直接加入脚本。
3. 下游一致性不能只靠人工阅读。至少自动检查：关键数字是否同时存在、证据编号是否可解析、SRT序号和时间码是否合法、素材数据是否回指母稿证据。
4. 可以复用外部Skill的方法约束而不强制采用其独立交付模板。例如公司母稿可吸收周期分析的证据门槛与置信度纪律，而不嵌入一份完整周期报告。
5. 无最终音频时生成的是估时SRT，不是发布级字幕；结构通过与音画同步是两种不同验收。
6. required resource 是否真实执行，不能只靠运行日志声明。最小证据必须同时包含资源 by-name、验证时的 `installed_ref`、该资源的原生或结构化执行产物，以及映射到 `required_outputs` 的 Capability Result；缺少任一项都不能把“参考过方法论”记作执行完成。
7. 下游只消费已验收的 Capability Result，能够把外部资源的真实贡献与主 Agent 的整合职责分开，避免主 Agent 在没有资源产物的情况下仿写结果。
8. 数字一致性自动检查必须排除SRT时间码、字幕序号和脚本时长，并容许同单位的合理取整与正负语义表达；自动检查通过后仍需人工复核新增因果、预测强化、风险弱化和画面暗示。

## 未来应采取的行动

1. Workflow保持顺序闸门：研究模块验收 → 证据台账 → 母稿冻结 → 脚本 → 字幕与素材，母稿冻结前不生成最终内容。
2. 每个脚本段落和素材项保留母稿章节或证据编号；发现母稿外事实时停止派生并回到母稿。
3. 对每次交付执行跨文件检查，至少覆盖证据引用、关键数字、SRT时间轴和必需交付物。
4. 字幕明确区分“估时稿”和“音频对齐稿”；有音频后重新生成或校准时间轴。
5. Workflow 每次 Capability 执行都声明独立 `capability_result`；执行记录保存 required resource、`installed_ref` 和产物位置，下游不得直接消费私有推理。
6. required resource 必须是 Capability 中的 execution 角色；若无法真实运行，应报告缺口或回退，而不是由主 Agent 模拟该资源完成。
7. 交付门禁保持“自动硬检查 + 人工语义复核”两层结构；门禁只报告并指向上游 Capability，不生成内容、不修复研究，也不引入评分或状态机。

## 适用范围

需要从同一研究事实源派生多种内容形态的上市公司研究、行业研究和知识型视频项目；尤其适用于多个外部资源共同提供证据、且需要证明 required resource 确实执行的任务。

## 不适用范围

不适用于一次性、无事实依赖的创意文案或没有稳定唯一内容源的开放式创作；自动数字匹配不能替代事实核验，也不能替代视频发布前的事实更新、版权审核、配音和音画对齐。

## 关联资产

- Workflow：`listed-company-research-video-production`
- Capability：`industry-research`、`company-business-analysis`、`financial-statement-interpretation`、`company-valuation-analysis`、`research-evidence-ledger`、`research-master-document-generation`、`investment-video-script-generation`、`video-subtitle-generation`、`video-material-planning`、`research-deliverable-validation`
- Agent：`research-content-producer`
- Skill：`industry-analysis`、`buffett`、`earnings-reader`、`financial-fraud-index`、`research-quality-gate`
