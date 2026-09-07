# Asset: voice.zhiwei

> 位置: `.ai/assets/voices/zhiwei/`

## 元数据

| 字段 | 值 |
|---|---|
| resource_key | `voice.zhiwei` |
| kind | `voices` |
| description | 清晰、专业的中文女声音色 |
| source | 豆包 TTS / 火山引擎 seed-tts-2.0 |
| version | conversational mixed v1；豆包 expressive，speech_rate=-10 |
| license | 账号自有/已确认可用于本 workspace |
| files | `reference.wav`、`emotion/`（含 `surprised.wav`） |
| requirements | mono 16kHz WAV；VoxCPM2/CosyVoice zero-shot reference |
| verification | 克隆短句无尾词残留；已通过播客 canary；`surprised.wav` 为豆包 expressive 生成；`questioning.wav` 为 2026-09-07 问句专用参考（吗/呢结尾），已生成 VoxCPM canary 待试听 |

## 调用说明

项目 profile 可将 `voice.zhiwei` 映射到合适的主持或解说角色；VoxCPM2 prompt 文本和情绪兼容资产保存在同目录。

## 注意事项

保持参考音频和 prompt 文本对应；当前参考文本为「我先说一个直觉啊，这个数字看起来挺亮眼，可是往下拆，现金流好像没有一起跟上。那这个增长，到底是真的变好了，还是只是表面看起来热闹？」；不使用项目公司内容重新覆盖该资源。

## 问句参考（questioning，2026-09-07）

问题：现有问句沿用 `curious` 参考，句尾升调不明显，VoxCPM2 复现不出可靠升调。

- 文件：`emotion/questioning.wav`（豆包 seed-tts-2.0-expressive，zh_female_xiaohe_uranus_bigtts，speech_rate=-10，14.28s，16kHz mono；生成脚本 `projects/investment-research-video/scripts/generate-doubao-question-reference.py`）
- prompt 文本：`先别急着说好事。价格是回来了，可这次的回暖，真的能站得住吗？我顺着你的逻辑再问一句：如果利润还留在低位，那现在这组价格，是不是已经提前预支了反弹呢？`
- 用法：编译器在 `delivery=rising_question` 时自动改用本参考（`compile_podcast_audio.py`）；主参考 `reference.wav` 未被修改。
- canary：`outputs/experiments/doubao-question-reference-v1/canary-voxcpm/segments/{Q1,Q3}.wav` 待试听，升调稳定后才有资格作为生产能力。
