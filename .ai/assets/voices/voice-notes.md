# Voice Asset Notes

本文件保存音色资产的选择规则、实验结论和历史踩坑；当前可用清单只看 [voices.md](./voices.md)。

## Reference selection

- 优先使用可复现、无 BGM/混响、单说话人的合成参考音频。
- 参考片段以完整句结束，避免尾词残留；通常 8–20 秒，响度接近 `-20dB`。
- 视频提取片段必须经过说话人、性别、尾部呼吸和混音检查。
- 每个音色保存参考 WAV、prompt 文本、来源、授权状态和验证结果。

## Cross-project lessons

- `luheng` 已通过播客 canary 试听，作为独立的备用分析音色资源；具体 Workflow 是否选用它由 Workflow profile 决定。
- 音色资源验证只说明音色可用，不等于某个播客 Workflow 版本被锁定，也不承诺最终噪声底。
- `inference_timesteps=20` 只改善部分高频平滑度，不能单独解决气声或持续性噪声。
- 自然压缩和增益会放大呼吸声；具体 Workflow 是否启用 natural 后处理由 Workflow profile 决定。
- 不把二次生成的情绪片段继续作为新的长期音色资产；后续情绪控制应优先测试文字 instruct 或其他显式 style adapter。

## Runtime notes

- VoxCPM2 环境：workspace 顶层 `.venv-voxcpm`。
- 共享显存环境批量运行前检查可用显存；显存不足时保留失败证据，不静默降级。
- 每次后端或模型版本升级后，先跑一个短 canary，再扩展完整节目。
- 参考片段尾部若出现 chirp、click 或尾词泄漏，优先更换/重做参考资产；不要先用固定裁切掩盖问题。

## Historical experiments

- `zhouyan`：已注册备用音色，未进入稳定 profile。
- `voice.shenyan`：已验证基础男声资源，可被不同项目 profile 选择。
- CosyVoice3、IndexTTS 和 boundary-clean 均属于 Workflow 实验分支，不改变已登记音色资源。
