# Experience: tushare-proxy-cashflow-distortion

> 仅沉淀会改变未来项目流程、资源选择、调用方法、质量检查或可复用脚本的经验证结论。

## 来源证据

项目：investment-research-system；运行：research-collection v0.3 贵州茅台实测（2026-08-15，industry-cycle-analysis 执行）。证据：`outputs/companies/贵州茅台/2026-08-15/research-materials/industry-cycle-analysis/白酒行业供需周期分析_20260815.md` 证据台账 E13；tushare 代理端点返回 `cashflow` 的 OCF 值 269 亿，与茅台 2026 半年报官方披露 706.91 亿**严重不符**，已弃用代理现金流数据、以官方披露为准。相关资源 installed_ref：tushare-connector（internal）。

## 触发场景

任何通过 tushare-connector 获取上市公司现金流数据（OCF/ICF/FCF 等）并用于研究、财务分析或跨期比较的任务。

## 问题与归属判定

- 问题：tushare 兼容代理的现金流字段存在与法定披露严重不符的情况（量级级偏差），仅靠字段勾稽无法拦截，直接引用会导致下游结论失真。
- 归属（owner）：`tushare-connector` 注意事项与踩坑。

## 可复用结论（resolution）

- 现金流类数据（尤其 OCF 总量）**不可直接信任代理返回**，关键现金流数字必须与法定财报（年报/半年报现金流量表）交叉核验后才能引用。
- 核验方法：取同报告期 `n_cashflow_act`（或官方披露 OCF）对照；偏差超过合理口径差异（如 <10%）即弃用代理值，改以官方披露为准并在产物中标注来源切换。
- 现有 `free_cashflow` 勾稽规则是衍生字段层防御，无法覆盖基础 OCF 总量失真，两层检查都需要。

## 回写目标

- `tushare-connector`（SKILL.md 注意事项与踩坑，追加条目）

## 适用范围

A 股上市公司研究/财务分析中所有依赖 tushare 兼容代理现金流数据的任务（含 tushare-connector 当前 internal 版本）。

## 不适用范围

- 已从法定披露原文（年报/半年报 PDF 正文）直接取数的任务（该路径不受影响）；
- 不涉及现金流字段的研究任务。

## 关联资产

- Skill: `tushare-connector`、`earnings-reader`、`financial-fraud-index`
- Workflow: `research-collection`
