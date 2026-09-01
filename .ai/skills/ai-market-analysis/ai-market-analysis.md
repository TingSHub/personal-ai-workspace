# ai-market-analysis

> 管理资产：`.ai/skills/ai-market-analysis/ai-market-analysis.md`；安装实体：`.claude/skills/ai-market-analysis/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | skillhub · @user_cf06cb04/ai-market-analysis (https://skillhub.cn) |
| installed_ref | tree-sha256:49c587ba8f1f |
| runtime | both |
| 调用入口 | $AI-market-analysis |
| 要求 | — |
| 更新 | reinstall · 从原 SkillHub 来源下载到临时目录，对比后替换安装实体；验证：加载 Skill 并完成一次主题路由验证 |
| 辅助脚本 | — |
| 经验引用 | industry-research-methodology |

## 调用

- 入口：`$AI-market-analysis`
- 先按用户主题选择已安装资源中的对应 reference，再结合当前项目数据使用框架。

## 注意事项与踩坑

- 这是框架库，不是实时数据源；所有时间敏感结论仍需检索和项目证据。
- ICT 基础设施实测没有完全对应的专用框架，可用 AI 框架补充，但不能把框架覆盖当成行业证据。
- 公司问题应先映射到具体行业，再选择框架。

## 更新

按 `skill.yaml` 的 update 说明从 SkillHub 重装；更新后至少验证一次主题路由和 reference 读取。
