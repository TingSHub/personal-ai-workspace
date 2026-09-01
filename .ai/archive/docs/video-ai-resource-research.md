# 高质量财经视频：外部资源调研报告

> 调研日期：2026-08-14
> 任务范围：纯资源发现与比较，不修改任何架构 / Workflow / Capability，不安装任何资源
> 目标形态：研究报告 → 动态 Web / Data Storytelling / Motion Graphics 视频（"随旁白播放的漂亮财经网页"→ MP4），无真人出镜，中文内容，未来可能公开发布与商业化
> 调研方式：9 个并行调研通道（内容策划 / 视觉导演+图表 / Remotion 深潜 / Remotion 之外路线 / 中文 TTS / 字幕 / 封面+审片 / 完整方案 / Agent 角色库），全部结论经 WebSearch/WebFetch 核实，数据截至 2026-08-14

---

## 0. 结论速览

1. **动态 Web 路线值得作为主路线**。当前存在两条成熟引擎主线：**HyperFrames**（HeyGen 开源，Apache-2.0 商业免费，40.9k stars，浏览器原生排版，且与本地 `codex-video-pipeline` 的 HyperFrames 渲染依赖**同栈**）与 **Remotion**（React 事实标准，字幕/TTS 官方一等公民，但 License 对 >3 人盈利组织收费）。建议 A/B 实测后二选一。
2. **不存在同时满足"中文 + 动态 Web + 数据叙事 + 可商用"的现成完整方案**（MoneyPrinterTurbo 中文最成熟但是素材拼贴型；html-video 形态最接近但只有 3 个月历史；DataMagic 概念最贴但 License 未声明）。**组合方案仍然必要**。
3. **中文 TTS 推荐策略：MiniMax Speech-02 与 Azure TTS 双主测 + CosyVoice 2/3 本地备份**。ChatTTS / Fish Speech / Spark-TTS / GPT-SoVITS 均因非商用 License 出局。数字→中文读法预处理（`cn2an`）是社区验证的标准实践。
4. **字幕走"已知文本强制对齐"路线**：Qwen3-ForcedAligner-0.6B（Apache-2.0，中文对齐精度公开实测最优 82ms 级），绕开 ASR 识别错误；渲染层用 `@remotion/captions` 逐词高亮，SRT 同源导出。
5. **内容编导与视觉导演（旁白→逐 Scene 视觉规格）两个方向外部没有成熟资源，需自研**；Agent 角色库（wshobson/agents + harness-100）可承担通用角色，视频流水线专用角色需自补。
6. **审片双通道**：Gemini API 视频输入（唯一能"看画面+听旁白"的托管通道）+ ffmpeg/PySceneDetect 抽帧 + Claude 高分辨率图片审查。**已核实：Claude API 当前不支持视频输入**。

---

## 1. 调研范围与方法

- 覆盖方向 1-9（内容策划、口播脚本、视觉导演、数据可视化、动态 Web 视频、中文 TTS、字幕、封面标题、审片）+ 完整解决方案 + Agent 角色库。
- 评价标准：实际效果优先于功能列表（找 demo/示例/用户证据）；维护活跃（12 个月内）；License 与商业使用查清；中文能力单独评估。
- 结论分档（不使用数字评分）：强烈建议实测 / 值得实测 / 暂时观察 / 不建议当前使用。

---

## 2. 本地现状盘点（只盘点，不 bias 推荐）

| 资产 | 状态 | 说明 |
|---|---|---|
| `content-production` capability + `research-content-producer` | ✅ 已实测 | 从冻结 RID 派生叙事策略/长脚本/5 短视频/估时 SRT/18 项素材规划，紫光股份案例质量门 0 阻断 |
| `media-production` capability + `video-production-executor` | ✅ 已实测 | 已产出 634 秒样片（ffmpeg blackdetect/freezedetect 无异常），但视觉层是 Pillow 静态图+简单运动，**质量门 PASS WITH WARNINGS，接近 PPT 翻页风险** |
| `video-quality-reviewer` + `research-quality-gate` | ✅ 已实测 | 只读验收；内容层门禁（证据/数字一致性/禁语/SRT 合法性）强，成片层弱 |
| `codex-video-pipeline`（外装 skill，reference） | ⚠️ 未实跑 | 完整链路方法论（研究→脚本→动态叙事→素材→旁白→声学字幕→**HyperFrames 渲染**→质检→封面→发布包），`setup.py doctor` 显示 HyperFrames 与配置未就绪，成片从未实跑 |
| TTS | ⚠️ 原型级 | 样片用 Google Translate TTS 端点，文档自评"公开发布许可需复核，正式发布替换为明确授权的声音提供方" |
| 字幕 | ⚠️ 估时稿 | estimated SRT 已生成；声学对齐（Whisper/sherpa-onnx）列为增强项但本机不可用 |
| 项目级评估文档 | 已有 | `projects/investment-research-system/docs/video-production-resource-evaluations.md`、`video-content-resource-evaluations.md`（2026-08-13），skill-hub 返回 0 候选、find-skills 当时网络失败 |

**本次调研的核心增量**：动态 Web 渲染引擎、商用中文 TTS、声学对齐字幕、多模态审片——正是上述链路的缺口。

---

## 3. 分方向候选明细

### 3.1 内容策划 / 财经口播脚本（方向 1+2）

**核心结论：外部没有真正成熟的"财经编导"专门资源**（主题选择、预期差、多空冲突、研报数据取舍必须自研）；可借鉴的是通用视频"包装方法论"与中文原生流水线。

| 候选 | 来源 | 维护 | 要点 | 下一步 |
|---|---|---|---|---|
| chenyuxiaojin/video-agent-skills | github.com/chenyuxiaojin/video-agent-skills | 活跃（单人，7 stars） | **中文原生** 11-skill 流水线：researcher organize 模式（素材→叙事大纲）、writer（280 字/分中文口播、三种开场模式）、producer（4 个人工检查点）、voice（MiniMax）、jianying-editor | 强烈建议实测 |
| digitalsamba/claude-code-video-toolkit | github.com/digitalsamba/claude-code-video-toolkit | 极活跃（1936 stars，近日更） | 无真人/数据叙事形态全流水线（planning→audio→editing→rendering），demo 含动态图表；脚本环节偏薄（只写 markdown） | 强烈建议实测（流水线骨架） |
| AgriciDaniel/claude-youtube | github.com/AgriciDaniel/claude-youtube | 活跃（312 stars，MIT） | YouTube 增长顾问：strategy/hook（5 种变体+掉粉风险）/thumbnail/script/SEO，留存工程化 | 值得实测（蒸馏 hook 方法论） |
| buda-ai/bunny-agent 内嵌 videodrone script-writer | github.com/buda-ai/bunny-agent（templates/videodrone-agent/…/script-writer） | 极活跃，Apache-2.0 | 大纲→逐字口播稿：`[Tone]/[Emphasis]/[Pause]` 交付提示 + `[VISUAL]/[TEXT OVERLAY]/[GRAPHIC]` 视觉提示 + 13 项质量自检 | 值得实测（交付/视觉提示规范直接衔接 storyboard） |
| CK42BB/vox-explainer-skill | github.com/CK42BB/vox-explainer-skill | 活跃（87 stars，MIT） | Vox 式节拍旁白：每节拍一个观点、8-14 秒口播、结构化 script.json | 值得实测（节奏方法论） |
| AlterLab-FC-Skills（video-essay） | github.com/AlterLab-IEU/AlterLab-FC-Skills | 一般（9 stars，MIT） | 长视频旁白工程：Argument Map、时长预算表（10 分钟≈1200-1400 字+2-3 分钟纯画面）、[PAUSE]/[ON-SCREEN TEXT] 标记 | 暂时观察（蒸馏框架） |
| CreatorSkills（商业市场） | creatorskills.co | 活跃 | 付费爆款 hook/脚本 skill（$7-19），17 个免费包 | 值得实测（只测免费包） |
| OpenClaw「蝦說財報」频道案例 | harrychang.cc/blog/ai-002-openclaw-automation | N/A（文章） | 中文财经全自动频道实战：narration.json 带 slide 引用 → HTML 幻灯片 → 截图 → TTS → Whisper 校验 → ffmpeg | 暂时观察（设计参考） |

**方向小结**：以 `video-agent-skills` 为骨架（中文节奏 + organize 模式），蒸馏 `claude-youtube` 的 hook/留存框架与 `bunny-agent` 的交付/视觉提示规范，自研 Content Director + 口播脚本（挂到现有 Capability 下）。财经正确性由现有研究质量门禁兜底。

### 3.2 视觉导演 / 数据可视化（方向 3+4）

**核心结论：外部没有"旁白→网页动效视频逐 Scene 视觉规格"的成熟资源**（现存分镜工具全部面向 AI 生成视频或手绘）；**图表方案成熟**，组合原则是"库管结构与首帧静态质量，渲染引擎管帧插值与大数字动画，禁用库内置计时动画"。

| 候选 | 来源 | 维护 | 要点 | 下一步 |
|---|---|---|---|---|
| hyv-storyboard（HearYourVOICE 插件） | github.com/killernay/HearYourVOICE | 活跃（136 stars，MIT） | 旁白→逐镜头视觉计划（取景/镜头运动/屏幕文字/情绪基调/素材建议），最贴近需求的 Schema | 值得实测（抽取 Schema） |
| PenShot | github.com/neopen/story-shot-agent | 活跃（139 stars，MIT） | 剧本→镜头级切分+时长规划，输出 AI 视频提示词；思路可借鉴，产物形态不兼容 | 值得实测（方法论） |
| **Apache ECharts** | echarts.apache.org | 极活跃（66.8k stars，v6 于 2025-07） | 财务图表主力：图表类型最全、**中文一等公民**、SSR SVG 逐帧渲染（v5.3.0+）、Apache-2.0；内置动画是计时型，需关闭后手动插值 | 强烈建议实测 |
| TradingView lightweight-charts | github.com/tradingview/lightweight-charts | 活跃（16.7k stars，v5.2） | 金融原生（K线/区间/收益率曲线/多面板），Apache-2.0（须保留署名），无逐帧接口需自写插值 | 值得实测 |
| Observable Plot | github.com/observablehq/plot | 偏慢（近 12 个月无 release） | D3 作者声明式 SVG，排版默认值公认最优，无内置动画（正合逐帧驱动）；ISC | 值得实测 |
| D3.js（+d3-annotation） | github.com/d3/d3 | 极活跃 | 高定制财务形态（估值区间带/产业链分层/Bull-Bear 标注）兜底层 | 强烈建议实测（D3）；d3-annotation 暂时观察（无人维护） |
| GSAP | gsap.com | 活跃（Webflow 收购后全插件免费） | 大数字/文字逐字动画、SVG 变形、时间线；表现层最强；闭源但商用免费 | 值得实测 |
| Flourish | flourish.studio | 活跃（Canva 旗下） | **视觉基准参考**：bar chart race/市占率流动/对比卡模板几乎就是目标画面类型；视频导出需 Enterprise（~$5k/年），不做生产工具 | 暂时观察（强烈建议看其模板） |
| Datawrapper | datawrapper.de | 活跃 | 新闻图表排版规范参考；无动画 | 不建议当前使用（仅设计规范） |
| Recharts / Chart.js | — | 活跃（MIT） | 逐帧驱动会闪烁；Chart.js 是 Canvas 非 SVG | 暂时观察 |
| LayerChart | github.com/techniq/layerchart | 活跃（MIT） | 数据故事化组件细致但绑 Svelte 栈 | 暂时观察 |

### 3.3 Remotion 专项（方向 5，核心）

**总体判断：高度契合主路线**。Remotion 本质就是"React 网页 → 逐帧视频"，与目标形态天然一致；56.3k stars、v4.0.509（2026-08-12，近乎每日发版）、300+ contributors。官方为 Agent 时代重写了 10+ 官方 Skills，直接缓解"LLM 写 Remotion 幻觉多"的社区痛点。

- **License（关键）**：非 OSI 开源。个人与 **≤3 人盈利组织免费且输出视频可商用**；4+ 人盈利组织需 Company License（Creators $25/座/月 或 Automators $0.01/渲染+$100/月最低）；v5.0 预告（Automators 强制 telemetry）。**按商业化主体规模核对**。
- **字幕/TTS**：`@remotion/captions`（MIT 包）word 级 + TikTok 式分组 + SRT 导入导出；Animated Captions 3 种卡拉OK逐词高亮组件（支持 CJK）；官方 ElevenLabs/Whisper 系列包（`@remotion/elevenlabs`、`@remotion/openai-whisper`、`@remotion/install-whisper-cpp`）。
- **渲染**：本地并发渲染；Lambda 分布式（官方实测 1 分钟 1080p ≈ $0.017，18.9s）；无 GPU（Canvas/WebGL 图表慢）；仅 sRGB。
- **中文**：Google Fonts Noto Sans SC、Lambda CJK 字体层；中文社区实测多。
- **未验证项**：ECharts 直连渲染、中文逐词卡拉OK观感、VTT 直接导入（需先转 SRT）。
- **局限**：React 学习曲线同类最高；包体积数百 MB；本地渲染偏慢。

| 周边资源 | 来源 | 要点 | 下一步 |
|---|---|---|---|
| remotion-dev/skills（官方技能包） | remotion.dev/docs/ai/skills | `/remotion-create`、`/remotion-captions`、`/remotion-markup` 等 10+，内置 charts/subtitles/voiceover 规则文档，Claude Code/Codex 直接安装 | 强烈建议实测 |
| @remotion/captions + Animated Captions | remotion.dev/docs/captions | 逐词高亮卡拉OK、TikTok 式分组、SRT 同源导出；中文按标点分组需自写 | 强烈建议实测 |
| reactvideoeditor/remotion-templates | github.com/reactvideoeditor/remotion-templates | 81 免费模板，Charts & Data 类 9 个（大数字滚动/图表生长/对比卡/环形进度） | 值得实测 |
| 官方 TTS 集成（ElevenLabs/Whisper 包） | remotion.dev/docs/elevenlabs | TTS MP3 → getAudioDuration → Whisper 词级时间戳 → 卡拉OK字幕，社区完整链路可参考 | 强烈建议实测 |
| 社区 Remotion MCP | 多个 | remotion-media-mcp、@instavar/mcp-server 等；个人维护，核心仍走 Remotion 本体 | 暂时观察 |
| openclaw-investor-relations-manager | npmjs.com/package/openclaw-investor-relations-manager | 财报→中文视频参考实现（营收/增长场景检测、KPI 圆环） | 暂时观察（架构参考） |

### 3.4 Remotion 之外路线（方向 5，核心发现）

| 候选 | 来源 | 维护 | 要点 | 下一步 |
|---|---|---|---|---|
| **HyperFrames** | github.com/heygen-com/hyperframes（hyperframes.dev） | 极活跃（**40.9k stars**，2026 年内从 ~2 万暴涨） | **"Write HTML. Render video. Built for agents."** HTML/CSS + 可 seek 动画（GSAP/CSS/Lottie/Anime.js）→ headless Chrome 逐帧 + FFmpeg → MP4；原生 `<audio>` 时间轴混流；**20 个官方 Agent skills**（kinetic captions/字幕/TTS/data-chart）；Apache-2.0 商业免费、输出无限制；浏览器原生排版（中文换行/标点自然生效）；**与本地 codex-video-pipeline 的 HyperFrames 渲染依赖同栈** | 强烈建议实测（**第一备选**） |
| html-video | github.com/nexu-io/html-video | 活跃但仅 3 个月（4.3k stars，Apache-2.0） | HTML→MP4 + agent 编排：21 个动画模板（含 NYT 风格数据叙事）、Hyperframes 引擎、MiniMax TTS 旁白+BGM ducking、中文 README、内容-graph 分镜编排 | 强烈建议实测 |
| Shotstack（html5 asset） | shotstack.io | 活跃（SaaS） | 云渲染兜底：可 seek HTML5 页面 → MP4，PAYG ~$0.30/min；限制：canvas 不捕获、须 SVG/DOM、字体须 TTF 直链 | 值得实测（免费沙箱先跑中文样片） |
| Revideo | github.com/redotvideo/revideo | 刚恢复活跃（4.0k stars，MIT） | Motion Canvas 工程化分支：TSX 场景 + renderVideo API + React Player，可部署渲染服务 | 值得实测（备选） |
| Motion Canvas | github.com/motion-canvas/motion-canvas | **停滞**（官网 NXDOMAIN，18.9k stars） | Canvas 矢量动画（Manim 的 TS 版）；基于 Canvas 而非 DOM → 中文财务排版成本高 | 不建议当前使用 |
| Canvas Commons（社区分支） | github.com/canvas-commons/canvas-commons | 活跃（221 stars） | Motion Canvas 接棒者，规模小 | 暂时观察 |
| Creatomate | creatomate.com | 活跃（SaaS） | 模板化批量（可视化编辑器模型，非自由 HTML 页面），~$0.2-0.9/min | 暂时观察 |
| Puppeteer/Playwright 录制系 | — | — | 丢帧/码率/格式硬伤（Playwright 内置硬编码 VP8 1Mbps），仅限样片 | 不建议当前使用（自研重复造轮子） |
| GSAP 时间线+录制自研 | — | — | 技术上可行，估 2-4 周工程量，已被 HyperFrames/Shotstack 封装覆盖 | 不建议当前使用 |

**方向小结**：Remotion 之外最值得备选的路线是 **HyperFrames**（Apache-2.0、浏览器原生排版、Agent 原生 skills、与本地链路同栈）；云渲染兜底用 Shotstack html5 asset。Canvas 系因停滞与中文排版短板降级。

### 3.5 中文 TTS（方向 6，高风险点）

**推荐策略：MiniMax + Azure 双主测，CosyVoice 本地备份；数字/缩写问题由前端预处理统一兜底（`cn2an` 是社区验证的标准实践，英文缩写无统一方案须逐模型实测）。**

| 候选 | 类型 | 关键事实 | 下一步 |
|---|---|---|---|
| **MiniMax Speech-02** | API | 中文自然度第一梯队（WER 2.25%）、情绪参数、文本内停顿标记；**异步长文本单次最高 100 万字符**（直接解决 10 分钟+旁白）；约 700 元/百万汉字；**数字读法有已知问题（1,234 类错读）需 normalize/预处理** | 强烈建议实测 |
| **Azure TTS** | API | **商用许可最清晰**、SSML 最完善（break/prosody/phoneme/sub alias）、微软工业级数字处理、zh-CN 音色几十个；约 $15-16/百万字符，免费层 12 个月 50 万字符/月；英文缩写需 sub alias 手动映射 | 强烈建议实测 |
| **CosyVoice 2/3** | 开源本地 | **唯一 License 干净（Apache-2.0）可商用的本地主流方案**；零样本克隆、流式、中文 WER 2.43%；**官方建议单次 10-200 字，长旁白必须自建分段拼接管线**；GPU 4GB 起（0.5B） | 强烈建议实测（本地备份） |
| 火山引擎 豆包 TTS | API | 中文自然度 2025 国产榜单登顶；风格锚点+质量自检专治长文分段音色漂移；**语音大模型版仅对企业认证开放**；约 225-650 元/百万字符 | 值得实测（需企业账号） |
| 讯飞 TTS | API | 老牌标杆；**中英混读自动处理是官方卖点**（AI/ROE 类缩写，需自测）；约 2 元/万字符 | 值得实测（对照组） |
| Edge TTS | 免费工具 | 40+ 中文音色（与 Azure 同源）、SSML 完善、零成本；**非官方接口商用许可模糊，维护者不建议商用**；GPLv3 代码 | 值得实测（**限内部试音**） |
| IndexTTS2 | 开源本地 | 中文自然度开源第一梯队；**文本内拼音标注可精确控制多音字/英文缩写**；**bilibili 自定义 ULA**（<1 亿 MAU 且年收入<10 亿可免费商用，金融场景条款需法务确认） | 值得实测（商用前邮件确认） |
| Kokoro | 开源本地 | 82M 极轻量纯 CPU；Apache-2.0；中文质量两极、**中英混读差（官方 Issue #238）** | 值得实测（限试音） |
| ChatTTS / Fish Speech / Spark-TTS | 开源本地 | **权重均为 CC BY-NC 系列，禁止商用**；预处理实践值得抄 | 不建议当前使用 |
| ElevenLabs | API | 中文非强项（自然度 7.8/10）+ UTF-8 计费约为英文 3 倍 | 暂时观察 |
| GPT-SoVITS | 开源本地 | 克隆定位+声音权属风险，不适合旁白主链路 | 暂时观察 |

### 3.6 字幕与时间轴（方向 7）

**核心结论：本项目旁白文本已知（研报→脚本→TTS），走"已知文本强制对齐"路线，架构上绕开 ASR 识别错误。**

| 候选 | 来源 | 关键事实 | 下一步 |
|---|---|---|---|
| **Qwen3-ForcedAligner-0.6B** | huggingface.co/Qwen/Qwen3-ForcedAligner-0.6B | 已知文本+音频→**字级**时间戳；中文对齐精度公开实测最优（82ms vs WhisperX 135ms）；Apache-2.0；单次 ~270s，alignLong 更长 | 强烈建议实测（**本方向首选**） |
| faster-whisper（v3-turbo） | github.com/SYSTRAN/faster-whisper | MIT；自转录一体；TTS 音频无噪声，v3-turbo 精度损失可忽略（快 3.4 倍）；中文词边界错误 10-15%、有长静音时间戳漂移缺陷 | 强烈建议实测（对照） |
| WhisperX | github.com/m-bain/whisperX | BSD-2；中文对齐弱于专用对齐器；**有回归史（v3.3.3-3.8.1 时间戳错位），必须用 v3.8.2+** | 值得实测（仅基线） |
| stable-ts | github.com/jianfch/stable-ts | MIT；断句/多格式导出（SRT/ASS 卡拉OK）最强；**已归档（2026-05 只读）** | 值得实测（只移植逻辑） |
| @remotion/captions | remotion.dev/docs/captions | **字幕即画面 DOM 的官方成熟方案**：word 级、逐词高亮、TikTok 式分页、SRT 导出；中文按标点分组需自写 | 强烈建议实测 |
| Capicola | github.com/michaelandrewgamble/capicola | MIT；TikTok/CapCut 风格逐词高亮 React 组件，自研参考实现 | 值得实测（读源码） |
| MFA / aeneas / whisper-timestamped / AutoCaptions | — | MFA 太重；aeneas AGPL+官方不支持中文；whisper-timestamped License 不明；AutoCaptions 输出 Premiere XML 错位 | 不建议当前使用（MFA 作精度对照可观察） |

**推荐流水线**：TTS 音频 + 脚本文本 → Qwen3-ForcedAligner（主力）/ faster-whisper（对照）→ word-level JSON → `@remotion/captions` 逐词高亮画进画面 → SRT/VTT **同源导出**；中文按 `。，？！` 分组层必须自写。

### 3.7 封面标题 + 多模态审片（方向 8+9）

**审片核心结论：Claude API 官方文档确认不支持视频输入（仅图片，单请求最高 600 张），因此审片必须走"双通道"——Gemini 喂 MP4（能听音频）+ Claude 抽帧高分辨率审查（图表可读性）。**

| 候选 | 类型 | 关键事实 | 下一步 |
|---|---|---|---|
| **Gemini API 视频输入** | API | 唯一"整个 MP4 + 音轨"托管通道（2M 上下文≈2 小时视频、时间戳问答）；覆盖配音自然度/前30秒/长时间无视觉变化（抽帧方案无法覆盖的维度） | 强烈建议实测 |
| Claude API 图片审查（抽帧） | API | 官方不支持视频；单请求 100-600 张图、高分辨率 2576px（图表可读性审查强于 Gemini 默认 1fps 采样） | 强烈建议实测 |
| video-research-mcp | github.com/Galbaz1/video-research-mcp | Claude Code 现成审片 MCP（51 工具，Gemini 3.5 Flash 驱动 + ffmpeg 抽帧）；无财经审片清单需自写 | 强烈建议实测（底座） |
| PySceneDetect | github.com/Breakthrough/PySceneDetect | 场景间隔硬指标（>30s 无切换→警告；前 30 秒场景数）；本地毫秒级 | 强烈建议实测 |
| llm-frames | github.com/john-ver/llm-frames | 抽帧拼网格图+时间戳 XML 喂 LLM（省 token）；单帧细节被压缩，不适合图表可读性维度 | 值得实测 |
| VideoDB benchmark-vlms | labs.videodb.io | 审片配置验证方法论（采样密度×模型×提示词×分辨率） | 值得实测（仅方法论） |
| Qwen3-VL（8B） | 开源 | 本地视频理解备选（8-10GB 显存，数据不出境）；研究性质 | 暂时观察 |
| NanoThumbnail | github.com/yoanbernabeu/NanoThumbnail | MIT+BYOK 封面生成（Replicate/Gemini），商业化合规友好；只管画面不管文案事实 | 值得实测 |
| cover-and-copy | 中文封面 Skill | 唯一逐行核实过内容的中文封面技能：构图纪律+红线（禁假 Logo/不夸大）；面向真人出镜需改造 | 暂时观察（取约束结构） |
| CTR 导向生成器（各 YouTube thumbnail agent） | — | 普遍默认夸大倾向，与"封面主张必须能被研报支撑"红线冲突 | 不建议当前使用 |

**红线执行建议**：把红线写进封面/标题质量契约（"标题与封面出现的任何数字、结论必须能在研报中找到原文支撑，否则拒绝生成"），不依赖工具自觉；审片清单里"是否曲解研究事实"须做"研报↔脚本↔旁白转写"三向文本比对，不能让 VLM 凭视觉自评。

### 3.8 完整解决方案（方向四）

**核心结论：没有现成完整方案同时满足"中文 + 动态 Web 渲染 + 数据叙事 + 可商用"→ 组合方案必要。**

| 候选 | 来源 | 关键事实 | 下一步 |
|---|---|---|---|
| **html-video**（nexu-io） | github.com/nexu-io/html-video | 见 3.4；唯一"真实 HTML 动画→MP4"完整编排（含 TTS/字幕/混音），与目标同构；项目太新 | 强烈建议实测 |
| **DataMagic**（HKUST） | github.com/HKUSTDial/DataMagic | 数据→中文叙事视频端到端（VLDB 2026），DVSpec 把视觉元素/数字绑定回数据字段（可核查，契合研报数字硬要求）；**未声明 License**、源码逐步开源、TTS 未披露 | 强烈建议实测（先体验 datamagic.chat 在线 demo，商用前确认授权） |
| MoneyPrinterTurbo | github.com/harry0703/MoneyPrinterTurbo | 103.4k stars、MIT、中文生态事实标准；成片是**素材拼贴型**（无排版/图表动画），画面与数据脱节；6 个已知 CVE | 值得实测（只借阶段划分与 TTS/字幕衔接） |
| VideoLingo | github.com/Huanshere/VideoLingo | 18.1k stars、Apache-2.0；**字幕+配音工程开源最佳**（WhisperX 词级对齐、Netflix 级单行字幕、术语表、断点续跑）；不做画面 | 值得实测（提取对齐/断句/术语表机制） |
| VStory（VisActor） | github.com/VisActor/VStory | MIT；VChart/VGrammar 系叙事可视化组件（图表动画层），不产 MP4 | 值得实测（图表组件） |
| ShortGPT | github.com/RayVentura/ShortGPT | 停滞 18 个月，素材拼贴型 | 暂时观察 |
| short-video-maker | github.com/gyoridavid/short-video-maker | Remotion 程序化合成+MCP，但**仅英语配音** | 暂时观察（架构参考） |
| ai-video-maker（ydssx） | github.com/ydssx/ai-video-maker | 0 stars 无成片证据 | 不建议当前使用 |

### 3.9 Agent 角色库（方向五）

| 候选 | 来源 | 关键事实 | 下一步 |
|---|---|---|---|
| **wshobson/agents（SuperClaude）** | github.com/wshobson/agents | 38.8k stars、MIT、94 插件/203 agents/175 skills；Claude Code+Codex 双 harness；**agent 即单 .md 可独立提取**；**无任何视频类角色**（内容角色为营销通才） | 强烈建议实测（主 Agent 来源候选） |
| **revfactory/harness-100** | github.com/revfactory/harness-100 | 100 个生产级 harness；**01-youtube-production 含 scriptwriter + content-strategist + thumbnail-designer + production-reviewer**（唯一带 Reviewer 的现成角色团队）；韩/英双语，Apache-2.0，`cp -r` 即提取 | 强烈建议实测 |
| anthropics/skills | github.com/anthropics/skills | 官方 169k stars；Skill 格式事实标准；**无视频/口播技能**；docx/pptx 可支撑分镜/脚本文档产出 | 值得实测（格式基准） |
| chenyuxiaojin/video-agent-skills | 见 3.1 | 中文视频流水线参考实现 | 值得实测（按环节提取） |
| rshah515/claude-code-subagents | github.com/rshah515/claude-code-subagents | 165 agents，维护趋停滞 | 暂时观察 |
| hesreallyhim 系列 | github.com/hesreallyhim | 社区清单索引（无 License 风险注意） | 暂时观察（发现渠道） |

**角色覆盖矩阵**（9 个目标角色 × 主要库）：

| 目标角色 | wshobson/agents | harness-100 | video-agent-skills | 结论 |
|---|---|---|---|---|
| Content Director | ✗（content-marketer 近似） | ~（content-strategist） | ~（producer 兼总导演） | 无精确角色，需自补 |
| Creative Director | ✗ | ✗ | ✗ | **全面缺失** |
| Financial Analyst | ~（偏交易） | ~（investor-report harness） | ✗ | 用本地 deep-analysis 等内部资源 |
| Video Script Writer | ✗ | ✓ | ✓ | 可覆盖 ✓ |
| Storyboard Artist | ✗ | ~ | ✓ | 可覆盖 ✓ |
| Motion Designer | ✗ | ✗ | ✗ | **全面缺失，需自补** |
| Video Producer | ✗ | ~ | ✓ | 可覆盖 ✓ |
| YouTube Strategist | ~（SEO 向） | ~ | ~（抖音向） | 半覆盖需改造 |
| Reviewer | ✗ | ✓ | ✗ | harness-100 可覆盖 ✓ |

**附带发现：5 个视频/TTS/字幕相关 MCP**：`video-studio-mcp`（ElevenLabs→Remotion→MP4+QA 帧）、`studiomeyer-io/mcp-video`（FFmpeg+Playwright，SRT 烧录/Whisper 字幕/TTS）、`stephengpope/remotion-media-mcp`、`samuelgursky/davinci-resolve-mcp`、`avotsai/avots-mcp`。

---

## 4. A. 最值得测试的 20 个资源（按用途分组）

### 组 1：Web 视频引擎（核心决策，先测这两组）

#### 1. HyperFrames（heygen-com/hyperframes）
- 类型: GitHub Project / 渲染引擎（开源）
- 来源: github.com/heygen-com/hyperframes（文档 hyperframes.dev，npm 包 `hyperframes`）
- 最近维护: 极活跃（40.9k stars，2026 年内从 ~2 万快速上涨；官方 demo 视频确认为 Claude Code 生成）
- 主要能力: HTML/CSS + 可 seek 动画（GSAP/CSS/Lottie/Anime.js）→ headless Chrome 逐帧 + FFmpeg → MP4；同一文件浏览器实时预览即视频预览；原生 `<audio>` 时间轴混流；20 个官方 Agent skills（kinetic captions/字幕/TTS/data-chart），Claude Code/Codex/Cursor 一键安装
- 为什么值得关注: 与"随旁白播放的漂亮财经网页"是同一设计哲学——**网页即成片，无构建步骤、无专有 DSL**；Apache-2.0 商业免费、输出无限制；确定性渲染适合流水线回归；HeyGen 生产在用；**与本地 `codex-video-pipeline` 的 HyperFrames 渲染依赖同栈，升级本地链路成本最低**；浏览器原生排版，中文换行/标点自然生效
- 局限: 项目较新、生态小于 Remotion；单机渲染为主（分布式栈成熟度低于 Remotion Lambda）；HTML 输入未沙箱化有执行风险；中文/CJK 未文档明示（机制上走真实浏览器，需实测）
- 适合阶段: Web Video（HTML→MP4 确定性渲染）
- 与项目匹配: 财务网页视频（大数字/图表/时间线/对比卡片/中文旁白字幕）是它的典型用例；**第一备选**
- 推荐下一步: **强烈建议实测**（中文长文本排版+图表+音轨混流各跑一条 30-60 秒样片）

#### 2. Remotion + 官方 Agent Skills（remotion-dev/skills）
- 类型: Framework + 官方 Skill 包
- 来源: remotion.dev；github.com/remotion-dev/remotion（skills 在 packages/skills）
- 最近维护: 极活跃（56.3k stars，v4.0.509，近乎每日发版）
- 主要能力: React 写"网页"→ 逐帧 MP4；useCurrentFrame/interpolate/spring 确定性逐帧；官方 charts 规则（禁第三方动画、帧号驱动）；`@remotion/captions` 逐词高亮卡拉OK + SRT 导入导出；官方 ElevenLabs/Whisper 集成包；10+ 官方 Agent Skills 直接给 Claude/Codex 用
- 为什么值得关注: 动态 Web 视频**事实标准**；官方为 Agent 时代重写技能体系，直接解决"LLM 写 Remotion 幻觉多"的痛点；81 个社区免费模板（大数字滚动/图表生长/对比卡）；渲染成本官方实测 1 分钟 1080p ≈ $0.017（Lambda）
- 局限: **License 非 OSI 开源**：≤3 人盈利组织免费+输出可商用，4+ 人需 Company License（$25/座/月 或 $0.01/渲染+$100/月最低）；React 学习曲线最高；包体积数百 MB；本地渲染慢；ECharts 直连与中文卡拉OK观感未验证
- 适合阶段: Web Video + Caption
- 与项目匹配: 与 HyperFrames 并列为主线候选，A/B 实测后二选一（或按场景混用）
- 推荐下一步: **强烈建议实测**（官方 skills 起手，重点验证中文逐词字幕观感）

#### 3. html-video（nexu-io）
- 类型: GitHub Project / 完整编排（渲染引擎上层）
- 来源: github.com/nexu-io/html-video
- 最近维护: 活跃但仅 3 个月（4.3k stars，Apache-2.0）
- 主要能力: 编码 agent 把 HTML/CSS/数据变 MP4：21 个动画模板（含 NYT 风格数据叙事折线图）、content-graph 分镜编排、Hyperframes 引擎录制、MiniMax TTS 旁白+BGM ducking 混音；支持粘贴文章 URL；CLI + 本地 Studio
- 为什么值得关注: 目前唯一主流开源"真实排版+CSS/GSAP 动画+数据图表→成片"完整编排，与目标**同构**；中文 README+中文示例；Apache-2.0 无按量收费；与 HyperFrames 引擎同源（若选 HyperFrames 路线可叠加）
- 局限: 项目太新、生态未沉淀；依赖编码 agent + Node/Playwright 环境；MiniMax TTS 中文支持需实测；金融图表模板需自写
- 适合阶段: Web Video（编排层）+ 完整方案
- 与项目匹配: 最快跑通"网页→成片"完整链路的候选
- 推荐下一步: **强烈建议实测**（先跑通 60-90 秒中文样片）

### 组 2：图表与视觉组件

#### 4. Apache ECharts
- 类型: Library（Apache-2.0）
- 来源: echarts.apache.org；github.com/apache/echarts
- 最近维护: 极活跃（66.8k stars，v6.0.0 于 2025-07-30）
- 主要能力: 图表类型最全（趋势/柱/饼/桑基/热力/瀑布/时间线）+ 内置初始动画、dataZoom、SVG/Canvas 双渲染器、**SSR SVG 渲染（v5.3.0+）可服务端逐帧出图**、按需加载
- 为什么值得关注: **中文一等公民**（中文标签/数字格式/字体适配最成熟），A 股财经媒体生态大量使用；Apache-2.0 商用无忧；覆盖营收/毛利/ROE/市占率/估值区间/产业链全套需求
- 局限: 内置动画是计时型非帧索引型（GitHub Issue #20234 开放请求）——逐帧驱动须关闭内置动画手动插值，或 SSR 逐帧+后期合成；大数字动画需自建计数组件
- 适合阶段: Web Video（图表部分主力）
- 与项目匹配: 财务图表主力，与渲染引擎"库管结构、引擎管帧"原则吻合
- 推荐下一步: **强烈建议实测**

#### 5. TradingView lightweight-charts
- 类型: Library（Apache-2.0，须保留署名）
- 来源: github.com/tradingview/lightweight-charts
- 最近维护: 活跃（16.7k stars，v5.2）
- 主要能力: 金融原生（K线/折线/面积/基线/多面板/收益率曲线/价格线标注），轻量 ~35kB
- 为什么值得关注: 股价走势/估值区间/涨跌对比/收益率曲线开箱即用，与 ECharts 互补
- 局限: 无饼图/桑基等通用图表；Canvas 命令式 API 无逐帧接口，进视频需自写数据切片插值
- 适合阶段: Web Video（行情/估值类场景）
- 与项目匹配: 用于"估值分位、Bull/Bear 区间"等金融原生画面
- 推荐下一步: **值得实测**

#### 6. Observable Plot
- 类型: Library（ISC）
- 来源: github.com/observablehq/plot
- 最近维护: 偏慢（近 12 个月无 release）
- 主要能力: D3 作者 Bostock 的声明式 SVG 绘图，默认排版质量公认最优
- 为什么值得关注: 纯 SVG 输出可与逐帧插值天然配合（每帧按数据切片重算）；LLM 生成 Plot 代码已有可靠先例；"数据故事化"编辑感最强
- 局限: 无内置动画 API（官方策略"结构由 Plot、动画由外部驱动"——正合逐帧思路但需自建）；维护放缓；蜡烛/区间等高级财务形态需自定义 mark
- 适合阶段: Web Video（高定制编辑感图表）
- 与项目匹配: 适合"干净、编辑感强"的财经图表，代码量远小于裸 D3
- 推荐下一步: **值得实测**

#### 7. GSAP
- 类型: Library（商用免费，闭源）
- 来源: gsap.com
- 最近维护: 活跃（Webflow 收购后全插件免费）
- 主要能力: 时间线/缓动/SplitText 逐字动画/MorphSVG/DrawSVG——大数字滚动、中文文字逐字表现、SVG 变形的现成最强层
- 为什么值得关注: 大数字 + 中文文字动画能力是财经视频表现层刚需；Remotion/HyperFrames 官方均列为可集成；免费商用
- 局限: 闭源（Webflow 标准许可）；动画计时型，在逐帧渲染中确定性需小心（官方实践建议 transform/opacity 优先）；无图表能力
- 适合阶段: Web Video（文字/转场/大数字表现层）
- 与项目匹配: 标题入场、数字滚动、文字强调；与渲染引擎时间线映射
- 推荐下一步: **值得实测**

### 组 3：中文 TTS

#### 8. MiniMax Speech-02
- 类型: API 服务
- 来源: platform.minimaxi.com
- 最近维护: 活跃（已迭代至 speech-2.8 系列）
- 主要能力: 中文自然度第一梯队（WER 2.25%）；emotion 情绪参数（happy/sad/calm）；文本内停顿标记 `<#0.5#>`；10 秒声音克隆；**异步长文本单次最高 100 万字符**
- 为什么值得关注: 中文自然度+情绪表现力最强候选，适合财经叙事的抑扬顿挫；长文本接口直接解决 10 分钟+旁白分段；低价（hd 3.5 元/万字符，约 700 元/百万汉字）
- 局限: **数字读法有已知问题（1,234 类错读）**，需开 normalize/pronunciation_dict 或前端预处理；英文缩写读法需实测；免费额度有限
- 适合阶段: TTS（高质量 API 主测）
- 与项目匹配: 与 Azure 构成双主测；数字/缩写由预处理层统一兜底
- 推荐下一步: **强烈建议实测**

#### 9. Azure TTS
- 类型: API 服务
- 来源: azure.microsoft.com/zh-cn/products/ai-services/text-to-speech
- 最近维护: 活跃（持续扩充语音库）
- 主要能力: zh-CN 神经语音几十个（XiaoxiaoNeural 实测中文第一梯队）；SSML 最完善（break/prosody/phoneme/sub alias）；400+ 语音；微软工业级 TN 引擎处理数字/百分比
- 为什么值得关注: **商用许可最清晰**；SSML 控制粒度细（停顿/重音/读音强制）；约 $15-16/百万字符，免费层 12 个月 50 万字符/月；长文 500 字分段是成熟实践；Edge TTS 试音后可无缝迁移（同源音色）
- 局限: 中文 phoneme 标签偶有不识别；英文缩写需 sub alias 手动映射；SSML 计入计费字符；情绪维度有限（中性播音感）
- 适合阶段: TTS（商用合规主链路）
- 与项目匹配: 中文财经长旁白 + 商用合规 → 最稳妥的主链路候选
- 推荐下一步: **强烈建议实测**

#### 10. CosyVoice 2 / 3
- 类型: 开源项目（本地部署，Apache-2.0）
- 来源: github.com/FunAudioLLM/CosyVoice
- 最近维护: 活跃（CosyVoice3 0.5B 于 2025-12 发布）
- 主要能力: 0.5B 零样本克隆（3-10 秒参考音频）；流式首包 ~1.5s；中文 WER 2.43%；CosyVoice3 支持指令控制（情感/语速/音量）+ 发音修复 + 文本归一化 + 多方言
- 为什么值得关注: **唯一 License 干净（模型权重与代码均 Apache-2.0）可商用的本地主流方案**；工程生态最成熟（Docker/WebUI/FastAPI/gRPC）；本地运行 0 边际成本
- 局限: **官方建议单次 10-200 字，超长 OOM**——10 分钟旁白必须自建分段拼接管线；生僻字发音偶漂移；GPU 4GB 起（0.5B 推荐 8-16GB）；数字读法需配合 ttsfrd 或预处理
- 适合阶段: TTS（本地备份/降本）
- 与项目匹配: 商用合规 + 可本地 → 本地开源类首选；代价是分段/预处理管线
- 推荐下一步: **强烈建议实测**

### 组 4：字幕

#### 11. Qwen3-ForcedAligner-0.6B
- 类型: 模型/库（Apache-2.0）
- 来源: huggingface.co/Qwen/Qwen3-ForcedAligner-0.6B（QwenLM/Qwen3-ASR）
- 最近维护: 2025 发布，2026 生态活跃（vLLM-omni/ComfyUI/Transformers 支持）
- 主要能力: 已知文本 + 音频 → **字级**时间戳；中文按单字切分；11 语言；单次 ~270s，alignLong() 支持更长
- 为什么值得关注: 中文对齐精度公开实测最优（普通话新闻 82ms vs WhisperX 135ms）；**与本项目场景完美契合：旁白文本已知（研报→脚本→TTS），强制对齐免疫 Whisper 中文识别错误**；Apache-2.0 可商用
- 局限: 不是识别器（文本必须已知）；推荐 GPU；不产 SRT（需自写转换几行）；标点/数字被过滤（分组逻辑需自处理）
- 适合阶段: Caption（对齐层主力）
- 与项目匹配: 字级 JSON 直喂渲染引擎字幕组件，架构最简
- 推荐下一步: **强烈建议实测**

#### 12. @remotion/captions + Animated Captions
- 类型: 框架组件（npm，MIT）
- 来源: remotion.dev/docs/captions
- 最近维护: 活跃（随 Remotion 持续发布）
- 主要能力: 统一 Caption 结构（text/startMs/endMs）；parseSrt 导入；createTikTokStyleCaptions 逐词分组；Animated Captions 三件套（Moving Pill/Popping Word/Word Highlight 卡拉OK）；serializeSrt 导出
- 为什么值得关注: **"字幕作为网页视频视觉一部分"的官方成熟方案**——字幕就是画面 DOM，与渲染同源；支持 CJK
- 局限: VTT 不能直接导入（需先转 SRT）；**中文无空格，分组逻辑默认英文分词需自写按标点分组**；中文逐词卡拉OK观感未验证
- 适合阶段: Caption（渲染层）
- 与项目匹配: 若走 Remotion 路线即字幕主力；若走 HyperFrames 路线其 kinetic captions skills 是对应物
- 推荐下一步: **强烈建议实测**

### 组 5：内容与脚本

#### 13. chenyuxiaojin/video-agent-skills
- 类型: Agent Library / Skill 集（MIT）
- 来源: github.com/chenyuxiaojin/video-agent-skills
- 最近维护: 活跃（单人维护，7 stars）
- 主要能力: 11 个 skill 从话题到剪映/DaVinci 时间线：producer（总导演+4 个人工检查点）、researcher（organize 模式：素材→叙事大纲）、writer（280 字/分中文口播、三种开场）、storyboarder、voice（MiniMax 中文）、editor、publisher（抖音/B站）
- 为什么值得关注: 唯一**中文原生**、形态最贴近"无真人数据视频"的第三方资源；researcher organize + writer 中文节奏几乎是"研报→大纲→口播稿"的现成骨架；MIT 可商用
- 局限: 7 stars 成熟度低；选题侧依赖抖音后台数据而非研报；无评审/动效角色
- 适合阶段: Content Director + Script
- 与项目匹配: 改动最小的一条现成内容路径
- 推荐下一步: **强烈建议实测**

#### 14. AgriciDaniel/claude-youtube
- 类型: Skill（MIT，312 stars）
- 来源: github.com/AgriciDaniel/claude-youtube
- 最近维护: 活跃
- 主要能力: YouTube 增长顾问：strategy（频道定位/内容支柱/选题）、hook（5 种变体+掉粉风险评级）、thumbnail（A/B 方案）、script（留存工程化）、SEO
- 为什么值得关注: "选题→包装→脚本"覆盖最完整的单一 skill；hook 框架可逐条照搬评估每期开场
- 局限: 全英文语境；无财经领域知识
- 适合阶段: Content Director（hook/包装方法论）
- 与项目匹配: 蒸馏成"财经编导 Checklist"；内容判断力仍需自研
- 推荐下一步: **值得实测**

#### 15. buda-ai/bunny-agent 内嵌 script-writer
- 类型: Skill（Apache-2.0）
- 来源: github.com/buda-ai/bunny-agent（templates/videodrone-agent/.claude/skills/script-writer）
- 最近维护: 极活跃
- 主要能力: 大纲→逐字口播稿：`[Tone]/[Emphasis]/[Pause]/[Energy]` 交付提示、`[VISUAL]/[TEXT OVERLAY]/[GRAPHIC]/[B-ROLL]` 视觉提示、语速计算、13 项质量自检
- 为什么值得关注: 脚本工程化程度开源最高；**视觉提示与下游 storyboard 天然衔接**（正是"脚本里就带画面指令"的形态）
- 局限: 全英文（150 词/分需换成 280 字/分中文节奏）；无财经知识
- 适合阶段: Script
- 与项目匹配: 交付/视觉提示规范可直接移植成中文口播稿模板
- 推荐下一步: **值得实测**

#### 16. digitalsamba/claude-code-video-toolkit
- 类型: Toolkit（MIT，1936 stars）
- 来源: github.com/digitalsamba/claude-code-video-toolkit
- 最近维护: 极活跃（近乎日更）
- 主要能力: 全流水线（planning→assets→review→audio→editing→rendering）；**明确无真人/AI 人物，支持 slides/motion graphics/data storytelling**；TTS 用 ElevenLabs 或自托管 Qwen3-TTS；模板含 concept-explainer
- 为什么值得关注: 形态与目标最接近的开源流水线骨架；1936 stars 社区验证；脚本写进 VOICEOVER-SCRIPT.md 由人审
- 局限: 脚本环节深度不足（需外挂自研口播规范）；Qwen3-TTS 中文需实测
- 适合阶段: Script + 流水线参考
- 与项目匹配: 渲染/配音侧最佳对标，脚本侧外挂自研规范
- 推荐下一步: **强烈建议实测**（作流水线骨架）

### 组 6：审片

#### 17. Gemini API 视频输入
- 类型: API 能力
- 来源: ai.google.dev/gemini-api/docs/video-understanding
- 最近维护: 活跃（GA）
- 主要能力: 原生视频输入：默认 1fps 采样、2M 上下文约 2 小时视频、时间戳问答、区间裁剪、**音频双流理解**
- 为什么值得关注: 唯一"整段 MP4 直接喂+能听旁白"的托管通道，正好覆盖抽帧方案无法覆盖的"配音自然度/长时间无视觉变化"；10 分钟视频一次调用出带时间戳审片报告
- 局限: 视频出境（公开研报风险可控）；1fps 对 30 秒内快速动画变化可能漏检；免费额度 2GB/日级
- 适合阶段: Review（整体审片通道）
- 与项目匹配: 审片 agent 的"眼睛+耳朵"
- 推荐下一步: **强烈建议实测**

#### 18. video-research-mcp
- 类型: MCP Server（MIT）
- 来源: github.com/Galbaz1/video-research-mcp
- 最近维护: 活跃（245 commits）
- 主要能力: 专为"Claude Code 看不懂视频"做的桥接：51 个 MCP 工具 + 17 个斜杠命令，ffmpeg 抽帧 + Gemini 3.5 Flash 驱动，>20MB 走 File API + context caching
- 为什么值得关注: Claude 生态内现成"video review agent"底座；输出 timestamped analysis.md 适合回填审片报告
- 局限: 依赖 GEMINI_API_KEY；无财经审片清单（12 维审查需自写提示词）
- 适合阶段: Review（底座）
- 与项目匹配: 装它 + 自写审片 checklist 提示词 = 审片 capability 底层
- 推荐下一步: **强烈建议实测**

#### 19. PySceneDetect
- 类型: 库（Python）
- 来源: github.com/Breakthrough/PySceneDetect
- 最近维护: 活跃（0.7.1 于 2026-07）
- 主要能力: 场景切换检测（内容/自适应/黑场淡入淡出），输出场景时间戳、切分视频
- 为什么值得关注: 把审片清单里的"节奏/长时间无视觉变化"**数值化**（场景间隔分布、前 30 秒场景数）；纯本地毫秒级零成本
- 局限: 只检测不理解；Motion Graphics 连续动画可能误报需调阈值
- 适合阶段: Review（确定性前置层）
- 与项目匹配: 审片 pipeline 的硬指标层，输出时间戳喂给后续抽帧审查
- 推荐下一步: **强烈建议实测**

#### 20. wshobson/agents（SuperClaude）
- 类型: Agent Repository（MIT）
- 来源: github.com/wshobson/agents
- 最近维护: 极活跃（2026-08，38.8k stars）
- 主要能力: 94 插件/203 agents/175 skills/16 orchestrators；Claude Code + Codex CLI + Cursor 多 harness；agent 即独立 .md 可单拷贝；内置 plugin-eval 三层质量评估
- 为什么值得关注: 当前社区最大最活跃的 Agent 库；README 明示每个 agent 可独立提取；MIT 无使用限制；**是未来主要 Agent 来源的第一候选**（视频专用角色需自补）
- 局限: 无视频流水线角色（Content Director/Motion Designer/Creative Director 均缺）；内容角色偏营销通才
- 适合阶段: 通用（Agent 来源）
- 与项目匹配: 承担通用角色（研究/文案/代码/质检），视频角色自补
- 推荐下一步: **强烈建议实测**（先试装 content-marketing 插件评估提示词质量）

---

## 5. B. 其中最值得优先测试的 5 个

1. **HyperFrames**（Web 视频引擎首选之一）—— 与目标形态同构、Apache-2.0 商业免费、40.9k stars 暴涨、官方 20 个 Agent skills、**与本地 `codex-video-pipeline` 同栈（升级现有链路成本最低）**。先跑一条 30-60 秒中文样片验证中文排版与音轨混流。
2. **Remotion + 官方 Skills**（Web 视频引擎首选之二）—— 事实标准、官方字幕/TTS 包齐全、Agent 技能体系成熟；必须与 HyperFrames 实测对比后二选一（或分场景混用）。重点验证：中文逐词字幕观感、ECharts 集成、License 边界是否可接受。
3. **MiniMax Speech-02**（TTS 主测）—— 中文自然度+情绪+长文本接口三项全占、价格低；数字读法问题用预处理层兜底（`cn2an` 标准实践）。与 Azure 并行测同一段财经文本对比听感与数字/缩写读法。
4. **Qwen3-ForcedAligner-0.6B**（字幕对齐）—— 已知文本强制对齐与本项目架构天然契合，中文精度公开实测最优、Apache-2.0。30 秒试片即可验证逐字高亮观感。
5. **chenyuxiaojin/video-agent-skills**（内容/脚本中文原生骨架）—— 改动最小的现成内容路径（researcher organize + 280 字/分中文节奏），先跑通"研报→大纲→口播稿"，再蒸馏 claude-youtube/bunny-agent 的方法论进自研 Prompt。

---

## 6. C. 推荐的 2-3 套组合方案

### 方案 A：HyperFrames 主线（推荐首选）

内容 Agent（video-agent-skills 骨架 + 自研编导 Prompt）→ 脚本 → **HTML/GSAP 页面（ECharts/Plot 图表 + 大数字动画）→ HyperFrames 渲染（官方 skills 生成）→ MiniMax/Azure TTS → Qwen3 强制对齐 → 画面内字幕 + 同源 SRT → 审片（Gemini + PySceneDetect + Claude 抽帧）**

- 优点：与目标形态 100% 同构（网页即成片）；Apache-2.0 无 License 风险；浏览器原生中文排版；官方 Agent skills 与本地 `codex-video-pipeline` 同栈（升级路径顺）；本地渲染零成本；浏览器预览即视频预览，迭代快
- 缺点：生态新（<2 年）、无 React 组件生态；中文实测未验证；LLM 直接生成 HTML 动画代码质量需 skills 约束；单机渲染为主
- 成本：引擎免费（本地）；TTS MiniMax 约 700 元/百万汉字 或 Azure 约 $15/百万字符；渲染 0 边际成本；人力主要是自研内容/视觉 Prompt 与组件库
- 复杂度：中（HTML/CSS/GSAP 技能要求低于 React）
- 成片质量潜力：高（真实浏览器排版 + 数据叙事组件全可用）

### 方案 B：Remotion 主线

内容层同 → **Remotion React 项目（官方 skills + 81 免费模板 + @remotion/captions）→ TTS → Whisper/Qwen3 词级时间戳 → 本地/Lambda 渲染 → 审片同**

- 优点：动态 Web 视频事实标准；React 组件生态最全（图表/字幕/转场）；官方字幕/TTS 集成包最成熟；逐帧控制粒度最强；渲染可分布式
- 缺点：**License 收费边界**（≤3 人盈利免费，4+ 人需 Company License）；React 学习曲线高；包体积大、本地渲染慢；LLM 生成代码需 2-3 轮修正（有官方 skills 缓解）
- 成本：小规模免费；TTS 同方案 A；Lambda 渲染约 $0.017/分钟视频（可选）
- 复杂度：中高（React/TS）
- 成片质量潜力：高（控制力最强，但依赖工程投入）

### 方案 C：最快出片验证组合

内容层同 → **html-video（nexu-io）直接跑通"脚本→HTML 模板→TTS→MP4"→ 审片同；或 DataMagic 在线 demo 先验证"数据→叙事视频"形态**

- 优点：60-90 秒 demo 可能一天内出片；验证形态可行性成本最低；html-video 与 HyperFrames 同引擎（升级方案 A 无缝）；DataMagic 的 DVSpec 数字可核查思想可借鉴
- 缺点：项目太新（3 个月）/ DataMagic License 未声明；模板需自写金融图表；成熟度不足以支撑正式发布链路
- 成本：极低（本地 + MiniMax 免费额度）
- 复杂度：低
- 成片质量潜力：中（快速验证形态，正式生产回到方案 A/B）

**推荐路径**：先 C 验证形态（1-2 天）→ 再 A/B 引擎 A/B 实测（各一条 60-90 秒样片）→ 选定引擎后按方案 A 或 B 补全组件库与 Prompt 体系。

---

## 7. D. 对动态 Web 视频路线的判断

**结论：值得作为当前主路线。** 依据：

1. **形态同构**：目标"随旁白播放的漂亮财经网页"与 HyperFrames/Remotion 的设计哲学是同一件事——成熟工程化载体已经存在（40.9k + 56.3k stars，均活跃），不是需要从零验证的新概念。
2. **与本地链路衔接顺**：现有 `codex-video-pipeline`（reference）本就依赖 HyperFrames 渲染，`media-production` capability 的验收标准（"画面不退化为简单 PPT 翻页"）正是这条路线要解决的质量缺口；升级是补全而非推翻。
3. **中文排版上限高**：真实浏览器排版引擎（HyperFrames）或 React DOM（Remotion）处理中文换行/标点/字体远优于 Pillow 静态图或 Canvas 手绘。
4. **数据叙事组件成熟**：ECharts/Plot/lightweight-charts 等财务图表 + GSAP 大数字动画全部现成，组合原则明确（库管结构、引擎管帧）。
5. **成本可控**：本地渲染免费，TTS 便宜（~700 元/百万汉字或 $15/百万字符），审片 API 按量付费；主要成本是工程与 Prompt 打磨。

**风险与边界条件**：
- 引擎二选一必须实测（中文排版、字幕观感、LLM 生成代码质量是分水岭）；
- **内容编导与视觉导演层是软肋**——外部无成熟资源，需要自研 Prompt/角色（这是本项目真正的护城河所在，也符合"内容质量 > 工具"的定位）；
- 中文 TTS 的数字/缩写读法与长文分段需预处理层兜底（`cn2an` + 逐模型实测）；
- License 核对清单见第 9 节（Remotion 收费边界、TTS 商用授权、字体 OFL、素材许可）；
- 不建议同时维护两条引擎主线——A/B 实测后收敛为一条，另一条降级为备选。

---

## 8. E. 下一步最小实验建议（60-90 秒 A/B Demo）

> 本次不实施。以下为建议方案，供你选择测试对象后执行。

**素材**：用紫光股份（或任一已完成公司）**已验收的内容资产**（冻结 RID + 长脚本 + 素材规划），取 60-90 秒片段（Hook + 一个核心财务论点，如营收/ROE 趋势或估值区间）。

**A/B 设计**：

| 维度 | A 方案 | B 方案 |
|---|---|---|
| 引擎 | HyperFrames（HTML/GSAP，官方 skills） | Remotion（官方 skills + 模板） |
| 图表 | ECharts 折线/柱状 + 大数字滚动 | 同左（或 Plot） |
| TTS | MiniMax Speech-02 vs Azure（同一段文本对比听感） | 同左 |
| 字幕 | 画面内逐词高亮（各自引擎方案）+ 同源 SRT | 同左 |
| 对齐 | Qwen3-ForcedAligner（文本已知） | 同左（faster-whisper 对照） |
| 审片 | Gemini 视频输入 + PySceneDetect + Claude 抽帧 checklist | 同左 |

**验收点**（每版成片对照）：① 中文排版与字体观感 ② 大数字/图表动画是否自然（非 PPT 感）③ 逐词字幕中文观感 ④ TTS 数字/百分比/英文缩写读法 ⑤ 前 30 秒吸引力 ⑥ 引擎工具链跑通成本（安装/生成/渲染时间）。

**成功标准**：至少一个方案在 6 个验收点全部通过或仅 1 项 WARN，且从内容资产到成片总耗时 < 1 天（含修 2-3 轮）。

---

## 9. License 与商业使用清单

| 资源 | License | 商用要点 |
|---|---|---|
| HyperFrames | Apache-2.0 | ✅ 商业免费，输出无限制 |
| Remotion | 自定义双轨（非 OSI） | ⚠️ ≤3 人盈利组织免费+输出可商用；4+ 人需 Company License（$25/座/月 或 $0.01/渲染+$100/月最低）；@remotion/captions 包本身 MIT |
| html-video | Apache-2.0 | ✅ |
| ECharts | Apache-2.0 | ✅ |
| lightweight-charts | Apache-2.0 | ✅ 须保留 TradingView 署名 |
| Observable Plot / D3 | ISC / BSD | ✅ |
| GSAP | Webflow 标准许可（免费商用） | ✅ 但闭源，禁用场景：与 Webflow 竞争的免代码动画构建器 |
| MiniMax TTS | API 付费 | ✅ 付费即商用授权（核对最新条款） |
| Azure TTS | API 付费 | ✅ 商用最清晰 |
| CosyVoice 2/3 | Apache-2.0（代码+权重） | ✅ 本地商用 |
| 讯飞 TTS | API 付费 | ✅ |
| Edge TTS | 非官方逆向 | ❌ **商用模糊**（微软无书面授权），仅限内部试音；正式发布迁移 Azure（同源音色） |
| ChatTTS / Fish Speech / Spark-TTS | CC BY-NC 系列 | ❌ **禁止商用** |
| IndexTTS2 | bilibili 自定义 ULA | ⚠️ <1 亿 MAU 且年收入<10 亿可免费商用；金融场景条款需法务确认 |
| Qwen3-ForcedAligner | Apache-2.0 | ✅ |
| faster-whisper / WhisperX | MIT / BSD-2 | ✅ |
| aeneas / whisper-timestamped | AGPL-3.0 / 不明 | ❌ |
| wshobson/agents | MIT | ✅ |
| harness-100 | Apache-2.0 | ✅ |
| video-agent-skills / claude-youtube / bunny-agent | MIT / MIT / Apache-2.0 | ✅ |
| DataMagic | **未声明** | ❌ 商用/发布前必须联系作者确认 |
| MoneyPrinterTurbo / VideoLingo | MIT / Apache-2.0 | ✅（有 CVE 需关注） |
| 中文字体（Noto Sans SC 等） | OFL | ✅ 可嵌入商用 |
| Pexels 素材 | Pexels License | ✅ 但须记录素材页/创作者/许可（现有链路已要求） |

**未明确项**：MiniMax 最新商用条款细节、IndexTTS2 金融条款解释、DataMagic License——标记为"需确认"。

---

## 10. 已排除候选摘要（筛选过程留痕）

- **Motion Canvas / Motionity**：上游停滞（官网 NXDOMAIN / 停更 4 年），Canvas 排版不适合中文财务网页形态
- **Puppeteer/Playwright/RecordRTC 录制系**：丢帧、码率（VP8 1Mbps）、格式硬伤，仅限样片；自研 GSAP+录制被 HyperFrames/Shotstack 封装覆盖（估 2-4 周工程量）
- **sajjadium/animate、unrevealed**：WebFetch 404，无法核实存在性
- **Highcharts**（专有，免费仅限非商业）、**Datawrapper**（无动画）、**Recharts/Chart.js**（逐帧不友好）
- **ChatTTS / Fish Speech / Spark-TTS / GPT-SoVITS**：非商用 License 或声音权属风险
- **ElevenLabs**：中文非强项 + UTF-8 3 倍计费
- **aeneas / whisper-timestamped / AutoCaptions / VideoCaptioner**：License 或形态错位
- **CTR 导向封面生成器**（多数 YouTube thumbnail agent）：默认夸大倾向，与事实红线冲突
- **ai-video-maker（ydssx）**：0 stars 无成片证据；**ShortGPT**：停滞 18 个月
- **gitroomhq/agent-media**：AI 演员 UGC 形态，与"非 AI 生成人物"要求冲突
- **iannuttall/claude-agents**：已 archived；**rshah515**：趋停滞
- **flourish 视频导出 / Datawrapper 付费**：成本与形态不可行（仅作视觉基准）

---

## 附录：关键事实速查（决策引用）

- HyperFrames：40.9k stars，Apache-2.0，20 官方 Agent skills，2026 年内从 ~2 万暴涨
- Remotion：56.3k stars，v4.0.509（2026-08-12），官方实测 1 分钟 1080p ≈ $0.017 / 18.9s（Lambda）
- html-video：4.3k stars（2026-05 创建），Apache-2.0，Hyperframes 引擎 + MiniMax TTS
- MoneyPrinterTurbo：103.4k stars，MIT，素材拼贴型天花板
- ECharts：66.8k stars，v6.0.0（2025-07-30），SSR SVG 渲染 v5.3.0+
- lightweight-charts：16.7k stars，v5.2；Observable Plot：v0.6.17（2025-02 后放缓）
- MiniMax：speech-02-hd 中文 WER 2.25%，hd 3.5 元/万字符，异步长文本 100 万字符/次
- Azure TTS：~$15-16/百万字符，免费层 12 个月 50 万字符/月
- CosyVoice 2/3：Apache-2.0（权重+代码），中文 WER 2.43%，建议单次 10-200 字
- Qwen3-ForcedAligner-0.6B：Apache-2.0，中文 82ms 平均偏差（WhisperX 135ms）
- WhisperX v3.8.2+ 修复跨语言时间戳错位回归（v3.3.3-3.8.1）
- Claude API：官方文档确认仅图片输入（JPEG/PNG/GIF/WebP），单请求 100-600 张；Gemini API 原生视频+音频
- wshobson/agents：38.8k stars，MIT，203 agents；harness-100：100 harness，含 production-reviewer
- 审片红线：研报↔脚本↔旁白转写三向文本比对（VLM 不能凭视觉自评"是否曲解研究事实"）
