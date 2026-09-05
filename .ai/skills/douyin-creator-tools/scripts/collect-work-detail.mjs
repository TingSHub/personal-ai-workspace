#!/usr/bin/env node

import fs from "node:fs";
import path from "node:path";
import process from "node:process";
import { chromium } from "../../../../.claude/skills/douyin-creator-tools/node_modules/playwright/index.mjs";

const PROFILE = "/home/henry/personal-ai-workspace/.claude/skills/douyin-creator-tools/.playwright/douyin-profile";

function arg(name, fallback = "") {
  const i = process.argv.indexOf(name);
  return i >= 0 ? process.argv[i + 1] ?? fallback : fallback;
}

function cleanUrl(raw) {
  const url = new URL(raw);
  const safe = ["ids", "fields", "aid", "item_id", "id", "user_id", "trend_type", "time_unit", "metrics_group", "metrics", "selected_metric_count"];
  const query = safe.filter((key) => url.searchParams.has(key))
    .map((key) => `${key}=${encodeURIComponent(url.searchParams.get(key))}`).join("&");
  return `${url.origin}${url.pathname}${query ? `?${query}` : ""}`;
}

function pick(obj, keys) {
  const out = {};
  for (const key of keys) if (obj?.[key] !== undefined) out[key] = obj[key];
  return out;
}

function normalizeMetrics(metrics = {}) {
  const ratioKeys = new Set(Object.keys(metrics).filter((key) => /rate|ratio|proportion/.test(key)));
  return Object.fromEntries(Object.entries(metrics).map(([key, value]) => {
    if (ratioKeys.has(key) && value !== null && value !== "") return [key, Number(value) * 100];
    if (/^-?\d+(\.\d+)?$/.test(String(value))) return [key, Number(value)];
    return [key, value];
  }));
}

const itemId = arg("--item-id");
const output = path.resolve(arg("--output", `detail-snapshot-${itemId}.json`));
const screenshot = path.resolve(arg("--screenshot", output.replace(/\.json$/i, ".png")));
if (!/^\d+$/.test(itemId)) throw new Error("--item-id must be a numeric Douyin item id");

const detailUrl = `https://creator.douyin.com/creator-micro/work-management/work-detail/${itemId}?enter_from=homepage`;
const browser = await chromium.launchPersistentContext(PROFILE, {
  headless: true,
  viewport: { width: 1600, height: 1000 }
});
const page = browser.pages()[0] ?? await browser.newPage();
const responses = new Map();

page.on("response", async (response) => {
  const url = response.url();
  if (!/creator\.douyin\.com\/(?:web\/api\/creator|janus\/douyin\/creator)/.test(url)) return;
  if (!/item|chapter|keyword|progress|bullet|portrait|traffic|source/.test(url)) return;
  try {
    const body = await response.json();
    responses.set(cleanUrl(url), { status: response.status(), body });
  } catch {
    // Some platform responses are redirects or non-JSON assets; omit them.
  }
});

try {
  await page.goto(detailUrl, { waitUntil: "domcontentloaded", timeout: 60000 });
  await page.waitForTimeout(10000);
  const text = await page.locator("body").innerText();
  if (text.includes("扫码登录")) throw new Error("Douyin login expired; manual QR login required");

  for (const tab of ["流量分析", "观众分析", "评论热词"]) {
    const locator = page.getByText(tab, { exact: true }).first();
    if (await locator.count()) {
      await locator.click().catch(() => {});
      await page.waitForTimeout(2500);
    }
  }
  await page.screenshot({ path: screenshot, fullPage: true });

  const payloads = Object.fromEntries(responses);
  const item = Object.values(payloads).find((x) => x.body?.items?.[0])?.body?.items?.[0] ?? {};
  const summarize = Object.values(payloads).find((x) => x.body?.item_list?.[0])?.body?.item_list?.[0] ?? {};
  const trends = Object.entries(payloads)
    .filter(([url, value]) => url.includes("metrics_trend") && value.body?.trend_map)
    .map(([url, value]) => ({ endpoint: url, trend_map: value.body.trend_map }));
  const chapters = Object.entries(payloads)
    .filter(([url]) => url.includes("/data/item/chapter"))
    .map(([url, value]) => ({ endpoint: url, data: value.body }));
  const keywords = Object.entries(payloads)
    .filter(([url]) => url.includes("/search/keyword"))
    .map(([url, value]) => ({ endpoint: url, data: value.body }));

  const result = {
    item_id: itemId,
    detail_url: detailUrl,
    captured_at: new Date().toISOString(),
    title: item.desc ?? summarize.desc ?? null,
    duration_seconds: item.video?.duration ? Number(item.video.duration) / 1000 : null,
    metrics: normalizeMetrics(item.metrics ?? {}),
    summary: pick(summarize, ["aweme_id", "desc", "duration", "create_time", "chapter_list", "chapter_abstract"]),
    trends,
    chapters,
    search_keywords: keywords,
    source_endpoints: [...responses.keys()]
  };
  fs.mkdirSync(path.dirname(output), { recursive: true });
  fs.writeFileSync(output, JSON.stringify(result, null, 2));
  console.log(JSON.stringify({ success: true, output, screenshot, source_count: responses.size }, null, 2));
} finally {
  await browser.close();
}
