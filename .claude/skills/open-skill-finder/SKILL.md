---
name: open-skill-finder
description: Discover, compare, inspect, score, and safely install Agent Skills from local directories, skills.sh, GitHub, curated indexes, and configurable registries. Use when users ask to find, recommend, compare, audit, or install a skill; need alternatives to a named skill; or want evidence about relevance, maintenance, provenance, dependencies, community feedback, security, and installation risk. Search across multiple sources, avoid hallucinated packages, validate every candidate before recommendation, and require explicit approval before installation.
---

# Open Skill Finder

Find useful Agent Skills without treating search rank as proof of safety or quality.

## Language

- Reply in Simplified Chinese by default when the user's language is unknown.
- Follow the user's language when it is clear.
- Use `scripts/render_cards.py --lang zh` or `--lang en` for consistent cards.

## Workflow

1. Restate the capability the user actually needs. Generate concise Chinese and English query variants when useful.
2. Probe available tools with `python scripts/probe_capabilities.py`.
3. Search installed Skills first, then multiple remote sources with `python scripts/search_skills.py`. Use at least two independent remote sources when available.
4. Normalize and deduplicate candidates by canonical repository plus Skill path. Never merge different paths merely because their names match.
5. Remove obvious semantic false positives. Open the actual `SKILL.md`; do not rely on a title, tag, install count, or search snippet.
6. Fetch promising candidates into a temporary or read-only location. Record the repository URL, Skill path, and exact commit when possible.
7. Inspect every candidate with `python scripts/inspect_skill.py <skill-directory>`. Inspect all bundled scripts, references, assets, hidden files, symlinks, package hooks, and remote URLs.
8. Reject invalid or high-risk candidates before quality scoring. Treat search relevance and popularity as discovery signals, never as a security verdict.
9. Rank the remaining candidates with `python scripts/rank_skills.py --query "..." --input candidates.json`.
10. Present compact evidence cards with `python scripts/render_cards.py --input ranked.json`. Explain uncertainty and distinguish facts from inference.
11. Ask for explicit user approval before installation. Install only the selected repository, path, and preferably pinned revision. Verify the installed copy afterward.

## Hard Rules

- Do not invent a Skill, repository, version, install command, metric, review, or license.
- Do not execute a candidate's scripts during discovery or inspection.
- Do not install a candidate that lacks a completed audit, has invalid structure, or has unresolved high/critical findings.
- Do not use unattended approval flags by default.
- Do not expose access tokens, private repository URLs, local secrets, or unrelated file contents.
- Do not silently modify shell profiles, global configuration, package registries, or security settings.
- Ask before adding system packages, runtimes, global packages, credentials, or services.
- If no trustworthy match exists, say so and offer to create a small Skill instead.

## Search Strategy

Use these sources in descending practical order, adapting to availability:

- Installed local Skills for immediate reuse and duplicate detection.
- skills.sh for broad ecosystem discovery.
- GitHub code search for repositories containing `SKILL.md`.
- Curated lists and configurable JSON registries for independent coverage.
- Forums, issues, discussions, and real usage examples as weak community evidence.

Read [references/providers.md](references/providers.md) before adding a registry or changing provider behavior.

## Safety Gate

Run structural validation and static security inspection before making an install recommendation. A clean scan means only that no configured rule found a problem; it is not a guarantee of safety.

Classify findings as:

- `critical`: clear destructive behavior, credential theft, hidden execution, or direct instruction hijacking.
- `high`: unbounded command execution, lifecycle hooks, unsafe remote execution, or writes outside expected scope.
- `medium`: undeclared network access, broad permissions, opaque binaries, unusual obfuscation, or unpinned downloads.
- `low`: portability, maintenance, documentation, or minor metadata concerns.

Read [references/security.md](references/security.md) for the review checklist and escalation rules.

## Ranking

Apply quality scoring only after the safety gate. Use the default 100-point model:

- relevance: 30
- GitHub project quality: 20
- provenance: 15
- maintenance: 10
- usage: 10
- independent community evidence: 5
- documentation, tests, and portability: 10

Do not let popularity compensate for an unresolved security finding. Read [references/scoring.md](references/scoring.md) before changing weights or interpreting missing evidence.

## Output

For each serious candidate, show:

- Skill name and match score
- source repository and exact Skill path
- latest known update
- security status and notable findings
- additional dependencies
- why it fits
- limitations or uncertainty

Hide routine compatibility and permissive-license details to keep the card compact. Show compatibility only when limited or exceptional. Show license only when missing, restrictive, inconsistent, or relevant to redistribution. Read [references/output-format.md](references/output-format.md) for examples.

## Installation

After approval, prefer the platform's standard installer if it can pin the exact source. Otherwise copy only the audited Skill directory and its declared files. Re-run inspection on the installed copy and report any difference.

Read [references/installation.md](references/installation.md) before performing an installation or suggesting a command.

## Included Tools

- `scripts/probe_capabilities.py`: report available search and audit tooling.
- `scripts/search_skills.py`: search local directories, skills.sh, GitHub, and configurable registries.
- `scripts/inspect_skill.py`: validate structure and perform conservative static inspection.
- `scripts/rank_skills.py`: calculate an explainable post-gate quality score.
- `scripts/render_cards.py`: render concise Chinese or English recommendation cards.

Run each script with `--help` for its exact interface.
