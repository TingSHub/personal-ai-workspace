/**
 * Stable error codes per RFC-01 + RFC-05.
 */
export type ErrorCode = 'engine-not-installed' | 'engine-not-registered' | 'template-invalid' | 'template-not-found' | 'render-failed' | 'render-timeout' | 'output-corrupt' | 'disk-full' | 'cancelled' | 'asset-not-found' | 'project-not-found' | 'invalid-input';
export declare class HtmlVideoError extends Error {
    readonly code: ErrorCode;
    readonly retryable: boolean;
    readonly context: Record<string, unknown>;
    readonly name = "HtmlVideoError";
    constructor(code: ErrorCode, message: string, retryable?: boolean, context?: Record<string, unknown>);
    toJSON(): Record<string, unknown>;
}
//# sourceMappingURL=errors.d.ts.map