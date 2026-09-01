# Capital Cycle Diagnostics

Use this reference when the user asks whether an industry is rising or declining, where it sits in the capital cycle, when a popular theme may be turning, or proposes capex and per-capita profit as timing signals.

Capital-cycle analysis is a supply-side cross-check on the main supply-demand framework. It does not make demand irrelevant and it does not replace the seven stages in `cycle-stages.md`.

## Decision boundary

- Diagnose an industry or chain node; do not claim a 70% or other career-income prediction rate without a dated, leakage-free, out-of-sample dataset.
- Keep industry direction, company returns, market pricing, and career outcomes separate. A clearing phase can suit an asset buyer while remaining hostile to employees.
- Treat `涌入 / 狂热 / 崩盘 / 继承` as narrative shorthand. Map evidence to introduction, growth, shortage, expansion, earnings realization, oversupply, or clearing.

## Run the diagnostic

1. Fix the chain node and geography. `AI`, `computer`, or `semiconductor` is too broad until the payer, product, capacity owner, and buyer are named.
2. Establish funded demand: actual use, budget owner, funding source, order quality, cancellability, and the observable condition that would tighten spending.
3. Normalize capex before comparing dates or firms.
4. Trace capex through construction, installation, qualification, yield ramp, and customer-backed output. Only the last qualified steps change effective supply.
5. Normalize the return proxy and confirm the numerator and denominator are comparable.
6. Compare capex direction, return direction, price, utilization, inventory, and order quality. The two-axis result narrows the hypothesis; it does not identify a unique stage.
7. Contrast industrial evidence with public attention, financing, valuation, admissions, or other lagging narrative signals when they are relevant.
8. State the stage hypothesis, evidence status, lag, and falsifier separately.

## Node-relative meaning

The same expenditure can have opposite meanings at different nodes:

| Observation | For the spender | For its supplier | Required interpretation |
|---|---|---|---|
| Hyperscaler data-center capex | Cloud-compute supply expansion | Demand for accelerators, HBM, networking, power and cooling | Analyze each node separately |
| Foundry capex | Future wafer supply | Demand for semiconductor equipment and materials | Follow installation, yield and customer qualification |
| Utility grid capex | Network supply expansion | Demand for transformers, switchgear and cables | Check funding, tenders, delivery and energization |

Do not call one aggregate capex number “industry supply” without naming the node.

## Normalize capex

Record all applicable fields:

- reporting entity, period, currency and fiscal/calendar-year basis;
- actual expenditure, cash paid, asset additions, finance leases, or management guidance;
- growth/expansion capex versus maintenance/replacement capex; if undisclosed, mark it `未拆分`;
- owned construction, joint venture, contracted capacity, lease, office/land, software/intangibles, logistics or non-core assets;
- funding from operating cash flow, cash reserves, debt, equity, public funds or supplier financing;
- announced, funded, under construction, installed, qualified, yield-ramped and customer-backed status.

Comparing unlike capex definitions is an evidence gap. Do not solve it by choosing the larger number.

## Normalize return proxies

Prefer node-level ROIC, operating margin, gross margin, free cash flow, unit profit, price-cost spread and utilization. If per-capita profit is used, record:

- profit total, operating profit, net profit, or adjusted profit;
- average employees versus period-end employees;
- consolidated group, segment, above-scale firms, listed-company basket, or another population;
- entry/exit of firms, acquisitions, outsourcing, layoffs and statistical revisions;
- same definition, unit, geography and reporting population across dates.

Per-capita profit can rise after layoffs and fall after hiring ahead of demand. It is an efficiency proxy, not a direct measure of wages, job openings, or career prospects.

## Two-axis cross-check

| Capex direction | Return direction | Working hypothesis | What must be checked next |
|---|---|---|---|
| Rising | Rising | Shortage, healthy expansion, or earnings realization | Whether qualified capacity is catching demand and whether returns exceed the cost of capital |
| Rising | Falling | Cost front-loading, late expansion, or emerging overbuild | Price, utilization, inventory, cancellations, financing strain and capacity-release dates |
| Falling | Falling | Clearing or structural demand decline | Whether capacity exits faster than funded demand and whether prices stabilize |
| Falling | Rising | Consolidation, harvest, mix improvement, or layoff-driven efficiency | Volume, market share, free cash flow and whether the improvement is repeatable |

Never write `capex up = industry up` or `capital flight = best entry`. Require price/order/inventory/margin evidence and a decision-specific horizon.

## Detect a popular theme turning down

Treat the late-cycle hypothesis as stronger when several of these divergences persist for at least two comparable releases:

- public attention, financing or admissions remain high while order growth slows;
- installed capacity rises while utilization, delivery time or price falls;
- revenue still grows while margin, ROIC or free cash flow weakens;
- inventory and cancellations rise while management maintains headline capex;
- capex funding shifts from operating cash flow toward debt, leases, equity or public support;
- leading firms delay projects while weaker entrants continue building;
- the market narrative relies on announced capacity or total addressable market rather than qualified output and funded demand.

These are hypotheses, not a vote-counting model. Weight evidence by definition, freshness, node coverage and causal proximity.

## Report block

When this reference is triggered, add one compact block in section 5. Use bullets rather than a second table so the canonical cycle timeline remains unique.

```markdown
### 5.x 资本周期交叉校验

- 观察节点：[specific chain node(s), not a whole-theme label]
- 资本开支方向：[direction + exact period + evidence IDs]
- 资本开支口径：[cash paid / asset additions / leases / guidance; entity, fiscal basis and inclusions]
- 资本开支性质：[growth / maintenance / replacement / mixed / undisclosed]
- 回报代理：[ROIC / margin / FCF / unit profit / per-capita proxy + period + evidence IDs]
- 口径可比性：[what is comparable; exact gap when it is not]
- 供给兑现时滞：[spend -> installation -> qualification -> yield -> customer-backed output]
- 交叉判断：[which two-axis hypothesis is supported, what other evidence agrees or conflicts]
- 反证条件：[numeric or event condition that would invalidate the diagnosis]
```

Keep the stage judgment separate from conclusion status and confidence. If capex or return definitions are not comparable, write `资本周期交叉判断：证据不足` rather than forcing a quadrant.
