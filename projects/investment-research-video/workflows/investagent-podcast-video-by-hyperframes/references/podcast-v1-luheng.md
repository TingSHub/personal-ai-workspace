# Podcast Workflow Profile: podcast-v1-luheng

这是 `investagent-podcast-video-by-hyperframes` 的一个可复用运行版本，不是账号资产。

## Locked configuration

| Field | Value |
|---|---|
| format | `host_analyst` |
| role map | `host=zhiwei`, `analyst=shenyan` |
| host asset | `voice.zhiwei` |
| analyst asset | `voice.luheng`，通过运行时 override 选择 |
| backend | VoxCPM2 continuation |
| inference timesteps | 10 |
| pauses | `--natural-pauses` |
| post process | `--post-process natural` |
| alternate backends | disabled |
| boundary cleaner | disabled |

## Invocation

```bash
.venv-voxcpm/bin/python \
  .ai/skills/podcast-audio-compiler/scripts/compile_podcast_audio.py \
  --episode <episode.json> \
  --outdir <company-output>/podcast/audio/<run-id> \
  --natural-pauses \
  --post-process natural \
  --inference-timesteps 10 \
  --voice-override shenyan=<workspace>/.ai/assets/voices/luheng/reference.wav \
  --emotion-override shenyan=<workspace>/.ai/assets/voices/luheng/emotion \
  --voice-prompt shenyan="大家好，我是陆衡。这里是账本两面。今天我们先把收入、利润和现金流放在一起看。增长是真的，但利润能不能留下，还要继续核对。有人更看重规模，也有人更在意回款，这个问题可能没有一句话答案。"
```

该 override 只作用于本次 Workflow 运行，不修改项目或账号默认 speaker 映射。

## Acceptance

- 同一 `episode.json`、speaker/role 契约和顶层资源 key 可用于不同公司。
- 每个 turn 独立生成；顺序、停顿和字幕来自实测 `segments.json`。
- `audio-qa.json` 记录 backend、override、停顿、后处理和复用片段数。
- 使用 voice.luheng 作为 shenyan 时，必须同时提供 voice.luheng/reference.wav、voice.luheng/emotion 和登记的 prompt_text。
- 任何 voice override 必须同时提供该资源 `ASSET.md` 中的 `prompt_text`；参考音频与 prompt 不匹配时不得进入生产。
- VoxCPM2 continuation 是本版本的生产后端；CosyVoice3、IndexTTS 和其他 clone mode 属于独立 A/B，不得静默混入本版本。

## Scope

本版本冻结节目音频编译参数，不冻结或复制任何音色文件。声音洁净度和情绪控制优化应创建新的 Workflow profile，不能修改本版本的含义。

## Cover contract

平台封面单独导出为 4:3 PNG（推荐 1440×1080），不进入正片时间轴；`cover.html` 作为可复现源文件保存。
