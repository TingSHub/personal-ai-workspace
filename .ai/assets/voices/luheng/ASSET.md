# Asset: voice.luheng

> 位置: `.ai/assets/voices/luheng/`

## 元数据

| 字段 | 值 |
|---|---|
| resource_key | `voice.luheng` |
| kind | `voices` |
| description | 陆衡；中性、克制、分析型男声 |
| source | 豆包 TTS / 火山引擎 `zh_male_liufei_uranus_bigtts` |
| version | reference WAV 由文件指纹确定 |
| license | 账号自有/已确认可用于本 workspace |
| files | `reference.wav`、`sample.mp3`、`emotion/` |
| requirements | mono 16kHz WAV；VoxCPM2 reference override |
| prompt_text | 「大家好，我是陆衡。这里是账本两面。今天我们先把收入、利润和现金流放在一起看。增长是真的，但利润能不能留下，还要继续核对。有人更看重规模，也有人更在意回款，这个问题可能没有一句话答案。」 |
| verification | 基础参考音频已通过稳定播客 canary；emotion/ 由 podcast-audio-compiler 的复用脚本生成并逐条检查 |

## 调用说明

播客 Workflow 可将逻辑角色 `analyst=shenyan` 显式 override 到 `voice.luheng`；资源本体不属于任何一个项目或节目版本。

## 注意事项

不是账号默认 speaker；不因某个项目选用而修改 `voice.shenyan` 的默认映射。
