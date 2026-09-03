---
name: topic-forward-signal-scanner
description: Scan free AkShare market signals for topic-forward candidate discovery.
---

# topic-forward-signal-scanner

Run the bundled scanner to collect a traceable JSON snapshot for the topic-forward workflow:

```bash
python3 .ai/skills/topic-forward-signal-scanner/scripts/fetch_market_signals.py \
  --date YYYYMMDD --out <signals.json>
```

The output contains `captured_at`, `trade_date`, `zt_pool`, `movers`, and `errors`. Treat the signal as candidate discovery only. Do not turn a limit-up or mover record into an investment claim; hand the candidate to research and require primary-source verification.

If an endpoint fails, keep the output and report its `errors` field. Do not silently replace an empty result with a conclusion.
