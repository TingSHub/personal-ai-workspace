/**
 * @html-video/content-graph — RFC-06.
 *
 * Structured intermediate representation produced by the agent's first round,
 * consumed by the second round to render HTML frame sequences.
 *
 * See research/2026-05-28-understand-anything-takeaways.md (#1 content-graph,
 * #4 graph-then-sort) for the design rationale.
 */
/**
 * Validate a ContentGraph. Stops at the first cycle (reports it) but collects
 * all other errors so the agent gets one round-trip of feedback.
 */
export function validate(graph) {
    const errors = [];
    const warnings = [];
    if (!graph.nodes || graph.nodes.length === 0) {
        errors.push({ code: 'empty-graph', message: 'Graph has no nodes' });
        return { ok: false, errors, warnings };
    }
    const ids = new Set();
    for (const n of graph.nodes) {
        if (ids.has(n.id)) {
            errors.push({
                code: 'duplicate-node-id',
                message: `Duplicate node id "${n.id}"`,
                ref: n.id,
            });
        }
        ids.add(n.id);
        const kind = n.kind;
        if (kind !== 'entity' && kind !== 'data' && kind !== 'text') {
            errors.push({
                code: 'invalid-kind',
                message: `Node "${n.id}" has unknown kind "${kind}"`,
                ref: n.id,
            });
        }
    }
    for (const e of graph.edges) {
        if (e.from === e.to) {
            errors.push({
                code: 'self-edge',
                message: `Edge ${e.from} → ${e.to} is a self-edge`,
                ref: `${e.from}->${e.to}`,
            });
        }
        if (!ids.has(e.from)) {
            errors.push({
                code: 'edge-from-unknown-node',
                message: `Edge from unknown node "${e.from}"`,
                ref: `${e.from}->${e.to}`,
            });
        }
        if (!ids.has(e.to)) {
            errors.push({
                code: 'edge-to-unknown-node',
                message: `Edge to unknown node "${e.to}"`,
                ref: `${e.from}->${e.to}`,
            });
        }
    }
    // Cycle detection on dependency edges (the only kind that constrains order).
    const cycleNode = findDependencyCycle(graph);
    if (cycleNode) {
        errors.push({
            code: 'cycle',
            message: `Dependency cycle detected involving node "${cycleNode}"`,
            ref: cycleNode,
        });
    }
    return { ok: errors.length === 0, errors, warnings };
}
// ---------------------------------------------------------------------------
// Topo sort
// ---------------------------------------------------------------------------
/**
 * Linearise the graph into a frame play order.
 *
 * Algorithm:
 *   1. Build dependency adjacency (only "dependency" edges constrain order).
 *   2. Kahn topological sort; ties broken by sequence-edge order, else by
 *      original node array order.
 *
 * Returns node ids in playback order. Throws on cycle (callers should validate
 * first; this is a defensive throw).
 */
export function topoSort(graph) {
    const indeg = new Map();
    const deps = new Map(); // from -> to (unblocks)
    const nodeOrder = new Map();
    graph.nodes.forEach((n, i) => {
        indeg.set(n.id, 0);
        deps.set(n.id, []);
        nodeOrder.set(n.id, i);
    });
    for (const e of graph.edges) {
        if (e.kind !== 'dependency')
            continue;
        if (!indeg.has(e.from) || !indeg.has(e.to))
            continue;
        deps.get(e.from).push(e.to);
        indeg.set(e.to, (indeg.get(e.to) ?? 0) + 1);
    }
    // Sequence edges as a soft preference: if A->B (sequence) and both indeg=0,
    // prefer A before B.
    const seqAfter = new Map(); // node -> nodes that should come after
    for (const e of graph.edges) {
        if (e.kind !== 'sequence')
            continue;
        if (!indeg.has(e.from) || !indeg.has(e.to))
            continue;
        if (!seqAfter.has(e.from))
            seqAfter.set(e.from, new Set());
        seqAfter.get(e.from).add(e.to);
    }
    const ready = [];
    for (const [id, d] of indeg)
        if (d === 0)
            ready.push(id);
    // Stable sort by original node order so output is deterministic
    ready.sort((a, b) => (nodeOrder.get(a) ?? 0) - (nodeOrder.get(b) ?? 0));
    const out = [];
    while (ready.length > 0) {
        // Pick the ready node that:
        //   1. is NOT a "sequence successor" of any other ready node, and
        //   2. earliest in original order among the survivors.
        let pickIdx = 0;
        for (let i = 0; i < ready.length; i++) {
            const cand = ready[i];
            const blockedBySequence = ready.some((other) => other !== cand && seqAfter.get(other)?.has(cand));
            if (!blockedBySequence) {
                pickIdx = i;
                break;
            }
        }
        const next = ready.splice(pickIdx, 1)[0];
        out.push(next);
        for (const succ of deps.get(next) ?? []) {
            indeg.set(succ, (indeg.get(succ) ?? 1) - 1);
            if (indeg.get(succ) === 0) {
                // Insert maintaining original-order stability
                const ord = nodeOrder.get(succ) ?? 0;
                let insertAt = ready.length;
                for (let i = 0; i < ready.length; i++) {
                    if ((nodeOrder.get(ready[i]) ?? 0) > ord) {
                        insertAt = i;
                        break;
                    }
                }
                ready.splice(insertAt, 0, succ);
            }
        }
    }
    if (out.length !== graph.nodes.length) {
        throw new Error(`topoSort: cycle detected (sorted ${out.length} of ${graph.nodes.length} nodes)`);
    }
    return out;
}
// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
function findDependencyCycle(graph) {
    const adj = new Map();
    for (const n of graph.nodes)
        adj.set(n.id, []);
    for (const e of graph.edges) {
        if (e.kind !== 'dependency')
            continue;
        if (!adj.has(e.from) || !adj.has(e.to))
            continue;
        adj.get(e.from).push(e.to);
    }
    const WHITE = 0, GRAY = 1, BLACK = 2;
    const color = new Map();
    for (const id of adj.keys())
        color.set(id, WHITE);
    const stack = [];
    for (const start of adj.keys()) {
        if (color.get(start) !== WHITE)
            continue;
        color.set(start, GRAY);
        stack.push({ id: start, iter: adj.get(start)[Symbol.iterator]() });
        while (stack.length > 0) {
            const top = stack[stack.length - 1];
            const next = top.iter.next();
            if (next.done) {
                color.set(top.id, BLACK);
                stack.pop();
            }
            else {
                const c = color.get(next.value);
                if (c === GRAY)
                    return next.value;
                if (c === WHITE) {
                    color.set(next.value, GRAY);
                    stack.push({ id: next.value, iter: adj.get(next.value)[Symbol.iterator]() });
                }
            }
        }
    }
    return null;
}
/**
 * Look up a node by id. Returns undefined if missing — callers handle.
 */
export function getNode(graph, id) {
    return graph.nodes.find((n) => n.id === id);
}
/**
 * Default per-frame duration when a node doesn't set one.
 */
export const DEFAULT_FRAME_DURATION_SEC = 3;
/**
 * Compute total video duration by summing per-frame durations along the
 * topo-sorted play order.
 */
export function totalDurationSec(graph) {
    const order = topoSort(graph);
    let total = 0;
    for (const id of order) {
        const n = getNode(graph, id);
        total += n?.durationSec ?? DEFAULT_FRAME_DURATION_SEC;
    }
    return total;
}
//# sourceMappingURL=index.js.map