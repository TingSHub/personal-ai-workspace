# Evidence Ledger

Maintain one record for every important claim. Use stable claim IDs such as `E1`, `E2`, and `E3` in the report body.

## Required fields

| Field | Meaning |
|---|---|
| `claim_id` | Stable report-local ID |
| `claim` | Exact supported statement |
| `type` | Actual, partial actual, guidance, plan, forecast, inference or assumption |
| `lane` | Chain, demand, supply, signals or market expectation |
| `publisher` | Original publisher |
| `url` | Direct original URL where possible |
| `published_at` | Source release date |
| `accessed_at` | Date opened during the research run |
| `period` | Data period covered |
| `geography` | Geographic scope |
| `unit_definition` | Unit and metric definition |
| `locator` | Page, table, section, paragraph or transcript timestamp |
| `opened` | `yes` only after the original was opened |
| `freshness` | `current`, `superseded` or `unchecked` after a newer-release check |
| `limitation` | Scope, comparability or attribution caveat |
| `contradicts` | Claim ID contradicted or qualified, if any |

## Integrity rules

1. Create ledger rows from actual research observations, not from a static profile or URL array.
2. Never default `opened` to `yes`, `freshness` to `current`, or a research subtask to `complete`.
3. Keep one claim narrow enough that its source and locator support the whole statement.
4. Use separate rows when one sentence mixes an actual result with a future plan.
5. Record a direct source URL rather than a search/taxonomy page whenever possible.
6. Preserve conflicting rows; do not overwrite or average them.
7. Count a source toward an evidence lane only when it materially supports that lane.
8. For a public-channel observation, put the platform, seller, SKU/specification, price definition, timestamp/timezone and availability in the claim or locator, and record promotion, delisting, regional and representativeness limits explicitly.
9. Do not upgrade a single-channel observation into an industry price or shortage claim unless a separate ledger row supplies cross-channel or upstream corroboration.

## Minimal JSON shape for deterministic generators

```json
{
  "claim_id": "E1",
  "claim": "Metric and period",
  "type": "actual",
  "lane": ["demand"],
  "publisher": "Publisher",
  "url": "https://original.example/report",
  "published_at": "YYYY-MM-DD",
  "accessed_at": "YYYY-MM-DD",
  "period": "YYYY Q1",
  "geography": "Global",
  "unit_definition": "unit and definition",
  "locator": "page 10, table 2",
  "opened": true,
  "freshness": "current",
  "limitation": "not segment-specific",
  "contradicts": []
}
```

Render the report’s data-currency table, evidence matrix, source counts, and research completion statuses from this ledger. Do not duplicate those states manually.
