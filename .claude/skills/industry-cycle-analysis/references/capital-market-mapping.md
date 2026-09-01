# Capital Market Mapping

Use this reference only after the industry-chain logic is clear. Loading this file is mandatory for full research: sections 6 (资金动向) and 7 (未来资金可能流向) of the report template depend on the checklists below.

## Core Warning

The stock market trades expectations, not just current reality.

```text
supply-demand gap != immediate stock rise
correct industry direction != correct timing
real shortage != unpriced opportunity
earnings realization != continued re-rating
low cyclical PE != cheap without normalizing earnings
price unchanged -> lower future PE != undervaluation
```

## Cycle-adjust valuation before interpreting it

For a cyclical industry, a low PE can coincide with peak earnings and a high PE can coincide with depressed earnings. Never use a static PE or PE percentile alone to label an industry cheap or expensive.

Every full report records an `估值口径校准` paragraph that:

- states whether current earnings or margins appear above, near, or below a mid-cycle level;
- cross-checks PE with margin plus at least one of price, inventory, or utilization;
- explains when PE is not meaningful because earnings are negative, distorted, or not comparable;
- names the alternative evidence used, such as PB, EV/EBITDA, replacement cost, normalized earnings, or price-versus-order divergence, without turning it into a buy/sell call.

## Reverse the expectations embedded in price

Use `隐含预期反推` only after obtaining a dated market price and a comparable, source-backed earnings or cash-flow base. Its purpose is to ask “what operating path must become true for the current price to be internally consistent?”, not to predict a future stock price.

Choose the method that matches the available evidence:

- **Simplified PE bridge**: useful as a transparent sensitivity screen. With current price `P0`, required equity return `k`, horizon `n`, and a mid-cycle exit multiple `Mn`, calculate `required EPSn = P0 × (1+k)^n / Mn`, then `required EPS CAGR = (required EPSn / EPS0)^(1/n) - 1`. Disclose that this simplification omits interim distributions unless they are modeled separately.
- **Reverse DCF**: preferred when free cash flow, reinvestment and capital structure can be modeled. Solve for the growth, margin, utilization, ROIC or reinvestment path that equates the present value of cash flows and terminal value to the current enterprise or equity value. Keep cash flow and discount-rate definitions consistent.
- **Price-unchanged sensitivity**: `future PE = current price / future EPS` is arithmetic only. It does not discount time, price risk, dilution or the probability that the earnings path occurs, so it cannot establish cheapness by itself.

Rules:

1. Date-align price, shares, net debt and the earnings/cash-flow base; state whether the base is actual, guidance, consensus or an analyst scenario.
2. Normalize cyclical peak/trough earnings and show the mid-cycle basis. Never extrapolate a rebound quarter or one-off gain as a durable base.
3. Disclose the required return, horizon, exit multiple or terminal-growth assumption. Use a range or scenarios when the assumption is material rather than hiding it in one point estimate.
4. Reconcile dilution, buybacks, leverage, capital expenditure, working capital and cash conversion. EPS growth unsupported by cash flow is not enough.
5. Translate the inferred financial hurdle back into observable industrial conditions: buyer funding, binding order quality, volume, price, margin, utilization, qualification, effective capacity and competitive response.
6. Label the result as `情景推算` or `推论`, then judge the hurdle as `产业证据支持 / 要求偏高 / 证据不足`. Do not output a target price, a buy/sell call or “大概率涨到” language.
7. If comparable inputs are unavailable, write the exact evidence gap and keep the market-pricing conclusion provisional; do not leave an empty table.

Use this table:

| 反推方法 | 已知输入 | 关键假设 | 反推出的门槛 | 产业证据对照 | 证据与局限 |
|---|---|---|---|---|---|
| PE桥接 / 反向DCF / 其他 | 价格日期、业绩或现金流期间、股本/净债务 | 期限、必要回报率、退出倍数或终值增长 | EPS/FCF/利润率/利用率/ROIC 所需路径 | 支持 / 要求偏高 / 证据不足，并说明对应产业条件 | 证据ID；情景推算的口径与缺口 |

## Mandatory attempt checklist (before any gap is declared)

Try each row and record the outcome in the section-6 attempts table — "拿到数据", "无公开数据", or "口径不可比". Skipping the attempt and writing a gap directly is a validation failure.

| Source type | Where to try (free/public) | What it tells you |
|---|---|---|
| 行业指数估值分位 | 中证指数官网（PE/PB 月报）、国证指数官网、指数编制方 factsheet、交易所披露 | 当前估值处于什么历史位置；周期行业必须再做盈利正常化，不能直接解释为贵或便宜 |
| 行业 ETF 份额与资金流 | 基金公司官网每日份额披露、交易所基金公告、ETF 发行方月报 | 增量资金在进还是在出 |
| 北向/两融（A股适用） | 港交所披露的北向持股、交易所两融余额统计 | 边际资金的方向和杠杆意愿 |
| 龙头股价 vs 盈利剪刀差 | 公司 IR 页的股价与已披露 EPS/营收，同日期对齐 | 市场跑在基本面前面还是后面 |
| 卖方/媒体叙事密度（定性） | 近三个月主要券商研报标题、财经媒体专题频率 | 叙事处于扩散哪个阶段 |

Rules:

- Each attempt must name the concrete source tried, not the category ("中证指数官网 CSI 半导体指数月度估值" — not "指数官网").
- A same-definition two-point series (e.g. index PE on two dates from the same publisher) satisfies one opened source; screenshots of chart platforms and AI summaries do not.
- If data was obtained, fill the mapping table below and cite it in the evidence ledger like any other claim.
- If all rows fail, the lane is a documented gap: conclusion stays provisional, and the qualitative paragraph below is still required.

## Layered proxy contract

Do not test whether one ETF perfectly represents the whole chain. Use the narrowest available evidence at three levels:

| Proxy layer | Acceptable original source | What must be recorded |
|---|---|---|
| Industry ETF/index | issuer, exchange or index provider | dated NAV/return/valuation/units and total coverage |
| Sub-chain proxy | focused ETF/index or disclosed basket | the chain nodes actually covered and omitted |
| Representative company | company IR plus same-date exchange/issuer evidence | reported earnings/orders versus the observed market proxy |

Every proxy row records the instrument or entity, node coverage, metric and period, original source, conclusion, and limitation. Partial coverage is expected and must be disclosed; it is not a failed attempt. If no industry ETF exists, combine sub-chain and company proxies and label market conclusions as narrower than the industry.

An attempts table with no usable metric does not satisfy the market lane. The report must either add at least one dated quantitative market observation or explicitly remain an evidence gap with a reduced evidence score.

## Qualitative pricing paragraph (always required)

Even with a full data gap, section 6 must answer, clearly labeled as inference:

- 市场当前大概率**已定价**什么（依据：叙事密度、龙头涨幅与已披露盈利的关系等间接证据）
- 市场当前大概率**未定价**什么
- 这个判断哪里可能错

Never present this paragraph's content as measured fact, and never attach precise percentage weights to "priced vs unpriced".

## Future capital flow (section 7, always required)

For each scenario (基准/上行/下行) derive where the profit pool moves next — from order lead times, qualification barriers, capacity elasticity, and bottleneck position. Not from price charts, fund positioning rumors, or target prices.

- Name the chain node that benefits first and why the transmission reaches it first.
- Name the node that benefits later or gets hurt, and the lag mechanism.
- Attach the evidence to watch that would confirm the shift is happening.
- Keep the disclaimer visible: 情景推演，不构成买卖建议、目标价或个股推荐。

## Expectation Stages

### 1. Expectation Start

Signals:

- few people discuss the bottleneck
- industry data begins to change
- companies have not yet reported strong earnings
- stock prices may begin moving before consensus forms

Question: is there evidence before the market narrative?

### 2. Expectation Diffusion

Signals:

- media and broker reports increase
- related tickers spread from core beneficiaries to adjacent concepts
- valuation expands faster than earnings
- investors debate the scale of the opportunity

Question: are second- and third-order beneficiaries being overextended?

### 3. Earnings Realization

Signals:

- financial reports confirm order, price, margin, or utilization improvement
- public data becomes easier to find
- the industry story becomes consensus

Question: has the market already paid for this reality?

### 4. Valuation Digestion

Signals:

- stock prices stop rising despite good results
- earnings catch up with valuation
- new buyers need stronger data to enter
- management guidance becomes more important

Question: is the stock waiting for the next upward revision, or has the expectation ended?

### 5. Expectation Reversal

Signals:

- capacity release approaches
- prices stop rising
- inventory builds
- order growth slows
- capex is questioned
- weak players cut prices

Question: is the industry still good while stocks start pricing the next downturn?

## Mapping Template

Use this table:

| Industry Reality | Market Expectation | Evidence | Interpretation |
|---|---|---|---|
| Demand rising | Not priced / pricing / priced | Source/date | Explain |
| Shortage appearing | Not priced / pricing / priced | Source/date | Explain |
| Earnings improving | Not priced / pricing / priced | Source/date | Explain |
| Capacity releasing | Not priced / pricing / priced | Source/date | Explain |

Do not convert this table into a buy/sell recommendation.
