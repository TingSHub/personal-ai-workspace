# Search Routing

Use this reference before collecting web evidence.

## Tool Roles

| Need | Preferred Route | Evidence Role |
|---|---|---|
| Previous reports, source URLs, or prior research decisions | `mem-search` when its `search`, `timeline`, and `get_observations` MCP tools are available | Leads only; reopen the original source and recheck freshness |
| Broad general-web discovery | Local SearXNG (`http://127.0.0.1:8080`) | Candidate sources only |
| Semantic discovery or missing vocabulary | Exa through `mcporter` | Candidate sources only |
| Original page or document | Direct browser/fetch; Jina Reader only as a reading fallback | Evidence after identity/date verification |
| Dynamic, login-gated, or anti-bot original page | `web-access` after static official page, PDF, or API routes are insufficient | Evidence only after original identity, date, metric, and locator verification |
| GitHub, Twitter/X, LinkedIn, YouTube, Bilibili, RSS, forums | Agent-Reach and its active backend | Leads, direct first-party statements, or expectation mapping |
| Company, regulator, government, association | Official site, filing, API, or original PDF | Preferred Tier 1 evidence |
| Public retail or distribution channel | Fixed platform, seller, SKU/specification and timestamped observation | Tier 2 channel observation only; industry inference requires cross-channel or upstream corroboration |

Use an available hosted web search/open capability when appropriate, but never depend on one named tool. Continue with SearXNG, Exa, direct page reading, or Agent-Reach according to the task.

## Commands

General discovery with SearXNG on Windows:

```powershell
$q = [Uri]::EscapeDataString("query")
Invoke-RestMethod "http://127.0.0.1:8080/search?q=$q&format=json"
```

Set `language=zh-CN` for Chinese queries and `language=en-US` for English queries. Inspect the first results before continuing: if they are off-topic, empty, or dominated by calendar/dictionary pages, treat that round as failed and switch to Exa instead of repeating the same query.

Semantic discovery:

```bash
mcporter call exa.web_search_exa 'query=query' numResults=8 --output json
```

Platform-specific discovery:

```bash
agent-reach doctor --json
opencli twitter search "query" -f yaml
gh search repos "query" --limit 10
```

Check `agent-reach doctor --json` before platform-specific work and use its `active_backend`. Never extract browser cookies or request credentials in chat.

## Optional History Recovery

Use `mem-search` only when the current session exposes its three required MCP tools and the task benefits from prior-session context.

1. Search by industry, metric, company, or source title.
2. Use the timeline to identify the relevant research run.
3. Fetch only the filtered observations.
4. Treat recovered conclusions, values, and URLs as leads. Reopen the original source in the current run, verify whether a newer release supersedes it, and create a new evidence-ledger entry.

Never set `opened=yes` or `freshness=current` merely because a source appeared in memory. If the MCP backend is unavailable, skip history recovery and continue with live discovery.

## Dynamic or Login-Gated Originals

Use `web-access` only when the target original requires browser rendering, interaction, login state, or an anti-bot fallback. Prefer an official static page, filing, PDF, or API when it contains the same evidence.

- Run the dependency check and display the automation-risk notice required by `web-access` before starting its CDP proxy.
- Create background tabs, preserve user tabs, and close only tabs created for the task.
- Record the original URL, publisher, publication date, data period, metric definition, and page/table/section locator. Browser-rendered text without this metadata does not pass the verification gate.
- If login or browser access is unavailable, record an original-source verification gap rather than promoting a search snippet or repost.

## Query Ladder

Run focused queries in four stages.

### 1. Discovery

```text
[industry] supply chain bottleneck 2025 2026
[industry] demand capacity price inventory 2025 2026
[行业] 供需 产能 价格 库存 订单 2025 2026
```

### 2. Primary Sources

```text
site:company-domain.com annual report OR quarterly results [metric]
site:gov-domain [industry] production capacity exports imports
site:association-domain [industry] shipment forecast statistics
[company] investor presentation capex capacity utilization
```

### 3. Exact Metrics

Include period, geography, unit, and definition:

```text
[product] effective capacity units/month China 2026 Q1
[product] average selling price inventory days 2025 2026
[company] order backlog capex guidance 2026 Q1 actual
```

### 4. Contradictions

```text
[project/company] delay cancellation ramp yield shortfall
[industry claim] oversupply inventory correction price decline
[metric] revised restated updated methodology
```

Search in Chinese and English when the supply chain is global.

## Public-Channel Proxy Verification

Use public-channel observations only when they can answer a concrete question that filings or industry statistics cannot answer at the same cadence.

1. Fix the platform or channel.
2. Fix the seller or quoting entity.
3. Fix the same SKU and specification; do not compare different generations, capacities, packages, or service terms.
4. Record whether the price is a list price, coupon price, observed transaction price, or other stated definition.
5. Record the observation timestamp with timezone and the availability state.
6. Check promotions, clearance, seller changes, product refreshes, delisting, and regional delivery restrictions.
7. Obtain a second channel or upstream source before inferring an industry-wide price move or shortage.

A single SKU being repriced, out of stock, or delisted proves only that channel event at that time. It does not by itself prove industry shortage, broad price inflation, or upstream capacity tightness.

## Verification Gates

Before treating a result as evidence:

1. Open the original source.
2. Record publisher, date, access date, geography, period, unit, and definition.
3. Label actual versus forecast.
4. Check whether a newer release supersedes it.
5. Search for a conflicting or disconfirming source.

Search snippets, generated summaries, and reposts do not pass this gate.

## Failure Routing

- SearXNG unavailable: record the failed health check. If an available hosted web search/open capability or direct official URL can continue the task, use it and record the fallback. Ask the user to start Docker Desktop only when local SearXNG is required and no adequate fallback exists.
- One SearXNG engine blocked: continue with responsive engines and record the limitation.
- SearXNG returns off-topic results: retry once with an explicit language and official-domain query; if quality is still poor, switch to Exa and record the discovery gap.
- Exa unavailable: continue with SearXNG and official-domain queries.
- Original page blocked: try official PDF/API, browser reading, then Jina Reader; retain the original URL.
- `mem-search` MCP tools unavailable: skip history recovery; do not block live research.
- `web-access` dependency or login unavailable: record the blocked original and the verification gap; continue with official static alternatives when possible.
- Social platform unavailable: mark the sentiment/early-signal gap; do not substitute social claims for Tier 1 evidence.
