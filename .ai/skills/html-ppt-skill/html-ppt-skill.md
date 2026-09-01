# html-ppt-skill

> 管理资产：`.ai/skills/html-ppt-skill/html-ppt-skill.md`；安装实体：`.claude/skills/html-ppt-skill/`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | github · https://github.com/lewislulu/html-ppt-skill |
| installed_ref | f3a8435d3901697d5ac5e64d356c933637e43107 |
| runtime | both |
| 调用入口 | 按 SKILL.md 指令：选主题/模板/布局 → 生成单文件静态 HTML 演示（键盘导航）；演讲者模式用 presenter-mode-reveal 模板写逐字稿 |
| 要求 | 纯静态 HTML/CSS/JS，无构建；Headless Chrome 渲染 PNG（render.sh，需 chrome）；仅 CDN webfonts |
| 更新 | git · 从上游仓库更新安装实体（保留本地说明）；验证：用模板生成一个最小 deck 并键盘导航/渲染验证 |
| 辅助脚本 | scripts/new-deck.sh（脚手架）；scripts/render.sh（Headless Chrome 渲染 PNG）；**质检脚本已抽离至 `static-html-qa`（by-name 引用，2026-08-16）**——长文/翻页形态生成后均跑该套检查（check-content-boundary / check-numbers / qa-html-report / screenshot-fullpage）；验证输出（verify-output/）可经 render.sh 重现，不入库 |
| 经验引用 | html-ppt-longform-report；multi-source-conflict-check；narration-content-lock；presenter-notes-verification |

## 作用

HTML PPT Studio：36 主题 / 15 全 deck 模板（含 presenter-mode-reveal 演讲者模式+逐字稿）/ 31 布局 / 27 CSS 动画 / 20 canvas FX 特效 / 键盘运行时（T 换主题、S 演讲者模式、N 备注）。生成专业静态 HTML 演示（PPT/幻灯片/小红书图文/技术分享/pitch deck），单文件可用。

## 实体位置

- 安装实体：`.claude/skills/html-ppt-skill/SKILL.md`（frontmatter + 完整指令）；资产在 assets/（base.css 设计系统、themes、animations）+ templates/（full-decks、single-page）+ scripts/

## 调用方式

- 触发词：presentation / ppt / slides / deck / 幻灯片 / 演讲稿 / 小红书图文 / 分享稿 / pitch deck 等
- 流程：选 full-deck 模板（或 single-page 布局）→ 按主题 token 填充内容 → 键盘运行时自检 → render.sh 出 PNG（如需）
- 与本项目衔接：可作为 Information Visualization Architect 视觉方案的**图文/分享稿执行层**（visual-plan 的图文形态落地）；presenter-mode-reveal 的逐字稿可与 finance-content-engineering 口播稿衔接

## 注意事项与踩坑

- 演讲者模式（演讲/逐字稿/提词器场景）必须用 `presenter-mode-reveal` 模板，每页 `<aside class="notes">` 写 150-300 字逐字稿。
- 36 主题为 token 设计系统（base.css），换主题不改内容结构；同一 deck 禁混用主题。
- render.sh 需 Headless Chrome；离线环境仅 CDN 字体不可用时回退系统字体。
- MIT 许可（© 2026 lewis）；安装实体约 15.6M（docs 含 hero.gif，验证输出不入库）。

### 补充规则

- **长文阅读型交付物（研究报告页/公司分析/投资者阅读页）只取设计层**：复用 base.css token 体系与主题（editorial-serif 类），**不用**翻页 runtime（runtime.js slide/键盘逻辑）与 data-anim 入场动画；滚动阅读页用 `scroll-behavior:smooth` + 锚点导航即可。
- **A 股财务页面红涨绿跌是设计红线**（`--up: 红 / --down: 绿`，负数标注用绿）；skill 默认蓝涨绿跌为美股惯例，必须显式覆盖，否则直接误导读者。
- 自包含约束：单文件、系统字体栈（无 CDN）、内联 SVG——本地可打开、可邮件、可归档。
- 质检三件套（见「辅助脚本」行）：check-content-boundary.py（内容边界）、check-numbers.py（数值一致性，SVG 坐标换算后必跑）、screenshot-fullpage.sh（全页截图，render.sh 是翻页导向不适用长文页）。

### 补充规则

- 多源研究统一 HTML 呈现前，期望数值清单（裁决后）必须经 `scripts/check-numbers.py` 校验——手工 SVG 坐标换算/转录必然引入错误，数字可信度是研究内容底线。
- 内容边界扫描（`scripts/check-content-boundary.py`）支持 `--ignore` 声明允许语境（资金流向事实等），免责声明行自动豁免。

> 用户边界修正补充（2026-08-16，见 investagent-html-report-v0.1 v0.1.1）：①HTML **不出现任何具体目标价**（机构或自研）——估值仅呈现 PE/PB/股息率/历史分位/不同增长假设下的 DCF 区间，「机构目标价均值区间」类表述删除，避免向荐股靠近；②不展示内部置信度/证据编号/证据台账/「结论状态」类内部研究表述；③措辞避免「唯一/无懈可击/绝对/最优质」等绝对化、营销化表达；④「企稳确认/压力信号」类基本面验证信号允许保留（帮用户理解如何验证研究判断），不得写成「出现信号即买卖」。


### 补充规则

- **每页 `<aside class="notes">` 是该页最终口播文本的唯一 Source of Truth**（Content Lock）：口语化/数字读法/停顿优化直接更新 notes；TTS 仅技术性处理；字幕由 notes 派生不另写文案；Speaker Script 与 Slide Visual 语义一致（修改核心观点需同步 Slide，纯表达层无需）。

### 补充规则

- Presenter Mode 回归验证：逐页 `#/N` → S 键打开 presenter popup → 检查期望片段；用 `static-html-qa/scripts/check-notes-presenter.py`；注意先翻页再按 S（验证的是当前激活页的 notes）。
