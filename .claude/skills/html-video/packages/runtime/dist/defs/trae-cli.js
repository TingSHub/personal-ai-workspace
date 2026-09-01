/**
 * Trae CLI public ACP adapter.
 *
 * html-video runs agent CLIs from the local studio/CLI process without a TTY.
 * Trae's ACP server therefore has to start in yolo mode so tool calls do not
 * block forever behind an interactive permission prompt the studio cannot
 * answer.
 */
export const traeCli = {
    id: 'trae-cli',
    name: 'Trae CLI',
    bin: 'traecli',
    versionArgs: ['--version'],
    buildArgs() {
        return ['acp', 'serve', '--yolo'];
    },
    streamFormat: 'acp-json-rpc',
    installUrl: 'https://www.volcengine.com/docs/86677/2227861?lang=zh',
};
//# sourceMappingURL=trae-cli.js.map