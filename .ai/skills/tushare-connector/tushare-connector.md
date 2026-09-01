# tushare-connector

> 管理资产：`.ai/skills/tushare-connector/tushare-connector.md`；安装实体：`.claude/skills/tushare-connector/SKILL.md`

## 元数据

| 字段 | 值 |
|---|---|
| kind | skill |
| 来源 | internal · workspace internal |
| installed_ref | internal |
| runtime | both |
| 调用入口 | $tushare-connector |
| 要求 | TUSHARE_TOKEN；TUSHARE_API_URL；network |
| 更新 | internal · 在 workspace 源码中评审修改并同步安装实体；验证：调用 trade_cal 或 daily_basic 验证凭证、端点和字段解析 |
| 辅助脚本 | — |
| 经验引用 | financial-analysis；financial-report-workflow；industry-research-methodology；tushare-proxy-cashflow-distortion |

workspace 共享 internal skill：tushare 兼容 API 数据连接器（凭证/端点 .env 自动加载）。

## 来源

- internal（workspace 自建，2026-08-09 从 investment-research-system 项目抽离）
- 安装位置：`.claude/skills/tushare-connector/`（workspace 内，所有项目可见）

## 用途

- 任何项目获取 A股/港股/美股行情、财务三表、历史数据、行业基准
- 自动加载已配置的 `TUSHARE_TOKEN` / `TUSHARE_API_URL`；资源文档不保存凭证值
- 替代第三方 tushare-data skill 的 SDK 硬编码端点问题

## 注意事项与踩坑

- 接口可能返回空数据或代理连接失败；先验证端点与字段，再重试或回退。
- `.env` 行内注释可能被旧客户端解析进 URL，注释应独立成行。
- 财务接口在同一 `ts_code + end_date` 下可能返回重复记录。查询时尽量携带 `ann_date`、`f_ann_date`、`report_type`、`update_flag`，进入分析前按业务键去重；数值冲突时保留冲突并用法定财报复核，不直接累加或静默取第一条。
- `free_cashflow` 等衍生字段必须先与 `n_cashflow_act` 和资本开支字段勾稽。无法解释时不要直接引用；如改用“经营现金流－购建长期资产支付现金”的近似口径，需在交付物中写明公式和限制。

### 补充规则

- 端点可能降级：主端点（fast.xiaodefa.cn）三表/指标接口返空时，切换备用端点（tt.xiaodefa.cn）后可用。端点异常先验证端点与字段，再重试或回退，不直接判定数据缺失。

### 补充规则

- 接口查询失败时重试 1-2 次（代理偶发连接错误）；`.env` 行内注释必须独立成行，否则会被旧客户端解析进 URL。

### 补充规则

- tushare 兼容接口 `daily` 可能返回倒序数据，使用时注意排序（如回测场景需反转）。

### 补充规则

- 代理现金流字段（尤其 OCF 总量）可能与法定披露严重不符（实测 269 亿 vs 官方半年报 706.91 亿，量级偏差）：关键现金流数字必须与法定财报交叉核验后才能引用；偏差超合理口径即弃用代理值、以官方披露为准并在交付物标注来源切换。
