# dazhiruoyu

> 管理资产：`.ai/skills/dazhiruoyu/dazhiruoyu.md`；安装实体：`.claude/skills/dazhiruoyu/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | skillhub · @user_99a25c17/dazhiruoyu (https://skillhub.cn) |
| installed_ref | tree-sha256:2b6016dd35a0 |
| runtime | both |
| 调用入口 | $market-research |
| 要求 | Python report dependencies for PDF output |
| 更新 | reinstall · 从原 SkillHub 来源下载到临时目录，对比后替换安装实体；验证：生成一份最小 PDF 并检查文件可打开 |
| 辅助脚本 | — |
| 经验引用 | industry-research-methodology |

## 调用

- 入口：`$market-research`
- 适合需要市场空间、竞争、进入策略和 PDF 交付的项目。

## 要求

- PDF 生成依赖以安装实体中的 requirements 为准。
- 生成前确认主题、地域和重点问题；公开数据不足时必须标注推测。

## 注意事项与踩坑

- TAM/SAM/SOM 阈值和进入门槛不能机械套用，B 端重资产行业尤其需要校正。
- PDF 脚本需要 reportlab/PyPDF2；复杂图表优先改用表格或文字说明。
- 真实项目中十二章节可以完整交付，但质量仍取决于来源与数据可得性。

## 更新

按 `skill.yaml` 从 SkillHub 重装，并用最小 Markdown 输入验证 PDF 可生成和打开。
