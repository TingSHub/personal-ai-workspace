/**
 * HTTP server for the project studio (RFC-05 §UI).
 * Serves @html-video/project-studio static UI + project / template REST APIs.
 */
import type { CliContext } from './context.js';
interface StudioHandle {
    url: string;
    port: number;
    close: () => void;
}
export declare function startStudioServer(ctx: CliContext, port: number): Promise<StudioHandle>;
/**
 * Recover the real filename from a multipart part header (issue #9).
 *
 * Two encodings can appear:
 *  - `filename*=UTF-8''%E4%B8%AD%E6%96%87.md` (RFC 5987, percent-encoded) —
 *    decode the percent-escapes after stripping the charset prefix.
 *  - `filename="中文.md"` — the bytes are UTF-8, but the multipart body was
 *    read as a latin1 string, so each UTF-8 byte became one latin1 char. Round
 *    -trip latin1→utf8 to restore the original. If the name was plain ASCII the
 *    round-trip is a no-op.
 */
export declare function decodeUploadFilename(star: string | undefined, plain: string | undefined): string;
/**
 * Best-effort parse of format params from a FREE-TEXT user reply.
 *
 * The format step is supposed to render an `hv-form` card (segmented buttons)
 * whose submit carries an explicit `[hv-form:submit]` marker. But the model
 * sometimes ignores that instruction and instead asks for the params in prose
 * ("9:16 竖屏 / 3s / 6 …"); the user then types the answer free-form, with no
 * marker. Without this parser the state machine can't tell the params were
 * already given, so it loops — re-asking the same thing in a different shape
 * (issue #2). We extract aspect / duration / frame_count heuristically so a
 * typed reply is treated the same as a card submit.
 *
 * Returns undefined when the text carries no recognisable format signal, so
 * callers can fall through to other phase logic.
 */
export declare function parseFormatReply(text: string): Record<string, string> | undefined;
export {};
//# sourceMappingURL=studio-server.d.ts.map