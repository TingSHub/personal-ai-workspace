# web-ppt

> 管理资产：`.ai/skills/web-ppt/web-ppt.md`；安装实体：`.claude/skills/web-ppt/`（git clone 安装，1.5MB）

## 元数据

| 字段 | 值 |
|---|---|
| name | web-ppt |
| kind | skill |
| description | 生成 HTML 演示文稿（独立三件套 slides.html/css/js，零依赖、浏览器直开）+ 视频录制（Playwright 截图 → TTS 配音 → FFmpeg 合成）；**Audio-First 视频：TTS 旁白驱动幻灯片时长**；双 TTS 引擎（Edge TTS 本地/快速 + CosyVoice 3.0 远程 GPU/声音克隆）；内置自动化 QA（lint/validate/auto-fix）；24 款内置 woff2 字体、9 套 WCAG 主题 |
| source.type | github |
| source.url | https://github.com/includewudi/web-ppt |
| source.installed_ref | commit b37610efff98（2026-05-14） |
| runtime | both（OpenCode / Claude） |
| invocation | 按 SKILL.md 决策树：四阶段 ppt-plan（内容策划/旁白）→ ppt-design（主题/配色/字体）→ ppt-build（编码生成）→ ppt-video（视频录制，可选）；子技能各目录 SKILL.md 按需加载 |
| requirements | 视频录制需 Playwright + FFmpeg；CosyVoice 需 GPU/远程服务（可选）；Edge TTS 本地可用 |
| update.method | git |
| update.instructions | 从上游仓库获取到临时目录，对比后替换安装实体；保留本地资源说明 |
| update.verify | 校验 SKILL.md frontmatter + 四阶段子技能目录齐全 + 最小 deck 生成 |
| scripts | ppt-video/scripts/（视频录制相关，含 TTS/字幕）；根 scripts/ |
| experience_refs | — |

## 调用说明

- 触发词广：PPT/幻灯片/演示文稿/配色/字体/主题/录制/配音/TTS/字幕/旁白/声音克隆等
- 四阶段工作流：Topic → Plan（页数/旁白文案/结构）→ Design（主题/配色/字体/布局）→ Build（HTML/CSS/JS 三件套）→ Video（可选：截图→TTS→FFmpeg）
- **与本项目衔接**：Audio-First 视频（旁白驱动时长）与 investagent-html-report-v0.1 的 P5 口播→视频链路高度相关——27 页 deck 的 speaker script（notes）可作 ppt-plan 的旁白输入；Edge TTS 引擎与本地 edge-tts 资源互补
- 与 html-ppt-skill / dashi-ppt 的关系：同为 HTML PPT 生成器，按最佳可用资源原则按场景选择（web-ppt 优势：零依赖三件套 + 内置 QA + 视频一体化；html-ppt-skill 优势：36 主题 + presenter 模式 + 已沉淀质检三件套；dashi-ppt 优势：1020 版式 + PPTX 导出）

## 注意事项与踩坑

- **无 LICENSE 文件**（2026-08-16 审查确认，仓库未提供许可声明）——使用前需与上游确认授权边界，商业分发场景谨慎（参照 huashu 处理先例：方法吸收、不直接复制实体）
- 触发词与 html-ppt-skill / dashi-ppt 重叠——按任务形态选择，不重复安装同类
- 视频录制依赖 Playwright + FFmpeg（本环境已具备）；CosyVoice 声音克隆需 GPU/远程服务，未实测
- 内置 QA（lint/validate/auto-fix）与 static-html-qa 质检三件套可互补：web-ppt 自带 lint 覆盖其生成形态，static-html-qa 仍作为跨生成器统一质检兜底
- 四阶段子技能为按需加载（references/ 与子目录 SKILL.md）——首次调用需通读主 SKILL.md 决策树

## 回写条目

（无——新注册资源，2026-08-16）
