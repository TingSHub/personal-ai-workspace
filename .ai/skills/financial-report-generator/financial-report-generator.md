# financial-report-generator

> 管理资产：`.ai/skills/financial-report-generator/financial-report-generator.md`；安装实体：`.claude/skills/financial-report-generator/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | internal · workspace internal |
| installed_ref | internal |
| runtime | both |
| 调用入口 | $financial-report-generator |
| 要求 | 真实且字段口径明确的财务数据 JSON |
| 更新 | internal · 在 workspace 源码中评审修改并同步安装实体；验证：使用已核对的真实三表样本验证核心指标 |
| 辅助脚本 | — |
| 经验引用 | financial-analysis；financial-report-workflow |

workspace 自研 internal skill：标准三表财务分析报告生成器（真实数据输入，无模拟数据）。

## 来源

- internal（workspace 自建，2026-08-10）
- 继承原 skillhub financial-report-analysis 的计算引擎（指标/风险/评分/排版），**数据层完全重写**（原版 SAMPLE_DATA 模拟数据不可用）
- 原第三方 skill 已删除（2026-08-10，用户指示）

## 用途

- 任何项目需要标准三表财务分析报告时使用
- 输入真实财务数据 JSON（tushare-connector 取数 + 年报核对）→ 输出标准化报告
