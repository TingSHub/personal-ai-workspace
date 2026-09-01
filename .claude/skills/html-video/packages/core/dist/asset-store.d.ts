/**
 * Content-addressed asset store, scoped per project.
 * RFC-05 §文件存储.
 */
import type { Asset, AssetType } from './types/index.js';
export interface AssetStoreOptions {
    projectRoot: string;
}
export declare class AssetStore {
    private readonly projectsDir;
    constructor(opts: AssetStoreOptions);
    private projectDir;
    private assetsDir;
    static computeId(filePath: string): Promise<string>;
    static computeInlineId(content: string): string;
    static guessMime(filePath: string): {
        mime: string;
        type: AssetType;
    };
    addFileAsset(projectId: string, sourcePath: string, userTags?: string[], userCaption?: string): Promise<Asset>;
    addInlineAsset(projectId: string, content: string, type: 'text' | 'data', userTags?: string[], userCaption?: string): Promise<Asset>;
    /**
     * Store raw bytes (e.g. an MP3 returned by a generation API) as a
     * content-addressed asset. The id is the sha1 of the bytes, so identical
     * payloads dedupe; `ext` drives the mime/type via {@link guessMime}.
     */
    addBufferAsset(projectId: string, bytes: Buffer, ext: string, userTags?: string[], userCaption?: string): Promise<Asset>;
    resolvePath(asset: Asset): string;
}
//# sourceMappingURL=asset-store.d.ts.map