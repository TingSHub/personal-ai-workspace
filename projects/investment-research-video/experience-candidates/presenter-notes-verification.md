# Experience: presenter-notes-verification

## 来源证据

- 项目：investment-research-html-mvp（2026-08-16，Presenter Mode 回归验证：S 键弹窗 + notes 期望片段抽查）
- 运行记录：`logs/run-20260816-workflow-v1.md`（口语化后 presenter 验证）
- 相关资源 installed_ref：html-ppt-skill（f3a8435）、static-html-qa（internal）

## 触发场景

- html-ppt-skill 形态翻页 deck 的 notes（speaker script）被修改（口语化改写/Content Lock 后）需要回归验证时
- 任何依赖 Presenter Mode 交付的 deck 交付前检查

## 问题与归属判定

- 问题：notes 是 display:none 的隐藏内容，普通 HTML QA（qa-html-report.py）不覆盖；Presenter 窗口是独立 popup，需专门验证 notes 是否真正显示且内容正确。
- 归属（owner）：static-html-qa 记录（scripts/check-notes-presenter.py 登记）；html-ppt-skill 记录（presenter 验证方法）

## 可复用结论（resolution）

- 验证方法：逐页 `#/N` 深链 → S 键打开 presenter popup → 检查期望片段在窗口文本中（Playwright `expect_popup`）。
- **check-notes-presenter.py**（static-html-qa/scripts/）：输入 deck.html + 期望清单 TSV（页号<TAB>片段），退出码 0/1/2；无清单时抽查前 3 页 notes 存在性。
- 注意：S 键验证的是**当前激活页**的 notes——先 `#/N` 翻页再按 S，避免检查到错误页面（实测 P2 内容在 P1 激活时找不到）。
- 与 qa-html-report.py 的关系：该脚本覆盖 DOM/布局，本脚本覆盖 presenter 内容层，两者互补。

## 回写目标

- static-html-qa 记录：辅助脚本行登记 check-notes-presenter.py（用途：翻页 deck Presenter Mode 内容验证）
- html-ppt-skill 记录注意事项（presenter 验证方法）

## 适用范围

- html-ppt-skill 形态 deck（.deck/.slide + runtime.js）；类似 presenter 弹窗形态的验证可借鉴

## 不适用范围

- 长文滚动页（无 presenter 模式）
- dashi-ppt 等自带编辑器的形态（其 presenter/预览机制不同，用其自带 QA）

## 关联资产

- static-html-qa（脚本归属资源）；html-ppt-skill（形态归属）；investagent-html-report-v0.1（Workflow by-name）
