#!/usr/bin/env node
/**
 * Render an existing cover.html to a standalone 4:3 PNG.
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
  await page.goto(`file://${path.resolve(coverPath)}`, { waitUntil: 'networkidle' });
  await page.addStyleTag({ content: 'html,body,.cover{width:1440px!important;height:1080px!important;}' });
  await page.screenshot({ path: path.resolve(outputPath), type: 'png' });
  await browser.close();
  console.log(JSON.stringify({ status: 'PASS', width: 1440, height: 1080, output: path.resolve(outputPath) }));
})().catch((error) => {
  console.error(error.stack || String(error));
  process.exit(1);
});
