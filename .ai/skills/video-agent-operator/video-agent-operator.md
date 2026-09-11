# video-agent-operator

> 管理资产：`.ai/skills/video-agent-operator/video-agent-operator.md`；安装实体：`.claude/skills/video-agent-skills/video-agent-operator/`。复用 video-agent-skills 内的现有子 Skill，不另装副本。

## 元数据

| 字段 | 值 |
|---|---|
| name | video-agent-operator |
| kind | skill |
| description | 基于已提供的账号指标与内容证据分析视频表现、比较历史基线并形成运营改进候选 |
| source | external · https://github.com/chenyuxiaojin/video-agent-skills · 子目录 video-agent-operator；父资源 video-agent-skills |
| installed_ref | 父资源登记为 fc80890（本次未重新核验远端）；当前 SKILL.md SHA-256：11cfbaf1b18608cc3426e82064fffbca0ac74dfa3233e3a61e03f7789b70e59e |
| runtime | both（读取指令执行；不依赖子 Agent 自动调度） |
| invocation | 读取安装实体 SKILL.md，按实际分析任务选择参考文件，消费已验收数据并留下分析产物；publish-review 调用时遵循其 diagnostics 阶段契约 |
| requirements | 真实账号数据、指标定义与采集时间、当前账号定位及可用历史对照；按输入格式选择 CSV/Excel/JSON 读取工具；无数据时报告缺项 |
| update | method：git；instructions：随 video-agent-skills 从上游取到临时目录，比较本子模块指令、脚本与参考文件，保留本地记录；verify：以小样例核对指标、缺失值和输出，再更新父子版本记录 |
| scripts | 无已实现的内置分析入口；三个 scripts/*.py 均为 0 字节，见调用限制；无新增本地辅助脚本 |
| experience_refs | — |

## 调用说明

- 按名称解析到本记录，再读取现有安装实体。账号以项目提供的实际定位为准；上游 growth/ai/vlog 账号设定不自动成为当前项目配置。
- 单账号指标计算与历史对照时读取 `references/metrics-guide.md`；仅在确需理解上游预设账号时读取 `references/account-profiles.md`。基准区间仅作辅助，具体分析以同账号、同类型内容及可比较观察窗口为依据。
- publish-review 已提供 JSON 时直接读取并核对字段口径，无需为套用 CSV 示例丢弃详情数据。具体输出位置、漏斗定义和验收条件由该 Workflow 管理。
- 缺失指标标明缺失；分母为零时标明不可计算。观察、归因假设和改进建议分开，不能凭相关性声称已证实原因。
- 分析需实际消费输入并留下可核对的计算与证据。只阅读方法论不算执行；可用当前执行环境计算，回执注明工具和数据来源，不声称使用了未实现的内置脚本。
- 选题建议交上游决策；经验回写通过 Experience Curator 和 Resource Manager，不直接修改外部安装实体。

## 已知限制与验证

- 2026-09-11 本地检查：`analyze_performance.py`、`generate_topics.py`、`analyze_competitors.py` 均为 0 字节。执行它们即使返回成功也不会完成分析，不作为生产入口或通过验收的依据。
- 飞书 API 与竞品自动采集在上游指令中是未来能力，本次登记不将其视为可用接口。
- 本次完成安装入口、参考文件、脚本内容和 Workflow by-name 解析检查；未执行真实账号分析，也未验证生产输出质量。
- 后续更新最小行为验证：使用明确标注的合成样例（播放 100、点赞 10、评论 2、收藏 3、分享 5），确认互动率为 20%；加入零播放和缺失指标案例，确认不伪造比率或因果结论。若新版实现内置脚本，还需实际调用其入口验证；通过后才将其登记为可用脚本。
