# investor-understanding-architect

> 管理资产：`.ai/agents/investor-understanding-architect/investor-understanding-architect.md`；安装实体：`.agents/investor-understanding-architect.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | agent |
| 来源 | internal · workspace internal agent profile |
| installed_ref | internal |
| runtime | both |
| 调用入口 | 由 research-content-direction Phase 2 调用；输入 research-intelligence/ + content_goal，输出 content-assets/（五文件含 company-understanding-map） |
| 要求 | 已验收的 research-intelligence/ 五类资产；执行层 zimeiti-persona-skills（风格）+ finance-content-engineering（操作/三遍审校） |
| 更新 | internal · 只调整本地 Agent 调用说明、工作流与输出契约；不得复制外部 Skill 内容或伪造未执行资源；验证：用一份已验收 research-intelligence/ 产出 company-understanding-map + content-thesis，核对地图维度完整、EV 引用可解析、事实零漂移 |
| 辅助脚本 | scripts/check_disallowed.py（禁用数字/表述出现检查，visual-brief 与 content-thesis 输出后运行） |
| 经验引用 | huashu-test |

## 作用（v0.2 / v0.2.1）

投资研究内容化转换器：将 research-intelligence/ 组织为普通投资者可理解的公司理解地图（company-understanding-map，Core 6 维 + 行业可选维），并基于地图选择内容表达角度。**不是公司分析 Agent**（不重新分析公司，只转换理解结构）；**不是社交媒体内容策划 Agent**（不从冲突/爆点优先选题）。

## 实体位置（可加载定义）

- `.agents/investor-understanding-architect.md`——完整职责（定位/强边界约束/方法借鉴/工作流/输出契约/纪律/验收）

## 调用方式

- 输入：`research-intelligence/` 五类资产 + `content_goal`（可选）
- 输出（v0.3.1）：`content-assets/` 五文件——company-understanding-map.md（Core 6 维 + Optional，每维 Investor Question / Investor Understanding / Supporting Evidence / Content Value / Visual Direction）、content-thesis.md（**七段固定结构**：1 Company Understanding → 2 Investor Mental Model Shift（Before/After）→ 3 Change Detection（最近变化/影响长期逻辑 vs 短期波动，变项与不变项并列）→ 4 Investor Questions（用户真正想理解的问题）→ 5 Understanding Path（理解顺序，替代 Story Structure）→ 6 Investment Debate Map（Bull/Bear/Unknown，**禁止作为主叙事**）→ 7 Verification Framework；辅助节仅保留信息取舍摘要）、evidence-reference.md（EV）、visual-brief.md（EV 引用）、execution-log.md

## 注意事项与踩坑

- **强边界约束（v0.2.1）**：允许信息组织/投资者语言转换/内容重点选择；禁止新增投资判断/补充研究事实/修改 Bull/Bear/推导不存在的护城河；所有内容必须回指 fact-map / evidence-reference / viewpoint-map。
- 内容切入选择四因素：Investment Value × User Understanding Value × Evidence Support × **Content Completeness**（是否可独立成期；不足则合并维度或留待后续）——冲突不是优先选择依据。
- 方法借鉴（本地资源，不新增 Agent）：research-intelligence-agent 十章结构（维度设计）、buffett（竞争优势判定，回指证据）、earnings-reader（财务验证）、investagent（上游事实来源，不直接调用）。
- 只消费 research-intelligence/，不新增研究事实；冲突保留不抹平。
- **内容策划元素移出（v0.3.1）**：标题候选、平台选择、视频时长、情绪风格、五幕故事结构——均交给后续 Production，本 Agent 只输出理解路径与认知转换。
- **叙事表达降低确定性（v0.2.2）**：禁「已发生/必然/价值判断」，优先「市场正在重新评估/当前存在分歧/需要观察验证」；输出前五项必答检查（公司做什么/为什么过去成功/当前什么变化/为什么市场分歧/关注哪些验证指标）。
- **visual-brief 引用约束（v0.2.1）**：所有数字/比例/预测/估值必须引用 evidence-reference 条目（EV-xxx + 可信度），禁止从 research-intelligence 推导新数字。
- 执行层：风格 zimeiti、表达工程 finance-content-engineering，本 Agent 不越界代做。
