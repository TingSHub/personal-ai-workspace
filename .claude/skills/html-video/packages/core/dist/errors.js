/**
 * Stable error codes per RFC-01 + RFC-05.
 */
export class HtmlVideoError extends Error {
    code;
    retryable;
    context;
    name = 'HtmlVideoError';
    constructor(code, message, retryable = false, context = {}) {
        super(message);
        this.code = code;
        this.retryable = retryable;
        this.context = context;
    }
    toJSON() {
        return {
            name: this.name,
            code: this.code,
            message: this.message,
            retryable: this.retryable,
            context: this.context,
        };
    }
}
//# sourceMappingURL=errors.js.map