/**
 * Hyperframes render() — real recording via Playwright + ffmpeg.
 *
 * Per-frame strategy (orchestrator already loops per node and concats):
 *   1. Launch chromium headless at the configured resolution
 *   2. recordVideo into a tmp dir
 *   3. file:// load the frame HTML
 *   4. wait `durationSec` so any opening animation completes + plays
 *   5. close → playwright dumps a webm
 *   6. ffmpeg transmux/encode the webm to mp4 at `outputPath`
 *
 * Upstream Hyperframes was never required at runtime for this adapter —
 * our generated HTML is plain inline-CSS+JS, chromium runs it as-is.
 */
import type { HtmlSceneOutput, RenderContext, RenderInput, RenderOutput } from '@html-video/core';
/** Real render: chromium records the page, ffmpeg transcodes to MP4. */
export declare function render(input: RenderInput, ctx: RenderContext): Promise<RenderOutput>;
/**
 * Render template to a single HTML preview.
 *
 * v0.1: read the source HTML file (a Hyperframes template is HTML+CSS+JS),
 * inject a banner showing the variables, copy referenced assets, write to ctx.workDir.
 * Real upstream Hyperframes integration will replace the inject + add a frame-bound clock.
 */
export declare function renderToHtml(input: RenderInput, ctx: RenderContext): Promise<HtmlSceneOutput>;
//# sourceMappingURL=render.d.ts.map