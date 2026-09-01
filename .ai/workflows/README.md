# Workflow 库（v0.2.2）

## 格式约定

- 所有 Global / Project Workflow 一律使用 **Markdown SOP**（导演手册）格式，模板见 `.ai/templates/workflow.md.template`（字段清单一律从模板读取，禁止内联字段定义）。
- SOP 结构固定为：Mission / Input / Output / Principles / Phase[Goal / Required Resources / Input / Output / Quality Criteria / Known Issues]；当前有效规则只写在这些运行章节中。
- Required Resources 直接 by-name 列出 Skill/Agent（表格第二列固定裸小写 `skill` 或 `agent`），零中间层引用；Workflow Markdown 是流程唯一事实源。
- 旧 YAML 版本已归档至 `.ai/archive/workflows/`（仅溯源，不构成执行契约）。

## Category 枚举

| Category | 位置 | 说明 |
|---|---|---|
| development | `.ai/workflows/development/` | 开发类流程 |
| task | `.ai/workflows/task/` | 任务类流程 |
| automation | `.ai/workflows/automation/` | 自动化类流程 |

## 索引

- 由 workflow-registry 索引（`.claude/skills/workflow-registry/`）：只索引元数据（位置/分类/项目关联/每 SOP 的 Required Resources by-name 列表），不解释、不执行。
- 当前 Global Workflow：
  - `task/closeout-and-commit`：收尾、经验候选、用户确认、文档交付与本地提交。
  - `task/video-content-extraction`：长视频内容提取。
  - `automation/voice-clone-from-tts`：从 TTS 参考音频生成可复用音色资产。
- 其他分类可能只保留 `.gitkeep`，不代表不存在项目级 Workflow。
- 项目级 Workflow 位于各自项目仓库 `projects/{project-name}/workflows/{name}/workflow.md`（例：investment-research-system 的 3 个 listed-company-* 生产 Workflow）。
