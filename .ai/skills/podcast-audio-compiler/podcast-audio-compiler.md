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
- **问句 canary（能力验证，先于规则承诺）**：`delivery=rising_question` 只是标注契约，不等于声学升调。使用 `voice.zhiwei` 的问句参考/emotion 资产必须先行生成问句 canary（2–3 个不同句型的问句 turn）并试听：升调稳定才允许把 `rising_question` 作为生产依赖；canary 失败时回退——更换问句参考音频与 emotion 资产，或把该问句改写为不依赖升调的表达（如陈述式引导），并把结论追加到 `.ai/assets/voices/voice-notes.md`。门禁只能证明标注存在，不能证明声学结果。
- **句首单音节风险**：以“对/嗯/好”开启且无句内 break 的 turn 属于该音色的吞音/黏连高风险形态，禁止再生产（契约源头：dialogue-director 实体）；单字回应必须在完整短语中生成，并在 QA 中抽查首字可辨识度。

## Notes

经验引用：`video-publish-review-to-investment-research-video-structure-and-qa`。

情绪参考资产是已登记的兼容资源，不在每个项目重新生成；后续文字 instruct 或 boundary-clean 试验必须使用独立 Workflow profile。音色选择、参考片段规则和历史实验见 `.ai/assets/voices/voices.md` 与 `.ai/assets/voices/voice-notes.md`。

## 节奏控制现状与复用路径

- 当前 VoxCPM2 编译器已复用 emotion 对应的情绪参考音频、逐句 WAV、natural-pauses 和 pause_after_ms；这些能力应继续作为默认生产链路。
- 问句专用参考：`voice.zhiwei` 的 `emotion/questioning.wav`（豆包 expressive，吗/呢 结尾）；`compile_podcast_audio.py` 遇到 `delivery=rising_question` 时自动切换（2026-09-07）。canary 在 `outputs/experiments/doubao-question-reference-v1/canary-voxcpm/`，升调试听稳定前不视为可信生产能力。
- 当逻辑 speaker 显式 override 到另一个 voice asset 时，使用 emotion-override 同步切换情绪参考目录，避免 reference 与 emotion 来自不同音色。
- 当前 delivery（如 pause_before_number、stress_contrast、short_pause）会写入音频元数据，但不会直接改变 VoxCPM2 的语速或句内停顿；natural-pauses 也只按 interaction_type 生成 turn 间静音。
- pacing_plan 已由现有逐句编译器执行：speech_rate 使用 FFmpeg atempo 做逐句变速，intra_turn_breaks 按文本标记拆分合成并插入静音，pause_after_ms 覆盖句尾停顿。默认解析必须保留 VoxCPM 原生语速，不得凭通用 speaker baseline 自动生成 target_rate_cps；只有导演明确标注的节奏才允许 atempo。发现“整体变慢”时先比较 raw WAV 与 paced WAV 的字速和时长，再决定是否需要局部节奏标注。
- 开场应允许比普通 turn 更长的句间停顿，并在“事实反差”和开放问题前声明句内停顿；停顿设计必须进入 segments.json 和 QA，而不是只写在 delivery 标签里。
- 生产前先对 episode manifest 做跨段重复检查，重点检查每个角色的段首、段尾和总结句；相同句式重复出现时必须改写推进关系，不能用固定口头禅填充每一节。可运行 `scripts/check_dialogue_repetition.py <episode.json>`，发现重复时退出码为 1。
- 生产后按开场、中段、转场、收束抽查每个角色的真实 WAV；局部音色变化、单字异常停顿、拼接边界或音量突变都应回到配音阶段重生成，并在 audio-qa 中记录时间点。
- 对单字回应（如“对”“没错”）不得单独切成极短 TTS 片段；应在完整短语中生成，并可用 `pause_anchors` 在完整短语后插入确定性停顿，避免首字被模型吞掉。

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
