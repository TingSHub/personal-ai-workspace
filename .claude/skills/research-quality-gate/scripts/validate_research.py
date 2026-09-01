#!/usr/bin/env python3
"""Deterministic quality checks for the listed-company research content pipeline."""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


REQUIRED_SECTIONS = (
    "公司投资摘要",
    "行业研究",
    "公司商业模式分析",
    "财务分析",
    "投资逻辑",
    "估值分析",
    "风险分析",
    "证据链",
)
RID_REQUIRED_SECTIONS = (
    "公司概览",
    "行业研究",
    "产业竞争分析",
    "公司业务分析",
    "护城河分析",
    "财务分析",
    "投资逻辑",
    "风险分析",
    "估值分析",
    "跟踪指标",
)
RID_CASE_MARKERS = ("Bull Case", "Base Case", "Bear Case")
LEDGER_FIELDS = ("claim", "source", "date", "confidence", "notes")
RISK_MARKERS = ("Bull Case", "Bear Case", "核心跟踪指标")
ADVICE_TERMS = ("稳赚", "必涨", "闭眼买", "强烈买入", "建议买入", "建议卖出", "目标价")
NUMBER_RE = re.compile(r"(?<![A-Za-z\d])[-+]?\d[\d,]*(?:\.\d+)?(?:%|亿元|万元|亿美元|倍|个百分点)?")
EVIDENCE_RE = re.compile(r"\bE\d{3,}\b")
TIMECODE_RE = re.compile(
    r"^(\d{2}):(\d{2}):(\d{2}),(\d{3}) --> (\d{2}):(\d{2}):(\d{2}),(\d{3})$"
)
TIME_RANGE_RE = re.compile(
    r"\b\d{1,2}:\d{2}(?::\d{2})?\s*[-–—]\s*\d{1,2}:\d{2}(?::\d{2})?\b"
)


@dataclass
class Finding:
    level: str
    check: str
    detail: str
    owner: str


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def normalize_number(token: str) -> str:
    token = token.replace(",", "")
    match = re.match(r"([-+]?\d+(?:\.\d+)?)(.*)", token)
    if not match:
        return token
    number, unit = match.groups()
    try:
        value = abs(float(number))
        number = f"{value:.8f}".rstrip("0").rstrip(".")
    except ValueError:
        pass
    return number + unit


def numbers(text: str) -> set[str]:
    text = re.sub(r"^\d{2}:\d{2}:\d{2},\d{3} --> .*?$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\d+\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"(?<!\d)\d{1,2}:\d{2}(?:-\d{1,2}:\d{2})?", "", text)
    text = re.sub(r"建议时长[：:]\s*\d+秒", "", text)
    values: set[str] = set()
    for match in NUMBER_RE.finditer(text):
        token = normalize_number(match.group())
        bare = re.match(r"[-+]?\d+(?:\.\d+)?", token)
        if not bare:
            continue
        value = float(bare.group())
        # Years, headings, evidence IDs, durations and isolated small counters are not research facts.
        if 1900 <= value <= 2100 and not re.search(r"%|亿元|万元|亿美元|倍|个百分点", token):
            continue
        if value <= 15 and not re.search(r"%|亿元|万元|亿美元|倍|个百分点", token):
            continue
        values.add(token)
    return values


def split_number(token: str) -> tuple[float, str]:
    match = re.match(r"([-+]?\d+(?:\.\d+)?)(.*)", token)
    if not match:
        return 0.0, token
    return abs(float(match.group(1))), match.group(2)


def unsupported_numbers(candidate: set[str], source: set[str]) -> list[str]:
    source_parts = [split_number(token) for token in source]
    unsupported: list[str] = []
    for token in candidate:
        value, unit = split_number(token)
        matched = False
        for source_value, source_unit in source_parts:
            if unit != source_unit:
                continue
            tolerance = max(0.005, abs(source_value) * 0.0005)
            if abs(value - source_value) <= tolerance:
                matched = True
                break
            if value.is_integer() and round(source_value) == value:
                matched = True
                break
        if not matched:
            unsupported.append(token)
    return sorted(unsupported)


def tc_ms(parts: tuple[str, ...]) -> int:
    h, m, s, ms = map(int, parts)
    return ((h * 60 + m) * 60 + s) * 1000 + ms


def check_srt(text: str) -> list[str]:
    errors: list[str] = []
    blocks = [block.strip().splitlines() for block in re.split(r"\n\s*\n", text.strip()) if block.strip()]
    previous_end = -1
    expected = 1
    for block in blocks:
        if block and block[0].strip().lower().startswith("note"):
            continue
        if len(block) < 3:
            errors.append(f"字幕块 {expected} 少于三行")
            expected += 1
            continue
        if block[0].strip() != str(expected):
            errors.append(f"字幕块 {expected} 序号为 {block[0].strip()!r}")
        match = TIMECODE_RE.match(block[1].strip())
        if not match:
            errors.append(f"字幕块 {expected} 时间码非法：{block[1].strip()}")
            continue
        start = tc_ms(match.groups()[:4])
        end = tc_ms(match.groups()[4:])
        if end <= start:
            errors.append(f"字幕块 {expected} 结束时间不晚于开始时间")
        if start < previous_end:
            errors.append(f"字幕块 {expected} 与前一块重叠或倒序")
        previous_end = end
        expected += 1
    if expected == 1:
        errors.append("SRT 没有字幕块")
    return errors


def add(findings: list[Finding], level: str, check: str, detail: str, owner: str) -> None:
    findings.append(Finding(level, check, detail, owner))


def has_any(text: str, terms: tuple[str, ...]) -> bool:
    return any(term in text for term in terms)


def section_blocks(text: str, heading_re: str) -> list[str]:
    matches = list(re.finditer(heading_re, text, re.MULTILINE))
    blocks: list[str] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        blocks.append(text[match.start() : end])
    return blocks


def check_narrative_plan(text: str, findings: list[Finding]) -> None:
    owner = "content-production"
    checks = (
        ("用户定位", ("目标观众", "受众", "用户定位"), ("用户痛点", "痛点")),
        ("核心冲突", ("核心冲突", "为什么用户应该关注"), ()),
        ("Hook设计", ("Hook", "开场", "前30秒"), ()),
        ("故事结构", ("故事结构", "8-15分钟", "8-15 分钟"), ()),
        ("标题方向", ("标题", "标题候选", "标题方向"), ()),
    )
    for check, required_a, required_b in checks:
        if has_any(text, required_a) and (not required_b or has_any(text, required_b)):
            add(findings, "PASS", f"内容策划/{check}", "关键字段存在", owner)
        else:
            add(findings, "FAIL", f"内容策划/{check}", "缺少关键字段", owner)

    angle_count = len(re.findall(r"(?:^|\n)\s*(?:[-*]|\d+[.、])\s*.*(?:角度|主题)", text))
    if angle_count < 2:
        angle_count = len(re.findall(r"角度[一二三四五六七八九十\d]", text))
    if angle_count >= 2:
        add(findings, "PASS", "内容策划/视频主题", f"识别 {angle_count} 个内容角度", owner)
    else:
        add(findings, "FAIL", "内容策划/视频主题", "少于 2 个内容角度", owner)

    if has_any(text, ("8-15分钟", "8-15 分钟")) or len(TIME_RANGE_RE.findall(text)) >= 4:
        add(findings, "PASS", "内容策划/8-15分钟结构", "结构时长或分段存在", owner)
    else:
        add(findings, "FAIL", "内容策划/8-15分钟结构", "缺少 8-15 分钟结构或足够时间分段", owner)


def check_long_script(text: str, findings: list[Finding]) -> None:
    owner = "content-production"
    required = (
        ("Hook", ("Hook", "钩子", "开场")),
        ("行业背景", ("行业背景", "行业")),
        ("公司优势", ("公司优势", "公司")),
        ("财务验证", ("财务验证", "财务")),
        ("投资逻辑", ("投资逻辑",)),
        ("风险", ("风险", "Bear Case")),
        ("总结", ("总结", "核心观点")),
        ("跟踪指标", ("跟踪指标", "观察指标")),
    )
    missing = [name for name, terms in required if not has_any(text, terms)]
    if missing:
        add(findings, "FAIL", "长视频脚本结构", f"缺少：{', '.join(missing)}", owner)
    else:
        add(findings, "PASS", "长视频脚本结构", "Hook、正文、风险、总结和跟踪指标均存在", owner)


def check_short_scripts(text: str, findings: list[Finding]) -> None:
    owner = "content-production"
    blocks = section_blocks(text, r"^##\s+(?:短视频|Short Video)\s*[1-5](?:\s*[:：].*)?$")
    if not blocks:
        blocks = re.split(r"\n(?=短视频\s*\d+|第[一二三四五]条)", text)
        blocks = [block for block in blocks if "短视频" in block or "标题" in block]
    count = len(blocks)
    if 3 <= count <= 5:
        add(findings, "PASS", "短视频数量", f"识别 {count} 个短视频", owner)
    else:
        add(findings, "FAIL", "短视频数量", f"识别 {count} 个短视频，要求 3-5 个", owner)
    for index, block in enumerate(blocks, 1):
        missing = [
            label
            for label, terms in (
                ("标题", ("标题", "## 短视频", "## Short Video")),
                ("Hook", ("Hook", "钩子")),
                ("内容", ("内容", "正文", "核心观点")),
                ("结尾", ("结尾", "收尾")),
            )
            if not has_any(block, terms)
        ]
        if missing:
            add(findings, "FAIL", f"短视频 {index} 结构", f"缺少：{', '.join(missing)}", owner)
    all_blocks_complete = all(
        has_any(block, ("标题", "## 短视频", "## Short Video"))
        and has_any(block, ("Hook", "钩子"))
        and has_any(block, ("内容", "正文", "核心观点"))
        and has_any(block, ("结尾", "收尾"))
        for block in blocks
    )
    if blocks and all_blocks_complete:
        add(findings, "PASS", "短视频结构", "每个短视频均包含标题、Hook、内容和结尾", owner)


def check_material_plan(material: str, defined: set[str], findings: list[Finding]) -> None:
    owner = "content-production"
    material_refs = set(EVIDENCE_RE.findall(material))
    table_lines = [
        line.strip()
        for line in material.splitlines()
        if line.strip().startswith("|") and not re.match(r"^\|\s*-", line.strip())
    ]
    header = table_lines[0] if table_lines else ""
    rows = table_lines[1:]
    missing_headers = [term for term in ("画面", "图表", "来源") if term not in header]
    row_errors: list[str] = []
    for index, row in enumerate(rows, 1):
        if not TIME_RANGE_RE.search(row):
            row_errors.append(f"第 {index} 行缺少时间段")
        if not EVIDENCE_RE.search(row):
            row_errors.append(f"第 {index} 行缺少 E### 证据")
    if missing_headers or not rows or row_errors:
        details = []
        if missing_headers:
            details.append(f"缺少列：{', '.join(missing_headers)}")
        if not rows:
            details.append("缺少素材行")
        details.extend(row_errors)
        add(findings, "FAIL", "素材规划结构", "；".join(details), owner)
    elif material_refs - defined:
        add(findings, "FAIL", "素材规划结构", f"素材引用未知证据：{', '.join(sorted(material_refs - defined))}", owner)
    else:
        add(findings, "PASS", "素材规划结构", f"{len(rows)} 个时间段均包含画面、图表、来源和证据", owner)


def validate_research_intelligence(path: Path, output: Path) -> int:
    findings: list[Finding] = []
    owner = "investment-research"
    if not path.is_file():
        add(findings, "FAIL", "文件存在", str(path), owner)
        text = ""
    else:
        text = read_text(path)

    for section in RID_REQUIRED_SECTIONS:
        pattern = rf"^##\s+(?:\d+\.\s*)?{re.escape(section)}\s*$"
        if re.search(pattern, text, re.MULTILINE):
            add(findings, "PASS", f"RID章节：{section}", "存在", owner)
        else:
            add(findings, "FAIL", "RID十章节", f"缺少：{section}", owner)

    absent_cases = [marker for marker in RID_CASE_MARKERS if marker not in text]
    if absent_cases:
        add(findings, "FAIL", "情景完整性", f"缺少：{'、'.join(absent_cases)}", owner)
    else:
        add(findings, "PASS", "情景完整性", "Bull、Base、Bear Case均存在", owner)

    ledger_match = re.search(r"^##\s+Evidence Ledger\s*$([\s\S]*?)(?=^##\s+|\Z)", text, re.MULTILINE)
    ledger = ledger_match.group(1) if ledger_match else ""
    if not ledger:
        add(findings, "FAIL", "Evidence Ledger", "缺少独立Evidence Ledger章节", owner)
    else:
        table_header = next((line.lower() for line in ledger.splitlines() if line.strip().startswith("|")), "")
        missing_fields = [field for field in LEDGER_FIELDS if field not in table_header]
        if missing_fields:
            add(findings, "FAIL", "Evidence Ledger字段", f"缺少：{', '.join(missing_fields)}", owner)
        else:
            add(findings, "PASS", "Evidence Ledger字段", "claim、source、date、confidence、notes齐全", owner)
        evidence_ids = set(EVIDENCE_RE.findall(ledger))
        if evidence_ids:
            add(findings, "PASS", "Evidence Ledger条目", f"识别{len(evidence_ids)}个证据编号", owner)
        else:
            add(findings, "FAIL", "Evidence Ledger条目", "未找到E###证据条目", owner)

    compression_constraint = re.search(
        r"(?:按|为了)(?:视频时长|传播|阅读时间).{0,12}(?:压缩|删减|精简)"
        r"|(?:篇幅|字数|视频时长).{0,12}(?:控制在|限制为)\s*\d+"
        r"|精简为\s*\d+[字页]",
        text,
    )
    if compression_constraint:
        add(findings, "FAIL", "研究阶段边界", "正文包含传播或篇幅压缩约束", owner)
    else:
        add(findings, "PASS", "研究阶段边界", "未发现传播或篇幅压缩约束", owner)

    failures = sum(item.level == "FAIL" for item in findings)
    status = "FAIL" if failures else "PASS"
    rows = [
        "# Research Intelligence Quality Report",
        "",
        f"- 结论：**{status}**",
        f"- 阻断项：{failures}",
        "",
        "|级别|检查项|结果|问题归属|",
        "|---|---|---|---|",
        *[f"|{x.level}|{x.check}|{x.detail.replace('|', '／')}|{x.owner}|" for x in findings],
        "",
        "## 输入版本",
        "",
        f"- research_intelligence_document: `{path}`",
        "",
        "> 本门禁只做确定性结构检查，不替代逐条来源复核；FAIL 应退回 investment-research。",
    ]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"{status}: {output}")
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--master", type=Path)
    parser.add_argument("--research-intelligence", type=Path)
    parser.add_argument("--scripts", type=Path)
    parser.add_argument("--narrative-plan", type=Path)
    parser.add_argument("--long-script", type=Path)
    parser.add_argument("--short-scripts", type=Path)
    parser.add_argument("--subtitles", type=Path)
    parser.add_argument("--materials", type=Path)
    parser.add_argument("--evidence", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    if args.research_intelligence:
        if args.master or args.scripts or args.narrative_plan or args.long_script or args.short_scripts:
            parser.error("--research-intelligence is a research-only mode and cannot be combined with content inputs")
        return validate_research_intelligence(args.research_intelligence, args.output)

    if not args.master:
        parser.error("provide --master for content validation or --research-intelligence for research-only validation")
    if not (args.subtitles and args.materials and args.evidence):
        parser.error("content validation requires --subtitles, --materials and --evidence")

    if not args.scripts and not (args.narrative_plan and args.long_script and args.short_scripts):
        parser.error("provide either --scripts or all of --narrative-plan, --long-script and --short-scripts")

    inputs = {
        "master": args.master,
        "subtitles": args.subtitles,
        "materials": args.materials,
        "evidence": args.evidence,
    }
    if args.scripts:
        inputs["scripts"] = args.scripts
    else:
        inputs["narrative_plan"] = args.narrative_plan
        inputs["long_script"] = args.long_script
        inputs["short_scripts"] = args.short_scripts
    findings: list[Finding] = []
    missing = [f"{name}: {path}" for name, path in inputs.items() if not path.is_file()]
    if missing:
        for item in missing:
            add(findings, "FAIL", "文件存在", item, "workflow")
        texts = {name: "" for name in inputs}
    else:
        texts = {name: read_text(path) for name, path in inputs.items()}

    master = texts["master"]
    legacy_mode = "scripts" in texts
    narrative_plan = "" if legacy_mode else texts["narrative_plan"]
    long_script = texts["scripts"] if legacy_mode else texts["long_script"]
    short_scripts = "" if legacy_mode else texts["short_scripts"]
    script = texts["scripts"] if legacy_mode else f"{long_script}\n\n{short_scripts}"
    srt = texts["subtitles"]
    material = texts["materials"]
    evidence = texts["evidence"]

    for section in REQUIRED_SECTIONS:
        if not re.search(rf"^##\s+(?:\d+\.\s*)?{re.escape(section)}\s*$", master, re.MULTILINE):
            add(findings, "FAIL", "母稿八章节", f"缺少：{section}", "research-master-document-generation")
    if all(marker in master for marker in RISK_MARKERS):
        add(findings, "PASS", "风险完整性", "Bull Case、Bear Case、核心跟踪指标均存在", "investment-research")
    else:
        absent = "、".join(marker for marker in RISK_MARKERS if marker not in master)
        add(findings, "FAIL", "风险完整性", f"缺少：{absent}", "investment-research")

    defined = set(EVIDENCE_RE.findall(evidence))
    referenced = set(EVIDENCE_RE.findall(master + narrative_plan + script + material))
    unknown = sorted(referenced - defined)
    if not defined:
        add(findings, "FAIL", "证据链", "未找到 E### 证据条目", "investment-research")
    elif unknown:
        add(findings, "FAIL", "证据链", f"未知证据编号：{', '.join(unknown)}", "investment-research")
    else:
        add(findings, "PASS", "证据链", f"识别 {len(defined)} 个证据编号，引用均可解析", "investment-research")

    master_numbers = numbers(master)
    srt_numbers = numbers(srt)
    script_owner = "content-production"
    script_check = "母稿→脚本数字" if legacy_mode else "母稿→长视频数字"
    script_new = unsupported_numbers(numbers(long_script), master_numbers)
    srt_new = unsupported_numbers(srt_numbers, master_numbers)
    if script_new:
        add(findings, "FAIL", script_check, f"脚本新增数字：{', '.join(script_new)}", script_owner)
    else:
        add(findings, "PASS", script_check, f"脚本 {len(numbers(long_script))} 个关键数字均见于母稿", script_owner)
    if not legacy_mode:
        short_new = unsupported_numbers(numbers(short_scripts), master_numbers)
        if short_new:
            add(findings, "FAIL", "母稿→短视频数字", f"短视频新增数字：{', '.join(short_new)}", "content-production")
        else:
            add(findings, "PASS", "母稿→短视频数字", f"短视频 {len(numbers(short_scripts))} 个关键数字均见于母稿", "content-production")
    if srt_new:
        add(findings, "FAIL", "母稿→字幕数字", f"字幕新增数字：{', '.join(srt_new)}", "content-production")
    else:
        add(findings, "PASS", "母稿→字幕数字", f"字幕 {len(srt_numbers)} 个关键数字均见于母稿", "content-production")
    if not legacy_mode:
        srt_script_new = unsupported_numbers(srt_numbers, numbers(long_script))
        if srt_script_new:
            add(findings, "FAIL", "长视频→字幕数字", f"字幕数字未见于长视频脚本：{', '.join(srt_script_new)}", "content-production")
        else:
            add(findings, "PASS", "长视频→字幕数字", f"字幕 {len(srt_numbers)} 个关键数字均见于长视频脚本", "content-production")

    if not legacy_mode:
        check_narrative_plan(narrative_plan, findings)
        check_long_script(long_script, findings)
        check_short_scripts(short_scripts, findings)

    combined_content = re.sub(r"^- \[[ xX]\].*$", "", script + "\n" + srt, flags=re.MULTILINE)
    advice_hits = []
    for term in ADVICE_TERMS:
        for match in re.finditer(re.escape(term), combined_content):
            prefix = combined_content[max(0, match.start() - 4) : match.start()]
            if not re.search(r"不(?:提供|做|是|构成)?$", prefix):
                advice_hits.append(term)
                break
    advice_hits = sorted(set(advice_hits))
    if advice_hits:
        add(findings, "FAIL", "投资建议化表达", f"命中：{', '.join(advice_hits)}", script_owner)
    else:
        add(findings, "PASS", "投资建议化表达", "未命中硬性禁语", script_owner)

    srt_errors = check_srt(srt) if srt else ["SRT 文件为空"]
    if srt_errors:
        add(findings, "FAIL", "SRT 格式", "；".join(srt_errors), "content-production")
    else:
        add(findings, "PASS", "SRT 格式", "序号、时间码和时序通过", "content-production")
        if re.search(r"\bestimated\b|估算|待校准|最终配音", srt, re.IGNORECASE):
            add(findings, "WARN", "SRT 估算时间轴", "检测到 estimated/估算时间轴标记，需按最终音频校准", "content-production")

    if legacy_mode:
        material_refs = set(EVIDENCE_RE.findall(material))
        if "|" not in material or not material_refs:
            add(findings, "FAIL", "素材引用", "素材清单缺少表格或 E### 证据引用", "content-production")
        elif material_refs - defined:
            add(findings, "FAIL", "素材引用", f"素材引用未知证据：{', '.join(sorted(material_refs - defined))}", "content-production")
        else:
            add(findings, "PASS", "素材引用", f"{len(material_refs)} 个素材证据引用均可解析", "content-production")
    else:
        check_material_plan(material, defined, findings)

    material_gaps = sorted({term for term in ("待授权", "需上线前更新", "待校准", "最终配音") if term in material})
    if material_gaps:
        add(
            findings,
            "WARN",
            "制作就绪度",
            f"仍有制作前置项：{', '.join(material_gaps)}",
            "content-production",
        )

    add(
        findings,
        "WARN",
        "语义复核",
        "仍需人工逐条确认：脚本无母稿外新事实/新增因果，预测与弱信号未被强化，风险未被削弱，画面不产生误导。",
        "quality-assurance",
    )

    failures = sum(item.level == "FAIL" for item in findings)
    warnings = sum(item.level == "WARN" for item in findings)
    status = "FAIL" if failures else ("PASS WITH WARNINGS" if warnings else "PASS")
    rows = [
        "# Research Quality Report",
        "",
        f"- 结论：**{status}**",
        f"- 阻断项：{failures}",
        f"- 自动告警：{warnings}",
        "",
        "|级别|检查项|结果|问题归属|",
        "|---|---|---|---|",
    ]
    rows.extend(f"|{x.level}|{x.check}|{x.detail.replace('|', '／')}|{x.owner}|" for x in findings)
    rows.extend(
        [
            "",
            "## 输入版本",
            "",
            *[f"- {name}: `{path}`" for name, path in inputs.items()],
            "",
            "## 语义复核记录",
            "",
            "- [ ] 脚本没有母稿外新事实或新增因果关系",
            "- [ ] 预测、推断和弱信号没有被改写为确定事实",
            "- [ ] Bull Case、Bear Case、风险影响和观察指标完整保留",
            "- [ ] 没有夸大表述、收益承诺或直接买卖建议",
            "- [ ] 素材画面不会暗示母稿未支持的事实",
            "",
            "> 本门禁只验收，不修复内容；FAIL 应退回表中对应 Capability。",
        ]
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"{status}: {args.output}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
