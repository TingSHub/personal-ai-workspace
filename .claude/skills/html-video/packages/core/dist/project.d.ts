/**
 * Project orchestrator: 单模板单视频工作流（RFC-05）。
 * - createProject
 * - addAsset / removeAsset
 * - setTemplate / setVariable / setVariables
 * - renderPreviewHtml: 调 EngineAdapter.renderToHtml() → HTML for iframe
 * - exportMp4: 调 EngineAdapter.render() → MP4 file
 */
import type { Asset, FrameRecord, Project } from './types/index.js';
import { type ContentGraph } from '@html-video/content-graph';
import type { AssetStore } from './asset-store.js';
import type { EngineRegistry, ProjectStore, TemplateRegistry } from './registry.js';
export interface CreateProjectInput {
    name: string;
    intent?: string;
    preferences?: Project['preferences'];
}
export interface ProjectOrchestratorDeps {
    projectRoot: string;
    engines: EngineRegistry;
    templates: TemplateRegistry;
    projects: ProjectStore;
    assets: AssetStore;
}
export declare class ProjectOrchestrator {
    private readonly deps;
    constructor(deps: ProjectOrchestratorDeps);
    create(input: CreateProjectInput): Promise<Project>;
    list(): Promise<Project[]>;
    load(id: string): Promise<Project>;
    remove(id: string): Promise<void>;
    addFileAsset(projectId: string, sourcePath: string, userCaption?: string): Promise<Project>;
    addInlineAsset(projectId: string, content: string, type: 'text' | 'data', userCaption?: string): Promise<Project>;
    /**
     * Store generated audio bytes (MP3 from MiniMax) as a project asset and
     * return the created Asset so the caller can reference it in `soundtrack`.
     * Unlike addFileAsset, this does NOT downgrade status — attaching a
     * soundtrack to an already-previewed video shouldn't invalidate the render.
     */
    addBufferAsset(projectId: string, bytes: Buffer, ext: string, userCaption?: string): Promise<{
        project: Project;
        asset: Asset;
    }>;
    removeAsset(projectId: string, assetId: string): Promise<Project>;
    setTemplate(projectId: string, templateId: string | null): Promise<Project>;
    setVariables(projectId: string, vars: Record<string, unknown>): Promise<Project>;
    setVariable(projectId: string, key: string, value: unknown): Promise<Project>;
    setAgent(projectId: string, agentId: string | null, agentModel?: string | null): Promise<Project>;
    /**
     * v0.3 chat-to-HTML: write raw HTML produced by an agent into the project's preview slot.
     * Single-frame fast-path. Clears any prior multi-frame graph state.
     */
    writePreviewHtmlRaw(projectId: string, html: string): Promise<{
        project: Project;
        htmlPath: string;
    }>;
    /**
     * Persist a content graph alongside the project. Validates first, throws
     * on cycles / unknown edges / etc.
     */
    writeContentGraph(projectId: string, graph: ContentGraph, opts?: {
        preserveFrames?: boolean;
    }): Promise<{
        project: Project;
        graphPath: string;
    }>;
    /**
     * Read the persisted content graph. Returns null if none.
     */
    readContentGraph(projectId: string): Promise<ContentGraph | null>;
    /**
     * Write one frame's HTML to disk. Updates the project's frames[] list,
     * keeping play-order consistent with the graph's topo sort.
     *
     * Frame filenames follow `<order>-<nodeId>.html` for visual debuggability.
     */
    writeFrameHtml(projectId: string, graphNodeId: string, html: string): Promise<{
        project: Project;
        frame: FrameRecord;
    }>;
    renderPreviewHtml(projectId: string): Promise<{
        project: Project;
        htmlPath: string;
    }>;
    exportMp4(args: {
        projectId: string;
        outputPath?: string;
        onProgress?: (pct: number, stage: string) => void;
        signal?: AbortSignal;
    }): Promise<{
        project: Project;
        outputPath: string;
    }>;
    /**
     * Resolve which engine + TemplateRef render a single frame. A frame that the
     * user has enhanced (engine='remotion' + nativeTemplateId) renders via the
     * native template's .tsx entry; otherwise it's the classic per-frame HTML on
     * the project's engine (hyperframes). The base `htmlPath` is always retained
     * on the frame so un-enhancing is non-destructive. (RFC-08/09)
     */
    private resolveFrameTemplateRef;
    /**
     * Enhance one data frame with a native engine template (the user-initiated
     * "motion enhancement" — RFC-08/09). Snapshots the source DataNode's `data`
     * onto the frame and points it at the native template. Asserts the node is a
     * `data` node and that its data fits the native template's expected shape, so
     * export doesn't later render NaN bars. The frame's `htmlPath` is untouched,
     * so {@link unenhanceFrame} fully reverts it.
     */
    enhanceFrameNative(projectId: string, graphNodeId: string, nativeTemplateId: string): Promise<{
        project: Project;
        frame: FrameRecord;
    }>;
    /**
     * Revert a frame's native enhancement back to its base hyperframes HTML.
     * Clears the three enhance fields; `htmlPath` was never touched. (RFC-08/09)
     */
    unenhanceFrame(projectId: string, graphNodeId: string): Promise<{
        project: Project;
        frame: FrameRecord;
    }>;
    /**
     * Render a single (enhanced) frame to a short MP4 for studio preview. A native
     * frame has no HTML to show in the iframe strip, so the studio renders it on
     * its own and plays the result as a <video>. Reuses {@link resolveFrameTemplateRef}
     * — the same per-frame engine/template resolution exportMp4 uses — so the
     * preview is pixel-identical to what the final export will stitch in.
     *
     * Writes to `frames/<order>.preview.mp4` (distinct from export's `frames/NN.mp4`
     * so the two never overwrite each other). No soundtrack mux — a per-frame
     * preview is silent and faster. Sets `frame.previewMp4Path` and saves (bumping
     * `updatedAt`, which the studio uses as the <video> cache-bust token).
     */
    renderFrameNativePreview(args: {
        projectId: string;
        graphNodeId: string;
        onProgress?: (pct: number, stage: string) => void;
        signal?: AbortSignal;
    }): Promise<{
        project: Project;
        frame: FrameRecord;
        previewPath: string;
    }>;
    /**
     * If the project has a soundtrack (music and/or narration), mux it into the
     * just-rendered video at `outputPath`. Renders to a temp file then renames
     * over the original. No-op when there's no soundtrack. Audio generation
     * never depends on ffmpeg — only this export-time mux does.
     */
    private applySoundtrack;
}
//# sourceMappingURL=project.d.ts.map