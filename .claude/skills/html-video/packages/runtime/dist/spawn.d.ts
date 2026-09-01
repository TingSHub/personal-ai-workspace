import type { AgentDef, AgentEvent, AgentInvokeContext, SpawnHandle } from './types.js';
/**
 * Spawn an agent CLI and stream events to the listener.
 * v0.1: only supports streamFormat='plain' fully (chunks emitted as text events).
 *       claude-stream / json-event-stream are scaffolded but yield to plain for now.
 */
export interface SpawnOptions {
    def: AgentDef;
    prompt: string;
    context: AgentInvokeContext;
    onEvent?: (event: AgentEvent) => void;
    signal?: AbortSignal;
}
export declare function spawnAgent(opts: SpawnOptions): SpawnHandle;
//# sourceMappingURL=spawn.d.ts.map