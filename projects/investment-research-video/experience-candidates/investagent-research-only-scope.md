# Experience: investagent-research-only-scope

## 来源证据

- 项目：investment-research-html-mvp（2026-08-16 运行，贵州茅台 600519）
- 运行记录：`logs/run-20260816-workflow-v1.md`（执行状态：TradingAgents 4 次尝试未产出完整决策、QuantDinger Docker 不可用降级；两者产出均被内容边界排除）
- 相关资源 installed_ref：investagent（tree-sha256:51aa7c2823bd）、industry-analysis（tree-sha256:a2a363fca3d9）、industry-cycle-analysis（tree-sha256:9e9b5dd25f8e）

## 触发场景

- 内容生产类项目（企业研究/内容页面）需要调用 investagent 获取公司研究，但最终产物禁止买卖建议/交易策略时
- 任何「研究结论用于内容呈现而非投资决策」的链路

## 问题与归属判定

- 问题：investagent 完整流水线约 40% 模块（TradingAgents 多Agent决策、QuantDinger 回测、买点判定/卖出清单）产出的是内容边界明确禁止的内容（持有建议、目标价、交易策略）。本轮中途才调整范围，导致 agent 已花费约 30 分钟尝试执行被排除的模块（4 次 TradingAgents 尝试均失败或产出无用结论）。
- 归属（owner）：investagent skill 记录（注意事项/回写条目）；investagent-html-report-v0.1 workflow SOP P1 Known Issues

## 可复用结论（resolution）

- 在内容生产链路中使用 investagent 时，**启动即限定执行范围**：只跑「研究+数据」模块（Buffett 定性评估、UZI 22 维数据采集、tushare 财务/行情采集），跳过 TradingAgents 决策与 QuantDinger 回测——不跑完再裁剪。
- 被排除模块不占用执行预算：TradingAgents 本环境（无 FRED key、Yahoo 限流）成功率低且产出对内容无价值。
- findings-summary 边界同步收敛：无决策/回测结论，执行状态如实标注「按项目内容边界排除」。
- 若未来确需决策结论（投资决策类项目），再单独以完整模式运行——范围选择是项目属性，不是 skill 缺陷。

## 回写目标

- investagent Skill 记录的现有注意事项/补充规则分区；回写时合并内容并通过 `experience_refs[]` 保留来源
- investagent-html-report-v0.1 workflow SOP Phase 1 Known Issues（已随 v0.1 写入）

## 适用范围

- 企业研究内容生产链路（HTML/内容页面为最终产物）
- investagent installed_ref tree-sha256:51aa7c2823bd 及后续版本（模块结构未大改时）

## 不适用范围

- 投资决策类项目（需要 Hold/Buy/Sell 结论与回测验证的完整模式）
- investagent 模块结构发生重大变化（如决策模块独立成 skill）后需重新验证

## 关联资产

- investagent-html-report-v0.1（Workflow by-name）
- industry-research-methodology、investagent-module-runtime-issues（既有经验，本经验为范围维度补充，不重复运行时问题）
