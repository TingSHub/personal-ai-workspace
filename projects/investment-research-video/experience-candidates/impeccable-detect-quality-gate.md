# Experience: impeccable-detect-quality-gate

> Experience 是反馈，不是永久知识库：合格经验先判定归属，回写至 Workflow SOP 或 Skill/Agent 记录（by-name 回填 `experience_refs[]`），**回写完成后归档**至 `.ai/archive/experiences/`；`.ai/experiences/` 只存未完成回写的在途经验，不无限堆积。

## 来源证据

investagent-html-report Phase 3+4 rerun（2026-08-19，贵州茅台 600519）：
- `npx impeccable detect investment-report.html` 首次实跑：32 项 anti-patterns（low-contrast 12 / tiny-text 12 / side-tab 6 / layout-transition 1 / flat-type-hierarchy 1）
- 修复 31 项后剩余 1 项 flat-type-hierarchy（人工裁决接受），见 `presentation-execution.md` QA Status
- 验证资源 installed_ref：impeccable v4.1.1（npm 3.6.0）· commit f88b2837a7d7c3182e46307bbbb091a1ed547571

## 触发场景

任何静态 HTML deck/长文报告在 static-html-qa PASS 之后、交付之前，需要额外的视觉质量层检查（a11y 对比度、字号、过渡动画、AI-tell 模式）。

## 问题与归属判定

- 问题：static-html-qa 覆盖溢出/SVG/数值/内容边界，但不查 WCAG 对比度、字号下限与动画实现；impeccable `detect` 确定性规则（无 LLM）恰好覆盖这些维度，且阈值更严格（body 文本 4.5:1、字号 ≥12px）。
- 归属（owner）：`.ai/skills/impeccable/impeccable.md` 注意事项 + experience_refs。

## 可复用结论（resolution）

1. HTML 交付前把 `npx impeccable detect <html>` 作为 static-html-qa 之后的补充门禁：两个工具维度互补，不可互相替代。
2. 预防阈值：meta/来源字号起点 12px（11px 必报 tiny-text）；弱化文本（来源行/页码）对比度 ≥4.6:1（#646a74 on #f4f4f2 实测 4.6:1，接近 4.5:1 阈值需再加深）；进度条等容器内动画用 clip-path（见 `deck-qa-implementation-pitfalls`）。
3. 阈值超严格项（flat-type-hierarchy 等）按「发现项人工裁决，不阻塞 PASS」处理，裁决理由写入执行记录。

## 回写目标

- `impeccable` skill 资产（`.ai/skills/impeccable/impeccable.md` 注意事项 + 回写条目）

## 适用范围

- 静态 HTML deck/长文报告交付前的视觉质量补充检查（investagent-html-report Phase 4 及同类流程）；impeccable v4.1.1

## 不适用范围

- 不替代 static-html-qa（溢出/SVG/数值/内容边界维度）；无浏览器/Node 环境时跳过（非阻塞门禁）；marketing/装饰性场景的激进建议（bolder/overdrive）不适用于金融内容

## 关联资产

- `impeccable` · `static-html-qa` · investagent-html-report workflow
