# Experience: notes-spoken-polish

## 来源证据

- 项目：investment-research-html-mvp（2026-08-16，27 页 deck 的 `<aside class="notes">` 口语化改写）
- 运行记录：`logs/run-20260816-workflow-v1.md`（零漂移校验：3 处近似化修正 + 核验表）
- 相关资源 installed_ref：finance-content-engineering（internal）、html-ppt-skill（f3a8435）

## 触发场景

- 把书面/半书面 speaker script 改写成朗读友好（口播）版本时
- 任何「文本改写但事实必须零漂移」的内容生产环节

## 问题与归属判定

- 问题：口语化改写容易在表达优化的名义下**引入事实漂移**——实测 3 类陷阱：①近似化（36.1% 写成「超过三分之一」、15.03 写成「十五平方公里出头」、10 倍加「左右」）；②数字转中文读法有方言变体（70 会错转成「七零」，正确是「七十」；2 作首位且位权≥百用「两」：两百/两千/两万，但 22 是「二十二」不是「两十二」）；③年份/月份转时间指代（2025→去年）需确认指代对象。
- 归属（owner）：finance-content-engineering 记录（script-polish 的 notes 应用补充 + scripts/check-fact-drift.py 登记）；investagent-html-report-v0.1 workflow SOP P3

## 可复用结论（resolution）

- 口语化规则（直接更新 notes）：百分比直读（「营收负 1.2%」→「营收下降 1.2%」）、大数读法（892→八百九十二）、单句 ≤25 字、书面语→口头语；**数字转中文读法允许，近似化禁止**。
- **事实零漂移校验必须脚本化**：`finance-content-engineering/scripts/check-fact-drift.py`（新旧版本数字集合对比：removed 须为中文读法/时间指代、added 不允许、近似词对比式检测——「约→左右/大概」属等价组替换允许）。
- 近似词等价组：约/左右/上下/大概/差不多/将近 同组（等价口语替换不算新近似）；「出头」独立组。
- 「约/不到」等若在研究口径中本来就存在（如「约 863 亿」），不因口语化引入而报——对比式检测只报新版新增。

## 回写目标

- finance-content-engineering 记录：script-polish 补充「notes 应用」+ 辅助脚本登记 check-fact-drift.py（用途：口播稿改写零漂移校验）
- investagent-html-report-v0.1 workflow SOP P3 Known Issues（口语化陷阱 + 校验脚本）

## 适用范围

- finance-content-engineering script-polish 及任何口播稿改写流程；已归档经验 `multi-source-conflict-check` 的数字可信度原则延伸（零漂移是同一底线的改写下限）

## 不适用范围

- 创作型口播稿（从零写、无旧版可对比）——无漂移可比对
- 非中文内容（中文读法/指代规则不适用）

## 关联资产

- finance-content-engineering（脚本归属资源）；investagent-html-report-v0.1（Workflow by-name）
