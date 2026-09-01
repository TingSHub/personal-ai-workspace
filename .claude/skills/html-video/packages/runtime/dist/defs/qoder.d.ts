import type { AgentDef } from '../types.js';
/**
 * Qoder CLI def (`qodercli`, by Qoder — npm `@qoder-ai/qodercli`).
 *
 * Qoder ships two binaries: `qoder` (the IDE / Electron wrapper) and
 * `qodercli` (the standalone coding agent CLI, installed via npm).
 * html-video uses the latter — it's the headless-capable one.
 *
 * Headless contract (same shape as Claude Code / Codex / Qwen):
 *   echo "<prompt>" | qodercli -p - --permission-mode bypass_permissions
 *
 *   -p -          →  non-interactive, read prompt from stdin, print to stdout.
 *   --permission-mode bypass_permissions  →  auto-approve all tool calls
 *     (file writes, shell, etc.) so the session never blocks on an
 *     interactive permission prompt the studio cannot answer.
 *
 * Prompt is passed via stdin (promptViaStdin: true) — avoids Windows shell
 * escaping issues with backticks, quotes, and CJK chars in long prompts.
 * Default stdout is plain text, so the extractor reads the fenced ```html``` block.
 *
 * Version probe: `qodercli -v` → e.g. "1.0.14".
 */
export declare const qoderCli: AgentDef;
//# sourceMappingURL=qoder.d.ts.map