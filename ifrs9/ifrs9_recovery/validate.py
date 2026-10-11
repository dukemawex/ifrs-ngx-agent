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
UNIT_FACTORS = {"NGN thousand": 0.001, "NGN million": 1.0, "NGN billion": 1000.0, "percent": 1.0, "indicator": 1.0}
NON_BANK_ENTITY = re.compile(r"holdings?\b|holdco|group plc|transnational|\bETI\b|\bUK\b|limited group|gtco", re.I)
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


DOC_SCOPES = {"consolidated_and_separate", "separate_only", "single_entity", "group_only", "holding_company_report"}
BANK_COLUMN_SCOPES = {"bank_separate", "bank_single_entity", "bank_subsidiary_disclosure"}
# bank_subsidiary_disclosure: an explicit operating-bank column in the audited notes of a holding-company report
# (e.g. GTCO 'GT Bank Nigeria' condensed results). Admissible only inside a holding_company_report, only when the
# reviewer has established entity-only (Nigeria operating bank, not subgroup) scope in column_scope_basis.
SCOPE_LABEL = {"bank_separate": "Standalone operating bank",
               "bank_single_entity": "Standalone operating bank",
               "bank_subsidiary_disclosure": "Operating bank: audited HoldCo package - explicit operating-bank subsidiary disclosure"}
GC_APPLICABLE = {"covers_bank_separate", "bank_single_entity"}
# Variables whose printed presentation is a deduction/expense and may be stored with the
# panel's expense-positive convention. Any other sign change is rejected.
SIGN_CONVERTIBLE = re.compile(r"^(total_impairment|loan_impairment|other_impairment|credit_impairment|"
                              r"loan_allowance(_[\w-]+)?|specific_allowance|collective_allowance|stage[123]_allowance(_[\w-]+)?)$")
_SHA_CACHE: dict[str, str] = {}
_PAGECOUNT_CACHE: dict[str, int] = {}
_RENDER_CACHE: dict[tuple[str, int], str] = {}


def _file_sha(path) -> str:
    key = str(path)
    if key not in _SHA_CACHE:
        from .util import sha256_file
        _SHA_CACHE[key] = sha256_file(path)
    return _SHA_CACHE[key]


def _page_count(path) -> int:
    key = str(path)
    if key not in _PAGECOUNT_CACHE:
        import pymupdf
        with pymupdf.open(path) as d:
            _PAGECOUNT_CACHE[key] = d.page_count
    return _PAGECOUNT_CACHE[key]


def _pixel_digest_of_png(path) -> str:
    import hashlib
    import pymupdf
    pm = pymupdf.Pixmap(str(path))
    return hashlib.sha256(bytes(pm.samples) + f"{pm.width}x{pm.height}".encode()).hexdigest()


def _pixel_digest_of_page(pdf_path, page: int, dpi: int = 110) -> str:
    import hashlib
    import pymupdf
    key = (str(pdf_path), page)
    if key not in _RENDER_CACHE:
        with pymupdf.open(pdf_path) as d:
            pm = d[page - 1].get_pixmap(dpi=dpi)
            _RENDER_CACHE[key] = hashlib.sha256(bytes(pm.samples) + f"{pm.width}x{pm.height}".encode()).hexdigest()
    return _RENDER_CACHE[key]


def check_scope(r: dict) -> list[str]:
    """Structured scope test. Narrative 'scope' text is preserved verbatim and never pattern-matched."""
    errs = []
    if NON_BANK_ENTITY.search(r.get("legal_entity", "")):
        errs.append("extracted legal entity looks like a holding company/group/foreign subsidiary")
    ds = r.get("document_scope", "")
    if ds not in DOC_SCOPES:
        errs.append(f"document_scope {ds!r} not recorded")
    if r.get("variable") == "gcu":
        if r.get("opinion_applicability") not in GC_APPLICABLE:
            errs.append(f"auditor opinion applicability {r.get('opinion_applicability')!r} does not establish coverage "
                        "of the operating bank (pending review)")
        return errs
    cs = r.get("column_scope", "")
    if cs not in BANK_COLUMN_SCOPES:
        errs.append(f"column_scope {cs!r} is not an operating-bank column")
    elif cs == "bank_separate" and ds not in ("consolidated_and_separate", "separate_only"):
        errs.append("bank_separate column claimed in a document without separate statements")
    elif cs == "bank_single_entity" and ds != "single_entity":
        errs.append("bank_single_entity column claimed in a document that is not single-entity")
    elif cs == "bank_subsidiary_disclosure" and ds != "holding_company_report":
        errs.append("bank_subsidiary_disclosure column claimed outside a holding-company report")
    if not str(r.get("column_scope_basis", "")).strip():
        errs.append("column_scope_basis (verbatim heading evidence) missing")
    return errs


def check_admission(r: dict, downloads: dict[str, dict], cohort: dict[str, dict], verify_files: bool = True) -> list[str]:
    required = [k for k in REQUIRED_EVIDENCE if not (k == "currency" and r.get("raw_units") in ("percent", "indicator"))]
    errs = [f"missing {k}" for k in required if not str(r.get(k, "")).strip()]
    if not (str(r.get("printed_page", "")).strip() or str(r.get("note_number", "")).strip()):
        errs.append("missing printed_page or note_number")
    if r.get("verification_status") not in ADMISSIBLE_STATUS:
        errs.append(f"verification_status {r.get('verification_status')!r} not admissible")
    if r.get("bank_key") not in cohort:
        errs.append("bank_key not in cohort")
    errs += check_scope(r)
    try:
        y = int(r.get("financial_year", ""))
        if y not in C.STUDY_YEARS and r.get("variable") != "opening_assets":
            errs.append("financial_year outside 2013-2022")
    except ValueError:
        errs.append("financial_year not an integer")
    # File identity: recompute SHA-256 from the local bytes; check page and rendered image.
    sha = r.get("pdf_sha256", "")
    pdf_path = C.ROOT / r.get("local_pdf_path", "") if r.get("local_pdf_path") else None
    if sha and sha not in downloads:
        errs.append("pdf_sha256 does not match any downloaded report")
    if pdf_path is None or not pdf_path.is_file():
        errs.append("local PDF missing")
    elif verify_files:
        actual = _file_sha(pdf_path)
        if actual != sha:
            errs.append("local PDF bytes do not hash to the recorded pdf_sha256")
        elif sha in downloads and downloads[sha].get("sha256") != actual:
            errs.append("download ledger hash differs from local PDF")
        try:
            pg = int(r.get("pdf_page_1_based", ""))
        except ValueError:
            pg = None
            errs.append("pdf_page_1_based not an integer")
        if pg is not None:
            try:
                n_pages = _page_count(pdf_path)
            except Exception:
                n_pages = None
                errs.append("local PDF unreadable")
            if n_pages is not None and not 1 <= pg <= n_pages:
                errs.append(f"pdf_page_1_based {pg} outside document")
            elif n_pages is not None:
                rp = r.get("rendered_page_path", "")
                img = C.ROOT / rp if rp else None
                if img is None or not img.is_file():
                    errs.append("rendered page image missing (page must be inspected)")
                else:
                    try:
                        same = _pixel_digest_of_png(img) == _pixel_digest_of_page(pdf_path, pg)
                    except Exception:
                        same = False
                    if not same:
                        errs.append("rendered page image does not correspond to the indicated PDF page")
    # Units and an explicit, justified sign transformation.
    try:
        derived = r.get("raw_value") == "derived"
        raw = None if derived else number(str(r.get("raw_value", "")).replace("%", "").strip())
        norm = number(r.get("normalised_value_ngnm_or_pct"))
        f = UNIT_FACTORS.get(r.get("raw_units", ""))
        st = r.get("sign_transform", "none") or "none"
        if st not in ("none", "expense_presented_negative"):
            errs.append(f"unknown sign_transform {st!r}")
        if st == "expense_presented_negative":
            if not SIGN_CONVERTIBLE.match(r.get("variable", "")):
                errs.append(f"sign transformation not permitted for {r.get('variable')}")
            if not str(r.get("sign_reason", "")).strip():
                errs.append("sign transformation without a recorded reason")
        if derived:
            if r.get("verification_status") != "derived_from_verified":
                errs.append("derived value not marked derived_from_verified")
            if not str(r.get("component_ids", "")).strip() or r.get("derive_formula") != "sum":
                errs.append("derived value without component_ids/derive_formula")
        elif f is None:
            errs.append(f"unknown raw_units {r.get('raw_units')!r}")
        elif raw is not None and norm is not None:
            mult = -1 if st == "expense_presented_negative" else 1
            if abs(mult * raw * f - norm) > 0.5 * f + 1e-9:
                if abs(abs(raw) * f - abs(norm)) <= 0.5 * f + 1e-9:
                    errs.append("unexplained sign reversal between raw and normalised value")
                else:
                    errs.append("normalised value does not match raw value x unit factor")
    except ValueError:
        errs.append("non-numeric raw or normalised value")
    return errs


def check_derived(r: dict, accepted_by_id: dict[str, dict]) -> list[str]:
    """Independently recompute a derived admission from its accepted component evidence."""
    errs = []
    ids = [c.strip() for c in str(r.get("component_ids", "")).split(";") if c.strip()]
    comps = [accepted_by_id.get(i) for i in ids]
    if not ids or any(c is None for c in comps):
        return [f"components not accepted: {[i for i, c in zip(ids, comps) if c is None]}"]
    for c in comps:
        if c["bank_key"] != r["bank_key"] or c["financial_year"] != r["financial_year"]:
            errs.append(f"component {c['evidence_id']} has different entity/year")
        if c["reporting_version"] != r["reporting_version"]:
            errs.append(f"component {c['evidence_id']} has different reporting version")
        if c.get("column_scope") != r.get("column_scope"):
            errs.append(f"component {c['evidence_id']} has different column scope")
        money = lambda u: u not in ("percent", "indicator")
        if money(c["raw_units"]) != money(r["raw_units"]):
            errs.append(f"component {c['evidence_id']} has incompatible units")
    total = sum(number(c["normalised_value_ngnm_or_pct"]) for c in comps)
    if abs(total - number(r["normalised_value_ngnm_or_pct"])) > 1e-6:
        errs.append(f"declared sum {r['normalised_value_ngnm_or_pct']} != recomputed {total}")
    return errs


def run() -> dict:
    ensure_admissions_template()
    baseline = read_csv(C.SELECTED_CSV)
    cohort = {r["bank"]: r for r in read_csv(C.TASKS / "cohort.csv")}
    dl = read_json(C.STATE / "download_state.json", {}).get("reports", {})
    downloads = {v["sha256"]: v for v in dl.values() if v.get("status") == "downloaded"}
    fieldnames = list(baseline[0].keys())
    baseline_keys = {(r["bank"], int(r["year"])) for r in baseline}
    panel = {(r["bank"], int(r["year"])): dict(r) for r in baseline}
    if len(panel) != len(baseline):
        raise SystemExit("Duplicate bank-year keys in baseline")
    changes: list[dict] = []
    review: list[dict] = []
    conflicts: list[dict] = []

    # 1. Admission control
    accepted: dict[tuple[str, int, str], dict] = {}
    accepted_by_id: dict[str, dict] = {}
    adm_rows = [r for r in read_csv(ADMISSIONS) if str(r.get("admit", "")).strip().lower() in ("1", "yes", "true")]
    adm_rows.sort(key=lambda r: r.get("raw_value") == "derived")  # components before derived values
    for r in adm_rows:
        errs = check_admission(r, downloads, cohort)
        if r.get("raw_value") == "derived" and not errs:
            errs += check_derived(r, accepted_by_id)
        key = (r.get("bank_key", ""), int(r["financial_year"]) if str(r.get("financial_year", "")).isdigit() else -1, r.get("variable", ""))
        if not errs and key in accepted and not same(number(accepted[key]["normalised_value_ngnm_or_pct"]), number(r["normalised_value_ngnm_or_pct"])):
            errs.append("conflicts with another admitted value for the same bank/year/variable")
            conflicts.append({"type": "admission_conflict", "bank": key[0], "year": key[1], "field": key[2],
                              "value_a": accepted[key]["normalised_value_ngnm_or_pct"],
                              "value_b": r["normalised_value_ngnm_or_pct"], "detail": "two admitted values differ"})
        review.append({**{k: r.get(k, "") for k in ("evidence_id", "bank_key", "financial_year", "variable", "normalised_value_ngnm_or_pct")},
                       "accepted": not errs, "errors": "; ".join(errs)})
        if not errs:
            accepted_by_id[r["evidence_id"]] = r
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
                    row[v] = panel_value(r)
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
        scopes = {fields[c].get("column_scope", "") for c in CORE if c in fields}
        bal_ok = False
        if core_ok:
            a, l, e = (number(fields[c]["normalised_value_ngnm_or_pct"]) for c in ("assets", "liabilities", "equity"))
            unit = max(UNIT_FACTORS.get(fields[c]["raw_units"], 1.0) for c in ("assets", "liabilities", "equity"))
            bal_ok = abs(a - l - e) <= tolerance(3, unit)
        if core_ok and len(versions) == 1 and len(scopes) == 1 and bal_ok:
            row = {k: "" for k in fieldnames}
            row.update({"bank": b, "year": y, "tier": cohort[b]["analytical_tier"],
                        "regime": "IAS 39" if y < C.ADOPTION_YEAR else "IFRS 9",
                        "origin": "Admitted this run", "scope": SCOPE_LABEL.get(next(iter(scopes)), "Standalone operating bank"),
                        "version_note": next(iter(versions)),
                        "source_url": fields["assets"]["source_url"]})
            for v, r in fields.items():
                if v in fieldnames:
                    row[v] = panel_value(r)
            panel[(b, y)] = row
            admitted_new_rows.append(f"{b} {y}")
            changes.append({"bank": b, "year": y, "field": "*row*", "old": "", "new": "added", "kind": "new_bank_year",
                            "basis": ";".join(r["evidence_id"] for r in fields.values()), "reason": "core set admitted and reconciled"})
        else:
            partial_new.append({"bank": b, "year": y, "admitted_fields": ";".join(sorted(fields)),
                                "core_complete": core_ok, "single_version": len(versions) == 1 and len(scopes) <= 1, "balance_ok": bal_ok})

    # 3. Recompute derived ratios from eligible inputs only.
    recompute_diffs = 0
    for (b, y), row in panel.items():
        calc = calculate(row)
        # Liquidity is used only with an explicit admissibility flag of 1.
        flag = number(row.get("liquidity_admissible"))
        row["liquidity_used"] = row.get("liquidity", "") if flag == 1 else ""
        for f, new in calc.items():
            old = number(row.get(f))
            if not same(old, new) and (b, y) in baseline_keys:
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

    ev = E.inherited()
    adm_ev = [{**r, "evidence_origin": "admissions.csv"} for r in accepted.values()]
    alt_path = C.DATA / "review" / "source_alternatives.csv"
    alternatives = read_csv(alt_path) if alt_path.is_file() else []
    idx = E.backing_index(ev + adm_ev)
    rc_path = C.DATA / "review" / "reviewer_conflicts.csv"
    reviewer_conflicts = read_csv(rc_path) if rc_path.is_file() else []
    documented = {(c["bank"], int(c["year"]), c["field"]): c for c in reviewer_conflicts
                  if c["type"] in ("source_internal_inconsistency",)}

    def status_for(passed: bool, b, y, fields) -> tuple[str, str]:
        if passed:
            return "pass", ""
        for f in fields:
            if (b, y, f) in documented:
                return "documented_source_exception", documented[(b, y, f)]["detail"][:200]
        return "fail", ""

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
            literal, ev_id = printed_literal(idx.get((b, y, "car"), []), row.get("car"))
            tol, why = car_tolerance(literal if literal is not None else row.get("car"),
                                     number(row.get("regulatory_capital")), number(row.get("rwa")),
                                     rounding_unit_ngnm(row.get("regulatory_capital"), row.get("rwa")))
            why += f"; printed literal {literal!r} from {ev_id}" if literal is not None else "; no evidence literal - stored value precision used"
            checks.append({"bank": b, "year": y, "check": "reported CAR vs capital/RWA", "residual": round(car - cc, 4),
                           "tolerance": round(tol, 6), "rounding_unit_ngnm": "", "passed": abs(car - cc) <= tol,
                           "note": f"{why}; basis={row.get('car_basis','')}; transitional={row.get('car_transitional','')}"})
    for c in checks:
        fields = {"assets = liabilities + equity": ("assets", "liabilities", "equity"),
                  "gross loans - allowance = net loans": ("gross_loans", "loan_allowance", "net_loans"),
                  "reported CAR vs capital/RWA": ("car", "regulatory_capital", "rwa")}[c["check"]]
        c["status"], c["exception_detail"] = status_for(bool(c["passed"]), c["bank"], c["year"], fields)

    # 4b. Average-asset denominators: opening assets vs the prior-year closing assets in the panel.
    denom = []
    for (b, y), row in sorted(panel.items()):
        oa, prev = number(row.get("opening_assets")), panel.get((b, y - 1))
        pa = number(prev.get("assets")) if prev else None
        if oa is None or pa is None:
            continue
        denom.append({"bank": b, "year": y, "opening_assets": oa, "prior_year_closing_assets": pa,
                      "difference": round(oa - pa, 6), "compatible": abs(oa - pa) <= 0.5,
                      "opening_version": (accepted.get((b, y, "opening_assets")) or {}).get("reporting_version", "baseline/inherited"),
                      "prior_closing_version": (accepted.get((b, y - 1, "assets")) or {}).get("reporting_version", prev.get("version_note", "baseline/inherited"))})

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
                alias_recs, label = E.alias_match(v, f, b, y, idx)
                if label:
                    recs, how = alias_recs, label
            if not how:
                comp_recs, label = E.component_match(v, f, b, y, idx)
                if label:
                    recs, how = comp_recs, label
            backing.append({"bank": b, "year": y, "field": f, "value": v,
                            "evidence_records": len(recs), "value_matches_evidence": bool(how), "match_basis": how,
                            "qualification": E.QUALIFICATIONS.get((b, y, f), ""),
                            "evidence_ids": ";".join(r["evidence_id"] for r in recs[:6])})
    # Inherited evidence that disagrees internally for one bank/year/variable.
    for (b, y, f), recs in idx.items():
        vals = sorted({number(r["normalised_value_ngnm_or_pct"]) for r in recs
                       if _num_ok(r["normalised_value_ngnm_or_pct"])} - {None})
        if len(vals) > 1 and (vals[-1] - vals[0]) > 0.5:
            conflicts.append({"type": "evidence_alternatives", "bank": b, "year": y, "field": f,
                              "value_a": vals[0], "value_b": vals[-1],
                              "detail": "; ".join(f"{r['evidence_id']}={r['normalised_value_ngnm_or_pct']} [{r['review_reason'][:70]}]" for r in recs[:4])})

    conflicts += reviewer_conflicts
    cands = K.load()
    conflicts += K.compare(cands, panel)
    write_csv(C.DATA / "candidates.csv", cands,
              ["bank", "year", "field", "value", "candidate_source", "locator", "status", "note"])
    write_csv(C.DATA / "conflicts.csv", conflicts, ["type", "bank", "year", "field", "value_a", "value_b", "detail"])
    # 7. Field-level status: keep reported, derived, restated, manual, inherited and recomputed values distinct.
    filled = {(c["bank"], c["year"], c["field"]) for c in changes if c["kind"] == "fill_blank"}
    corrected = {(c["bank"], c["year"], c["field"]) for c in changes if c["kind"] == "correction"}
    exc_fields = {(c["bank"], int(c["year"]), c["field"]): c["type"] for c in reviewer_conflicts}
    field_status = []
    for (b, y), row in sorted(panel.items()):
        for f in PANEL_VALUE_FIELDS + DERIVED:
            v = row.get(f, "")
            if not str(v).strip():
                continue
            adm = accepted.get((b, y, f))
            if f in DERIVED and f not in PANEL_VALUE_FIELDS:
                basis, version = "recomputed_ratio", ""
            elif adm is not None and ((b, y) not in baseline_keys or (b, y, f) in filled or (b, y, f) in corrected):
                basis = adm.get("value_basis", "reported")
                if "restated" in adm.get("original_or_comparative", "").lower():
                    basis += "+restated_comparative"
                version = adm.get("reporting_version", "")
            else:
                basis, version = "baseline_inherited", row.get("version_note", "")
            field_status.append({"bank": b, "year": y, "field": f, "value": v, "value_basis": basis,
                                 "change_kind": "fill_blank" if (b, y, f) in filled else "correction" if (b, y, f) in corrected
                                 else "new_row" if (b, y) not in baseline_keys and f not in DERIVED else "",
                                 "reporting_version": version, "evidence_id": adm.get("evidence_id", "") if adm else "",
                                 "exception_flag": exc_fields.get((b, y, f), "")})
    write_csv(C.DATA / "field_status.csv", field_status)
    write_csv(C.DATA / "denominator_compatibility.csv", denom)
    out_fields = fieldnames + [c for c in ("liquidity_used",) if c not in fieldnames]
    rows = [panel[k] for k in sorted(panel)]
    write_csv(C.DATA / "verified_panel.csv", rows, out_fields)
    write_csv(C.DATA / "change_register.csv", changes, ["bank", "year", "field", "old", "new", "kind", "basis", "reason"])
    write_csv(C.DATA / "admission_review.csv", review)
    write_csv(C.DATA / "partial_new_bank_years.csv", partial_new,
              ["bank", "year", "admitted_fields", "core_complete", "single_version", "balance_ok"])
    write_csv(C.DATA / "reconciliation_checks.csv", checks,
              ["bank", "year", "check", "residual", "tolerance", "rounding_unit_ngnm", "passed", "status", "exception_detail", "note"])
    write_csv(C.DATA / "exceptions_register.csv", exc, ["id", "bank", "year", "field", "expected", "actual", "status", "rule"])
    write_csv(C.DATA / "evidence_backing.csv", backing)
    alt_ev = [{**a, "evidence_origin": "review/source_alternatives.csv"} for a in alternatives]
    write_csv(C.DATA / "evidence_long.csv", ev + adm_ev + alt_ev, E.EVIDENCE_COLUMNS)
    write_json(C.DATA / "validate_state.json", {
        "at": utcnow(), "admissions_reviewed": len(review), "admissions_accepted": len(accepted),
        "new_bank_years": admitted_new_rows, "partial_new": len(partial_new),
        "recompute_differences": recompute_diffs, "changes": len(changes),
        "exceptions_violated": [x["id"] for x in exc if x["status"] == "VIOLATED"],
    })
    return {"panel_rows": len(rows), "admissions_accepted": len(accepted), "new_bank_years": admitted_new_rows,
            "recompute_differences": recompute_diffs, "checks": len(checks),
            "checks_failed": sum(c["status"] == "fail" for c in checks),
            "checks_documented_exceptions": sum(c["status"] == "documented_source_exception" for c in checks),
            "exceptions_violated": [x["id"] for x in exc if x["status"] == "VIOLATED"],
            "fields_without_matching_evidence": sum(not b["value_matches_evidence"] for b in backing),
            "fields_checked_for_evidence": len(backing), "conflicts": len(conflicts)}


def panel_value(r: dict):
    """Percentages keep their printed precision ("20 %" stays "20") so rounding checks use it."""
    if r.get("raw_units") == "percent" and r.get("raw_value") not in ("", "derived"):
        return str(r["raw_value"]).replace("%", "").replace(",", "").strip()
    return number(r["normalised_value_ngnm_or_pct"])


def printed_literal(records: list[dict], stored) -> tuple[str | None, str]:
    """The printed CAR literal from the evidence record that supports the stored value."""
    v = number(stored)
    lit_path = C.DATA / "review" / "printed_literals.csv"
    overrides = {o["evidence_id"]: o["printed_literal"] for o in read_csv(lit_path)} if lit_path.is_file() else {}
    for r in records:
        raw = str(overrides.get(r.get("evidence_id"), r.get("raw_value", ""))).replace("%", "").strip()
        try:
            if raw and raw != "derived" and v is not None and abs(number(raw) - v) < 1e-9:
                return raw, r.get("evidence_id", "")
        except ValueError:
            continue
    return None, ""


def car_tolerance(printed, capital: float | None, rwa: float | None, unit: float) -> tuple[float, str]:
    """Half the printed display step of the CAR, plus the effect of rounding capital and RWA.
    Derived from each value's own displayed precision; no global widening."""
    from .ratios import decimals
    d = decimals(printed)
    display = 0.5 * 10 ** (-d)
    inputs = 0.0
    if capital and rwa:
        inputs = 100 * (0.5 * unit / rwa + capital * 0.5 * unit / rwa ** 2)
    return display + inputs + 1e-9, f"display precision {d} dp (+/-{display}) + input rounding {inputs:.2e}"


def _num_ok(v) -> bool:
    try:
        return number(v) is not None
    except ValueError:
        return False
