/**
 * @html-video/core — MiniMax audio provider.
 *
 * MiniMax exposes speech (`/t2a_v2`) and music (`/music_generation`) under the
 * same host, the same Bearer key, and the same response shape — both wrap the
 * payload in a `base_resp` envelope and return the audio as a hex string in
 * `data.audio`. So one provider + one key covers both narration and music.
 *
 * The request/parse pattern is ported from open-design's `renderMinimaxTTS`
 * (apps/daemon/src/media.ts): fetch → Bearer → check `base_resp.status_code`
 * (an HTTP 200 can still be a logical failure) → `Buffer.from(hex, 'hex')`.
 *
 * Credentials are read from the environment so the studio works without any
 * config file; a missing key yields `null` from {@link resolveMinimaxCredentials}
 * and callers report it gracefully instead of throwing.
 */
export interface MinimaxCredentials {
    apiKey: string;
    baseUrl: string;
}
export interface MinimaxAudioResult {
    /** Decoded audio bytes (MP3). */
    bytes: Buffer;
    /** File extension to store under. */
    ext: '.mp3';
    /** Human-readable note of what was produced (provider · model · size). */
    providerNote: string;
    /** Reported duration in seconds, if the API surfaced it. */
    durationSec?: number;
}
/**
 * Resolve MiniMax credentials from the environment. Returns `null` (not throw)
 * when no key is set, so the studio can show a friendly "configure your key"
 * message instead of a 500.
 *
 * Key precedence:  OD_MINIMAX_API_KEY → MINIMAX_API_KEY
 * Base precedence: OD_MINIMAX_BASE_URL → MINIMAX_BASE_URL → default
 */
export declare function resolveMinimaxCredentials(env?: NodeJS.ProcessEnv): MinimaxCredentials | null;
/**
 * Generate spoken narration via MiniMax TTS (`/t2a_v2`).
 * Defaults to a neutral Mandarin male voice that reads both zh + en well.
 */
export declare function generateTts(opts: {
    text: string;
    voiceId?: string;
    languageBoost?: string;
    speed?: number;
    vol?: number;
    pitch?: number;
    creds: MinimaxCredentials;
    signal?: AbortSignal;
}): Promise<MinimaxAudioResult>;
/**
 * Generate background music via MiniMax (`/music_generation`).
 * Instrumental-only by default (a video soundtrack rarely wants vocals).
 */
export declare function generateMusic(opts: {
    prompt: string;
    instrumental?: boolean;
    creds: MinimaxCredentials;
    signal?: AbortSignal;
}): Promise<MinimaxAudioResult>;
//# sourceMappingURL=minimax.d.ts.map