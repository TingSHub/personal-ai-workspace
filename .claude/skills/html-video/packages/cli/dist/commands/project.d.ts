/**
 * Project-centric CLI commands per RFC-05.
 */
import type { CliContext } from '../context.js';
export declare function projectCreate(ctx: CliContext, opts: {
    name: string;
    intent?: string;
    aspect?: string;
    commercial?: boolean;
}): Promise<void>;
export declare function projectList(ctx: CliContext): Promise<void>;
export declare function projectShow(ctx: CliContext, id: string): Promise<void>;
export declare function projectDelete(ctx: CliContext, id: string): Promise<void>;
export declare function projectAddAsset(ctx: CliContext, id: string, opts: {
    file?: string;
    inlineText?: string;
    inlineDataFile?: string;
    caption?: string;
}): Promise<void>;
export declare function projectRemoveAsset(ctx: CliContext, id: string, assetId: string): Promise<void>;
export declare function projectSetTemplate(ctx: CliContext, id: string, templateId: string): Promise<void>;
export declare function projectSetVar(ctx: CliContext, id: string, key: string, valueJson: string): Promise<void>;
export declare function projectSetVars(ctx: CliContext, id: string, varsFile: string): Promise<void>;
export declare function projectPreview(ctx: CliContext, id: string): Promise<void>;
export declare function projectRender(ctx: CliContext, id: string, opts: {
    output?: string;
    streamProgress?: boolean;
}): Promise<void>;
//# sourceMappingURL=project.d.ts.map