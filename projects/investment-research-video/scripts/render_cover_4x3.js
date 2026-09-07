#!/usr/bin/env node
/**
 * Render an existing cover.html to a standalone 4:3 landscape PNG.
 * Usage: node scripts/render_cover_4x3.js <cover.html> <cover.png>
 */

const { chromium } = require('/home/henry/node_modules/playwright');
const path = require('path');

const [coverPath, outputPath] = process.argv.slice(2);
if (!coverPath || !outputPath) {
  console.error('usage: node scripts/render_cover_4x3.js <cover.html> <cover.png>');
  process.exit(2);
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1440, height: 1080 }, deviceScaleFactor: 1 });
  // 必须带上 ?format=landscape，页面才会切换 .landscape 布局与横版背景
  await page.goto(`file://${path.resolve(coverPath)}?format=landscape`, { waitUntil: 'networkidle' });
  await page.evaluate(async () => {
    await document.fonts.ready;
    await Promise.all([...document.images].map((i) => i.decode().catch(() => {})));
  });
  // 全幅导出：覆盖 stage 缩放与 fit() transform，隐藏预览工具栏
  await page.addStyleTag({
    content:
      'html,body{width:1440px!important;height:1080px!important}.cover{width:1440px!important;height:1080px!important;transform:none!important}.toolbar,.hint{display:none!important}',
  });
  await page.waitForTimeout(200);
  // 只截 #cover 元素，输出画布原生 1440×1080 全幅 PNG
  await page.locator('#cover, .cover').first().screenshot({ path: path.resolve(outputPath), type: 'png' });
  await browser.close();
  console.log(JSON.stringify({ status: 'PASS', width: 1440, height: 1080, output: path.resolve(outputPath) }));
})().catch((error) => {
  console.error(error.stack || String(error));
  process.exit(1);
});
