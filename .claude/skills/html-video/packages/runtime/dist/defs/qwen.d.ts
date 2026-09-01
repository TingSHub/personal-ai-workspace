import type { AgentDef } from '../types.js';
/**
 * Qwen Code def (`qwen`, by Alibaba — QwenLM/qwen-code).
 *
 * Qwen Code is a fork of Gemini CLI, so the headless contract matches: piping
 * a prompt on stdin to a non-TTY invocation runs it once and exits, default
 * stdout is free-form text. We stay in plain mode and read the fenced
 * ```html``` block from the output.
 *
 * bin is `qwen` (npm `@qwen-code/qwen-code`), NOT `gemini`.
 */
export declare const qwen: AgentDef;
//# sourceMappingURL=qwen.d.ts.map