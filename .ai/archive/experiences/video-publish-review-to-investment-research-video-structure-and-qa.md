---
name: video-publish-review-to-investment-research-video-structure-and-qa
description: 复盘驱动生产时，先选行业/公司叙事架构并在成片前检查口播重复、声音一致性和封面大字主角
type: methodology
status: archived
owner: topic-forward-lead, investagent-podcast-video-by-hyperframes
asset: topic-forward-lead, investagent-podcast-video-by-hyperframes, podcast-audio-compiler, video-agent-skills
tags: [video-structure, podcast-video, qa, cover, voice-consistency]
---

# Experience: video-publish-review-to-investment-research-video-structure-and-qa

## 来源证据

- 项目：`projects/video-publish-review` → `projects/investment-research-video`
- 运行主题：2026-09-03 液冷产业链行业对比播客视频
- 用户复盘：02、03 存在多句重复；约 2:57 女声变化；约 1:37 男声说“液”时出现异常停顿；男声各节段尾反复使用“不能只看一个漂亮的概念标签”，女声也存在同类固定段尾。
- 用户结构判断：内容要么讲产业链、要么讲公司；更合理的通用路径是“先讲行业，再讲几家公司，最后落到特殊公司”，但模板只作参考，应由复盘和调研结果选择。
- 相关产物：`projects/investment-research-video/outputs/companies/飞龙股份/2026-09-03/podcast/qa/episode-qa.md`、`.../script/episode.json`、`.../composition/cover.html`

## 触发场景

当 `topic-forward-lead` 依据复盘结果生成选题卡并把下一支内容交给 `investment-research-video` 生产时；尤其适用于行业与公司容易混在一起、播客对话容易模板化、或封面在手机端承载点击承诺的选题。

## 问题与归属判定

- 问题：本次先用行业名词开场，后续主体几乎全部落到单家公司，造成标题承诺和正文结构不一致；对话存在跨话题重复、角色段尾固定化和疑似 TTS 局部音色/停顿异常；封面需要突出最值得讲的行业、产业链或公司，手机端只看得清大字。
- 归属（owner）：结构选择和封面要求属于 `topic-forward-lead` → `investagent-podcast-video-by-hyperframes` 的项目工作流契约；口播重复与声音异常属于 `podcast-audio-compiler` / `video-agent-skills` 及播客成片 QA 的质量检查。

## 可复用结论（resolution）

1. 生产时先消费选题卡中的主问题、内容范围和差异化角度，再由内容导演选择叙事方向；至少明确本期是行业、单家公司或公司对比，不把某个方向当成必选模板。
2. 行业主题的默认参考结构是“行业问题/产业链 → 2–4 家公司角色对比 → 最能验证核心问题的特殊公司 → 边界与未验证项”。公司数量由证据决定，不能为套模板硬加公司。
3. 开场必须兑现本期范围：如果标题承诺行业，就在前 10 秒提出行业问题并给出公司比较维度；不要只说几句泛泛的行业名词后转成单家公司介绍。
4. 脚本验收增加跨段去重：检查每个角色的段首、段尾和总结句，禁止同一句结论在多个话题机械复现；同一核心判断要通过推进、反问或证据变化来表达。
5. 音频验收增加时间点抽检：每个角色至少抽查开场、中段、转场和收束；对局部音色变化、单字异常停顿、拼接边界和音量突变做标记，未通过就回到配音阶段。
6. 封面只保留一个主角和一组大字。主角从行业、产业链、公司中选最能代表本期冲突且最引人注目的对象；手机缩略图测试下，小字、日期、公司全称和研究注释全部删除或移入发布文案。

## 回写目标

交由 `experience-curator` 判定后，已分别合并到 `topic-forward-lead`、`investagent-podcast-video-by-hyperframes`、`podcast-audio-compiler` 和 `video-agent-skills` 的既有 Principles / Quality Criteria / Known Issues 章节。

## 适用范围

适用于当前投资研究播客视频链路；音频问题结论来自本次 VoxCPM2 运行，具体阈值应在后续配音版本中继续验证。

## 不适用范围

若选题研究证据只支持单家公司，仍应采用单家公司深挖；行业模板不是固定格式，也不能替代研究结论。未有时间点证据时，不把声音变化断言为确定的模型或设备故障。

## 关联资产

`topic-forward-lead`、`investagent-podcast-video-by-hyperframes`、`podcast-audio-compiler`、`video-agent-skills`、`experience-curator`
