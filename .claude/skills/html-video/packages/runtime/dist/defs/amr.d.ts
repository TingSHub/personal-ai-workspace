import type { AgentDef } from '../types.js';
interface VelaProfile {
    runtimeKey?: string;
    apiUrl?: string;
    user?: {
        email?: string;
        plan?: string;
    } | null;
}
/** Read ~/.vela/config.json and return the active profile (prod by default). */
export declare function readVelaProfile(): {
    name: string;
    profile: VelaProfile;
} | null;
export declare const amr: AgentDef;
export interface AmrModel {
    id: string;
    label: string;
}
/**
 * List the live AMR catalog via `vela model list`. Each line is
 * `<model-id>\t<provider>`; the id is already the link-facing slug AMR accepts
 * in session/set_model, so no normalization is needed. Ordered preferred-first.
 */
export declare function listAmrModels(resolvedBin: string): Promise<AmrModel[]>;
export {};
//# sourceMappingURL=amr.d.ts.map