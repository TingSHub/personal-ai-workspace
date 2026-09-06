# humor-master

> 管理资产：`.ai/skills/humor-master/humor-master.md`；安装实体：`.claude/skills/humor-master/`

## 元数据

| 字段 | 值 |
|---|---|
| name | humor-master |
| kind | skill |
| description | 提供反转、比喻、自嘲、善意吐槽、节奏和幽默浓度控制等通用喜剧技法，用于财经口播的创意发散与局部润色 |
| source | github · https://github.com/caicai688/humor.skill |
| installed_ref | af8a082b55e666d825703beb80a68868f50347cd |
| runtime | claude / codex |
| invocation | `$humor-master`；仅在事实、论点和受众情绪判断完成后，以轻度模式生成若干幽默角度，再由主编选择并改写 |
| requirements | 必须先锁定事实和专业边界；不复制外部表演语料，不直接模仿具名喜剧演员；涉及真实难过、弱势群体或重大损失时关闭幽默 |
| update | git · 按上游仓库固定 commit 重新安装到 `.claude/skills/humor-master/`；verify：读取 SKILL.md 并用同一事实段落做低浓度幽默测试，检查事实漂移和过度表演 |
| scripts | — |
| experience_refs | — |

## 调用说明

这是三套里最强、也最容易压过账号主线的一套。把它当作“幽默技法库/创意审稿器”，不要作为默认人格注入整篇稿件；默认浓度应为轻，最多让一两个转折或比喻更有记忆点。它可以帮助解决行情低迷时的共情、行情普通时的轻松化表达，但不能把投资风险、事实证据和结论责任变成段子。

当前上游仓库根目录未确认到可用许可证，且其说明涉及大量外部表演语料；因此本登记只允许内部实验和机制评估，暂不用于公开商业成片、语料再分发或复制具体表演文本。许可证与语料来源确认后，再决定是否纳入生产工作流。
