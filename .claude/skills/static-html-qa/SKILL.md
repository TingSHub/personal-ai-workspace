---
name: static-html-qa
description: 静态 HTML 通用前端质检（workspace 共享 internal skill）——任何方式生成的 HTML 交付前统一执行：内容边界扫描（check-content-boundary.py）、数值一致性校验（check-numbers.py）、前端质检（qa-html-report.py：多视口/逐页截图 + DOM 溢出 + SVG 文字重叠/出界 + 图例重叠 + 字体加载失败 + console error + 页面截断 + 图表字号审计，--mode auto 自动识别翻页 deck / 长滚动页）、长文全页截图（screenshot-fullpage.sh）。当 html-ppt-skill、dashi-ppt 或其他生成器产出的 HTML 需要交付前质检时使用；触发词：质检、QA、检查 HTML、溢出检查。
---

# static-html-qa

## 作用

跨生成器通用的静态 HTML 质检能力：无论 HTML 由 html-ppt-skill、dashi-ppt-skill 或其他方式生成，交付前统一跑同一套检查（内容边界、数值一致性、前端布局、多视口/逐页截图）。**质检与生成器解耦**——这是本 skill 存在的意义。

## 调用

脚本位于管理资产 `.ai/skills/static-html-qa/scripts/`（资源资产，本 SKILL.md 仅提供指令）。执行顺序（全部 PASS=0 才可交付）：

```bash
QA=.ai/skills/static-html-qa/scripts
python3 $QA/check-content-boundary.py <html> [--ignore 允许语境词...]   # 内容边界
python3 $QA/check-numbers.py <期望清单.tsv> <html>                      # 数值一致性（期望值来自裁决结果）
python3 $QA/qa-html-report.py <html> [--viewports ...] [--mode auto]    # 前端质检（形态自适应）
bash $QA/screenshot-fullpage.sh <html> [output.png]                     # （可选）长文全页截图
```

- Python playwright 依赖：自动探测工作区 `.venv`（`$QA_PYTHON` 可显式指定）；npm 全局 `@playwright/cli` 是 JS 包不能用于 Python 导入。
- `qa-html-report.py` 形态检测：存在 `.slide.is-active`/`.slide.active` 且页面不滚动 → 翻页模式（逐页检查 + 逐页截图，导航 hash → ArrowRight → JS toggle 三级 fallback）；否则长文模式（fullPage 截图）。
- 退出码契约：0=PASS / 1=有发现（人工裁决，修复后重跑）/ 2=用法错误。

## 注意事项与踩坑

- SVG 元素的 scrollWidth 无 overflow 语义，溢出检查必须跳过 SVGElement（由专门 SVG 出界/重叠检查覆盖）。
- 内容边界扫描：免责声明行（含「不构成任何投资建议」）自动豁免；允许语境（如资金流向事实）用 `--ignore` 显式声明。
- 翻页 deck 的 overview 克隆（`.mini-slide` / dashi 克隆页）不影响激活页检查。
- dashi-ppt 的渲染后 SVG 布局缺陷（如雷达图轴标签溢出）由其内置门禁（渲染前校验）漏检，必须由本 skill 兜底。
