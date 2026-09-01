# Experience: audio-first-video-render

## 来源证据

- 项目：investment-research-html-mvp（2026-08-16，27 页 deck → final.mp4，829.44s 与音频完全对齐）
- 运行记录：`logs/run-20260816-workflow-v1.md`；产物 `outputs/experiments/video/index/render/final.mp4`
- 相关资源 installed_ref：web-ppt（commit b37610ef，ppt-video/scripts/render.py）

## 触发场景

- 已有逐页截图（frames）+ 逐页旁白音频（voiceover）需要合成视频时
- 任何「音频驱动时长」的幻灯片视频制作

## 问题与归属判定

- 问题：幻灯片视频若按固定时长（如每页 4 秒）切页，与旁白不同步；手写 ffmpeg 时间轴容易错位。
- 归属（owner）：investagent-html-report-v0.1 workflow SOP（P5 视频渲染）；web-ppt 记录（render.py 复用说明）

## 可复用结论（resolution）

- **最终方案（2026-08-17）**：视频渲染用 **HyperFrames composition**（scene data-start/data-duration 由音频时长驱动，框架精确切换）——**不用 web-ppt render.py 的 xfade 链**（26 级链式 xfade 时长累积误差导致后半段滞后一页，实测 t=780s 应 P26 实际 P25）。HyperFrames 全片同步验证：7 时刻本页像素差 1.7-2.3。

- **目录契约**（web-ppt render.py）：`<dir>/frames/slide_NN.png`（0 基索引）+ `<dir>/voiceover/slide_NN.mp3` → 自动：ffprobe 每页音频时长 → 视频时长 = 音频 + buffer → ASS 字幕（时间轴基于音频 offset）→ ffmpeg xfade 过渡 → video_only.mp4 → 合并音频 → final.mp4。
- **Audio-First 原则**：音频是页面时长的唯一驱动源（旁白读完 → 过渡切页）；字幕由音频时间轴派生（不另写文案）。
- **实测踩坑**：render.py 的合并步骤在后台运行时静默失败（无 final.mp4）——手动 `ffmpeg -y -i video_only.mp4 -i narration-full.mp3 -c:v copy -c:a aac -b:a 192k -shortest final.mp4` 兜底成功；渲染后必须验证 final.mp4 存在 + 时长与音频一致。
- **音画同步验证法**：抽帧（`ffmpeg -ss <t> -i final.mp4 -frames:v 1`）vs 源页截图做像素差对比（<30 视为同页）——在每页切换时刻附近抽帧验证。
- 截图来源可直接复用 qa-html-report 的 paged 产物（index-pNN-WxH.png → frames/slide_NN.png 改名）。

## 回写目标

- investagent-html-report-v0.1 workflow SOP P5（render.py 复用 + 合并兜底 + 同步验证）
- web-ppt 记录注意事项（render.py 合并步骤的静默失败坑）

## 适用范围

- 逐页截图 + 逐页音频 → 幻灯片视频；任意 HTML deck 截图的视频化

## 不适用范围

- 需要动画/动态图表的视频（render.py 是静态帧 + xfade）
- 复杂音效/多音轨（单旁白轨）

## 关联资产

- web-ppt（render.py 归属资源）；investagent-html-report-v0.1（Workflow by-name）；static-html-qa（截图来源）
