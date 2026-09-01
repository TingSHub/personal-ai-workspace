import type { AgentDef } from '../types.js';
/**
 * Trae CLI public ACP adapter.
 *
 * html-video runs agent CLIs from the local studio/CLI process without a TTY.
 * Trae's ACP server therefore has to start in yolo mode so tool calls do not
 * block forever behind an interactive permission prompt the studio cannot
 * answer.
 */
export declare const traeCli: AgentDef;
//# sourceMappingURL=trae-cli.d.ts.map