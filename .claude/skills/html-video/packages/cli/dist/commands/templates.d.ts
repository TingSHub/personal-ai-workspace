import type { CliContext } from '../context.js';
interface SearchOpts {
    intent?: string;
    aspect?: string;
    licenseAllow?: string;
    top?: number;
}
export declare function searchTemplates(ctx: CliContext, opts: SearchOpts): Promise<void>;
export declare function inspectTemplate(ctx: CliContext, id: string): Promise<void>;
export {};
//# sourceMappingURL=templates.d.ts.map