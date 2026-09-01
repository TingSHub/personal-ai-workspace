#!/usr/bin/env node
// 指标导出辅助脚本：登录态内导出创作者中心作品列表 Excel（含完播率/5s完播率/2s跳出率/封面点击率/平均播放时长）。
// 方法来源：TzFilm-Douyin-Tool SKILL.md（旧 URL 仍服务 Garfish 导出页）+ xhs_douyin_content 选择器。
// 约束：只操作登录态对应的本人账号；不绕登录/验证码/风控；失败即停。

import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { pathToFileURL, fileURLToPath } from "node:url";
import { createRequire } from "node:module";

const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const DEFAULT_REPO = path.resolve(SCRIPT_DIR, "../../../../.claude/skills/douyin-creator-tools");
const DATA_CENTER_URL = "https://creator.douyin.com/creator-micro/data-center/content";

function parseArgs(argv) {
  const args = { out: "", repo: DEFAULT_REPO, profile: "", headless: false, timeout: 60 };
  for (let i = 2; i < argv.length; i += 1) {
    const key = argv[i];
    if (key === "--out") { args.out = argv[++i]; continue; }
    if (key === "--repo") { args.repo = argv[++i]; continue; }
    if (key === "--profile") { args.profile = argv[++i]; continue; }
    if (key === "--headless") { args.headless = true; continue; }
    if (key === "--timeout") { args.timeout = Number(argv[++i]); continue; }
    console.error(`未知参数: ${key}`);
    process.exit(2);
  }
  return args;
}

function fail(message, code) {
  console.error(JSON.stringify({ success: false, error: message }));
  process.exit(code);
}

async function loadRepoModules(repoRoot) {
  const require = createRequire(path.join(repoRoot, "package.json"));
  const playwright = require("playwright");
  const lockUrl = pathToFileURL(path.join(repoRoot, "src/lib/browser-session-lock.mjs"));
  const lockModule = await import(lockUrl);
  return { playwright, lockModule };
}

async function main() {
  const args = parseArgs(process.argv);
  if (!args.out) fail("缺少 --out 路径", 2);
  const repoRoot = path.resolve(args.repo);
  if (!fs.existsSync(path.join(repoRoot, "package.json"))) {
    fail(`仓库不存在: ${repoRoot}`, 2);
  }
  const profileDir = args.profile
    ? path.resolve(args.profile)
    : path.join(repoRoot, ".playwright/douyin-profile");

  const { playwright, lockModule } = await loadRepoModules(repoRoot);
  const reservation = lockModule.acquireBrowserSessionLock(profileDir);
  let context;
  try {
    const { chromium } = playwright;
    context = await chromium.launchPersistentContext(profileDir, {
      headless: args.headless,
      viewport: null
    });
    const page = context.pages()[0] ?? (await context.newPage());
    await page.bringToFront().catch(() => {});

    await page.goto(DATA_CENTER_URL, { waitUntil: "domcontentloaded", timeout: 60000 });
    await page.waitForTimeout(3000);

    // 登录检测：跳转登录页或出现扫码提示
    const currentUrl = page.url();
    const bodyText = await page.evaluate(() => document.body?.innerText?.slice(0, 2000) ?? "");
    if (/\/login/.test(currentUrl) || /扫码|二维码|登录抖音/.test(bodyText)) {
      fail("登录态过期：请先执行 npm run auth 重新扫码登录", 2);
    }

    // 投稿列表视图切换（2026-05-22 改版后：默认投稿分析视图，radio 类名已变化，用文本定位）
    const tabRadio = page.getByText("投稿列表", { exact: true }).first();
    try {
      await tabRadio.waitFor({ state: "visible", timeout: 20000 });
    } catch {
      fail("未找到「投稿列表」控件：页面结构可能已改版（TzFilm Pitfall #4），需人工核查页面结构", 3);
    }

    await tabRadio.click();
    await page.waitForTimeout(2000);

    // 刷新数据（可选，失败不阻断）
    const refreshBtn = page.locator("button", { hasText: "刷新数据" }).first();
    await refreshBtn.click({ timeout: 5000 }).catch(() => {});
    await page.waitForTimeout(3000);

    // 导出数据 + 下载等待
    const exportBtn = page.locator("button", { hasText: "导出数据" }).first();
    const downloadPromise = page.waitForEvent("download", { timeout: args.timeout * 1000 });
    await exportBtn.click({ timeout: 10000 });
    const download = await downloadPromise;
    fs.mkdirSync(path.dirname(path.resolve(args.out)), { recursive: true });
    await download.saveAs(args.out);

    // PK 头校验：登录态过期时抖音返回 JSON 错误体（TzFilm Mode A）
    const fd = fs.openSync(args.out, "r");
    const header = Buffer.alloc(2);
    fs.readSync(fd, header, 0, 2, 0);
    fs.closeSync(fd);
    if (header.toString("ascii") !== "PK") {
      fs.rmSync(args.out, { force: true });
      fail("下载内容非 xlsx：登录态过期（返回 JSON 错误体），请执行 npm run auth 重新扫码", 2);
    }

    const result = { success: true, output: path.resolve(args.out), captured_at: new Date().toISOString() };
    console.log(JSON.stringify(result));
  } catch (error) {
    fail(`导出失败: ${error.message}`, 1);
  } finally {
    await context?.close().catch(() => {});
    reservation.release();
  }
}

main();
