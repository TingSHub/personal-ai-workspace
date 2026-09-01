export const cursorAgent = {
    id: 'cursor-agent',
    name: 'Cursor Agent',
    bin: 'cursor-agent',
    versionArgs: ['--version'],
    buildArgs(_prompt, _ctx) {
        return ['--print'];
    },
    streamFormat: 'plain',
    promptViaStdin: true,
    installUrl: 'https://cursor.com/cli',
};
//# sourceMappingURL=cursor-agent.js.map