# toocoldcc-bagholder50

> 管理资产：`.ai/skills/toocoldcc-bagholder50/toocoldcc-bagholder50.md`；安装实体：`.claude/skills/toocoldcc-bagholder50/`（SKILL.md + references/data-schema.md + scripts/fetch_bagholder50.py + agents/openai.yaml）

## 元数据

| 字段 | 值 |
|---|---|
| name | toocoldcc-bagholder50 |
| kind | skill |
| description | 拉取并校验「韭菜50 / Bagholder 50」指数的公开 agent feed，返回最新成分股、排名、评分、当日收益与指数摘要；只读、无 API key |
| source | github · https://github.com/toocoldcc/bagholder50 · installed_ref `163f3837ff54113b8a345cc5504c298de884cac8`（main，2026-09-09 获取）· MIT License（Copyright 2026 toocoldcc 冷西西） |
| runtime | both（纯 Python 3 标准库 CLI，任何 agent 可调用） |
| invocation | 在安装目录内 `python3 -X utf8 scripts/fetch_bagholder50.py --view auto` |
| requirements | Python ≥ 3.10（本机 3.12.3）；无第三方依赖；出网可访问 `https://indices-toocoldcc.pages.dev` |
| update | git · 从 GitHub 重新取 `skills/toocoldcc-bagholder50/` 覆盖安装实体，保留本文件；verify：跑一次 `--view auto`，应 exit 0 且 `selection.status ∈ {ready, not_ready}` |
| scripts | `scripts/fetch_bagholder50.py`：拉取 + schema 校验 + 按北京时间与交易日历选择视图；需要最新成分股或指数摘要时使用 |
| experience_refs | — |

## 调用说明

### 作用与来源

读取 toocoldcc 发布的 Bagholder 50（韭菜50）指数 agent feed，输出 `index_summary`、`selection`（`signal_date` / `trade_date` / `status`）和 50 条成分股（`ts_code` / `name` / `today_return` / `bagholder_rank` / `bagholder_score`）。数据来自单一固定 HTTPS 端点，客户端拒绝自定义 URL 与重定向，限制响应 1MB，做两次重试，并校验 rank 连续、score 非递增、代码格式与日历哈希。

### 输出语义

- `selection.status=ready` 时按发布顺序报告 `index_summary` 与 `items`；小数收益率换算为百分比。
- `selection.status=not_ready` 是**正常发布状态**（退出码仍为 0），只报告 `selection.message`，不得改用旧名单或其他数据源。
- 命令非零退出时读 stderr 的 JSON 错误（`ENDPOINT_POLICY_VIOLATION` / `FETCH_FAILED` / `CALENDAR_INVALID` / `SCHEMA_MISMATCH` / `INVALID_JSON`），不得回退到别处取数。
- `selection.trade_date` 是该名单代表的交易日，`signal_date` 是对应收盘信号日；日期逻辑由客户端决定，调用方不要自行复算。

### 注意事项与踩坑

1. 本机没有 `python` 别名，必须用 `python3`（SKILL.md 允许换启动器）。
2. `--view auto` 的选择规则：交易日 15:00 前取当日视图，15:00 后与休市日取**下一个交易日**的 `avoid_tomorrow`。因此晚上运行时 `trade_date` 通常是次日。
3. `--view holdings_today` / `avoid_tomorrow` / `all` 属于诊断视图，不是「最新」，feed 也不是历史归档；不要用它们拼历史名单。
4. 该指数刻画的是**高拥挤度尾部**（bagholder 视角），成分股是「被套牢/拥挤」名单，**不是买入推荐**，也不是交易接口或收益保证。用于内容时必须保持这一语义，禁止转写为选股或买卖建议。
5. 方法论文档记基准日 2016-01-04、基点 1000，而 feed 的 `index_summary.latest_point` 2026-09-09 报 0.3273；两者换算口径未在 skill 中说明，引用点位时必须标注为 feed 口径，不要自行还原成方法论点位。
6. 该指数是**散户拥挤度反向理论指数**：四个因子（追涨热度 / 换手放大 / 龙虎榜次数 / 特大单净额）全部按「高值更差」方向等权合成，取横截面 Top50；`rank=1` 表示最拥挤、最需警惕。它测的是行为拥挤，不是股东户数或散户持股比例。

### 与选题的可能关系

可作为「拥挤度 / 情绪面」的旁证信号源，用于判断某个题材是否已经过度拥挤；它不能替代事件、公告或财务证据，也不能作为选题成立与否的判据。
