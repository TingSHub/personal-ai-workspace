# multi-search

> 管理资产：`.ai/skills/multi-search/multi-search.md`；安装实体：`.claude/skills/multi-search/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | github · https://github.com/Nex-ZMH/Agent-websearch-skill |
| installed_ref | tree-sha256:6535cb0b3ab7 |
| runtime | claude |
| 调用入口 | `$multi-search`；workspace 推荐入口 `.ai/skills/multi-search/scripts/run_multi_search.py`（默认 Tavily-first） |
| 要求 | network；从 workspace 根 `.env` 注入 `TAVILY_API_KEY` / `BING_API_KEY`，不记录密钥值 |
| 更新 | git · 从上游仓库获取到临时目录，对比后替换安装实体；验证：对同一查询返回至少一个可打开来源并标明实际使用引擎 |
| 辅助脚本 | — |
| 经验引用 | financial-report-workflow；multi-search-total-failover；company-intelligence-news-product-facts；podcast-composition-input-contract |

智能多引擎搜索：自动检测网络环境并按优先级切换引擎（DuckDuckGo → Tavily → Bing API → Bing 爬虫），支持自动配额管理与网络缓存。

- 来源：GitHub（Nex-ZMH/Agent-websearch-skill，外部安装，2026-08-10）
- 安装位置：`.claude/skills/multi-search/`（multi_search.py，Python）
- 依赖：`requests` / `tavily` / `duckduckgo_search`；调用前按 `skill.yaml` 检查当前环境
- License：**GPL-3.0**（copyleft——个人使用无碍，注意勿闭源再分发）
- Codex 入口：`.codex/skills/multi-search`（由 `.codex/skills` 目录级映射自动提供）
- API Key：优先从 workspace 根 `.env` 注入进程环境，再由安装实体读取 `TAVILY_API_KEY` / `BING_API_KEY`；不在资源文档中保存值
- 用途：网络搜索、多引擎自动切换、舆情/资讯检索（web-search capability）
- 踩坑：真实项目中 DuckDuckGo/Bing 路径可能受网络影响；质量检索优先验证 Tavily 结果并实际打开来源
- 踩坑：行情/数据类网页多为 JS 渲染，摘要抓取常失败——记为失败尝试并回退聚合源，不得把搜索摘要伪装为已打开原始来源

### 补充规则

- 本地适配器的网络检测会**误报 Tavily 不可用**（标记 ❌ 并最终回退 Bing 爬虫失败），而同一 `TAVILY_API_KEY` 直连 `api.tavily.com` 返回 200。判定适配器失败前，先用 `.env` 的 key 直连验证一次，不要据此判定“无网络搜索能力”。
- 三引擎可能同时全挂（DuckDuckGo/Tavily 检测不可用 + Bing 爬虫缺 beautifulsoup4 依赖）：修复超过约 5 分钟即降级 WebSearch/WebFetch 直连，实测直连检索质量未受损、证据台账 opened 比例不受影响。
- 本地调用必须通过 `.ai/skills/multi-search/scripts/run_multi_search.py` 或等价方式先加载 workspace 根 `.env`；直接 `import multi_search` 不会自动读取 `.env`。
- 默认使用质量优先模式，让 Tavily 先于 DuckDuckGo/Bing；需要平衡模式时显式传 `--balanced`。
- 若 `multi-search`（含 Tavily-first 路由）真实失败，立即降级到当前会话的原生 Web 搜索能力；不得把 `multi-search` 的失败写成“没有网络搜索能力”。
- 若原生 Web 搜索也暂时不可用，中文财经新闻再降级到 `news-search` 的 Iwencai API 入口；使用 `.env` 中的 `IWENCAI_BASE_URL` / `IWENCAI_API_KEY`，并保留响应中的来源、日期和 URL。

### 补充规则

- 公司新闻与产品事实发现使用 `prefer_quality=True` 优先 Tavily；搜索摘要仅用于发现候选，最终事实必须打开原文并记录事件日期、发布日期、来源级别和定位信息。
- 新闻、奖项、型号和项目事实应与公司主线绑定后再交给脚本，不把搜索结果直接作为口播事实。
