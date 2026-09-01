import type { AgentDef } from './types.js';
/**
 * Built-in agent definitions. Order matters: the first one in the list is
 * the default selection in the studio composer.
 *
 * Default = anthropic-api (HTTP / Messages API), because the local
 * `claude --print` CLI has a non-deterministic 1-byte-empty-reply mode on
 * long creative outputs (verified 2026-05-28). Direct API doesn't.
 */
export declare const AGENT_DEFS: AgentDef[];
export declare function findAgent(id: string): AgentDef | undefined;
//# sourceMappingURL=registry.d.ts.map