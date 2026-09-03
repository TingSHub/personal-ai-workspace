# Scoring model

Scoring begins only after structural and security review. Candidates without an audit may be ranked for discovery but must remain `needs_audit` and ineligible for installation.

## Default weights

| Component | Points | Evidence |
|---|---:|---|
| Relevance | 30 | Name, description, path, and actual instructions match the task |
| GitHub project quality | 20 | Repository exists, stars/forks as weak signals, not archived |
| Provenance | 15 | Canonical source, exact path, commit, independent provider evidence |
| Maintenance | 10 | Recent meaningful update and responsive maintenance |
| Usage | 10 | Install/download evidence, preferably independently verifiable |
| Community | 5 | Independent discussions, examples, and reports |
| Docs, tests, portability | 10 | Clear description, examples, tests, valid structure, few platform assumptions |

## Interpretation

- `85–100`: unusually strong evidence; still review permissions and dependencies.
- `70–84`: good candidate with normal caveats.
- `55–69`: usable when the fit is specific and limitations are acceptable.
- below `55`: weak evidence or weak match; prefer a stronger candidate or create a small Skill.

These bands are guidance, not certification.

## Missing evidence

Score missing data as missing, not as zero-quality proof. Explain important gaps. A new but well-written Skill can be better than a popular stale one.

## Hard gates

Never add or subtract points to bypass these conditions:

- invalid or missing `SKILL.md` metadata;
- unresolved high or critical static finding;
- Skill path differs from the inspected path;
- source cannot be identified;
- installed content differs from the audited revision.

Apply a relevance floor before ranking. By default, candidates with less than 4/30 relevance points are omitted even if their repository is popular. Retrieve and read the actual `SKILL.md` when registry metadata is too sparse to establish relevance.

## Gaming resistance

Stars, downloads, tags, descriptions, and semantic similarity can all be manipulated. Cap their influence and require evidence from the actual files. Do not infer safety from popularity.
