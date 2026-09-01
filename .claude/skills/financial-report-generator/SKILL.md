---
name: financial-report-generator
description: 上市公司标准财务分析报告生成器（workspace 自研 internal skill）——输入真实财务数据 JSON（tushare-connector 取数），输出标准化三表分析报告（指标/风险/评分/排版）。当项目需要"标准三表财务分析报告"、"自动生成财务分析摘要"时使用。
---

# financial-report-generator

标准三表财务分析报告生成器。继承原 skillhub financial-report-analysis 的计算引擎，**重写数据层**：无内置模拟数据，公司信息参数化，输入为真实数据 JSON。

## 为什么存在

- 原 skillhub financial-report-analysis 内置 SAMPLE_DATA 模拟数据（假数据）+ 公司信息硬编码（白酒/2001-08-27），无法用于真实报告
- 本生成器吸收其可用的计算引擎（指标/风险规则/评分模型/报告排版），数据层全部重写

## 用法

CLI：
```bash
python3 <skill_dir>/scripts/financial_report_generator.py <data.json>
```

库：
```python
import sys; sys.path.insert(0, "<skill_dir>/scripts")
from financial_report_generator import analyze_report, format_report
report = analyze_report(data_dict)   # data_dict 为真实财务数据（见脚本 docstring 结构）
print(format_report(report))
```

## 数据输入结构（与 tushare-connector 输出对齐）

```json
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
```
单位：亿元。数据由 tushare-connector 取数 + 年报文本核对生成。

## 注意

- **净利润口径**：脚本按输入数据计算，合并净利与归母净利需在数据准备时明确（建议输入合并口径并注明）
- 速动比率当前为简化计算（=流动比率），如需精确值由数据层提供存货后扩展
- 输出为文本报告；免责声明自动附加

## Validation（操作后必须执行）

- 报告含【财务指标】且数值与输入数据计算一致（毛利率/负债率/现金流比抽查）
- 报告含【风险提示】与【投资建议】
- 输入缺失字段时返回明确错误而非崩溃
