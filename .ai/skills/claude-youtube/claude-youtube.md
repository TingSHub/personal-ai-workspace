# claude-youtube

> 管理资产：`.ai/skills/claude-youtube/claude-youtube.md`；安装实体：`.claude/skills/claude-youtube/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | github · https://github.com/AgriciDaniel/claude-youtube |
| installed_ref | 84c3fa6 |
| runtime | claude |
| 调用入口 | 读取 skills/ 下 strategy/hook/script 子技能 SKILL.md 按其指示执行；英文方法论，产出可用中文 |
| 要求 | 英文词数/语速基准需换算中文（75 词/30s ≈ 140 字/30s；150wpm ≈ 280 字/分）；YouTube 平台机制（Shorts/中插广告/RPM）对 B站/抖音无效，只取方法论 |
| 更新 | git · 拉取上游新版本到临时目录审查后更新 vendor；保留本资源说明；验证：hook 子技能对一段中文财经内容产出 5 个 Hook 变体 |
| 辅助脚本 | — |
| 经验引用 | — |

## 作用

YouTube 增长顾问 skill（英文语境方法论）。本实验验证：strategy（Niche Authority 频道定位）+ hook（5 种心理机制变体，推荐 Curiosity-Gap，附流失风险/流量来源适配）+ script（Grab/Promise/Stakes 留存工程化，376 字中文脚本 + Retention Risk Map + Pattern Interrupt Log，事实核对 0 硬错误）。

## 调用

- 路径：skills/claude-youtube/sub-skills/{strategy,hook,script}.md + references/{retention-scripting-guide,algorithm-guide,analytics-guide}.md + templates/niche-authority-channel.md
- 执行：按 SKILL.md 协议依次 Context-Gathering → 频道类型检测（Niche Authority）→ strategy → hook（先读 retention guide）→ script
- 本实验产物：`projects/investment-research-system/experiments/listed-company-video-production/outputs/content/claude-youtube/`

## 调用注意事项

- **词数/语速必须换算**：75 词/30s ≈ 中文 140 字/30s（280 字/分）；150wpm ≈ 280 字/分。不换算时长估算偏差约 2 倍
- 平台机制基准（Shorts 2-3s 打断、8 分钟中插广告、RPM/CPM、US 观众留存 55%/20%/68%）对 B站/抖音/视频号无效——只取方法论，不引用其基准数字
- DataForSEO/YouTube API 无凭据时资源自带回退（"Never block a workflow"，用参考文件基准并标注）
- "AI 配音掉 70% 留存"等结论在中文语境无本地实证，引用需谨慎

## 常见失败原因

- Hook 定义为前 30 秒（约 75 英文词）——60-90 秒视频里 Hook 占 1/3 偏长，需按 script.md"按目标时长计算分段"压缩
- 产出偏"英文 YouTube 运营"视角（频道增长/SEO），财经内容只取其叙事结构层
- 个别叙事判断（如"AI 概念正热"）超出研究口径——引用其输出后必须做口径核验（本实验 FACT-CHECK 记录 5 项）

## 最佳实践

- **Retention Risk Map 是全生态最工程化的留存设计**：每个时间点写"为什么流失+怎么缓解"，可直接吸收为自研脚本规范
- Curiosity-Gap 对"增长 vs 质量"双叙事题材天然适配（数据层双重叙事，缺口来自事实结构）
- 其"证据优先、避免 clickbait 伤 Quality Click Ratio"原则与财经红线方向一致——合规最省心的候选
- 策略层（微领域起步+常青搜索定位）可用于频道定位决策
