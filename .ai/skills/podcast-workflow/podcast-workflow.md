# podcast-workflow

> 外部参考资源：GitHub `questionjie-max/podcast-workflow`

## 元数据

| 字段 | 值 |
|---|---|
| name | podcast-workflow |
| kind | skill |
| description | AI 播客工作流参考：情绪标签、自然对话文稿、合规复核和分段 TTS |
| source | github: https://github.com/questionjie-max/podcast-workflow |
| installed_ref | `a0cb51ec25b1baacbac6213023154d048cfa2ac7` |
| runtime | claude / codex（参考，不作为当前运行时） |
| invocation | 阅读上游 `SKILL.md` 的 emotion tags、style instructions 和 chunking strategy；不直接替换本账号 VoxCPM 音色链路 |
| requirements | 上游默认依赖 Xiaomi MiMo TTS；当前项目不依赖该后端 |
| update | manual：重新读取 GitHub 固定 commit；verify：检查情绪标签、分段策略和许可证是否变化 |
| scripts | 无本地辅助脚本 |
| experience_refs | 无 |

## 调用说明

### 可复用部分

- 每个段落/turn 显式标注情绪，不让 TTS 自己猜语气。
- 用 style instruction 把“好奇、沉思、认真、略带调侃、回到现实”等情绪映射到朗读方式。
- 先按情绪切分，再按长度切小块，最后逐段生成并合并。
- 文稿要求像和朋友分享发现，短句、长短节奏交替、适量语气词和标点停顿。
- TTS 前保留人工 review 和合规 review。

### 当前项目的适配方式

- `emotion`、`delivery`、`reply_to_turn_id` 和 `interaction_type` 写入 Phase 2 的 episode manifest。
- Phase 3 继续使用账号级 VoxCPM 音色；MiMo 只作为情绪编排方法参考，不作为后端替换。
- 情绪先通过回应句式、标点、停顿和重音文本实现；要实现更明显的声学情绪，需要为每位主持人补充多情绪参考音色，或接入支持 style instruction 的 TTS adapter。

### 限制

- 上游仓库 README/技能文档描述的是 MiMo TTS 后端，不能证明 VoxCPM 会自动执行同等的情绪匹配。
- “情绪标签”本身不是情绪音频；必须检查生成音频是否真的有语速、停顿、重音和音高变化。
- 不复制上游 prompt 或第三方声音资产；只吸收可验证的编排方法。
