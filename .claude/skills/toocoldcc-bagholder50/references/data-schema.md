# Bagholder 50 Agent feed contract

## Canonical endpoint

`https://indices-toocoldcc.pages.dev/data/agent/bagholder50.json`

The website's formal build produces this compact endpoint from its Bagholder 50
publication artifact and its local `tushare.trade_cal` data. Consumers need one
HTTP request and no financial API, external calendar, or API key.

The client rejects custom URLs and redirects, limits the response to one
megabyte, and makes at most two attempts for transient network failures.

## Website feed

The website publishes:

```json
{
  "schema_version": 1,
  "data_product": "bagholder50_agent_feed",
  "generated_at_utc": "YYYY-MM-DDTHH:MM:SSZ",
  "canonical_url": "https://indices-toocoldcc.pages.dev/data/agent/bagholder50.json",
  "index": {},
  "selection_policy": {},
  "views": {},
  "provenance": {}
}
```

`index.summary` contains latest date/point, the published annualized return,
and 1-, 5-, and 20-trading-day returns. `views.holdings_today` and
`views.avoid_tomorrow` each carry `status`, `signal_date`, `trade_date`, and
`items`.

`selection_policy` fixes `UTC+08:00`, the `15:00:00` cutoff, expected update
time, and a compact calendar contract:

```json
{
  "source": "tushare.trade_cal",
  "coverage_start": "YYYY-MM-DD",
  "coverage_end": "YYYY-MM-DD",
  "open_dates": ["YYYY-MM-DD"],
  "sha256": "..."
}
```

Absence from `open_dates` means closed only within the declared coverage range.
The hash covers the canonical object containing `source`, both coverage dates,
and `open_dates`, before hash fields are added.

Automatic selection is strict: before `15:00` on an open date the client uses
a ready view matching today's trade date, preferring the prior close's
`avoid_tomorrow` after midnight; at or after `15:00`, and throughout closed
days, it uses only a ready `avoid_tomorrow` for the next open date. A missing
target view yields `not_ready`; the client never falls back to an older list.

`provenance.bagholder50.sha256` identifies the exact website
`data/bagholder50.json` bytes used to derive the feed. The calendar provenance
hash must match the calendar contract. These hashes support reproducibility but
are not publisher signatures.

Each ready constituent view contains exactly 50 unique rows with:

| Field | Validation |
| --- | --- |
| `ts_code` | `000001.SZ`/`.SH`/`.BJ`-style code |
| `name` | Non-empty published security name |
| `today_return` | Finite decimal return |
| `bagholder_rank` | Integer sequence `1..50` |
| `bagholder_score` | Finite value in `[0, 1]`, non-increasing by rank |

A pending view must contain an empty `items` list. The feed exposes adjacent
date views only, not arbitrary historical constituents.

## Client output

Default output is compact and versioned:

```json
{
  "schema_version": 1,
  "tool_version": "1.2.1",
  "source": {},
  "index_summary": {},
  "view": "auto",
  "selection": {},
  "items": []
}
```

`selection.status=not_ready` is an expected publication state and exits zero.
Technical failures exit nonzero and write JSON to stderr with one of:

- `ENDPOINT_POLICY_VIOLATION`
- `FETCH_FAILED`
- `CALENDAR_INVALID`
- `SCHEMA_MISMATCH`
- `INVALID_JSON`
