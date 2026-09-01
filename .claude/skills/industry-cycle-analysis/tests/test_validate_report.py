from __future__ import annotations

import re
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

from validate_corpus import audit  # noqa: E402
from validate_report import validate  # noqa: E402


CAPITAL_CYCLE_BLOCK = """### 5.1 资本周期交叉校验

- 观察节点：核心部件制造与认证产能，不把整个示例行业合并为单一节点。
- 资本开支方向：2025H1 至 2026H1 资产增加继续上升，方向依据 E3、E6。
- 资本开支口径：甲公司合并口径资产增加额，按自然年比较；不等同现金支付或管理层指引（E3）。
- 资本开支性质：增长性与维护性混合且未拆分，因此不能把总额全部视为新增产能。
- 回报代理：2025H2 至 2026H1 单位利润同比增加 8%，并以毛利率复核（E5、E6）。
- 口径可比性：资本开支主体和自然年可比；单位利润分子与分母统计范围不变，但与集团净利润不可比。
- 供给兑现时滞：资产增加后仍需安装、客户认证、良率爬坡和连续交付，当前估计需要两个至三个季度。
- 交叉判断：资本开支上升且回报改善支持健康扩张假设，但仍需订单、库存、交期和利用率共同确认。
- 反证条件：若订单覆盖低于一倍且库存连续两个季度上升，即推翻健康扩张判断。

"""


def valid_report(timestamp: datetime | None = None) -> str:
    timestamp = timestamp or datetime.now(timezone(timedelta(hours=8)))
    nodes = []
    for index, name in enumerate(("矿物提纯", "核心部件", "整机集成", "终端运营"), start=1):
        nodes.append(
            f"""#### 1.2.{index} {name}

**它是干什么的**：节点{index}把特定物料和工艺转成可验收产品，决定下游能否按计划投产并持续运行。

**向谁采购**：节点{index}向专业材料商、关键设备制造商和能源服务机构采购不同投入品。

**卖给谁**：节点{index}向下一制造环节、系统集成商以及具备明确预算的终端运营者销售。

**代表企业**：

| 企业/机构 | 上市地/代码或属性 | 角色 | 产能/生产控制方式 | 代表性依据 | 证据 |
|---|---|---|---|---|---|
| 节点{index}甲公司 | 上交所 / 60000{index} | 主要供应商 | 自有工厂并控制认证产线 | 已披露产品收入和客户结构 | E{index} |
| 节点{index}乙机构 | 未上市/机构 | 行业运营者 | 委外生产并以长协锁定合格产能 | 发布持续运营及招标数据 | E{index + 4} |

**怎么赚钱、议价能力**：节点{index}依靠合格产能利用率、良率和服务附加值取得毛利；只有认证稀缺时才有提价能力。

**为什么会卡住**：节点{index}受认证周期、熟练人员和专用设备交付约束，名义产能不能直接等同有效供给。

**进阶视角**：节点{index}的领先指标不是规划产能，而是认证通过后连续交付与单位利润同步改善；若只有订单没有良率，利润不会兑现（E{index}、E{index + 4}）。
"""
        )

    ledger_rows = []
    publishers = ("国家统计局", "行业协会", "甲公司年报", "交易所", "能源署", "海关", "乙机构", "研究院")
    for index, publisher in enumerate(publishers, start=1):
        ledger_rows.append(
            f"| E{index} | {publisher} | 指标或披露 {index} | https://example.com/source-{index} | 第{index}页 | 2026-07-18 | yes | 当前 | 口径仅覆盖样本{index} |"
        )

    return f"""# 示例行业供需周期分析

分析日期：{timestamp.isoformat(timespec="seconds")}
地理范围：全球，并对中国市场单列说明
数据时效：截至分析日期已经正式发布的原始资料
行业边界：从上游原料到终端运营，不包含纯金融交易

## 0. 一页看懂

### 这个行业是做什么的
该行业把稀缺物料转成终端可以持续使用的工业系统，收入由真实交付和运行服务共同形成。

### 三个最重要的数字
1. 2025 年有效供给为 120 单位（E1）。
2. 2025 年真实需求为 116 单位（E2）。
3. 2026 年已公告但未认证产能为 30 单位（E3）。

结论状态：可发布
周期阶段：上行确认
置信度：中
证据截至时间：{timestamp.isoformat(timespec="seconds")}
上调条件：订单覆盖连续两个季度高于 1.5 倍且单位利润继续改善
下调条件：终端使用量转负且认证产能集中释放

## 1. 产业链地图

```mermaid
flowchart LR
  A[矿物提纯] --> B[核心部件] --> C[整机集成] --> D[终端运营]
```

### 1.1 钱和订单怎么走
终端运营者依据实际使用量付款，整机集成商再用验收回款覆盖部件和原料采购。

{''.join(nodes)}

### 1.3 权力与利润传导

| 问题 | 回答（必须点名具体环节和企业，禁止通用套话） | 证据 | 缺口 |
|---|---|---|---|
| 谁最终付款？ | 使用客户向终端运营者付款，运营者再覆盖集成、部件和提纯采购。 | E2 | 细分合同未完全披露。 |
| 付款方资金来源与预算持续性 | 终端运营者以经营现金流、存量现金和债务融资支付；若自由现金流转负、融资成本上升或资本开支指引下调，预算即出现可观测收紧。 | E2、E5 | 未披露按产品拆分的已承诺预算。 |
| 利润当前集中在哪个环节，为什么？ | 认证产能稀缺时利润集中于核心部件，交付正常化后向集成与运营移动。 | E3、E5 | 分部利润口径不可完全比较。 |
| 谁承担资本开支和库存风险？ | 核心部件公司承担扩产和良率风险，集成商承担库存及验收回款风险。 | E3、E6 | 供应链融资条款未公开。 |

## 2. 需求

### 2.1 政策重要性闸门

- 政策是否实质驱动当前周期：否
- 判断依据：当前需求由终端使用和认证交付驱动，政策只是背景变量（E2）。
- 主要作用通道：不适用；已检查需求、供给和准入
- 政策状态截至：{timestamp.isoformat(timespec="seconds")}

需求由存量替换、终端新增利用量和安全冗余共同推动，不能把意向订单直接计入已经发生的采购（E2）。

**进阶视角**：当使用量增速高于预算增速时，运营者会先消化闲置资源；预算、招标和验收连续出现才能确认需求进入兑现阶段（E2、E5）。

## 3. 供给

供给必须区分公告、开工、安装、认证与稳定良率，只有最后两项才能形成短期有效产能（E1、E3）。

| 供给动作 | 公告或计划 | 已安装/已投产 | 已通过量产与客户认证 | 订单支撑、性质与可撤销性 | 当前有效性 |
|---|---|---|---|---|---|
| 核心部件扩产 | 计划增加 30 单位 | 已安装 12 单位 | 8 单位完成客户认证 | 已有采购订单，但预付款、长协及取消条款未披露；存在多头下单风险（E3） | 仅认证部分计入有效供给 |
| 集成产线升级 | 计划改造两条线 | 一条已投产 | 已通过首批验收 | 框架意向不代表不可撤销硬订单，重复下单比例仍是公开缺口（E4） | 只能计入已验收部分 |

**进阶视角**：新增厂房只改变远期供给上限，认证和良率爬坡决定当期交付；设备到位而人员不足仍会造成供给延迟（E1、E3）。

## 4. 供需矛盾与高频信号

| 信号 | 当前读数 | 解释 | 证据 |
|---|---|---|---|
| 终端使用量 | 同比增加 12% | 使用量快于存量释放，需求真实改善 | E2 |
| 订单覆盖 | 1.4 倍 | 可见度增加但仍需观察取消率 | E3 |
| 交付周期 | 18 周 | 认证资源紧张形成排队 | E4 |
| 单位利润 | 同比增加 8% | 供需改善开始进入利润表 | E5 |
| 在制库存 | 环比下降 4% | 交付快于投料，尚未形成积压 | E6 |

## 5. 周期位置与传导

| 阶段/日期 | 性质 | 信号 | 利润池往哪移 | 关键时滞 | 证据 | 下一步验证 |
|---|---|---|---|---|---|---|
| 2024H2 去库存 | 已发生 | 终端使用温和增加 | 运营端 | 一个季度 | E2 | 库存下降 |
| 2025H1 修复 | 已发生 | 利用量加速而认证偏慢 | 核心部件 | 两个季度 | E3 | 利润企稳 |
| 2025H2 上行确认 | 已发生 | 订单兑现且供给受限 | 认证产能 | 三个季度 | E4 | 交付延长 |
| 2026H1 风险检验 | 风险窗口 | 公告产能进入认证 | 集成与运营 | 半年 | E6 | 良率和库存 |

**进阶视角**：与上轮只靠补库存不同，本轮需要终端使用量和认证交付共同成立；利润先于大规模扩产改善才是有效收紧（E5、E6）。

{CAPITAL_CYCLE_BLOCK}

什么会证明这个判断错了：终端使用量连续下降，同时新增认证产能提前释放并造成库存回升。

## 6. 资金动向

| 尝试的来源类型 | 具体来源 | 结果（拿到数据 / 无公开数据 / 口径不可比） |
|---|---|---|
| 行业指数估值分位 | 示例产业指数发行商 | 拿到 2026-07-17 估值数据 |
| 行业 ETF 份额/资金流 | 示例 ETF 发行商 | 拿到 2026-07-17 NAV 和份额 |
| 龙头股价与盈利剪刀差 | 甲公司 IR | 拿到 2026Q1 盈利与同期市场指标 |

| 代理层级（行业/子链/公司） | 工具/主体 | 覆盖节点 | 指标与期间 | 来源 | 结论 | 局限 |
|---|---|---|---|---|---|---|
| 行业 | 示例 ETF | 全链上市公司 | 2026-07-17 NAV 120.5，年内回报 12.0% | E7 | 叙事已扩散 | 不代表未上市供应商 |
| 公司 | 节点甲公司 | 核心部件 | 2026Q1 利润同比增长 8% | E3 | 盈利开始兑现 | 单一公司样本 |

产业现实是利润先在认证稀缺的部件端改善，估值反应是否充分需要与可比公司的订单兑现交叉验证。

- 市场当前大概率**已定价**：订单增长与当前利润改善。
- 市场当前大概率**未定价**：新线认证良率与取消风险。

### 6.3 估值口径校准

不能用静态低 PE 直接判断便宜：利润高点会机械压低市盈率，利润低点会抬高或使其失真。估值必须与毛利率和利润所处位置、产品价格、库存及产能利用率一起核验；当前缺少同口径历史分位，因此只保留口径不可比的数据缺口（E3、E5）。

### 6.4 隐含预期反推

| 反推方法 | 已知输入 | 关键假设 | 反推出的门槛 | 产业证据对照 | 证据与局限 |
|---|---|---|---|---|---|
| PE桥接 | 2026-07-17 价格100元；2026Q1正常化每股收益EPS 2元 | 5年期限、必要回报率10%、中周期退出倍数20倍 | 第5年EPS需达到8.05元，复合增速约32.1% | 证据不足：订单和有效供给尚不能支持连续五年该增速 | E3、E5、E7；情景推算，不输出目标价 |

## 7. 未来资金可能流向

| 情景 | 触发条件 | 利润池往哪个环节移动 | 先受益的环节 | 后受益/受损的环节 | 需要盯的证据 |
|---|---|---|---|---|---|
| 基准 | 认证按计划完成 | 核心部件向集成移动 | 核心部件 | 集成受益、低效产能受损 | 认证和交付 |
| 上行 | 终端使用超预期且设备延后 | 稀缺认证产能 | 核心部件 | 运营端后受益 | 订单和交期 |
| 下行 | 新增产能集中认证 | 现金流稳定的运营端 | 运营服务 | 高库存部件受损 | 库存和利润 |

以上情景不构成任何买卖建议。

## 8. 分歧与反证

主流叙事强调规划产能足够；本报告认为短期有效供给取决于认证、人员和良率，二者应由交付周期验证。

## 9. 观察哨与跟踪

| 指标 | 基线 | 来源 | 频率 | 正向触发 | 反证触发 |
|---|---|---|---|---|---|
| 终端使用量 | 2025 年 116 单位 | 行业协会 | 月度 | 三个月同比加速 | 三个月同比转负 |
| 认证产能 | 2025 年 120 单位 | 公司公告 | 季度 | 增速低于需求 | 集中提前释放 |
| 交付周期 | 2025 年末 18 周 | 交易所问询 | 季度 | 延长且利润改善 | 缩短且库存上升 |
| 单位利润 | 2025 年 8 元 | 公司年报 | 季度 | 连续两个季度上升 | 连续两个季度下降 |
| 在制库存 | 2025 年 32 单位 | 统计机构 | 月度 | 下降且交付增加 | 上升且订单减少 |

### 9.1 可比时间序列

| 指标 | 时点 | 数值 | 单位 | 证据 |
|---|---|---:|---|---|
| 终端使用量 | 2024 | 104 | 单位 | E2 |
| 终端使用量 | 2025 | 116 | 单位 | E2 |

## 10. 术语表

| 术语 | 解释 |
|---|---|
| 有效产能 | 已认证并能以稳定良率交付的产能 |
| 在制库存 | 已投料但尚未完成验收的产品 |
| 订单覆盖 | 在手订单相对当前收入的倍数 |

## 附录A 证据台账

| 证据ID | 发布方 | 材料 | URL | 定位 | 访问日期 | 已打开 | 时效 | 局限 |
|---|---|---|---|---|---|---|---|---|
{chr(10).join(ledger_rows)}

## 附录B 数据时效与证据覆盖

所有数字均使用分析时点已经发布的资料；计划值与实际值分别标注，缺口不以预测值填补。

## 附录C 证据就绪度与研究执行记录

| 证据泳道 | 状态 | 已打开 | 最低要求 | 证据 |
|---|---|---:|---:|---|
| 产业链 | Ready | 3 | 2 | E1、E3、E4 |
| 需求 | Ready | 2 | 2 | E2、E5 |
| 供给与有效产能 | Ready | 2 | 2 | E1、E3 |
| 价格/订单/库存/利润 | Ready | 3 | 2 | E4、E5、E6 |
| 资本市场预期 | Ready | 2 | 2 | E7、E8 |
"""


class ValidateReportTests(unittest.TestCase):
    def assert_has_error(self, report: str, needle: str) -> None:
        errors, _ = validate(report, "full", True)
        self.assertTrue(any(needle in item for item in errors), errors)

    def test_complete_report_passes(self) -> None:
        errors, warnings = validate(valid_report(), "full", True)
        self.assertEqual([], errors)
        self.assertEqual([], warnings)

    def test_legacy_report_without_capital_cycle_block_still_passes(self) -> None:
        report = valid_report().replace(CAPITAL_CYCLE_BLOCK, "")
        errors, warnings = validate(report, "full", True)
        self.assertEqual([], errors)
        self.assertEqual([], warnings)

    def test_capital_cycle_block_requires_every_field(self) -> None:
        report = valid_report().replace(
            "- 资本开支口径：甲公司合并口径资产增加额，按自然年比较；不等同现金支付或管理层指引（E3）。\n",
            "",
        )
        self.assert_has_error(report, "missing or empty field: 资本开支口径")

    def test_capital_cycle_block_rejects_ignoring_demand(self) -> None:
        report = valid_report().replace(
            "不把整个示例行业合并为单一节点。",
            "不把整个示例行业合并为单一节点，而且需求不重要，只看供给即可。",
        )
        self.assert_has_error(report, "rejected shortcut: ignores funded demand")

    def test_capital_cycle_block_rejects_capex_as_effective_supply(self) -> None:
        report = valid_report().replace(
            "不等同现金支付或管理层指引",
            "资本开支就是有效供给，且不等同现金支付或管理层指引",
        )
        self.assert_has_error(report, "rejected shortcut: equates capex with effective supply")

    def test_capital_cycle_block_rejects_career_forecast_shortcut(self) -> None:
        report = valid_report().replace(
            "资本开支上升且回报改善支持健康扩张假设",
            "人均利润足以直接预测职业收入；资本开支上升且回报改善支持健康扩张假设",
        )
        self.assert_has_error(report, "rejected shortcut: turns per-capita profit into a forecast")

    def test_policy_gate_is_required(self) -> None:
        report = valid_report().replace(
            """### 2.1 政策重要性闸门

- 政策是否实质驱动当前周期：否
- 判断依据：当前需求由终端使用和认证交付驱动，政策只是背景变量（E2）。
- 主要作用通道：不适用；已检查需求、供给和准入
- 政策状态截至：""",
            """### 2.1 已删除的闸门

- 政策状态截至：""",
        )
        self.assert_has_error(report, "missing policy-materiality gate")

    def test_material_policy_requires_structured_jurisdiction_row(self) -> None:
        report = valid_report().replace(
            "政策是否实质驱动当前周期：否",
            "政策是否实质驱动当前周期：是",
        )
        self.assert_has_error(report, "requires a structured jurisdiction row")

    def test_non_material_policy_rejects_country_padding(self) -> None:
        policy_table = """
| 国家/地区 | 政策或工具 | 状态与截至日期 | 影响环节 | 可核实经济效应 | 落地差或局限 | 到期/反转风险 | 证据 |
|---|---|---|---|---|---|---|---|
| 示例国 | 示例规则 | 已发布规则，截至 2026-07-18 | 需求 | 影响一个单位 | 尚未形成订单 | 规则可能到期 | E2 |
"""
        report = valid_report().replace(
            "需求由存量替换、终端新增利用量",
            f"{policy_table}\n需求由存量替换、终端新增利用量",
        )
        self.assert_has_error(report, "must not retain a jurisdiction table")

    def test_combined_upstream_downstream_is_rejected(self) -> None:
        report = valid_report().replace(
            "**向谁采购**：节点1向专业材料商、关键设备制造商和能源服务机构采购不同投入品。\n\n**卖给谁**：节点1向下一制造环节、系统集成商以及具备明确预算的终端运营者销售。",
            "**上游买什么 / 下游卖给谁**：向材料商采购，并向系统集成商销售。",
        )
        self.assert_has_error(report, "combined upstream/downstream")

    def test_missing_field_is_rejected(self) -> None:
        report = valid_report().replace(
            "**为什么会卡住**：节点2受认证周期、熟练人员和专用设备交付约束，名义产能不能直接等同有效供给。\n\n",
            "",
        )
        self.assert_has_error(report, "node '核心部件' missing structured field: bottleneck")

    def test_duplicate_fields_are_rejected(self) -> None:
        shared = "节点3向专业材料商、关键设备制造商和能源服务机构采购不同投入品。"
        report = valid_report().replace(
            "节点3向下一制造环节、系统集成商以及具备明确预算的终端运营者销售。",
            shared,
        )
        self.assert_has_error(report, "repeats the same content")

    def test_future_timestamp_is_rejected(self) -> None:
        report = valid_report(datetime.now(timezone.utc) + timedelta(days=1))
        self.assert_has_error(report, "timestamp is in the future")

    def test_company_coverage_is_rejected(self) -> None:
        report = valid_report().replace(
            "| 节点4乙机构 | 未上市/机构 | 行业运营者 | 委外生产并以长协锁定合格产能 | 发布持续运营及招标数据 | E8 |\n",
            "",
        )
        self.assert_has_error(report, "fewer than 2 representative companies")

    def test_production_control_column_is_required(self) -> None:
        report = valid_report().replace(" | 产能/生产控制方式", "", 1).replace(
            " | 自有工厂并控制认证产线", "", 1
        ).replace(" | 委外生产并以长协锁定合格产能", "", 1)
        self.assert_has_error(report, "missing 产能/生产控制方式")

    def test_empty_production_control_is_rejected(self) -> None:
        report = valid_report().replace(
            "| 节点2甲公司 | 上交所 / 600002 | 主要供应商 | 自有工厂并控制认证产线 |",
            "| 节点2甲公司 | 上交所 / 600002 | 主要供应商 |  |",
        )
        self.assert_has_error(report, "lacks a production-control model")

    def test_payer_funding_row_is_required(self) -> None:
        report = valid_report().replace(
            "| 付款方资金来源与预算持续性 | 终端运营者以经营现金流、存量现金和债务融资支付；若自由现金流转负、融资成本上升或资本开支指引下调，预算即出现可观测收紧。 | E2、E5 | 未披露按产品拆分的已承诺预算。 |\n",
            "",
        )
        self.assert_has_error(report, "missing 付款方资金来源与预算持续性")

    def test_payer_funding_needs_tightening_condition(self) -> None:
        report = valid_report().replace(
            "；若自由现金流转负、融资成本上升或资本开支指引下调，预算即出现可观测收紧",
            "",
        ).replace("未披露按产品拆分的已承诺预算", "产品资金来源已经披露")
        self.assert_has_error(report, "lacks an observable tightening condition")

    def test_precise_funding_runway_without_evidence_is_rejected(self) -> None:
        report = valid_report().replace(
            "终端运营者以经营现金流、存量现金和债务融资支付；",
            "终端运营者以经营现金流、存量现金和债务融资支付，可以烧 3 年；",
        ).replace("| E2、E5 | 未披露按产品拆分的已承诺预算。 |", "|  | 未披露按产品拆分的已承诺预算。 |", 1)
        self.assert_has_error(report, "falsely precise")

    def test_order_quality_column_is_required(self) -> None:
        report = valid_report().replace("订单支撑、性质与可撤销性", "客户订单支撑")
        self.assert_has_error(report, "missing supply table")

    def test_framework_intention_cannot_be_firm_order(self) -> None:
        report = valid_report().replace(
            "框架意向不代表不可撤销硬订单，重复下单比例仍是公开缺口",
            "框架意向已经确定为不可撤销硬订单，重复下单比例为零",
        )
        self.assert_has_error(report, "framework intention is treated as a firm order")

    def test_duplicate_ordering_risk_is_required(self) -> None:
        report = valid_report().replace("多头下单", "客户采购").replace("重复下单", "客户采购")
        self.assert_has_error(report, "missing duplicate or multi-supplier ordering risk")

    def test_incomplete_public_channel_proxy_is_rejected(self) -> None:
        block = """
### 4.1 公开渠道代理

| 平台/渠道 | SKU/规格 | 卖家/主体 | 价格口径 | 观察时间 | 可得性 | 对比基线 | 证据 | 局限 | 交叉验证 |
|---|---|---|---|---|---|---|---|---|---|
| 示例商城 | 64GB | 自营 | 79.9 元 | 2026-07-27 | 有货 | 2026-06 为 39.9 元 | E8 | 单一商品 | 无 |
"""
        report = valid_report().replace("## 5. 周期位置与传导", f"{block}\n## 5. 周期位置与传导")
        self.assert_has_error(report, "explicit price definition")
        self.assert_has_error(report, "timestamp lacks")
        self.assert_has_error(report, "lacks cross-channel")
        self.assert_has_error(report, "single-channel inference limitation")

    def test_valid_public_channel_proxy_passes(self) -> None:
        block = """
### 4.1 公开渠道代理

| 平台/渠道 | SKU/规格 | 卖家/主体 | 价格口径 | 观察时间 | 可得性 | 对比基线 | 证据 | 局限 | 交叉验证 |
|---|---|---|---|---|---|---|---|---|---|
| 示例商城 | 同代 64GB 型号 | 平台自营 | 含税挂牌价 79.9 元 | 2026-07-27 14:30 +08:00 | 有货 | 2026-06-27 同口径 39.9 元 | E8 | 促销与区域可得性会影响挂牌价；单一 SKU 不代表全市场 | 第二平台同规格及上游报价交叉验证（E6、E8） |

单一渠道不能外推行业或全市场短缺，只能证明该时点的渠道现象。
"""
        errors, warnings = validate(
            valid_report().replace("## 5. 周期位置与传导", f"{block}\n## 5. 周期位置与传导"),
            "full",
            True,
        )
        self.assertEqual([], errors)
        self.assertEqual([], warnings)

    def test_low_pe_directly_equal_to_cheap_is_rejected(self) -> None:
        report = valid_report().replace(
            "不能用静态低 PE 直接判断便宜",
            "低 PE 就是便宜",
        )
        self.assert_has_error(report, "direct proof of cheap valuation")

    def test_valuation_calibration_is_required(self) -> None:
        report = valid_report().replace("### 6.3 估值口径校准", "### 6.3 常规比较")
        self.assert_has_error(report, "missing substantive 估值口径校准")

    def test_implied_expectation_reverse_test_checks_assumptions(self) -> None:
        report = valid_report().replace(
            "5年期限、必要回报率10%、中周期退出倍数20倍",
            "5年期限",
        )
        self.assert_has_error(report, "hides the discount or terminal assumption")

    def test_implied_expectation_reverse_test_rejects_target_price(self) -> None:
        report = valid_report().replace(
            "E3、E5、E7；情景推算，不输出目标价",
            "E3、E5、E7；情景推算，合理目标价500元",
        )
        self.assert_has_error(report, "outputs a target price")

    def test_implied_expectation_explicit_gap_can_pass(self) -> None:
        report = re.sub(
            r"### 6\.4 隐含预期反推[\s\S]*?(?=## 7\. 未来资金可能流向)",
            "### 6.4 隐含预期反推\n\n公开数据缺口：未取得同日期价格、正常化每股收益与股本数据；已尝试交易所和公司IR，下一步监测季度报告。\n\n",
            valid_report(),
        )
        errors, warnings = validate(report, "full", True)
        self.assertEqual([], errors)
        self.assertEqual([], warnings)

    def test_legacy_report_without_reverse_test_still_passes(self) -> None:
        report = re.sub(
            r"### 6\.4 隐含预期反推[\s\S]*?(?=## 7\. 未来资金可能流向)",
            "",
            valid_report(),
        )
        errors, warnings = validate(report, "full", True)
        self.assertEqual([], errors)
        self.assertEqual([], warnings)

    def test_explicit_not_applicable_and_public_gap_can_pass(self) -> None:
        report = valid_report().replace(
            "委外生产并以长协锁定合格产能",
            "非生产主体；生产控制方式不适用，仅提供行业运营数据",
            1,
        ).replace(
            "| E2、E5 | 未披露按产品拆分的已承诺预算。 |",
            "|  | 公开数据缺口：未披露按产品拆分的已承诺预算及融资到期结构。 |",
            1,
        ).replace(
            "框架意向不代表不可撤销硬订单，重复下单比例仍是公开缺口（E4）",
            "公开数据缺口：合同条款未披露，无法判断可撤销性；重复下单比例亦未披露（E4）",
        )
        errors, warnings = validate(report, "full", True)
        self.assertEqual([], errors)
        self.assertEqual([], warnings)

    def test_all_gap_capital_market_evidence_is_rejected(self) -> None:
        report = valid_report().replace(
            "2026-07-17 NAV 120.5，年内回报 12.0%",
            "未取得公开数据",
        ).replace(
            "2026Q1 利润同比增长 8%",
            "未构建同日序列",
        )
        self.assert_has_error(report, "contains no dated usable metric")

    def test_missing_future_flow_field_is_rejected(self) -> None:
        report = valid_report().replace(
            "| 基准 | 认证按计划完成 | 核心部件向集成移动 | 核心部件 | 集成受益、低效产能受损 | 认证和交付 |",
            "| 基准 | 认证按计划完成 | 核心部件向集成移动 |  | 集成受益、低效产能受损 | 认证和交付 |",
        )
        self.assert_has_error(report, "scenario has an empty field")

    def test_duplicate_cycle_timeline_is_rejected(self) -> None:
        report = valid_report()
        start = report.index("| 阶段/日期", report.index("## 5. 周期位置与传导"))
        end = report.index("\n\n", start)
        table = report[start:end]
        report = report[:end] + "\n\n" + table + report[end:]
        self.assert_has_error(report, "section 5 must contain exactly one cycle timeline table")

    def test_duplicate_future_flow_table_is_rejected(self) -> None:
        report = valid_report()
        start = report.index("| 情景", report.index("## 7. 未来资金可能流向"))
        end = report.index("\n\n", start)
        table = report[start:end]
        report = report[:end] + "\n\n" + table + report[end:]
        self.assert_has_error(report, "section 7 must contain exactly one future-capital-flow scenario table")

    def test_duplicate_no_advice_disclaimer_is_rejected(self) -> None:
        report = valid_report().replace(
            "以上情景不构成任何买卖建议。",
            "> 以上情景不构成任何买卖建议。\n\n> 情景推演不构成买卖建议或个股推荐。",
        )
        self.assert_has_error(report, "duplicate no-advice disclaimers")

    def test_repeated_chinese_full_stop_is_rejected(self) -> None:
        report = valid_report().replace("需求真实改善 |", "需求真实改善。。 |")
        self.assert_has_error(report, "repeated Chinese full stop")

    def test_missing_conclusion_confidence_is_rejected(self) -> None:
        report = valid_report().replace("置信度：中\n", "")
        self.assert_has_error(report, "independent conclusion field: 置信度")

    def test_cross_report_prose_reuse_is_rejected(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            first = root / "01_first.md"
            second = root / "02_second.md"
            first.write_text(valid_report(), encoding="utf-8")
            second.write_text(valid_report(), encoding="utf-8")
            errors, _, _ = audit([first, second], first, True)
        self.assertTrue(any("cross-report repeated prose" in item for item in errors), errors)
        self.assertTrue(any("cross-report repeated cycle timeline" in item for item in errors), errors)


if __name__ == "__main__":
    unittest.main()
