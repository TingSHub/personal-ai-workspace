# doubao-tts

> 管理资产：`.ai/skills/doubao-tts/doubao-tts.md`；协议原文：`.ai/skills/doubao-tts/references/`

## 元数据

| 字段 | 值 |
|---|---|
| name | doubao-tts |
| kind | skill |
| description | 豆包语音合成：原生音色、声音复刻、expressive 情绪参考、单向/双向 WebSocket 和播客 API |
| source | 火山引擎(bytedance openspeech API)· 非开源服务 |
| installed_ref | seed-tts-2.0(API) |
| runtime | both |
| invocation | 项目脚本：`projects/investment-research-video/scripts/tts-doubao-v3-ws-test.py`；参考音频：`generate-doubao-conversational-references.py` / `generate-doubao-surprised-references.py` |
| requirements | 网络可达 `openspeech.bytedance.com`；工作区 `.env` 中按接口配置凭证；不要把凭证写入 Skill 或脚本 |
| update | API 版本演进由火山引擎管理;脚本本地维护 |
| 辅助脚本 | 旧版 `doubao-voice-ref.py`/`tts-doubao.py`；V3 双向 WebSocket `tts-doubao-v3-ws-test.py`；参考音频生成脚本见 `projects/investment-research-video/scripts/` |
| 经验引用 | — |

## 作用

豆包 TTS 是本项目的远程参考音频来源和可选播客生成后端。当前本地生产链主要用它生成 16kHz 单声道 WAV，再交给 VoxCPM2 做本地逐句合成。

## 接口选择

- **双向流式 WebSocket**：文本可以分段输入，音频分段输出，适合实时交互；当前 V3 测试客户端使用 `wss://openspeech.bytedance.com/api/v3/tts/bidirection`、`X-Api-Resource-Id: seed-tts-2.0`。
- **单向流式 WebSocket/HTTP**：一次提交文本、流式返回音频，适合批量或普通低延迟合成；需要简单稳定地生成单段参考音频时优先考虑。
- **播客 API WebSocket V3**：直接生成双人播客，支持轮次、角色和播客专属事件；效果自然但属于独立的付费/额度型产品，不作为当前本地 VoxCPM2 主链。
- **音频生成 HTTP**：可用文本提示和音频参考做创作型生成，适合探索，不作为当前标准参考音频入口。

## 当前音色映射

- 知微：`zh_female_xiaohe_uranus_bigtts`
- 慎言：`zh_male_liufei_uranus_bigtts`
- expressive 模型：`seed-tts-2.0-expressive`
- 参考音频：知微使用 `speech_rate=-10`，慎言使用 `speech_rate=0`；生成后统一转为单声道 16kHz WAV。

## 关键参数和限制

- `speech_rate` 文档范围为 `[-50, 100]`，`0` 为默认，`100` 约为 2 倍速，`-50` 约为 0.5 倍速。参考音频只建议小幅调整，当前女声使用 `-10`。
- `context_texts` 是语音指令/上下文控制参数，仅适用于支持该能力的豆包 2.0 原生或复刻音色；不能把“指定了复刻模型”和 `context_texts` 混用。
- `model`、`speaker`、`context_texts` 的组合必须按对应接口文档验证；当前 expressive 参考音频采用自然口语文本直接朗读，不依赖 `context_texts`。
- 语音指令可以控制情绪、语气、方言和语速，但指令文本不是情绪参考音频的替代品。当前已验证的做法是用含停顿、反问和犹豫的自然文本生成参考音频。
- 参考音频要保持单人、无 BGM/混响、结尾完整，且参考文本必须与音频内容一致；VoxCPM2 的 `prompt_text` 不匹配会降低克隆稳定性。

## 当前调用示例

```bash
.venv/bin/python projects/investment-research-video/scripts/tts-doubao-v3-ws-test.py \
  --episode projects/investment-research-video/outputs/companies/协鑫能科/2026-09-01/podcast/script/episode.json \
  --outdir /tmp/doubao-v3-test \
  --turns 4 \
  --model seed-tts-2.0-expressive
```

参考音频生成脚本：

```bash
.venv/bin/python projects/investment-research-video/scripts/generate-doubao-conversational-references.py
.venv/bin/python projects/investment-research-video/scripts/generate-doubao-surprised-references.py
```

## 常见失败和避坑

- V3 双向协议不是普通 JSON WebSocket：必须按二进制帧、事件号、压缩和会话 ID 处理，不能直接 `send(json)`。
- 服务端 `20000000`/完成事件和音频数据事件要分开处理；空 `data` 不等于失败。
- 将 `context_texts` 和不支持它的复刻模型组合，会导致参数不生效或请求失败。
- 参考音频默认语速过快时，VoxCPM2 往往也会偏快；先调参考音频，再在本地编排阶段处理整体节奏。
- `.env` 只保留本地凭证；Skill 文档只记录变量名和接口要求，不记录任何值。

## 原始文档

已归档在 `.ai/skills/doubao-tts/references/`：

- `豆包语音_双向流式语音合成WebSocket_1788516060.pdf`
- `豆包语音_单向流式语音合成WebSocket_1788353015.pdf`
- `豆包语音_单向流式语音合成HTTP_1788353015.pdf`
- `豆包语音_播客API-websocket-v3协议_1788257385.pdf`
- `豆包语音_语音指令与标签_1787233892.pdf`
- `豆包语音_音频生成HTTP_1787232315.pdf`
- `TTS Websocket Bidirection protocols.zip`

## 兼容旧版 HTTP 调用

`doubao-voice-ref.py` 仍可用于单段参考音频生成：

```bash
.venv/bin/python projects/investment-research-video/scripts/doubao-voice-ref.py \
  --voice zh_female_xiaohe_uranus_bigtts \
  --out /tmp/zhiwei-reference.wav
```

旧版脚本读取 `.env` 的 `VOLC_API_KEY`，并将 24kHz MP3 转成 16kHz 单声道 WAV。服务端 `20000000` 是正常事件，只有带 `data` 时才解码音频。

## 合规与凭证

火山引擎为商业服务，遵循其服务条款；本项目用于内部生产。`.env` 中的 `APP_ID`、`ACCESS_TOKEN`、`SECRET_KEY`、`VOLC_API_KEY` 等仅供本地调用，Skill 文档不保存值。

## 最佳实践

- 参考文本设计：覆盖自然陈述、数据强调、对比张力、疑问收尾；优先使用真人口语节奏，不要只写抽象的“请用怀疑语气”。
- 音色资产化：远程合成一次参考，保存到 `.ai/assets/voices/<speaker>/reference.wav`，同时更新对应 `ASSET.md` 和 `prompt` 文本；VoxCPM 本地克隆后不依赖豆包 API。
