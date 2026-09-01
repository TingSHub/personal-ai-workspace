export const hermes = {
    id: 'hermes',
    name: 'Hermes (local CLI)',
    bin: 'hermes',
    versionArgs: ['version'],
    buildArgs(prompt) {
        // hermes -q reads its query from argv (not stdin). argv length on
        // macOS is ~256KB which fits any reasonable prompt.
        return ['chat', '-Q', '-q', prompt];
    },
    streamFormat: 'plain',
    installUrl: 'https://hermes.agentinfo.dev',
};
//# sourceMappingURL=hermes.js.map