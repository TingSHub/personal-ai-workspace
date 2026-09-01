# In-flight Experiences（在途经验索引）

经验反馈闭环的检索入口：`.ai/experiences/` 只存**未完成回写的在途经验**（合格经验经「提炼 → 判定归属 → 回写 → 归档」后移入 `.ai/archive/experiences/`）。本表是机器检索索引（一行一条），语义以经验文件为准，不构成执行契约。

## 在途索引表

| 经验（by-name） | type | 一句话摘要（description） | 回写目标（owner） | 加入日期 |
|---|---|---|---|---|
| （示例）`audio-first-video-render` | methodology | 视频生产先定稿脚本→TTS→按真实音频时长分配 Scene 时长→再写画面 | investagent-video-production | 2026-08-17 |

## 维护规则

- **promote（确认回写）**：候选经用户确认后移入本目录，同时在表内登记一行（by-name / type / description / owner / 日期）
- **归档**：回写完成后文件移入 `.ai/archive/experiences/`，本表删除对应行，归档映射表同步登记（见 `.ai/archive/experiences/README.md`）
- **frontmatter 必填**：`name`（= 文件名 slug）、`description`（触发场景一句话，检索相关性判断以此为准）、`type`、`status: in-flight`、`owner`、`asset`、`tags`；字段清单从 `.ai/templates/experience.md.template` 读取
- 当前在途为空（初始状态，仅保留本索引）
