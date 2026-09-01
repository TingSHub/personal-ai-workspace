# zimeiti-persona-skills

> 管理资产：`.ai/skills/zimeiti-persona-skills/zimeiti-persona-skills.md`；安装实体：`.claude/skills/zimeiti-persona-skills/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | github · https://github.com/momozi1996/awesome-ai-persona-skills |
| installed_ref | ddb35e538b3b9e817e39f0ce0a9129b5c0a8f0c8 |
| runtime | claude |
| 调用入口 | 按风格读取 .claude/skills/zimeiti-persona-skills/{style}-skill/SKILL.md，以该文风身份执行内容表达 |
| 要求 | 内容事实必须来自已验收研究资产（research-intelligence/），文风是表达层，不改变事实；事实红线不变：PEG/失真分位/已证伪记忆/未落地政策在任何文风下禁用 |
| 更新 | git · 从上游仓库更新 zimeiti/ 目录，对比后替换安装实体，保留本地说明；验证：用一份已验收研究摘要分别按 2 个文风产出内容方案，核对事实未漂移 |
| 辅助脚本 | — |
| 经验引用 | — |

自媒体大 V 文风库：awesome-ai-persona-skills 仓库 zimeiti/ 目录（MIT 许可，二次创作保留出处），2026-08-15 正式注册（实测于 research-content-direction Phase 2 贵州茅台案例）。

## 12 个文风

| 风格 | 目录 | 特征 |
|---|---|---|
| 数字生命卡兹克 | shuzishengmingkazike-skill | 平实直接、数据碾压、自嘲幽默、Slogan 式干货 |
| 量子位 | liangziwei-skill | 数据驱动、速报+深析+智库三位一体、中性陈述 |
| 秋芝2046 | qiuzhi2046-skill | 爆款创作者风格 |
| 赛文乔伊 | saiwenqiaoyi-skill | 爆款创作者风格 |
| 硅星人 | guixingren-skill | 硅谷一线视角、中美双线叙事 |
| 新智元 | xinzhiyuan-skill | AI 科技媒体风格 |
| 机器之心 | jiqizhixin-skill | 技术深度媒体风格 |
| 极客公园 | jikegongyuan-skill | 科技媒体风格 |
| 量子位 / 李继刚 / 特工宇宙 / 赛博禅心 | liangziwei / lijigang / tegongyuzhou / saibochanshin | 各账号风格 |

## 实测结论（2026-08-15，贵州茅台案例，style-fit-assessment.md）

- 两套文风均不直接套用：卡兹克人设错位、量子位建制错位。
- **主文风选「卡兹克改造版」**：数据碾压 + 结论前置 + 自嘲式数据标注（与财务数字同构到近乎零改造）；情绪阶梯降档、自嘲限定标注场景、结尾留验证窗口不留买卖建议。
- **结构与纪律取量子位**：三层内容结构（快讯→深度→专题）+ 数字时间戳 + 多空并列中性陈述。
- 研究框架为骨、双风格元素为皮；事实红线（PEG/失真分位/已证伪记忆/未落地政策）在任何文风下不变。

## 调用

- 按风格读取 `{style}-skill/SKILL.md` 激活对应文风；未指定风格时默认卡兹克改造版。
- 文风是表达层：内容事实必须来自已验收研究资产（如 research-intelligence/），不新增研究事实、不联网补数据。
- 内容取舍只做筛选与表达组织，不改变研究事实。

## 注意事项与踩坑

- 人设类元素（AI 门童、100 人编辑部等）与投研克制存在错位，使用时必须降档改造。
- 数字必须回指 fact-map 的可信度分层：高可信数字可直接引用，低-中可信数字需标注口径，PEG/失真分位禁用。
- 结尾叙事可留验证窗口（如"批价 1550-1600 + 2026Q3 报表"），不写买卖建议。

## 更新

按 skill.yaml 从上游 GitHub 更新；更新后需重新验证文风质量与事实纪律。
