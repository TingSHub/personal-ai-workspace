# human-understanding

> 外部参考资源：GitHub `suw294550-boop/human-understanding`

## 元数据

| 字段 | 值 |
|---|---|
| name | human-understanding |
| kind | skill |
| description | 口语、模糊和不完整反馈的意图还原与上下文理解模板 |
| source | github: https://github.com/suw294550-boop/human-understanding |
| installed_ref | `53399d28b06d043808df658e39bfc81482b35753` |
| runtime | claude / codex（参考，不作为独立运行时） |
| invocation | 在理解用户对视频、对话和口播的自然反馈时，读取口语映射、上下文指代和偏好记忆规则；不要直接复制其 prompt 到生产稿 |
| requirements | 无运行时依赖；上游 README 声明 MIT，但仓库未附独立 LICENSE 文件 |
| update | manual：重新读取 GitHub 固定 commit 的 `SKILL.md`、`human-understanding-prompt.md` 和 README；verify：检查口语映射、上下文规则和许可证声明是否变化 |
| scripts | 无本地脚本 |
| experience_refs | 无 |

## 调用说明

### 可复用部分

- 把“有点怪”“不像真人”“再自然一点”“这个不对”等反馈还原成可执行问题，而不是只按字面改一个词。
- 主动利用最近上下文解析“这个、那个、上次那个”的指代，减少重复询问。
- 把用户偏好沉淀为可复用决策，例如“女方主理人”“VoxCPM2 首选”“交锋模式显式指定”。
- 用简洁、直接、自然的方式回应用户，不把工作流术语暴露到最终内容里。

### 当前播客工作流适配

- 在 Phase 2 之前用于把用户的试听反馈转成 Dialogue Director 可消费的约束：角色、节奏、回应关系、语气词、段落长度和情绪。
- 在 Experience Curator 之前用于识别反馈背后的可复用规则，而不是把某家公司的例句写进模板。
- 与 `humanizer-zh` 分工：本资源理解“用户到底想改什么”，不负责直接改写口播文本。

### 限制与踩坑

- 这是一个轻量 Skill 模板，主要是 prompt 和口语映射，没有音频、TTS 或对话规划执行器。
- “主动补全信息”不能覆盖财经研究事实；证据、数字和模式切换仍必须来自 Workflow 与 manifest 契约。
- 不把用户一句模糊反馈直接变成永久规则，必须结合上下文判断其是否是稳定偏好。
