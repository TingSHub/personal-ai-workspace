# video-quality-reviewer

> 管理资产：`.ai/agents/video-quality-reviewer/video-quality-reviewer.md`；安装实体：`.agents/video-quality-reviewer.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | agent |
| 来源 | internal · workspace internal agent profile |
| installed_ref | internal |
| runtime | both |
| 调用入口 | 由当前项目主 Agent 按 Workflow 与项目输出模板执行 |
| 要求 | 已渲染的预览视频；最终旁白音频；声学对齐字幕；视觉素材与素材规划；ffprobe 或等效媒体检查能力 |
| 更新 | internal · 只调整本地质量检查说明和输出契约，不改写上游内容或渲染产物；验证：对同一预览视频完成媒体检查、字幕同步抽查、视觉一致性复核并写出独立报告 |
| 辅助脚本 | — |
| 经验引用 | research-master-content-pipeline |

## 作用

对预览成片做只读质量验收：内容一致性、字幕与音频同步、视觉可读性、素材来源和最终可发布性。只检查，不补内容、不改渲染、不重做字幕。

## 实体位置（可加载定义）

- `.agents/video-quality-reviewer.md`——完整职责（定位/调用边界/一致性检查）

## 调用方式

- 输入：已渲染的预览视频、最终旁白音频、声学对齐字幕、视觉素材与素材规划
- 输出：发布前问题清单（含位置、证据和回退步骤）

## 注意事项与踩坑

- 质量报告必须引用已生成的预览视频、最终旁白音频和正式字幕。
- 字幕必须来自最终旁白音频，不是估时稿。
- 检查内容与冻结研究一致、视觉不退化 PPT、BGM 不盖人声、文件流与封面发布文案完整。

## 跨项目使用边界

- 只读验收，不改写 Notes、字幕、研究事实、Composition 或渲染结果；发现问题时输出位置、证据和建议回退阶段。
- 验收结论必须区分媒体事实、同步观察、内容一致性判断和未验证项，不以“看起来正常”替代可复核证据。
