import type { AgentEvent } from './types.js';
export interface RunAcpOptions {
    /** Resolved absolute path to the agent binary (e.g. vela). */
    bin: string;
    /** Argv after the binary, e.g. ['agent','run','--runtime','opencode']. */
    args: string[];
    prompt: string;
    cwd: string;
    /** Model id for session/set_model. Omit / 'default' → skip set_model. */
    model?: string;
    env?: Record<string, string>;
    onEvent: (e: AgentEvent) => void;
    signal: AbortSignal;
    clientName?: string;
    clientVersion?: string;
}
export declare function runAcpAgent(opts: RunAcpOptions): Promise<{
    exitCode: number;
}>;
//# sourceMappingURL=acp-client.d.ts.map