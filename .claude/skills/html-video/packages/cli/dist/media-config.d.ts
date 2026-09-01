/**
 * Studio media-provider config — persists API credentials entered through the
 * Settings UI to `.html-video/media-config.json` under the project root, so
 * users don't have to set environment variables by hand.
 *
 * Credential precedence when resolving (config file wins over env, since the
 * GUI is the explicit user choice):
 *   media-config.json  →  OD_MINIMAX_API_KEY / MINIMAX_API_KEY env
 *
 * Mirrors open-design's `.od/media-config.json` shape loosely; we only need
 * MiniMax here. The file holds the raw key, so it lives in the gitignored
 * `.html-video/` runtime dir, never the repo.
 */
import { type MinimaxCredentials } from '@html-video/core';
export declare class MediaConfigStore {
    private readonly path;
    private readonly dir;
    constructor(projectRoot: string);
    private read;
    private write;
    /** What the Settings UI shows: whether a key is set + masked key + base URL.
     *  Never returns the raw key. Reports the source (config file vs env). */
    getMinimaxStatus(): {
        configured: boolean;
        source: 'config' | 'env' | 'none';
        maskedKey: string;
        baseUrl: string;
    };
    /** Persist a key (and optional base URL) entered in the UI. */
    setMinimax(apiKey: string, baseUrl?: string): void;
    /** Forget the stored MiniMax key (env fallback, if any, still applies). */
    clearMinimax(): void;
    /** Resolve usable credentials: config file first, then env. null if neither. */
    resolveMinimax(): MinimaxCredentials | null;
}
//# sourceMappingURL=media-config.d.ts.map