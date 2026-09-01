# research-content-producer

> 管理资产：`.ai/agents/research-content-producer/research-content-producer.md`；安装实体：`.agents/research-content-producer.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | agent |
| 来源 | internal · workspace internal agent profile |
| installed_ref | internal |
| runtime | both |
| 调用入口 | 由当前项目主 Agent 按 Workflow 和项目输出模板执行 |
| 要求 | 已通过上游 Capability 验收并冻结的 Research Intelligence Document；能读取项目模板并进行长文本结构化生成的模型 |
| 更新 | internal · 只调整本地 Agent 调用说明和项目输出契约，不复制外部投研 Skill 方法论；验证：用同一 Research Intelligence Document 依次生成内容策划、长视频、短视频、SRT和素材清单并执行跨文件一致性检查 |
| 辅助脚本 | — |
| 经验引用 | research-master-content-pipeline |

## 作用

从已冻结的 Research Intelligence Document 依次派生内容策划、长视频脚本、短视频脚本、字幕和素材规划。研究综合与冲突消解由 `research-intelligence-agent` 负责，本 Agent 不再生成研究母稿。

## 实体位置（可加载定义）

- `.agents/research-content-producer.md`——完整职责（定位/调用边界/一致性检查/更新）

## 调用方式

- 输入：已验收并冻结的 Research Intelligence Document + 项目输出模板
- 输出：内容策划 → 长视频脚本 → 短视频脚本 → SRT 字幕 → 素材清单（各独立落盘，逐级消费已验收产物）

## 注意事项与踩坑

- 不独立补充财务数字、估值数据或行业事实；重要结论没有证据时必须退回上游步骤。
- 内容策划必须包含受众、痛点、核心冲突、多个角度、30 秒 Hook、8-15 分钟故事结构和标题方向。
- 关键数字跨母稿、脚本、字幕保持一致；没有最终音频时 SRT 标为估时稿。
