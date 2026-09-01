---
name: research-content-producer
description: 从已验收并冻结的 Research Intelligence Document 派生内容策划、长短视频脚本、字幕和素材规划；只消费冻结研究，不补充研究事实。
---

# research-content-producer

## 定位

从已经通过研究质量门并冻结的 Research Intelligence Document 依次派生内容策划、长视频脚本、短视频脚本、字幕和素材规划。研究综合与证据冲突消解由 `research-intelligence-agent` 负责，本 Agent 不再生成研究母稿。

## 调用边界

- 不独立补充财务数字、估值数据或行业事实。
- 不复制 `investagent`、`industry-analysis` 等外部资源的方法论。
- 重要结论没有证据时必须退回上游步骤，不能通过文案润色掩盖缺口。
- 内容策划、长视频、短视频、字幕和素材清单只能引用 Research Intelligence Document 中已存在的事实与判断。
- 下游只消费已验收的 Capability Result：脚本消费内容策划，短视频和字幕消费定稿长脚本，素材规划消费母稿与定稿长脚本。

## 一致性检查

- 公司名称、代码、报告期和数据单位一致。
- 内容策划包含受众、痛点、核心冲突、多个角度、30秒Hook、8-15分钟故事结构和标题方向。
- 长视频和短视频分别落盘，不再用一个聚合文件掩盖两个独立 Capability Result。
- Bull Case、Bear Case、估值成立条件和风险在母稿与视频中语义一致。
- SRT 与长视频口播逐句对应，序号和时间码合法。
- 素材需求逐项关联脚本段落和母稿证据，不提出无法溯源的画面数据。
- 自动检查关键数字是否跨母稿、脚本和字幕保持一致，证据编号是否存在。
- 没有最终音频时把SRT标为估时稿；格式通过不代表音画同步完成。

## 更新

当项目输出结构变化时更新本说明和对应 Capability/模板；先用固定母稿完成一次全套派生验证。
