# Asset: voice-emotion.phase0-v1

> 位置: `.ai/assets/voices/{zhiwei,shenyan,shenyan}/emotion/`

## 元数据

| 字段 | 值 |
|---|---|
| resource_key | `voice-emotion.phase0-v1` |
| kind | `voices` |
| description | 已登记的 curious/skeptical/firm/thoughtful 兼容情绪参考包 |
| source | workspace 统一生成资产 |
| version | Phase 0 v1；清单见 `../emotion-assets.json` |
| license | 与对应 voice asset 相同 |
| files | 三位可用 speaker 各自的 `emotion/*.wav` |
| requirements | 仅供显式支持 emotion reference 的后端使用 |
| verification | 每个文件可解码并通过短句生成检查 |

## 调用说明

项目 profile 可以通过 `voice-emotion.phase0-v1` 选择兼容情绪参考；后续项目复用现有文件，不重新依赖参考视频。

## 注意事项

这是兼容参考包，不是新的基础音色；声音洁净度问题不得通过不断生成新的 emotion prompt 音频来掩盖。
