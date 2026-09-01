# Policy Materiality Gate

Use this reference only when a full report's policy gate is `是` or the answer is uncertain. The gate prevents two opposite errors: silently omitting policy in policy-driven industries, and padding every report with a mechanical country list.

## Decide `是` or `否`

Answer `是` only when an enacted, funded, or actively executed policy materially changes at least one current cycle variable:

- end demand, procurement eligibility, or buyer economics;
- effective supply, qualification, permitting, or operating constraints;
- regulated price, reimbursement, profit pool, cost, tax, subsidy, tariff, quota, or trade flow;
- capital expenditure timing, financing, or localization.

Answer `否` when the current cycle is mainly explained by commercial demand, inventories, technology, weather, commodity economics, or company capital discipline and policy is only background noise. `否` means the policy channel was checked; it does not mean policy never affects the industry.

## Evidence and status rules

- Give one sentence explaining the decision and cite its evidence IDs.
- Record `政策状态截至` with a date and timezone.
- For `是`, cover only materially relevant jurisdictions. Do not force China, the United States, Europe, Japan, and Korea into every report.
- Label every item `提案`, `已立法`, `已发布规则`, `已执行`, or `已拨付`. Do not merge these states.
- Quantify the economic effect when the source permits: funding, tax rate, tariff, capacity target, procurement rule, eligibility threshold, or implementation deadline.
- Separate announced targets and budget envelopes from awarded, disbursed, installed, qualified, or operating outcomes.
- Prefer government, regulator, legislature, or official program pages. Industry or company sources may explain transmission, but should not be the only proof of a legal status.
- Write only verifiable economic effects and implementation gaps. Exclude political evaluation, national-value judgments, and geopolitical speculation.

## Report shape

Always write the four gate fields:

```markdown
### 2.1 政策重要性闸门

- 政策是否实质驱动当前周期：是 / 否
- 判断依据：[一句话 + 证据 ID]
- 主要作用通道：[需求 / 供给 / 价格与利润 / 成本 / 贸易流 / 资本开支 / 融资与资本准入 / 认证与经营准入，可多选]
- 政策状态截至：[YYYY-MM-DD HH:mm:ss 时区]
```

When the answer is `是`, add one table:

```markdown
| 国家/地区 | 政策或工具 | 状态与截至日期 | 影响环节 | 可核实经济效应 | 落地差或局限 | 到期/反转风险 | 证据 |
|---|---|---|---|---|---|---|---|
|  |  | 已立法/已发布规则/已执行/已拨付，截至 YYYY-MM-DD |  |  |  |  | E_ |
```

When the answer is `否`, stop after the four fields. Do not add an empty table or `N/A` rows.
