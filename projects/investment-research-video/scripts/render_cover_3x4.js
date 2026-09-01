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
  await page.goto(`file://${path.resolve(coverPath)}`, { waitUntil: 'networkidle' });
  await page.addStyleTag({ content: 'html,body,.cover{width:1080px!important;height:1440px!important;}' });
  await page.screenshot({ path: path.resolve(outputPath), type: 'png' });
  await browser.close();
  console.log(JSON.stringify({ status: 'PASS', width: 1080, height: 1440, output: path.resolve(outputPath) }));
})().catch((error) => {
  console.error(error.stack || String(error));
  process.exit(1);
});
