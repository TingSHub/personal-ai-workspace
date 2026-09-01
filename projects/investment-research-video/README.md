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
