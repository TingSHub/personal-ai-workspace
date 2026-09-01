#!/usr/bin/env python3
"""上市公司标准财务分析报告生成器（workspace 自研 internal skill）。

继承原 skillhub financial-report-analysis 的计算引擎（指标/风险/评分/排版），
重写数据层：输入为真实财务数据 JSON（由 tushare-connector 取数生成），
无内置模拟数据，公司信息参数化。

用法（CLI）：
  python3 financial_report_generator.py <data.json>
  数据 JSON 结构见下（与 tushare-connector 输出对齐）：

  {
    "公司名称": "紫光股份", "股票代码": "000938",
    "行业": "IT设备", "上市日期": "1999-11-04", "注册资本": "26.53亿",
    "报告期": "2025年年报",
    "资产负债表": {"总资产": 963.0, "总负债": 788.0, "股东权益": 175.0,
                    "流动资产": 722.0, "流动负债": 662.0},
    "利润表": {"营业收入": 967.48, "营业成本": 826.32,
               "净利润": 21.7, "毛利润": 141.16},
    "现金流量表": {"经营活动现金流": 34.87, "投资活动现金流": -5.3,
                    "筹资活动现金流": -16.49}
  }

用法（库）：
  from financial_report_generator import analyze_report, format_report
  report = analyze_report(data_dict)
  print(format_report(report))
"""
import json
import sys
from datetime import datetime
from typing import Dict, List


def calculate_financial_ratios(financial_data: Dict) -> Dict:
    """计算财务指标（盈利能力/偿债能力/运营能力/现金流）。"""
    bs, inc, cf = financial_data["资产负债表"], financial_data["利润表"], financial_data["现金流量表"]
    roe = inc["净利润"] / bs["股东权益"] * 100
    roa = inc["净利润"] / bs["总资产"] * 100
    gross_margin = inc["毛利润"] / inc["营业收入"] * 100
    net_margin = inc["净利润"] / inc["营业收入"] * 100
    debt_ratio = bs["总负债"] / bs["总资产"] * 100
    current_ratio = bs["流动资产"] / bs["流动负债"]
    asset_turnover = inc["营业收入"] / bs["总资产"]
    ocf_to_ni = cf["经营活动现金流"] / inc["净利润"]
    return {
        "盈利能力": {
            "ROE(净资产收益率)": f"{roe:.2f}%",
            "ROA(总资产收益率)": f"{roa:.2f}%",
            "毛利率": f"{gross_margin:.2f}%",
            "净利率": f"{net_margin:.2f}%",
        },
        "偿债能力": {
            "资产负债率": f"{debt_ratio:.2f}%",
            "流动比率": f"{current_ratio:.2f}",
            "速动比率": f"{current_ratio:.2f}",
        },
        "运营能力": {"总资产周转率": f"{asset_turnover:.2f}"},
        "现金流": {"经营现金流/净利润": f"{ocf_to_ni:.2f}"},
    }


def analyze_risks(financial_data: Dict, ratios: Dict) -> List[Dict]:
    """风险分析（规则化）。"""
    risks = []
    debt_ratio = float(ratios["偿债能力"]["资产负债率"].replace("%", ""))
    if debt_ratio > 70:
        risks.append({"类型": "偿债风险", "等级": "高",
                      "描述": f"资产负债率为{debt_ratio:.2f}%，高于70%警戒线",
                      "建议": "关注公司债务结构和偿债能力"})
    elif debt_ratio > 50:
        risks.append({"类型": "偿债风险", "等级": "中",
                      "描述": f"资产负债率为{debt_ratio:.2f}%，处于中等水平",
                      "建议": "需关注债务变化趋势"})
    cash_ratio = float(ratios["现金流"]["经营现金流/净利润"])
    if cash_ratio < 0.8:
        risks.append({"类型": "现金流风险", "等级": "高",
                      "描述": "经营活动现金流/净利润低于0.8，利润质量存疑",
                      "建议": "关注应收账款和存货情况"})
    return risks


def generate_investment_advice(ratios: Dict, risks: List[Dict]) -> Dict:
    """投资建议（100 分制评分模型）。"""
    score = 100
    for risk in risks:
        score -= 20 if risk["等级"] == "高" else 10
    roe = float(ratios["盈利能力"]["ROE(净资产收益率)"].replace("%", ""))
    if roe > 20:
        score += 10
    if score >= 90:
        rating, advice = "优秀", "公司财务状况优秀，具备投资价值"
    elif score >= 70:
        rating, advice = "良好", "公司财务状况良好，可考虑投资"
    elif score >= 60:
        rating, advice = "一般", "公司财务状况一般，需谨慎投资"
    else:
        rating, advice = "较差", "公司财务状况较差，不建议投资"
    return {"综合评分": score, "评级": rating, "投资建议": advice}


def analyze_report(data: Dict) -> Dict:
    """主分析函数：直接消费真实数据 dict（无内置模拟数据）。"""
    try:
        ratios = calculate_financial_ratios(data)
        risks = analyze_risks(data, ratios)
        advice = generate_investment_advice(ratios, risks)
        return {
            "分析时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "公司信息": {k: data[k] for k in ("公司名称", "股票代码", "行业", "上市日期", "注册资本") if k in data},
            "报告期": data["报告期"],
            "财务指标": ratios,
            "风险提示": risks if risks else [{"类型": "无明显风险", "等级": "低",
                                            "描述": "未发现重大财务风险", "建议": "继续保持关注"}],
            "投资建议": advice,
        }
    except KeyError as e:
        return {"错误": f"数据缺少字段: {e}"}
    except Exception as e:
        return {"错误": str(e)}


def format_report(report: Dict) -> str:
    """格式化报告为文本。"""
    if "错误" in report:
        return f"报告生成失败: {report['错误']}"
    lines = ["=" * 50, "财务分析报告", "=" * 50, "\n【公司信息】"]
    for k, v in report["公司信息"].items():
        lines.append(f"  {k}: {v}")
    lines.append(f"\n【报告期】{report['报告期']}")
    lines.append("\n【财务指标】")
    for category, metrics in report["财务指标"].items():
        lines.append(f"\n  {category}:")
        for k, v in metrics.items():
            lines.append(f"    - {k}: {v}")
    lines.append("\n【风险提示】")
    for risk in report["风险提示"]:
        lines.append(f"  - [{risk['等级']}] {risk['类型']}: {risk['描述']}")
        lines.append(f"    建议: {risk['建议']}")
    lines.append("\n【投资建议】")
    advice = report["投资建议"]
    lines.append(f"  综合评分: {advice['综合评分']}分")
    lines.append(f"  评级: {advice['评级']}")
    lines.append(f"  建议: {advice['投资建议']}")
    lines += ["\n" + "=" * 50, "免责声明: 本报告仅供参考，不构成投资建议", "=" * 50]
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    with open(sys.argv[1], encoding="utf-8") as f:
        report = analyze_report(json.load(f))
    print(format_report(report))
