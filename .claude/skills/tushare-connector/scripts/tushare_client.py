#!/usr/bin/env python3
"""tushare 兼容 API 薄封装客户端（investment-research-system 数据层，跨项目复用）。

凭证配置自动加载（按优先级）：
  1. 环境变量：TUSHARE_API_URL / TUSHARE_TOKEN（最高优先）
  2. .env 文件：从当前目录向上查找（项目目录 → workspace 根），
     首个含 TUSHARE_* 的 .env 生效。workspace 根 .env 为共享配置，
     所有项目跑 workflow 自动生效，无需逐项目配置。

用法（CLI）：
  python3 tushare_client.py <api_name> '<params_json>' ['fields_csv']

  例：python3 tushare_client.py daily '{"ts_code":"600519.SH","start_date":"20260801","end_date":"20260809"}' 'ts_code,trade_date,close'

用法（库）：
  from tushare_client import query
  df = query("daily", {"ts_code": "600519.SH"}, "ts_code,trade_date,close")

输出：标准 tushare 响应（code==0）时打印/返回 JSON 数据；错误时输出 code/msg 并退出码 1。
"""
import json
import os
import sys
from pathlib import Path

import requests

_ENV_KEYS = ("TUSHARE_API_URL", "TUSHARE_TOKEN")


def _load_dotenv(start_dir: Path) -> dict:
    """从 start_dir 向上查找最近的 .env，解析 TUSHARE_* 键。返回 dict（不含已有环境变量覆盖）。"""
    found = {}
    d = start_dir
    for _ in range(6):  # 最多向上 6 层（项目 → workspace 根 → 停止）
        env_file = d / ".env"
        if env_file.is_file():
            for line in env_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, _, value = line.partition("=")
                key = key.strip()
                if key in _ENV_KEYS:
                    found[key] = value.strip().strip('"').strip("'")
            if found:  # 找到含 TUSHARE_* 的 .env 即停（最近者优先）
                return found
        if (d / ".git").exists() and d.parent == d:  # 到根为止
            break
        parent = d.parent
        if parent == d:
            break
        d = parent
    return found


# 配置解析：环境变量优先，.env 兜底（以 cwd 为起点向上查找）
def _resolve(key: str, default: str = "") -> str:
    val = os.environ.get(key)
    if val:
        return val
    return _load_dotenv(Path.cwd()).get(key, default)


API_URL = _resolve("TUSHARE_API_URL", "https://api.tushare.pro")
TOKEN = _resolve("TUSHARE_TOKEN", "")


def query(api_name: str, params: dict, fields: str = "") -> dict:
    """调用 tushare 兼容接口。返回解析后的 data dict（fields + items）。"""
    if not TOKEN:
        raise SystemExit(
            "错误：未找到 TUSHARE_TOKEN。请在 workspace 根 .env 配置（共享）或设置环境变量:\n"
            "  export TUSHARE_TOKEN=<your_token>\n"
            "（自定义端点同理: export TUSHARE_API_URL=<url> 或 .env 中配置）"
        )
    payload = {"api_name": api_name, "token": TOKEN, "params": params or {}}
    if fields:
        payload["fields"] = fields
    resp = requests.post(API_URL, json=payload, timeout=30)
    resp.raise_for_status()
    body = resp.json()
    if body.get("code") != 0:
        raise SystemExit(f"接口错误 {api_name}: code={body.get('code')} msg={body.get('msg')}")
    return body["data"]


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    api_name = sys.argv[1]
    params = json.loads(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2] else {}
    fields = sys.argv[3] if len(sys.argv) > 3 else ""
    data = query(api_name, params, fields)
    print(json.dumps(data, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
