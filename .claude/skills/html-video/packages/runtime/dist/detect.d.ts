import type { AgentDef, DetectedAgent } from './types.js';
/** PATH → static binFallbacks → async resolveBinFallback (e.g. bundled npm pkg). */
export declare function resolveBin(def: AgentDef): Promise<string | null>;
export declare function detectOne(def: AgentDef): Promise<DetectedAgent>;
export declare function detectAll(opts?: {
    force?: boolean;
}): Promise<DetectedAgent[]>;
//# sourceMappingURL=detect.d.ts.map