# video-production-executor

> 管理资产：`.ai/agents/video-production-executor/video-production-executor.md`；安装实体：`.agents/video-production-executor.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | agent |
| 来源 | internal · workspace internal agent profile |
| installed_ref | internal |
| runtime | both |
| 调用入口 | 由当前项目主 Agent 按 Workflow 与项目输出模板执行 |
| 要求 | 已验收的内容策划、长视频脚本、字幕初稿和素材规划；FFmpeg 与 ffprobe；Python 3.12；Node.js；配音提供方、人工旁白输入或已配置的 TTS/voice provider；图片生成或图表生成能力 |
| 更新 | internal · 只调整本地视频生产调用说明和输出契约，不改写上游研究事实；验证：针对同一内容资产包依次产出旁白、视觉素材、对齐字幕、预览视频和发布包，并用 ffprobe、字幕凭据和质量报告复核 |
| 辅助脚本 | — |
| 经验引用 | research-master-content-pipeline |

## 作用

把已验收的视频内容资产包推进到可播放样片和发布包（旁白、视觉素材、字幕、预览成片、发布包）。只负责生产执行，不补研究、不改研究结论、不重做内容策划。

## 实体位置（可加载定义）

- `.agents/video-production-executor.md`——完整职责（定位/调用边界/一致性检查/更新）

## 调用方式

- 输入：已验收的内容策划、长视频脚本、字幕初稿和素材规划
- 输出：旁白、视觉素材、对齐字幕、预览视频、发布包

## 注意事项与踩坑

- 不新增研究事实、财务数字、估值结论或风险判断。
- 视觉素材优先自制图表/SVG/PIL/matplotlib 或已授权素材，不默认抓取来源不明图片。
- 渲染前锁定最终旁白、字幕和视觉素材版本；预览视频须同时含视频流和音频流，不是简单 PPT 翻页。
