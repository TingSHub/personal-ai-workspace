# Archive: Experiences（已归档经验）

经验反馈闭环的归档区：经验经「提炼 → 判定归属 → 回写 → 归档」闭环后存放于此。`.ai/experiences/` 仅存未完成回写的在途经验（当前为空，仅 `.gitkeep`）。

## 回写映射表

| 经验（by-name） | 回写目标 | 归档日期 |
|---|---|---|
| `research-master-content-pipeline` | `research-quality-gate` SKILL.md 注意事项（结论 4：吸收外部 Skill 方法约束而不强制其交付模板）；listed-company-research-video-production / listed-company-research-production workflow SOP（SRT/证据纪律 Quality Criteria 与 Known Issues，由 worker-1 在 P1.4 完成） | 2026-08-15 |
| `financial-analysis` | `tushare-connector` SKILL.md 注意事项（端点降级切换备用、倒序/重试）；`cninfo-connector` SKILL.md 注意事项（动态 orgId 优先、东财 search 非 JSON）；`marketpulse` SKILL.md 注意事项（无 AISA_API_KEY 降级）；listed-company-research-production SOP Phase1 Known Issues（worker-1） | 2026-08-15 |
| `financial-report-workflow` | `tushare-connector` SKILL.md 注意事项（重试、`.env` 注释独立成行）；listed-company-research-production SOP Phase1 Known Issues（worker-1） | 2026-08-15 |
| `industry-research-methodology` | `investagent` SKILL.md 注意事项（环境齐备才编排、无 Docker/LLM key 降级）；`industry-analysis` SKILL.md 注意事项（估值接入 tushare 真实分位）；listed-company-research-production SOP Phase2 Known Issues（worker-1） | 2026-08-15 |
| `tushare-proxy-cashflow-distortion` | `tushare-connector` SKILL.md 回写条目（代理现金流与法定披露交叉核验、弃用代理值） | 2026-08-15 |
| `investagent-module-runtime-issues` | `investagent` SKILL.md 回写条目（QuantDinger 镜像降级、yfinance A 股映射、FRED 诚实降级、UZI lite 档、记忆幻觉核实） | 2026-08-15 |
| `multi-search-total-failover` | `multi-search` SKILL.md 回写条目（三引擎全挂降级 WebSearch/WebFetch 直连） | 2026-08-15 |
| `huashu-test` | `finance-content-engineering` skill.yaml experience_refs + SKILL.md 来源说明（huashu 方法财经化重写） | 2026-08-15 |
| `content-director-validation` | `investor-understanding-architect`（优化依据：多视角提案/冲突保留/fact-map 约束有效；输出偏重与 visual brief 缺失待优化） | 2026-08-15 |
| `content-pipeline-reliability` | `research-intelligence-agent`（输出自检契约 + scripts/check_factmap.py）；`investor-understanding-architect`（visual-brief 引用约束 + scripts/check_disallowed.py）；`information-visualization-architect`（引用可解析性检查 + scripts/check_ev_refs.py） | 2026-08-15 |
| `doubao-tts-integration` | investagent-video-production workflow SOP P2（TTS 选型：edge-tts 优先/豆包 seed-tts-2.0 备选、生成模型不用于批量 TTS、两套 API 勿混） | 2026-08-17 |
| `audio-first-video-render` | investagent-video-production workflow SOP P3/P4（HyperFrames Audio-First、禁 xfade 链、抽帧同步验证） | 2026-08-17 |
| `investagent-research-only-scope` | `investagent` SKILL.md 回写条目（内容生产链路只跑研究+数据、跳过决策/回测、启动即限定范围）；investagent-html-report workflow SOP P1 Known Issues | 2026-08-16 |
| `multi-source-conflict-check` | investagent-html-report workflow SOP P2 Quality Criteria/Known Issues；`html-ppt-skill`（辅助脚本登记 check-numbers.py + 回写条目） | 2026-08-16 |
| `notes-spoken-polish` | `finance-content-engineering`（script-polish notes 应用 + scripts/check-fact-drift.py）；investagent-html-report SOP P3 | 2026-08-16 |
| `narration-content-lock` | `html-ppt-skill` 回写条目（notes 唯一 SoT/Content Lock）；investagent-html-report SOP P3 | 2026-08-16 |
| `presenter-notes-verification` | `static-html-qa`（scripts/check-notes-presenter.py）；`html-ppt-skill` 注意事项 | 2026-08-16 |
| `html-ppt-longform-report` | `html-ppt-skill` 回写条目（长文只取设计层、红涨绿跌、质检三件套）+ 辅助脚本登记（check-content-boundary.py / check-numbers.py / screenshot-fullpage.sh） | 2026-08-16 |
| `impeccable-detect-quality-gate` | `impeccable` 注意事项（detect 阈值与预防起点）+ 回写条目 | 2026-08-19 |
| `deck-qa-implementation-pitfalls` | `static-html-qa` 注意事项（transform scroll 虚报、notes 显式隐藏）+ 回写条目 | 2026-08-19 |
| `taste-skill-financial-editorial` | `taste-skill` 注意事项（金融 editorial 应用与边界）+ 辅助脚本登记（scripts/check-em-dash.py）+ 回写条目 | 2026-08-19 |

| `hyperframes-cli-runtime-contract` | investagent-video-by-hyperframes SOP Phase 4/5 Known Issues 回写条目（check 约定/clip class/字体/对比度/确定性验证）；hyperframes 资产记录注意事项 | 2026-08-20 |
| `video-pilot-media-degradation` | investagent-video-by-hyperframes SOP Phase 4 Known Issues 回写条目（TTS 降级路径/空行分段坑/时长裁决/Audio First 验证） | 2026-08-20 |
| `generic-video-visual-direction` | investagent-podcast-video-by-hyperframes SOP Phase 4/5 视觉质量门禁；hyperframes 资源记录经验引用（scene manifest/数据动效/开场 canary/非空结尾） | 2026-08-24 |
| podcast-audio-pacing-contract | investagent-podcast-video-by-hyperframes Phase 3；podcast-audio-compiler 节奏控制现状与复用路径（保留 VoxCPM2，补可执行语速/句内停顿字段） | 2026-08-24 |
| `company-intelligence-news-product-facts` | investagent-podcast-video-by-hyperframes Phase 1/1.5/2/4/5；multi-search；editorial-director-agent | 2026-08-27 |
| `podcast-editorial-gate-and-audio-render-regression` | investagent-podcast-video-by-hyperframes Phase 1.5/3/4/5；editorial-director-agent；podcast-audio-compiler；qwen3-forced-aligner | 2026-08-27 |
| `cosyvoice3-production-backend-selection` | investagent-podcast-video-by-hyperframes Phase 3；podcast-v1-luheng；podcast-audio-compiler | 2026-08-27 |
| `podcast-script-first-pauses` | investagent-podcast-video-by-hyperframes Phase 2/3/5；projects/investment-research-video/scripts/check_podcast_artifact_consistency.py | 2026-09-01 |

## 溯源说明

本表为溯源/导航信息，不构成执行契约；语义以对应 Workflow SOP 与 skill.yaml/agent.yaml 为准。经验文件保留完整原文，不修改、不删除；回写条目的正文编辑与合并由 Resource Manager 执行或复核（写回分区约定，M5）。
