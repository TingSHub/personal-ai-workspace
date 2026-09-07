# research-quality-gate

> 管理资产：`.ai/skills/research-quality-gate/research-quality-gate.md`；安装实体：`.claude/skills/research-quality-gate/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | internal · workspace internal skill |
| installed_ref | internal |
| runtime | both |
| 调用入口 | $research-quality-gate 或 python3 .claude/skills/research-quality-gate/scripts/validate_research.py |
| 要求 | Python 3 标准库；研究阶段提供Research Intelligence Document；内容阶段提供同版研究底稿、策划、长短脚本、SRT、素材和evidence ledger |
| 更新 | internal · 随项目输出契约调整检查规则；保持只检查、不生成、不修复的边界；验证：运行Research Intelligence十章测试、旧聚合CLI回归与Content Layer独立输入测试，再用真实项目验证通过与拦截 |
| 辅助脚本 | scripts/validate_research.py（自动检查Research Intelligence十章、Evidence Ledger，以及内容结构、证据编号、跨文件数字、禁语、SRT和素材引用） |
| 经验引用 | research-master-content-pipeline |

## 作用

只验收上市公司研究交付物，不研究、不生成、不直接修复。执行实体位于 `.claude/skills/research-quality-gate/`，Codex 通过 `.codex/skills` 目录级映射加载。

## 注意事项与踩坑

- evidence ledger 可以是独立文件，也可以直接传入包含第 8 章证据链的母稿。
- 自动数字检查只识别阿拉伯数字；语义等价、中文数字和因果强化仍需人工复核。
- 比较数字前必须排除 SRT 时间码、字幕序号和脚本建议时长，避免把格式数字误报为母稿外事实。
- 同单位比较允许合理整数化，例如母稿 `453.06亿元` 与口播 `453亿元`；正负号由语句表达时按绝对值匹配，但语义复核仍要确认方向没有被改写。
- 每次更新数字归一化规则，都要保留一个合法交付物正例和一个注入母稿外数字的反例；只验证“能通过”不足以证明门禁有效。
- `PASS WITH WARNINGS` 不是最终放行，必须完成报告末尾的语义复核清单。
- SRT 没有最终配音时只能验证格式与时序，不能验证真实音画同步。
- `content_depth=deep_explainer` 还要语义检查 Knowledge Map、Historical And Market Relation、新闻事件线、价格—利润—市场预期关系和事实锚定幽默；缺失时退回研究或表达层，不在门禁内补写。

## 脚本

`scripts/validate_research.py` 的路径是安装实体内的相对路径；命令和参数见执行 Skill 的 `SKILL.md`。

### 补充规则

- 可以吸收外部 Skill 的方法约束而不强制采用其独立交付模板：例如公司母稿可吸收周期分析的证据门槛与置信度纪律，而不必嵌入一份完整周期报告。门禁检查同理——只校验所需证据纪律，不要求外部模板结构完整出现。
