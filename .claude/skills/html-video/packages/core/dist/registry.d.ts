/**
 * Registries for engine adapters, templates, and projects.
 * RFC-05: Storyboard removed; Project takes its place.
 */
import type { EngineAdapter, EngineId, Project, TemplateMetadata } from './types/index.js';
export declare class EngineRegistry {
    private adapters;
    register(adapter: EngineAdapter): void;
    get(id: EngineId): EngineAdapter;
    list(): EngineAdapter[];
    has(id: EngineId): boolean;
}
export declare class TemplateRegistry {
    private templates;
    scan(rootDir: string): Promise<TemplateMetadata[]>;
    get(id: string): TemplateMetadata;
    has(id: string): boolean;
    list(): TemplateMetadata[];
    search(opts: {
        intent?: string;
        aspect?: string;
        licenseAllow?: string[];
        enginesAvailable?: EngineId[];
        top?: number;
    }): {
        template: TemplateMetadata;
        score: number;
        reason: string;
    }[];
}
export declare class ProjectStore {
    private projectRoot;
    constructor(projectRoot: string);
    private dir;
    private projectDir;
    private path;
    /** Ensure project directory exists; returns its absolute path. */
    ensureDir(id: string): Promise<string>;
    save(project: Project): Promise<void>;
    load(id: string): Promise<Project>;
    list(): Promise<Project[]>;
    remove(id: string): Promise<void>;
}
//# sourceMappingURL=registry.d.ts.map