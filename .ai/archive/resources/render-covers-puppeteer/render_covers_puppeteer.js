const puppeteer = require(process.env.PUPPETEER_CORE || 'puppeteer-core');
const path = require('path');

const [coverPath, output4x3, output3x4] = process.argv.slice(2);
if (!coverPath || !output4x3 || !output3x4) {
  console.error('usage: render_covers_puppeteer.js <cover.html> <cover.png> <cover-3x4.png>');
  process.exit(2);
}

(async () => {
  const browser = await puppeteer.launch({
    headless: 'shell',
    executablePath: process.env.HYPERFRAMES_CHROME || undefined,
  });
  for (const item of [
    { width: 1440, height: 1080, output: output4x3 },
    { width: 1080, height: 1440, output: output3x4 },
  ]) {
    const page = await browser.newPage();
    await page.setViewport({ width: item.width, height: item.height, deviceScaleFactor: 1 });
    await page.goto(`file://${path.resolve(coverPath)}`, { waitUntil: 'networkidle0' });
    const cropFix = item.width === 1440 ? '.hero{left:1040px!important;right:auto!important;}' : '';
    await page.addStyleTag({ content: `html,body,.cover{width:${item.width}px!important;height:${item.height}px!important;}${cropFix}` });
    await page.screenshot({ path: path.resolve(item.output), type: 'png' });
    await page.close();
  }
  await browser.close();
  console.log(JSON.stringify({ status: 'PASS', outputs: [path.resolve(output4x3), path.resolve(output3x4)] }));
})().catch((error) => {
  console.error(error.stack || String(error));
  process.exit(1);
});
