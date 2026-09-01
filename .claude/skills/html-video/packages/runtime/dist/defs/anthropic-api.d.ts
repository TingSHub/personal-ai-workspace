/**
 * Anthropic Messages API (HTTP) agent.
 *
 * Bypasses the `claude --print` CLI entirely — that interface has a
 * non-deterministic "silently return 1 byte" failure mode on long creative
 * outputs (verified by hand on Joey's machine). Talking to the Messages API
 * directly is reliable and stream-friendly.
 *
 * Auth resolution (first match wins):
 *   1. ANTHROPIC_API_KEY        (canonical)
 *   2. ANTHROPIC_AUTH_TOKEN     (Joey's OpenRouter routing setup)
 *
 * Base URL:
 *   ANTHROPIC_BASE_URL or default https://api.anthropic.com
 *   When OpenRouter is in use, ANTHROPIC_BASE_URL is set to
 *   https://openrouter.ai/api — the OpenRouter shim accepts the standard
 *   Anthropic Messages payload + bare model names (claude-sonnet-4-6 etc).
 *
 * Model: claude-sonnet-4-6 by default. Sonnet 4.6 strikes the best balance
 * of speed / creativity / instruction-following for our HTML output;
 * upgradable per-call later if needed.
 */
import type { AgentDef } from '../types.js';
export declare const anthropicApi: AgentDef;
//# sourceMappingURL=anthropic-api.d.ts.map