# video-agent-skills

> 管理资产：`.ai/skills/video-agent-skills/video-agent-skills.md`；安装实体：`.claude/skills/video-agent-skills/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | github · https://github.com/chenyuxiaojin/video-agent-skills |
| installed_ref | fc80890 |
| runtime | claude |
| 调用入口 | 读取各 skill 的 SKILL.md 按其指示执行（Claude Code 原生 skills 形态）；researcher 走 organize 模式输入冻结母稿 |
| 要求 | 冻结研究素材（叙事大纲唯一输入）；writer 需外部给定秒级时长分配（资源字数表最小档 5 分钟）；storyboarder/visual 依赖 GEMINI_API_KEY（无离线降级） |
| 更新 | git · 拉取上游新版本到临时目录审查 SKILL.md 变更后更新 vendor；保留本资源说明；验证：researcher organize 模式对一份中文研究素材产出叙事大纲 + writer 产出一段中文口播稿 |
| 辅助脚本 | — |
| 经验引用 | `video-publish-review-to-investment-research-video-structure-and-qa` |

## 作用

中文原生视频流水线 skill 集（11 个）。本实验验证：researcher organize 模式（输入冻结母稿 → 10,979 字叙事整理稿，叙事目的标注+原文引用+金句索引）+ writer（230 汉字中文口播稿，反常识开头，事实核对 0 硬错误）。

## 调用

- 按其 SKILL.md 原生执行：researcher 走 organize 模式（has_source_material: true）→ writer（识别 tech-sci 加载模板）→ producer（project.json + 人工检查点）
- 注意：本实验以 Claude 直接扮演各 skill 角色执行（其在 Claude Code 中的原生运行方式）；producer 的 4 个人工检查点需用户确认
- 本实验产物：`projects/investment-research-system/experiments/listed-company-video-production/outputs/content/video-agent-skills/`

## 调用注意事项

- 推荐输入：已冻结研究母稿（organize 模式要求"通读后按叙事重组"，输入必须完整）
- 字数表最小档是 5 分钟——60-90 秒短视频需外部给定秒级时长分配（模型补位，非资源原生能力）
- 多文档输入无结构化合并机制（sources.json 是搜索模式产物）——多份研报需先自行合并为母稿

## 常见失败原因

- **storyboarder 硬依赖 GEMINI_API_KEY**（generate_storyboard.py 无离线降级，SKILL.md 明确职责边界）——无 key 时跳过并标记
- writer 的"素材富裕模式"依赖整理稿 ≥60% 字数保留（不足时输出会偷懒）
- 数字口语化会四舍五入（34.61%→34%）——事实核对时注意与精确值区分，发布前用精确值
- 默认长视频叙事框架（案例式论证），短视频需大幅压缩

## 最佳实践

- researcher organize 是"研报→叙事大纲"的最佳现成骨架：强制叙事目的标注+金句索引，把编剧约束为语言转换
- writer 的中文口播（280 字/分、第一人称、破立结合）可作为口播规范的基准参考
- 与其他候选组合：hook 用 claude-youtube 方法论、时长分配用外部 Scene 表
- 生产前先接收叙事架构 brief：行业主题默认按“行业问题 → 公司角色对比 → 特殊案例”组织，但必须用复盘和研究证据决定是否采用；脚本验收应检查范围兑现、跨段重复和角色段尾模板化。
