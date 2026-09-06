# finance-humor-writing

> 管理资产：`.ai/skills/finance-humor-writing/finance-humor-writing.md`；安装实体：`.claude/skills/finance-humor-writing/`

## 元数据

| 字段 | 值 |
|---|---|
| name | finance-humor-writing |
| kind | skill |
| description | 面向中小投资者的财经口播表达层：按行情、财报、公司和估值主线选择不同的轻幽默机制，在事实冻结后提升可看性、通俗度和共情，不新增事实或投资建议 |
| source | internal · 由本项目对外部幽默/写作技能的机制吸收与财经内容工程本地化形成 |
| installed_ref | internal-2026-09-06 |
| runtime | claude / codex |
| invocation | `$finance-humor-writing`；由主线 Agent 选定内容模式后调用，完成财经幽默化表达、事实保留检查和降级说明 |
| requirements | 必须有已冻结的内容主线、观众状态、事实来源和结论；默认轻度幽默；不得复制外部原句或具名人物口吻；成片前仍需通过事实与财经边界审校 |
| update | internal · 修改入口或 `references/` 后，用同一研究输入分别跑四种模式并核对事实零漂移、观众契约、幽默浓度和硬性不通过条件 |
| scripts | — |
| experience_refs | — |

## 调用说明

这是本项目自己的财经表达 Skill，不是外部技能的简单叠加。它把外部资源中的可迁移机制重新组织为四种财经模式：行情陪伴、账本预期差、生意拆解、机制翻译；其中“轻锋反差”只是横向修辞，不是第五条内容主线。

入口只放路由和硬约束，详细资产分层在安装实体的 `references/`：`distillation-map.md` 记录外部机制到本地规则的转译，`mode-guides.md` 记录四条主线，`humor-patterns.md` 记录财经技法和反例，`voice-contract.md` 记录中小投资者站位，`evaluation.md` 记录同题测试与成片复盘。

推荐调用顺序：

`主线 Agent` → `finance-humor-writing` → `finance-content-engineering` → `renwei-writing` → `boundary-rewrite` → `research-quality-gate`

它不负责选题、研究、数据计算、投资判断、配音或剪辑。最重要的验收不是“笑点多不多”，而是中小投资者能否感到被理解，并且在笑点之后记住一个准确的判断。

本地化时只吸收机制，不复制 `witty-blog-voice`、`ying-style-writing`、`humor-master` 的原句、人物模仿规则或外部语料。任何外部资源的许可证和语料来源问题，不会因为本 Skill 的创建而被继承或绕过。
