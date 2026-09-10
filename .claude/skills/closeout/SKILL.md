---
name: closeout
description: Explicitly review a completed workspace task, audit directory placement, propose reusable knowledge changes, and apply approved changes before creating a local Git commit. Use only when the user invokes $closeout.
---

# Closeout

Execute `closeout-and-commit` as the manual entry point for task completion. The Workflow remains the authoritative orchestration contract; this Skill makes invocation reliable and supplies the workspace-specific review mechanics.

## Modes

- `review` (default): inspect and return the baseline, directory findings, and approval proposal directly in the conversation; do not create evidence files, move files, update canonical assets, stage, or commit.
- `apply`: apply only proposal items the user explicitly approved, revalidate, then commit only if commit approval is included.
- `commit-only`: omit knowledge distillation, but still run completion, structure, secret, scope, and staged-diff checks.
- `distill-only`: propose reusable Experience and documentation changes without directory mutations or Git commit.

If the invocation does not state a mode, run `review`. A general request to “finish” or “commit” does not select `apply` and does not constitute approval for directory moves, canonical knowledge writes, deletion, or commit.

## Review

1. Read `closeout-and-commit` and the current task's accepted artifacts and validation evidence.
2. Freeze the repository HEAD, worktree status, task-owned files, pre-existing changes, and exclusions.
3. Check completion before governance. Unfinished required work or failed validation is a blocker.
4. Run `python3 .claude/skills/closeout/scripts/scan_workspace_structure.py --root .` when this workspace contains it.
5. Semantically review touched files, their parent directories, repository control directories, and relevant references. Judge ownership, lifecycle, naming consistency, duplication, discoverability, and extension shape. Do not reorganize vendored or runtime trees merely because they are large.
6. Present one approval matrix with stable item IDs covering file scope, directory moves, Experience candidates, documentation writes, deferred items, and local commit authorization. Return it in chat; only write a review bundle when the user explicitly requests an audit record.

Every directory proposal must state current path, proposed path, rationale, affected references, migration risk, and whether it blocks commit. Classify findings as `BLOCKER`, `RECOMMENDED`, `OPTIONAL`, or `ACCEPTED_EXCEPTION`.

## Apply

Require approval that maps to proposal item IDs. Apply no unlisted item. Treat move, merge, archive, delete, canonical knowledge write, and Git commit as distinct actions.

- Preserve pre-existing changes and use an explicit task-owned file list.
- Use `experience-curator` for Experience promotion, `resource-manager` for Skill/Agent records, and `work-for-me` for Workflow indexing and validation.
- Prefer recoverable moves to deletion. Update identified path and by-name references in the same approved item.
- Re-run structural scanning, reference checks, task tests, secret checks, and `git diff --cached --check` after mutation.
- Stage only approved files, display the staged names and diff summary, and create one local commit for this workspace only when commit authorization is explicit. Never push or create a PR unless separately requested.

Stop before commit on failed required tests, unresolved blockers, secrets, stale references, scope ambiguity, or a staged file outside the approved list. Report the exact blocker and retain recoverable proposal/receipt artifacts.

## Outputs

Keep closeout output conversational by default. Review, approval proposals, validation results, and handoff are returned in chat and do not create `baseline.md`, `directory-review.md`, `approval-proposal.md`, or staging bundles unless the user explicitly asks to save an audit record. Canonical asset changes and Git commits remain real file mutations when separately approved. Do not create placeholder files for unused phases.
