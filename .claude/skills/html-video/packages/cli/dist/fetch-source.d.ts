/**
 * Fetch external content sources (web articles + GitHub repos) server-side and
 * turn them into Markdown the agent can read.
 *
 * Why server-side: the studio's agents (claude --print / cursor-agent / codex /
 * the Messages API) have no network access and only consume a plain-text
 * prompt. So when a user pastes a link, the server fetches + flattens it here,
 * stores it as a text asset, and lets the existing attachment→prompt pipeline
 * feed it to the agent.
 *
 * Zero runtime deps (matches the CLI package's minimalism): native fetch +
 * a lean regex HTML→Markdown pass, GitHub's public REST API for repos.
 */
export interface FetchedSource {
    url: string;
    title: string;
    markdown: string;
    kind: 'article' | 'repo';
    truncated: boolean;
}
/** Extract up to `max` distinct http(s) URLs from free text (in order). */
export declare function extractUrls(text: string, max?: number): string[];
/**
 * Reject URLs that point at localhost / link-local / private network ranges
 * (SSRF guard). Only plain http(s) public hosts are allowed.
 */
export declare function assertPublicHttpUrl(raw: string): URL;
/** Dispatch: GitHub repo URL → repo summary, anything else → article. */
export declare function fetchSource(rawUrl: string, signal?: AbortSignal): Promise<FetchedSource>;
/** Lean, dependency-free HTML→Markdown. Not a full converter — just enough to
 *  give the agent readable prose with headings, lists, links kept. */
export declare function htmlToMarkdown(html: string): string;
//# sourceMappingURL=fetch-source.d.ts.map