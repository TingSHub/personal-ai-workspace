# writing-dna-skill

> 管理资产：`.ai/skills/writing-dna-skill/writing-dna-skill.md`；安装实体：`.claude/skills/writing-dna-skill/`

## 元数据

| 字段 | 值 |
|---|---|
| name | writing-dna-skill |
| kind | skill |
| description | 从分类型语料中蒸馏语言、结构、选题逻辑、素材策略、认知框架与呈现规则，形成可复用 Writing DNA |
| source | github · https://github.com/larashero3-dotcom/writing-dna-skill |
| installed_ref | ee3d97ee27268004b5187d97711161f44fc4aae4 |
| runtime | claude / codex |
| invocation | `$writing-dna-skill`；对指定语料库执行分层蒸馏并生成 Writing-DNA.md 及分层产物 |
| requirements | 至少一批完整、可合法处理的语料；本项目视频语料需先按内容主线标注 article_type 等元数据；视频版需补充口播节奏、双人回合和画面协作分析 |
| update | git · 按上游仓库固定 commit 重新安装到 `.claude/skills/writing-dna-skill/`；verify：读取 SKILL.md、模板和一个最小语料目录，确认可生成分层产物与 Writing-DNA.md |
| scripts | — |
| experience_refs | — |

## 调用说明

用于把土豆等参考账号的公开视频口播按主线分组，蒸馏成市场行情、财报预期差、公司/产业链、估值/机制四套风格参考资产。它负责抽取可操作规则，不负责决定本账号的选题、事实结论或财经边界。

本项目不得直接复刻原句、个人口头禅、具体观点或原作者身份；原始音频和转写只在有处理权限的内部目录使用。Writing DNA 需要经过 `creator-spoken-content-analysis` 的口播与双人对白补充，再交给本账号自己的表达 Agent。

语料过少时只能标为初版假设，不能把它当成稳定风格。写作前应读取分层产物和同类型原文，但研究事实必须来自当前冻结研究包。
