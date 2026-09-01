# Experience: doubao-tts-integration

## 来源证据

- 项目：investment-research-html-mvp（2026-08-16，27 页 notes 豆包 TTS 全量合成，829.5s）
- 运行记录：`logs/run-20260816-workflow-v1.md`（TTS 链路）；脚本 `projects/investment-research-html-mvp/scripts/tts-doubao.py`
- 凭证：workspace 根 `.env` 的 VOLC_API_KEY（gitignore）

## 触发场景

- 中文旁白 TTS 批量合成（口播稿/notes → 音频）时
- 火山引擎语音技术/豆包 TTS 接入

## 问题与归属判定

- 问题：豆包 TTS 有**两套体系**容易混：①方舟 Ark（/api/v3/tts，Bearer token，模型 doubao-tts）——key 格式不匹配；②语音技术 Speech（openspeech.bytedance.com/api/v3/tts/create，**X-Api-Key header**）——控制台「快捷 API 接入」给的 key 是 UUID 格式。实测方舟拒绝 `api-key-日期` 格式 key；语音技术 v3 用 X-Api-Key + JSON body。
- 关键坑：**音色 ID（如 zh_male_liufei_uranus_bigtts）属于语音合成模型（bigtts 系列），需要单独开通**——只开通 seed-audio-1.0（音频生成模型）时传 voice_type 不报错但不保证生效，实际音色由 text_prompt 描述控制（"沉稳清晰的男声，用平实专业的财经解说语气朗读：..."）。
- 归属（owner）：investagent-html-report-v0.1 workflow SOP（P5 口播→视频阶段）

## 可复用结论（resolution）

- **TTS 选型结论（2026-08-17 最终验证）**：批量固定音色旁白优先 **edge-tts（Xiaoxiao +8%）**——音色统一、免费本地；豆包 seed-tts-2.0 作为高质量备选（需开通语音合成模型）；**音频生成模型（seed-audio）不用于批量 TTS**（每次采样音色随机）。

- **接入契约**：`POST https://openspeech.bytedance.com/api/v3/tts/create`，header `X-Api-Key`，body `{"model": "seed-audio-1.0", "text_prompt": "<音色描述>：<文本>", "audio_config": {"format": "mp3", "sample_rate": 48000}, "watermark": {}}`；响应 JSON 的 `audio` 字段是 **base64 编码的 mp3**。
- **免费额度**：新用户 2 万字符（本项目 27 页 ~4300 字，免费够用）；超出约 2-5 元/万字符。
- **音色策略**：seed-audio 描述式（可跑通）→ 需要精确音色 ID 时开通 bigtts 语音合成模型（改 --model + voice_type 生效）。
- **批量脚本**：tts-doubao.py（逐段合成 + 缓存命中 + ffprobe 时长 + concat 拼接 + SRT 派生）；**concat.txt 必须用绝对路径**（相对路径按 concat 文件目录解析会失败，实测 exit 254）。
- 音频时长 = 页级 SRT 的时间轴（Audio-First：音频驱动页面时长）。

## 回写目标

- investagent-html-report-v0.1 workflow SOP P5（TTS 接入契约 + 音色/模型开通区分 + 免费额度）

## 适用范围

- 中文旁白批量 TTS（火山语音技术 v3 体系）；seed-audio-1.0 及开通 bigtts 后

## 不适用范围

- 方舟 Ark 体系（不同鉴权/端点）；非火山 TTS（edge-tts/CosyVoice 走各自接入）

## 关联资产

- investagent-html-report-v0.1（Workflow by-name）；tts-doubao.py（项目脚本，随工作流定型后按资源边界登记）
