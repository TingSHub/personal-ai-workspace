# Experience Knowledge: financial-report-workflow

> 跨项目可复用经验资产（V0.1.3 Experience Knowledge）。来源：investment-research-system 四件套报告全流程执行，2026-08-11 用户确认沉淀。

## 日期
2026-08-11

## 项目
investment-research-system（来源项目）

## 场景
紫光股份（000938.SZ）四件套财报分析报告全流程执行——升级后 workflow（12 步：三表→舆情→解读→行业对比→风险→估值→治理→输出）首跑，含数据层端点修复

## 结果
成功——四件套交付（深度分析/风险识别/可视化/标准三表），行业对比、估值、治理三个判断性章节首次产出真实结论

## 优点
- 行业对比（4.5）+ 估值历史分位（5.5）+ 治理股东交叉验证（6.5）带来此前缺失的判断性内容，报告深度质变
- web-search 舆情（multi-search/Tavily）检索到业绩预告（净利预增 83.5%+）与控股股东减持预警，与股东数据**交叉验证成立**
- dataviz 规范可视化（调色板验证通过、浅/深双主题、悬停、表格视图）提升交付形态
- financial-report-generator 数据链路（tushare 取数→JSON→标准报告）验证可用

## 不足
- tushare 主端点 fast.xiaodefa.cn 降级（三表/指标接口返空），切备用 tt.xiaodefa.cn 后可用
- 代理偶发连接错误，需重试 1-2 次
- 生成器字段坑：`total_cogs` 是营业总成本（应用 `oper_cost`）；流动资产/负债字段名是 `total_cur_assets`/`total_cur_liab`
- `.env` 行内注释会被解析进 URL（客户端不支持行内注释）
- marketpulse 无 AISA_API_KEY 降级（美股数据缺口）
- news-search 对公司名查询返回导航页（价值低），multi-search（Tavily）为主力

## 建议
- 数据层：端点优先 tt.xiaodefa.cn；查询失败重试；`.env` 注释独立成行
- 生成器输入：营业成本用 `oper_cost`；字段名以 tushare 实际返回为准（先探测字段再组装）
- web-search 步骤：multi-search `prefer_quality=True`（Tavily）为主，news-search 仅热点聚合补充
- 同名主体辨别（紫光古汉≠紫光股份）须持续执行

## 未来应采取的行动

- 财报工作流保留行业对比、历史估值、治理和来源交叉验证步骤。
- 数据接口失败时先验证端点和字段，再回退；`.env` 注释必须独立成行。
- 公司新闻检索优先使用 `multi-search`，`news-search` 作为热点聚合补充。
- 财务接口数据进入分析前按证券代码和报告期去重，并保留披露版本字段；冲突值回到法定财报核验。
- `free_cashflow` 等供应商衍生字段必须先与经营现金流和资本开支勾稽；无法解释时使用披露公式的近似口径并明确局限。
- 公告PDF采集同时验证文件存在和正文可检索，不能把下载成功等同于证据可用。

## 适用范围

A股上市公司多交付物财报研究。验证资源包括 `tushare-connector@internal`、`financial-report-generator@internal`、`multi-search@tree-sha256:6535cb0b3ab7`。

## 不适用范围

不适用于没有真实三表、年报原文或来源核验条件的快速生成任务。

## 关联资产

- Capability：`market-data`、`web-search`
- Skill：`tushare-connector`、`financial-report-generator`、`multi-search`、`news-search`

---

## 2026-08-12 数据规范化与公告可读性补充

### 来源项目与证据

`investment-research-system` 执行 `listed-company-research-video-production` 紫光股份首跑；项目记录为 `logs/listed-company-research-video-production-ziguang-20260812.md`。验证资源：`tushare-connector@internal`、`cninfo-connector@internal`。

### 经验证结论

1. 当前Tushare兼容接口在同一 `ts_code + end_date` 下可能返回重复财务记录，部分完全相同，部分字段一条为空、一条有值。不能直接拼接、累加或无条件取第一条。
2. 去重时应主动请求可用的 `ann_date`、`f_ann_date`、`report_type`、`update_flag`，优先使用最新有效披露；数值冲突时保留冲突并回到法定财报，不静默覆盖。
3. 本轮 `free_cashflow` 在重复记录中出现空值与不可勾稽数值，因此未直接使用。采用“经营现金流－购建长期资产支付现金”时，必须明确它是近似口径而非公司披露的正式自由现金流。
4. 当前 `cninfo-connector` 搜索CLI只展示公告ID，而下载调用需要 `adjunctUrl`，人工补路径会增加日期和URL错误风险。
5. PDF非空只证明下载成功；研究步骤还必须确认正文可检索、可定位。缺少本地PDF解析工具时，应在采集阶段选择已验证的替代解析路径。

### 适用与不适用范围

适用于当前Tushare兼容端点与CNINFO连接器支持的A股财报研究。资源更新后需结合 `installed_ref` 重新实测；不能据此推断所有Tushare官方接口都会重复，或所有运行环境都缺少PDF解析工具。
