"""Release statistics, summary and manifest computed only from saved machine-readable outputs.

Nothing in the summary is typed by hand: every count comes from release_stats(),
and tests/test_real_data.py recomputes the same counts independently from the CSVs.
"""
from __future__ import annotations

import subprocess
from collections import Counter

from . import config as C
from .util import number, read_csv, read_json, sha256_file, utcnow, write_json

from . import eligibility as E


def _git(*args) -> str:
    try:
        return subprocess.run(["git", *args], cwd=C.ROOT, capture_output=True, text=True, timeout=20).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        return ""


def nimble_usage() -> dict:
    """Counted from the call ledger (plugin) and the REST budget state; never from hand-kept totals."""
    calls = read_csv(C.DATA / "review" / "nimble_calls.csv")
    plugin = [c for c in calls if c.get("channel") == "mcp_plugin"]
    by_tool: dict[str, int] = {}
    for c in plugin:
        by_tool[c["tool"]] = by_tool.get(c["tool"], 0) + 1
    budget = read_json(C.STATE / "nimble_budget.json", {})
    rest = [c for c in calls if c.get("channel") == "rest"]
    return {
        "rest_client": {"attempted_requests": int(budget.get("used", 0)) if budget else len(rest), "cap": 100,
                        "retries": sum(int(c.get("attempts") or 1) - 1 for c in rest),
                        "failed_attempts": sum(c.get("outcome") not in ("completed", "ok") for c in rest),
                        "note": "REST client not run in this release (no nimble_budget state); key value never printed"},
        "mcp_plugin": {"invocations": len(plugin), "attempts": sum(int(c.get("attempts") or 1) for c in plugin), "by_tool": by_tool,
                       "failed": sum(c.get("outcome") not in ("completed", "ok") for c in plugin),
                       "note": "Plugin invocation counts do not establish provider-internal HTTP request counts or billing; billed requests not available"},
        "shared_cap": 100, "cap_changed": False,
    }


def release_stats() -> dict:
    D = C.DATA
    base = read_csv(C.SELECTED_CSV)
    panel = read_csv(D / "verified_panel.csv")
    changes = read_csv(D / "change_register.csv")
    fs = read_csv(D / "field_status.csv")
    recon = read_csv(D / "reconciliation_checks.csv")
    backing = read_csv(D / "evidence_backing.csv")
    conflicts = read_csv(D / "conflicts.csv")
    gaps = read_csv(D / "unresolved_gaps.csv") if (D / "unresolved_gaps.csv").is_file() else []
    gcr = read_csv(D / "review" / "going_concern_reviews.csv")
    adm_review = read_csv(D / "admission_review.csv")
    vdec = read_csv(D / "review" / "version_decisions.csv")
    denom = read_csv(D / "denominator_compatibility.csv")
    nimble = nimble_usage()
    tests = read_json(C.OUTPUTS / "test_results.json", {})
    base_keys = {(r["bank"], r["year"]) for r in base}
    pre = sum(int(r["year"]) < C.ADOPTION_YEAR for r in panel)

    endpoints = E.summarise()

    gc_panel = [r for r in fs if r["field"] == "gcu"]
    gc_base = [r for r in gc_panel if (r["bank"], r["year"]) in base_keys and r["change_kind"] == ""]
    gc_fill = [r for r in gc_panel if r["change_kind"] == "fill_blank"]
    gc_new = [r for r in gc_panel if r["change_kind"] == "new_row"]
    reviews = [r for r in gcr if r["gcu_code"] != ""]
    rev_keys = {(r["bank"], r["year"]) for r in reviews}
    confirms = [r for r in gc_base if (r["bank"], r["year"]) in rev_keys]

    status = Counter(r["status"] for r in recon)
    return {
        "generated_utc": utcnow(),
        "git_commit": _git("rev-parse", "HEAD"), "git_branch": _git("rev-parse", "--abbrev-ref", "HEAD"),
        "panel": {"rows": len(panel), "banks": len({r["bank"] for r in panel}), "pre_adoption": pre,
                  "post_adoption": len(panel) - pre, "baseline_rows": len(base),
                  "baseline_rows_retained": sum((r["bank"], r["year"]) in base_keys for r in panel),
                  "new_rows": sum((r["bank"], r["year"]) not in base_keys for r in panel)},
        "changes": dict(Counter(c["kind"] for c in changes)),
        "fills_by_field": dict(Counter(c["field"] for c in changes if c["kind"] == "fill_blank")),
        "field_basis": dict(Counter(r["value_basis"] for r in fs)),
        "admissions": {"rows": len(adm_review), "accepted": sum(r["accepted"] == "True" for r in adm_review),
                       "rejected": sum(r["accepted"] != "True" for r in adm_review)},
        "reconciliation": {"run": len(recon), **{k: v for k, v in status.items()}},
        "evidence_lineage": {"checked": len(backing), "matched": sum(b["value_matches_evidence"] == "True" for b in backing),
                             "qualified": sum(bool(b.get("qualification")) for b in backing)},
        "going_concern": {"reviews_recorded": len(reviews), "reviews_coded_1": sum(r["gcu_code"] == "1" for r in reviews),
                          "partial_reviews": sum(r["report_reviewed"].startswith("partially") for r in gcr),
                          "not_reviewed_listed": sum(r["gcu_code"] == "" for r in gcr),
                          "panel_coded": len(gc_panel), "panel_unknown": len(panel) - len(gc_panel),
                          "panel_coded_1": sum(number(r["value"]) == 1 for r in gc_panel),
                          "baseline_codes_retained": len(gc_base), "baseline_codes_confirmed_by_review": len(confirms),
                          "fills_in_baseline_rows": len(gc_fill), "codes_on_new_rows": len(gc_new)},
        "conflicts": dict(Counter(c["type"] for c in conflicts)),
        "version_decisions": dict(Counter(v["classification"] for v in vdec)),
        "denominators": {"checked": len(denom), "incompatible": sum(d["compatible"] != "True" for d in denom),
                         "differing": [f"{d['bank']} {d['year']} (opening {d['opening_assets']} from {d['opening_version']}; "
                                       f"prior closing {d['prior_year_closing_assets']} from {d['prior_closing_version']})"
                                       for d in denom if d["compatible"] != "True"]},
        "remaining": {"bank_years": sum(g["gap_type"] == "bank_year" for g in gaps),
                      "field_requests": sum(g["gap_type"] != "bank_year" for g in gaps)},
        "endpoints": endpoints,
        "row_versions": _row_versions(),
        "unresolved_exceptions": _unresolved(recon, vdec),
        "remaining_by_bank": _remaining_by_bank(gaps),
        "readiness": {"estimators": read_csv(C.OUTPUTS / "readiness" / "estimator_recommendations.csv") if (C.OUTPUTS / "readiness" / "estimator_recommendations.csv").is_file() else [],
                      "objectives": read_csv(C.OUTPUTS / "readiness" / "objective_readiness.csv") if (C.OUTPUTS / "readiness" / "objective_readiness.csv").is_file() else []},
        "nimble": nimble,
        "tests": tests,
    }


def _row_versions() -> dict:
    path = C.DATA / "row_versions.csv"
    rv = read_csv(path) if path.is_file() else []
    fb = [r for r in rv if r["fallback_class"]]
    return {"rows": len(rv), "treatments": dict(Counter(r["treatment"] for r in rv)),
            "fallback_rows": [f"{r['bank']} {r['year']} ({r['fallback_class']}; source {r['primary_source']}; labelled restated: {r['labelled_restated']})" for r in fb],
            "unreconciled_version_mixes": sum(r["version_mix_reconciliation"] == "UNRECONCILED" for r in rv)}


def _unresolved(recon: list[dict], vdec: list[dict]) -> list[str]:
    out = [f"{r['bank']} {r['year']} {r['check']}: documented source exception" for r in recon if r["status"] == "documented_source_exception"]
    keep = ("source internal inconsistency", "unexplained difference", "confirmed scope difference", "possible scope incompatibility")
    out += [f"{d['bank']} {d['year']} {d['field']}: {d['classification']}" + ("; OWNER DECISION PENDING" if "PENDING" in d["decision"] else "")
            for d in vdec if d["classification"].startswith(keep)]
    out += [f"{c['bank']} {c['year']} {c['field']}: {c['type']}" for c in read_csv(C.DATA / "review" / "reviewer_conflicts.csv")
            if c["type"] == "source_internal_inconsistency_cross_report"]
    return out


def _remaining_by_bank(gaps: list[dict]) -> dict:
    by: dict[str, list[str]] = {}
    for g in gaps:
        if g["gap_type"] == "bank_year":
            by.setdefault(g["bank"], []).append(str(g["year"]))
    return {b: sorted(v) for b, v in sorted(by.items())}


def render(stats: dict, audit: dict, handoff: dict) -> str:
    p, g, rc, t = stats["panel"], stats["going_concern"], stats["reconciliation"], stats["tests"]
    ch = stats["changes"]
    L = ["# Reconciliation summary", "",
         f"Generated {stats['generated_utc']} from the saved outputs (code commit `{stats['git_commit']}`, branch `{stats['git_branch']}`).",
         "Every number below is computed by `ifrs9_recovery.summary.release_stats()`; see `outputs/release_stats.json`.", "",
         "## Panel", "",
         f"- Selected bank-years: **{p['rows']}** across {p['banks']} banks ({p['pre_adoption']} pre-adoption, {p['post_adoption']} post-adoption).",
         f"- Baseline rows: {p['baseline_rows']} (all {p['baseline_rows_retained']} retained); additional rows admitted: {p['new_rows']}.",
         "- These are selected rows, not complete observations for every endpoint (see endpoint table).", "",
         "## What changed relative to the frozen baseline", "",
         "- Raw input files: unchanged (SHA-256 checked by `inventory`).",
         f"- Non-blank baseline measurements changed: {ch.get('correction', 0)} (corrections are the only route).",
         f"- Authorised fills of blank baseline cells: {ch.get('fill_blank', 0)} ({', '.join(f'{k} {v}' for k, v in stats['fills_by_field'].items()) or 'none'}).",
         f"- Recomputed derived values that differ from stored: {ch.get('recomputed_derived', 0)}.",
         f"- Additional bank-years: {ch.get('new_bank_year', 0)}.",
         f"- Field basis of all non-blank cells: {', '.join(f'{k} {v}' for k, v in sorted(stats['field_basis'].items()))}.", "",
         "## Admission and reconciliation", "",
         f"- Admissions: {stats['admissions']['accepted']} accepted, {stats['admissions']['rejected']} rejected "
         "(file hash recomputed, page and rendered image re-verified, structured scope, explicit sign transform, derived values recomputed).",
         f"- Reconciliation checks run: {rc['run']}; pass {rc.get('pass', 0)}; fail {rc.get('fail', 0)}; "
         f"documented source exception {rc.get('documented_source_exception', 0)}.",
         f"- Evidence lineage: {stats['evidence_lineage']['matched']} of {stats['evidence_lineage']['checked']} non-blank inputs matched to an evidence record; "
         f"{stats['evidence_lineage']['qualified']} carry an explicit qualification.",
         f"- Average-asset denominators: {stats['denominators']['checked']} checked against prior-year closing assets; "
         f"{stats['denominators']['incompatible']} differ (listed in `data/denominator_compatibility.csv`). "
         "Each ratio uses the opening balance from the same report as its closing balance; differing pairs are not smoothed.",
         *[f"  - {x}" for x in stats['denominators'].get('differing', [])], "",
         "## Outcome eligibility (one ruleset: `ifrs9_recovery.eligibility`, `data/outcome_eligibility.csv`)", "", "Available = value present; descriptive/longitudinal/inferential uses are distinct; change pairs = year-on-year changes that are comparable; fallback rows stay in the primary sample but are dropped in sensitivity runs.", "", "| Outcome | Available | Descriptive | Longitudinal | Change pairs | Eligible (inferential) | Excluded from inference | Banks | Pre | Post | Tier 1 | Tier 2 | Fallback rows |", "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    L += [f"| {k} | {v['available']} | {v['descriptive']} | {v['longitudinal']} | {v['change_pairs']} | {v['eligible']} | {v['excluded_from_inference']} | {v['banks']} | {v['pre']} | {v['post']} | {v['tier1']} | {v['tier2']} | {v['fallback_rows_in_sample']} |" for k, v in stats["endpoints"].items()]
    L += ["", "Rows excluded from inference (rule ids in `data/outcome_eligibility.csv`, reasons in `data/review/eligibility_rules.csv`):", ""]
    L += [f"- {k}: " + "; ".join(v["excluded_rows"]) for k, v in stats["endpoints"].items() if v["excluded_rows"]]
    L += ["", "## Going concern", "",
          f"- Full original-year auditor reports reviewed and recorded: {g['reviews_recorded']} ({g['reviews_coded_1']} coded 1); "
          f"partially available reports (left uncoded): {g.get('partial_reviews', 0)}.",
          f"- Bank-years explicitly listed as not reviewed: {g['not_reviewed_listed']}.",
          f"- Panel rows coded: {g['panel_coded']} ({g['panel_coded_1']} coded 1); unknown: {g['panel_unknown']}. Unknown is not zero.",
          f"- Of the coded rows: {g['baseline_codes_retained']} baseline codes retained ({g['baseline_codes_confirmed_by_review']} confirmed by this review), "
          f"{g['fills_in_baseline_rows']} filled in baseline rows, {g['codes_on_new_rows']} on additional rows.",
          "- A zero means no material-uncertainty section or going-concern emphasis was found after the recorded review; it does not certify survival.",
          f"- With {g['panel_coded_1']} positive event(s), a multivariable going-concern model is not supported; report event counts before choosing an estimator.", "",
          "## Version decisions and conflicts", "",
          "- Version classifications: " + ", ".join(f"{k} {v}" for k, v in sorted(stats["version_decisions"].items())) + " (`data/review/version_decisions.csv`).",
          "- Conflicts recorded: " + ", ".join(f"{k} {v}" for k, v in sorted(stats["conflicts"].items())) + ".", "",
          "## Reporting versions (`data/row_versions.csv`)", "",
          *[f"- {k}: {v}" for k, v in stats["row_versions"]["treatments"].items()],
          "- Fallback rows (primary, dropped in sensitivity): " + "; ".join(stats["row_versions"]["fallback_rows"]) + ".",
          f"- Unreconciled version mixes: {stats['row_versions']['unreconciled_version_mixes']}.", "",
          "## Unresolved exceptions", "",
          *[f"- {x}" for x in stats["unresolved_exceptions"]], "",
          "## Model readiness (`outputs/readiness/readiness.md`; no thesis regressions run)", "",
          *[f"- {r['objective']} {r['description']}: {r['readiness']} (testable: {r['statistically_testable_outcomes'] or 'none'})" for r in stats["readiness"]["objectives"]],
          "- IFRS9_D is perfectly collinear with a full set of year fixed effects.", "",
          "## Remaining", "",
          f"- Bank-year positions not admitted: {stats['remaining']['bank_years']}; field requests in selected rows outstanding: {stats['remaining']['field_requests']}.",
          *[f"  - {b}: {', '.join(v)}" for b, v in stats["remaining_by_bank"].items()], "",
          "## Tests", ""]
    if t:
        for suite, r in t.get("suites", {}).items():
            L.append(f"- {suite}: {r.get('passed', 0)} passed, {r.get('failed', 0)} failed, {r.get('skipped', 0)} skipped.")
        L.append(f"- Test run: {t.get('run_utc', '')}.")
    else:
        L.append("- Not run in this export.")
    n = stats["nimble"]
    L += ["", "## Nimble usage", "",
          f"- REST client attempted requests: {n.get('rest_client', {}).get('attempted_requests', 0)} (cap {n.get('shared_cap', 100)}, unchanged).",
          f"- Plugin invocations: {n.get('mcp_plugin', {}).get('invocations', 0)} "
          f"({', '.join(f'{k} {v}' for k, v in n.get('mcp_plugin', {}).get('by_tool', {}).items())}). Provider-billed requests: not available.", "",
          "## Workbook and handoff", "",
          f"- Formula audit after LibreOffice recalculation: {audit}.",
          f"- Handoff zip: {handoff.get('files', 0)} files; rendered evidence page images included: {handoff.get('evidence_images', 0)}; "
          f"admission image paths without an included image: {handoff.get('missing_images', 0)}.",
          f"- Source PDFs are NOT included ({handoff.get('pdfs', 0)} files); each is listed with URL and SHA-256 in `reports/index.csv`. "
          "Manual and image-only transcriptions cannot be reproduced from a hash alone: re-inspect the cited page.", "",
          "## Not done", "",
          "- No regression, hypothesis test or volatility estimate was run, and the thesis was not updated.",
          "- No candidate (unverified) amount was promoted to the panel.",
          f"- Going-concern codes remain unknown for {g['panel_unknown']} panel rows.", ""]
    return "\n".join(L)


def release_manifest(stats: dict) -> dict:
    files = {}
    for rel in ["data/verified_panel.csv", "data/evidence_long.csv", "data/change_register.csv", "data/field_status.csv",
                "data/reconciliation_checks.csv", "data/admission_review.csv", "data/conflicts.csv", "data/unresolved_gaps.csv",
                "data/review/specs.csv", "data/review/admissions.csv", "data/review/going_concern_reviews.csv",
                "data/review/version_decisions.csv", "outputs/IFRS9_Verified_Master.xlsx"]:
        p = C.ROOT / rel
        if p.is_file():
            files[rel] = sha256_file(p)
    inputs = {p.name: sha256_file(p) for p in sorted(C.INPUTS.glob("*")) if p.is_file()}
    return {"generated_utc": stats["generated_utc"], "git_commit_at_export": stats["git_commit"],
            "git_branch": stats["git_branch"], "run_id": f"export-{stats['generated_utc']}",
            "input_hashes": inputs, "output_hashes": files,
            "note": "git_commit_at_export is the commit checked out when exporting; outputs are committed in the following commit."}
