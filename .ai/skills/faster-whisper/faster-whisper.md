# faster-whisper

> 管理资产：`.ai/skills/faster-whisper/faster-whisper.md`；运行环境：`outputs/companies/紫光股份/2026-08-21/.venv-asr/`；辅助脚本：`outputs/companies/紫光股份/2026-08-21/scripts/transcribe-faster-whisper.py`

## 元数据

| 字段 | 值 |
|---|---|
| name | faster-whisper |
| kind | skill |
| description | 本地中文视频转写(CTranslate2 加速 whisper,CPU 可跑) |
| source | github · Systran/faster-whisper |
| installed_ref | faster-whisper 1.2.1(pip) |
| runtime | both |
| invocation | `.venv-asr/bin/python scripts/transcribe-faster-whisper.py <audio.wav> --model medium --outdir <dir>` |
| requirements | Python 3.10+;ffmpeg(音频提取);模型自动下载(HF,medium ~1.5GB) |
| update | pip 更新;模型按需下载 |
| 辅助脚本 | `transcribe-faster-whisper.py`(转写 → transcript.md + json) |
| 经验引用 | — |

## 作用

中文视频转写:medium 模型质量佳(实测 22 分钟音频 CER 可接受),CPU 转写 22 分钟约 13 分钟,GPU 更快。输出带时间戳分段文本。

## 调用

- 先 `ffmpeg -i <video> -vn -ac 1 -ar 16000 <audio.wav>` 提取音轨,再转写
- `--model small|medium|large-v3`:medium 中文质量/速度平衡;蒸馏等高质量场景用 medium+
- vad_filter=True 过滤静音;beam_size=5

## 调用注意事项

- 转写稿**无说话人标注**:多说话人视频的说话人归属需基频分析等客观验证,不凭句式猜测(实测教训:苏晴/房叔误判事故)
- HF 模型下载慢时可设 HF_ENDPOINT 镜像或 ModelScope

## 常见失败原因

- 音频格式:需 16kHz mono wav(脚本内不转换,先 ffmpeg 转)

## 最佳实践

- 转写是蒸馏/内容分析的前置:先转写再分析,保证文本可追溯
- 中文财经术语转写误差(如「正级收入」→「政企收入」):关键数字需对照原视频抽查
