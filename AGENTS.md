# Personal AI Workspace

## Purpose

A personal AI asset management and orchestration system. It manages reusable Workflows (Markdown SOPs), Skill/Agent resources, and validated Experience so real projects can deliver higher-quality results with less repeated work. Claude, Codex, or another Agent performs execution; this repository is not an Agent runtime.

## Rules

- Before starting a task, look for an existing Workflow first (`.ai/workflows/`)
- Do not recreate an existing Skill or Agent resource (`.ai/skills/`, `.ai/agents/`)
- Manage Skill/Agent resources with Resource Manager (`.claude/skills/resource-manager/`)
- Index Workflows with the Workflow Registry (`.claude/skills/workflow-registry/`)
- Create new projects with the Project Registry (`.claude/skills/project-registry/`)
- Field lists always come from `.ai/templates/` templates; never inline field definitions
- The top-level repo and `projects/*` are physically isolated: never commit project code to this repo
- Reference Workflows / Skills / Agents / Experiences by name, never by relative path
- Runtime state (`.omc/`) is never committed; `.codex/skills` is one directory symlink to `../.claude/skills`
- **Default call path**: Project → Workflow → Skill/Agent. The Workflow is the single source of truth as a Markdown SOP; each phase's Required Resources must actually run and leave an independent artifact; downstream steps consume only accepted artifacts.
- **Best-available selection**: never use local-first routing. Choose by actual effectiveness, output quality, stability, dependency cost, maintenance cost, and current-project fit. Discover across workspace, installed external skills, skill-hub, find-skills, and agent repositories; source is not a priority. Fall back only when the preferred resource cannot be made usable or fails acceptance. Do not add aggregate scores, availability states, or setup-cost models.
- **Resource boundary**: Skill/Agent records are technical calling guides. They contain source, installed revision, invocation, requirements, update method, known issues, and optional local scripts. Never modify vendored external resources to add local behavior; keep local notes/scripts in the resource asset.
- **Experience feedback loop**: project execution records stay in `projects/{name}/logs/`. At project completion, Experience Curator keeps only conclusions that will change a future workflow, resource invocation, quality check, or reusable script, and decides their owner. It stages a Candidate in `projects/{name}/experience-candidates/`; after **user confirmation**, it writes the conclusion back to the target Workflow SOP or Skill/Agent record (backfilling `experience_refs[]` by name), then archives the experience file under `.ai/archive/experiences/`. Ordinary logs never enter the asset library.

## Structure

- `.ai/skills` — Skill resource records, calling notes, and local scripts
- `.ai/agents` — Agent resource records, calling notes, and local scripts
- `.ai/archive/capabilities` — archived retired Capability layer (historical quality contracts, traceability only)
- `.ai/experiences` — in-flight experiences (feedback loop: archived to `.ai/archive/experiences/` after write-back)
- `.ai/workflows` — workflow library (development / task / automation)
- `.ai/templates` — templates (single source of truth)
- `.ai/rules` — rules index
- `.claude/skills` — manager and executable skills
- `projects` — actual projects (independent git repos)

## Known Limitations

- Installed third-party resources may ship their own code/scripts. Local calling helpers belong under the matching `.ai/skills/<name>/scripts/` or `.ai/agents/<name>/scripts/` directory and must not modify the external installation.
- Do not create per-Skill links or copies under `.codex/skills`; maintain the single directory symlink so Claude and Codex always see the same installation tree.
