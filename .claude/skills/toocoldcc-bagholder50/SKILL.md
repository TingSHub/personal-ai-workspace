---
name: toocoldcc-bagholder50
description: Fetch the latest validated 韭菜50/Bagholder 50 constituents and index summary with a bundled read-only Python client. Use for current holdings, ranks, scores, returns, represented trade date, publication status, or data freshness.
---

# Bagholder 50 Data

For ordinary requests, resolve paths from this skill directory and run once:

`python -X utf8 scripts/fetch_bagholder50.py --view auto`

Use another Python 3 launcher only if needed. Require Python 3.10 or newer and
install no packages.

- If `selection.status=ready`, report `index_summary` and then `items` in their
  published order. Format decimal returns as percentages.
- If `selection.status=not_ready`, report `selection.message` and no list.
- If the command exits nonzero, report the JSON error from stderr and stop.

Never use another source, view, calendar, or old list as fallback. Do not infer,
re-rank, refill, or combine constituents.

Treat `selection.trade_date` as the represented list date and
`selection.signal_date` as its close-signal date. Let the client choose the
correct view; do not reproduce its date logic.

## Diagnostics

Only when the user explicitly asks for diagnostics, use one of:

- `--view holdings_today`
- `--view avoid_tomorrow`
- `--view all`
- `--verbose`

Explicit views are not “latest” and the feed is not a historical archive. Read
[references/data-schema.md](references/data-schema.md) only for output fields or
error codes.

This is an index-data feed, not an order API, tradability guarantee, or
personalized investment advice. Constituents identify the published
high-crowding tail and are not recommendations to buy.
