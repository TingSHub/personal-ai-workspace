# humanizer-zh

> 外部参考资源：GitHub `op7418/Humanizer-zh`

## 元数据

| 字段 | 值 |
|---|---|
| name | humanizer-zh |
| kind | skill |
| description | 中文文本 AI 腔识别与自然化改写方法，覆盖 24 类常见模式 |
| source | github: https://github.com/op7418/Humanizer-zh |
| installed_ref | `91f3d394db8419c20d67ebe22a96cf8fee0a404b` |
| runtime | claude / codex（参考，不作为独立运行时） |
| invocation | Phase 2 口播稿生成后，以 bounded editorial review 方式检查 AI 腔；必须保留事实、speaker turn、interaction、emotion、delivery 和数字口径 |
| requirements | 无运行时依赖；上游 LICENSE 为 MIT；内容参考 `blader/humanizer`、`hardikpandya/stop-slop` 和 Wikipedia AI writing guide |
| update | manual：重新读取 GitHub 固定 commit 的 `SKILL.md`、README 和 LICENSE；verify：检查规则清单、中文适配和上游许可是否变化 |
| scripts | 无本地脚本 |
| experience_refs | 无 |

## 调用说明

### 可复用部分

- 识别夸大意义、宣传腔、模糊归因、机械三段式、过度连接词、过度限定和通用积极结论。
- 打破句式同质化，混合短句、长句、第一人称反应和有限的不确定性。
- 把“观点—具体反应—数据—限制”写得更像人在思考，而不是报告模板。
- 允许适度不完美和自然停顿，但不靠堆“嗯、对、但是”制造真人感。

### 当前播客工作流适配

- 接入 Phase 2 的 Dialogue Director 生成环节，作为文本风格参考和有限审校，不作为无条件后处理器。
- 重点检查主理人追问是否过于公式化、分析师回答是否像报告、是否重复使用“这个问题很准”“不能只看”等固定句式。
- 与 `content-policy.md` 联合使用：口播自然化不能删除证据、改变数字方向、改变口径或破坏 `reply_to_turn_id`。
- 改写后必须重新生成音频；不能只替换字幕文本。

### 限制与踩坑

- 它处理的是文字自然度，不会生成真人停顿、呼吸、抢话、音高或情绪；声学表现仍由 TTS 和音频编排负责。
- “去 AI 痕迹”不能等同于随意口语化；财经稿不能为了鲜活而加入未经证实的经历、观点或夸张判断。
- 不应在 Phase 3 直接自由改稿；所有改写必须回到 Phase 2 并重新通过 manifest、数字和证据检查。
