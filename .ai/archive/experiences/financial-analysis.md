# Experience Knowledge: financial-analysis

> 跨项目可复用经验资产（V0.1.3 Experience Knowledge）。来源：investment-research-system 项目两轮真实执行，2026-08-09 用户确认沉淀。

## 日期
2026-08-09

## 项目
investment-research-system（来源项目）

## 场景
上市公司财报深度分析（贵州茅台 600519.SH / 紫光股份 000938.SZ），引用项目 workflow `financial-report-analysis`（获取层→分析层→输出层，交付三件套）

## 结果
全链路跑通，三件套交付齐全（深度分析报告 + 风险识别报告 + 可视化报告），含年报文本链与证据链；两次执行分别验证了不同环节

## 优点
- 数据层抽离为 workspace 共享 internal skills（tushare-connector / cninfo-connector），跨项目 by-name 复用，example-project 验证零配置可用
- 年报文本核对机制有效：三表数据与年报附注/审计意见交叉验证
- financial-report-generator 引擎验证可用，输出标准三表分析

## 不足
- marketpulse 无 AISA_API_KEY 时降级跳过，美股数据缺口需在报告中注明
- 可视化报告 HTML 生成稳定，MD 转换缺工具（可选）
- cnfinancialscraper 的 cninfo_scraper orgId 硬编码有 bug（已由动态 orgId 构造替代并归档）
- 原 skillhub financial-report-analysis 内置 SAMPLE_DATA 为假数据，不可直接使用（已被自建替代）

## 建议
- 环比需注意年报/季报口径，应使用同比
- 构造 xlsx 必须为横向表：行=指标名，列=报告期（纯日期），第一行是期间行；纵向表会导致报告全空
- cninfo 数据走巨潮官方动态 orgId 构造（gssz/gssh+代码）；东财 search 接口返回非 JSON
- tushare income.n_income 为合并净利，归母口径看 n_income_attr_p 或年报文本
- 负债率跳变需结合年报"购买子公司少数股权"等现金流科目核实

---

## 原 workflow lessons 全文（迁移备份，2026-08-09）

1. 2026-08-09 首次真实执行（贵州茅台 600519.SH）：tushare 数据层 + 三表解读 + 量化风险检查 + 可视化报告全链路跑通
2. marketpulse 无 AISA_API_KEY 降级跳过
3. financial-fraud-index 无 PDF 输入用量化版替代
4. financial-report-analysis 内置 SAMPLE_DATA 为假数据不可直接用（需真实数据）
5. 环比需注意年报/季报口径（应同比）
6. 可视化报告 HTML 生成成功、MD 转换缺工具可选
7. 本 workflow 为项目投资研究的子流程（原编排 skill 已并入本流程，2026-08-09 重构）
8. 2026-08-09 补充年报获取步骤（cnfinancialscraper，打通 fraud-index 完整版输入链）
9. 2026-08-09 步骤按原编排详细度展开子要点（可执行性增强）
10. 2026-08-09 第二次执行（紫光股份 000938.SZ）验证年报文本链：cnfinancialscraper 的 cninfo_scraper orgId 硬编码有 bug（000938→9900013389 错误，正确为 gssz0000938），已用项目 scripts/cninfo_client.py（动态 orgId 构造 gssz/gssh+代码）适配替代
11. 东财接口 search 返回非 JSON 需走巨潮官方
12. tushare income.n_income 为合并净利（归母看 n_income_attr_p 或年报文本）
13. 负债率跳变需结合年报"购买子公司少数股权"现金流科目核实
14. 2026-08-09 数据层抽离为 workspace 共享 internal skills（tushare-connector / cninfo-connector），跨项目 by-name 引用，从 example-project 验证零配置可用

## 未来应采取的行动

- 财报项目默认先获取真实三表和法定披露原文，再执行解读、风险和报告生成。
- 年报/季报比较使用同比口径；归母净利润优先使用 `n_income_attr_p` 或年报原文复核。
- 不恢复使用包含模拟数据的 `financial-report-analysis` 生成正式报告。

## 适用范围

A股上市公司财报分析、三表交叉验证和标准报告生成。验证资源：`tushare-connector@internal`、`cninfo-connector@internal`、`financial-report-generator@internal`。

## 不适用范围

缺少真实财务数据或法定披露原文时，不应据此给出精确公司结论；美股数据需要另行验证适配资源。

## 关联资产

- Capability：`market-data`
- Skill：`tushare-connector`、`cninfo-connector`、`earnings-reader`、`financial-fraud-index`、`financial-report-generator`
