import type { AgentDef } from '../types.js';
/**
 * Codex CLI def (`codex`, by OpenAI).
 *
 * Slim version matching html-video's text-first model: the studio reads the
 * model's free-form output and extracts the fenced ```html``` block, so we run
 * `codex exec` in plain (non-JSON) mode rather than `--json` — the latter emits
 * NDJSON envelopes that the v0.1 spawn loop would dump verbatim into the chat.
 *
 * `--skip-git-repo-check` lets it run in the project dir without a git repo;
 * prompt is piped via stdin (long HTML-generation prompts).
 */
export declare const codex: AgentDef;
//# sourceMappingURL=codex.d.ts.map