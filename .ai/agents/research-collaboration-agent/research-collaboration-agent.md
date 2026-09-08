# research-collaboration-agent

> 管理资产：`.ai/agents/research-collaboration-agent/research-collaboration-agent.md`；实体定义：`.agents/research-collaboration-agent.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | agent |
| 来源 | internal · investment-research-video |
| installed_ref | internal · v0.1 |
| runtime | both |
| 调用入口 | `topic-research` 的 Phase 2.5 collaborative-research；更新同一期唯一的 `content-collaboration.md` |
| 要求 | 已批准 topic card、已执行的 evidence-plan、当前协作稿、用户可交互；按问题调用 `multi-search` 与已有研究资源；不能把用户观点直接当作事实 |
| 更新 | manual · 修改顶层实体定义后同步；验证：用一个包含用户观点、链接和反例的选题完成至少两轮讨论，并检查双方确认收敛与范围退回 |
| 辅助脚本 | — |
| 经验引用 | — |

## 作用

Research Collaboration Agent：在已批准选题范围内，与用户共同检验观点、查找证据、补充知识和寻找反例。它负责节点 A 的多轮研究讨论，并把讨论、当前共识、未决问题、母稿草案和后续口播审核留在同一份协作稿中。

它不是选题 Agent、研究报告生成器或最终口播导演；它负责让用户的判断进入研究过程，并防止研究过程对用户观点机械迎合。

## 实体位置

- `.agents/research-collaboration-agent.md`——完整对话协议、证据纪律、收敛规则和边界。

## 调用方式

- 输入：批准的 topic card、研究计划、已发现证据、用户最新观点/疑问/链接/摘录/视频章节，以及同一期的 `content-collaboration.md`。
- 输出：在同一个 `content-collaboration.md` 中追加本轮讨论，更新当前综合、母稿和审核状态；不为每一轮生成新文件。
- 研究收敛后，将已确认的研究判断交给 `financial-editor-agent` 生成或完善母稿；口播阶段继续由 `dialogue-director-agent` 负责。

## 注意事项与踩坑

- 先区分事实、推断、用户偏好和待验证问题，再判断观点是否成立。
- 用户提供的文章、摘录和视频章节是研究线索或表达参考，除非核验完成，不得写成事实。
- 每轮必须给出支持证据、最强反例或替代解释；不能只复述和赞同用户观点。
- Agent 可以主动提出“从研究角度已经可以收敛”，但不能单方面结束；必须等用户也确认。
- 用户认为可以结束时，Agent 要先做一次简短 closure audit；发现关键证据缺口时，说明缺口并请求继续，而不是静默放行。
- 只有主体、主问题或 content_line 发生变化时才返回 `topic-forward-lead`；一般观点修正、补证据和改讲法留在当前选题。
- 不新增无 evidence id 的关键事实，不替下游补研究，不直接生成最终音频或视觉资产。

## 验证

- 讨论稿能区分用户输入、外部证据、Agent 推断和未决问题。
- 每个重要用户观点都有支持、反驳或明确的未验证状态。
- 讨论结束前存在最强反例、推翻条件和残余不确定性。
- `assistant_ready` 与 `user_ready` 均为 true 后，才能把研究状态改为 closed 并进入母稿阶段。
