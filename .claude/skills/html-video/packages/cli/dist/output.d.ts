/**
 * JSON-first output helpers per RFC-03.
 * `--json` (default for agent) emits NDJSON-friendly single-object lines.
 * Non-JSON mode uses simple readable text.
 */
export declare function setJsonMode(on: boolean): void;
export declare function ok(payload: unknown): void;
export declare function fail(code: string, message: string, ctx?: Record<string, unknown>): never;
export declare function progress(stage: string, pct: number, extra?: Record<string, unknown>): void;
//# sourceMappingURL=output.d.ts.map