"""Ratio definitions (unchanged from the starting pack) and reconciliation tolerances."""
from __future__ import annotations

import math
from decimal import Decimal

from .util import number

DERIVED = ["average_assets", "roa", "eqta", "ocf_ratio", "allr", "car_computed", "impairment_assets",
           "broad_coverage", "npl_calc", "stage3_ratio", "stage3_coverage", "roa_closing", "leverage",
           "ln_assets", "balance_residual", "loan_residual"]

DEFINITIONS = {
    "average_assets": "(matched opening assets + closing assets) / 2; both positive",
    "roa": "ROA_avg_pct = 100 * PAT / average_assets",
    "eqta": "equity_assets_pct = 100 * equity / closing assets",
    "ocf_ratio": "OCF_avgassets_pct = 100 * OCF / average_assets",
    "allr": "allowance_grossloans_pct = 100 * customer-loan allowance / gross customer loans",
    "car_computed": "CAR_calc_pct = 100 * regulatory capital / RWA",
    "impairment_assets": "100 * total income-statement impairment / average_assets (broad measure)",
    "broad_coverage": "broad_NPL_coverage_pct = 100 * total customer-loan allowance / NPL amount (not NPL-specific)",
    "npl_calc": "NPL_ratio_pct = 100 * regulatory NPL amount / matched gross loans",
    "stage3_ratio": "100 * Stage 3 gross / gross loans (not a regulatory NPL ratio)",
    "stage3_coverage": "Stage3_coverage_pct = 100 * Stage 3 allowance / Stage 3 gross",
    "roa_closing": "100 * PAT / closing assets (diagnostic; not a substitute for roa)",
    "leverage": "leverage_pct = 100 * liabilities / assets",
    "ln_assets": "ln(closing assets, NGN million)",
    "balance_residual": "assets - liabilities - equity (NGN million)",
    "loan_residual": "gross loans - loan allowance - net loans (NGN million)",
}


def pct(n: float | None, d: float | None) -> float | None:
    """Null (never infinite) when either input is missing or the denominator is not positive."""
    return 100 * n / d if n is not None and d is not None and d > 0 else None


def calculate(row: dict) -> dict[str, float | None]:
    g = lambda k: number(row.get(k))
    a, o, e, l, p, cf = g("assets"), g("opening_assets"), g("equity"), g("liabilities"), g("pat"), g("ocf")
    gl, al, nl = g("gross_loans"), g("loan_allowance"), g("net_loans")
    avg = (a + o) / 2 if a is not None and o is not None and a > 0 and o > 0 else None
    return {
        "average_assets": avg, "roa": pct(p, avg), "eqta": pct(e, a), "ocf_ratio": pct(cf, avg),
        "allr": pct(al, gl), "car_computed": pct(g("regulatory_capital"), g("rwa")),
        "impairment_assets": pct(g("total_impairment"), avg), "broad_coverage": pct(al, g("npl_amount")),
        "npl_calc": pct(g("npl_amount"), gl), "stage3_ratio": pct(g("stage3_gross"), gl),
        "stage3_coverage": pct(g("stage3_allowance"), g("stage3_gross")), "roa_closing": pct(p, a),
        "leverage": pct(l, a), "ln_assets": math.log(a) if a is not None and a > 0 else None,
        "balance_residual": a - l - e if None not in (a, l, e) else None,
        "loan_residual": gl - al - nl if None not in (gl, al, nl) else None,
    }


def decimals(value) -> int:
    s = str(value).strip()
    if not s or "e" in s.lower():
        return 0
    d = Decimal(s.replace(",", ""))
    return max(0, -d.as_tuple().exponent)


def rounding_unit_ngnm(*values) -> float:
    """Infer the source rounding unit in NGN million from recorded decimals.

    Values carried from NGN'000 sources have three decimals (unit 0.001m); whole
    numbers imply NGN-million rounding (unit 1m). Float artefacts beyond three
    decimals are treated as thousand-level precision.
    """
    ds = [min(decimals(v), 3) for v in values if str(v).strip()]
    return 10 ** (-max(ds)) if ds else 1.0


def tolerance(n_components: int, unit: float) -> float:
    """Half a rounding unit per independently rounded component."""
    return 0.5 * unit * n_components + 1e-9


def same(a: float | None, b: float | None) -> bool:
    if a is None or b is None:
        return a is None and b is None
    return math.isclose(a, b, rel_tol=1e-10, abs_tol=1e-7)
