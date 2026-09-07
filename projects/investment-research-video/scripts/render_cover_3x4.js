#!/usr/bin/env node
/**
 * Render an existing cover.html to a standalone 3:4 portrait PNG.
 * Usage: node scripts/render_cover_3x4.js <cover.html> <cover.png>
 */

const { chromium } = require('/home/henry/node_modules/playwright');
const path = require('path');

const [coverPath, outputPath] = process.argv.slice(2);
if (!coverPath || !outputPath) {
  console.error('usage: node scripts/render_cover_3x4.js <cover.html> <cover.png>');
  process.exit(2);
}

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1440 }, deviceScaleFactor: 1 });
  // 默认即竖版布局；等待本地字体与内嵌背景图片就绪后再截图
  await page.goto(`file://${path.resolve(coverPath)}?format=portrait`, { waitUntil: 'networkidle' });
  await page.evaluate(async () => {
    await document.fonts.ready;
    await Promise.all([...document.images].map((i) => i.decode().catch(() => {})));
  });
  // 全幅导出：覆盖 stage 缩放与 fit() transform，隐藏预览工具栏
  await page.addStyleTag({
    content:
      'html,body{width:1080px!important;height:1440px!important}.cover{width:1080px!important;height:1440px!important;transform:none!important}.toolbar,.hint{display:none!important}',
  });
  await page.waitForTimeout(200);
  // 只截 #cover 元素，输出画布原生 1080×1440 全幅 PNG
  await page.locator('#cover, .cover').first().screenshot({ path: path.resolve(outputPath), type: 'png' });
  await browser.close();
  console.log(JSON.stringify({ status: 'PASS', width: 1080, height: 1440, output: path.resolve(outputPath) }));
})().catch((error) => {
  console.error(error.stack || String(error));
  process.exit(1);
});
