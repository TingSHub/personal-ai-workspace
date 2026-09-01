---
name: tushare-connector
description: tushare 兼容 API 数据连接器（workspace 共享 internal skill）——凭证/端点自动从 workspace 根 .env 加载（TUSHARE_TOKEN/TUSHARE_API_URL），支持任意兼容端点。当任何项目需要获取 A股/港股/美股行情、财务三表、历史数据、行业基准时使用。
---

# tushare-connector

workspace 级共享数据连接器：封装 tushare 兼容 HTTP API（纯 requests，不依赖 tushare SDK 的硬编码端点）。

## 为什么存在

- 第三方 skill（tushare-data）的 SDK 端点硬编码为 api.tushare.pro，且依赖环境变量手动配置
- 本连接器：**端点/密钥自动加载**（workspace 根 `.env`，向上查找），任何项目零配置即可用
- 跨项目复用：所有项目通过本 skill 取数，一处维护

## 凭证配置（workspace 根 .env，gitignored）

```
TUSHARE_TOKEN=xxx
TUSHARE_API_URL=https://tt.xiaodefa.cn    # 备用端点（fast.xiaodefa.cn 主端点 2026-08-11 起降级，三表/指标接口返空；tt 端点可用）
# 注意：代理偶发连接错误，查询失败重试 1-2 次；官方端点需官方 token（当前 token 仅代理有效）
```

优先级：环境变量 > .env（从 cwd 向上查找最近含 TUSHARE_* 的文件）。

## 用法

CLI：
```bash
python3 <skill_dir>/scripts/tushare_client.py <api_name> '<params_json>' ['fields_csv']
# 例：python3 .../tushare_client.py daily '{"ts_code":"600519.SH","start_date":"20260801","end_date":"20260809"}' 'ts_code,trade_date,close'
```

库：
```python
import sys; sys.path.insert(0, "<skill_dir>/scripts")
from tushare_client import query
data = query("daily", {"ts_code": "600519.SH"}, "ts_code,trade_date,close")
# data = {"fields": [...], "items": [...]}
```

## 注意

- 响应已解包为 data 部分（fields/items），无 code/data 包装
- income 接口的 `n_income` 为合并净利，归母用 `n_income_attr_p`
- 常用接口：stock_basic / daily / income / balancesheet / cashflow / fina_indicator / trade_cal

## Validation（操作后必须执行）

- 输出含 `"items"` 键且非空
- `grep -q "TUSHARE_TOKEN" <workspace>/<.env>` 或在错误提示中确认指引给出
