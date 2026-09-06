# witty-blog-voice

> 管理资产：`.ai/skills/witty-blog-voice/witty-blog-voice.md`；安装实体：`.claude/skills/witty-blog-voice/`

## 元数据

| 字段 | 值 |
|---|---|
| name | witty-blog-voice |
| kind | skill |
| description | 用文明毒舌、反讽、自嘲、夸张和短节奏，把已有观点或事实稿改得更有锋芒、更像人在说话 |
| source | github · https://github.com/houguofei/witty-blog-voice |
| installed_ref | a5f4cddd85eac3486bd2da550b435ebc458a4ce7 |
| runtime | claude / codex |
| invocation | `$witty-blog-voice`；在事实和主论点冻结后，对标题、开头、转折和结尾做轻量幽默化改写 |
| requirements | 必须有原始草稿或已验收事实；不得改动数据、结论和合规边界；使用机制而非冒充特定作家 |
| update | git · 按上游仓库固定 commit 重新安装到 `.claude/skills/witty-blog-voice/`；verify：读取 SKILL.md 并用一段已冻结稿件完成“轻度锋利化”对照测试 |
| scripts | — |
| experience_refs | — |

## 调用说明

适合做表达层的中等强度增味：把“报告式陈述”改成有观察、有反差、略带自嘲的口播，优先作用于开场、段间转折和收束，不建议整篇高浓度使用。财经视频中要把攻击对象从具体个人转为现象、机制或自己的误判；事实、数字、来源和判断强度必须原样受控。

上游仓库标注 MIT 许可证。仅迁移反讽、节奏、比喻和共情机制，不复制原句，不做现实人物的直接风格冒充。与 `renwei-writing` 配合时，最后做一次“是否为了好笑而损失人味或准确性”的回查。
