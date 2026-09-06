# podcast-audio-compiler

> 管理资产：`.ai/skills/podcast-audio-compiler/podcast-audio-compiler.md`
> 脚本目录：`.ai/skills/podcast-audio-compiler/scripts/`

## Contract

将同一份 `episode.json` 编译为逐句 WAV、交替全片音频、`segments.json`、SRT 和 `audio-qa.json`。编译器只执行已锁定的文本、speaker、role、emotion、delivery 和 pause 字段，不补研究事实、不临时改数字。

## Workflow profiles

具体版本参数由调用它的 Workflow 管理，例如
`investagent-video-execution` 的 `audio-compile` Phase；当前生产参数直接以该 Workflow 为准。
本 Skill 只定义通用编译契约，不拥有账号资产或播客版本。

## Entrypoints

```text
scripts/compile_podcast_audio.py       VoxCPM2，稳定生产
scripts/compile_index_tts_audio.py    IndexTTS-2.5，显式 A/B
scripts/compile_cosyvoice_audio.py    CosyVoice3，显式 A/B/instruct
scripts/generate_emotion_assets.py    Phase 0 一次性情绪资产
scripts/resolve_pacing_plan.py        emotion/delivery/interaction → 确定性 pacing_plan
scripts/check_dialogue_repetition.py  episode manifest 的跨段重复句与固定段尾检查
```

默认入口：

```bash
.venv-voxcpm/bin/python .ai/skills/podcast-audio-compiler/scripts/compile_podcast_audio.py \
  --episode <episode.json> --outdir <output> \
  --natural-pauses --post-process natural \
  --voice-override shenyan=<workspace>/.ai/assets/voices/shenyan/reference.wav
```

## Hard gates

- manifest 必须包含 `format_mode`、`role_map`、`turn_id`、`topic_id`、`speaker` 和 `text`。
- voice override 必须同时传入对应资源的 `prompt_text`；参考音频与 prompt 文本不一致时停止，不使用逻辑 speaker 的默认 prompt 静默替代。
- 相邻 speaker、voice asset、turn 顺序和文件存在性检查失败即停止。
- 每个 turn 独立生成；字幕时间来自真实音频，不使用字数估时。
- QA 必须记录 backend、profile/override、停顿、后处理和缓存复用数。
- 后端 A/B 必须使用同一 manifest，输出目录和 backend 明确隔离。

### 补充规则

- TTS 完成后，对每个 turn 执行已知文本对齐或反向转写检查；QA 必须记录 turn 数、异常句和重生成闭环，不能只检查文件存在。
- 全局时间线校验应将相邻 turn 间隔与 `pause_after_ms` 对照，避免把已记录停顿误判为时间线断裂。

## Notes

经验引用：`video-publish-review-to-investment-research-video-structure-and-qa`。

情绪参考资产是已登记的兼容资源，不在每个项目重新生成；后续文字 instruct 或 boundary-clean 试验必须使用独立 Workflow profile。音色选择、参考片段规则和历史实验见 `.ai/assets/voices/voices.md` 与 `.ai/assets/voices/voice-notes.md`。

## 节奏控制现状与复用路径

- 当前 VoxCPM2 编译器已复用 emotion 对应的情绪参考音频、逐句 WAV、natural-pauses 和 pause_after_ms；这些能力应继续作为默认生产链路。
- 当逻辑 speaker 显式 override 到另一个 voice asset 时，使用 emotion-override 同步切换情绪参考目录，避免 reference 与 emotion 来自不同音色。
- 当前 delivery（如 pause_before_number、stress_contrast、short_pause）会写入音频元数据，但不会直接改变 VoxCPM2 的语速或句内停顿；natural-pauses 也只按 interaction_type 生成 turn 间静音。
- pacing_plan 已由现有逐句编译器执行：speech_rate 使用 FFmpeg atempo 做逐句变速，intra_turn_breaks 按文本标记拆分合成并插入静音，pause_after_ms 覆盖句尾停顿。再用同一批 WAV/SRT/QA 做 A/B，不先换 TTS 后端，也不把 HyperFrames Audio 当作口播语速控制器。
- 开场应允许比普通 turn 更长的句间停顿，并在“事实反差”和开放问题前声明句内停顿；停顿设计必须进入 segments.json 和 QA，而不是只写在 delivery 标签里。
- 生产前先对 episode manifest 做跨段重复检查，重点检查每个角色的段首、段尾和总结句；相同句式重复出现时必须改写推进关系，不能用固定口头禅填充每一节。可运行 `scripts/check_dialogue_repetition.py <episode.json>`，发现重复时退出码为 1。
- 生产后按开场、中段、转场、收束抽查每个角色的真实 WAV；局部音色变化、单字异常停顿、拼接边界或音量突变都应回到配音阶段重生成，并在 audio-qa 中记录时间点。

### pacing_plan 字段

```json
{
  "target_rate_cps": 3.9,
  "speech_rate": 0.96,
  "pause_after_ms": 360,
  "intra_turn_breaks": [
    {"after": "经营现金流反而下降了。", "pause_ms": 360}
  ]
}
```

字段挂在 episode manifest 的单个 turn 上；target_rate_cps 推荐范围为 3.2–4.3，speech_rate 作为无目标字速时的兼容 fallback；断点标记必须在原文中可定位。编译器会把目标、原始和实际字速写回 segments.json，供 QA 和 A/B 对比。
