# render-covers-puppeteer(已归档)

账户米白账本封面渲染工具(puppeteer-core,单文件):一次调用同时输出 4:3/3:4 两个 check PNG。
未被取代、仍可用于封面 check 渲染;因 `scripts/` 主路径治理(固定渲染入口统一为
`scripts/render_cover_3x4.js` / `render_cover_4x3.js`,由 workflow by-name 引用)而移入归档,可恢复使用。

- 用法:`node render_covers_puppeteer.js <cover.html> <cover.png> <cover-3x4.png>`
- 注意:它不激活 `?format=landscape` 且整页截图(含工具栏/留白),如需全幅导出用 `scripts/render_cover_4x3.js` 与 `render_cover_3x4.js`
- 归档日期:2026-09-05(closeout)
