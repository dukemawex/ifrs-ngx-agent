"""Stage 3: Nimble discovery for queued search/extract jobs, resumable and budgeted.

Discovered URLs are leads only. They enter the report queue for direct download;
nothing found here is ever treated as a verified value.
"""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

from . import config as C
from .nimble import AuthFailure, BudgetExhausted, EgressDenied, NimbleClient, preflight, result_urls
from .util import read_csv, read_json, utcnow, write_csv, write_json

STATE_FILE = C.STATE / "discover_state.json"


def run(resume: bool = True, settings: C.Settings | None = None, max_priority: int | None = None, client: NimbleClient | None = None,
        preflight_fn=preflight) -> dict:
    settings = settings or C.load_settings()
    jobs = [j for j in read_csv(C.DATA / "task_queue.csv") if j["kind"] in ("search", "extract")]
    if max_priority is not None:
        jobs = [j for j in jobs if int(j["priority"]) <= max_priority]
    state = read_json(STATE_FILE, {}) if resume else {}
    state.setdefault("jobs", {})
    pending = [j for j in jobs if state["jobs"].get(j["job_id"], {}).get("status") not in ("done",)]
    est = sum(int(j["nimble_calls_estimate"]) for j in pending)
    state["last_run"] = {"started_utc": utcnow(), "pending_jobs": len(pending),
                         "estimated_requests_this_batch": est, "cap": settings.max_requests}

    blocker = None
    if not settings.has_key and not settings.dry_run:
        blocker = "auth_missing: NIMBLE_API_KEY not set in environment or local .env"
    pf = preflight_fn()
    state["last_run"]["preflight"] = pf
    if not pf.get("reachable") and not settings.dry_run:
        blocker = (blocker + "; " if blocker else "") + f"egress: {pf['host']} {pf.get('reason')}"

    leads: list[dict] = []
    if blocker:
        for j in pending:
            state["jobs"][j["job_id"]] = {"status": "blocked", "reason": blocker, "at": utcnow()}
    else:
        client = client or NimbleClient(settings)
        if est > client.budget.remaining:
            state["last_run"]["note"] = f"Batch estimate {est} exceeds remaining budget {client.budget.remaining}; processing in priority order until the cap."

        def work(j: dict) -> tuple[dict, dict]:
            try:
                if j["kind"] == "search":
                    res = client.search(j["query"], max_results=10)
                    urls = result_urls(res.get("response"))
                else:
                    res = client.extract(j["url"])
                    urls = []
                return j, {"status": "dry_run" if res.get("dry_run") else "done",
                           "cached": res.get("cached"), "lead_count": len(urls), "leads": urls, "at": utcnow()}
            except (BudgetExhausted, AuthFailure, EgressDenied) as e:
                return j, {"status": "blocked", "reason": f"{type(e).__name__}: {e}", "at": utcnow()}
            except Exception as e:  # one failed job must not stop the others
                return j, {"status": "error", "reason": f"{type(e).__name__}: {str(e)[:200]}", "at": utcnow()}

        with ThreadPoolExecutor(max_workers=settings.max_concurrency) as pool:
            for j, outcome in pool.map(work, pending):
                state["jobs"][j["job_id"]] = outcome
                write_json(STATE_FILE, state)  # checkpoint after every job
    for j in jobs:
        st = state["jobs"].get(j["job_id"], {})
        for lead in st.get("leads", []):
            leads.append({"job_id": j["job_id"], "bank": j["bank"], "target_years": j["target_years"],
                          "query": j["query"], **lead, "status": "lead_unverified"})
    state["last_run"]["finished_utc"] = utcnow()
    state["last_run"]["blocker"] = blocker
    write_json(STATE_FILE, state)
    write_csv(C.DATA / "discovery_leads.csv", leads,
              ["job_id", "bank", "target_years", "query", "url", "title", "snippet", "status"])
    statuses = [state["jobs"].get(j["job_id"], {}).get("status", "pending") for j in jobs]
    return {"jobs": len(jobs), "estimated_requests": est, "blocker": blocker,
            "status_counts": {s: statuses.count(s) for s in sorted(set(statuses))}, "leads": len(leads)}
