# hyperframes-audio

> 管理资产：`.ai/skills/hyperframes-audio/hyperframes-audio.md`；安装实体：`.claude/skills/hyperframes-audio/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | github · https://github.com/heygen-com/hyperframes |
| installed_ref | c32b804 · HyperFrames bundled skill |
| runtime | both |
| 调用入口 | 按实体定义使用 Composition audio track 的 FX、voiceover carve 和参数自动化 |
| 要求 | Node.js、HyperFrames 项目、已放入 Composition 的音频；不负责媒体寻找、TTS 或 Clip 时序 |
| 更新 | git · 随 HyperFrames 官方技能套件更新；验证：读取实体并完成一条已放置音频的 check |
| 辅助脚本 | `scripts/carve.mjs`：生成或应用 voiceover carve 参数；按实体说明调用 |
| 经验引用 | — |

## 调用说明

用于已有 Composition 音频的混音、ducking、EQ、压缩、限幅、延迟和效果自动化。它不替代播客的 VoxCPM2 编译器，也不负责章节或 Scene 时间轴。
