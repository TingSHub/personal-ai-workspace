---
name: industry-cycle-analysis
description: 产业供需周期分析 Skill，触发词包括“产析skill”。用于研究行业、赛道或产业链的需求来源、有效供给、产能周期、价格/订单/库存/利润、资本开支、产业链传导和资本市场预期阶段，也用于判断行业在走上坡还是下坡、资本周期处于哪一段、热门风口是否已进入晚周期。适合半导体、AI算力、光通信、新能源、化工、钢铁、资源品、机器人、数据中心、电力、液冷等周期性或成长性行业；不要用于职业收入命中率预测、短线荐股、技术分析、K线预测、目标价或直接投资建议。
---

# Industry Cycle Analysis

## Core rule

Start from the real economy. Map market expectations only after the industrial chain, evidence coverage, and supply-demand conflict are clear.

```text
real demand -> buyer/budget/funding durability -> order quality -> effective supply
-> price/inventory/margin
-> capex -> qualified capacity -> cycle turn -> market expectation stage
```

Never convert a filled template into a confident conclusion. A missing metric is an evidence gap, not permission to write generic prose.

## Write for two audiences at once

Every full report must work for both readers:

1. **First-time reader**: after one pass of the main body they can retell the industry chain, who pays whom, representative companies, the current cycle stage, capital flows, and where money may go next. Requirements:
   - Main body (sections 0-10) comes first; all audit material (evidence ledger, data currency, readiness, execution record) goes to appendices.
   - Section 0 opens with a plain-language "这个行业是做什么的" before any cycle judgment.
   - Every jargon term or abbreviation used in the body appears in the `## 10. 术语表` section with a plain-language explanation.
   - Representative companies get real introductions (listing venue/ticker, position in the segment, production-control model, why representative) — never bare name lists.
   - All table headers and section labels are Chinese.
2. **Experienced reader**: the report must contain judgment they cannot get from a Wikipedia-level summary. Requirements:
   - Each of sections 1.2 (per node), 2, 3, and 5 carries a `进阶视角` block: calibration traps, the sharpest current controversy, prior-cycle comparison, or where nominal capacity dies before becoming effective supply. These blocks must state a position backed by evidence IDs, or explicitly record that no controversy was found and where you looked.
   - Section 8 must contrast the mainstream market narrative with this report's judgment and say whose evidence is harder. "无分歧" is acceptable only with the search trail recorded.
   - Prior-cycle comparison in section 5 names concrete years and lag lengths, or states honestly that no comparable prior cycle exists.

Anti-boilerplate rules (hard):

- No explanatory sentence may repeat 3+ times within one report. If you notice yourself reusing a sentence pattern across nodes or rows, the content is not yet researched — go back to evidence.
- Node explanations must describe the concrete action and output of that node ("把设计图变成硅片上的电路"), never circular definitions ("X负责把上游投入转成Y可采购的产品").
- Chain nodes are stages or actors, never products (焦炭 is a product; 焦化厂 is the node).
- Parallel inputs (equipment, materials, energy, software, finance) must appear as parallel branches in the mermaid chart, not be omitted or serialized.
- Every data period must be an explicit year-month or quarter; "最新已披露期" is banned.
- Watchpoint `指标` cells contain indicator names, never values.
- A full report contains at least four important chain nodes. For every `1.2.x` node, write separate labeled fields for `它是干什么的`, `向谁采购`, `卖给谁`, `怎么赚钱、议价能力`, `为什么会卡住`, a table with at least two representative companies/institutions, and an evidence-backed `进阶视角`. Never merge the supplier and buyer fields or repeat one sentence across them.

## Choose the research mode

- Use a **quick scan** for boundary clarification, a preliminary cycle hypothesis, or a short update. Keep the evidence table compact, but still label facts, inferences, assumptions, freshness, and gaps.
- Use **full research** when the user asks for a report, deep research, cross-chain comparison, or capital-market mapping. Load `references/report-template.md`, `references/quality-checklist.md`, `references/evidence-ledger.md`, and `references/capital-market-mapping.md` (the last is mandatory because sections 6-7 of the template require its attempt checklist).
- For agentic or multi-round deep research, also load `references/deepsearch-research-protocol.md`.
- For full research, always run the policy-materiality gate. Load `references/policy-materiality.md` when the gate is `是` or when the answer is uncertain.
- Load `references/framework.md`, `references/supply-demand-questions.md`, or `references/cycle-stages.md` only when that part of the analysis needs them.
- When the user asks whether an industry is rising or declining, invokes the capital cycle, treats capex or per-capita profit as a timing signal, or asks whether a popular theme is already late-cycle, load `references/capital-cycle-diagnostics.md`. Use it as a cross-check on the seven cycle stages, not as a replacement stage system.

## Synchronize time and release status first

1. Query the system time before collecting data.
2. Store the timestamp and timezone in the report.
3. Build a release-status list for the important sources and metrics.
4. Treat “latest” as the latest officially released value available at the analysis timestamp. Never infer that a quarterly report exists merely because the calendar entered the next quarter.
5. Distinguish full-quarter actuals, partial monthly actuals, guidance, plans, forecasts, and stale values.

Windows PowerShell:

```powershell
Get-Date -Format "yyyy-MM-dd HH:mm:ss zzz"
```

POSIX:

```bash
date "+%Y-%m-%d %H:%M:%S %z"
```

If Q2 monthly data exist but Q2 financial results have not been released, write “Q2 partial monthly actuals + Q1 financial actuals”; do not write “Q2 actuals covered”.

## Route and verify evidence

Before web research, load `references/search-routing.md`. Rank sources with `references/source-priority.md`.

Use this ladder:

```text
discovery -> open original -> verify metric and definition -> freshness check
-> contradiction search -> evidence ledger -> conclusion
```

Treat search snippets, generated summaries, reposts, and social posts as leads. Promote a claim to evidence only after opening an original or authoritative reproduction and recording its metadata and locator.

Public channel observations such as an e-commerce SKU price or availability can be evidence for that exact seller, SKU, price definition, and timestamp. They are not authoritative statistics for upstream pricing or industry-wide shortage. Load `references/source-priority.md` and `references/search-routing.md` before using them.

## Maintain an evidence ledger

Record every important claim using `references/evidence-ledger.md`.

- Set `opened=yes` only when the source was actually opened in the current research run or a preserved auditable run.
- Set `freshness=current` only after checking whether a newer release supersedes the source.
- Record publisher, publication date, access date, period, geography, unit/definition, locator, actual/forecast status, and limitations.
- Derive search rounds, tool routes, source counts, and completion status from the run. Never hard-code `Latest`, `Opened`, or `Complete` in a report generator.
- Keep industry evidence separate from market-pricing or narrative evidence.

## Apply the evidence-readiness gate

Assess these lanes before naming a cycle stage:

| Lane | Full-research minimum |
|---|---:|
| Industry chain and relationships | 2 opened reliable sources |
| Demand | 3 opened reliable sources |
| Supply and effective capacity | 3 opened reliable sources |
| Price/order/inventory/margin | 3 opened sources, or an explicit gap |
| Capital-market expectations | 2 opened sources, or a gap documented via the mandatory attempts below |

Rules:

- If demand, supply/effective capacity, or price/order/inventory/margin has a material gap, mark the cycle conclusion **provisional** and cap confidence at medium.
- If both demand and effective supply are unresolved, write `阶段待验证` rather than forcing a stage label.
- An explicit evidence gap is honest completion of a search subtask, but it is not positive evidence for the industry conclusion.
- Do not reuse one source as if it independently satisfied several unrelated lanes.

## Capital-market lane: mandatory attempts before declaring a gap

Declaring the capital-market lane a gap without trying is not allowed. Before writing any gap:

1. Load `references/capital-market-mapping.md` and actually attempt the free-source checklist there (index valuation percentile, sector ETF flows/shares, northbound/margin balances where applicable, leader price-vs-earnings divergence). Record every attempt and its outcome in the section-6 attempts table — including failures.
2. Whether or not quantitative data was obtained, section 6 must contain the qualitative paragraph: what the market has probably already priced, what it probably has not, and on what indirect evidence — clearly labeled as inference, never as measured fact.
3. When dated market prices and comparable earnings or cash-flow inputs are available, run the `隐含预期反推` in `references/capital-market-mapping.md`: infer the earnings, cash-flow, margin, utilization, or return-on-capital hurdle embedded in the current price, then compare that hurdle with industry evidence. Treat “price unchanged -> lower future PE” only as a sensitivity calculation, not proof of undervaluation. If the required inputs are unavailable, record the precise gap instead of inventing a hurdle.
4. Section 7 (未来资金可能流向) is mandatory: for each of the three scenarios in section 8's logic, state which chain node the profit pool would shift toward, which benefits first/later, derived from order lead times, qualification barriers, and capacity elasticity — never from price charts. Keep the no-buy/sell-advice disclaimer visible.
5. Only after steps 1-3 are recorded may the lane be marked gap, and the conclusion stays provisional.

### Use a layered proxy basket, not an impossible one-instrument test

No listed instrument is required to represent an entire industrial chain. Map market evidence in three layers and state the coverage boundary of each layer:

1. **Industry ETF or index**: broad narrative, valuation and fund-performance proxy.
2. **Sub-chain proxy**: an ETF, index or listed basket concentrated in the bottleneck node.
3. **Representative company**: price-versus-reported-earnings or order evidence for a named node.

For every usable proxy record `代理层级`, `工具/主体`, `覆盖节点`, `指标与期间`, `来源`, `结论`, and `局限`. A current NAV, dated total return, holdings weight, valuation multiple, shares outstanding, or same-date price-versus-earnings observation is usable market evidence when the original issuer, exchange, index provider, or company source was opened. A product's incomplete chain coverage is a limitation, not a reason to discard the observation.

If every attempt failed, name the exact pages opened and why each metric was unavailable. An all-gap attempts table cannot satisfy the market-evidence lane or receive a full evidence score.

## Model relationships explicitly

1. Define the industry boundary, adjacent industries, substitutes, and geography.
2. Represent important nodes and explicit edges: `from`, `relation`, `to`, and evidence IDs.
3. Do not infer suppliers and buyers from array adjacency. Equipment, materials, infrastructure, and finance often enter a production process in parallel.
4. Separate:
   - production/physical flow;
   - order and budget flow;
   - profit and cost-bearing flow.
5. For each important node, explain what it is, what it does, suppliers, buyers, representative companies, monetization, bottleneck role, and evidence.

For AI-related semiconductors, distinguish at least:

```text
AI use -> model/cloud budget -> data center/server -> GPU or ASIC + HBM
-> advanced packaging and test -> foundry
materials/equipment -> packaging/foundry capacity (parallel inputs)
```

## Execute the analysis

1. Define the boundary and explicit relationship graph.
2. Build the release-status list and research plan with a maximum of three search rounds per subtask by default.
3. Collect the latest available actuals for demand, supply/effective capacity, price/orders/inventory/margins, expansion timing, and representative companies.
4. Separate announced capacity from installed, qualified, yield-ramped, and customer-backed capacity.
5. Find the buyer and demand trigger; separate actual use from policy, restocking, capex, or expectation. Identify whether the buyer's budget is funded by operating cash flow, balance-sheet cash, debt, equity, or public funding, and name the observable condition that would tighten it.
6. Test order quality before treating backlog or long-dated schedules as demand support: distinguish deposits, binding long-term or take-or-pay contracts, cancellable orders, framework intentions, and undisclosed terms; look for duplicate or multi-supplier ordering.
7. Run the policy-materiality gate: answer `是` or `否`, give one evidence-backed sentence, name the transmission channel, and stamp the policy status date. If `是`, cover only jurisdictions that materially change demand, supply, price/profit, cost, trade flow, qualification, capital expenditure, or financing access; distinguish proposal, enacted rule, and executed funding. If `否`, do not pad the report with country-by-country `N/A` rows.
8. Locate the bottleneck or surplus and explain the transmission lag from demand to orders, revenue, margin, capex, qualified capacity, and reversal.
9. Preserve conflicting evidence and unresolved definitions instead of averaging them away.
10. Judge the cycle stage only after applying the evidence-readiness gate.
11. Map industrial reality to the market expectation stage without giving a buy/sell call. For cyclical industries, never interpret a PE percentile without calibrating current earnings, margin, price, inventory, and utilization against the cycle. When usable inputs exist, reverse-engineer the operating hurdle implied by the current price using a disclosed required return and terminal/exit assumption; compare the hurdle with demand funding, order quality, effective supply, margins, reinvestment, dilution, and the mid-cycle baseline. Do not turn the result into a target price.
12. Produce 3-5 falsifiable watchpoints with an actual source, baseline, frequency, direction, and numeric or event threshold.
13. When public data permits, preserve at least one real comparable time series: the same indicator, definition, unit, geography, and reporting entity across two or more dates. Never combine revenue, margin, inventory, forecasts, or different companies into a synthetic line. If no such series is available, write the precise evidence gap and the source to monitor next.
14. Keep the stage judgment separate from its epistemic status. Record `阶段判断`, `结论状态`, `置信度`, `证据截至时间`, `上调条件`, and `下调条件` as independent fields. A stage may be “扩张” while the conclusion remains “暂定”; the interface must never make these look like one label.
15. Build the cycle timeline from 4-6 industry-specific dated events or quarters. Mark each row as an actual, company plan, forecast, or risk window. The visible time label must carry meaning beyond a reused sequence of calendar years.
16. For capital-cycle questions, diagnose each relevant chain node separately. Normalize capex and return metrics, classify the direction of both, state the lag from spending to qualified supply, and name a falsifier. Never infer an industry or career outcome from capex plus per-capita profit alone.

## Write and validate the report

For full research:

1. Use `references/report-template.md` and preserve the exact header labels `分析日期`, `地理范围`, `数据时效`, and `行业边界`. Follow its section order: reader-facing body (0-10) first, audit appendices (A/B/C) last.
2. Separate facts, inferences, assumptions, and gaps.
3. Include the mermaid chain map with parallel inputs, at least four fully structured node explanations, representative-company tables with production-control models and two or more rows per node, the funding-durability row, order-quality and cancellation evidence or a precise gap, the policy-materiality gate, capital-flow attempts table, cycle-adjusted valuation calibration, an implied-expectation reverse test when usable inputs exist (otherwise a precise gap), layered market-proxy evidence, qualitative pricing paragraph, complete future-capital-flow scenarios, mainstream-vs-report contrast, watchpoints, the glossary, and either a comparable time-series table or an explicit time-series evidence gap. When `references/capital-cycle-diagnostics.md` is triggered, also include its compact cross-check block in section 5.
4. Do not use placeholders such as `官方/协会/公司`, `待按产品核验`, `市场可能交易`, `见数据时效表`, or a generic “连续两期改善”. Also banned as filler: `钱和订单从…的需求向前传`, `负责把上游投入转成…可采购、可验证的产品或服务`, `核心产品需求`, `新增场景`, `直接观测`/`交叉验证` as an entire interpretation cell, `最新已披露期` as a period, and reusing one identical Limitation sentence across every ledger row.
5. Run:

```bash
python scripts/validate_report.py path/to/report.md --mode full --strict
```

6. Use `references/quality-checklist.md` for the final substantive pass. A structurally valid Skill does not prove that a generated report is valid.
7. For a multi-report delivery, run `python scripts/validate_corpus.py <reports-directory> --pattern "??_*.md" --benchmark <benchmark-report> --strict` after every report passes the single-report validator. Corpus validation catches cross-report boilerplate and depth gaps that a single-file schema check cannot see.

## One industry, one research run

Never batch-generate reports for multiple industries by re-instantiating one filled report with different nouns. Each industry requires its own search rounds, its own evidence ledger, and its own chain map. Shared boilerplate across reports for different industries is a defect: if two reports contain the same explanatory sentence outside the fixed template scaffolding and 尾注, at least one of them was not researched.

## Optional export and cleanup

- If a PDF is requested, resolve the Skill directory first and run its `scripts/md_to_pdf.py`; do not assume the current working directory is the Skill directory.
- Create a task-specific temporary directory for downloads. Clean it only if temporary files were actually created, record those paths, and verify the resolved cleanup target stays inside that directory.
- Never wildcard-delete workspace or user data.

Keep these warnings visible in full reports:

```text
supply-demand gap != stock-price rise
correct direction != correct timing
earnings realization != continued stock rise
price unchanged -> lower future PE != undervaluation
capex growth != effective supply
per-capita profit != career outcome
AI answer != fact
stale data != current fact
```
