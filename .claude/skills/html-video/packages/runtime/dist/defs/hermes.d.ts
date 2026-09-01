/**
 * Hermes (Python CLI by Hermes Agent project) as a local agent runtime.
 *
 *   hermes chat -q "<prompt>" -Q
 *
 * `-Q` (quiet) prints just the response text to stdout, prefixed with one
 * `session_id: ...` header line. We strip that line in the studio prompt
 * code path so the user doesn't see it.
 *
 * Hermes default backend is OpenRouter — same provider Joey already uses,
 * so any model-side outage that hits Anthropic also hits hermes via the
 * same route. Useful as a parallel comparison agent rather than a
 * fundamentally redundant one.
 */
import type { AgentDef } from '../types.js';
export declare const hermes: AgentDef;
//# sourceMappingURL=hermes.d.ts.map