# static-html-qa

> 管理资产：`.ai/skills/static-html-qa/static-html-qa.md`；脚本：`.ai/skills/static-html-qa/scripts/`；安装实体：`.claude/skills/static-html-qa/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | internal · 2026-08-16 从 html-ppt-skill 质检脚本抽离为通用能力（dashi-ppt 等生成器复用） |
| installed_ref | internal |
| runtime | both |
| 调用入口 | 生成 HTML 后执行质检脚本三件套（见「辅助脚本」）；翻页/长文形态自动检测；SKILL.md 实体在 `.claude/skills/static-html-qa/`（可通过 Skill 工具加载） |
| 要求 | Python playwright（自动探测 .venv，`$QA_PYTHON` 可指定）；截图可选 Playwright CLI |
| 更新 | internal · 脚本改进须经真实产物验证（长文 + 翻页至少各一次 PASS） |
| 辅助脚本 | scripts/qa-html-report.py（前端质检：多视口/逐页截图 + DOM 溢出 + SVG 文字重叠/出界 + 图例重叠 + **多序列图表缺图例/线标注** + 字体失败 + console error + 页面截断 + 字号审计；`--mode auto/longform/paged` 形态自适应，auto 自动检测翻页 deck 或长滚动页；paged 模式按激活页 scope 检查，排除 overview 克隆与页面外 UI）；scripts/check-content-boundary.py（内容边界扫描，生成后必跑）；scripts/check-numbers.py（数值一致性校验，期望值 TSV 与 HTML 比对）；scripts/screenshot-fullpage.sh（长文 HTML 全页截图）；scripts/check-notes-presenter.py（翻页 deck Presenter Mode 验证：S 键弹窗 + notes 期望片段抽查，notes 锁定/改写后回归必跑） |
| 经验引用 | multi-source-conflict-check；html-ppt-longform-report；presenter-notes-verification；narration-content-lock；deck-qa-implementation-pitfalls |

## 作用

跨生成器通用的静态 HTML 质检能力：无论 HTML 由 html-ppt-skill、dashi-ppt-skill 或其他方式生成，交付前统一跑同一套检查（内容边界、数值一致性、前端布局、多视口/逐页截图）。

## 调用方式

- 生成链路（如 investagent-html-report-v0.1 P3/P4）在交付前执行：
  1. `check-content-boundary.py <html> [--ignore ...]` — 内容边界（PASS=0）
  2. `check-numbers.py <期望.tsv> <html>` — 数值一致性（PASS=0）
  3. `qa-html-report.py <html>` — 前端质检（PASS=0；翻页 deck 自动逐页检查）
  4. （可选）`screenshot-fullpage.sh <html>` — 长文全页截图
- 退出码契约：0=PASS / 1=有发现（人工裁决）/ 2=用法错误

## 注意事项与踩坑

- 形态检测：存在 `.slide.is-active`/`.slide.active` 且页面不滚动 → 翻页模式（逐页检查+截图）；否则长文模式（fullPage）。
- 翻页模式逐页导航三级 fallback：hash 深度链接 → ArrowRight → JS toggle 激活类。
- SVG 元素的 scrollWidth 无 overflow 语义，溢出检查必须跳过 SVGElement（由专门的 SVG 出界/重叠检查覆盖）。
- 内容边界扫描：免责声明行（含「不构成任何投资建议」）自动豁免；允许语境用 `--ignore` 显式声明。
- **transform 变换元素 scroll 尺寸虚报（经验: deck-qa-implementation-pitfalls）**：溢出检测基于 scrollWidth/scrollHeight，transform 旋转/缩放不更新 scroll 尺寸——`scaleX(0)` 进度条会被报「sw 390 vs cw 8」类溢出；容器内动画改 `clip-path:inset()` 过渡（不影响 scroll，也不触发 layout-transition 类规则）；移动端竖排旋转箭头改用 `::after` 内容替换。
- **notes 必须显式隐藏**：deck CSS 缺 `.notes{display:none}` 时，翻页检查会把 notes 当可见元素报溢出；S 演讲者模式由运行时单独读取，不依赖可见性。
- dashi-ppt 生成的 deck 也要跑本套检查：其内置门禁（goal-spec/swiss/copy）是渲染前校验，不覆盖渲染后 SVG 布局（实测雷达图轴标签溢出由 qa-html-report.py 兜底发现）。

## 回写条目（来源: html-ppt-longform-report）

- 从 html-ppt-skill 抽离的质检三件套 + 截图脚本（2026-08-16）；原 html-ppt-skill 记录的「辅助脚本」行保留指向说明。

## 回写条目（来源: multi-source-conflict-check）

- 数值一致性校验（check-numbers.py）是多源研究 → 统一 HTML 链路的必跑项；SVG 坐标换算/转录必然引入错误，数字可信度是研究内容底线。

## 回写条目（来源: deck-qa-implementation-pitfalls）

- 2026-08-19：贵州茅台 Phase 4 三轮修复实证 transform 旋转/缩放 scroll 虚报与 notes 显式隐藏要求（见注意事项）。
