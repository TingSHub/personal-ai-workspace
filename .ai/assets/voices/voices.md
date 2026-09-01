# Workspace voice asset registry

本文件只维护跨项目可复用的音色资源；项目角色、节目主持人和默认映射由各项目 `account-profile` 决定。实验记录见 [voice-notes.md](./voice-notes.md)。

## Asset inventory

| resource_key | display name | acoustic profile | reference | verification |
|---|---|---|---|---|
| `voice.zhiwei` | 林知微 | 清晰、专业、女声 | `zhiwei/reference.wav` | validated |
| `voice.shenyan` | 顾慎言 | 克制、分析型、男声 | `shenyan/reference.wav` | validated |
| `voice.luheng` | 陆衡 | 中性、克制、分析型男声 | `luheng/reference.wav` | validated |
| `voice.zhouyan` | 周砚 | 中性、克制、分析型男声 | `zhouyan/reference.wav` | A/B only |

每个资源的来源、许可证、prompt 文本、格式和验证记录在对应目录的 `ASSET.md`。音频本体与元数据必须同目录保存。

## Emotion bundle

已登记的兼容情绪参考位于：

```text
.ai/assets/voices/{zhiwei,shenyan}/emotion/{curious,skeptical,firm,thoughtful}.wav
```

清单和生成记录见 `.ai/assets/voices/emotion-assets.json`。项目通过 `resource_key` 选择资源，不重新依赖参考视频。

## Hard rules

- 项目不得复制音色本体；只在 `account-profile` 保存资源选择和用途。
- 不跨 backend 或 profile 静默复用音频缓存。
- 音色身份、尾词残留、杂音和响度抽检未通过时，不进入项目 Workflow。
- 后续声音洁净度优化建立新资源或新 Workflow profile；不得悄悄覆盖当前资源。
