# Safe installation

Installation is a separate, user-approved phase.

## Before installation

1. Confirm the selected repository, Skill path, and revision.
2. Confirm that structure and security inspection completed.
3. Explain required runtimes, packages, network services, credentials, and global changes.
4. Show unresolved medium findings and obtain explicit acceptance.
5. Ask which supported agent location to use only when it cannot be inferred safely.

## Installation methods

Prefer the agent platform's standard Skill installer when it preserves provenance and supports an exact repository/path. Otherwise copy only the audited Skill directory and declared supporting files.

Do not:

- execute repository-provided bootstrap scripts merely to install a Skill;
- add unattended confirmation flags by default;
- install unrelated Skills from a monorepo;
- add global packages without explaining size, privileges, and removal;
- overwrite an existing Skill without showing the difference and asking permission.

## After installation

1. Re-run static inspection against the installed path.
2. Compare file hashes with the audited copy.
3. Confirm that the agent can discover the Skill.
4. Run only a harmless smoke test that the user authorized.
5. Report installed location, revision, dependencies, and removal steps.

## Updating

Treat an update like a new candidate. Review the diff, audit the new revision, and ask before replacing the installed copy.
