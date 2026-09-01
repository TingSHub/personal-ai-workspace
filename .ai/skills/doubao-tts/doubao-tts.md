# doubao-tts

> 管理资产：`.ai/skills/doubao-tts/doubao-tts.md`；辅助脚本：`projects/investment-research-video/scripts/doubao-voice-ref.py`、`tts-doubao.py`

## 元数据

| 字段 | 值 |
|---|---|
| name | doubao-tts |
| kind | skill |
| description | 豆包 TTS(火山引擎 seed-tts-2.0):专业音色合成——克隆参考源/批量配音 |
| source | 火山引擎(bytedance openspeech API)· 非开源服务 |
| installed_ref | seed-tts-2.0(API) |
| runtime | both |
| invocation | `python3 scripts/doubao-voice-ref.py --voice <音色ID> --out <wav>`(单段参考合成)/ `tts-doubao.py --notes <txt>`(批量) |
| requirements | VOLC_API_KEY(workspace 根 .env);网络可达 openspeech.bytedance.com |
| update | API 版本演进由火山引擎管理;脚本本地维护 |
| 辅助脚本 | `doubao-voice-ref.py`(克隆参考合成,单段)/ `tts-doubao.py`(批量配音,旧版 seed-audio) |
| 经验引用 | — |

## 作用

豆包 TTS 合成专业级中文语音。核心用途(本项目):**合成干净的克隆参考音频**——无 BGM/噪声/混响、结尾可控、音色 ID 可复现,是 VoxCPM 克隆的首选参考源(优于视频提取)。

## 调用

- 克隆参考合成:`doubao-voice-ref.py --voice zh_female_xiaohe_uranus_bigtts --out <wav>`;参考文本需覆盖多种情绪(陈述/数据强调/对比/疑问)且结尾干净完整句
- 已用音色:`zh_female_xiaohe_uranus_bigtts`(小禾,正式音色参考源);`zh_male_jieshuoxiaoming_uranus_bigtts`(小明,克隆有杂音已弃用)
- API 响应:`code 20000000` 为 OK 事件,音频在 data 字段(base64 mp3 块,NDJSON 流)

## 调用注意事项

- **data=None 判断**:code 20000000(OK)+ data 为空是流式事件(如会话开始),不是错误;只在有 data 时解 base64
- 输出 mp3 24kHz → 转 16kHz wav 作为克隆参考(脚本内处理)
- 商用红线:火山引擎为商业服务,遵循其服务条款;本项目用于内部生产

## 常见失败原因

- 把 20000000 OK 事件当错误退出(已修,见 doubao-voice-ref.py)
- 缺 VOLC_API_KEY → 从 .env 加载(脚本自动)

## 最佳实践

- 克隆参考文本设计:覆盖陈述/数据强调/对比张力/哲理/疑问收尾,结尾「欢迎…告诉我」类闭合句
- 音色资产化:合成一次参考,配方存 voices.md,VoxCPM 本地克隆后不依赖豆包 API
