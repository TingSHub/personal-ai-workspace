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
| verification | 克隆短句无尾词残留；已通过播客 canary；`surprised.wav` 为豆包 expressive 生成 |

## 调用说明

项目 profile 可将 `voice.zhiwei` 映射到合适的主持或解说角色；VoxCPM2 prompt 文本和情绪兼容资产保存在同目录。

## 注意事项

保持参考音频和 prompt 文本对应；当前参考文本为「我先说一个直觉啊，这个数字看起来挺亮眼，可是往下拆，现金流好像没有一起跟上。那这个增长，到底是真的变好了，还是只是表面看起来热闹？」；不使用项目公司内容重新覆盖该资源。
