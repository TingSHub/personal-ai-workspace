# qwen3-forced-aligner

> 管理资产：`.ai/skills/qwen3-forced-aligner/qwen3-forced-aligner.md`；安装实体：`.claude/skills/qwen3-forced-aligner/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | other · https://huggingface.co/Qwen/Qwen3-ForcedAligner-0.6B；包 https://pypi.org/project/qwen-asr/ |
| installed_ref | qwen-asr 0.0.6（transformers 4.57.6 后端） |
| runtime | both |
| 调用入口 | python -c 调 Qwen3ForcedAligner.from_pretrained("Qwen/Qwen3-ForcedAligner-0.6B", dtype=torch.bfloat16, device_map="cuda:0").align(audio, text, language="Chinese") |
| 要求 | Python 3.12 + venv；GPU ≥ 8GB（0.6B bfloat16 实测 RTX 3060 可用）；CPU 未验证；torch（CUDA 版）+ transformers 4.57（5.x 无 forced-alignment pipeline）；模型权重首次下载 ~1.3GB（HF Hub） |
| 更新 | package-manager · pip install -U qwen-asr 后重跑一条 30 秒中文对齐验证；注意 qwen-asr 会固定 transformers 版本；验证：一条 30-60 秒中文 TTS 音频 + 已知文本对齐，字级时间戳末字误差 <1s |
| 辅助脚本 | — |
| 经验引用 | podcast-editorial-gate-and-audio-render-regression |

## 作用

Qwen3-ForcedAligner-0.6B（qwen-asr 包）：**已知文本强制对齐**——TTS 音频 + 脚本文本 → 中文字级时间戳。本实验 84.14s 音频 → 396 个字级时间戳（末字 83.36s，误差 <1s），SRT 自动分组 9 行，GPU 推理约 1-2 分钟。

## 调用

- 安装：`pip install qwen-asr`（会固定 transformers 4.57.x；建议隔离 venv）；模型权重首次下载 ~1.3GB
- 用法：
  ```python
  from qwen_asr import Qwen3ForcedAligner
  model = Qwen3ForcedAligner.from_pretrained("Qwen/Qwen3-ForcedAligner-0.6B", dtype=torch.bfloat16, device_map="cuda:0")
  results = model.align(audio="narration.mp3", text="已知文本", language="Chinese")
  # results[0][0].text / .start_time / .end_time（字级）
  ```
- 本实验脚本：`projects/investment-research-system/experiments/listed-company-video-production/scripts/align_minimal.py`（字级 JSON + SRT 分组：停顿 >0.5s + 标点断开）

## 调用注意事项

- 文本必须已知（它是对齐器不是识别器）——本项目旁白文本来自脚本，天然满足
- 标点/数字会被过滤（对齐输出不含标点，分组逻辑需自处理）
- 单次对齐最长约 270s，更长用 alignLong()；多音字/英文缩写按拼音标注（IndexTTS 系才支持，本模型不额外处理）
- GPU 推荐；bfloat16；0.6B 在 RTX 3060 实测流畅

## 常见失败原因

- **transformers 5.x 无 forced-alignment pipeline**（实测 5.15 报 unknown task）——必须用 qwen-asr 包（其依赖 transformers 4.57）
- qwen-asr 首次 pip 安装可能因网络缓存失败——重试即可
- 对齐质量与 TTS 清晰度强相关：Edge/Azure 系干净音频效果优秀；带 BGM 或混响音频需先分离
- faster-whisper 与 torch cu130 的 libcublas 版本不匹配会 GPU 报错（ctranslate2 需 libcublas.so.12）——用 CPU int8 兜底

## 回写条目（来源: podcast-editorial-gate-and-audio-render-regression）

- 在逐句 TTS 生产中，优先对每个已知文本 turn 做短音频对齐，记录空结果、越界时间和异常 turn；逐句结果可直接作为音频 QA 的可追溯证据。

## 最佳实践

- **Audio First 链路核心组件**：script → TTS → Qwen3 对齐 → 字级 JSON → 引擎字幕组件/SRT 同源导出
- 字级 JSON 直喂 Remotion captions（startMs 换算）或 HyperFrames captions skills；SRT 供平台上传
- 与 faster-whisper 对照使用：对齐器管"已知文本精确时间"，whisper 管"未知音频转写"
