---
name: finance-content-engineering
description: 财经内容工程（workspace 共享 internal skill）——从研究资产生成选题候选（topic-gen：输入 research-intelligence/ → topic-options.md），把内容草稿优化为财经口播稿（script-polish：输入 draft-script.md → polished-script.md），内置财经化规则（事实约束/投资内容纪律/280 字口播规范）与三遍审校流程。当需要从研究资产做内容选题、把书面稿改写成财经口播稿、或对财经内容做事实与表达审校时使用。
---

# finance-content-engineering

## 作用

为财经研究内容提供：选题设计辅助（topic-gen）、口播脚本工程化处理（script-polish）、内容表达优化。

**不是**：研究 Agent、投资分析 Agent、Content Director Agent——只提供方法与流程，输出内容资产，不做内容决策。

## 来源

internal adaptation from huashu experiment（2026-08-15 实测）：提取 huashu-topic-gen 选题方法与 huashu-script-polish 三遍审校流程，重写为财经领域本地版本。不复制 huashu 原 SKILL（无明确 License、面向泛内容），方法以本地化模板沉淀。

## 两种工作模式

### 模式 A：topic-gen — 选题设计

**输入**：`research-intelligence/`（五类资产，优先）或 `research-summary/`

**流程**：

1. 从 `content-opportunity.md` 与 `conflict-map.md` 提取核心矛盾与故事线候选。
2. 从 `fact-map.md` 校验每个选题的支撑事实（来源、可信度分层）。
3. 从 `evidence-gap.md` 检查选题是否触碰未验证信息。
4. 生成 3-4 个**角度互斥**的选题候选。

**输出**：`topic-options.md`

字段：

- 主题方向
- 核心问题
- 叙事角度
- 支撑事实（含来源与口径）
- 风险提示（事实风险 / 合规风险）

### 模式 B：script-polish — 口播稿工程化

**输入**：`draft-script.md`

**流程**：三遍审校（见下）。

**输出**：`polished-script.md`

字段：

- 优化后的口播稿（含停顿 / 重音标注）
- 停顿建议
- 重音建议
- 数字朗读建议

## 财经化规则

### 事实约束

- 禁止：无来源数字、模糊增长描述（如「大幅增长」）、夸张收益表达。
- 所有重要数字必须：有来源、有时间范围、有口径说明。
- 估算 / 代理数据必须显式标注（回指 fact-map 可信度分层；PEG / 失真分位 / 已证伪记忆 / 未落地政策禁用）。

### 投资内容纪律

- 避免：标题党、绝对化判断（「必然」「稳赢」）、推荐买卖。
- 保留：Bull Case、Bear Case、不确定性表述。
- 结尾可留验证窗口（如「批价 1550-1600 + 2026Q3 报表」），不写投资建议。

### 口播规则

- 中文财经内容默认约 **280 字/分钟**（实测验证）。
- 过长句拆分，听觉理解优先（单句宜 ≤ 25 字）。
- 数字优化朗读：大数读法（「1.68 万亿」优于「16876 亿」），百分比直读。
- 专业术语保持准确，不因口语化牺牲准确性。

## 三遍审校流程

### Review 1：事实检查

- 数字回指 fact-map / 来源。
- 公司名称、时间、来源无误。
- 估算口径已标注。

### Review 2：表达检查

- 口语化程度（书面语 → 口头语）。
- 听觉理解（断句、节奏、是否适合朗读）。

### Review 3：传播检查

- 开头吸引力（钩子在前 3 句）。
- 信息密度（删冗余）。
- 节奏（长短句交替）。

## 验收

- 从研究资产生成选题候选：3-4 个，角度互斥，支撑事实可回指。
- 将内容草稿优化成财经口播稿：280 字/分、数字朗读标注、事实零漂移。
- 不代替 Content Director：只输出资产（topic-options / polished-script），不做内容决策。
