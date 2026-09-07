---
name: research-quality-gate
description: 验收上市公司 Research Intelligence Document，或检查冻结研究底稿、视频脚本、SRT、素材清单和证据链的一致性与完整性。只检查、不补研究、不生成内容；当研究流水线交付前需要质量门禁或跨文件一致性检查时使用。
---

# Research Quality Gate

## 边界

- 只验收已有产物，不补数据、不改结论、不润色脚本。
- 硬检查由 `scripts/validate_research.py` 执行；语义检查由当前 Agent 对照母稿逐条复核。
- 发现问题时输出位置、证据和修复方向，把产物退回对应上游 Capability；不要在门禁内直接修复。
- `PASS` 表示已执行的检查未发现阻断项，不代表投资结论正确，也不替代人工事实核验。

## 输入

研究阶段只需提供 Research Intelligence Document。内容派生阶段必须提供同一版本的：

1. Research Intelligence Document（新研究流程）或历史 Research Master Document（兼容内容回归）
2. 内容策划、长视频脚本和三至五个短视频脚本；旧版聚合长短脚本仍兼容
3. SRT 字幕
4. 视频素材需求清单
5. evidence ledger（可与母稿第 8 章为同一文件）

## 执行

研究阶段先运行：

```bash
python3 scripts/validate_research.py \
  --research-intelligence <research-intelligence-document.md> \
  --output <research-quality-report.md>
```

内容派生阶段运行：

```bash
python3 scripts/validate_research.py \
  --master <research-intelligence-document.md> \
  --narrative-plan <content-narrative-plan.md> \
  --long-script <video-script.md> \
  --short-scripts <short-video-script.md> \
  --subtitles <subtitles.srt> \
  --materials <material-plan.md> \
  --evidence <evidence-ledger.md> \
  --output <quality-report.md>
```

旧项目可继续使用 `--scripts <聚合长短脚本.md>`，不能与三项 Content Layer 输入混用。新项目优先使用独立输入，确保每个 Capability Result 可单独验收。

若输入标记 `content_depth=deep_explainer`，在通用自动检查后必须增加以下语义门禁：

- `Knowledge Map` 存在，并能从普通观众直觉、必要术语、证据到判断变化形成完整路径；不能用术语清单代替；
- `Historical And Market Relation` 存在，并至少区分历史事实、市场叙事/观点和编辑推断；周期题不能只给当前价格点；
- 涉及行业股价时，至少有一段带时间窗口和来源的“价格—利润—市场预期”关系材料；允许定性趋势，不允许无来源的涨跌故事；
- 新闻事实包含事件日、主体、动作和机制意义；“市场传闻/某股上涨”不能独立作为证据；
- 主要幽默点能回指事实、观众误读或数字反差，并在笑点后回到机制、证据或验证条件；无事实锚点的段子退回表达层；
- 深度素材不足时只能降低为 `standard` 并记录原因，不能在脚本层自行补历史或股价事实。

Research Intelligence 检查：十章、Bull/Base/Bear、Evidence Ledger 的 claim/source/date/confidence/notes 字段及研究阶段边界。内容回归检查继续兼容历史母稿八章节、证据引用、内容策划、长短视频结构、数字一致性、禁语、SRT与素材引用。

随后完成语义复核，并把结果追加到同一 `quality-report.md`：

- 脚本是否出现母稿没有的新事实或新增因果关系。
- 是否把预测、推断或弱信号改写成确定事实。
- 是否删弱 Bear Case、风险影响或观察指标。
- 是否出现收益承诺、单向吹捧或直接买卖建议。
- 素材画面是否可能暗示母稿未支持的事实。

## 输出判定

- `FAIL`：存在缺文件、缺核心章节、未知证据、跨文件新增数字、投资建议化禁语、SRT 格式/时序错误等阻断项。
- `PASS WITH WARNINGS`：无阻断项，但存在需要人工确认的语义风险或资料缺口。
- `PASS`：无阻断项且语义复核无待办。

输出必须列出每项检查的通过/失败、文件定位、问题归属 Capability 和建议回退步骤。
