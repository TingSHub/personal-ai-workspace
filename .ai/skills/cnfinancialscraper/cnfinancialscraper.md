# cnfinancialscraper

> 管理资产：`.ai/skills/cnfinancialscraper/cnfinancialscraper.md`；安装实体：`.claude/skills/cnfinancialscraper/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | skillhub · community @user_9d5a2a39 |
| installed_ref | v4.9.0 |
| runtime | both |
| 调用入口 | unavailable |
| 要求 | — |
| 更新 | reinstall · 如需恢复，从原 SkillHub 来源下载到临时目录并重新验证 orgId；验证：使用已知 A 股代码验证公告搜索与 PDF 下载 |
| 辅助脚本 | — |
| 经验引用 | financial-analysis |

当前安装实体已归档。原资源的 cninfo `orgId` 硬编码会对部分 A 股代码产生错误，公告和年报获取已由 `cninfo-connector` 替代。

如需恢复，按 `skill.yaml` 从原 SkillHub 来源重新安装，并用已知代码验证公告搜索与 PDF 下载；未经验证不得重新加入 Capability 候选。
