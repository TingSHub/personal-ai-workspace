# 2026-09-08｜选题前瞻重新跑通

## 纠正

上一轮误把 `2026-09-06-rerun-01` 的 10 张 `TOPIC-R1-*` 卡当成新结果。本轮从 2026-09-08 重新执行发现、去重、路由和卡片组装；旧批次不作为本轮结果。

## 实际执行

- `topic-forward-signal-scanner`：已执行；涨停池和全量行情接口均 `ConnectionError`，错误保留在新目录 `signals.json`。
- `multi-search`：已执行；三组查询因 DuckDuckGo、Bing、Tavily 均不可用返回空数组，结果保留在 `multi-search.json`。
- 公开原文轻量核验：使用 2026-09-08 盘面报道，以及工信部 6G、网信办数字化绿色化、市场监管总局质量月等政策原文，线索和研究缺口写入 `editorial-leads-2026-09-08.json`。
- `finance-content-engineering`：按 topic-gen 规则形成 12 个互斥问题，先锁主线再写标题。
- `topic-angle-router-agent`：生成 `topic-angle-matrix.json`，12 张卡各只有一条主线、一个表达 Agent 和一个解释深度。
- `boundary-rewrite`：卡片保留可验证冲突，删除交易指令、目标价和收益承诺。

## 验收结果

- 新目录：`projects/investment-research-video/outputs/topic-forward/2026-09-08-rerun-01/`
- 新卡数量：12；ID 全部为 `TOPIC-R2-*`；与旧 `TOPIC-R1-*` ID 重叠数为 0。
- `check-topic-angle-routing.py`：`PASS topic-angle-routing cards=12`。
- 状态：`pending_approval`；未进入 `topic-research`、脚本、配音、渲染或发布。

## 下一闸门

用户批准一个 `TOPIC-R2-*` 后，才把该卡原样移交 `topic-research`；旧的 `TOPIC-R1-*` 批次不再作为本轮选择入口。
