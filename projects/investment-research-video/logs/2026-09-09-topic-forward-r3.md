# 2026-09-09｜选题前瞻重跑（TOPIC-R3 批次）

## 触发

用户批准「重跑一轮（2026-09-09）」，不用 2026-09-08 的 `TOPIC-R2-*` 待批卡。

## 实际执行

- `topic-forward-signal-scanner`：已执行；涨停池 48 只、涨幅榜 200 只，`errors` 为空（上一轮两路接口均 `ConnectionError`，本轮恢复）。
- `multi-search`：本地适配器网络检测把 Tavily 误判为不可用，最终全部失败；改用 workspace `.env` 的 Tavily 入口直连检索，20 组查询成功，记录写入 `multi-search.json` 并保留适配器失败详情。
- 公开原文核验：对航运、煤炭、粮食、DeepSeek、信息通信规划、黄金等关键前提逐条打开原文；发现「99 个转基因品种国审」实为 2025-04-08 旧闻，已剔除，不入卡。
- `finance-content-engineering` + `topic-angle-router-agent`：12 张卡各锁定一条 `content_line`、一个表达 Agent 与一种解释深度。
- `boundary-rewrite`：卡片合规词扫描无命中（买入/卖出/目标价/收益承诺等）。

## 产物

- 目录：`outputs/topic-forward/2026-09-09/`
- 卡片：12 张 `TOPIC-R3-*`，状态 `pending_approval`
- 门禁：`check-topic-angle-routing.py` → `PASS topic-angle-routing cards=12`
- 主线分布：market_pulse 3 / earnings_gap 2 / company_industry 5 / valuation_mechanism 2

## 未入卡 seeds 与原因

- 电网设备当日催化未找到原文，卡片以「板块信号已核实、催化待研究」形式入卡并标注。
- 中东局势与油轮遇袭：地缘军事题材，事实与合规风险高，暂不入卡。
- 鱼粉/饲料：单一来源、题材偏窄，暂不入卡。
- 转基因国审：来源为 2025-04-08，时效不成立，剔除。

## 脚本变更

`assemble-topic-forward.py` 原先把日期与 run id 硬编码为 `2026-09-08 / rerun-01`。本轮改为必填 `--date`、`--run-id`、`--topic-prefix`，并支持 `--resources` 传入执行记录表；默认行为不再写死某一轮。

## 下一闸门

用户从 `TOPIC-R3-01` 至 `TOPIC-R3-12` 中批准一张。批准内容是「研究对象 + content_line + 核心问题」，批准后原样移交 `topic-research`。
