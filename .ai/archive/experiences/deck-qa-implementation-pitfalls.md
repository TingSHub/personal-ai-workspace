# Experience: deck-qa-implementation-pitfalls

> Experience 是反馈，不是永久知识库：合格经验先判定归属，回写至 Workflow SOP 或 Skill/Agent 记录（by-name 回填 `experience_refs[]`），**回写完成后归档**至 `.ai/archive/experiences/`；`.ai/experiences/` 只存未完成回写的在途经验，不无限堆积。

## 来源证据

investagent-html-report Phase 4 rerun（2026-08-19，贵州茅台 600519）：qa-html-report.py 三轮修复记录（见 `presentation-execution.md` QA Status）：
- 缺 `.notes{display:none}` → p12 报 aside.notes 溢出（r:-86, b:34）
- 移动端 `.flow .arrow` transform:rotate(90deg) → 390×844 报 6 处 span.arrow 溢出（sw 16 vs cw 26，scroll 尺寸不随 transform 变化）
- 进度条 scaleX(0) → 报 #bar-fill 溢出（sw 390 vs cw 8）；改 clip-path 后 PASS
- 验证资源 installed_ref：static-html-qa internal；html-ppt-skill github · f3a8435d3901697d5ac5e64d356c933637e43107

## 触发场景

生成/修改带 reveal 动画、notes、进度条的静态 HTML deck 时；或 qa-html-report.py 对「结构上正确」的页面报出滚动尺寸溢出时。

## 问题与归属判定

- 问题：qa-html-report.py 的溢出检测基于 scrollWidth/scrollHeight 与视觉尺寸之差，transform 旋转/缩放元素不更新 scroll 尺寸，导致误报；notes 未显式隐藏时按可见元素参与翻页溢出检查。
- 归属（owner）：`.ai/skills/static-html-qa/static-html-qa.md` 注意事项 + experience_refs。

## 可复用结论（resolution）

1. deck CSS 必须显式 `.notes{display:none}`（仅 S 演讲者模式显示），缺失会被翻页溢出检查误报。
2. 容器内动画（进度条等）优先 clip-path / opacity，避免 width/transform 动画：width 触发 impeccable layout-transition，scaleX 被 qa 脚本按 scroll 尺寸虚报；clip-path 两者都不触发。标准实现 = 外层 `overflow:hidden` 固定尺寸 + 内层 `clip-path:inset(0 X% 0 0)` 过渡。
3. 移动端竖排布局的旋转元素（箭头等）改用内容替换（`::after` 字符），不用 transform 旋转。

## 回写目标

- `static-html-qa` skill 资产（`.ai/skills/static-html-qa/static-html-qa.md` 注意事项 + 回写条目）

## 适用范围

- 任何经 qa-html-report.py 检测的静态 HTML deck（翻页形态）；qa-html-report.py 当前版本

## 不适用范围

- 长文滚动页无此问题（无翻页溢出检查路径）；QA 脚本未来若改 scroll 检测语义则本条需复验

## 关联资产

- `static-html-qa` · `html-ppt-skill` · `impeccable` · investagent-html-report workflow
