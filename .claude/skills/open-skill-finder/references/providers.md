# Search providers

Use more than one provider whenever remote access permits. A provider returning a result proves only that the listing exists.

## Built-in providers

### Local directories

Search standard Agent Skill roots first. Local discovery is fast, reveals duplicates, and may satisfy the request without downloading anything. Do not execute discovered files.

### skills.sh

Use the public search endpoint for broad discovery. Treat install counts as self-reported registry metadata unless independently verified. Open the source repository and actual Skill path before recommendation.

### GitHub

Use authenticated GitHub code search through `gh` when available. Search for `SKILL.md`, then inspect the repository, exact path, activity, license, issues, and commit. A repository star count is a weak quality signal, not a trust guarantee.

### Custom registries

Pass repeated `--registry name=https://example/api/search` arguments. The endpoint should accept `q` and `limit` query parameters and return either an array or an object containing `skills`, `results`, or `items`.

Recognized fields include:

```json
{
  "name": "example-skill",
  "description": "What it does",
  "source_url": "https://github.com/owner/repo",
  "skill_path": "skills/example-skill",
  "installs": 123,
  "stars": 45,
  "updated_at": "2026-01-01T00:00:00Z",
  "license": "MIT"
}
```

Unknown fields are ignored. Never pass credentials in a registry URL because URLs may appear in logs and evidence output.

## Query generation

Generate a small set of high-signal variants:

- the user's original phrase;
- a short capability phrase;
- the likely English ecosystem term;
- a common synonym or tool name when necessary.

Do not issue dozens of near-identical searches. Preserve which query produced each candidate.

## Deduplication

Use canonical repository plus Skill path as identity. The same repository may contain multiple legitimate Skills. Identical names in different repositories are not duplicates.

## Forum and community evidence

Issues, discussions, Hacker News, Reddit, tutorials, and independent examples can reveal whether the Skill works in practice. Use them as a small supporting signal. Record a URL and date; do not convert anonymous praise into a factual security or quality claim.

## Provider failure

Degrade provider by provider. Return partial results with an `errors` array. Do not claim that no Skill exists merely because one registry is unavailable.
