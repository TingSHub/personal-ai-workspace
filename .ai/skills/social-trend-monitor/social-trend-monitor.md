# social-trend-monitor

> 管理资产：`.ai/skills/social-trend-monitor/social-trend-monitor.md`；安装实体：`.claude/skills/social-trend-monitor/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| name | social-trend-monitor |
| kind | skill |
| description | 社交趋势监控：多平台热点追踪，生成趋势日报与内容机会判断 |
| source | github · https://github.com/yangliu2060/smith--skills 子目录 social-trend-monitor/ · installed_ref 332d98c8269e6257757787db243b03f43671482d（**仓库无 LICENSE，仅内部使用不对外分发**） |
| runtime | claude（纯 prompt skill，依赖 WebSearch/WebFetch/Write 工具） |
| invocation | 用户说"查看社交趋势 / 今天什么火 / trending topics"时按 SKILL.md 六步执行；报告存 `~/.claude/cache/social-trends/trends-YYYY-MM-DD.md` |
| requirements | WebSearch / WebFetch / Write 可用；无第三方依赖 |
| update | manual · 重新拉取上游固定 commit 的 social-trend-monitor/ 子目录，对比后替换安装实体；verify：SKILL.md frontmatter 完整 + 六步流程结构未变 |
| scripts | 无 |
| experience_refs | 无 |

## 调用说明

### 用途

每日/按需生成跨平台趋势日报：Reddit / Instagram / TikTok 各 Top 10（标题/热度/链接），跨平台共同趋势与内容机会洞察。趋势报告可作 publish-review 选题反哺的输入之一。

### 适配与限制（本 workspace 实测结论）

- **监控的是海外平台**（Reddit/Instagram/TikTok），不含抖音/国内平台；国内热点扫描用 `news-search` / `multi-search` 补位，海外风向用本 skill
- 纯 prompt + 公开搜索实现，实时性受搜索引擎索引限制；无 API，数据为搜索快照非全量
- 对 A 股投研选题的价值路径：海外 AI/半导体/科技风向 → 国产算力等映射选题的"海外催化"证据
- 报告目录 `~/.claude/cache/social-trends/` 在 workspace 之外，跨期对比时需把当期报告归档到复盘项目的 docs/ 下
