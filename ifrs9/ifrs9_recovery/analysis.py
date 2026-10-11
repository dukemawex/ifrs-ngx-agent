"""Outcome-specific analysis-ready datasets (Phase 5), built only through eligibility.sample()/load().

outputs/analysis/<name>.csv holds every selected bank-year with a value for that outcome (descriptive universe),
with the use flags, rule ids and the ratio inputs; filter on inferential_use for the primary inferential sample.
outputs/analysis/outcome_summary.csv reports N, banks, pre/post, Tier 1/2, missing rows, exclusions and version
restrictions per dataset. Counts are computed from the same rows that are written.
"""
from __future__ import annotations

from . import config as C
from . import eligibility as E
from .util import read_csv, write_csv

DATASETS = {  # file name -> (outcome, extra panel columns)
    "going_concern": ("gcu", []),
    "car": ("car", ["car_basis", "car_transitional", "car_minimum", "regulatory_capital", "rwa", "capital_transitional", "car_computed"]),
    "roa": ("roa", ["pat", "assets", "opening_assets", "average_assets"]),
    "equity_assets": ("eqta", ["equity", "assets"]),
    "ocf_average_assets": ("ocf_ratio", ["ocf", "assets", "opening_assets", "average_assets"]),
    "allowance_gross_loans": ("allr", ["loan_allowance", "gross_loans", "allowance_pool_status"]),
    "impairment_average_assets": ("impairment_assets", ["total_impairment", "assets", "opening_assets", "average_assets"]),
    "npl_ratio": ("npl_calc", ["npl_amount", "gross_loans", "npl_reported"]),
    "broad_npl_coverage": ("broad_coverage", ["loan_allowance", "npl_amount"]),
    "stage3_coverage": ("stage3_coverage", ["stage3_allowance", "stage3_gross"]),
    "liquidity": ("liquidity", ["liquidity_used", "liquidity_admissible", "liquidity_average", "liquidity_max", "liquidity_min"]),
}
FRAME = 130  # 13 banks x 10 years
OUT = C.OUTPUTS / "analysis"


def build() -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    elig = E.load()
    panel = {(r["bank"], r["year"]): r for r in read_csv(C.DATA / "verified_panel.csv")}
    summary, written = [], {}
    for name, (outcome, extra) in DATASETS.items():
        rows = []
        for r in E.sample(outcome, "descriptive", rows=elig):
            p = panel[(r["bank"], r["year"])]
            rows.append({**{k: r[k] for k in E.COLUMNS if k != "outcome"}, **{c: p.get(c, "") for c in extra}})
        cols = [c for c in E.COLUMNS if c != "outcome"] + extra
        write_csv(OUT / f"{name}.csv", rows, cols)
        inf = [r for r in rows if r["inferential_use"]]
        excl = [r for r in rows if not r["inferential_use"]]
        summary.append({
            "dataset": name, "outcome": outcome, "definition": E.OUTCOMES[outcome][2],
            "descriptive_n": len(rows), "eligible_n": len(inf), "banks": len({r["bank"] for r in inf}),
            "pre": sum(int(r["ifrs9_d"]) == 0 for r in inf), "post": sum(int(r["ifrs9_d"]) == 1 for r in inf),
            "tier1": sum(r["tier"] == "Tier 1" for r in inf), "tier2": sum(r["tier"] == "Tier 2" for r in inf),
            "change_pairs": sum(r["change_comparable"] for r in rows),
            "selected_rows_missing_value": len(panel) - len(rows), "frame_positions_missing": FRAME - len(rows),
            "excluded_from_inference": len(excl),
            "exclusion_reasons": " | ".join(f"{r['bank']} {r['year']}: {r['rule_ids']}" for r in excl),
            "fallback_rows_in_eligible": sum(r["sensitivity_drop"] for r in inf),
            "version_restrictions": ("primary sample includes fallback comparatives; drop rows with sensitivity_drop=True for "
                                     "the original-year-only sensitivity; never pair inputs from different versions "
                                     "(row_versions.csv)"),
        })
        written[name] = len(rows)
    write_csv(OUT / "outcome_summary.csv", summary, list(summary[0].keys()))
    return {"datasets": written, "summary_rows": len(summary)}
