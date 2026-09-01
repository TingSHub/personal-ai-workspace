import type { AgentDef } from '../types.js';
/**
 * Gemini CLI def (`gemini`, by Google — google-gemini/gemini-cli).
 *
 * Headless usage: piping a prompt on stdin to a non-TTY `gemini` invocation
 * drops it into one-shot mode (prints the answer, exits) — verified locally
 * 2026-06-04 (a stdin-only run went straight to the auth check rather than
 * opening the interactive TUI). Default stdout is free-form text
 * (`--output-format text`), which our extractor reads to pull the fenced
 * ```html``` block, so we stay in plain mode.
 *
 * No model / API key is set here: if the user hasn't configured GEMINI_API_KEY
 * (or another auth method) the CLI prints a clear auth error to stdout, which
 * surfaces in the studio chat as-is.
 */
export declare const gemini: AgentDef;
//# sourceMappingURL=gemini.d.ts.map