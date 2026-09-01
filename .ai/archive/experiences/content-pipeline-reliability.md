# Experience: content-pipeline-reliability

> 仅沉淀会改变未来项目流程、资源选择、调用方法、质量检查或可复用脚本的经验证结论。

## 来源证据

项目：investment-research-system；运行：Research Content Pipeline v0.2/v0.2.1 增量优化与可靠性验证（2026-08-15，紫光股份案例两轮）。证据：`experiments/listed-company-content-pipeline-v1/pipeline-v0.2-optimization-report.md`、`pipeline-v0.2.1-reliability-report.md`；产物 `outputs/companies/紫光股份/2026-08-15/content-assets/`。相关资源 installed_ref：research-intelligence-agent / investor-understanding-architect / information-visualization-architect（internal）。

## 触发场景

三层 Director Pipeline 执行与迭代；fact-map 分级、evidence-reference 生成、visual-brief 消费、visual-plan 数据回指等环节的质量检查。

## 问题与归属判定

- 问题：v0.2 实测发现事实层冲突未被显式标记（21.6 vs 21.0 亿）、visual-brief 引用超范围（博通 61.7% 无出处）、VD 存在隐式裁决与补数行为——需要契约约束与机械检查。
- 归属（owner）：三个 Director Agent 的执行契约（自检/引用约束/输入约束）与可复用检查脚本。

## 可复用结论（resolution）

1. **四级可信度（L4 隔离）有效**：统计派生/间接计算（估值倍数、分位、隐含反推、回测、TAM 测算）一律 L4——L4 与 L1 硬隔离后，"估值分位误作高可信必用"的 v0.1 缺陷消除；L4 只能作观点材料（观点卡/无刻度示意/脚注）。
2. **自检机制有效**：RD 输出自检（数字一致性 Conflict 块 + 来源完整性）暴露了 15 个冲突（12 个为新发现）——此前被隐式裁决/忽略的问题浮出水面；修正 3 处事实错误、取消 2 处自行裁决。冲突双值"保留不自动选择"是正确纪律。
3. **EV 引用闭环达成可追溯性**：evidence-reference 条目编号（EV-xxx）+ visual-brief 引用约束 + VD 引用可解析性检查——任何视觉元素可追溯到 fact-map 条目与研究来源；v0.2 的真实缺口（博通 61.7%）由上游 EV-049 修复形成闭环。
4. **双值视觉呈现纪律**：Conflict 双值以双值组件呈现（主值实线 + 副值灰化虚线 + 口径小标），副值不做主值放大动画——"不裁决"原则的视觉落实。
5. **机械检查应脚本化**：引用可解析性、来源完整性、Conflict 块格式、禁用数字出现均为纯机械检查——脚本化（各 Agent scripts/ 目录）后秒级完成，替代人工 grep，节省 token 与时间。

## 回写目标

- `research-intelligence-agent`（输出自检契约 + `scripts/check_factmap.py`）
- `investor-understanding-architect`（visual-brief 引用约束 + 脚本自检）
- `information-visualization-architect`（引用可解析性检查 + `scripts/check_ev_refs.py`）

## 适用范围

三层 Director Pipeline（research-intelligence → content-assets → visual-plan）的后续执行与迭代；同类"事实层 → 内容层 → 视觉层"信息流。

## 不适用范围

- 单层一次性内容生成（无多 Agent 链路时检查链价值降低）；
- Agent 契约已随版本变化时，需按新版本复验。

## 关联资产

- Agent: `research-intelligence-agent`、`investor-understanding-architect`、`information-visualization-architect`
- Workflow: `research-content-direction`
- Experience: [[content-director-validation]]
