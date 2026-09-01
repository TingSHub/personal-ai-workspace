import type { EngineCapabilities } from '@html-video/core';
/**
 * Static capability declaration for Remotion (RFC-08 §1, cross-checked
 * 2026-06-06 against remotion@4.0.x).
 *
 * `licensing: 'commercial-restricted'` is a FIRST-CLASS field here, not a
 * footnote: Remotion is free for individuals / companies ≤3 people / non-profit,
 * but 4+ person teams pay. The agent reads this to steer "free / cheap" jobs
 * toward the free-osi engines (hyperframes / revideo) and only suggest Remotion
 * when the team already uses React or needs Lambda scale. That honesty is the
 * meta-layer's advantage over a Remotion-only tool — surface it, don't hide it.
 */
export declare const capabilities: EngineCapabilities;
//# sourceMappingURL=capabilities.d.ts.map