# finance-fraud-detector

> 管理资产：`.ai/agents/finance-fraud-detector/finance-fraud-detector.md`；安装实体：`.agents/finance-fraud-detector.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | agent |
| 来源 | github · https://github.com/jnMetaCode/agency-agents-zh（finance/finance-fraud-detector.md）|
| installed_ref | 70289a7fb030d5027ad824ae62823f9e7c8aa951 |
| runtime | both |
| 调用入口 | 按角色 system prompt 身份执行（人设型专家 agent，外部登记）——用于财务异常/舞弊风险筛查等具体任务执行 |
| 要求 | 按角色定义执行；输出需按本项目事实纪律核验（回指 evidence-reference 等） |
| 更新 | git · 从上游仓库更新对应文件，对比后替换安装实体；验证：加载角色完成一次最小任务 |
| 辅助脚本 | — |
| 经验引用 | — |

## 作用

专注交易欺诈检测与金融风险防控的分析专家，精通支付宝/微信支付/银联渠道的风控策略、反洗钱合规、电信诈骗识别、央行征信应用和互联网金融风控体系搭建，帮助企业守住资金安全底线。

## 实体位置（可加载定义）

- `.agents/finance-fraud-detector.md`——完整职责（人设背景/身份与记忆/核心使命/关键规则/技术交付物）

## 调用方式

- 作为专家角色加载执行对应领域任务（投资研究/财务分析/舞弊检测/内容创作/平台运营）
- 与 internal Director（决策层）职责分离：Director 负责决策与编排，本类 agent 负责具体任务执行

## 注意事项与踩坑

- 外部登记 agent（来源 agency-agents-zh，中文名「财务舞弊检测」），人设型定义——方法论与领域知识可复用，结论须按项目事实纪律核验。
- 投资/财务类输出不得直接作为研究事实源：事实以 research-materials/ 已验收产物为准（本类 agent 作执行补充）。
- 更新上游时注意格式差异（frontmatter name 为中文）。

### 补充规则

（无——外部登记，无本地经验回写）
