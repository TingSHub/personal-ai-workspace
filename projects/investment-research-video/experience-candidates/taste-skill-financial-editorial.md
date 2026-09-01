# Experience: taste-skill-financial-editorial

> Experience 是反馈，不是永久知识库：合格经验先判定归属，回写至 Workflow SOP 或 Skill/Agent 记录（by-name 回填 `experience_refs[]`），**回写完成后归档**至 `.ai/archive/experiences/`；`.ai/experiences/` 只存未完成回写的在途经验，不无限堆积。

## 来源证据

investagent-html-report Phase 3 rerun（2026-08-19，贵州茅台 600519）：
- taste-skill 首次真实项目应用（v2 experimental · commit dfb6f9f9e93a39f673b1827c0889cc28326d1800）：Design Read 声明、三拨盘（VARIANCE 5 / MOTION 3 / DENSITY 4）、palette-rotation、em-dash 清零、eyebrow ≤4、12 场景 9 布局族
- 上次运行（08-18）设计恰好落在 taste-skill 禁用的暖纸+brass 色族（#f4efe5/#b98a2f/#a61b29 全在禁令 hex 清单），换冷色 editorial 后通过全部 QA 门禁
- 证据见 `presentation-execution.md`「视觉方向（taste-skill 应用记录）」

## 触发场景

长文金融/企业研究 HTML deck 或报告页的视觉方向设计（Phase 3 视觉转译阶段）；任何「AI 生成的界面一看就是模板」的改进需求。

## 问题与归属判定

- 问题：LLM 默认审美（暖纸+brass 色族、等距卡片、eyebrow 泛滥、em-dash 连用、同一布局重复）在金融长文 deck 中同样出现；taste-skill 的规则族可消解，但需按金融内容边界裁剪。
- 归属（owner）：`.ai/skills/taste-skill/taste-skill.md` 注意事项 + experience_refs + 辅助脚本登记。

## 可复用结论（resolution）

1. 先声明 Design Read（页类/受众/语言/体系一句话），再定三拨盘：金融 editorial 取克制侧（VARIANCE 4-5 / MOTION 3 / DENSITY 4-5）。
2. Palette-rotation 真实有效：AI 默认暖纸+brass 色族有精确 hex 禁令清单，金融 deck 换冷色 editorial（冷灰纸+墨黑+单一红涨绿跌语义色）后设计质量与可读性均通过门禁。
3. 机械规则直接应用：em-dash 全页清零（脚本：`check-em-dash.py`，见 taste-skill 辅助脚本）；eyebrow ≤ ceil(场景数/3)；同页布局族不重复；形状一致（单一圆角系统）。
4. 金融内容边界 > taste-skill 激进指令：图像生成优先（单文件自包含约束冲突时跳过）、Go all out 类表达不适用于 Read 模式研究报告；红涨绿跌等财务语义由项目规则覆盖。

## 回写目标

- `taste-skill` skill 资产（`.ai/skills/taste-skill/taste-skill.md` 注意事项 + 辅助脚本登记 `scripts/check-em-dash.py` + 回写条目）

## 适用范围

- 长文金融/企业研究 HTML deck 与报告页的视觉方向；taste-skill v2 experimental（API 未锁定，升级需按 CHANGELOG 复验）

## 不适用范围

- dashboard/数据表格/多步产品 UI（taste-skill 明确 Out of Scope）；图表密集页仍以 html-ppt-skill + static-html-qa 为主；不替代内容边界与数值一致性检查

## 关联资产

- `taste-skill` · `html-ppt-skill` · `static-html-qa` · investagent-html-report workflow
