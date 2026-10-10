"""Bounded Nimble client: persistent request budget, cache, retries, key redaction.

Endpoints follow the handoff's documented contract (POST {base}/search and
{base}/extract with a Bearer key). Request bodies use only parameters named in
that contract; anything else must be confirmed in the current docs first.
"""
from __future__ import annotations

import hashlib
import json
import threading
import time
from dataclasses import dataclass
from typing import Any, Callable

import requests

from . import config as C
from .util import append_log, read_json, utcnow, write_json

BUDGET_FILE = C.STATE / "nimble_budget.json"
LOG_FILE = C.LOGS / "nimble_requests.jsonl"
RETRYABLE = {429, 500, 502, 503, 504}


class BudgetExhausted(RuntimeError):
    pass


class AuthFailure(RuntimeError):
    pass


class EgressDenied(RuntimeError):
    pass


@dataclass
class Budget:
    cap: int
    path: Any = BUDGET_FILE

    def __post_init__(self) -> None:
        self._lock = threading.Lock()
        data = read_json(self.path, {}) or {}
        self.attempted = int(data.get("attempted_requests", 0))
        # A stricter cap persisted from an earlier run always wins.
        self.cap = min(self.cap, int(data.get("cap", self.cap)))

    @property
    def remaining(self) -> int:
        return max(0, self.cap - self.attempted)

    def take(self) -> None:
        with self._lock:
            if self.attempted >= self.cap:
                raise BudgetExhausted(f"Nimble request cap reached ({self.cap})")
            self.attempted += 1
            write_json(self.path, {"cap": self.cap, "attempted_requests": self.attempted,
                                   "remaining": self.remaining, "updated_utc": utcnow()})


def preflight(base: str = C.NIMBLE_BASE, session: requests.Session | None = None) -> dict:
    """Check that the API host is reachable without sending the key (no paid call)."""
    s = session or requests.Session()
    host = base.split("/")[2]
    try:
        r = s.head(f"https://{host}/", timeout=15, allow_redirects=False)
        return {"host": host, "reachable": True, "status": r.status_code}
    except requests.exceptions.ProxyError as e:
        return {"host": host, "reachable": False, "reason": "egress_denied_by_proxy", "detail": str(e)[:200]}
    except requests.exceptions.RequestException as e:
        return {"host": host, "reachable": False, "reason": type(e).__name__, "detail": str(e)[:200]}


class NimbleClient:
    def __init__(self, settings: C.Settings, budget: Budget | None = None,
                 session: requests.Session | None = None, sleep: Callable[[float], None] = time.sleep,
                 cache_dir=None, base: str = C.NIMBLE_BASE) -> None:
        self.settings = settings
        self.budget = budget or Budget(settings.max_requests)
        self.session = session or requests.Session()
        self.sleep = sleep
        self.cache_dir = cache_dir or (C.CACHE / "nimble")
        self.base = base
        self._secrets = [settings.auth_header()["Authorization"].split(" ", 1)[1]] if settings.has_key else []

    def _cache_path(self, endpoint: str, body: dict):
        key = hashlib.sha256(json.dumps([endpoint, body], sort_keys=True).encode()).hexdigest()
        return self.cache_dir / f"{endpoint}_{key[:24]}.json"

    def _post(self, endpoint: str, body: dict) -> dict:
        cpath = self._cache_path(endpoint, body)
        cached = read_json(cpath)
        if cached is not None:
            return {"cached": True, **cached}
        if self.settings.dry_run:
            append_log(LOG_FILE, {"endpoint": endpoint, "body": body, "dry_run": True})
            return {"cached": False, "dry_run": True, "response": None}
        if not self.settings.has_key:
            raise AuthFailure("NIMBLE_API_KEY is not configured")
        url = f"{self.base}/{endpoint}"
        headers = {**self.settings.auth_header(), "Content-Type": "application/json"}
        delay = 2.0
        for attempt in range(self.settings.max_retries + 1):
            self.budget.take()  # every attempt, including retries, counts
            try:
                r = self.session.post(url, json=body, headers=headers, timeout=self.settings.timeout_s)
            except requests.exceptions.ProxyError as e:
                append_log(LOG_FILE, {"endpoint": endpoint, "attempt": attempt, "error": "egress_denied"}, self._secrets)
                raise EgressDenied(str(e)[:200]) from None
            except requests.exceptions.RequestException as e:
                append_log(LOG_FILE, {"endpoint": endpoint, "attempt": attempt, "error": type(e).__name__}, self._secrets)
                if attempt == self.settings.max_retries:
                    raise
                self.sleep(delay); delay = min(delay * 2, 60); continue
            append_log(LOG_FILE, {"endpoint": endpoint, "body": body, "attempt": attempt, "status": r.status_code}, self._secrets)
            if r.status_code in (401, 403):
                raise AuthFailure(f"Nimble returned {r.status_code}; not retrying")
            if r.status_code in RETRYABLE and attempt < self.settings.max_retries:
                ra = r.headers.get("Retry-After")
                try:
                    wait = min(float(ra), 120.0) if ra is not None else delay
                except ValueError:
                    wait = delay
                self.sleep(wait); delay = min(delay * 2, 60); continue
            r.raise_for_status()
            payload = {"request": {"endpoint": endpoint, "body": body}, "fetched_utc": utcnow(), "response": r.json()}
            write_json(cpath, payload)
            return {"cached": False, **payload}
        raise RuntimeError("unreachable")

    def search(self, query: str, max_results: int = 10, include_domains: list[str] | None = None,
               exclude_domains: list[str] | None = None) -> dict:
        body: dict[str, Any] = {"query": query, "max_results": max_results,
                                "search_depth": self.settings.search_depth}
        if include_domains:
            body["include_domains"] = include_domains
        if exclude_domains:
            body["exclude_domains"] = exclude_domains
        return self._post("search", body)

    def extract(self, url: str) -> dict:
        if not url.startswith("https://"):
            raise ValueError("Only public https URLs may be extracted")
        return self._post("extract", {"url": url, "formats": ["html", "markdown"]})


def result_urls(response: dict | None) -> list[dict]:
    """Pull (url, title, snippet) from a search response without assuming one exact schema."""
    if not response:
        return []
    items = None
    for key in ("results", "data", "organic", "items"):
        if isinstance(response.get(key), list):
            items = response[key]
            break
    out = []
    for it in items or []:
        if isinstance(it, dict) and it.get("url"):
            out.append({"url": it["url"], "title": it.get("title", ""),
                        "snippet": (it.get("content") or it.get("snippet") or it.get("description") or "")[:500]})
    return out
