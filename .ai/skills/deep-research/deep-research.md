# deep-research

> 管理资产：`.ai/skills/deep-research/deep-research.md`；安装实体：`.claude/skills/deep-research/`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | github · https://github.com/hoolulu/deep-research |
| installed_ref | v5.1.0 · commit `ef9c190fb516bafe7a08565c3d4a09045b73aa74` |
| runtime | both |
| 调用入口 | `$deep-research`；读取安装实体 `SKILL.md`，按本地/在线模式执行 |
| 要求 | Python 3；在线模式需要网络、搜索/抓取链路（Scrapling/SearXNG 可选）；离线模式可直接读取 MD/TXT/PDF/DOCX；需要当前运行时的 LLM/子任务能力 |
| 更新 | manual · 从 GitHub main 获取到临时目录后比对，再替换 `.claude/skills/deep-research/`；验证：读取 VERSION、运行最小离线资料调研并检查报告 QA |
| 辅助脚本 | —（沿用安装实体 `tools/dr_tools.py`、`tools/dr_check.py`；不复制到本地资源目录） |
| 经验引用 | — |

## 作用

多阶段深度研究流水线：分析大纲 → 采集数据 → 并行章节写作 → 引用装配与 QA。支持 quick / standard / deep，适用于行业研究、趋势前瞻、竞品扫描、政策解读和技术专题。

## 调用说明

- 在线研究：调用安装实体的 `SKILL.md` 与 `command/research.md`，先生成大纲和结构化 data pool，再装配带引用报告。
- 本地资料研究：将已下载的 PDF/TXT/MD/DOCX 目录作为输入，优先使用本地资料；需要联网补充时必须明确声明。
- 适合做外部研究补充和竞品/行业扫描，不替代本项目 `Research Intelligence` 的事实冻结、官方披露归档和质量门。
- 若输出要进入上市公司脚本，只能把报告作为候选研究材料；关键数字必须回溯到 `official-information/`、结构化数据源或独立验证后的来源。

## 输出与验证

- 原生输出：临时 `outline.json`、`data-pool.json`、章节文件、最终 Markdown 报告、引用列表、可信评估和免责声明。
- 最小验证：检查 `VERSION`；离线模式使用一份本地资料跑 quick；确认报告包含目录、来源、免责声明、数据类型和 QA 结果。
- 版本 5.1.0 的报告结构和校验规则以安装实体 `RULES.md`、`TYPES.md`、`profiles.json` 为准。

## 注意事项与踩坑

- 上游 prompt 含 OpenCode `task()`、语言检测和报告目录约定；在 Codex 中需要映射到当前原生子任务/文件工具，不直接假设 OpenCode 运行时存在。
- 在线模式依赖外部搜索与抓取服务，SearXNG/Scrapling 失败时允许降级，但必须在执行记录中标注；不要把搜索摘要当作最终证据。
- 报告默认是公开网络综合，不等于券商正式报告；每个数字、时间和口径仍需项目级复核。
- 不把它的 `reports/` 目录直接登记为项目研究资产；项目应复制或引用已验收的独立结果，并保留来源映射。
- 上游仓库包含浏览器端报告导出和本地抓取组件，安装前已完成 MIT 许可检查和常见凭据模式扫描，未发现阻断项。

## 来源

- GitHub 仓库：`hoolulu/deep-research`
- 当前版本：`VERSION = 5.1.0`
- 许可证：MIT

## 适配建议

当前不直接加入播客 Workflow 的 Required Resources。先用它针对“东山精密同行竞争格局/光模块与高速 PCB 产业链”做一次离线+联网对比试跑，验收来源质量、同行口径和数据可追溯性后，再决定是否接入 Phase 1。
