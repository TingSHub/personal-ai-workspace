# Open Skill Finder

English · [简体中文](README.md)

An open-source Skill for general AI agents. It searches local installations, skills.sh, GitHub, and configurable registries, then validates structure, performs static security inspection, scores evidence, and verifies provenance before recommending or installing an Agent Skill.

The goal is not to return the most results. It is to find Skills that actually fit, come from traceable sources, and have explainable risks.

## Why this project exists

Many Skill finders rely on one registry and primarily sort by keywords, installs, or stars. That is fast, but it creates several problems:

- one provider outage can remove the entire search capability;
- rank and popularity do not prove safety or suitability;
- same-name Skills and different paths in a monorepo can be merged incorrectly;
- installation may happen before scripts, dependencies, permissions, and URLs are reviewed;
- recommendations rarely expose evidence gaps.

Open Skill Finder separates the workflow:

```text
Multi-source discovery → normalization → structure/security gate → explainable score → approved installation
```

The security gate outranks the score. An unaudited candidate may be shown for discovery, but it is never marked installable. Popularity cannot offset a high-risk finding.

## Features

- Multi-source discovery: installed Skills, skills.sh, GitHub Code Search, and custom JSON registries.
- Correct identity: deduplicate by repository plus Skill path, not name alone.
- Static inspection: examine `SKILL.md`, scripts, references, hidden files, symlinks, lifecycle hooks, remote URLs, and suspicious instructions.
- Explainable scoring: relevance, project quality, provenance, maintenance, usage, community evidence, docs/tests/portability.
- Safer installation: identify exact source and revision, request approval, and verify the installed copy.
- Chinese and English output: Simplified Chinese by default, English on request.
- General architecture: follows the open Agent Skills structure without binding to one agent or model provider.

## Quick start

### Install as a Skill

```bash
npx skills add https://github.com/30bewater/open-skill-finder
```

You may also copy this repository into a Skills directory supported by your agent. Installation paths vary by client.

Example prompts:

```text
Find a Skill for converting video, images, and audio. Compare sources and risks, but do not install yet.
```

```text
Find three general-purpose Skills for GitHub issue triage and give me evidence cards in English.
```

### Use the scripts directly

The scripts use only the Python standard library. Python 3.10+ is recommended.

```bash
python scripts/probe_capabilities.py
python scripts/search_skills.py "media processing" --output candidates.json
python scripts/inspect_skill.py /path/to/example-skill --output audit.json
python scripts/rank_skills.py --query "media processing" --input candidates.json --output ranked.json
python scripts/render_cards.py --input ranked.json --lang en
```

Run any script with `--help` for the full interface.

## Custom registries

```bash
python scripts/search_skills.py "pdf" \
  --registry my-index=https://example.com/api/skills/search
```

The endpoint receives `q` and `limit`, and returns an array or an object containing `skills`, `results`, or `items`. See [references/providers.md](references/providers.md) for the field schema. Do not place access tokens in registry URLs.

## Scoring

| Component | Points |
|---|---:|
| Relevance | 30 |
| GitHub project quality | 20 |
| Provenance | 15 |
| Maintenance | 10 |
| Usage evidence | 10 |
| Independent community evidence | 5 |
| Documentation, tests, and portability | 10 |

See [references/scoring.md](references/scoring.md). Stars, installs, and semantic similarity are all gameable, so their influence is capped.

## Security boundary

The bundled inspector is a conservative static scanner and does not execute candidate scripts. It can detect a useful set of risky patterns, but a clean report is not proof of safety. For sensitive environments, add an independent scanner and human review.

Any unresolved `high` or `critical` finding blocks an installation recommendation. Network access, package installation, credential requests, and global configuration changes must be explained and approved separately. See [references/security.md](references/security.md).

## Project layout

```text
open-skill-finder/
├── SKILL.md
├── agents/openai.yaml
├── scripts/
├── references/
├── tests/
└── README_EN.md
```

## Design principles

- Separate search from trust.
- Prefer actual files over registry summaries.
- Prefer evidence over popularity.
- Mark missing information instead of guessing.
- Treat installation as a separate, approved phase.
- Default to Simplified Chinese while always offering English output.

## References and acknowledgements

The design was informed by the open Agent Skills specification and public ideas from Vercel Skills, SkillX, oakoss/agent-skills, AgentBay Skills, Cisco AI Defense Skill Scanner, Sentry Skill Scanner, and VoltAgent Awesome Agent Skills. See [NOTICE](NOTICE). This repository is an independent implementation and does not contain copied source code from those projects.

## License

[MIT License](LICENSE)
