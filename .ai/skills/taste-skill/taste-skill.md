# taste-skill

> 管理资产：`.ai/skills/taste-skill/taste-skill.md`；安装实体：`.claude/skills/taste-skill/SKILL.md`（已安装，2026-08-19）

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | external · github: https://github.com/Leonxlnx/taste-skill |
| installed_ref | v2 (experimental，install name `design-taste-frontend`) · commit dfb6f9f9e93a39f673b1827c0889cc28326d1800（2026-08-19 拉取） |
| runtime | both |
| 调用入口 | 已安装：复制上游 `skills/taste-skill/SKILL.md` 至 `.claude/skills/taste-skill/`，由 Agent 按需加载（纯 Markdown 指令型，无运行时依赖）；上游安装方式：`npx skills add https://github.com/Leonxlnx/taste-skill --skill design-taste-frontend` |
| 要求 | 无运行时依赖；Section 4 要求环境中存在图像生成工具时优先用生成图做素材（无图像生成工具时跳过该条）；redesign 场景必须有既有品牌资产（logo/色/字体/摄影）作为起点 |
| 更新 | git 重拉取或 `npx skills add` 重装；验证：对照 CHANGELOG 确认 v2 API（安装名 / 三拨盘 / 章节结构）稳定后再升 stable |
| 辅助脚本 | scripts/check-em-dash.py（全页可见文本 em-dash/en-dash 扫描，taste-skill 零破折号规则的机械化检查；生成 deck/报告后必跑，退出码 0=无命中 / 1=有命中 / 2=用法错误） |
| 经验引用 | taste-skill-financial-editorial |

## 作用

Anti-Slop 前端设计 Skill（install name: `design-taste-frontend`）：布局、排版、动效、间距的去模板化设计方向指引。核心机制：先读 brief 推断设计方向（Design Read）→ 三拨盘配置（DESIGN_VARIANCE / MOTION_INTENSITY / VISUAL_DENSITY）→ 反 AI 默认清单（Inter+slate-900、紫色渐变、玻璃拟态、等距三卡片等禁令）→ 交付前 Pre-flight 检查。适用 landing / portfolio / redesign / editorial 页类。

## 来源

- github · MIT（LICENSE 在仓库根）
- 仓库内含 13 个子 Skill（taste-skill / imagegen-frontend-web / brandkit / brutalist-skill 等），主 Skill 是 `skills/taste-skill/`；v1 保留为 `taste-skill-v1`

## 用途

- 让 AI 生成的界面不显模板化：landing、作品集、重设计、editorial/长文页的视觉方向输入
- 反 AI 默认纪律与项目「结构服从信息，不服从模板」原则同向；长文企业研究报告按 editorial 页类适用
- 三拨盘可作为与 html-ppt-skill 设计 token 体系并列的视觉语言选择参考

## 注意事项与踩坑

- **适用范围明确排除**：dashboard / 数据表格 / 多步产品 UI 不在其范围——本项目 HTML 中图表与数据密集页面仍以 html-ppt-skill + static-html-qa 为主，taste-skill 只参与整体视觉方向（排版/间距/氛围）。
- **金融 editorial 应用（经验: taste-skill-financial-editorial）**：先声明 Design Read 再定三拨盘（金融长文取克制侧 VARIANCE 4-5 / MOTION 3 / DENSITY 4-5）；palette-rotation 真实有效——AI 默认暖纸+brass 色族（#f4efe5/#b98a2f/#a61b29 等）有精确 hex 禁令清单，冷色 editorial 换色后通过全部 QA；机械规则直接应用（em-dash 清零脚本、eyebrow ≤ceil(n/3)、布局族不重复、单一圆角系统）；金融内容边界 > 本 skill 激进指令（图像生成优先与单文件自包含冲突时跳过、Go all out 不适用于 Read 模式研究报告）。
- **v2 为 experimental pre-release**：API（安装名、拨盘名、章节结构）尚未锁定，升级需对照 CHANGELOG。
- **图像生成指令冲突**：Section 4「有图像工具必须用生成图」与单文件自包含（内联 CSS/SVG、无 CDN、本地可打开）约束冲突时，以项目约束为准；金融长文报告不以营销图为主。
- 与企业研究内容边界同向但需叠加：避免绝对化/营销化措辞与过度视觉冲击（与 impeccable 的 bolder/overdrive 同理，只取其克制侧）。

### 补充规则

- 2026-08-19：注册并安装外部 Skill（复制 SKILL.md 至 `.claude/skills/taste-skill/`，frontmatter 保持上游 `design-taste-frontend`）；investagent-html-report Phase 3 注记为可选资源。

### 补充规则

- 2026-08-19：真实项目验证（investagent-html-report Phase 3 rerun，贵州茅台 600519）——Design Read + 克制 dials + palette-rotation（弃用暖纸色族改冷色 editorial）后通过全部 QA 门禁；生成 `scripts/check-em-dash.py` 作为零破折号机械化检查。
