"""Descriptive and model-readiness diagnostics (Phase 6). No thesis regressions are estimated here.

All samples come from eligibility.sample(); outputs go to outputs/readiness/ and are summarised in readiness.md.
"""
from __future__ import annotations

import statistics as st
from collections import defaultdict

from . import config as C
from . import eligibility as E
from .util import number, write_csv

OUT = C.OUTPUTS / "readiness"
CONTINUOUS = ["car", "car_computed", "roa", "eqta", "ocf_ratio", "allr", "impairment_assets", "npl_calc",
              "broad_coverage", "stage3_coverage", "liquidity", "leverage"]
MIN_PER_PERIOD_VOL = 3   # sample SD needs >= 3 observations per regime to be informative
MIN_BANKS_BOTH = 6       # banks observed in both regimes needed for a within-bank comparison
CONTROLS = ["ln_assets", "leverage"]  # candidate controls (k counted below)

# Research objectives inferred from the study title and dataset variables; map to the thesis's own wording before use.
OBJECTIVES = [
    ("O1", "Effect of IFRS 9 adoption on loan-loss provisioning", ["allr", "impairment_assets", "broad_coverage", "npl_calc", "stage3_coverage"]),
    ("O2", "Effect of IFRS 9 adoption on capital adequacy", ["car", "car_computed"]),
    ("O3", "Effect of IFRS 9 adoption on profitability, cash generation and balance-sheet stability", ["roa", "ocf_ratio", "eqta", "leverage", "liquidity"]),
    ("O4", "Going-concern indicators before and after IFRS 9", ["gcu"]),
    ("O5", "Tier 1 versus Tier 2 differences in the IFRS 9 effect", ["allr", "car", "roa", "eqta"]),
    ("O6", "Change in volatility of key indicators after IFRS 9", ["roa", "car", "allr", "impairment_assets"]),
]


def _sd(x):
    return st.stdev(x) if len(x) >= 2 else None


def _vals(rows):
    return [float(r["value"]) for r in rows]


def build() -> dict:
    OUT.mkdir(parents=True, exist_ok=True)
    elig = E.load()
    trend, tiers, vol, within, sizes = [], [], [], [], []
    feas = {}
    for o in CONTINUOUS + ["gcu"]:
        inf = E.sample(o, "inferential", rows=elig)
        lon = E.sample(o, "longitudinal", rows=elig)
        by_bank = defaultdict(lambda: {0: [], 1: []})
        for r in inf:
            by_bank[(r["bank"], r["tier"])][int(r["ifrs9_d"])].append(float(r["value"]))
        both = {k: v for k, v in by_bank.items() if v[0] and v[1]}
        for (b, t), v in sorted(both.items()):
            trend.append({"outcome": o, "bank": b, "tier": t, "n_pre": len(v[0]), "n_post": len(v[1]),
                          "mean_pre": round(st.mean(v[0]), 4), "mean_post": round(st.mean(v[1]), 4),
                          "diff_post_minus_pre": round(st.mean(v[1]) - st.mean(v[0]), 4)})
        for t in ("Tier 1", "Tier 2"):
            for d, lab in ((0, "pre (IAS 39)"), (1, "post (IFRS 9)")):
                x = [float(r["value"]) for r in inf if r["tier"] == t and int(r["ifrs9_d"]) == d]
                tiers.append({"outcome": o, "tier": t, "period": lab, "n": len(x), "banks": len({r["bank"] for r in inf if r["tier"] == t and int(r["ifrs9_d"]) == d}),
                              "mean": round(st.mean(x), 4) if x else "", "median": round(st.median(x), 4) if x else "",
                              "sd": round(_sd(x), 4) if _sd(x) is not None else "", "min": min(x) if x else "", "max": max(x) if x else ""})
        lb = defaultdict(lambda: {0: [], 1: []})
        for r in lon:
            lb[(r["bank"], r["tier"])][int(r["ifrs9_d"])].append((int(r["year"]), float(r["value"])))
        nfeas = 0
        for (b, t), v in sorted(lb.items()):
            ok = len(v[0]) >= MIN_PER_PERIOD_VOL and len(v[1]) >= MIN_PER_PERIOD_VOL
            nfeas += ok
            vol.append({"outcome": o, "bank": b, "tier": t, "n_pre": len(v[0]), "years_pre": " ".join(str(y) for y, _ in sorted(v[0])),
                        "sd_pre": round(_sd([x for _, x in v[0]]), 4) if len(v[0]) >= 2 else "",
                        "n_post": len(v[1]), "years_post": " ".join(str(y) for y, _ in sorted(v[1])),
                        "sd_post": round(_sd([x for _, x in v[1]]), 4) if len(v[1]) >= 2 else "",
                        "feasible": ok, "units": "percent" if o != "gcu" else "indicator"})
        feas[o] = nfeas
        x = _vals(inf)
        if len(x) >= 3:
            means = defaultdict(list)
            for r in inf:
                means[r["bank"]].append(float(r["value"]))
            bm = {b: st.mean(v) for b, v in means.items()}
            dev = [float(r["value"]) - bm[r["bank"]] for r in inf]
            tot, wsd = _sd(x), _sd(dev)
            within.append({"outcome": o, "n": len(x), "banks": len(bm), "total_sd": round(tot, 4),
                           "between_sd": round(_sd(list(bm.values())), 4) if len(bm) >= 2 else "",
                           "within_sd": round(wsd, 4) if wsd is not None else "",
                           "within_share_of_variance": round((wsd / tot) ** 2, 3) if tot else "",
                           "banks_observed_both_regimes": len(both)})
        n, nb, n_both = len(inf), len({r["bank"] for r in inf}), len(both)
        t1 = {r["bank"] for r in inf if r["tier"] == "Tier 1"}; t2 = {r["bank"] for r in inf if r["tier"] == "Tier 2"}
        events = sum(float(r["value"]) == 1 for r in inf) if o == "gcu" else None
        for model, k, ok, note in [
            ("pooled OLS: y ~ IFRS9_D + Tier1 + ln_assets + leverage", 5, n >= 10 * 5, "cluster-robust SE by bank"),
            ("bank FE: y ~ IFRS9_D + ln_assets + leverage | bank", 3 + nb, n_both >= MIN_BANKS_BOTH and n - nb >= 10 * 3,
             f"identified from {n_both} banks observed in both regimes"),
            ("bank FE + year FE: y ~ IFRS9_D | bank + year", None, False,
             "NOT IDENTIFIED: IFRS9_D = 1{year>=2018} is an exact linear combination of the year dummies"),
            ("DiD: y ~ Tier1 x Post | bank + year", 1 + nb + 9, len(t1 & {b for (b, _) in both}) >= 2 and len(t2 & {b for (b, _) in both}) >= 2 and n >= 40,
             f"Tier 1 banks in both regimes: {len(t1 & {b for (b, _) in both})}; Tier 2: {len(t2 & {b for (b, _) in both})}; few clusters -> wild cluster bootstrap"),
        ] + ([("logit: gcu ~ IFRS9_D (+ covariates)", 2, (events or 0) >= 10 * 2,
               f"{events} positive events; events per parameter {round((events or 0) / 2, 1)}; multivariable model needs >= 10 events per parameter")] if o == "gcu" else []):
            sizes.append({"outcome": o, "model": model, "N": n, "banks": nb, "parameters": k if k else "",
                          "obs_per_parameter": round(n / k, 1) if k else "", "feasible": ok, "note": note})
    write_csv(OUT / "trend_matched_pre_post.csv", trend, list(trend[0].keys()))
    write_csv(OUT / "tier_comparison.csv", tiers, list(tiers[0].keys()))
    write_csv(OUT / "volatility_feasibility.csv", vol, list(vol[0].keys()))
    write_csv(OUT / "within_bank_variation.csv", within, list(within[0].keys()))
    write_csv(OUT / "model_sample_sizes.csv", sizes, list(sizes[0].keys()))
    rec, objectives = recommend(sizes, feas, elig)
    write_csv(OUT / "estimator_recommendations.csv", rec, list(rec[0].keys()))
    write_csv(OUT / "objective_readiness.csv", objectives, list(objectives[0].keys()))
    (OUT / "readiness.md").write_text(render(rec, objectives, sizes), encoding="utf-8")
    return {"outcomes": len(CONTINUOUS) + 1, "estimators": len(rec), "objectives": len(objectives)}


def recommend(sizes, feas, elig):
    by = defaultdict(dict)
    for s in sizes:
        by[s["outcome"]][s["model"].split(":")[0]] = s
    rec = []
    for o in CONTINUOUS + ["gcu"]:
        m = by[o]
        n = m["pooled OLS"]["N"]
        if o == "gcu":
            lg = m["logit"]
            est = ("descriptive only: event counts by regime and tier; exact (Fisher) comparison of event shares; "
                   "no multivariable model" if not lg["feasible"] else "penalised (Firth) logit")
            status = "descriptive"
        elif m["bank FE"]["feasible"]:
            est = ("bank fixed effects with IFRS9_D (no year FE: collinear) and macro controls instead; bank-clustered SEs with "
                   "wild cluster bootstrap (few clusters); robustness: pooled OLS, drop fallback rows")
            status = "testable"
        elif n >= 20 and m["pooled OLS"]["N"] >= 20:
            est = "pooled OLS with cluster-robust SEs as exploratory only; report matched pre/post bank means"
            status = "exploratory"
        else:
            est = "descriptive only (too few eligible observations / banks observed in both regimes)"
            status = "descriptive"
        did = m.get("DiD", {})
        rec.append({"outcome": o, "eligible_n": n, "banks": m["pooled OLS"]["banks"],
                    "status": status, "recommended_estimator": est,
                    "tier_did_feasible": did.get("feasible", False), "volatility_banks_feasible": feas.get(o, 0),
                    "collinearity_warning": "IFRS9_D is perfectly collinear with a full set of year fixed effects"})
    status = {r["outcome"]: r for r in rec}
    objectives = []
    for oid, label, outs in OBJECTIVES:
        if oid == "O5":
            ok = [o for o in outs if status[o]["tier_did_feasible"]]
        elif oid == "O6":
            ok = [o for o in outs if status[o]["volatility_banks_feasible"] >= MIN_BANKS_BOTH]
        else:
            ok = [o for o in outs if status[o]["status"] == "testable"]
        objectives.append({"objective": oid, "description": label, "outcomes": ";".join(outs),
                           "statistically_testable_outcomes": ";".join(ok),
                           "descriptive_only_outcomes": ";".join(o for o in outs if o not in ok),
                           "readiness": ("exploratory test only (bank-level SDs from >=3 observations per regime)" if oid == "O6" and ok
                                         else "testable" if ok else "descriptive only"),
                           "note": "objective wording inferred from the study title and variables; confirm against the thesis"})
    return rec, objectives


def render(rec, objectives, sizes) -> str:
    L = ["# Model readiness (no thesis regressions run)", "",
         "Generated from `data/outcome_eligibility.csv` via `ifrs9_recovery.eligibility.sample()`.", "",
         "## Collinearity warning", "",
         "IFRS9_D = 1 for 2018-2022 is an exact linear combination of the year dummies. A specification with IFRS9_D and a full set "
         "of year fixed effects is not identified. Use bank fixed effects with time-varying macro controls, or identify a "
         "differential effect (e.g. Tier 1 x Post) with bank and year fixed effects.", "",
         "With 12 banks the number of clusters is small: report wild-cluster-bootstrap inference.", "",
         "## Recommended estimator by outcome", "",
         "| Outcome | Eligible N | Banks | Status | Tier DiD feasible | Banks with volatility feasible | Recommended estimator |", "|---|---|---|---|---|---|---|"]
    L += [f"| {r['outcome']} | {r['eligible_n']} | {r['banks']} | {r['status']} | {r['tier_did_feasible']} | {r['volatility_banks_feasible']} | {r['recommended_estimator']} |" for r in rec]
    L += ["", "## Objectives", "", "| Objective | Testable outcomes | Descriptive only | Readiness |", "|---|---|---|---|"]
    L += [f"| {o['objective']} {o['description']} | {o['statistically_testable_outcomes'] or '-'} | {o['descriptive_only_outcomes'] or '-'} | {o['readiness']} |" for o in objectives]
    L += ["", "Objective wording is inferred from the study title and dataset variables; map it onto the thesis's own objectives.", "",
          "## Files", "", "- trend_matched_pre_post.csv, tier_comparison.csv, volatility_feasibility.csv, within_bank_variation.csv,",
          "  model_sample_sizes.csv, estimator_recommendations.csv, objective_readiness.csv"]
    return "\n".join(L) + "\n"
