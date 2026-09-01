# research-intelligence-agent

> 管理资产：`.ai/agents/research-intelligence-agent/research-intelligence-agent.md`；安装实体：`.agents/research-intelligence-agent.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | agent |
| 来源 | internal · workspace internal agent profile |
| installed_ref | internal |
| runtime | both |
| 调用入口 | 由 research-content-direction Phase 1 调用；输入 research-materials/，输出 content-assets/research-intelligence/ |
| 要求 | 已验收的研究资料目录 research-materials/（investagent / industry-analysis / industry-cycle-analysis 原生产物 + execution-log.md）；能处理异构格式产物（HTML / PDF / Markdown / JSON / 图片）并区分事实、判断与缺口 |
| 更新 | internal · 只更新本地 Agent 调用说明、输出资产类型与边界；不得复制外部 Skill 内容或伪造未执行资源；验证：用一个已完成上市公司案例（research-materials/ 完整产物）生成五类输出资产，人工抽样核对事实来源与 execution-log 一致性 |
| 辅助脚本 | scripts/check_factmap.py（fact-map 输出自检：Conflict 块格式/Level 标注/来源完整性/L4 语气，输出前运行）；scripts/verify_financial.py（财务一致性验证：双值对比/PE-PB-ROE 重算/比率核对，验证冲突时可选使用） |
| 经验引用 | — |

## 作用

Research Intelligence Agent（v0.3 重命名）：将 research skills 产出的资料转换为结构化研究资产（「我们知道什么？」）——理解、整理、评估 research-materials/ 原始研究产物，为后续内容生产提供高质量基础资产；对可验证的事实冲突负责验证解决（财报 > tushare 数据优先级，有依据补数）。消费研究资产，不生产新的研究资产。

## 实体位置（可加载定义）

- `.agents/research-intelligence-agent.md`——完整职责（定位/输入/核心职责/边界/输出/执行原则/验收）

## 调用方式

- 输入：`research-materials/` 目录（investagent / industry-analysis / industry-cycle-analysis 产物 + execution-log.md）
- 输出：`content-assets/research-intelligence/` 五类资产（fact-map / viewpoint-map / conflict-map / evidence-gap / content-opportunity）；资产类型固定、文件内部结构自由

## 注意事项与踩坑

- 理解与验证并重（v0.3）：事实回指 research-materials/；验证用优先级数据（财报第一、tushare 第二），有依据补数记录来源；不重新执行研究、不生成完整报告、不生产视频内容、不裁决观点分歧。
- 可信度评估依据 `execution-log.md` 的资源执行状态（真实执行 / 降级 / 未执行）。
- 冲突观点原样保留并标注来源，不自行裁决。
- **四级可信度（v0.2/v0.2.1）**：fact-map 每条事实标注 Level 1-4（直接事实/可靠二手/模型整理/转述推算），统计派生/间接计算一律 L4；viewpoint-map 每条观点标注 coverage（来源数量/覆盖等级/风险）——下游必须保留该等级，禁止将 Level 4 表述为确定事实。
- **输出自检（v0.2.1 execution contract）**：fact-map 生成后执行数字一致性检查（同指标冲突标记 Conflict 块：指标/来源A/来源B/原因/处理=保留不自动选择）+ 来源完整性检查（L1/2/4 必须含 source/date/section）。
