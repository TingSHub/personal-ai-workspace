# hyperframes

> 管理资产：`.ai/skills/hyperframes/hyperframes.md`；安装实体：`.claude/skills/hyperframes/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | github · https://github.com/heygen-com/hyperframes |
| installed_ref | c32b804 |
| runtime | both |
| 调用入口 | npx hyperframes <init|add|catalog|lint|check|preview|snapshot|render|publish|upgrade>；官方 Agent Skills 套件（9 个，随主技能安装，按主技能 SKILL.md 入口指令随用随载）：hyperframes 入口 + hyperframes-core / -creative / -animation / -audio / -cli / -keyframes / -registry + media-use |
| 要求 | Node 22+（官方要求，本机 v25.9）；google-chrome 系统浏览器；FFmpeg；network（首次 npx 拉取与 Google Fonts 分片本地化） |
| 更新 | git · 拉取上游新版本到临时目录审查（README、skills、CLI 变更、LICENSE）后更新 vendor 安装；保留本资源说明；验证：npx hyperframes check 通过 + 一条 10 秒含中文与音频的样片渲染 |
| 辅助脚本 | — |
| 经验引用 | `generic-video-visual-direction` |

## 作用

HTML/CSS + 可 seek 动画 → headless Chrome 逐帧 → MP4 的 Web 视频引擎。与"随旁白播放的财经网页"形态同构；本实验 84.17s 中文财经视频渲染耗时 1m36s（2525 帧 high quality）。

## 调用

- **主技能入口（必须先读）**：`.claude/skills/hyperframes/SKILL.md` 是任何 HyperFrames 任务的第一入口——按「项目状态 → 意图层 → 创作路由」状态机执行：已有项目直接操作（inspect/diagnose/validate/preview/render）；全新创作先意图捕获（angle/length/destination）建立 BRIEF.md，再按路由表选创作 workflow（默认 /faceless-explainer）
- 领域子技能按入口指令加载：hyperframes-core（composition 契约/data-* 时序/tracks/sub-compositions）、hyperframes-creative（设计 spec/beats/色板）、hyperframes-animation（seek-safe 动画/七种 adapter）、hyperframes-keyframes（seek-safe 关键帧诊断）、hyperframes-audio（混音/自动化包络）、hyperframes-cli（开发循环 lint/check/preview/render）、hyperframes-registry（catalog/add 复用 blocks）、media-use（voiceover TTS/BGM/SFX/字幕/素材 resolve）
- 官方工作流（faceless-explainer）：init（scaffold + pin CLI 版本）→ BRIEF.md → frame preset → STORYBOARD/SCRIPT → composition → media（media-use 配音/素材）→ lint/check → preview → render
- 常用：`npx hyperframes check`（质量门，报错带元素 id+时间戳+修复建议）、`npx hyperframes snapshot --at <s>`（秒级出图）、`npx hyperframes render --quality high`、`npx hyperframes catalog --query <效果>`（先查库再手写动画）
- 本实验验证的参考实现：`projects/investment-research-system/experiments/listed-company-video-production/outputs/web/hyperframes/`（v1/v2 全源文件）

## 调用注意事项

- 推荐输入：已冻结的脚本 + 每幕一个核心观点的 Scene 划分 + 已生成的旁白音频（Audio First，见经验文档）
- **CLI 未预装**：本机无全局 hyperframes；首次 `npx hyperframes init` 拉取慢（实测 auth 8m10s），init 时项目自动 pin CLI 版本（当前 npm 最新 0.8.4），后续按 pin 渲染保持可复现；恢复旧项目先 `npx hyperframes@latest upgrade --project . --check` 探测
- 系统需有 google-chrome；Google Fonts CJK 分片由 render 期自动本地化嵌入，离线可渲染
- 单条已有旁白不在官方 per-frame TTS 模型内：手工插入 `<audio class="clip" data-start="0" data-duration="84.144">` 到 index.html（可复用 `outputs/web/hyperframes/v1-first-shot/scripts/insert-audio.mjs`）
- 配音走 media-use（HeyGen free-usage 路径 + 本地 Kokoro 备选）；HeyGen key 缺失时官方 TTS/BGM 能力不可用，如实降级并记录

## 常见失败原因

- **lint 92 条警告**：frame_id 直接用作元素 id（`05-outlook-*` 选择器在 querySelector 抛 SyntaxError）——id 必须以字母开头（`f05-outlook-*`）；批量重命名时注意不要误伤 `data-composition-id` / `__timelines` key
- **check content_overlap**：大字号（220-240px）ascent 上探压标签，数字与标签间距需 ≥56px（16-18px 必叠）；"但"字类 pivot 文字与相邻元素需显式定位
- **assemble 轨道冲突**：同一 track 多个 clip 重叠（05-outlook 三个 clip 占同 track）——clip 必须分 track
- 对比度：cartesian 预设的 taupe 色 #8A8178 在小字上 3.14:1 不达 WCAG 4.5:1（check 警告），加深至 #6E675C
- 首次 `npx hyperframes` 拉取慢（实测 auth 8m10s），耐心等待或预拉取

## 最佳实践

- **Audio First**：先定稿脚本 → 生成 TTS → 按音频实际时长分配 Scene 时长 → 再写画面。先设计画面再配音必然音画不同步
- 动画全部用"数据动作"（条生长、线描画、数字逐位滚动、对比翻转），转场用硬切（数据新闻标准），禁止淡入淡出
- 每幕一个核心观点，同屏数字峰值 ≤3；大数字 220-240px + 标签层级
- 图表用手写 SVG + GSAP（官方 nyt-graph demo 同款），精确比例（如成本 39.05% vs 收入 34.61% 平行条），不用 ECharts
- 迭代循环用 check/snapshot：报错自带修复建议，15 分钟可完成一轮"去装饰+加网格线"级修改
