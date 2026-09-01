/**
 * Minimal ACP (Agent Client Protocol) JSON-RPC client over child-process stdio.
 *
 * Used for AMR (the `vela agent run --runtime opencode` runtime), which speaks
 * ACP rather than printing to stdout. This is a slim, single-prompt client —
 * just enough to drive one turn and stream the text back; it does NOT implement
 * the full OD daemon ACP surface (permissions, terminals, MCP, multi-turn).
 *
 * Handshake (all newline-delimited JSON-RPC 2.0 on stdin/stdout):
 *   → initialize        { protocolVersion, clientCapabilities, clientInfo }
 *   → session/new       { cwd, mcpServers: [] }
 *   → session/set_model  { sessionId, modelId }   (only when model !== 'default')
 *   → session/prompt     { sessionId, prompt: [{type:'text', text}] }
 *   ← session/update notifications: agent_message_chunk.content.text = output
 *   ← result for the prompt request id = turn complete
 *
 * Distilled from open-design/apps/daemon/src/acp.ts (the production version).
 */
import { spawn as cpSpawn } from 'node:child_process';
import { resolve as resolvePath } from 'node:path';
const ACP_PROTOCOL_VERSION = 1;
const DEFAULT_STAGE_TIMEOUT_MS = 120_000;
export async function runAcpAgent(opts) {
    const cwd = resolvePath(opts.cwd || process.cwd());
    const child = cpSpawn(opts.bin, opts.args, {
        cwd,
        env: { ...process.env, ...(opts.env ?? {}) },
        stdio: ['pipe', 'pipe', 'pipe'],
    });
    if (!child.stdin || !child.stdout) {
        opts.onEvent({ type: 'error', message: 'ACP: child has no stdio pipes' });
        return { exitCode: -1 };
    }
    let stderrBuf = '';
    child.stderr?.on('data', (c) => { stderrBuf += c.toString('utf8'); });
    return await new Promise((done) => {
        let settled = false;
        let nextId = 1;
        let sessionId = null;
        let initId = null;
        let newSessionId = null;
        let setModelId = null;
        let promptId = null;
        let buf = '';
        let stageTimer = null;
        const writeRpc = (id, method, params) => {
            child.stdin.write(`${JSON.stringify({ jsonrpc: '2.0', id, method, params })}\n`);
        };
        const armTimer = (label) => {
            if (stageTimer)
                clearTimeout(stageTimer);
            stageTimer = setTimeout(() => finish(-1, `ACP timed out waiting for ${label}`), DEFAULT_STAGE_TIMEOUT_MS);
        };
        const finish = (code, errMsg) => {
            if (settled)
                return;
            settled = true;
            if (stageTimer)
                clearTimeout(stageTimer);
            if (errMsg) {
                const tail = stderrBuf.trim().slice(-400);
                opts.onEvent({ type: 'error', message: tail ? `${errMsg} — ${tail}` : errMsg });
            }
            try {
                child.kill('SIGTERM');
            }
            catch { /* already gone */ }
            done({ exitCode: code });
        };
        opts.signal.addEventListener('abort', () => finish(-1));
        child.on('error', (err) => finish(-1, `ACP spawn failed: ${err.message}`));
        child.on('exit', (code) => {
            // Normal completion path resolves on the prompt result; an exit before
            // that is an error (often: not logged in, surfaced on stderr).
            if (!settled)
                finish(code ?? -1, `vela exited (code ${code ?? 'null'}) before the turn completed`);
        });
        const handle = (msg) => {
            // --- responses to our requests (have an id + result/error) ---
            if ('id' in msg && (('result' in msg) || ('error' in msg))) {
                if (msg.error) {
                    const e = msg.error;
                    return finish(-1, `ACP error${e.code ? ` ${e.code}` : ''}: ${e.message ?? 'unknown'}`);
                }
                const id = msg.id;
                if (id === initId) {
                    // initialized → open a session
                    newSessionId = nextId++;
                    armTimer('session/new');
                    return writeRpc(newSessionId, 'session/new', { cwd, mcpServers: [] });
                }
                if (id === newSessionId) {
                    const result = msg.result;
                    sessionId = result?.sessionId ?? null;
                    if (!sessionId)
                        return finish(-1, 'ACP: session/new returned no sessionId');
                    if (opts.model && opts.model !== 'default') {
                        setModelId = nextId++;
                        armTimer('session/set_model');
                        return writeRpc(setModelId, 'session/set_model', { sessionId, modelId: opts.model });
                    }
                    return sendPrompt();
                }
                if (id === setModelId) {
                    return sendPrompt();
                }
                if (id === promptId) {
                    // Turn complete.
                    opts.onEvent({ type: 'message_end', reason: 'ok' });
                    return finish(0);
                }
                return;
            }
            // --- notifications (method, no response expected) ---
            if (msg.method === 'session/update') {
                const params = msg.params;
                const update = params?.update;
                if (update?.sessionUpdate === 'agent_message_chunk') {
                    const content = update.content;
                    if (content?.text) {
                        armTimer('session/prompt stream');
                        opts.onEvent({ type: 'text', chunk: content.text });
                    }
                }
                return;
            }
            // --- requests FROM the agent (permission etc.) — auto-deny/ignore ---
            if (msg.method === 'session/request_permission' && 'id' in msg) {
                // We run non-interactively; reject so the agent proceeds with defaults
                // rather than hanging. (OD picks an allow option; for our read-only
                // text turn, declining is safe and avoids file mutations.)
                const params = msg.params;
                const allow = params?.options?.find((o) => /allow|accept|yes/i.test(o.kind ?? o.optionId ?? ''));
                const optionId = allow?.optionId ?? params?.options?.[0]?.optionId;
                if (optionId)
                    child.stdin.write(`${JSON.stringify({ jsonrpc: '2.0', id: msg.id, result: { outcome: { outcome: 'selected', optionId } } })}\n`);
                return;
            }
        };
        const sendPrompt = () => {
            promptId = nextId++;
            armTimer('session/prompt');
            writeRpc(promptId, 'session/prompt', {
                sessionId,
                prompt: [{ type: 'text', text: opts.prompt }],
            });
        };
        child.stdout.on('data', (chunk) => {
            buf += chunk.toString('utf8');
            let nl;
            while ((nl = buf.indexOf('\n')) >= 0) {
                const line = buf.slice(0, nl).trim();
                buf = buf.slice(nl + 1);
                if (!line)
                    continue;
                let msg;
                try {
                    msg = JSON.parse(line);
                }
                catch {
                    continue;
                } // ignore non-JSON noise
                try {
                    handle(msg);
                }
                catch (e) {
                    finish(-1, `ACP handler error: ${e instanceof Error ? e.message : e}`);
                }
            }
        });
        // Kick off the handshake.
        initId = nextId++;
        armTimer('initialize');
        writeRpc(initId, 'initialize', {
            protocolVersion: ACP_PROTOCOL_VERSION,
            clientCapabilities: { terminal: false },
            clientInfo: { name: opts.clientName ?? 'html-video', version: opts.clientVersion ?? '0.1' },
        });
    });
}
//# sourceMappingURL=acp-client.js.map