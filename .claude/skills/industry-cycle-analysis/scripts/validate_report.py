#!/usr/bin/env python3
"""Validate an industry-cycle Markdown report for structural, evidence-integrity, and readability gates."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path


FULL_SECTIONS = [
    "## 0. 一页看懂",
    "## 1. 产业链地图",
    "## 2. 需求",
    "## 3. 供给",
    "## 4. 供需矛盾与高频信号",
    "## 5. 周期位置与传导",
    "## 6. 资金动向",
    "## 7. 未来资金可能流向",
    "## 8. 分歧与反证",
    "## 9. 观察哨与跟踪",
    "## 10. 术语表",
    "## 附录A 证据台账",
    "## 附录B 数据时效与证据覆盖",
    "## 附录C 证据就绪度与研究执行记录",
]

REQUIRED_HEADERS = ["分析日期", "地理范围", "数据时效", "行业边界"]
READINESS_LANES = [
    "产业链",
    "需求",
    "供给与有效产能",
    "价格/订单/库存/利润",
    "资本市场预期",
]

PLACEHOLDERS = {
    "generic source": r"官方/协会/公司|公司披露或行业数据|官方或交易所高频数据优先",
    "unverified metric": r"待按产品核验|视公开口径|见数据时效表",
    "generic market statement": r"市场可能交易",
    "generic watchpoint": r"连续2期改善且与价格/利润同向|连续2期恶化或与库存背离",
    "generic transition window": r"未来2[-至]6(?:个)?季度",
    "boilerplate chain note": r"钱和订单从\s*\S+\s*的需求向前传",
    "circular node definition": r"负责把上游投入转成\S*可采购",
    "generic demand slot": r"核心产品需求|新增场景",
    "undated period": r"最新已披露期",
    "generic budget-entry description": r"把真实使用需求变成预算和采购[，,]是整条链最终能否回款的入口",
}

# Interpretation-style cells that carry zero information when they are the whole cell.
EMPTY_INTERPRETATION_CELLS = {"直接观测", "交叉验证"}

# Sentences at least this long that repeat REPEAT_LIMIT+ times indicate template filling.
REPEAT_MIN_LEN = 18
REPEAT_LIMIT = 3

NODE_FIELD_PATTERNS = {
    "what": r"^\*\*它是干什么的\*\*[：:]\s*(.+)$",
    "suppliers": r"^\*\*向谁采购\*\*[：:]\s*(.+)$",
    "buyers": r"^\*\*卖给谁\*\*[：:]\s*(.+)$",
    "money": r"^\*\*怎么赚钱、议价能力\*\*[：:]\s*(.+)$",
    "bottleneck": r"^\*\*为什么会卡住\*\*[：:]\s*(.+)$",
    "advanced": r"^\*\*进阶视角\*\*[：:]\s*(.+)$",
}

NODE_FIELD_MIN_LENGTH = {
    "what": 12,
    "suppliers": 10,
    "buyers": 10,
    "money": 20,
    "bottleneck": 10,
    "advanced": 36,
}


def section(text: str, heading: str) -> str:
    start = text.find(heading)
    if start < 0:
        return ""
    rest = text[start + len(heading) :]
    match = re.search(r"\n##\s+", rest)
    return rest if match is None else rest[: match.start()]


def table_rows(block: str) -> list[list[str]]:
    rows = []
    for line in block.splitlines():
        stripped = line.strip()
        if not stripped.startswith("|"):
            continue
        cells = [cell.strip() for cell in stripped.strip("|").split("|")]
        if all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells if cell):
            continue
        rows.append(cells)
    return rows


def markdown_tables(block: str) -> list[list[list[str]]]:
    """Return Markdown tables separately so validation targets the intended table."""
    tables: list[list[list[str]]] = []
    current: list[list[str]] = []
    for line in block.splitlines():
        stripped = line.strip()
        if stripped.startswith("|"):
            cells = [cell.strip() for cell in stripped.strip("|").split("|")]
            if not all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells if cell):
                current.append(cells)
            continue
        if current:
            tables.append(current)
            current = []
    if current:
        tables.append(current)
    return tables


def table_with_headers(block: str, required: set[str]) -> list[list[str]]:
    """Return the first table whose header contains every required label."""
    for rows in markdown_tables(block):
        if rows and required.issubset(set(rows[0])):
            return rows
    return []


def normalize_text(value: str) -> str:
    return re.sub(r"[\s`*_，。；;：:、（）()\[\]]+", "", value).lower()


def extract_node_blocks(chain: str) -> list[tuple[str, str]]:
    matches = list(
        re.finditer(r"^(?:###|####)\s*1\.2\.\d+\s+(.+?)\s*$", chain, re.MULTILINE)
    )
    blocks: list[tuple[str, str]] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(chain)
        next_section = re.search(r"^###\s+1\.(?!2\.)", chain[match.end() : end], re.MULTILINE)
        if next_section:
            end = match.end() + next_section.start()
        blocks.append((match.group(1).strip(), chain[match.end() : end]))
    return blocks


def node_field(block: str, key: str) -> str:
    match = re.search(NODE_FIELD_PATTERNS[key], block, re.MULTILINE)
    return match.group(1).strip() if match else ""


def representative_company_rows(block: str) -> list[list[str]]:
    rows = representative_company_table(block)
    return rows[1:] if rows else []


def representative_company_table(block: str) -> list[list[str]]:
    marker = re.search(r"^\*\*代表企业\*\*[：:]?\s*$", block, re.MULTILINE)
    if not marker:
        return next(
            (
                rows
                for rows in markdown_tables(block)
                if rows and any("企业" in cell or "机构" in cell for cell in rows[0])
            ),
            [],
        )
    tail = block[marker.end() :]
    next_field = re.search(r"^\*\*(?:怎么赚钱、议价能力|为什么会卡住|进阶视角)\*\*", tail, re.MULTILINE)
    table = tail if not next_field else tail[: next_field.start()]
    return next(iter(markdown_tables(table)), [])


def row_index(headers: list[str], label: str) -> int:
    try:
        return headers.index(label)
    except ValueError:
        return -1


def parse_timestamp(raw: str) -> datetime | None:
    value = raw.strip().replace("Z", "+00:00")
    value = re.sub(r"\s+(UTC|GMT)([+-]\d{1,2}:?\d{0,2})$", r" \2", value, flags=re.IGNORECASE)
    value = re.sub(r"([+-]\d{2})(\d{2})$", r"\1:\2", value)
    try:
        parsed = datetime.fromisoformat(value)
    except ValueError:
        return None
    return parsed if parsed.tzinfo is not None else None


def validate(text: str, mode: str, strict: bool) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    for header in REQUIRED_HEADERS:
        if not re.search(rf"^{re.escape(header)}[：:]\s*\S+", text, re.MULTILINE):
            errors.append(f"missing required header: {header}")

    timestamp = re.search(r"^分析日期[：:]\s*(.+)$", text, re.MULTILINE)
    if timestamp and not re.search(r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}(?::\d{2})?.*(?:[+-]\d{2}:?\d{2}|(?:UTC|GMT))", timestamp.group(1)):
        errors.append("analysis timestamp must include a date, HH:mm, and timezone")
    elif timestamp:
        parsed_timestamp = parse_timestamp(timestamp.group(1))
        if parsed_timestamp is None:
            errors.append("analysis timestamp is not a parseable timezone-aware datetime")
        elif parsed_timestamp.astimezone(timezone.utc) > datetime.now(timezone.utc) + timedelta(minutes=5):
            errors.append("analysis timestamp is in the future; query system time instead of hard-coding it")

    if mode == "full":
        for heading in FULL_SECTIONS:
            if heading not in text:
                errors.append(f"missing full-report section: {heading}")

    for label, pattern in PLACEHOLDERS.items():
        if re.search(pattern, text, re.IGNORECASE):
            errors.append(f"placeholder or generic content remains: {label}")

    if re.search(r"。。+", text):
        errors.append("repeated Chinese full stop remains")

    # --- Anti-boilerplate: no long sentence may repeat REPEAT_LIMIT+ times ---
    sentences = re.split(r"[。；;\n]", text)
    counts = Counter(s.strip() for s in sentences if len(s.strip()) >= REPEAT_MIN_LEN)
    for sentence, count in counts.items():
        if count >= REPEAT_LIMIT and not sentence.startswith("|") and not sentence.startswith("-"):
            errors.append(
                f"sentence repeated {count}x (template filling suspected): {sentence[:40]}..."
            )

    # --- Section 0: plain-language intro and key numbers ---
    overview = section(text, "## 0. 一页看懂")
    if mode == "full":
        if "这个行业是做什么的" not in overview:
            errors.append("section 0 missing plain-language intro '这个行业是做什么的'")
        if "三个最重要的数字" not in overview:
            errors.append("section 0 missing '三个最重要的数字'")
        if not re.search(r"结论状态[：:]", overview):
            errors.append("section 0 missing 结论状态")
        for field in ("周期阶段", "置信度", "证据截至时间", "上调条件", "下调条件"):
            if not re.search(rf"{field}[：:]\s*\S+", overview):
                errors.append(f"section 0 missing independent conclusion field: {field}")
        intro_match = re.search(
            r"###\s*这个行业是做什么的\s*(.*?)(?=\n###\s|\Z)",
            overview,
            re.DOTALL,
        )
        if intro_match and "结论状态" in intro_match.group(1):
            errors.append("section 0 industry intro contains conclusion status")

    # --- Section 1: mermaid chart, node explanations, representative companies ---
    chain = section(text, "## 1. 产业链地图")
    if mode == "full":
        if "```mermaid" not in chain:
            errors.append("industry chain map must be a mermaid diagram")
        if not re.search(r"###\s*1\.2", chain):
            errors.append("missing per-node explanations (### 1.2.x)")
        if "代表企业" not in chain:
            errors.append("missing representative-company tables in chain nodes")
        if not re.search(r"上市地|代码|未上市", chain):
            errors.append("representative companies lack listing venue/ticker information")
        if "谁最终付款" not in chain:
            errors.append("missing money-flow table (谁最终付款…)")

        if re.search(r"\*\*上游买什么\s*/\s*下游卖给谁\*\*", chain):
            errors.append("combined upstream/downstream node field remains; use separate 向谁采购 and 卖给谁 fields")

        nodes = extract_node_blocks(chain)
        if len(nodes) < 4:
            errors.append(f"only {len(nodes)} detailed chain nodes; full research requires at least 4")

        for node_name, block in nodes:
            values: dict[str, str] = {}
            for key, minimum in NODE_FIELD_MIN_LENGTH.items():
                value = node_field(block, key)
                values[key] = value
                if not value:
                    errors.append(f"node '{node_name}' missing structured field: {key}")
                elif len(normalize_text(value)) < minimum:
                    errors.append(
                        f"node '{node_name}' field '{key}' is too thin ({len(normalize_text(value))} < {minimum})"
                    )

            normalized = [normalize_text(value) for value in values.values() if value]
            if len(normalized) != len(set(normalized)):
                errors.append(f"node '{node_name}' repeats the same content across structured fields")

            company_table = representative_company_table(block)
            companies = company_table[1:] if company_table else []
            company_headers = company_table[0] if company_table else []
            control_index = row_index(company_headers, "产能/生产控制方式")
            if control_index < 0:
                errors.append(
                    f"node '{node_name}' representative-company table missing 产能/生产控制方式"
                )
            if len(companies) < 2:
                errors.append(f"node '{node_name}' has fewer than 2 representative companies/institutions")
            for company in companies:
                if len(company) < 4 or not company[0] or not company[1]:
                    errors.append(f"node '{node_name}' has an incomplete representative-company row")
                    continue
                if not re.search(r"交易所|证交所|澳交所|伦交所|德交所|台交所|未上市|非上市|机构|多主体|非单一|NYSE|NASDAQ|LSE|SSE|SZSE|HKEX|ASX|TSX|TSE|NSE|SIX|XETRA|EPA|Euronext|纳斯达克|纽交所|港交所|上交所|深交所", company[1], re.IGNORECASE):
                    errors.append(f"node '{node_name}' company '{company[0]}' lacks a listing venue or unlisted/institution label")
                if not re.search(r"\bE\d+\b", " ".join(company)):
                    errors.append(f"node '{node_name}' company '{company[0]}' lacks an evidence ID")
                if control_index >= 0:
                    control = company[control_index] if len(company) > control_index else ""
                    if not normalize_text(control):
                        errors.append(
                            f"node '{node_name}' company '{company[0]}' lacks a production-control model"
                        )
                    elif not re.search(
                        r"自有|合资|委外|外包|代工|长协|锁量|市场采购|外采|采购|租赁|特许|运营|控制|权益|非单一|多主体|非生产主体|不适用",
                        control,
                        re.IGNORECASE,
                    ):
                        errors.append(
                            f"node '{node_name}' company '{company[0]}' production-control model is not explicit"
                        )

            if not re.search(r"\bE\d+\b", values.get("advanced", "")):
                errors.append(f"node '{node_name}' advanced view lacks an evidence ID")

        profit_block = chain.split("### 1.3", 1)[1] if "### 1.3" in chain else ""
        profit_rows = table_rows(profit_block)
        if len(profit_rows) < 5:
            errors.append("power-and-profit map has fewer than 4 data rows")
        money_table = table_with_headers(profit_block, {"问题", "证据", "缺口"})
        funding_row = next(
            (
                row
                for row in money_table[1:]
                if row and row[0].strip("？? ") == "付款方资金来源与预算持续性"
            ),
            [],
        )
        if not funding_row:
            errors.append("money-flow table missing 付款方资金来源与预算持续性")
        else:
            headers = money_table[0]
            evidence_index = row_index(headers, "证据")
            gap_index = row_index(headers, "缺口")
            answer_index = next(
                (
                    index
                    for index, header in enumerate(headers)
                    if index not in (0, evidence_index, gap_index)
                ),
                1,
            )
            answer = funding_row[answer_index] if len(funding_row) > answer_index else ""
            evidence = funding_row[evidence_index] if 0 <= evidence_index < len(funding_row) else ""
            gap = funding_row[gap_index] if 0 <= gap_index < len(funding_row) else ""
            if not re.search(
                r"经营现金流|自由现金流|存量现金|净现金|债务|股权|财政|预算|融资|拨款",
                answer,
                re.IGNORECASE,
            ):
                errors.append("payer funding row lacks a concrete funding source")
            if not re.search(
                r"收紧|耗尽|下调|削减|推迟|放缓|到期|融资成本|自由现金流|杠杆|取消|暂停|违约|缺口|未披露",
                f"{answer} {gap}",
                re.IGNORECASE,
            ):
                errors.append("payer funding row lacks an observable tightening condition")
            if not re.search(r"\bE\d+\b", evidence) and len(normalize_text(gap)) < 8:
                errors.append("payer funding row needs evidence or a precise public-data gap")
            if re.search(r"(?:还能?|可以|可)\s*烧\s*\d+(?:\.\d+)?\s*(?:年|个月)", answer) and not re.search(
                r"\bE\d+\b", evidence
            ):
                errors.append("payer funding runway is falsely precise without evidence")

    # --- Section 4: interpretation cells must carry content ---
    demand = section(text, "## 2. 需求")
    if mode == "full":
        policy_gate = re.search(
            r"^###\s*2\.1\s+政策重要性闸门\s*$([\s\S]*?)(?=^###\s+|^##\s+|\Z)",
            demand,
            re.MULTILINE,
        )
        if not policy_gate:
            errors.append("section 2 missing policy-materiality gate")
        else:
            gate = policy_gate.group(1)
            answer = re.search(r"政策是否实质驱动当前周期[：:]\s*(是|否)\s*$", gate, re.MULTILINE)
            if not answer:
                errors.append("policy-materiality answer must be exactly 是 or 否")
            basis = re.search(r"判断依据[：:]\s*(.+)$", gate, re.MULTILINE)
            if not basis or not re.search(r"\bE\d+\b", basis.group(1)):
                errors.append("policy-materiality basis must include an evidence ID")
            channel = re.search(r"主要作用通道[：:]\s*(.+)$", gate, re.MULTILINE)
            if not channel or not normalize_text(channel.group(1)):
                errors.append("policy-materiality gate missing transmission channel")
            status_date = re.search(r"政策状态截至[：:]\s*(.+)$", gate, re.MULTILINE)
            if not status_date or not re.search(
                r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}(?::\d{2})?.*(?:[+-]\d{2}:?\d{2}|(?:UTC|GMT))",
                status_date.group(1),
            ):
                errors.append("policy-materiality status must include a date, HH:mm, and timezone")

            policy_required = {
                "国家/地区",
                "政策或工具",
                "状态与截至日期",
                "影响环节",
                "可核实经济效应",
                "落地差或局限",
                "到期/反转风险",
                "证据",
            }
            policy_rows = table_with_headers(gate, policy_required)
            if answer and answer.group(1) == "是":
                if len(policy_rows) < 2:
                    errors.append("policy-materiality answer 是 requires a structured jurisdiction row")
                else:
                    for row in policy_rows[1:]:
                        if len(row) < len(policy_required) or any(not normalize_text(cell) for cell in row[:8]):
                            errors.append("policy-materiality jurisdiction row has an empty field")
                        if not re.search(r"提案|已立法|已发布规则|已执行|已拨付", " ".join(row)):
                            errors.append("policy-materiality jurisdiction row lacks an explicit policy status")
                        if not re.search(r"\bE\d+\b", " ".join(row)):
                            errors.append("policy-materiality jurisdiction row lacks an evidence ID")
            if answer and answer.group(1) == "否" and policy_rows:
                errors.append("policy-materiality answer 否 must not retain a jurisdiction table")

            allowed_channels = (
                "需求",
                "供给",
                "价格与利润",
                "成本",
                "贸易流",
                "资本开支",
                "融资与资本准入",
                "认证与经营准入",
            )
            if channel and not any(item in channel.group(1) for item in allowed_channels):
                errors.append("policy-materiality gate uses an unsupported transmission channel")

    # --- Section 3: effective supply and order quality ---
    supply = section(text, "## 3. 供给")
    if mode == "full":
        supply_rows = next(
            (
                rows
                for rows in markdown_tables(supply)
                if rows
                and "订单支撑、性质与可撤销性" in rows[0]
                and any("公告" in cell or "计划" in cell for cell in rows[0])
                and any(
                    "验证" in cell or "认证" in cell or "量产" in cell
                    for cell in rows[0]
                )
            ),
            [],
        )
        if len(supply_rows) < 2:
            errors.append("section 3 missing supply table with 订单支撑、性质与可撤销性")
        else:
            headers = supply_rows[0]
            order_index = headers.index("订单支撑、性质与可撤销性")
            for row in supply_rows[1:]:
                order_quality = row[order_index] if len(row) > order_index else ""
                if len(normalize_text(order_quality)) < 8:
                    errors.append("supply row has an empty or thin order-quality field")
                    continue
                if not re.search(
                    r"预付款|长协|take-or-pay|不可撤销|可撤销|取消|框架|意向|条款|未披露|订单|招标|采购|承诺|缺口|销售|交付",
                    order_quality,
                    re.IGNORECASE,
                ):
                    errors.append("supply row does not identify order nature or cancellability")
                if re.search(r"框架意向", order_quality) and re.search(
                    r"确定|硬订单|不可撤销|锁定", order_quality
                ) and not re.search(r"不能|不代表|非|未|无法|缺口", order_quality):
                    errors.append("framework intention is treated as a firm order")
        if not re.search(r"重复下单|多头下单", supply):
            errors.append("section 3 missing duplicate or multi-supplier ordering risk")

    # --- Section 4: interpretation cells must carry content ---
    signals = section(text, "## 4. 供需矛盾与高频信号")
    if mode == "full" and signals:
        signal_rows = table_rows(signals)
        if len(signal_rows) < 6:
            errors.append("supply-demand signal table has fewer than 5 data rows")
        for row in signal_rows:
            for cell in row:
                if cell in EMPTY_INTERPRETATION_CELLS and "平台/渠道" not in row:
                    errors.append(
                        f"signal interpretation cell is contentless boilerplate: '{cell}'"
                    )

        if re.search(r"###\s*4\.1\s+公开渠道代理|平台/渠道\s*\|\s*SKU/规格", signals):
            channel_required = {
                "平台/渠道",
                "SKU/规格",
                "卖家/主体",
                "价格口径",
                "观察时间",
                "可得性",
                "对比基线",
                "证据",
                "局限",
                "交叉验证",
            }
            channel_rows = table_with_headers(signals, channel_required)
            if len(channel_rows) < 2:
                errors.append("public-channel proxy is missing its required structured table")
            else:
                headers = channel_rows[0]
                indexes = {header: headers.index(header) for header in channel_required}
                for row in channel_rows[1:]:
                    if any(
                        len(row) <= index or not normalize_text(row[index])
                        for index in indexes.values()
                    ):
                        errors.append("public-channel proxy row has an empty required field")
                        continue
                    if not re.search(
                        r"挂牌价|券后价|成交价|含税价|未税价",
                        row[indexes["价格口径"]],
                    ):
                        errors.append("public-channel proxy lacks an explicit price definition")
                    if not re.search(
                        r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}(?::\d{2})?.*(?:[+-]\d{2}:?\d{2}|UTC|GMT)",
                        row[indexes["观察时间"]],
                        re.IGNORECASE,
                    ):
                        errors.append("public-channel proxy timestamp lacks date, HH:mm and timezone")
                    if not re.search(r"\bE\d+\b", row[indexes["证据"]]):
                        errors.append("public-channel proxy row lacks an evidence ID")
                    if not re.search(r"\bE\d+\b", row[indexes["交叉验证"]]):
                        errors.append("public-channel proxy lacks cross-channel or upstream evidence")
            if not re.search(r"单一渠道.{0,12}(?:不能|不可).{0,12}(?:行业|全市场)", signals):
                errors.append("public-channel proxy lacks the single-channel inference limitation")

    # --- Section 5: prior-cycle comparison and falsification ---
    cycle = section(text, "## 5. 周期位置与传导")
    if mode == "full":
        cycle_tables = markdown_tables(cycle)
        if len(cycle_tables) != 1:
            errors.append("section 5 must contain exactly one cycle timeline table")
        cycle_rows = next(
            (rows for rows in cycle_tables if rows and any("阶段" in cell or "日期" in cell for cell in rows[0])),
            [],
        )
        if len(cycle_rows) < 5:
            errors.append("cycle timeline has fewer than 4 data rows")
        if len(cycle_rows) > 7:
            errors.append("cycle timeline has more than 6 data rows")
        if cycle_rows:
            header = cycle_rows[0]
            if not any("性质" in cell for cell in header):
                errors.append("cycle timeline missing actual/plan/forecast/risk type column")
            timeline_text = " ".join(" ".join(row) for row in cycle_rows[1:])
            if not re.search(r"已发生|实际", timeline_text):
                errors.append("cycle timeline has no actual event row")
            if not re.search(r"计划|预测|风险窗口", timeline_text):
                errors.append("cycle timeline does not distinguish plans, forecasts or risk windows")
        if "进阶视角" not in cycle:
            errors.append("section 5 missing 进阶视角 prior-cycle comparison")
        if not re.search(r"什么会证明这个判断错了|What would prove this wrong", cycle):
            errors.append("section 5 missing falsification condition")

        # Capital-cycle diagnostics are conditional so legacy reports remain valid.
        # Once the author opts into the block, however, its definitions and
        # falsification fields are part of the publication contract.
        capital_cycle_match = re.search(
            r"^###\s+5\.\d+\s+资本周期交叉校验(?:（[^\n]*）)?\s*$([\s\S]*?)(?=^###\s+|^##\s+|\Z)",
            cycle,
            re.MULTILINE,
        )
        if capital_cycle_match:
            capital_cycle = capital_cycle_match.group(1)
            capital_fields = (
                "观察节点",
                "资本开支方向",
                "资本开支口径",
                "资本开支性质",
                "回报代理",
                "口径可比性",
                "供给兑现时滞",
                "交叉判断",
                "反证条件",
            )
            for field in capital_fields:
                match = re.search(
                    rf"^[-*]\s*{re.escape(field)}[：:]\s*(.+)$",
                    capital_cycle,
                    re.MULTILINE,
                )
                if match is None or len(normalize_text(match.group(1))) < 8:
                    errors.append(f"capital-cycle block missing or empty field: {field}")

            evidence_ids = set(re.findall(r"\bE\d+\b", capital_cycle))
            if len(evidence_ids) < 2:
                errors.append("capital-cycle block needs at least 2 distinct evidence IDs")
            if not re.search(r"增长性|扩张性|维护性|替换性|混合|未拆分", capital_cycle):
                errors.append("capital-cycle block does not classify capex nature")
            if not re.search(r"平均人数|期末人数|统计范围|合并范围|分子|分母|可比|不可比", capital_cycle):
                errors.append("capital-cycle block does not explain metric comparability")

            rejected_shortcuts = {
                "ignores funded demand": r"需求不重要|忽略需求|只看供给|无需看需求",
                "equates capex with effective supply": r"资本开支(?:就是|等于|=)有效供给",
                "maps capex directly to industry direction": r"资本开支(?:上涨|上升|增长).{0,8}(?:就是|等于|意味着).{0,8}(?:行业上涨|行业上坡|上行)",
                "claims supply alone determines returns": r"(?:回报|收益).{0,8}(?:只由|完全由|仅由).{0,8}供给决定|供给.{0,8}(?:唯一|完全).{0,8}决定.{0,8}(?:回报|收益)",
                "turns per-capita profit into a forecast": r"人均(?:净)?利润.{0,12}(?:直接|足以|可以).{0,8}(?:预测|判断).{0,8}(?:工资|招聘|就业|职业|收入|行业)",
            }
            for label, pattern in rejected_shortcuts.items():
                if re.search(pattern, capital_cycle):
                    errors.append(f"capital-cycle block contains a rejected shortcut: {label}")

    # --- Advanced-reader blocks across the body ---
    if mode == "full":
        advanced_count = len(re.findall(r"进阶视角", text))
        required_advanced = len(extract_node_blocks(chain)) + 3
        if advanced_count < required_advanced:
            errors.append(
                f"only {advanced_count} 进阶视角 blocks; expected at least {required_advanced} for every node plus demand, supply and cycle"
            )

    # --- Section 6: capital-flow attempts table + qualitative paragraph ---
    capital = section(text, "## 6. 资金动向")
    if mode == "full":
        for required in ["尝试的来源类型", "已定价", "未定价"]:
            if required not in capital:
                errors.append(f"section 6 missing mandatory element: {required}")
        attempt_rows = [
            row
            for row in table_rows(capital)
            if row and row[0] not in ("尝试的来源类型", "产业现实")
            and any(cell for cell in row[1:])
        ]
        if "尝试的来源类型" in capital and len(attempt_rows) < 3:
            errors.append("capital-flow attempts table has fewer than 3 recorded attempts")

        proxy_required = {"工具/主体", "覆盖节点", "指标与期间", "来源", "结论", "局限"}
        proxy_rows = table_with_headers(capital, proxy_required)
        if len(proxy_rows) < 3:
            errors.append("capital-market proxy table has fewer than 2 evidence rows")
        else:
            headers = proxy_rows[0]
            metric_index = headers.index("指标与期间")
            source_index = headers.index("来源")
            usable = [
                row for row in proxy_rows[1:]
                if len(row) > max(metric_index, source_index)
                and re.search(r"\d{4}[-年/.]|\d{4}Q\d|\d+(?:\.\d+)?%|\d+(?:\.\d+)?倍", row[metric_index])
                and re.search(r"https?://|\bE\d+\b", row[source_index])
                and not re.search(r"无公开数据|未取得|不可得|未构建", row[metric_index])
            ]
            if not usable:
                errors.append("capital-market proxy table contains no dated usable metric")

        if attempt_rows and all(
            any(re.search(r"无公开数据|未取得|不可得|口径不可比|未构建", cell) for cell in row)
            for row in attempt_rows
        ) and len(proxy_rows) < 3:
            errors.append("all capital-market attempts are gaps; market lane cannot be complete")

        calibration = re.search(
            r"(?:^###\s*\d+(?:\.\d+)*\s*)?估值口径校准[：:]?\s*([\s\S]*?)(?=^###\s+|^##\s+|\Z)",
            capital,
            re.MULTILINE,
        )
        if not calibration or len(normalize_text(calibration.group(1))) < 30:
            errors.append("section 6 missing substantive 估值口径校准")
        else:
            calibration_text = calibration.group(1)
            if not re.search(r"PE|市盈率|估值", calibration_text, re.IGNORECASE):
                errors.append("valuation calibration does not identify the valuation metric")
            if not re.search(r"利润|盈利|毛利率|净利率", calibration_text):
                errors.append("valuation calibration is not tied to the profit cycle")
            if not re.search(r"价格|库存|利用率|开工率|产能", calibration_text):
                errors.append("valuation calibration is not tied to an operating-cycle metric")
            if not re.search(r"\bE\d+\b|不适用|亏损|口径不可比|数据缺口|无公开", calibration_text):
                errors.append("valuation calibration lacks evidence or an explicit applicability gap")
        if re.search(
            r"(?:低\s*PE|低市盈率|PE\s*低).{0,10}(?:等于|就是|意味着|说明).{0,8}(?:便宜|低估)",
            capital,
            re.IGNORECASE,
        ):
            errors.append("low PE is treated as direct proof of cheap valuation")

        implied = re.search(
            r"^###\s*\d+(?:\.\d+)*\s*隐含预期反推\s*([\s\S]*?)(?=^###\s+|^##\s+|\Z)",
            capital,
            re.MULTILINE,
        )
        if implied:
            implied_text = implied.group(1)
            if "公开数据缺口" in implied_text:
                if len(normalize_text(implied_text)) < 30:
                    errors.append("implied-expectation gap is not specific enough")
            else:
                implied_required = {"反推方法", "已知输入", "关键假设", "反推出的门槛", "产业证据对照", "证据与局限"}
                implied_rows = table_with_headers(implied_text, implied_required)
                if len(implied_rows) < 2:
                    errors.append("implied-expectation reverse test lacks a complete row")
                else:
                    headers = implied_rows[0]
                    for row in implied_rows[1:]:
                        values = {
                            header: row[headers.index(header)] if len(row) > headers.index(header) else ""
                            for header in implied_required
                        }
                        if not re.search(r"价格|市值|企业价值", values["已知输入"]):
                            errors.append("implied-expectation reverse test lacks a dated market-value input")
                        if not re.search(r"EPS|每股收益|利润|盈利|现金流|FCF|EBITDA|ROIC", values["已知输入"], re.IGNORECASE):
                            errors.append("implied-expectation reverse test lacks a comparable fundamental base")
                        if not re.search(r"必要回报率|折现率|资本成本|WACC|退出倍数|终值|terminal", values["关键假设"], re.IGNORECASE):
                            errors.append("implied-expectation reverse test hides the discount or terminal assumption")
                        if not re.search(r"EPS|每股收益|FCF|现金流|CAGR|增速|利润率|利用率|ROIC|路径", values["反推出的门槛"], re.IGNORECASE):
                            errors.append("implied-expectation reverse test does not state an operating hurdle")
                        if not re.search(r"产业证据支持|要求偏高|证据不足", values["产业证据对照"]):
                            errors.append("implied-expectation reverse test lacks an industry-evidence verdict")
                        if not re.search(r"\bE\d+\b|https?://", values["证据与局限"]):
                            errors.append("implied-expectation reverse test lacks evidence")
                        if not re.search(r"情景|推论|假设|局限|缺口", values["证据与局限"]):
                            errors.append("implied-expectation reverse test is not labeled as a scenario or inference")

            for line in implied_text.splitlines():
                target_call = re.search(r"目标价|合理股价|股价.{0,8}(?:涨到|达到)", line)
                target_context = line[max(0, target_call.start() - 8) : target_call.start()] if target_call else ""
                if target_call and not re.search(r"不构成|不得|不能|不输出|禁止|不是", target_context):
                    errors.append("implied-expectation reverse test outputs a target price")
                    break
            if re.search(
                r"(?:股价|价格)不变.{0,30}(?:低估|便宜|低位)",
                implied_text,
            ):
                errors.append("price-unchanged future PE is treated as proof of undervaluation")

    # --- Section 7: future capital flow scenarios ---
    future = section(text, "## 7. 未来资金可能流向")
    if mode == "full":
        for scenario in ["基准", "上行", "下行"]:
            if scenario not in future:
                errors.append(f"section 7 missing scenario: {scenario}")
        if not re.search(r"不构成.{0,12}买卖建议", future):
            errors.append("section 7 missing no-advice disclaimer")
        disclaimer_count = len(
            re.findall(r"^>\s*.*不构成.*(?:买卖建议|个股推荐).*$", future, re.MULTILINE)
        )
        if disclaimer_count > 1:
            errors.append("section 7 contains duplicate no-advice disclaimers")
        future_tables = markdown_tables(future)
        if len(future_tables) != 1:
            errors.append("section 7 must contain exactly one future-capital-flow scenario table")
        future_required = {"情景", "触发条件", "利润池往哪个环节移动", "先受益的环节", "后受益/受损的环节", "需要盯的证据"}
        future_rows = table_with_headers(future, future_required)
        if len(future_rows) != 4:
            errors.append("section 7 must contain exactly three complete scenario rows")
        else:
            for row in future_rows[1:]:
                if len(row) < 6 or any(not normalize_text(cell) for cell in row[:6]):
                    errors.append(f"section 7 scenario has an empty field: {row[0] if row else 'unknown'}")

    # --- Section 8: mainstream narrative contrast ---
    contrast = section(text, "## 8. 分歧与反证")
    if mode == "full" and "主流叙事" not in contrast:
        errors.append("section 8 missing mainstream-narrative vs report contrast")

    # --- Section 9: watchpoints ---
    watch = section(text, "## 9. 观察哨与跟踪")
    for header in ["基线", "来源", "频率", "正向触发", "反证触发"]:
        if mode == "full" and header not in watch:
            errors.append(f"watchpoint table missing field: {header}")

    # Watchpoint indicator cells must be names, not values.
    watch_tables = markdown_tables(watch)
    watch_rows = next(
        (
            rows
            for rows in watch_tables
            if rows
            and any(header.startswith("基线") for header in rows[0])
            and {"来源", "频率", "正向触发", "反证触发"}.issubset(set(rows[0]))
        ),
        [],
    )
    if mode == "full" and len(watch_rows) < 6:
        errors.append("watchpoint table has fewer than 5 data rows")
    for row in watch_rows[1:]:
        if row and re.search(r"\d[\d,.]*\s*(元|美元|欧元|亿|万|吨|百万|GWh|MW|TWh|%)", row[0]):
            errors.append(f"watchpoint indicator cell contains a value, not an indicator name: '{row[0][:30]}'")

    series_heading = re.search(r"^###\s*9\.1\s+可比时间序列\s*$", watch, re.MULTILINE)
    series_gap = re.search(
        r"可比时间序列缺口|Evidence gap:\s*comparable time series unavailable|可比时间序列(?:不可用|缺口)",
        watch,
        re.IGNORECASE,
    )
    if mode == "full" and not series_heading and not series_gap:
        errors.append("missing comparable time-series table or explicit time-series evidence gap")
    if series_heading:
        series_block = watch[series_heading.end() :].split("跟踪数据库", 1)[0].split("Tracking database:", 1)[0]
        lines = [line for line in series_block.splitlines() if line.strip().startswith("|")]
        if len(lines) >= 3:
            headers = [cell.strip() for cell in lines[0].strip().strip("|").split("|")]
            idx = {h: i for i, h in enumerate(headers)}
            ind_key = "指标" if "指标" in idx else "Indicator"
            unit_key = "单位" if "单位" in idx else "Unit"
            val_key = "数值" if "数值" in idx else "Value"
            missing = [k for k in (ind_key, unit_key, val_key) if k not in idx]
            if missing:
                errors.append(f"comparable time-series table missing columns: {', '.join(missing)}")
            groups: dict[tuple[str, str], int] = {}
            for line in lines[2:]:
                cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
                if len(cells) < len(headers):
                    continue
                indicator = cells[idx[ind_key]] if ind_key in idx else ""
                unit = cells[idx[unit_key]] if unit_key in idx else ""
                value = cells[idx[val_key]] if val_key in idx else ""
                if indicator and unit and re.fullmatch(r"[-+]?\d[\d,]*(?:\.\d+)?", value):
                    groups[(indicator, unit)] = groups.get((indicator, unit), 0) + 1
            if not any(count >= 2 for count in groups.values()):
                errors.append("comparable time-series table needs at least two numeric points for one indicator and unit")
        elif mode == "full" and not series_gap:
            errors.append("comparable time-series table has fewer than two data rows")

    # --- Section 10: glossary ---
    glossary = section(text, "## 10. 术语表")
    if mode == "full":
        glossary_terms = [row[0] for row in table_rows(glossary)[1:] if row and row[0]]
        if len(glossary_terms) < 3:
            errors.append("glossary has fewer than 3 terms; jargon must be explained for first-time readers")

    # --- Appendix A: evidence ledger ---
    ledger = section(text, "## 附录A 证据台账")
    if not ledger:
        ledger = section(text, "## 10. 证据台账")  # legacy fallback
    ledger_headers = ["证据ID", "发布方", "访问日期", "已打开", "时效", "局限"]
    legacy_headers = ["Claim ID", "Publisher", "Accessed", "Opened", "Freshness", "Limitation"]
    if mode == "full":
        if not any(h in ledger for h in ledger_headers) and not any(h in ledger for h in legacy_headers):
            errors.append("evidence ledger missing (appendix A)")
        else:
            active = ledger_headers if any(h in ledger for h in ledger_headers) else legacy_headers
            for header in active:
                if header not in ledger:
                    errors.append(f"evidence ledger missing field: {header}")

    opened_rows = [line for line in ledger.splitlines() if re.search(r"\|\s*(?:yes|是)\s*\|", line, re.IGNORECASE)]
    for row in opened_rows:
        if re.search(r"\|\s*(?:—|-|未记录|n/a)\s*\|\s*(?:yes|是)\s*\|", row, re.IGNORECASE):
            errors.append("opened evidence row is missing a usable locator")
        if not re.search(r"https?://", row):
            errors.append("opened evidence row is missing an original-source URL")

    # Ledger limitation cells must not all be one identical sentence.
    ledger_data_rows = table_rows(ledger)
    if len(ledger_data_rows) > 3:
        limitations = [row[-1] for row in ledger_data_rows[1:] if row and len(row[-1]) > 8]
        if limitations and len(set(limitations)) == 1:
            errors.append("every ledger Limitation cell is the same sentence; write per-source limitations")

    ledger_ids = re.findall(r"^\|\s*(E\d+)\s*\|", ledger, re.MULTILINE)
    duplicate_ids = sorted({claim_id for claim_id in ledger_ids if ledger_ids.count(claim_id) > 1})
    if duplicate_ids:
        errors.append(f"duplicate evidence IDs in ledger: {', '.join(duplicate_ids)}")
    referenced_ids = set(re.findall(r"\bE\d+\b", text))
    missing_ids = sorted(referenced_ids - set(ledger_ids))
    if missing_ids:
        errors.append(f"evidence IDs referenced but absent from ledger: {', '.join(missing_ids)}")
    if mode == "full" and strict and len(ledger_ids) < 8:
        errors.append(f"full strict report has only {len(ledger_ids)} evidence-ledger rows; expected at least 8")

    ledger_table = table_rows(ledger)
    if ledger_table:
        headers = ledger_table[0]
        publisher_header = "发布方" if "发布方" in headers else "Publisher"
        if publisher_header in headers:
            publisher_index = headers.index(publisher_header)
            publishers = {
                row[publisher_index].strip()
                for row in ledger_table[1:]
                if len(row) > publisher_index and row[publisher_index].strip()
            }
            if mode == "full" and strict and len(publishers) < 5:
                errors.append(f"evidence ledger has only {len(publishers)} distinct publishers; expected at least 5")

    # --- Appendix C: readiness + execution ---
    readiness = section(text, "## 附录C 证据就绪度与研究执行记录")
    if not readiness:
        readiness = section(text, "## 0. 结论与证据就绪度")  # legacy fallback
    for lane in READINESS_LANES:
        if mode == "full" and lane not in readiness:
            errors.append(f"missing evidence-readiness lane: {lane}")

    for row in readiness.splitlines():
        match = re.match(
            r"^\|\s*(.+?)\s*\|\s*(Ready|Gap|就绪|缺口)\s*\|\s*(\d+)\s*\|\s*(\d+)",
            row,
            re.IGNORECASE,
        )
        if not match:
            continue
        lane, status, opened, required = match.groups()
        if status.lower() in ("ready", "就绪") and int(opened) < int(required):
            errors.append(
                f"readiness lane '{lane.strip()}' is Ready but has {opened} opened sources; requires {required}"
            )

    has_gap = bool(re.search(r"\|\s*(?:Gap|缺口)\s*\|", readiness, re.IGNORECASE))
    conclusion_zone = overview if overview else readiness
    if has_gap and re.search(r"结论状态[：:]\s*可发布", conclusion_zone):
        errors.append("report has evidence gaps but conclusion status is publishable")
    if has_gap and not re.search(r"结论状态[：:]\s*(?:暂定|阶段待验证)", conclusion_zone):
        errors.append("report has evidence gaps but conclusion is not marked provisional")

    for row in readiness.splitlines():
        if re.search(r"\|\s*(?:complete|完成)\s*\|", row, re.IGNORECASE) and not re.search(r"\bE\d+\b", row):
            errors.append("research row marked complete without evidence IDs")

    urls = set(re.findall(r"https?://[^)\s|>]+", text))
    if mode == "full" and strict and len(urls) < 8:
        errors.append(f"full strict report has only {len(urls)} distinct source URLs; expected at least 8")
    elif mode == "full" and len(urls) < 8:
        warnings.append(f"only {len(urls)} distinct source URLs")

    if re.search(r"Original Opened\?", text):
        errors.append("legacy self-attestation column 'Original Opened?' remains; use the evidence ledger")
    if re.search(r"\|\s*Latest\?\s*\|", text):
        errors.append("legacy 'Latest?' checkbox remains; use metric-level freshness and access dates")

    return errors, warnings


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("report", type=Path)
    parser.add_argument("--mode", choices=("quick", "full"), default="full")
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()

    text = args.report.read_text(encoding="utf-8")
    errors, warnings = validate(text, args.mode, args.strict)

    for item in warnings:
        print(f"WARNING: {item}")
    for item in errors:
        print(f"ERROR: {item}")

    if errors:
        print(f"Report validation failed: {len(errors)} error(s), {len(warnings)} warning(s).")
        return 1

    print(f"Report validation passed: {len(warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
