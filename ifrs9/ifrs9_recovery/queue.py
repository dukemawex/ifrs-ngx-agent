"""Stage 2: build the executable queue from the task files and seeds.

Three job kinds:
  search   - one Nimble search per outstanding bank-year not already covered by a seed lead
  extract  - Nimble extraction of a seeded HTML archive page
  report   - direct streamed download of a public PDF (no Nimble call)
"""
from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict

from . import config as C
from .util import read_csv, read_json, write_csv, write_json

BATCH1_BANKS = {"Wema", "Union"}

# Seed leads that the handoff says can cover specific outstanding years through
# current-year or comparative columns. Coverage is a lead, not an admission.
SEED_YEAR_COVERAGE = {
    "STAN_BANK_2022": [2022, 2021],
    "STAN_BANK_2021": [2021, 2020],
    "STAN_BANK_2018_LINK": [2018],
    "STAN_BANK_2019_LINK": [2019],
    "FIDELITY_BANK_2022": [2022, 2021],
    "WEMA_2022_MIRROR": [2022, 2021],
}

YEAR_RE = re.compile(r"(20[0-2][0-9])")


def _job_id(kind: str, key: str) -> str:
    return f"{kind}-" + hashlib.sha1(f"{kind}|{key}".encode()).hexdigest()[:10]


def split_urls(cell: str | None) -> list[str]:
    return [u.strip() for u in (cell or "").split("|") if u.strip()]


def _is_pdf_url(url: str) -> bool:
    return ".pdf" in url.lower()


def build() -> dict:
    gaps = read_csv(C.TASKS / "bank_year_gaps.csv")
    fgaps = read_csv(C.TASKS / "field_gaps_selected.csv")
    seeds = read_csv(C.SEEDS / "report_sources.csv")
    cohort = {r["bank"]: r for r in read_csv(C.TASKS / "cohort.csv")}
    batches = read_json(C.TASKS / "priority_batches.json", {})

    covered: dict[tuple[str, int], list[str]] = defaultdict(list)
    for s in seeds:
        for y in SEED_YEAR_COVERAGE.get(s["source_id"], []):
            covered[(s["bank"], y)].append(s["source_id"])

    gap_priority = {(g["bank"], int(g["year"])): int(g["priority"]) for g in gaps}
    bank_min_priority: dict[str, int] = {}
    for (b, _), p in gap_priority.items():
        bank_min_priority[b] = min(p, bank_min_priority.get(b, 9))

    jobs: list[dict] = []
    # Report jobs from seeds (deduplicated by URL; source_ids joined).
    by_url: dict[str, dict] = {}
    for s in seeds:
        url = s["url"].strip()
        years = SEED_YEAR_COVERAGE.get(s["source_id"], [])
        pri = min([gap_priority.get((s["bank"], y), 6) for y in years] or [bank_min_priority.get(s["bank"], 6)])
        if s["bank"] in BATCH1_BANKS:
            pri = 1
        job = by_url.setdefault(url, {
            "job_id": _job_id("pdf" if _is_pdf_url(url) else "extract", url),
            "kind": "report" if _is_pdf_url(url) else "extract",
            "priority": pri, "bank": s["bank"], "source_ids": s["source_id"],
            "target_years": ";".join(map(str, years)), "url": url, "origin": "seed",
            "query": "", "nimble_calls_estimate": 0 if _is_pdf_url(url) else 1,
            "notes": s["notes"],
        })
        job["priority"] = min(job["priority"], pri)
        if s["source_id"] not in job["source_ids"]:
            job["source_ids"] += "; " + s["source_id"]
    # Report jobs from field-gap requests that point at an existing source.
    for f in fgaps:
        for url in split_urls(f.get("existing_source_url")):
            pri = 1 if f["bank"] in BATCH1_BANKS else 6
            job = by_url.setdefault(url, {
                "job_id": _job_id("pdf" if _is_pdf_url(url) else "extract", url),
                "kind": "report" if _is_pdf_url(url) else "extract",
                "priority": pri, "bank": f["bank"], "source_ids": "", "target_years": "",
                "url": url, "origin": "field_gap_existing_source", "query": "",
                "nimble_calls_estimate": 0 if _is_pdf_url(url) else 1, "notes": "",
            })
            job["priority"] = min(job["priority"], pri)
            yrs = set(filter(None, job["target_years"].split(";")))
            yrs.add(f["year"])
            job["target_years"] = ";".join(sorted(yrs))
    jobs.extend(by_url.values())

    # Search jobs: one per outstanding bank-year without a seed lead.
    for g in gaps:
        key = (g["bank"], int(g["year"]))
        if covered.get(key):
            continue
        jobs.append({
            "job_id": _job_id("search", f"{g['bank']}|{g['year']}"),
            "kind": "search", "priority": int(g["priority"]), "bank": g["bank"],
            "source_ids": "", "target_years": g["year"], "url": "", "origin": "bank_year_gap",
            "query": g["search_query"], "nimble_calls_estimate": 1,
            "notes": f"{g['current_status']}; {g['priority_reason']}; entity={cohort.get(g['bank'], {}).get('operating_bank_search_name', '')}",
        })

    jobs.sort(key=lambda j: (j["priority"], {"report": 0, "extract": 1, "search": 2}[j["kind"]], j["bank"], j["target_years"]))
    for i, j in enumerate(jobs, 1):
        j["order"] = i
    cols = ["order", "job_id", "kind", "priority", "bank", "target_years", "source_ids", "url",
            "query", "origin", "nimble_calls_estimate", "notes"]
    write_csv(C.DATA / "task_queue.csv", jobs, cols)

    est = sum(int(j["nimble_calls_estimate"]) for j in jobs)
    plan = {
        "jobs": len(jobs),
        "by_kind": {k: sum(j["kind"] == k for j in jobs) for k in ("report", "extract", "search")},
        "estimated_nimble_requests_first_attempt": est,
        "bank_years_with_seed_leads": sorted(f"{b} {y}" for (b, y) in covered if (b, y) in gap_priority),
        "priority_batches": batches.get("batches", []),
    }
    write_json(C.DATA / "queue_plan.json", plan)
    return plan
