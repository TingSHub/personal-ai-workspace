# boundary-rewrite

> 管理资产：`.ai/skills/boundary-rewrite/boundary-rewrite.md`；安装实体：`.claude/skills/boundary-rewrite/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | internal · 财经内容边界规则与用户确认案例 |
| installed_ref | internal · v0.1 |
| runtime | both |
| 调用入口 | 显式调用 `$boundary-rewrite`；财经脚本、标题和公共文案的边界审校 |
| 要求 | 已锁定的财经文本；不得改变事实、数字口径或证据强度 |
| 更新 | manual · 修改 `.claude/skills/boundary-rewrite/SKILL.md` 后同步本记录；验证：运行实体内测试样例并检查违规表达被改写 |
| 辅助脚本 | — |
| 经验引用 | — |

## 调用说明

将目标价、评级、买卖倾向和情绪化定性改写为边界内表达，保留事实张力和信息价值。允许区分第三方市场观点与本方建议，但不得把企业研究内容转化为交易指令。

本项目中由 `finance-content-engineering` 或 `financial-editor-agent` 先锁定事实，再进行表达边界审校；不能在 Phase 3 音频阶段自由改写。

## 跨项目使用边界

- 对财经研究、脚本、字幕、标题和公共文案均适用；项目 Workflow 只需声明当前产物是否属于企业研究内容。
- 规则扫描或改写不能替代事实核验，也不能把未裁决冲突、内部置信度或证据台账暴露到面向观众的产物。
