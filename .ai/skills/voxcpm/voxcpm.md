# voxcpm

> 管理资产：`.ai/skills/voxcpm/voxcpm.md`；共享运行环境：`/home/henry/personal-ai-workspace/.venv-voxcpm/`

## 元数据

| 字段 | 值 |
|---|---|
| name | voxcpm |
| kind | skill |
| description | 本地 GPU TTS + 音色克隆(OpenBMB VoxCPM2,Apache-2.0,30 语言含中文,终极克隆/语音设计) |
| source | github · https://github.com/OpenBMB/VoxCPM |
| installed_ref | openbmb/VoxCPM2(2B,safetensors BF16 4.3GB) |
| runtime | both |
| invocation | `/home/henry/personal-ai-workspace/.venv-voxcpm/bin/python <脚本>`;`VoxCPM.from_pretrained("openbmb/VoxCPM2", load_denoiser=False, optimize=False)` |
| requirements | Python 3.10-3.12;PyTorch ≥2.5 + torchaudio 匹配版本(实测 torch 2.11.0+cu126 + torchaudio 2.11.0+cu126,cu126 索引 torchaudio 最高 2.11);RTX 3060 12GB(峰值 ~10.6GB);CUDA ≥12 |
| update | pip 安装新版本 + 复验克隆效果;环境重建需保持 torch/torchaudio 版本匹配 |
| 辅助脚本 | 项目内:`voxcpm-batch.py`(批量克隆配音)/ `clone-voxcpm-hosts.py`(参考实现)/ `test-voxcpm.py` |
| 经验引用 | — |

## 作用

本地 TTS + 音色克隆:终极克隆(参考音频 + prompt 文本 → 复刻音色/情绪/节奏)、可控克隆(仅音色)、语音设计(文字描述生成音色)。中文 CER 0.97%(Seed-TTS-eval)。生成参数:`cfg_value=2.0, inference_timesteps=10`(速度档;步数 20 更顺但慢 1.5-2 倍)。

## 调用

- 批量配音:`voxcpm-batch.py --script <SCRIPT.md> --outdir <dir> --voice zhiwei|shenyan`(输出 segments/ + narration-full.mp3 + segments.json)
- 克隆配方(参考片段 + prompt 文本)见顶层 `.ai/assets/voices/` 的 `ASSET.md`；项目 account-profile 只选择 `resource_key`。账号默认音色为林知微(`voice.zhiwei`)与顾慎言(`voice.shenyan`)
- 显存管理:PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True + 每句后 gc/empty_cache;切屏等图形活动会 OOM,批量前查 nvidia-smi free ≥8GB

## 调用注意事项

- **尾词残留**:终极克隆会把参考片段尾词带到输出开头——参考片段必须结尾干净完整句;合成后检查残留
- **杂音**:个别克隆源生成句中间有杂音(实测豆包小明音色)——有杂音即弃用该源
- **性别验证**:视频提取的参考片段必须基频验证(男<160Hz/女≥160Hz)
- **WSL2 共享显存**:Windows 图形占用波动(3-9GB),可用显存 = 12GB - 图形占用

## 常见失败原因

- torchaudio 加载失败 = torch/torchaudio 版本不匹配(cu126 索引配套 2.11)
- CUDA unknown error = 显存不足(图形占用高)或瞬时状态,重试或等图形空闲

## 最佳实践

- 克隆参考源优先级:豆包等专业 TTS 合成音 > 视频提取(干净/可控/可复现)
- 音色资产化:每个音色 = 参考片段 + prompt 文本配方,存 voices.md 可复用
