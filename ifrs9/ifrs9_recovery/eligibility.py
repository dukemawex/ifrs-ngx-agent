"""Single analytical-eligibility ruleset shared by the summary, workbook, analysis exports and readiness tables.

For each (bank-year, outcome) the uses are kept distinct:
  available         - a value exists in the selected panel (unknown going concern is never available as 0);
  descriptive_use   - may be shown in descriptive tables/charts (with qualifiers where a rule applies);
  longitudinal_use  - may enter within-bank change / trend comparisons;
  change_comparable - the change from the previous year is valid (both years longitudinal, no break);
  inferential_use   - may enter pooled tests and models (primary sample);
  sensitivity_drop  - row is primary but must be dropped in a robustness check (fallback presentations).

Rules come from data/review/eligibility_rules.csv (curated, each with reason and source register) and from
machine-readable flags: panel allowance_pool_status, panel liquidity_admissible, field_status exception flags,
row_versions fallback classes and unreconciled version mixes. Every consumer must call sample()/load();
nothing else may decide eligibility.
"""
from __future__ import annotations

from collections import defaultdict

from . import config as C
from .util import number, read_csv, write_csv

OUTCOMES = {
    "gcu": ("gcu", ["gcu"], "Going-concern uncertainty (auditor material-uncertainty section or GC emphasis = 1)"),
    "car": ("car", ["car"], "Reported CAR, full-impact basis where both are printed (%)"),
    "car_computed": ("car_computed", ["regulatory_capital", "rwa"], "Regulatory capital / RWA (%)"),
    "roa": ("roa", ["pat", "assets", "opening_assets"], "PAT / average assets (%)"),
    "eqta": ("eqta", ["equity", "assets"], "Equity / total assets (%)"),
    "ocf_ratio": ("ocf_ratio", ["ocf", "assets", "opening_assets"], "Operating cash flow / average assets (%)"),
    "allr": ("allr", ["loan_allowance", "gross_loans"], "Customer-loan allowance / gross customer loans (%)"),
    "impairment_assets": ("impairment_assets", ["total_impairment", "assets", "opening_assets"], "Total impairment / average assets (%)"),
    "npl_calc": ("npl_calc", ["npl_amount", "gross_loans"], "NPL amount / gross loans (%)"),
    "broad_coverage": ("broad_coverage", ["loan_allowance", "npl_amount"], "Total loan allowance / NPL amount (%)"),
    "stage3_coverage": ("stage3_coverage", ["stage3_allowance", "stage3_gross"], "Stage 3 allowance / Stage 3 gross (%)"),
    "liquidity": ("liquidity_used", ["liquidity_used"], "Liquidity ratio used (%)"),
    "leverage": ("leverage", ["liabilities", "assets"], "Liabilities / assets (%)"),
}
EXCLUDING_FLAGS = {"source_internal_inconsistency"}
COLUMNS = ["bank", "year", "tier", "regime", "ifrs9_d", "outcome", "value", "available", "descriptive_use",
           "longitudinal_use", "change_comparable", "inferential_use", "sensitivity_drop", "excluded_uses",
           "rule_ids", "reasons", "fallback_class", "primary_version"]
PATH = C.DATA / "outcome_eligibility.csv"


def _rules() -> list[dict]:
    """Curated + machine-derived rules as dicts: bank, year, outcomes(set), excluded(set), break(bool), id, reason."""
    out = []
    for r in read_csv(C.DATA / "review" / "eligibility_rules.csv"):
        out.append({"bank": r["bank"], "year": r["year"], "outcomes": set(r["outcomes"].split(";")),
                    "excluded": {u for u in r["excluded_uses"].split(";") if u}, "break": r["break_before"] == "yes",
                    "id": r["rule_id"], "reason": r["reason"], "sens": False})
    panel = read_csv(C.DATA / "verified_panel.csv")
    for p in panel:
        if p.get("allowance_pool_status", "").lower().startswith("exclude"):
            out.append({"bank": p["bank"], "year": p["year"], "outcomes": {"allr", "broad_coverage"},
                        "excluded": {"inferential", "longitudinal"}, "break": False, "id": "AUTO-POOL",
                        "reason": f"panel allowance_pool_status: {p['allowance_pool_status']}", "sens": False})
        if str(p.get("liquidity_admissible", "")).strip() in ("0", "0.0"):
            out.append({"bank": p["bank"], "year": p["year"], "outcomes": {"liquidity"},
                        "excluded": {"inferential", "longitudinal", "descriptive"}, "break": False, "id": "AUTO-LIQ",
                        "reason": "panel liquidity_admissible = 0", "sens": False})
    for f in read_csv(C.DATA / "field_status.csv"):
        if f["exception_flag"] in EXCLUDING_FLAGS:
            outs = {o for o, (_, ins, _) in OUTCOMES.items() if f["field"] in ins}
            if outs:
                out.append({"bank": f["bank"], "year": f["year"], "outcomes": outs, "excluded": {"inferential"},
                            "break": False, "id": "AUTO-FLAG", "reason": f"{f['field']} flagged {f['exception_flag']}", "sens": False})
    rv_path = C.DATA / "row_versions.csv"
    for v in read_csv(rv_path) if rv_path.is_file() else []:
        if v["fallback_class"]:
            out.append({"bank": v["bank"], "year": v["year"], "outcomes": set(OUTCOMES), "excluded": set(),
                        "break": v["fallback_class"] == "fallback: labelled restatement", "id": "AUTO-FALLBACK",
                        "reason": f"{v['fallback_class']} (original-year report unavailable; source {v['primary_source']})", "sens": True})
        if v["version_mix_reconciliation"] == "UNRECONCILED":
            out.append({"bank": v["bank"], "year": v["year"], "outcomes": set(OUTCOMES), "excluded": {"inferential", "longitudinal"},
                        "break": True, "id": "AUTO-VERSIONMIX", "reason": f"unreconciled version mix: {v['version_mix']}", "sens": False})
    return out


def build() -> list[dict]:
    panel = read_csv(C.DATA / "verified_panel.csv")
    rv = {(v["bank"], v["year"]): v for v in read_csv(C.DATA / "row_versions.csv")} if (C.DATA / "row_versions.csv").is_file() else {}
    rules = defaultdict(list)
    for r in _rules():
        for o in r["outcomes"]:
            rules[(r["bank"], r["year"], o)].append(r)
    rows = []
    for p in panel:
        k = (p["bank"], p["year"])
        for o, (col, _, _) in OUTCOMES.items():
            val = number(p.get(col, ""))
            avail = val is not None
            rs = rules.get((*k, o), [])
            excl = set().union(*[r["excluded"] for r in rs]) if rs else set()
            rows.append({"bank": p["bank"], "year": p["year"], "tier": p["tier"], "regime": p["regime"],
                         "ifrs9_d": int(int(p["year"]) >= C.ADOPTION_YEAR), "outcome": o, "value": "" if val is None else val,
                         "available": avail, "descriptive_use": avail and "descriptive" not in excl,
                         "longitudinal_use": avail and "longitudinal" not in excl, "change_comparable": False,
                         "inferential_use": avail and "inferential" not in excl,
                         "sensitivity_drop": avail and any(r["sens"] for r in rs),
                         "excluded_uses": ";".join(sorted(excl)) if avail else "",
                         "rule_ids": ";".join(sorted({r["id"] for r in rs})), "reasons": " | ".join(dict.fromkeys(r["reason"] for r in rs)),
                         "fallback_class": rv.get(k, {}).get("fallback_class", ""), "primary_version": rv.get(k, {}).get("primary_version", ""),
                         "_break": any(r["break"] for r in rs)})
    idx = {(r["bank"], int(r["year"]), r["outcome"]): r for r in rows}
    for r in rows:
        prev = idx.get((r["bank"], int(r["year"]) - 1, r["outcome"]))
        r["change_comparable"] = bool(r["longitudinal_use"] and prev and prev["longitudinal_use"] and not r["_break"])
    for r in rows:
        r.pop("_break")
    write_csv(PATH, rows, COLUMNS)
    return rows


def _b(v) -> bool:
    return str(v) in ("True", "true", "1")


def load() -> list[dict]:
    rows = read_csv(PATH)
    for r in rows:
        for c in ("available", "descriptive_use", "longitudinal_use", "change_comparable", "inferential_use", "sensitivity_drop"):
            r[c] = _b(r[c])
    return rows


def sample(outcome: str, use: str = "inferential", drop_fallback: bool = False, rows: list[dict] | None = None) -> list[dict]:
    """The one accessor for analytical samples. use: descriptive | longitudinal | inferential | change."""
    rows = load() if rows is None else rows
    key = {"descriptive": "descriptive_use", "longitudinal": "longitudinal_use", "inferential": "inferential_use",
           "change": "change_comparable"}[use]
    return [r for r in rows if r["outcome"] == outcome and r[key] and not (drop_fallback and r["sensitivity_drop"])]


def summarise(rows: list[dict] | None = None) -> dict:
    rows = load() if rows is None else rows
    out = {}
    for o in OUTCOMES:
        rs = [r for r in rows if r["outcome"] == o]
        av = [r for r in rs if r["available"]]
        inf = [r for r in av if r["inferential_use"]]
        excl = [r for r in av if not r["inferential_use"]]
        out[o] = {"label": OUTCOMES[o][2], "panel_rows": len(rs), "available": len(av), "missing": len(rs) - len(av),
                  "descriptive": sum(r["descriptive_use"] for r in av), "longitudinal": sum(r["longitudinal_use"] for r in av),
                  "change_pairs": sum(r["change_comparable"] for r in av), "eligible": len(inf),
                  "excluded_from_inference": len(excl), "banks": len({r["bank"] for r in inf}),
                  "pre": sum(r["ifrs9_d"] in (0, "0") for r in inf), "post": sum(r["ifrs9_d"] in (1, "1") for r in inf),
                  "tier1": sum(r["tier"] == "Tier 1" for r in inf), "tier2": sum(r["tier"] == "Tier 2" for r in inf),
                  "fallback_rows_in_sample": sum(r["sensitivity_drop"] for r in inf),
                  "excluded_rows": [f"{r['bank']} {r['year']} ({r['rule_ids']})" for r in excl]}
    return out
