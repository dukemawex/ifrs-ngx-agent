"""Stage 6: admission control, merge, recomputation and reconciliation.

The 47 baseline rows are retained unless an evidence-backed correction is logged.
New bank-years are added only when PAT, assets, liabilities and equity are all
admitted from one coherent operating-bank report version and the balance check passes.
"""
from __future__ import annotations

import re

from . import config as C
from . import candidates as K
from . import evidence as E
from .ratios import DERIVED, calculate, rounding_unit_ngnm, same, tolerance
from .util import number, read_csv, read_json, utcnow, write_csv, write_json

ADMISSIONS = C.DATA / "review" / "admissions.csv"
ADMISSION_EXTRA = ["admit", "is_correction", "correction_reason"]
REQUIRED_EVIDENCE = [
    "bank_key", "legal_entity", "financial_year", "variable", "raw_value", "raw_units", "currency",
    "normalised_value_ngnm_or_pct", "scope", "report_title", "report_year", "source_url", "pdf_sha256",
    "local_pdf_path", "pdf_page_1_based", "source_column_heading", "original_or_comparative",
    "reporting_version", "short_source_excerpt", "rendered_page_path", "method", "verification_status",
    "access_timestamp_utc",
]
ADMISSIBLE_STATUS = {"verified_reported", "derived_from_verified"}
CORE = ["pat", "assets", "liabilities", "equity"]
UNIT_FACTORS = {"NGN thousand": 0.001, "NGN million": 1.0, "NGN billion": 1000.0, "percent": 1.0}
NON_BANK_ENTITY = re.compile(r"holdings?\b|holdco|group plc|transnational|\bETI\b|\bUK\b|limited group|gtco", re.I)
NON_BANK_SCOPE = re.compile(r"\b(group|consolidated)\b", re.I)
PANEL_VALUE_FIELDS = ["pat", "assets", "liabilities", "equity", "ocf", "opening_assets", "gross_loans", "loan_allowance",
                      "net_loans", "total_impairment", "loan_impairment", "other_impairment", "credit_impairment",
                      "npl_amount", "npl_reported", "car", "car_transitional", "car_minimum", "regulatory_capital",
                      "rwa", "capital_transitional", "capital_addback", "liquidity", "gcu", "stage3_gross",
                      "stage3_allowance", "pbt", "gross_earnings", "specific_allowance", "collective_allowance"]

# Starting-pack exceptions that must survive unless a stronger source resolves them.
KNOWN_EXCEPTIONS = [
    {"id": "X-UBA-2015-ALW", "bank": "UBA", "year": 2015, "field": "loan_allowance", "expected": 13043.0,
     "rule": "UBA 2015 customer-loan allowance 13,043, not the candidate alternative"},
    {"id": "X-UBA-2016-ALW", "bank": "UBA", "year": 2016, "field": "loan_allowance", "expected": 29741.0,
     "rule": "UBA 2016 customer-loan allowance 29,741, not the candidate alternative"},
    {"id": "X-UBA-2022-LIQ", "bank": "UBA", "year": 2022, "field": "liquidity_admissible", "expected": 0.0,
     "rule": "UBA 2022 liquidity excluded until year-end/max inconsistency is reconciled"},
    {"id": "X-UNION-2017-PAT", "bank": "Union", "year": 2017, "field": "pat", "expected": 11239.0,
     "rule": "Union 2017 PAT uses the AMCON-restated comparative; not an ECL impact"},
    {"id": "X-UNION-2018-ALW", "bank": "Union", "year": 2018, "field": "loan_allowance", "expected": 45359.0,
     "rule": "Union 2018 original presentation retained; 190m reinstatement discrepancy unresolved"},
    {"id": "X-UNION-2022-S3", "bank": "Union", "year": 2022, "field": "stage3_coverage", "expected": None,
     "rule": "Union 2022 Stage 3 allowance subtotals conflict; matched Stage 3 coverage excluded"},
    {"id": "X-STERLING-2018-19", "bank": "Sterling", "year": 2018, "field": "scope", "expected": None,
     "rule": "Sterling 2018/2019 Bank and Group figures differ; Bank perimeter required"},
    {"id": "X-WEMA-2015-PAT", "bank": "Wema", "year": 2015, "field": "pat", "expected": None,
     "rule": "Wema 2015 PAT differs between original and later comparative presentation"},
]


def ensure_admissions_template() -> None:
    if not ADMISSIONS.is_file():
        write_csv(ADMISSIONS, [], E.EVIDENCE_COLUMNS + ADMISSION_EXTRA)


def check_admission(r: dict, downloads: dict[str, dict], cohort: dict[str, dict]) -> list[str]:
    errs = [f"missing {k}" for k in REQUIRED_EVIDENCE if not str(r.get(k, "")).strip()]
    if not (str(r.get("printed_page", "")).strip() or str(r.get("note_number", "")).strip()):
        errs.append("missing printed_page or note_number")
    if r.get("verification_status") not in ADMISSIBLE_STATUS:
        errs.append(f"verification_status {r.get('verification_status')!r} not admissible")
    if r.get("bank_key") not in cohort:
        errs.append("bank_key not in cohort")
    if NON_BANK_ENTITY.search(r.get("legal_entity", "")):
        errs.append("legal_entity looks like a holding company/group/foreign subsidiary")
    if NON_BANK_SCOPE.search(r.get("scope", "")) or NON_BANK_SCOPE.search(r.get("source_column_heading", "")):
        errs.append("scope/column is Group or Consolidated, not the operating bank")
    try:
        y = int(r.get("financial_year", ""))
        if y not in C.STUDY_YEARS and r.get("variable") != "opening_assets":
            errs.append("financial_year outside 2013-2022")
    except ValueError:
        errs.append("financial_year not an integer")
    sha = r.get("pdf_sha256", "")
    if sha and sha not in downloads:
        errs.append("pdf_sha256 does not match any downloaded report")
    elif sha and not (C.ROOT / downloads[sha]["local_pdf_path"]).is_file():
        errs.append("local PDF missing")
    rp = r.get("rendered_page_path", "")
    if rp and not (C.ROOT / rp).is_file():
        errs.append("rendered page image missing (page must be inspected)")
    try:
        raw, norm = number(r.get("raw_value")), number(r.get("normalised_value_ngnm_or_pct"))
        f = UNIT_FACTORS.get(r.get("raw_units", ""))
        if f is None:
            errs.append(f"unknown raw_units {r.get('raw_units')!r}")
        elif raw is not None and norm is not None and abs(raw * f - norm) > 0.5 * f + 1e-9:
            errs.append("normalised value does not match raw value x unit factor")
    except ValueError:
        errs.append("non-numeric raw or normalised value")
    return errs


def run() -> dict:
    ensure_admissions_template()
    baseline = read_csv(C.SELECTED_CSV)
    cohort = {r["bank"]: r for r in read_csv(C.TASKS / "cohort.csv")}
    dl = read_json(C.STATE / "download_state.json", {}).get("reports", {})
    downloads = {v["sha256"]: v for v in dl.values() if v.get("status") == "downloaded"}
    fieldnames = list(baseline[0].keys())
    panel = {(r["bank"], int(r["year"])): dict(r) for r in baseline}
    if len(panel) != len(baseline):
        raise SystemExit("Duplicate bank-year keys in baseline")
    changes: list[dict] = []
    review: list[dict] = []
    conflicts: list[dict] = []

    # 1. Admission control
    accepted: dict[tuple[str, int, str], dict] = {}
    for r in read_csv(ADMISSIONS):
        if str(r.get("admit", "")).strip().lower() not in ("1", "yes", "true"):
            continue
        errs = check_admission(r, downloads, cohort)
        key = (r.get("bank_key", ""), int(r["financial_year"]) if str(r.get("financial_year", "")).isdigit() else -1, r.get("variable", ""))
        if not errs and key in accepted and not same(number(accepted[key]["normalised_value_ngnm_or_pct"]), number(r["normalised_value_ngnm_or_pct"])):
            errs.append("conflicts with another admitted value for the same bank/year/variable")
            conflicts.append({"type": "admission_conflict", "bank": key[0], "year": key[1], "field": key[2],
                              "value_a": accepted[key]["normalised_value_ngnm_or_pct"],
                              "value_b": r["normalised_value_ngnm_or_pct"], "detail": "two admitted values differ"})
        review.append({**{k: r.get(k, "") for k in ("evidence_id", "bank_key", "financial_year", "variable", "normalised_value_ngnm_or_pct")},
                       "accepted": not errs, "errors": "; ".join(errs)})
        if not errs:
            accepted[key] = r

    # 2. Merge: new rows need the full core set, coherent version, and a passing balance check.
    by_by: dict[tuple[str, int], dict[str, dict]] = {}
    for (b, y, v), r in accepted.items():
        by_by.setdefault((b, y), {})[v] = r
    admitted_new_rows, partial_new = [], []
    for (b, y), fields in by_by.items():
        if (b, y) in panel:
            row = panel[(b, y)]
            for v, r in fields.items():
                if v not in fieldnames:
                    continue
                new = number(r["normalised_value_ngnm_or_pct"])
                old = number(row.get(v))
                if old is None:
                    row[v] = new
                    changes.append({"bank": b, "year": y, "field": v, "old": "", "new": new, "kind": "fill_blank",
                                    "basis": r["evidence_id"], "reason": "admitted reviewed evidence"})
                elif not same(old, new):
                    if str(r.get("is_correction", "")).lower() in ("1", "yes", "true") and r.get("correction_reason"):
                        row[v] = new
                        changes.append({"bank": b, "year": y, "field": v, "old": old, "new": new, "kind": "correction",
                                        "basis": r["evidence_id"], "reason": r["correction_reason"]})
                    else:
                        conflicts.append({"type": "admitted_vs_selected", "bank": b, "year": y, "field": v,
                                          "value_a": old, "value_b": new,
                                          "detail": "selected value retained; mark is_correction with reason to replace"})
            continue
        core_ok = all(c in fields for c in CORE)
        versions = {fields[c]["reporting_version"] for c in CORE if c in fields}
        bal_ok = False
        if core_ok:
            a, l, e = (number(fields[c]["normalised_value_ngnm_or_pct"]) for c in ("assets", "liabilities", "equity"))
            unit = max(UNIT_FACTORS.get(fields[c]["raw_units"], 1.0) for c in ("assets", "liabilities", "equity"))
            bal_ok = abs(a - l - e) <= tolerance(3, unit)
        if core_ok and len(versions) == 1 and bal_ok:
            row = {k: "" for k in fieldnames}
            row.update({"bank": b, "year": y, "tier": cohort[b]["analytical_tier"],
                        "regime": "IAS 39" if y < C.ADOPTION_YEAR else "IFRS 9",
                        "origin": "Admitted this run", "scope": "Standalone operating bank",
                        "version_note": next(iter(versions)),
                        "source_url": fields["assets"]["source_url"]})
            for v, r in fields.items():
                if v in fieldnames:
                    row[v] = number(r["normalised_value_ngnm_or_pct"])
            panel[(b, y)] = row
            admitted_new_rows.append(f"{b} {y}")
            changes.append({"bank": b, "year": y, "field": "*row*", "old": "", "new": "added", "kind": "new_bank_year",
                            "basis": ";".join(r["evidence_id"] for r in fields.values()), "reason": "core set admitted and reconciled"})
        else:
            partial_new.append({"bank": b, "year": y, "admitted_fields": ";".join(sorted(fields)),
                                "core_complete": core_ok, "single_version": len(versions) == 1, "balance_ok": bal_ok})

    # 3. Recompute derived ratios from eligible inputs only.
    recompute_diffs = 0
    for (b, y), row in panel.items():
        calc = calculate(row)
        # Liquidity is used only with an explicit admissibility flag of 1.
        flag = number(row.get("liquidity_admissible"))
        row["liquidity_used"] = row.get("liquidity", "") if flag == 1 else ""
        for f, new in calc.items():
            old = number(row.get(f))
            if not same(old, new):
                recompute_diffs += 1
                changes.append({"bank": b, "year": y, "field": f, "old": "" if old is None else old,
                                "new": "" if new is None else new, "kind": "recomputed_derived",
                                "basis": "ratios.calculate", "reason": "derived value recomputed from current inputs"})
            row[f] = "" if new is None else new
        # Union 2022 matched Stage 3 coverage stays excluded (conflicting subtotals).
        if b == "Union" and y == 2022 and row.get("stage3_coverage") not in ("", None):
            changes.append({"bank": b, "year": y, "field": "stage3_coverage", "old": row["stage3_coverage"], "new": "",
                            "kind": "exception_enforced", "basis": "U11", "reason": "conflicting Stage 3 allowance definitions"})
            row["stage3_coverage"] = ""

    # 4. Reconciliation checks.
    checks = []
    for (b, y), row in sorted(panel.items()):
        a, l, e = row.get("assets"), row.get("liabilities"), row.get("equity")
        if all(str(x).strip() for x in (a, l, e)):
            u = rounding_unit_ngnm(a, l, e)
            res = number(a) - number(l) - number(e)
            tol = tolerance(3, u)
            checks.append({"bank": b, "year": y, "check": "assets = liabilities + equity", "residual": round(res, 6),
                           "tolerance": tol, "rounding_unit_ngnm": u, "passed": abs(res) <= tol})
        gl, al, nl = row.get("gross_loans"), row.get("loan_allowance"), row.get("net_loans")
        if all(str(x).strip() for x in (gl, al, nl)):
            u = rounding_unit_ngnm(gl, al, nl)
            res = number(gl) - number(al) - number(nl)
            tol = tolerance(3, u)
            checks.append({"bank": b, "year": y, "check": "gross loans - allowance = net loans", "residual": round(res, 6),
                           "tolerance": tol, "rounding_unit_ngnm": u, "passed": abs(res) <= tol})
        car, cc = number(row.get("car")), number(row.get("car_computed"))
        if car is not None and cc is not None:
            tol, why = car_tolerance(row.get("car"), row.get("car_basis", ""))
            checks.append({"bank": b, "year": y, "check": "reported CAR vs capital/RWA", "residual": round(car - cc, 4),
                           "tolerance": tol, "rounding_unit_ngnm": "", "passed": abs(car - cc) <= tol,
                           "note": f"{why}; basis={row.get('car_basis','')}; transitional={row.get('car_transitional','')}"})

    # 5. Known exceptions retained?
    exc = []
    for x in KNOWN_EXCEPTIONS:
        row = panel.get((x["bank"], x["year"]))
        actual = row.get(x["field"], "") if row else "(row absent)"
        if x["expected"] is None:
            status = "retained (documented; value not altered)" if not (x["field"] == "stage3_coverage" and str(actual).strip()) else "VIOLATED"
        else:
            status = "retained" if same(number(actual), x["expected"]) else "VIOLATED"
        exc.append({**x, "actual": actual, "status": status})
    for e in read_json(C.WORK / "update_pack" / "prior_evidence" / "exceptions.json", []):
        exc.append({"id": e[0], "bank": "Union", "year": e[2], "field": e[1], "expected": "", "rule": f"{e[3]} -> {e[4]}",
                    "actual": "", "status": f"inherited exception ({e[5]})"})

    # 6. Evidence backing of every selected monetary/indicator value.
    ev = E.inherited()
    adm_ev = [{**r, "evidence_origin": "admissions.csv"} for r in accepted.values()]
    idx = E.backing_index(ev + adm_ev)
    backing = []
    for (b, y), row in sorted(panel.items()):
        for f in PANEL_VALUE_FIELDS:
            v = row.get(f, "")
            if not str(v).strip():
                continue
            recs = idx.get((b, y, f), [])
            how = "direct" if E.evidence_matches(v, recs) else ""
            if not how and f == "opening_assets":
                prev = idx.get((b, y - 1, "assets"), [])
                if E.evidence_matches(v, prev):
                    recs, how = prev, "prior-year closing assets"
            if not how:
                comp_recs, label = E.component_match(v, f, b, y, idx)
                if label:
                    recs, how = comp_recs, label
            backing.append({"bank": b, "year": y, "field": f, "value": v,
                            "evidence_records": len(recs), "value_matches_evidence": bool(how), "match_basis": how,
                            "evidence_ids": ";".join(r["evidence_id"] for r in recs[:6])})
    # Inherited evidence that disagrees internally for one bank/year/variable.
    for (b, y, f), recs in idx.items():
        vals = sorted({number(r["normalised_value_ngnm_or_pct"]) for r in recs
                       if _num_ok(r["normalised_value_ngnm_or_pct"])} - {None})
        if len(vals) > 1 and (vals[-1] - vals[0]) > 0.5:
            conflicts.append({"type": "evidence_alternatives", "bank": b, "year": y, "field": f,
                              "value_a": vals[0], "value_b": vals[-1],
                              "detail": "; ".join(f"{r['evidence_id']}={r['normalised_value_ngnm_or_pct']} [{r['review_reason'][:70]}]" for r in recs[:4])})

    cands = K.load()
    conflicts += K.compare(cands, panel)
    write_csv(C.DATA / "candidates.csv", cands,
              ["bank", "year", "field", "value", "candidate_source", "locator", "status", "note"])
    write_csv(C.DATA / "conflicts.csv", conflicts, ["type", "bank", "year", "field", "value_a", "value_b", "detail"])
    out_fields = fieldnames + [c for c in ("liquidity_used",) if c not in fieldnames]
    rows = [panel[k] for k in sorted(panel)]
    write_csv(C.DATA / "verified_panel.csv", rows, out_fields)
    write_csv(C.DATA / "change_register.csv", changes, ["bank", "year", "field", "old", "new", "kind", "basis", "reason"])
    write_csv(C.DATA / "admission_review.csv", review)
    write_csv(C.DATA / "partial_new_bank_years.csv", partial_new,
              ["bank", "year", "admitted_fields", "core_complete", "single_version", "balance_ok"])
    write_csv(C.DATA / "reconciliation_checks.csv", checks,
              ["bank", "year", "check", "residual", "tolerance", "rounding_unit_ngnm", "passed", "note"])
    write_csv(C.DATA / "exceptions_register.csv", exc, ["id", "bank", "year", "field", "expected", "actual", "status", "rule"])
    write_csv(C.DATA / "evidence_backing.csv", backing)
    write_csv(C.DATA / "evidence_long.csv", ev + adm_ev, E.EVIDENCE_COLUMNS)
    write_json(C.DATA / "validate_state.json", {
        "at": utcnow(), "admissions_reviewed": len(review), "admissions_accepted": len(accepted),
        "new_bank_years": admitted_new_rows, "partial_new": len(partial_new),
        "recompute_differences": recompute_diffs, "changes": len(changes),
        "exceptions_violated": [x["id"] for x in exc if x["status"] == "VIOLATED"],
    })
    return {"panel_rows": len(rows), "admissions_accepted": len(accepted), "new_bank_years": admitted_new_rows,
            "recompute_differences": recompute_diffs, "checks": len(checks),
            "checks_failed": sum(not c["passed"] for c in checks),
            "exceptions_violated": [x["id"] for x in exc if x["status"] == "VIOLATED"],
            "fields_without_matching_evidence": sum(not b["value_matches_evidence"] for b in backing),
            "fields_checked_for_evidence": len(backing), "conflicts": len(conflicts)}


def car_tolerance(car_raw, basis: str) -> tuple[float, str]:
    """Half the published rounding step. A whole-percent step applies only where the
    basis note documents a whole/rounded published ratio and the stored value is integral."""
    from .ratios import decimals
    v = number(car_raw)
    documented = re.search(r"whole|rounded", basis or "", re.I)
    if documented and v is not None and float(v).is_integer():
        return 0.5 + 0.01, "whole-percent published ratio (documented)"
    return 0.5 * 10 ** (-decimals(car_raw)) + 0.01, "rounding from recorded decimals"


def _num_ok(v) -> bool:
    try:
        return number(v) is not None
    except ValueError:
        return False
