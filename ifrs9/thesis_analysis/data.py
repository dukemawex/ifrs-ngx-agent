"""Load the frozen release (read-only) after verifying every file against RELEASE_MANIFEST.json."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RELEASE_ID = "IFRS9_release_2026-10-11_v4"  # earlier results archived in thesis_results_v1/ (97), _v2/ (98), _v3/ (114)
REL = ROOT / "releases" / RELEASE_ID
OUT = ROOT / "thesis_results"
ADOPTION = 2018
COHORT_EXCLUDED = {"FCMB": "Formally excluded: a sufficiently consistent standalone First City Monument Bank Limited 2013-2022 "
                            "reporting series could not be established under the evidence verification protocol (no "
                            "bank-only statements; FCMB Group 'Company' column is the holding company). Not replaced."}
COHORT = ["Access", "Ecobank Nigeria", "Fidelity", "First Bank", "GTBank", "Stanbic", "Sterling", "UBA", "Union", "Unity", "Wema", "Zenith"]
YEARS = list(range(2013, 2023))

# outcome key -> (release source, label, short label, units)
OUTCOMES = {
    "allr": ("analysis/allowance_gross_loans.csv", "Loan-loss allowance / gross customer loans", "Allowance / gross loans", "%"),
    "impairment_assets": ("analysis/impairment_average_assets.csv", "Total impairment charge / average total assets", "Impairment / average assets", "%"),
    "car": ("analysis/car.csv", "Reported capital adequacy ratio (full-impact basis where both printed)", "CAR", "%"),
    "roa": ("analysis/roa.csv", "Profit after tax / average total assets", "ROA", "%"),
    "ocf_ratio": ("analysis/ocf_average_assets.csv", "Operating cash flow / average total assets", "OCF / average assets", "%"),
    "eqta": ("analysis/equity_assets.csv", "Total equity / total assets", "Equity / assets", "%"),
    "leverage": ("outcome_eligibility.csv", "Total liabilities / total assets", "Leverage", "%"),
    "npl_calc": ("analysis/npl_ratio.csv", "NPL amount / gross loans", "NPL ratio", "%"),
    "broad_coverage": ("analysis/broad_npl_coverage.csv", "Total loan allowance / NPL amount", "Broad NPL coverage", "%"),
    "stage3_coverage": ("analysis/stage3_coverage.csv", "Stage 3 allowance / Stage 3 gross exposure", "Stage 3 coverage", "%"),
    "liquidity": ("analysis/liquidity.csv", "Liquidity ratio used", "Liquidity ratio", "%"),
    "gcu": ("analysis/going_concern.csv", "Auditor material-uncertainty section or going-concern emphasis (1/0)", "Going-concern uncertainty", "indicator"),
}
CORE = ["allr", "impairment_assets", "car", "roa", "ocf_ratio", "eqta", "leverage"]
SPARSE = ["npl_calc", "broad_coverage", "stage3_coverage", "liquidity"]


def sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_release() -> dict:
    man = json.loads((REL / "RELEASE_MANIFEST.json").read_text())
    bad = {rel: meta["sha256"] for rel, meta in man["files"].items() if sha256(REL / rel) != meta["sha256"]}
    if bad:
        raise SystemExit(f"frozen release altered: {sorted(bad)[:5]}")
    return {"release_id": man["release_id"], "code_commit": man["code_commit"], "files_verified": len(man["files"])}


def _b(s: pd.Series) -> pd.Series:
    return s.astype(str).isin(["True", "true", "1"])


def panel() -> pd.DataFrame:
    p = pd.read_csv(REL / "verified_panel.csv")
    p["year"] = p["year"].astype(int)
    p["ifrs9_d"] = (p["year"] >= ADOPTION).astype(int)
    p["tier1"] = (p["tier"] == "Tier 1").astype(int)
    return p


def outcome(key: str) -> pd.DataFrame:
    """Descriptive-universe rows for one outcome with the frozen eligibility flags and controls joined."""
    src = OUTCOMES[key][0]
    d = pd.read_csv(REL / src)
    if src == "outcome_eligibility.csv":
        d = d[(d["outcome"] == key) & _b(d["descriptive_use"])].copy()
    for c in ("available", "descriptive_use", "longitudinal_use", "change_comparable", "inferential_use", "sensitivity_drop"):
        d[c] = _b(d[c])
    d["year"] = d["year"].astype(int)
    d["value"] = d["value"].astype(float)
    d["ifrs9_d"] = (d["year"] >= ADOPTION).astype(int)
    d["tier1"] = (d["tier"] == "Tier 1").astype(int)
    p = panel()[["bank", "year", "ln_assets", "equity", "assets", "regulatory_capital", "car", "gcu", "scope"]]
    p = p.rename(columns={c: f"p_{c}" for c in p.columns if c not in ("bank", "year")})
    d = d.merge(p, on=["bank", "year"], how="left", validate="one_to_one")
    d["ln_assets"] = d["p_ln_assets"]
    d["unity_negative_capital"] = (d["bank"] == "Unity") & ((d["p_equity"] < 0) | (d["p_car"] < 0) | (d["p_regulatory_capital"] < 0))
    d["documented_exception"] = ~d["inferential_use"]
    d["holdco_disclosure"] = d["p_scope"].fillna("").str.contains("HoldCo package")
    d["outcome"] = key
    assert set(d["bank"]) <= set(COHORT), set(d["bank"]) - set(COHORT)
    return d.sort_values(["bank", "year"]).reset_index(drop=True)


def all_outcomes() -> dict[str, pd.DataFrame]:
    return {k: outcome(k) for k in OUTCOMES}


def inferential(d: pd.DataFrame) -> pd.DataFrame:
    return d[d["inferential_use"]].copy()
