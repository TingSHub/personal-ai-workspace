
# Experience: published-video-dialogue-caption-visual-sync

## 来源证据

- 项目：`investment-research-video`，猪周期估值 run `2026-09-06`，用户于 2026-09-07 完播后反馈。
- 调查记录：`2026-09-07-published-video-feedback-investigation`。
- 产物证据：4 个顾慎言 turn 以单音节“对”开头且无句内 break；11 个林知微问句多数仍为 `delivery=normal`；图表仅在 topic 起始一次性绘制；OUTRO 标题由生成器写死。
- 验证时版本：workspace commit `516fa49` 加未提交生产链修改；`podcast-audio-compiler` installed_ref `internal`；VoxCPM2 continuation、inference timesteps 10。

## 触发场景

双人中文 TTS 视频在完播审阅中出现句首单音节吞音/黏连、问句没有升调、数字字幕为中文大写/中文读法、图表与讲述时间脱节，或画面泄漏“双方总结”等制作标签。

## 问题与归属判定

- 单音节与问句语调属于 `podcast-audio-compiler` 和 `dialogue-director-agent` 的可执行表演契约。
- 来源主体是否需要口播、口播/展示数字分轨属于 `finance-content-engineering` 的表达规则。
- 数据点随口播 reveal 属于 `information-visualization-architect` 与 `investagent-video-execution` 的图表时间线契约。
- OUTRO 制作标签属于项目 Composition 生成器缺陷。

## 可复用结论（resolution）

1. 已知会吞音的男声不得以“对/嗯/好”等单音节开启 turn；改成承担语义的短语。标点、同段生成和 ASR 识别均不能替代试听门禁。
2. 问句必须用可执行 delivery 标注，并按音色做问句 canary；问号只负责文本语义，不保证声学升调。**2026-09-07 追加**：句尾语气颗粒（吗/呢/吧…）或疑问语汇（怎么看/什么/对吗…）才是 TTS 升调的主驱动；bare 结构问句（“是不是反转了？”）一律改写加“呢/吗”。canary 已生成并试听：`zhiwei/emotion/questioning.wav` + 2×2 对照（`outputs/experiments/doubao-question-reference-v1/`），Q1/Q3 判定可用。
3. 事实句默认直接说事实，来源通过 evidence、脚注和发布来源清单承载；只有观点、预测、估计、争议口径或来源身份本身重要时才在口播中点名主体。
4. `text` 是 pronunciation-safe TTS 文本，`display_text` 是 viewer-facing 字幕文本；后者优先阿拉伯数字、百分号和单位，两者必须数值等价。
5. 多步图必须声明 `narration_beats` 并按真实 segment start 逐点、逐节点或逐指标 reveal；仅在 scene 开头整体 draw 不算口播同步。
6. 画面标题只写本期结论或内容标题，不显示“双人总结、主持人提问、分析师回答”等制作元信息。

## 回写目标

- `podcast-audio-compiler`：单音节禁用边界、问句 canary、`display_text` 透传与 QA。
- `dialogue-director-agent`、`finance-content-engineering`：来源口播最小化、问句 delivery、双文本数字等价。
- `information-visualization-architect`、`investagent-video-execution`：`narration_beats` 和真实音频时间线 reveal 门禁；登记 `check_podcast_visual_sync.py`。

## 适用范围

中文双人播客/财经解释视频；当前 VoxCPM2 continuation profile 及使用同类逐 turn TTS、字幕和 HyperFrames Composition 的流程。

## 不适用范围

- 引述券商判断、机构预测或存在争议的估计时，来源主体仍应在口播中保留。
- 年份、证券代码、序号等按位朗读的数字不能机械改成普通数值读法。
- 单镜头只表达一个静态结论时，不强制拆成多步 reveal。

## 关联资产

`podcast-audio-compiler`、`dialogue-director-agent`、`finance-content-engineering`、`information-visualization-architect`、`investagent-video-execution`
