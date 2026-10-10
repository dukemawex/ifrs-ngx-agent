"""Stage 4: stream-download original public PDFs with identity checks; checkpoint per report.

A report is accepted only if the final response is HTTP 200 from a public https
host, the bytes start with %PDF-, and the size is within MAX_PDF_MB. HTML error
pages saved as .pdf are rejected.
"""
from __future__ import annotations

import hashlib
import ipaddress
import os
import tempfile
from urllib.parse import urljoin, urlparse

import requests

from . import config as C
from .util import bank_slug, read_csv, read_json, utcnow, write_csv, write_json

STATE_FILE = C.STATE / "download_state.json"
BLOCKED_HOST_SUFFIXES = (".local", ".internal", ".localhost", "metadata.google.internal")
MAX_REDIRECTS = 5
UA = "Mozilla/5.0 (research data verification; contact via repository owner)"


def url_is_public_https(url: str) -> tuple[bool, str]:
    p = urlparse(url)
    if p.scheme != "https":
        return False, f"scheme {p.scheme!r} not allowed (https only)"
    host = (p.hostname or "").lower()
    if not host or "." not in host:
        return False, "missing or single-label host"
    if host == "localhost" or host.endswith(BLOCKED_HOST_SUFFIXES):
        return False, "local/internal host"
    try:
        ip = ipaddress.ip_address(host)
        if not ip.is_global:
            return False, "non-public IP literal"
    except ValueError:
        pass
    if p.username or p.password:
        return False, "credentials in URL"
    return True, ""


def fetch_pdf(url: str, dest_dir, max_mb: int, session: requests.Session | None = None,
              stem: str = "report") -> dict:
    s = session or requests.Session()
    rec = {"requested_url": url, "final_url": "", "http_status": "", "content_type": "",
           "bytes": 0, "sha256": "", "local_pdf_path": "", "status": "", "reason": "", "accessed_utc": utcnow()}
    current = url
    for _ in range(MAX_REDIRECTS + 1):
        ok, why = url_is_public_https(current)
        if not ok:
            rec.update(status="rejected", reason=f"unsafe url: {why}", final_url=current)
            return rec
        try:
            r = s.get(current, stream=True, timeout=(20, 120), allow_redirects=False, headers={"User-Agent": UA})
        except requests.exceptions.ProxyError as e:
            rec.update(status="egress_denied", reason=f"proxy refused {urlparse(current).hostname}: {str(e)[:120]}", final_url=current)
            return rec
        except requests.exceptions.RequestException as e:
            rec.update(status="network_error", reason=f"{type(e).__name__}: {str(e)[:160]}", final_url=current)
            return rec
        if r.status_code in (301, 302, 303, 307, 308) and r.headers.get("Location"):
            current = urljoin(current, r.headers["Location"])
            r.close()
            continue
        break
    else:
        rec.update(status="rejected", reason="too many redirects", final_url=current)
        return rec
    rec.update(final_url=current, http_status=r.status_code, content_type=r.headers.get("Content-Type", ""))
    if r.status_code != 200:
        rec.update(status="http_error", reason=f"HTTP {r.status_code}")
        r.close()
        return rec
    limit = max_mb * 1024 * 1024
    declared = r.headers.get("Content-Length")
    if declared and declared.isdigit() and int(declared) > limit:
        rec.update(status="too_large", reason=f"Content-Length {declared} > {max_mb} MB")
        r.close()
        return rec
    dest_dir.mkdir(parents=True, exist_ok=True)
    h = hashlib.sha256()
    n = 0
    head = b""
    fd, tmp = tempfile.mkstemp(dir=dest_dir, suffix=".part")
    try:
        with os.fdopen(fd, "wb") as f:
            for chunk in r.iter_content(1 << 16):
                if not chunk:
                    continue
                if len(head) < 8:
                    head += chunk[: 8 - len(head)]
                n += len(chunk)
                if n > limit:
                    raise OverflowError
                h.update(chunk)
                f.write(chunk)
    except OverflowError:
        os.unlink(tmp)
        rec.update(status="too_large", reason=f"stream exceeded {max_mb} MB")
        return rec
    except requests.exceptions.RequestException as e:
        os.unlink(tmp)
        rec.update(status="network_error", reason=f"interrupted: {type(e).__name__}")
        return rec
    if not head.startswith(b"%PDF-"):
        os.unlink(tmp)
        rec.update(status="not_pdf", reason=f"signature {head[:8]!r}; content-type {rec['content_type']}", bytes=n)
        return rec
    digest = h.hexdigest()
    final = dest_dir / f"{stem}_{digest[:12]}.pdf"
    os.replace(tmp, final)
    rec.update(status="downloaded", bytes=n, sha256=digest, local_pdf_path=str(final.relative_to(C.ROOT)) if C.ROOT in final.parents else str(final))
    return rec


def run(resume: bool = True, settings: C.Settings | None = None, max_priority: int | None = None, session: requests.Session | None = None) -> dict:
    settings = settings or C.load_settings()
    jobs = [j for j in read_csv(C.DATA / "task_queue.csv") if j["kind"] == "report"]
    if max_priority is not None:
        jobs = [j for j in jobs if int(j["priority"]) <= max_priority]
    # Discovered PDF leads join the queue after seeded reports.
    leads_path = C.DATA / "discovery_leads.csv"
    if leads_path.is_file():
        for l in read_csv(leads_path):
            if ".pdf" in l["url"].lower():
                jobs.append({"job_id": "lead-" + hashlib.sha1(l["url"].encode()).hexdigest()[:10], "kind": "report",
                             "priority": "7", "bank": l["bank"], "target_years": l["target_years"],
                             "source_ids": "", "url": l["url"], "origin": "nimble_lead"})
    # Leads found by the reviewer's fallback discovery (web search) while Nimble is unavailable.
    extra = C.DATA / "review" / "extra_sources.csv"
    if extra.is_file():
        for l in read_csv(extra):
            if max_priority is not None and int(l["priority"]) > max_priority:
                continue
            jobs.append({"job_id": "xs-" + hashlib.sha1(l["url"].encode()).hexdigest()[:10], "kind": "report",
                         "priority": l["priority"], "bank": l["bank"], "target_years": l["target_years"],
                         "source_ids": l["source_id"], "url": l["url"], "origin": f"fallback:{l['discovery_method']}"})
    state = read_json(STATE_FILE, {}) if resume else {}
    state.setdefault("reports", {})
    for j in jobs:
        prev = state["reports"].get(j["job_id"])
        if prev and prev.get("status") == "downloaded" and (C.ROOT / prev["local_pdf_path"]).is_file():
            continue
        rec = fetch_pdf(j["url"], C.REPORTS / bank_slug(j["bank"]), settings.max_pdf_mb, session,
                        stem=f"{bank_slug(j['bank'])}_{j['job_id']}")
        rec.update({k: j.get(k, "") for k in ("job_id", "bank", "priority", "target_years", "source_ids", "origin")})
        state["reports"][j["job_id"]] = rec
        write_json(STATE_FILE, state)  # checkpoint after each report
    rows = list(state["reports"].values())
    write_csv(C.DATA / "download_log.csv", rows,
              ["job_id", "bank", "priority", "target_years", "source_ids", "origin", "requested_url", "final_url",
               "http_status", "content_type", "bytes", "sha256", "local_pdf_path", "status", "reason", "accessed_utc"])
    statuses = [r["status"] for r in rows]
    return {"reports": len(rows), "status_counts": {s: statuses.count(s) for s in sorted(set(statuses))}}
