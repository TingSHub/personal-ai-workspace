# DeepSearch Research Protocol

Use this reference when the user expects deep industry research rather than a compact framework answer.

The target is:

```text
DeepSearch depth + Skill boundaries + explicit stopping conditions
```

## Research Split

Create 6-10 subtasks before browsing. For a normal industry-cycle report, use:

| Subtask | Minimum Evidence | Default Search Budget |
|---|---:|---:|
| Industry boundary and chain | 2 reliable sources | 2 rounds |
| Demand driver | 3 reliable sources | 3 rounds |
| Supply constraint | 3 reliable sources | 3 rounds |
| Capacity and capex timeline | 3 reliable sources | 3 rounds |
| Price, order, inventory, margin | 3 reliable sources | 3 rounds |
| Company/node beneficiaries | 2 reliable sources | 2 rounds |
| Policy, technology, substitution variables | 2 reliable sources | 2 rounds |
| Capital-market expectation mapping | 2 reliable sources | 2 rounds |

One search round means one focused query set plus original-source reading and compression. A result page or snippet without original-source reading does not complete a round. Do not run open-ended browsing.

For the policy subtask, first answer the policy-materiality gate. If the answer is `否`, record the checked channel and stop; the two-source minimum does not force a country survey. If the answer is `是`, open the current government or regulator text, record legal/implementation status and date, and expand only the jurisdictions that materially change the cycle judgment.

## Search Sequence

For each subtask, use this order:

1. Discovery: identify entities, vocabulary, candidate sources, and disputed claims.
2. Primary-source verification: open filings, official statistics, association data, company presentations, tenders, or direct transcripts.
3. Metric verification: search the exact KPI with period, geography, unit, and definition.
4. Contradiction search: actively look for later data, alternative definitions, delays, cancellations, and disconfirming evidence.

Use `search-routing.md` to choose SearXNG, Exa, direct page reading, or Agent-Reach channels. Do not spend all three rounds repeating broad market-size queries.

## Evidence Minimums

For each important claim, try to collect:

- one primary source, or
- two independent specialist sources, or
- one specialist source plus one corroborating data point.

If the minimum is not met, label the claim as weak evidence or unresolved.

## Source Notes

For every useful source, capture:

```text
source name
URL or document path
publish date
access date
claim supported
data definition
geography
time period
confidence: high / medium / low
retrieval tool
original opened: yes / no
```

Do not keep raw pages in the reasoning context. Compress each source into 3-6 bullet points.

## Conflict Merge Rules

When sources disagree:

1. Check whether the definitions differ: nominal capacity vs effective capacity, shipments vs orders, global vs China, calendar year vs fiscal year.
2. Prefer company filings, regulatory documents, government/association data, and direct management statements over media summaries.
3. If the source dates differ, explain which is more recent and whether later data may supersede earlier data.
4. If the conflict remains unresolved, keep both numbers and explain what future data would resolve it.

Never silently average conflicting numbers.

## Cost Controls

Use these hard limits unless the user explicitly asks for a larger research run:

- Maximum 3 search rounds per subtask.
- Maximum 12 high-value sources in the final synthesis for a normal report.
- Maximum 20 high-value sources for a long report.
- A high-value source may support multiple subtasks. Evidence minimums are coverage requirements, not a requirement to collect a separate source for every table cell.
- Stop browsing when additional sources repeat existing facts without changing the cycle judgment.
- Stop browsing when the next missing fact is likely proprietary, delayed, or unavailable in public sources.

## Log and Tool Output Controls

Never read full agent journals, JSONL files, logs, browser traces, or verbose terminal outputs.

Allowed patterns:

```bash
tail -n 120 run.log
rg "result|error|timeout|evidence|source" run.log
python scripts/safe_log_extract.py run.jsonl --tail 120 --filter result error timeout evidence source
```

Disallowed patterns:

```bash
cat run.log
cat journal.jsonl
Get-Content run.log
Get-Content journal.jsonl
```

If the only available artifact is huge, first extract the recent or relevant slice, then summarize it locally before using it.

## Local Compression Template

After each search round, write a compact observation:

```text
Subtask:
Search round:
Sources read:
New facts:
Changed inference:
Remaining gaps:
Stop or continue:
```

Only this compressed observation should feed the final synthesis.

## Stop Conditions

Stop research and synthesize when any of these are true:

- The cycle-stage judgment no longer changes after one additional round.
- The missing data is likely proprietary or unavailable.
- Sources repeat the same facts.
- The search budget for the subtask is exhausted.
- The user asked for a fast answer rather than a long report.

When stopping with gaps, say exactly what remains unknown.
