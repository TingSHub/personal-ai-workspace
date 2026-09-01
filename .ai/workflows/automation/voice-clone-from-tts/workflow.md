# Workflow: voice-clone-from-tts

> 位置: Global: .ai/workflows/automation/voice-clone-from-tts/workflow.md

## Mission

用专业 TTS(豆包)合成干净的克隆参考音频,再用 VoxCPM 终极克隆为本地可复用的品牌音色,并注册音色资产配方。解决「从视频提取参考音频」的音质问题(噪声/残留/说话人混杂),让音色资产化、可复现、不依赖视频源。

## Input

| 字段 | 必填 | 说明 |
|---|---|---|
| voice_id | 是 | 豆包 TTS 音色 ID(如 zh_female_xiaohe_uranus_bigtts) |
| voice_name | 是 | 音色资产名(如 xiaohe),用于 voices.md 注册 |
| reference_text | 否 | 克隆参考文本;默认模板(覆盖陈述/数据强调/对比/疑问,结尾闭合句) |
| 人设描述 | 否 | 音色人设(如「专业女声,财经播报」),记入配方 |

## Output

| 产物 | 位置 | 格式 |
|---|---|---|
| 克隆参考音频 | `{assets}/voices/clone-reference/{voice_name}.wav` | wav 16kHz,结尾干净完整句 |
| 音色配方 | `{assets}/voices/voices.md` 条目 | 参考片段 + prompt 文本 + 生成参数 + 验证记录 |
| 验证样音 | `{workdir}/example/{voice_name}-test-*.wav` | 克隆测试句(无残留/无杂音) |

## Principles

- 克隆源优先级:**专业 TTS 合成 > 视频提取**(合成源干净/可控/可复现)
- 参考片段结尾必须干净完整句(尾词残留防护)
- 合成后必验:尾词残留 / 杂音 / 性别基频 / 开头音量
- 音色资产化:每个音色 = 参考片段 + prompt 文本配方,存 voices.md 可复用
- by-name 引用资源;真实执行留痕

## Phase 1: 参考合成 — 豆包 TTS

### Goal

用指定豆包音色合成 8-25s 克隆参考音频,文本覆盖多种情绪(陈述/数据强调/对比张力/哲理/疑问),结尾闭合完整句。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| doubao-tts | skill | 必选 | 火山引擎 seed-tts-2.0 · VOLC_API_KEY | 合成参考音频;code 20000000 为 OK 事件非错误;辅助脚本 `scripts/doubao-voice-ref.py` |

### Input

- voice_id / voice_name / reference_text(或默认模板)

### Output

- `{assets}/voices/clone-reference/{voice_name}.wav`(16kHz,时长 8-25s)

### Quality Criteria

- 音频时长 8-25s;响度正常(mean ~-20dB);无 BGM/噪声(合成源天然满足)
- 结尾为完整闭合句(句号/问号收尾,无半句)
- 文本覆盖 ≥3 种情绪表达

### Known Issues

- 豆包 API 流式响应:data 为空 + code 20000000 是事件不是错误;只取有 data 的行
- 音色 ID 发音/语速差异:合成后先听/探测,不满意换 ID 或调整参考文本

## Phase 2: 克隆 — VoxCPM 终极克隆

### Goal

用 VoxCPM2 终极克隆(参考音频 + prompt 文本)生成目标音色,复刻音色/情绪/节奏。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| voxcpm | skill | 必选 | OpenBMB VoxCPM2 · torch 2.11+cu126 配套 | 终极克隆 `generate(text, prompt_wav_path, prompt_text)`;显存管理见资源记录 |

### Input

- Phase 1 参考音频 + prompt 文本(参考文本与音频内容一致)

### Output

- 克隆验证样音 2 句(不同文本:陈述 + 数据对比)
- `{workdir}/example/{voice_name}-test-*.wav`

### Quality Criteria

- 克隆样音音色正确(与参考一致)
- 无尾词残留(参考片段尾词不得出现在输出开头)
- 无中间杂音;开头音量与整体一致(辅音起音可接受)
- 生成参数记录:`cfg_value=2.0, inference_timesteps=10`

### Known Issues

- 尾词残留:参考片段结尾不干净 → 输出开头残留尾词;更换/修剪参考片段,不手工修
- 杂音:个别克隆源生成句中间有杂音 → 弃用该源(实测豆包小明音色)
- 显存:WSL2 共享显存,批量前 nvidia-smi free ≥8GB;切屏/图形活动触发 CUDA OOM

## Phase 3: 注册 — 音色资产

### Goal

将验证通过的音色注册到资产配方(voices.md),固化参考片段 + prompt 文本 + 生成参数 + 人设。

### Required Resources

| Resource | Type | 必选/可选 | 来源/版本 | 适用与已知限制 |
|---|---|---|---|---|
| resource-manager | skill | 必选 | internal | 音色资产按资源规范维护(voices.md 为项目内资产文件,记录配方) |

### Input

- Phase 2 验证通过的克隆音色 + 配方要素

### Output

- `{assets}/voices/voices.md` 新增/更新音色条目(参考片段 + prompt 文本 + 生成参数 + 人设 + 验证记录)
- 废弃音色移入废弃记录(注明原因)

### Quality Criteria

- voices.md 条目完整(克隆参考/prompt 文本/生成参数/验证记录)
- 废弃音色有废弃原因记录
- 资产路径可解析,克隆配方可复现(重新生成结果一致)

### Known Issues

- 音色资产跨项目复用:voices.md 在项目内,跨项目用需复制资产或引用路径
