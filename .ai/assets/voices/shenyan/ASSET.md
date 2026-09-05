# Asset: voice.shenyan

> 位置: `.ai/assets/voices/shenyan/`

## 元数据

| 字段 | 值 |
|---|---|
| resource_key | `voice.shenyan` |
| kind | `voices` |
| description | 顾慎言；中性、克制、分析型男声 |
| source | 豆包 TTS / 火山引擎 `zh_male_liufei_uranus_bigtts` |
| version | conversational mixed v1；豆包 expressive，speech_rate=0 |
| license | 账号自有/已确认可用于本 workspace |
| files | `reference.wav`、`sample.mp3`、`emotion/` |
| requirements | mono 16kHz WAV；VoxCPM2 reference override |
| prompt_text | 「等等，这个数字我得先打个问号。收入是涨了没错，可现金流怎么还没跟上？先别急着说业务变好了，利润到底是怎么来的，还得再看一眼。」 |
| verification | 基础参考音频已通过稳定播客 canary；emotion/ 由 podcast-audio-compiler 的复用脚本生成并逐条检查 |

## 调用说明

播客 Workflow 可将逻辑角色 `analyst=shenyan` 显式 override 到 `voice.shenyan`；资源本体不属于任何一个项目或节目版本。

## 注意事项

不是账号默认 speaker；不因某个项目选用而修改 `voice.shenyan` 的默认映射。
