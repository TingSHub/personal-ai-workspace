# pdf

> 管理资产：`.ai/skills/pdf/pdf.md`；安装实体：`.claude/skills/pdf/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | github · https://github.com/anthropics/skills (skills/pdf) |
| installed_ref | tree-sha256:d0f18af163b2 |
| runtime | both |
| 调用入口 | $pdf |
| 要求 | Skill 声明的 PDF/OCR 工具 |
| 更新 | git · 从上游仓库获取 skills/pdf 到临时目录，对比后替换安装实体；验证：提取一个最小 PDF 的文本并确认页数 |
| 辅助脚本 | — |
| 经验引用 | — |

PDF 处理能力：读取/提取文本表格、合并/拆分、旋转、水印、创建新 PDF、表单填写、加解密、图片提取、OCR。

## 来源

- 仓库：https://github.com/anthropics/skills（官方）`skills/pdf`
- 由 Resource Manager 管理

## 安装说明（licensing 注记）

- **License：Proprietary（source-available）**——LICENSE.txt（© 2025 Anthropic, PBC）含完整条款；个人/私有使用无碍，避免公开再分发
- 安装实体自带的 `scripts/` 属于第三方内容；本地辅助脚本如有新增，放入资源资产目录而不修改安装实体

## 使用

触发场景：任何 PDF 处理需求（.pdf 提及即触发）。实现方式：Python 库 + 命令行工具（详见 SKILL.md / REFERENCE.md / FORMS.md）。
