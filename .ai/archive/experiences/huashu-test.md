# Experience: huashu-test

> 仅沉淀会改变未来项目流程、资源选择、调用方法、质量检查或可复用脚本的经验证结论。

## 来源证据

项目：investment-research-system；运行：research-content-direction Phase 2 补充测试（2026-08-15，贵州茅台案例）。证据：`outputs/companies/贵州茅台/2026-08-15/content-assets/content-thesis/huashu-test/`（topic-gen-output.md 4 个互斥选题、script-polish-output.md 370 字口播稿 @280 字/分 ≈79 秒、huashu-fit-assessment.md）。被测资源：huashu-skills（alchaincyf/huashu-skills，无 LICENSE），相关资源 installed_ref：finance-content-engineering（internal，本次测试结论的产物）。

## 触发场景

- 内容生产需要选题设计与口播稿工程化方法时；
- 评估外部内容创作 skill 是否纳入本地系统时（尤其无 LICENSE 或面向泛内容的候选）。

## 问题与归属判定

- 问题：huashu-skills 的 topic-gen 选题方法与 script-polish 三遍审校流程实测有效，但无明确 LICENSE、面向泛内容，直接复制会引入合规与领域错位风险。
- 归属（owner）：`finance-content-engineering`（本地财经化重写 Skill）。

## 可复用结论（resolution）

- **方法提取有效**：topic-gen 选题模板（角度互斥 + 优劣分析）、script-polish 三遍审校流程（事实→表达→传播）可移植到财经领域；实测产出 4 个互斥选题与 79 秒口播稿，数字零漂移。
- **财经化改造要点**：补事实保真层（支撑事实回指 fact-map 可信度分层）；语速参数化 280 字/分（非英文 150 词/分）；术语保留 + 数字直读（大数读法）；过滤标题党公式与作者个人风格绑定；选题模板增加"事实风险"字段（原模板缺失）。
- **排除项**：`huashu-research` / `huashu-info-search`（多轮搜索新增事实，违反「研究底稿为唯一事实源」约束）；原 SKILL 整体照搬（无 LICENSE，改走本地化重写）。
- **分层互补**：huashu 类技能定"怎么落地动作"（操作层），与 zimeiti 类风格库定"写什么调性"（风格层）互补不冲突。

## 回写目标

- `finance-content-engineering`（skill.yaml 的 experience_refs 已引用本经验；SKILL.md 来源说明「internal adaptation from huashu experiment」）

## 适用范围

A 股财经内容生产中的选题设计与口播稿工程化；finance-content-engineering（internal）调用场景。

## 不适用范围

- 非财经泛内容创作（可参考原 huashu-skills）；
- 需要新增研究事实或联网补数据的场景（唯一事实源约束）。

## 关联资产

- Skill: `finance-content-engineering`、`zimeiti-persona-skills`
- Workflow: `research-content-direction`
