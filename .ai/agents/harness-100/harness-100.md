# harness-100

> 管理资产：`.ai/agents/harness-100/harness-100.md`；安装实体：`.agents/harness-100.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | agent |
| 来源 | github · https://github.com/revfactory/harness-100 |
| installed_ref | 8e8d35c |
| runtime | claude |
| 调用入口 | 拷贝 en/01-youtube-production/.claude/agents/*.md 角色文件，按角色 system prompt 身份执行（单代理顺序扮演已验证；原生 5-agent 团队未测） |
| 要求 | 角色文件全英文，中文语速约定（280 字/分）需外部补入；thumbnail-designer 依赖 gemini-3-pro-imagegen skill（未安装时只能出文字概念） |
| 更新 | git · 拉取上游新版本到临时目录审查后更新 vendor；保留本资源说明；验证：content-strategist + scriptwriter 对一份中文素材产出策略简报与口播稿 |
| 辅助脚本 | — |
| 经验引用 | — |

## 作用

100 个生产级 agent harness 集合。本实验验证 01-youtube-production：content-strategist（策略简报 7 块格式）+ scriptwriter（298 字中文口播稿，Hook 用"反差陈述+震撼数字"组合公式，含 Visual Cue/Editing Note）+ production-reviewer（交叉校验，事实核对 0 硬错误）。

## 调用

- 路径：`en/01-youtube-production/.claude/agents/{content-strategist,scriptwriter,production-reviewer,seo-optimizer,thumbnail-designer}.md` + skills/{youtube-production,hook-writing,thumbnail-psychology}
- 执行：以角色 system prompt 身份顺序扮演（本实验验证路径）；角色自带 Error Handling 降级路径（web search 失败/API 缺失均可继续）
- 本实验产物：`projects/investment-research-system/experiments/listed-company-video-production/outputs/content/harness-100/`

## 调用注意事项

- 角色文件全英文、默认 5-15 分钟 YouTube 长视频假设（Segment <2 分钟、Hook 0:00-0:30）——60-90 秒需自行压缩时间码与段落数
- 无中文字数/语速约定（"other languages may vary"）——中文需外部补 280 字/分
- scriptwriter 要求先读 strategist 简报（角色间交付顺序不能乱）
- thumbnail-designer 依赖 gemini-3-pro-imagegen skill（未安装时只能出文字概念）
- 原生 5-agent 团队（SendMessage 交付流）本实验未验证——单代理扮演下团队协议为纸面收益

## 常见失败原因

- 把英文 150 词/分直接套中文会整体偏差约 2 倍（时长估算）
- 角色要求 web search 竞品调研时无网络会走降级路径（输出标注数据限制）——可用冻结素材替代
- production-reviewer 的严重度分级与一致性矩阵是自检模板，不要跳过

## 最佳实践

- hook-writing skill 的 15 种模式 + 组合公式（反差陈述+震撼数字）是全场最可移植资产，直接套中文财经 Hook
- 角色文件作为"角色定义范式"参考：模板化交付物格式（策略简报/脚本分段/复核矩阵）可直接吸收进自研角色
- 提取方式 `cp -r` 拷贝 .claude 目录即可，独立使用无仓库依赖
