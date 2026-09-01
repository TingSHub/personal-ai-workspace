import type { TemplateRef, ValidationResult } from '@html-video/core';
/**
 * Validate a template against the Remotion adapter. Cheap & read-only (RFC-01):
 * no bundling, no model calls — just engine match + source existence + a soft
 * note when the optional Remotion peer deps aren't installed yet.
 *
 * Phase 1: a template's `sourcePath` is an HTML frame the bridge renders. The
 * `engine` field may be 'remotion' (native, Phase 2) or 'hyperframes' (an HTML
 * frame the user explicitly chose to render through Remotion) — accept both so
 * the bridge can take any HTML frame.
 */
export declare function validate(template: TemplateRef): ValidationResult;
/** Best-effort, synchronous check that the Remotion renderer can be resolved. */
export declare function remotionInstalled(): boolean;
//# sourceMappingURL=validate.d.ts.map