# Investment Research Video

一句话描述：investagent 研究 → 企业研究 HTML/deck（每页 speaker script）→ TTS 配音 → HyperFrames 视频的完整内容生产链路验证。

## Goal

验证「研究 → 一次内容规划（deck + speaker script）→ 口语化（Content Lock）→ TTS → HyperFrames 视频」闭环。

先做结果，再优化流程。不提前设计复杂 Agent 架构（不创建 Research Director / Content Director / Visual Director）。

## Resources Used

- industry-analysis — 行业/产业链研究（P1）
- industry-cycle-analysis — 供需周期研究（P1）
- investagent — 公司研究+数据（P1，内容生产链路只跑「研究+数据」范围）
- html-ppt-skill — HTML 生成（长文/翻页设计体系）
- dashi-ppt — 工业级翻页 PPT（可选，P3；版式槽位约束严格，渲染后需 static-html-qa 兜底）
- static-html-qa — 跨生成器质检（内容边界/数值一致性/前端 QA，P3/P4 必跑）

## Workflows

- 本 MVP 使用内置流程（用户定义）：Step 1 Research Source（原样保留研究报告内容）→ Step 2 HTML Generation（html-ppt-skill 生成单文件 HTML）。后续若沉淀为可复用流程，再按 workflow-registry 登记。

## 产物

- `outputs/maotai-600519/investment-report.html` — 投资者阅读 HTML 报告
- `outputs/maotai-600519/preview.png` — 全页截图预览
- `docs/mvp-evaluation.md` — MVP 评估报告（4 个评估问题）

## Project 运行约束

本目录是 workspace 唯一主项目下的内容生产子项目，归属于 workspace 顶层 Git 仓库；项目说明统一维护在本 README，不再使用独立的 `AGENTS.md`、`CLAUDE.md` 或 `project.yaml`。

### 项目元数据

- 名称：investment-research-video
- 描述：investagent 研究 → 企业研究 HTML/deck（含 speaker script）→ TTS 配音 → HyperFrames 视频的完整内容生产链路。
- 当前状态：持续维护中。

### 活动 Workflows

- `investagent-html-report`：研究 → 冲突检查 → HTML/deck 生成。
- `investagent-video-production`：notes 口语化 → TTS → composition → 渲染。
- `investagent-video-by-hyperframes`：研究 → 编辑综合 → HyperFrames 全权接管创作与渲染。
- `investagent-podcast-video-by-hyperframes`：播客式视频的脚本、音频、视觉和 HyperFrames 合成链路。

### 必要资源

- `industry-analysis`、`industry-cycle-analysis`、`investagent`：研究阶段。
- `html-ppt-skill`：HTML/deck 生成。
- `finance-content-engineering`：口语化与零漂移校验。
- `static-html-qa`：内容边界、数值、前端和 Presenter 质检。
- `edge-tts`：TTS 配音。
- `hyperframes`：视频渲染。

### 统一开发规则

- 研究、deck、口播和字幕不得出现目标价、买卖建议或操作区间，使用中性研究语言。
- 每页 notes 是最终口播文本的唯一 Source of Truth；TTS 只做技术性处理，字幕由 notes 派生。
- 视频页面时长等于音频时长；禁止多级 xfade 链造成累积误差。
- 口语化改写后必须执行事实零漂移检查；不得近似化数字或改变口径。
- 字段清单一律从 workspace 的 `.ai/templates/` 读取。
- 项目执行记录写入 `logs/`，不直接进入资产库；可复用候选经用户确认后交给 `experience-curator`。
