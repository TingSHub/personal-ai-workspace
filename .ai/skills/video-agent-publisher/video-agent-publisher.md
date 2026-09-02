# video-agent-publisher

> 管理资产：`.ai/skills/video-agent-publisher/video-agent-publisher.md`；安装实体：`.claude/skills/video-agent-skills/video-agent-publisher/`

## 元数据

| 字段 | 值 |
|---|---|
| name | video-agent-publisher |
| kind | skill |
| description | 为抖音、B站、视频号、小红书、快手、YouTube生成平台差异化发布元数据和来源清单 |
| source | internal workspace skill · `.claude/skills/video-agent-skills/video-agent-publisher/` |
| runtime | claude / codex |
| invocation | `python scripts/generate_metadata.py <script.md> <outline.md> <output_dir>`；`python scripts/compile_sources_list.py <script.md> [output.md]` |
| requirements | 已验收 script、研究来源清单和平台字数/封面规则；不执行真实发布 |
| update | manual · 随外部实体更新本地调用说明；verify：生成 metadata.json 和 sources.md 并检查平台字段 |
| scripts | 外部实体内置 `generate_metadata.py`、`compile_sources_list.py` |
| experience_refs | 无 |

## 调用说明

该资源只负责 `publish/metadata.json` 和 `publish/sources.md`，不代替 AiToEarn 或浏览器发布工具。每个平台必须有独立标题、描述、标签、封面和字数校验；研究事实不能因平台改写而改变。生成结果进入 AiToEarn Flow 的 `content` 与每个平台 item 的 `overrides`。
