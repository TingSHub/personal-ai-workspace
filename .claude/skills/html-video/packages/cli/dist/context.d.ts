/**
 * Bootstrap shared CLI context: project root, registries, stores, orchestrator.
 */
import { AssetStore, EngineRegistry, ProjectOrchestrator, ProjectStore, TemplateRegistry } from '@html-video/core';
import { MediaConfigStore } from './media-config.js';
export interface CliContext {
    projectRoot: string;
    engines: EngineRegistry;
    templates: TemplateRegistry;
    projects: ProjectStore;
    assets: AssetStore;
    orchestrator: ProjectOrchestrator;
    templatesDir: string;
    mediaConfig: MediaConfigStore;
}
export declare function findProjectRoot(start?: string): string;
export declare function bootstrap(opts?: {
    cwd?: string;
}): Promise<CliContext>;
//# sourceMappingURL=context.d.ts.map