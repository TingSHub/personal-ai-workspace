# Asset: voice.shenyan

> 位置: `.ai/assets/voices/shenyan/`

## 元数据

| 字段 | 值 |
|---|---|
| resource_key | `voice.shenyan` |
| kind | `voices` |
| description | 克制、分析型的中文男声音色 |
| source | 账号自有基础参考音频 |
| version | reference WAV 由文件指纹确定 |
| license | 账号自有/已确认可用于本 workspace |
| files | `reference.wav`、`emotion/` |
| requirements | mono 16kHz WAV；VoxCPM2/CosyVoice zero-shot reference |
| verification | 克隆短句无尾词残留；已通过音色验证 |

## 调用说明

项目 profile 可将 `voice.shenyan` 映射到合适的解说或分析角色；具体 Workflow 也可显式 override 到另一个已注册 voice key。

## 注意事项

默认资源不因单次 A/B 运行自动替换；持续气声/噪声实验应生成新资源或新 profile。
