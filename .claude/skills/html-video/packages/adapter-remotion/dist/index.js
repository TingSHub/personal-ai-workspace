import { capabilities } from './capabilities.js';
import { validate, remotionInstalled } from './validate.js';
import { render } from './render.js';
const adapter = {
    id: 'remotion',
    name: 'Remotion',
    upstreamVersion: '4.x',
    capabilities,
    validate,
    render,
};
export default adapter;
export { adapter, remotionInstalled };
//# sourceMappingURL=index.js.map