"""Record a report fetched outside the requests-based downloader (plain curl request, no special headers).

Used only when a public issuer URL answers the pipeline's descriptive User-Agent with HTTP 403 but serves the same
public file to an ordinary request. Same checks as download.fetch_pdf: public https URL, %PDF- signature, size cap,
SHA-256, file stored as reports/<bank>/<bank>_<job>_<hash12>.pdf, and the download state/log updated for that job.

    python -m ifrs9_recovery.manual_fetch <source_id>
"""
from __future__ import annotations

import hashlib
import os
import subprocess
import sys
import tempfile

from . import config as C
from .download import STATE_FILE, url_is_public_https
from .util import bank_slug, read_csv, read_json, utcnow, write_csv, write_json


def fetch(source_id: str) -> dict:
    src = next(r for r in read_csv(C.DATA / "review" / "extra_sources.csv") if r["source_id"] == source_id)
    url = src["url"]
    ok, why = url_is_public_https(url)
    if not ok:
        raise SystemExit(f"unsafe url: {why}")
    job = "xs-" + hashlib.sha1(url.encode()).hexdigest()[:10]
    dest = C.REPORTS / bank_slug(src["bank"])
    dest.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=dest, suffix=".part")
    os.close(fd)
    settings = C.load_settings()
    res = subprocess.run(["curl", "-sS", "-L", "--proto", "=https", "--max-redirs", "5", "--max-time", "300",
                          "--max-filesize", str(settings.max_pdf_mb * 1024 * 1024), "-o", tmp,
                          "-w", "%{http_code} %{url_effective} %{content_type}", url], capture_output=True, text=True)
    code, final, ctype = (res.stdout.split(" ") + ["", "", ""])[:3]
    data = open(tmp, "rb").read()
    rec = {"job_id": job, "bank": src["bank"], "priority": src["priority"], "target_years": src["target_years"],
           "source_ids": source_id, "origin": f"fallback:{src['discovery_method']}; manual curl fetch (pipeline UA got HTTP 403)",
           "requested_url": url, "final_url": final, "http_status": code, "content_type": ctype, "bytes": len(data),
           "sha256": "", "local_pdf_path": "", "status": "", "reason": "", "accessed_utc": utcnow()}
    if code != "200" or not data.startswith(b"%PDF-"):
        os.unlink(tmp)
        rec.update(status="http_error" if code != "200" else "not_pdf", reason=f"HTTP {code}; {res.stderr[:120]}")
    else:
        digest = hashlib.sha256(data).hexdigest()
        final_path = dest / f"{bank_slug(src['bank'])}_{job}_{digest[:12]}.pdf"
        os.replace(tmp, final_path)
        rec.update(status="downloaded", sha256=digest, local_pdf_path=str(final_path.relative_to(C.ROOT)))
    state = read_json(STATE_FILE, {"reports": {}})
    state["reports"][job] = rec
    write_json(STATE_FILE, state)
    rows = list(state["reports"].values())
    write_csv(C.DATA / "download_log.csv", rows,
              ["job_id", "bank", "priority", "target_years", "source_ids", "origin", "requested_url", "final_url",
               "http_status", "content_type", "bytes", "sha256", "local_pdf_path", "status", "reason", "accessed_utc"])
    return rec


if __name__ == "__main__":
    r = fetch(sys.argv[1])
    print({k: r[k] for k in ("job_id", "status", "bytes", "sha256", "local_pdf_path", "reason")})
