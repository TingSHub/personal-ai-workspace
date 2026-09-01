# edge-tts

> 管理资产：`.ai/skills/edge-tts/edge-tts.md`；安装实体：`.claude/skills/edge-tts/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | github · https://github.com/rany2/edge-tts |
| installed_ref | 7.2.8 |
| runtime | both |
| 调用入口 | edge-tts --voice zh-CN-YunjianNeural --rate=+8% --file input.txt --write-media out.mp3（venv 隔离安装） |
| 要求 | Python 3.10+ venv；network（微软端点）；商用红线：非官方逆向接口，微软无书面授权，维护者不建议商用；正式发布迁移 Azure（同源音色） |
| 更新 | package-manager · pip install -U edge-tts 后重跑一条中文试音验证；验证：一段 60 秒中文财经文本合成 + 时长/读法抽查 |
| 辅助脚本 | — |
| 经验引用 | — |

## 作用

免费调用微软 Edge 朗读同款神经语音的非官方 CLI（zh-CN 音色 40+，SSML/rate 支持）。本实验验证：84.14s 中文财经长文一次合成（455 字符），rate=+8% 生效，数字/百分比/AI 读法经 whisper 转写全部验证正确。

## 调用

- venv 隔离安装：`python3 -m venv <dir> && <dir>/bin/pip install edge-tts`
- 合成：`edge-tts --voice zh-CN-YunjianNeural --rate=+8% --file input.txt --write-media out.mp3`
- 本实验产物：`projects/investment-research-system/experiments/listed-company-video-production/outputs/tts/edge-test/`（narration-yunjian.mp3 90.9s / narration-yunjian-rate108.mp3 84.1s）

## 调用注意事项

- **商用红线：不可商用**。非官方逆向接口，微软无书面授权、服务可能随时失效、无 SLA，维护者明确不建议商用；代码 GPLv3
- 仅限内部原型/试音；正式发布迁移 Azure（同源音色，Edge 试音结论可直接延续）
- 输入文本建议做"数字→中文读数"预处理（34.61%→百分之三十四点六一，cn2an 路线）——本实验验证预处理后读法零出错
- 无情感控制参数；长文本分段建议 ≤500 字/段

## 常见失败原因

- 未预处理时部分数字/缩写读法不可控（建议全部走预处理层）
- 网络不可达时合成失败（微软端点）；rate 参数过大音质劣化（+8% 实测自然）
- 商用项目误用此工具的风险最高（许可模糊）——资源文档与正式链路必须隔离

## 最佳实践

- 原型期多音色 A/B 试听的最快路径（零成本、分钟级）
- 与 Qwen3 对齐器配合验证"音频→字幕"链路（本实验全链路跑通）
- 音色选择：财经男声 zh-CN-YunjianNeural（沉稳新闻感）为主，女声 Xiaoxiao 作对照
