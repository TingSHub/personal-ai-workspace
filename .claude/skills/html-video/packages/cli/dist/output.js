/**
 * JSON-first output helpers per RFC-03.
 * `--json` (default for agent) emits NDJSON-friendly single-object lines.
 * Non-JSON mode uses simple readable text.
 */
let JSON_MODE = true;
export function setJsonMode(on) {
    JSON_MODE = on;
}
export function ok(payload) {
    if (JSON_MODE) {
        process.stdout.write(`${JSON.stringify({ status: 'ok', ...payload })}\n`);
    }
    else {
        process.stdout.write(`${pretty(payload)}\n`);
    }
}
export function fail(code, message, ctx = {}) {
    if (JSON_MODE) {
        process.stdout.write(`${JSON.stringify({ status: 'error', code, message, ...ctx })}\n`);
    }
    else {
        process.stderr.write(`✘ ${code}: ${message}\n`);
    }
    process.exit(1);
}
export function progress(stage, pct, extra = {}) {
    if (JSON_MODE) {
        process.stdout.write(`${JSON.stringify({ type: 'progress', stage, pct, ...extra })}\n`);
    }
    else {
        process.stdout.write(`  ${stage}: ${pct}%\n`);
    }
}
function pretty(p) {
    if (p == null)
        return '(empty)';
    if (typeof p === 'string')
        return p;
    return JSON.stringify(p, null, 2);
}
//# sourceMappingURL=output.js.map