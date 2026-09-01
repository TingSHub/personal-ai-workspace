# Capability 归档索引（v0.2.2 架构收敛）

归档日期：2026-08-15
归档原因：v0.2.2 架构收敛——四层（Project→Workflow→Capability→Skill/Agent）收敛为三层（Project→Workflow→Agent/Skill）。Capability 层退役，Workflow 转 Markdown SOP，Required Resources 直接 by-name 列 Skill/Agent。

> 本表为溯源/导航信息，不构成执行契约；语义以对应 Workflow SOP 与 skill.yaml/agent.yaml 为准。

## 目录

- 5 个 capability.yaml 完整归档于此（无删除无丢失），原始位置：`.ai/capabilities/{name}/capability.yaml`
- 各 capability 的 `resources` 清单（含 strength/weakness/test_result/recommended_usage 注记）已迁移至对应 Workflow SOP 的 Required Resources 表
- `selection` 原则（best_available_resource）已进入 `.ai/rules/rules.md`（V0.2.2）
- 原始文件可通过本仓库 git 历史或本目录随时回查

## Capability → Workflow Phase 映射表（5 能力 × 11 Phase）

| Capability | Workflow | Phase | 说明 |
|---|---|---|---|
| data-acquisition | listed-company-research-production | Phase 1: acquire-and-verify-sources | 数据、法定披露与证据底稿获取 |
| investment-research | listed-company-research-production | Phase 2: execute-research-intelligence | 研究综合为 Research Intelligence Document |
| quality-assurance | listed-company-research-production | Phase 3: validate-research-intelligence | 研究交付独立质量门 |
| content-production | listed-company-research-video-production | Phase 1: design-content | 内容策略与脚本规划 |
| content-production | listed-company-research-video-production | Phase 2: produce-content-assets | 长/短视频、字幕初稿与素材规划 |
| quality-assurance | listed-company-research-video-production | Phase 3: validate-content-package | 内容包独立质量门 |
| media-production | listed-company-video-production | Phase 1: plan-media-production | 制作计划 |
| media-production | listed-company-video-production | Phase 2: produce-media-assets | 旁白、视觉、字幕与成片生产 |
| media-production | listed-company-video-production | Phase 3: render-preview | 预览成片渲染 |
| quality-assurance | listed-company-video-production | Phase 4: validate-media | 媒体层独立质量门 |
| media-production | listed-company-video-production | Phase 5: package-publish-assets | 发布包组装 |

（3 个 workflow 共 11 个 Phase：research-production 3 + research-video-production 3 + video-production 5）

## 各 Capability 原始 resources 清单（by-name，供溯源）

| Capability | resources（原 execution 角色） |
|---|---|
| content-production | codex-video-pipeline (skill) / research-content-producer (agent) |
| data-acquisition | cninfo-connector / tushare-connector / marketpulse / tushare-data / multi-search (skill) |
| investment-research | research-intelligence-agent (agent) / investagent / industry-analysis / buffett / earnings-reader / industry-cycle-analysis / deep-analysis / financial-fraud-index (skill) |
| media-production | codex-video-pipeline (skill) / video-production-executor (agent) |
| quality-assurance | research-quality-gate / video-quality-reviewer / codex-video-pipeline (skill/agent) |

> 各资源完整注记（strength/weakness/test_result/recommended_usage/dependency_cost/maintenance_cost）见对应 capability.yaml 原文件与迁移后的 Workflow SOP Required Resources 表。
