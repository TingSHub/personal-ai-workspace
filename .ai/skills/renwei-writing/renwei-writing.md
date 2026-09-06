# renwei-writing

> 管理资产：`.ai/skills/renwei-writing/renwei-writing.md`；安装实体：`.claude/skills/renwei-writing/`

## 元数据

| 字段 | 值 |
|---|---|
| name | renwei-writing |
| kind | skill |
| description | 在润色、改写和去 AI 腔时保留说话人的位置、情绪、代价和个人手迹，采用少改、可解释、逐处回溯的编辑方式 |
| source | github · https://github.com/orange2ai/renwei-writing |
| installed_ref | c6566884997f3688478f43ecdac29423757548a0 |
| runtime | claude / codex |
| invocation | `$renwei-writing`；对已有口播稿或用户提供的草稿执行保人味编辑和事后检查 |
| requirements | 必须有原始草稿或明确的作者意图；只检查和解释实际改动；闭源商业成片或专有商业交付需先取得上游商业授权 |
| update | git · 按上游仓库固定 commit 重新安装到 `.claude/skills/renwei-writing/`；verify：读取 SKILL.md、事后检查清单和案例，完成一段最小“少改稿”验证 |
| scripts | — |
| experience_refs | — |

## 调用说明

用于表达层最后的“保人味”检查，不用于替代选题、研究或内容导演。核心原则是少动、先把毛边视为手迹、不凭空添加画面和数据、不强行制造金句；改完逐处说明改动原因，并检查宣传腔、套路对仗、意义拔高、万能展望和短句轰炸等 AI 痕迹。

该资源的上游许可证对闭源商业软件、专有产品和商业交付要求商业授权。当前仅登记和评估；在授权边界确认前，不将其作为公开商业成片的必经资源，也不把其衍生规则写入公开交付资产。
