#!/usr/bin/env python3
"""Fetch, validate, and select the public Bagholder 50 agent feed."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
import time as time_module
from datetime import date, datetime, time, timedelta, timezone
from itertools import pairwise
from urllib.error import HTTPError, URLError
from urllib.request import HTTPRedirectHandler, Request, build_opener

DEFAULT_URL = "https://indices-toocoldcc.pages.dev/data/agent/bagholder50.json"
TOOL_VERSION = "1.2.1"
OUTPUT_SCHEMA_VERSION = 1
UPSTREAM_SCHEMA_VERSION = 1
USER_AGENT = f"toocoldcc-bagholder50-skill/{TOOL_VERSION}"
BEIJING = timezone(timedelta(hours=8), name="UTC+08:00")
DEFAULT_TIMEOUT = 20.0
MAX_RESPONSE_BYTES = 1024 * 1024
MAX_ATTEMPTS = 2
RETRYABLE_HTTP_STATUS = {408, 425, 429, 500, 502, 503, 504}
VIEWS = ("auto", "all", "holdings_today", "avoid_tomorrow")
TS_CODE_PATTERN = re.compile(r"^\d{6}\.(?:SH|SZ|BJ)$")
SHA256_PATTERN = re.compile(r"^[0-9a-f]{64}$")


class SkillError(RuntimeError):
    """Technical failure with a stable machine-readable code."""

    code = "INTERNAL_ERROR"


class EndpointPolicyError(SkillError):
    code = "ENDPOINT_POLICY_VIOLATION"


class FetchError(SkillError):
    code = "FETCH_FAILED"


class CalendarError(SkillError):
    code = "CALENDAR_INVALID"


class SchemaError(SkillError):
    code = "SCHEMA_MISMATCH"


class SelectionNotReady(RuntimeError):
    """Expected state: the target list has not been published yet."""

    def __init__(
        self,
        message: str,
        *,
        target_trade_date: date,
        selection_basis: str,
        today_is_trading_day: bool,
    ) -> None:
        super().__init__(message)
        self.target_trade_date = target_trade_date
        self.selection_basis = selection_basis
        self.today_is_trading_day = today_is_trading_day


class _RejectRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise EndpointPolicyError("agent endpoint redirects are not allowed")


open_url = build_opener(_RejectRedirects()).open


def fetch(url: str = DEFAULT_URL, timeout: float = DEFAULT_TIMEOUT) -> tuple[bytes, str]:
    """Read the fixed HTTPS agent endpoint with bounded size and one retry."""

    if url != DEFAULT_URL or not url.startswith("https://"):
        raise EndpointPolicyError("URL is not the approved canonical HTTPS agent endpoint")
    request = Request(url, headers={"Accept": "application/json", "User-Agent": USER_AGENT})
    for attempt in range(MAX_ATTEMPTS):
        try:
            with open_url(request, timeout=timeout) as response:
                status = int(getattr(response, "status", 200))
                final_url = str(response.geturl())
                content_type = response.headers.get("Content-Type", "")
                content_length = response.headers.get("Content-Length")
                if final_url != DEFAULT_URL:
                    raise EndpointPolicyError("agent endpoint redirected away from its canonical URL")
                if status != 200:
                    if status in RETRYABLE_HTTP_STATUS and attempt + 1 < MAX_ATTEMPTS:
                        time_module.sleep(0.25)
                        continue
                    raise FetchError(f"agent endpoint returned HTTP {status}")
                if content_length:
                    try:
                        advertised_size = int(content_length)
                    except ValueError as exc:
                        raise FetchError("agent endpoint returned an invalid Content-Length") from exc
                    if advertised_size > MAX_RESPONSE_BYTES:
                        raise FetchError("agent response exceeds the one-megabyte limit")
                body = response.read(MAX_RESPONSE_BYTES + 1)
        except EndpointPolicyError:
            raise
        except HTTPError as exc:
            if exc.code in RETRYABLE_HTTP_STATUS and attempt + 1 < MAX_ATTEMPTS:
                time_module.sleep(0.25)
                continue
            raise FetchError(f"agent feed fetch failed with HTTP {exc.code}") from exc
        except (URLError, TimeoutError, OSError) as exc:
            if attempt + 1 < MAX_ATTEMPTS:
                time_module.sleep(0.25)
                continue
            raise FetchError(f"agent feed fetch failed: {exc}") from exc

        if len(body) > MAX_RESPONSE_BYTES:
            raise FetchError("agent response exceeds the one-megabyte limit")
        if not body or body.lstrip().startswith(b"<"):
            raise FetchError("agent endpoint returned HTML or an empty body, not JSON")
        if "json" not in content_type.lower():
            raise FetchError(
                f"agent endpoint is not advertised as JSON: {content_type or '<missing>'}"
            )
        return body, content_type
    raise FetchError(f"agent feed fetch failed after {MAX_ATTEMPTS} attempts")


def _finite_number(value: object, label: str) -> float:
    if isinstance(value, bool):
        raise SchemaError(f"{label} is not a finite number")
    try:
        normalized = float(value)
    except (TypeError, ValueError) as exc:
        raise SchemaError(f"{label} is not a finite number") from exc
    if not math.isfinite(normalized):
        raise SchemaError(f"{label} is not a finite number")
    return normalized


def _parse_date(value: object, label: str) -> date:
    try:
        return date.fromisoformat(str(value))
    except ValueError as exc:
        raise SchemaError(f"{label} is not a valid YYYY-MM-DD date") from exc


def _validate_rows(rows: object, expected: int, label: str) -> list[dict]:
    if not isinstance(rows, list):
        raise SchemaError(f"{label} is not a JSON list")
    if len(rows) != expected:
        raise SchemaError(f"{label} has {len(rows)} rows; expected {expected}")
    normalized: list[dict] = []
    codes: set[str] = set()
    ranks: list[int] = []
    scores: list[float] = []
    for row in rows:
        if not isinstance(row, dict):
            raise SchemaError(f"{label} contains a non-object row")
        code = str(row.get("ts_code", "")).strip()
        if not TS_CODE_PATTERN.fullmatch(code):
            raise SchemaError(f"{label} contains an invalid ts_code: {code!r}")
        if code in codes:
            raise SchemaError(f"{label} contains a duplicate ts_code: {code!r}")
        name = row.get("name")
        if not isinstance(name, str) or not name.strip():
            raise SchemaError(f"{label} contains an invalid name for {code}")
        rank = row.get("bagholder_rank")
        if isinstance(rank, bool) or not isinstance(rank, int):
            raise SchemaError(f"{label} contains an invalid rank for {code}")
        score = _finite_number(row.get("bagholder_score"), f"{label} score for {code}")
        if not 0.0 <= score <= 1.0:
            raise SchemaError(f"{label} score is outside [0, 1] for {code}")
        today_return = _finite_number(row.get("today_return"), f"{label} today_return for {code}")
        codes.add(code)
        ranks.append(rank)
        scores.append(score)
        normalized.append(
            {
                "ts_code": code,
                "name": name.strip(),
                "today_return": today_return,
                "bagholder_rank": rank,
                "bagholder_score": score,
            }
        )
    if ranks != list(range(1, expected + 1)):
        raise SchemaError(f"{label} ranks are not consecutive 1..{expected}")
    if any(left < right for left, right in pairwise(scores)):
        raise SchemaError(f"{label} scores are not descending with published rank")
    return normalized


def _validate_summary(value: object, data_end: date) -> dict:
    if not isinstance(value, dict):
        raise SchemaError("index.summary is missing")
    latest_date = _parse_date(value.get("latest_date"), "index.summary.latest_date")
    if latest_date != data_end:
        raise SchemaError("index summary latest_date does not match data_end_date")
    latest_point = _finite_number(value.get("latest_point"), "index.summary.latest_point")
    if latest_point <= 0:
        raise SchemaError("index.summary.latest_point is not positive")
    annualized_return = _finite_number(
        value.get("annualized_return"),
        "index.summary.annualized_return",
    )
    recent = value.get("recent_returns")
    if not isinstance(recent, dict):
        raise SchemaError("index.summary.recent_returns is missing")
    normalized_recent = {}
    for key in ("1d", "5d", "20d"):
        window = recent.get(key)
        if not isinstance(window, dict):
            raise SchemaError(f"index.summary.recent_returns.{key} is missing")
        start = _parse_date(window.get("start_date"), f"{key}.start_date")
        end = _parse_date(window.get("end_date"), f"{key}.end_date")
        if not start < end == data_end:
            raise SchemaError(f"index.summary.recent_returns.{key} has inconsistent dates")
        normalized_recent[key] = {
            "return": _finite_number(window.get("return"), f"{key}.return"),
            "start_date": start.isoformat(),
            "end_date": end.isoformat(),
        }
    return {
        "latest_date": latest_date.isoformat(),
        "latest_point": latest_point,
        "annualized_return": annualized_return,
        "recent_returns": normalized_recent,
    }


def _validate_calendar(value: object, data_end: date) -> tuple[dict, list[date]]:
    if not isinstance(value, dict) or value.get("source") != "tushare.trade_cal":
        raise CalendarError("agent feed has no approved trading-calendar contract")
    coverage_start = _parse_date(value.get("coverage_start"), "calendar.coverage_start")
    coverage_end = _parse_date(value.get("coverage_end"), "calendar.coverage_end")
    if not coverage_start <= data_end < coverage_end:
        raise CalendarError("trading-calendar coverage does not contain data_end and future dates")
    raw_dates = value.get("open_dates")
    if not isinstance(raw_dates, list) or not raw_dates:
        raise CalendarError("calendar.open_dates is not a non-empty list")
    dates = [_parse_date(item, "calendar.open_dates item") for item in raw_dates]
    if dates != sorted(set(dates)):
        raise CalendarError("calendar.open_dates is not sorted and unique")
    if dates[0] < coverage_start or dates[-1] > coverage_end:
        raise CalendarError("calendar.open_dates falls outside its declared coverage")
    contract = {
        "source": "tushare.trade_cal",
        "coverage_start": coverage_start.isoformat(),
        "coverage_end": coverage_end.isoformat(),
        "open_dates": [item.isoformat() for item in dates],
    }
    canonical = json.dumps(contract, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    expected_hash = hashlib.sha256(canonical).hexdigest()
    if value.get("sha256") != expected_hash:
        raise CalendarError("calendar.sha256 does not match the published calendar contract")
    return {**contract, "sha256": expected_hash}, dates


def _validate_view(value: object, expected: int, label: str) -> dict:
    if not isinstance(value, dict):
        raise SchemaError(f"views.{label} is missing")
    status = str(value.get("status", ""))
    if status not in {"ready", "pending"}:
        raise SchemaError(f"views.{label}.status is invalid")
    signal_date = _parse_date(value.get("signal_date"), f"views.{label}.signal_date")
    trade_date = _parse_date(value.get("trade_date"), f"views.{label}.trade_date")
    if trade_date <= signal_date:
        raise SchemaError(f"views.{label}.trade_date is not after its signal date")
    raw_items = value.get("items")
    if status == "pending":
        if raw_items != []:
            raise SchemaError(f"views.{label}.items must be empty when pending")
        items: list[dict] = []
    else:
        items = _validate_rows(raw_items, expected, f"views.{label}.items")
    return {
        "status": status,
        "signal_date": signal_date.isoformat(),
        "trade_date": trade_date.isoformat(),
        "items": items,
    }


def _parse_now(value: str | None) -> datetime:
    if not value:
        return datetime.now(BEIJING)
    normalized = value.strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError as exc:
        raise SkillError("test clock must be an ISO datetime") from exc
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=BEIJING)
    return parsed.astimezone(BEIJING)


def _select(
    views: dict,
    now: datetime,
    calendar: dict,
    calendar_dates: list[date],
) -> tuple[str, dict, str, date, bool]:
    today = now.date()
    coverage_start = _parse_date(calendar["coverage_start"], "calendar.coverage_start")
    coverage_end = _parse_date(calendar["coverage_end"], "calendar.coverage_end")
    if not coverage_start <= today <= coverage_end:
        raise CalendarError(f"trading calendar does not cover {today.isoformat()}")
    today_is_trading_day = today in set(calendar_dates)
    before_close = today_is_trading_day and now.time() < time(15, 0)
    if before_close:
        target = today
        basis = "today_before_close"
    else:
        target = next((item for item in calendar_dates if item > today), None)
        if target is None:
            raise CalendarError(f"trading calendar has no open date after {today.isoformat()}")
        basis = "next_trading_day"

    holdings = views["holdings_today"]
    avoidance = views["avoid_tomorrow"]
    if before_close and avoidance["status"] == "ready" and avoidance["trade_date"] == target.isoformat():
        return "avoid_tomorrow", avoidance, basis, target, True
    if before_close and holdings["status"] == "ready" and holdings["trade_date"] == target.isoformat():
        return "holdings_today", holdings, basis, target, True
    if not before_close and avoidance["status"] == "ready" and avoidance["trade_date"] == target.isoformat():
        return "avoid_tomorrow", avoidance, basis, target, today_is_trading_day
    raise SelectionNotReady(
        f"最新成分股尚未更新；预计每个交易日 20:00（北京时间）更新。目标交易日：{target.isoformat()}。",
        target_trade_date=target,
        selection_basis=basis,
        today_is_trading_day=today_is_trading_day,
    )


def normalize(
    payload: object,
    url: str,
    body: bytes,
    view: str,
    *,
    now: datetime | None = None,
    verbose: bool = False,
) -> dict:
    if not isinstance(payload, dict):
        raise SchemaError("agent feed response is not a JSON object")
    if payload.get("schema_version") != UPSTREAM_SCHEMA_VERSION:
        raise SchemaError(f"unsupported agent feed schema_version: {payload.get('schema_version')!r}")
    if payload.get("data_product") != "bagholder50_agent_feed" or payload.get("canonical_url") != DEFAULT_URL:
        raise SchemaError("unexpected agent feed identity or canonical URL")
    try:
        generated_at = datetime.fromisoformat(str(payload.get("generated_at_utc", "")).replace("Z", "+00:00"))
    except ValueError as exc:
        raise SchemaError("generated_at_utc is not an ISO datetime") from exc
    if generated_at.tzinfo is None:
        raise SchemaError("generated_at_utc has no timezone")

    index = payload.get("index")
    if not isinstance(index, dict):
        raise SchemaError("agent feed has no index object")
    if index.get("internal_code") != "bagholder50_index" or index.get("index_name_en") != "Bagholder 50":
        raise SchemaError("unexpected Bagholder 50 identity")
    try:
        expected = int(index["constituent_count"])
    except (KeyError, TypeError, ValueError) as exc:
        raise SchemaError("index.constituent_count is invalid") from exc
    if expected != 50:
        raise SchemaError(f"unexpected constituent_count: {expected}")
    data_end = _parse_date(index.get("data_end_date"), "index.data_end_date")
    summary = _validate_summary(index.get("summary"), data_end)

    policy = payload.get("selection_policy")
    if (
        not isinstance(policy, dict)
        or policy.get("timezone") != "UTC+08:00"
        or policy.get("market_close") != "15:00:00"
    ):
        raise SchemaError("unsupported selection policy")
    calendar, calendar_dates = _validate_calendar(policy.get("calendar"), data_end)
    raw_views = payload.get("views")
    if not isinstance(raw_views, dict):
        raise SchemaError("agent feed has no views object")
    views = {
        "holdings_today": _validate_view(raw_views.get("holdings_today"), expected, "holdings_today"),
        "avoid_tomorrow": _validate_view(raw_views.get("avoid_tomorrow"), expected, "avoid_tomorrow"),
    }
    if views["holdings_today"]["status"] != "ready":
        raise SchemaError("views.holdings_today must be ready")
    for name, item in views.items():
        if _parse_date(item["signal_date"], f"views.{name}.signal_date") > data_end:
            raise SchemaError(f"views.{name}.signal_date is after index.data_end_date")

    provenance = payload.get("provenance")
    if not isinstance(provenance, dict):
        raise SchemaError("agent feed has no provenance object")
    for name in ("bagholder50", "calendar"):
        value = provenance.get(name)
        if not isinstance(value, dict) or not SHA256_PATTERN.fullmatch(str(value.get("sha256", ""))):
            raise SchemaError(f"provenance.{name}.sha256 is invalid")
    if provenance["calendar"]["sha256"] != calendar["sha256"]:
        raise SchemaError("provenance calendar hash does not match selection policy")

    local_now = now or datetime.now(BEIJING)
    local_now = local_now.replace(tzinfo=BEIJING) if local_now.tzinfo is None else local_now.astimezone(BEIJING)
    selected: list[dict]
    if view == "auto":
        try:
            source_view, chosen, basis, target, today_is_trading_day = _select(
                views,
                local_now,
                calendar,
                calendar_dates,
            )
        except SelectionNotReady as exc:
            selected = []
            selection = {
                "status": "not_ready",
                "source_view": None,
                "selection_basis": exc.selection_basis,
                "now_beijing": local_now.isoformat(),
                "today_is_trading_day": exc.today_is_trading_day,
                "target_trade_date": exc.target_trade_date.isoformat(),
                "signal_date": None,
                "trade_date": None,
                "message": str(exc),
            }
        else:
            selected = chosen["items"]
            selection = {
                "status": "ready",
                "source_view": source_view,
                "selection_basis": basis,
                "now_beijing": local_now.isoformat(),
                "today_is_trading_day": today_is_trading_day,
                "target_trade_date": target.isoformat(),
                "signal_date": chosen["signal_date"],
                "trade_date": chosen["trade_date"],
            }
    elif view in views:
        chosen = views[view]
        selected = chosen["items"]
        selection = {
            "status": "ready" if chosen["status"] == "ready" else "not_ready",
            "source_view": view if chosen["status"] == "ready" else None,
            "selection_basis": "explicit_view",
            "now_beijing": local_now.isoformat(),
            "target_trade_date": chosen["trade_date"],
            "signal_date": chosen["signal_date"] if selected else None,
            "trade_date": chosen["trade_date"] if selected else None,
        }
        if not selected:
            selection["message"] = f"该日期视图尚未生成。目标交易日：{chosen['trade_date']}。"
    else:
        selected = []
        selection = None

    result = {
        "schema_version": OUTPUT_SCHEMA_VERSION,
        "tool_version": TOOL_VERSION,
        "source": {
            "url": url,
            "sha256": hashlib.sha256(body).hexdigest(),
            "hash_scope": "fetched_agent_feed_response_body",
            "fetched_at_utc": datetime.now(timezone.utc).isoformat(),  # noqa: UP017
            "published_at_utc": generated_at.astimezone(timezone.utc).isoformat(),  # noqa: UP017
        },
        "index_summary": summary,
        "view": view,
        "selection": selection,
        "items": selected,
    }
    if verbose or view == "all":
        result["feed_metadata"] = {
            "index": {key: value for key, value in index.items() if key != "summary"},
            "selection_policy": {**policy, "calendar": {**calendar, "open_dates": None}},
            "provenance": provenance,
        }
    if view == "all":
        result["views"] = views
    return result


def _error_payload(exc: Exception) -> dict:
    code = exc.code if isinstance(exc, SkillError) else "INVALID_JSON"
    return {
        "schema_version": OUTPUT_SCHEMA_VERSION,
        "tool_version": TOOL_VERSION,
        "status": "error",
        "error": {"code": code, "message": str(exc)},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--view", choices=VIEWS, default="auto")
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="include feed metadata; --view all also includes both source lists",
    )
    args = parser.parse_args()
    try:
        body, _ = fetch()
        payload = json.loads(body.decode("utf-8"))
        result = normalize(payload, DEFAULT_URL, body, args.view, verbose=args.verbose)
    except (UnicodeDecodeError, json.JSONDecodeError, SkillError) as exc:
        print(json.dumps(_error_payload(exc), ensure_ascii=False), file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
