#!/usr/bin/env node
// 通过创作者中心单作品详情页的官方“导出”按钮下载结构化 Excel。
// 只操作登录态对应的本人账号；不读取或保存 Cookie、msToken、a_bogus 等鉴权信息。

import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { pathToFileURL, fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const DEFAULT_REPO = path.resolve(SCRIPT_DIR, "../../../../.claude/skills/douyin-creator-tools");

function parseArgs(argv) {
  const args = { itemId: "", outDir: "", repo: DEFAULT_REPO, profile: "", headless: true, timeout: 20 };
  for (let i = 2; i < argv.length; i += 1) {
    const key = argv[i];
    if (key === "--item-id") { args.itemId = argv[++i]; continue; }
    if (key === "--out-dir") { args.outDir = argv[++i]; continue; }
    if (key === "--repo") { args.repo = argv[++i]; continue; }
    if (key === "--profile") { args.profile = argv[++i]; continue; }
    if (key === "--headed") { args.headless = false; continue; }
    if (key === "--timeout") { args.timeout = Number(argv[++i]); continue; }
    throw new Error(`未知参数: ${key}`);
  }
  if (!/^\d+$/.test(args.itemId)) throw new Error("--item-id must be a numeric Douyin item id");
  if (!args.outDir) throw new Error("缺少 --out-dir 路径");
  return args;
}

async function loadRepoModules(repoRoot) {
  const require = createRequire(path.join(repoRoot, "package.json"));
  const playwright = require("playwright");
  const lockUrl = pathToFileURL(path.join(repoRoot, "src/lib/browser-session-lock.mjs"));
  const lockModule = await import(lockUrl);
  return { playwright, lockModule };
}

async function sectionExportButton(page, section) {
  const title = page.locator("div.card-title-M2BOZI").filter({ hasText: section }).first();
  if (!(await title.count())) return null;
  const card = title.locator("xpath=ancestor::div[contains(@class, 'card-')][1]");
  const button = card.locator("button:visible", { hasText: "导出" }).first();
  return (await button.count()) ? button : null;
}

async function clickAndSave(page, button, outputPath, timeoutMs) {
  if (!button) throw new Error("未找到对应模块的导出按钮，页面可能已改版");
  const downloadPromise = page.waitForEvent("download", { timeout: timeoutMs });
  await button.click({ timeout: 10000 });
  const download = await downloadPromise;
  await download.saveAs(outputPath);
  const header = Buffer.alloc(2);
  const fd = fs.openSync(outputPath, "r");
  fs.readSync(fd, header, 0, 2, 0);
  fs.closeSync(fd);
  if (header.toString("ascii") !== "PK") {
    fs.rmSync(outputPath, { force: true });
    throw new Error("下载内容不是 xlsx，登录态可能已过期");
  }
  return { file: outputPath, suggested_filename: download.suggestedFilename(), bytes: fs.statSync(outputPath).size };
}

const args = parseArgs(process.argv);
const repoRoot = path.resolve(args.repo);
const profileDir = args.profile ? path.resolve(args.profile) : path.join(repoRoot, ".playwright/douyin-profile");
const outputDir = path.resolve(args.outDir);
fs.mkdirSync(outputDir, { recursive: true });
const detailUrl = `https://creator.douyin.com/creator-micro/work-management/work-detail/${args.itemId}?enter_from=homepage`;
const { playwright, lockModule } = await loadRepoModules(repoRoot);
const reservation = lockModule.acquireBrowserSessionLock(profileDir);
let context;
const files = [];
const errors = [];

try {
  context = await playwright.chromium.launchPersistentContext(profileDir, {
    headless: args.headless,
    viewport: { width: 1600, height: 1000 }
  });
  const page = context.pages()[0] ?? await context.newPage();
  await page.goto(detailUrl, { waitUntil: "domcontentloaded", timeout: 60000 });
  await page.waitForTimeout(9000);
  const bodyText = await page.locator("body").innerText();
  if (/扫码登录|登录抖音|登录后/.test(bodyText)) throw new Error("登录态过期，请人工重新扫码");

  const trafficTab = page.getByText("流量分析", { exact: true }).first();
  if (!(await trafficTab.count())) throw new Error("未找到流量分析标签");
  await trafficTab.click();
  await page.waitForTimeout(2500);
  for (const section of ["内容吸引力", "观众参与度", "流量来源"]) {
    try {
      const button = await sectionExportButton(page, section);
      files.push({ section, ...(await clickAndSave(page, button, path.join(outputDir, `${section}.xlsx`), args.timeout * 1000)) });
    } catch (error) {
      errors.push({ section, error: error.message });
    }
  }

  const audienceTab = page.getByText("观众分析", { exact: true }).first();
  if (await audienceTab.count()) {
    await audienceTab.click();
    await page.waitForTimeout(2500);
    try {
      // 观众分析页只有一个导出按钮；模块标题在不同版本中不总是使用 card-title-M2BOZI。
      const button = page.locator("button:visible", { hasText: "导出" }).first();
      files.push({ section: "观众分析", ...(await clickAndSave(page, button, path.join(outputDir, "观众分析.xlsx"), args.timeout * 1000)) });
    } catch (error) {
      errors.push({ section: "观众分析", error: error.message });
    }
  } else {
    errors.push({ section: "观众分析", error: "未找到观众分析标签" });
  }
} finally {
  await context?.close().catch(() => {});
  reservation.release();
}

const manifest = { item_id: args.itemId, detail_url: detailUrl, captured_at: new Date().toISOString(), files, errors };
fs.writeFileSync(path.join(outputDir, "export-manifest.json"), JSON.stringify(manifest, null, 2));
console.log(JSON.stringify(manifest, null, 2));
if (errors.length && !files.length) process.exitCode = 1;
