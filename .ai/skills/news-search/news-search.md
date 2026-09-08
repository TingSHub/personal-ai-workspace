# news-search

> 管理资产：`.ai/skills/news-search/news-search.md`；安装实体：`.claude/skills/news-search/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | skillhub · https://api.skillhub.cn/api/v1/download?slug=news-search |
| installed_ref | tree-sha256:569fe046726c |
| runtime | claude |
| 调用入口 | `$news-search`；Iwencai API 推荐入口 `.ai/skills/news-search/scripts/iwencai_news_search.py` |
| 要求 | network；workspace 根 `.env` 中的 `IWENCAI_BASE_URL` / `IWENCAI_API_KEY` |
| 更新 | reinstall · 从原 SkillHub 下载地址获取到临时目录，对比后替换安装实体；验证：使用一个近期事件查询并打开至少一个结果来源 |
| 辅助脚本 | `scripts/iwencai_news_search.py` |
| 经验引用 | financial-report-workflow |

新闻查询技能：查询各大搜索网站的新闻结果（百度新闻、今日头条、Bing 新闻、Google 新闻、新浪新闻），支持多源聚合与去重。

- 来源：Iwencai SkillHub 商店（外部安装，2026-08-10）
- 安装位置：`.claude/skills/news-search/`（含 scripts/news-search.js，Playwright 无头浏览器）
- workspace API 适配器：`.ai/skills/news-search/scripts/iwencai_news_search.py`，调用 `POST {IWENCAI_BASE_URL}/v1/comprehensive/search`，读取根 `.env`，不输出或保存密钥
- 依赖：`node >= 18`、playwright、playwright-extra、puppeteer-extra-plugin-stealth；调用前检查当前环境
- Codex 入口：`.codex/skills/news-search`（由 `.codex/skills` 目录级映射自动提供）
- 用途：新闻检索、舆情/资讯聚合分析
- 踩坑：公司名检索可能返回导航页或混入同名主体；引用前必须打开结果并核验主体

### Iwencai API 调用

```bash
python3 .ai/skills/news-search/scripts/iwencai_news_search.py "人工智能" --max 10 --format json
```

该入口返回标题、URL、摘要、原始来源、发布日期和可追踪类型；搜索结果只用于发现，最终事实仍需打开原文核验。它是 `multi-search` 失败后的第二级降级资源：路由优先尝试 `multi-search`，失败后先用当前会话原生 Web 搜索，原生 Web 也不可用时再调用本入口。
