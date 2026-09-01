# dashi-ppt

> 管理资产：`.ai/skills/dashi-ppt/dashi-ppt.md`；安装实体：`.claude/skills/dashi-ppt/`（npx 安装）；项目引用：investment-research-html-mvp（README Resources Used + investagent-html-report-v0.1 SOP）

## 元数据

| 字段 | 值 |
|---|---|
| name | dashi-ppt |
| kind | skill |
| description | 工业级 HTML 翻页 PPT 生成器：12 套主题（theme10 金色指数风适合金融/投资）、1020 版式页、每页 3 模板方案 + 1 Agent 定制（v4）、浏览器内可编辑、可导出 PPTX/PDF；goal.json 驱动（schemaVersion 2） |
| source.type | github |
| source.url | https://github.com/chuspeeism/dashi-ppt-skill |
| source.installed_ref | npm v0.4.5（2026-08-16 npx 安装；仓库 SKILL.md 标注 0.4.11，以安装实体为准） |
| runtime | both |
| invocation | 按 SKILL.md：整理 goal JSON → scaffold（`npm run goal:scaffold -- --title ... --theme <themeXX> --pages <n> --roles ...`）→ 按 goal.fill-plan.json 填文案槽 → `validate:goal-spec` → `scripts/render_goal_deck.sh` 渲染 |
| requirements | Node.js 20+ 与 npm；导出 PPTX/PDF 需本机 Chrome/Chromium/Edge；首次渲染在 project/ 装依赖（官方源不可达自动锁 npmmirror） |
| update.method | package-manager |
| update.instructions | `npx dashi-ppt-skill@latest` 重跑即原地更新；国内镜像 `npx --registry=https://registry.npmmirror.com dashi-ppt-skill@latest` |
| update.verify | 生成一个最小 goal 并 scaffold + validate:goal-spec + render 通过 |
| scripts | project/ npm scripts（goal:scaffold / layout:query / inspect:layout / props:safe / validate:goal-spec / validate-swiss-deck / validate-goal-copy）；scripts/render_goal_deck.sh |
| experience_refs | — |

## 调用说明

- 触发词：PPT / 演示文稿 / 幻灯片 / 汇报材料；明确「PPTX/可编辑 PPTX」才交付 PPTX 文件（先 HTML + 本机导出服务）
- 流程：确认主题风格与媒体需求 → 写逐页 content brief → scaffold → 按 fill-plan 填充 → validate:goal-spec → render
- 金融/投资内容强相关可自选 theme10（普通自动选择不选）
- 生成后必须跑 `static-html-qa` 质检（内置门禁是渲染前校验，不覆盖渲染后 SVG 布局）

## 注意事项与踩坑

- **版式槽位约束严格**：fill-plan 的 text maxChars、数组 fixedLength（如 tiles.data 固定 24 点）、value 数值范围（0-100）由 validate:goal-spec 精确报出——填充前先 inspect:layout 确认字段，避免多轮返工（实测 12 页经 3 轮 schema 修正）。
- 数组项类型以校验器报错为准（comparison 的 points 是字符串数组、distribution rows 是 name/tag/value/delta 数值结构）。
- 无真实素材且不能生图时：media 槽留空可行，版式自动降级（按 SKILL.md 非交互规则）。
- 渲染脚本会启动本机预览服务（HTTP 5200 端口）——实验/批处理结束后需手动停止（kill PID，见 .preview-server.json）。
- 内容边界在填充阶段执行：只填裁决后数据，不得为凑槽位新增事实（实验发现：版式缺位宁可留空也不补数）。
- **渲染后布局质量需外部兜底**：实测雷达图轴标签（"分散度92"等）超出 SVG 画布——内置门禁漏检，由 qa-html-report.py 发现；生成后逐页检查是必跑项。
- **图表可能缺图例**：实测某页折线图 10 条线无图例/线标注（qa-html-report.py 多序列图表检查命中）——版式库图表不保证带图例，需人工确认或换带图例的 layout。
- 编辑器 UI（浏览器内编辑控制台的提示面板）会混入 DOM，qa 检查按内容容器（.slide/.deck/main/section）范围排除。

### 补充规则

（无——新注册资源，2026-08-16）
