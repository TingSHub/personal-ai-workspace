/**
 * @html-video/content-graph — RFC-06.
 *
 * Structured intermediate representation produced by the agent's first round,
 * consumed by the second round to render HTML frame sequences.
 *
 * See research/2026-05-28-understand-anything-takeaways.md (#1 content-graph,
 * #4 graph-then-sort) for the design rationale.
 */
export type NodeKind = 'entity' | 'data' | 'text';
export interface BaseNode {
    /** Stable id; agent picks readable strings like "intro_logo", "stat_users". */
    id: string;
    kind: NodeKind;
    /**
     * Short label for UI (graph view). Optional — falls back to id.
     */
    label?: string;
    /**
     * Optional intent hint for the frame composer:
     *   "intro" / "data-bar" / "image-pan" / "quote" / "outro" / "list" / ...
     * Free-form; the frame-composer agent maps it to template choice.
     */
    frameIntent?: string;
    /**
     * Suggested duration in seconds for this frame. Defaults to 3s if absent.
     */
    durationSec?: number;
}
export interface EntityNode extends BaseNode {
    kind: 'entity';
    /**
     * Free-form props for branding entities (logo path, brand color, etc).
     * The frame-composer reads these to seed the HTML.
     */
    props: Record<string, unknown>;
}
export interface DataNode extends BaseNode {
    kind: 'data';
    /**
     * Concrete data points to visualise: numbers, percentages, time series.
     * Schema is permissive — any JSON the composer can render.
     */
    data: unknown;
}
export interface TextNode extends BaseNode {
    kind: 'text';
    /**
     * Headline / quote / caption / paragraph copy.
     */
    text: string;
}
export type Node = EntityNode | DataNode | TextNode;
export type EdgeKind = 'sequence' | 'contrast' | 'dependency';
export interface Edge {
    /** Source node id */
    from: string;
    /** Target node id */
    to: string;
    kind: EdgeKind;
    /**
     * Optional human-readable reason ("contrasts before/after", "depends on
     * concept introduced in B"). Helps the frame-composer pick layout cues.
     */
    reason?: string;
}
export interface ContentGraph {
    /** Schema version. v1 = this RFC-06 draft. */
    schemaVersion: 1;
    /**
     * High-level intent classification. Steers the frame-composer:
     *   - "single-frame": short brand/title card; collapse to one frame.
     *   - "explainer":   teach a concept; honour dependency edges.
     *   - "data-viz":    walk through numbers; sequence edges drive order.
     *   - "promo":       pacy social-cut style.
     *   - "comparison":  before/after; contrast edges drive layout.
     */
    intent: 'single-frame' | 'explainer' | 'data-viz' | 'promo' | 'comparison' | 'other';
    /**
     * One-line synopsis the agent writes for itself / the user. Shown in
     * studio's graph view as the "what is this video about?" header.
     */
    synopsis?: string;
    nodes: Node[];
    edges: Edge[];
}
export interface GraphValidationError {
    code: 'duplicate-node-id' | 'edge-from-unknown-node' | 'edge-to-unknown-node' | 'self-edge' | 'cycle' | 'empty-graph' | 'invalid-kind';
    message: string;
    /** Offending node or edge for UI highlighting. */
    ref?: string;
}
export interface GraphValidationResult {
    ok: boolean;
    errors: GraphValidationError[];
    warnings: GraphValidationError[];
}
/**
 * Validate a ContentGraph. Stops at the first cycle (reports it) but collects
 * all other errors so the agent gets one round-trip of feedback.
 */
export declare function validate(graph: ContentGraph): GraphValidationResult;
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
export declare function topoSort(graph: ContentGraph): string[];
/**
 * Look up a node by id. Returns undefined if missing — callers handle.
 */
export declare function getNode(graph: ContentGraph, id: string): Node | undefined;
/**
 * Default per-frame duration when a node doesn't set one.
 */
export declare const DEFAULT_FRAME_DURATION_SEC = 3;
/**
 * Compute total video duration by summing per-frame durations along the
 * topo-sorted play order.
 */
export declare function totalDurationSec(graph: ContentGraph): number;
//# sourceMappingURL=index.d.ts.map