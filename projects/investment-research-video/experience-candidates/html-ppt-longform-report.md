# Experience: html-ppt-longform-report

## 来源证据

- 项目：investment-research-html-mvp（2026-08-16，贵州茅台 600519，两轮 HTML 生成）
- 运行记录：`logs/run-20260816-workflow-v1.md`；产物 `outputs/companies/贵州茅台/2026-08-16/investment-report.html`（61KB 单文件、9 张内联 SVG 图表、10,513px 全页截图）
- 相关资源 installed_ref：html-ppt-skill（f3a8435d3901697d5ac5e64d356c933637e43107）

## 触发场景

- 用 html-ppt-skill 生成「长文阅读型」交付物（企业研究报告页、文章页、投资者阅读页），而非翻页 PPT 时
- 任何 A 股财务数据可视化页面（涨跌色语义）

## 问题与归属判定

- 问题：html-ppt-skill 是翻页导向（deck/slide runtime、键盘导航、presenter），直接套用会产生「PPT 化」的阅读页面；且默认设计 token 中涨跌色为蓝/绿（美股惯例），直接用于 A 股财务页面会误导读者（A 股红涨绿跌）。另：手工 SVG 图表坐标换算易错、无自动校验；全页截图无开箱脚本。
- 归属（owner）：html-ppt-skill 记录（注意事项/辅助脚本）

## 可复用结论（resolution）

- **长文报告只取设计层**：复用 base.css 的 token 体系（色板/衬线排版/卡片/阴影）与主题文件（editorial-serif 类），**不要**翻页 runtime（runtime.js 的 slide/键盘逻辑）、不要 data-anim 入场动画——单文件滚动阅读页，`scroll-behavior:smooth` + 锚点导航足够。
- **A 股财务页面红涨绿跌是设计红线**：`--up: 红 / --down: 绿`，负数标注用绿；AI 默认蓝涨绿跌（美股惯例）必须显式覆盖。
- **自包含约束**：单文件、系统字体栈（无 CDN）、内联 SVG——本地可打开、可邮件、可归档。
- **质检三件套**（辅助脚本，均已沉淀到 html-ppt-skill scripts/）：
  - `check-content-boundary.py`——扫描内容边界禁用词（买卖建议/回测/操作区间等），支持允许上下文白名单
  - `check-numbers.py`——期望数值清单（TSV）与 HTML 逐一比对，支持取整容差——SVG 坐标换算后必跑
  - `screenshot-fullpage.sh`——Playwright CLI 全页截图（render.sh 是翻页导向，不适用长文页）

## 回写目标

- html-ppt-skill 记录（`.ai/skills/html-ppt-skill/html-ppt-skill.md`）注意事项分区，回写条目标记 `## 回写条目（来源: html-ppt-longform-report）`
- 「辅助脚本」行登记三个新脚本（用途 + 使用时机）
- 「经验引用」行回填

## 适用范围

- 长文阅读型 HTML 交付物（研究报告/公司分析/投资者阅读页）
- html-ppt-skill installed_ref f3a8435d3901697d5ac5e64d356c933637e43107 及后续版本（设计 token 体系未大改时）

## 不适用范围

- 真正的翻页 PPT/deck 场景（应使用 skill 完整模板与 runtime）
- 非金融类页面（红涨绿跌规则不适用）
- 需要浏览器交互/数据刷新/JS 框架的页面（本经验要求纯静态自包含）

## 关联资产

- investagent-html-report-v0.1（Workflow by-name）
- html-ppt-skill（脚本归属资源）
