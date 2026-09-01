# industry-report-generator

> 管理资产：`.ai/skills/industry-report-generator/industry-report-generator.md`；安装实体：`.claude/skills/industry-report-generator/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | skillhub · @user_aad6add3/industry-report-generator (https://skillhub.cn) |
| installed_ref | tree-sha256:88f1afd7ad8e |
| runtime | both |
| 调用入口 | $industry-report-generator |
| 要求 | network for current data；document generation dependencies |
| 更新 | reinstall · 从原 SkillHub 来源下载到临时目录，对比后替换安装实体；验证：生成一份最小 Word 报告并检查来源段落 |
| 辅助脚本 | — |
| 经验引用 | industry-research-methodology |

## 调用

- 入口：`$industry-report-generator`
- 适合需要八步结构和 Word 文档交付的行业研究项目。

## 注意事项与踩坑

- 开始前确认行业、地域和重点方向。
- 数据和判断必须标注来源；信息不足时明确说明，不生成看似精确的数字。
- 八步结构保证覆盖面，不替代对来源质量和结论逻辑的审查。
- 生成后检查 docx 能否打开、标题层级和来源清单是否完整。

## 更新

按 `skill.yaml` 从 SkillHub 重装，更新后生成一份最小 Word 报告验证。
