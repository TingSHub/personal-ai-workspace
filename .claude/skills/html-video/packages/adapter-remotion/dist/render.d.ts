import type { RenderInput, RenderContext, RenderOutput } from '@html-video/core';
/**
 * Make an HTML frame safe to render inside Remotion's headless chromium iframe.
 *
 * A render-blocking external `<link rel="stylesheet">` (e.g. Google Fonts) keeps
 * the iframe's render tree from painting until the stylesheet resolves. In the
 * headless render environment that request is slow or unreachable, so it never
 * resolves and Remotion screenshots a fully black frame — even though the DOM is
 * correct. (Same family as the file:// fetch issue tracked in #16/#18.)
 *
 * Video rendering must be deterministic and offline-safe, so we do NOT gamble on
 * a network font load: we convert blocking external stylesheet links into
 * non-blocking async loads (media="print" + onload swap). The font applies if it
 * arrives in time; if not, the CSS `font-family` fallback (templates declare one,
 * e.g. `'Archivo Black', sans-serif`) renders instead. Either way paint is never
 * blocked. Inline <style> and same-document CSS are untouched.
 */
export declare function neutralizeBlockingResources(html: string): string;
export declare function render(input: RenderInput, ctx: RenderContext): Promise<RenderOutput>;
//# sourceMappingURL=render.d.ts.map