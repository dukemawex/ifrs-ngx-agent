"""All thesis computations. Every function returns DataFrames that are written to thesis_results/ and later
re-read by the report, so each number in analysis_report.md traces to an exported file."""
from __future__ import annotations

import math

import numpy as np
import pandas as pd
from scipy import stats

from . import data as D
from . import econ as E

GROUPS = [("Full sample", None, None), ("Pre-IFRS 9 (2013-2017)", None, 0), ("Post-IFRS 9 (2018-2022)", None, 1),
          ("Tier 1", 1, None), ("Tier 2", 0, None), ("Tier 1 pre", 1, 0), ("Tier 1 post", 1, 1),
          ("Tier 2 pre", 0, 0), ("Tier 2 post", 0, 1)]


def _desc(x: pd.Series) -> dict:
    x = x.dropna()
    return {"N": len(x), "mean": x.mean() if len(x) else np.nan, "sd": x.std(ddof=1) if len(x) > 1 else np.nan,
            "min": x.min() if len(x) else np.nan, "p25": x.quantile(.25) if len(x) else np.nan,
            "median": x.median() if len(x) else np.nan, "p75": x.quantile(.75) if len(x) else np.nan,
            "max": x.max() if len(x) else np.nan}


# ---------------------------------------------------------------- 1. sample profile
def sample_profile(O: dict[str, pd.DataFrame]) -> dict[str, pd.DataFrame]:
    p = D.panel()
    rows = []
    for b in D.COHORT + ["FCMB"]:
        pb = p[p["bank"] == b]
        tier = pb["tier"].iloc[0] if len(pb) else "Tier 2"
        yrs = sorted(pb["year"])
        rows.append({"bank": b, "tier": tier, "cohort_status": "excluded (see note)" if b in D.COHORT_EXCLUDED else "included",
                     "selected_bank_years": len(yrs), "pre_2018": sum(y < D.ADOPTION for y in yrs), "post_2018": sum(y >= D.ADOPTION for y in yrs),
                     "years_selected": " ".join(map(str, yrs)), "years_missing": " ".join(str(y) for y in D.YEARS if y not in yrs) if b not in D.COHORT_EXCLUDED else "all (excluded)",
                     "note": D.COHORT_EXCLUDED.get(b, "")})
    cov = pd.DataFrame(rows)
    inc = cov[cov["cohort_status"] == "included"]
    cov = pd.concat([cov, pd.DataFrame([{"bank": "Total (12-bank cohort)", "tier": f"{(inc.tier == 'Tier 1').sum()} Tier 1 / {(inc.tier == 'Tier 2').sum()} Tier 2",
                                         "cohort_status": "", "selected_bank_years": inc.selected_bank_years.sum(),
                                         "pre_2018": inc.pre_2018.sum(), "post_2018": inc.post_2018.sum(),
                                         "years_selected": f"{inc.selected_bank_years.sum()} of {12 * len(D.YEARS)} frame positions", "years_missing": "", "note": ""}])], ignore_index=True)
    grid = p.pivot_table(index="bank", columns="year", values="tier", aggfunc="first").reindex(D.COHORT)
    elig = []
    for k, (src, label, short, units) in D.OUTCOMES.items():
        d = O[k]; inf = d[d["inferential_use"]]; exc = d[~d["inferential_use"]]
        elig.append({"outcome": k, "variable": short, "definition": label, "units": units,
                     "available_N": len(d), "eligible_N": len(inf), "excluded_N": len(exc),
                     "excluded_rows": "; ".join(f"{r.bank} {r.year} ({r.rule_ids})" for r in exc.itertuples()),
                     "banks": inf["bank"].nunique(), "pre": int((inf.ifrs9_d == 0).sum()), "post": int((inf.ifrs9_d == 1).sum()),
                     "tier1": int((inf.tier1 == 1).sum()), "tier2": int((inf.tier1 == 0).sum()),
                     "fallback_rows_in_eligible": int(inf["sensitivity_drop"].sum()),
                     "missing_in_selected_rows": len(p) - len(d), "missing_in_120_frame": 120 - len(d),
                     "analysis_role": "inferential models" if k in D.CORE else ("event description only" if k == "gcu" else "descriptive only (too sparse)"),
                     "source_file": f"releases/{D.RELEASE_ID}/{src}"})
    return {"coverage": cov, "grid": grid, "eligibility": pd.DataFrame(elig)}


# ---------------------------------------------------------------- 2. descriptives
def descriptives(O) -> pd.DataFrame:
    out = []
    for k in D.CORE + D.SPARSE + ["gcu"]:
        d = D.inferential(O[k])
        for g, t, r in GROUPS:
            s = d
            if t is not None: s = s[s.tier1 == t]
            if r is not None: s = s[s.ifrs9_d == r]
            out.append({"outcome": k, "variable": D.OUTCOMES[k][2], "group": g, "banks": s.bank.nunique(), **_desc(s["value"])})
    return pd.DataFrame(out)


def prepost(O) -> pd.DataFrame:
    out = []
    for k in D.CORE + D.SPARSE:
        d = D.inferential(O[k]); a, b = d[d.ifrs9_d == 0]["value"], d[d.ifrs9_d == 1]["value"]
        row = {"outcome": k, "variable": D.OUTCOMES[k][2], "N_pre": len(a), "N_post": len(b),
               "mean_pre": a.mean(), "mean_post": b.mean(), "diff_mean_post_minus_pre": b.mean() - a.mean(),
               "median_pre": a.median(), "median_post": b.median(), "diff_median": b.median() - a.median()}
        if len(a) > 1 and len(b) > 1:
            row["welch_t_p_naive"] = stats.ttest_ind(b, a, equal_var=False).pvalue
            row["mann_whitney_p_naive"] = stats.mannwhitneyu(b, a, alternative="two-sided").pvalue
        row["note"] = "pooled comparison ignores repeated bank observations; see matched_prepost.csv and regression_results.csv"
        out.append(row)
    return pd.DataFrame(out)


def tiers(O) -> pd.DataFrame:
    out = []
    for k in D.CORE + D.SPARSE:
        d = D.inferential(O[k])
        for lab, r in (("All years", None), ("Pre-IFRS 9", 0), ("Post-IFRS 9", 1)):
            s = d if r is None else d[d.ifrs9_d == r]
            a, b = s[s.tier1 == 1]["value"], s[s.tier1 == 0]["value"]
            row = {"outcome": k, "variable": D.OUTCOMES[k][2], "period": lab, "N_tier1": len(a), "banks_tier1": s[s.tier1 == 1].bank.nunique(),
                   "N_tier2": len(b), "banks_tier2": s[s.tier1 == 0].bank.nunique(),
                   "mean_tier1": a.mean(), "mean_tier2": b.mean(), "diff_mean_t1_minus_t2": a.mean() - b.mean(),
                   "median_tier1": a.median(), "median_tier2": b.median()}
            if len(a) > 1 and len(b) > 1:
                row["welch_t_p_naive"] = stats.ttest_ind(a, b, equal_var=False).pvalue
                row["mann_whitney_p_naive"] = stats.mannwhitneyu(a, b, alternative="two-sided").pvalue
            out.append(row)
        m = {(t, r): d[(d.tier1 == t) & (d.ifrs9_d == r)]["value"].mean() for t in (0, 1) for r in (0, 1)}
        out.append({"outcome": k, "variable": D.OUTCOMES[k][2], "period": "Difference-in-means (T1 change - T2 change)",
                    "diff_mean_t1_minus_t2": (m[(1, 1)] - m[(1, 0)]) - (m[(0, 1)] - m[(0, 0)])})
    return pd.DataFrame(out)


# ---------------------------------------------------------------- 3-5. trends, matched, volatility
def trends(O) -> tuple[pd.DataFrame, pd.DataFrame]:
    long, slopes = [], []
    for k in D.CORE:
        d = O[k]
        for r in d.itertuples():
            long.append({"outcome": k, "bank": r.bank, "tier": r.tier, "year": r.year, "value": r.value,
                         "inferential_use": r.inferential_use, "longitudinal_use": r.longitudinal_use, "rule_ids": r.rule_ids if isinstance(r.rule_ids, str) else ""})
        for (b, t), g in D.inferential(d)[lambda x: x.longitudinal_use].groupby(["bank", "tier"]):
            for lab, r in (("pre", 0), ("post", 1)):
                s = g[g.ifrs9_d == r]
                if len(s) >= 3:
                    sl = stats.linregress(s.year, s.value)
                    slopes.append({"outcome": k, "bank": b, "tier": t, "period": lab, "n": len(s), "years": " ".join(map(str, s.year)),
                                   "slope_pp_per_year": sl.slope, "first": s.value.iloc[0], "last": s.value.iloc[-1]})
    return pd.DataFrame(long), pd.DataFrame(slopes)


def matched(O) -> tuple[pd.DataFrame, pd.DataFrame]:
    banks, summ = [], []
    for k in D.CORE:
        d = D.inferential(O[k]); d = d[d.longitudinal_use]
        g = d.groupby(["bank", "tier", "ifrs9_d"])["value"].agg(["mean", "count"]).unstack("ifrs9_d")
        g = g.dropna()
        for (b, t), r in g.iterrows():
            banks.append({"outcome": k, "bank": b, "tier": t, "n_pre": int(r[("count", 0)]), "n_post": int(r[("count", 1)]),
                          "mean_pre": r[("mean", 0)], "mean_post": r[("mean", 1)], "diff_post_minus_pre": r[("mean", 1)] - r[("mean", 0)]})
        bk = pd.DataFrame([x for x in banks if x["outcome"] == k])
        for lab, sub in (("All matched banks", bk), ("Tier 1", bk[bk.tier == "Tier 1"]), ("Tier 2", bk[bk.tier == "Tier 2"])):
            diff = sub["diff_post_minus_pre"]
            row = {"outcome": k, "variable": D.OUTCOMES[k][2], "group": lab, "banks": len(sub), "mean_of_bank_pre_means": sub.mean_pre.mean(),
                   "mean_of_bank_post_means": sub.mean_post.mean(), "mean_diff": diff.mean(), "median_diff": diff.median(),
                   "banks_increase": int((diff > 0).sum()), "banks_decrease": int((diff < 0).sum())}
            if len(sub) >= 5:
                row["wilcoxon_signed_rank_p"] = stats.wilcoxon(diff).pvalue
                row["paired_t_p"] = stats.ttest_rel(sub.mean_post, sub.mean_pre).pvalue
                row["sign_test_p"] = stats.binomtest(int((diff > 0).sum()), int((diff != 0).sum())).pvalue
            row["compatibility"] = "same measurement definition both regimes; rows flagged non-comparable (longitudinal exclusions) removed"
            summ.append(row)
    return pd.DataFrame(banks), pd.DataFrame(summ)


def volatility(O) -> tuple[pd.DataFrame, pd.DataFrame]:
    banks, summ = [], []
    for k in D.CORE:
        d = D.inferential(O[k]); d = d[d.longitudinal_use]
        for (b, t), g in d.groupby(["bank", "tier"]):
            a, c = g[g.ifrs9_d == 0].value, g[g.ifrs9_d == 1].value
            if len(a) >= 3 and len(c) >= 3:
                f = c.var(ddof=1) / a.var(ddof=1) if a.var(ddof=1) > 0 else np.nan
                pf = 2 * min(stats.f.cdf(f, len(c) - 1, len(a) - 1), stats.f.sf(f, len(c) - 1, len(a) - 1)) if f == f else np.nan
                banks.append({"outcome": k, "bank": b, "tier": t, "n_pre": len(a), "years_pre": " ".join(map(str, g[g.ifrs9_d == 0].year)),
                              "sd_pre": a.std(ddof=1), "n_post": len(c), "years_post": " ".join(map(str, g[g.ifrs9_d == 1].year)),
                              "sd_post": c.std(ddof=1), "sd_ratio_post_pre": c.std(ddof=1) / a.std(ddof=1) if a.std(ddof=1) > 0 else np.nan,
                              "variance_ratio_F_p_exploratory": pf})
        bk = pd.DataFrame([x for x in banks if x["outcome"] == k])
        row = {"outcome": k, "variable": D.OUTCOMES[k][2], "banks_with_3_plus_each_regime": len(bk), "status": "EXPLORATORY (>=3 observations per regime per bank)"}
        if len(bk):
            lr = np.log(bk.sd_ratio_post_pre.replace(0, np.nan)).dropna()
            row.update({"median_sd_pre": bk.sd_pre.median(), "median_sd_post": bk.sd_post.median(), "median_sd_ratio": bk.sd_ratio_post_pre.median(),
                        "banks_sd_increase": int((bk.sd_post > bk.sd_pre).sum()), "banks_sd_decrease": int((bk.sd_post < bk.sd_pre).sum())})
            if len(lr) >= 5:
                row["wilcoxon_log_sd_ratio_p"] = stats.wilcoxon(lr).pvalue
        summ.append(row)
    return pd.DataFrame(banks), pd.DataFrame(summ)


# ---------------------------------------------------------------- 6. models
def design(d: pd.DataFrame, spec: str):
    """Return (X, y, names, absorbed) on the demeaned (bank FE) or raw (pooled) scale."""
    g = d["bank"].to_numpy()
    y = d["value"].to_numpy(float)
    post = d["ifrs9_d"].to_numpy(float); size = d["ln_assets"].to_numpy(float); t1 = d["tier1"].to_numpy(float)
    trend = (d["year"] - 2013).to_numpy(float)
    if spec == "M0":
        X = np.column_stack([np.ones(len(d)), post, t1]); names = ["const", "IFRS9_D", "Tier1"]
        return X, y, names, 0
    cols, names = [], []
    if spec in ("M1", "M2", "M3", "M5"):
        cols.append(post); names.append("IFRS9_D")
    if spec in ("M4", "M4s", "M5"):
        cols.append(t1 * post); names.append("Tier1_x_IFRS9_D")
    if spec in ("M2", "M4s"):
        cols.append(size); names.append("ln_assets")
    if spec == "M3":
        cols.append(trend); names.append("trend")
    if spec in ("M4", "M4s"):
        for yv in sorted(d["year"].unique())[1:]:
            cols.append((d["year"] == yv).to_numpy(float)); names.append(f"year_{yv}")
    X = E.demean(np.column_stack(cols), g)
    keep = X.std(axis=0) > 1e-12          # drop columns with no within variation
    X = X[:, keep]; names = [n for n, k in zip(names, keep) if k]
    return X, E.demean(y, g), names, d["bank"].nunique()


SPECS = {
    "M0": "Pooled OLS: y ~ IFRS9_D + Tier1 (bank-clustered; transparency only)",
    "M1": "Bank FE: y ~ IFRS9_D  [principal]",
    "M2": "Bank FE: y ~ IFRS9_D + ln(total assets)  [specification check]",
    "M3": "Bank FE: y ~ IFRS9_D + linear trend  [level shift relative to bank trend]",
    "M4": "Bank FE + year FE: y ~ Tier1 x IFRS9_D  [principal tier model; IFRS9_D absorbed by year FE]",
    "M4s": "Bank FE + year FE: y ~ Tier1 x IFRS9_D + ln(total assets)  [specification check]",
    "M5": "Bank FE: y ~ IFRS9_D + Tier1 x IFRS9_D  [Tier 2 effect + Tier 1 differential, no year FE]",
}
KEY_TERM = {"M0": "IFRS9_D", "M1": "IFRS9_D", "M2": "IFRS9_D", "M3": "IFRS9_D", "M4": "Tier1_x_IFRS9_D", "M4s": "Tier1_x_IFRS9_D", "M5": "Tier1_x_IFRS9_D"}


def estimate(d: pd.DataFrame, spec: str, bootstrap=True, B=E.B_DEFAULT):
    d = d.dropna(subset=["value", "ln_assets"]).reset_index(drop=True)
    X, y, names, absorbed = design(d, spec)
    res, info = E.fit(X, y, d["bank"].to_numpy(), names, absorbed_groups=absorbed, bootstrap=bootstrap, B=B)
    for r in res:
        r.update({"N": info["N"], "banks": info["clusters"], "pre": int((d.ifrs9_d == 0).sum()), "post": int((d.ifrs9_d == 1).sum()),
                  "r2_within" if spec != "M0" else "r2": info["r2"]})
    return res, info, d, X, y, names


def models(O, B=E.B_DEFAULT) -> pd.DataFrame:
    out = []
    for k in D.CORE:
        d = D.inferential(O[k])
        for spec in SPECS:
            res, *_ = estimate(d, spec, B=B)
            for r in res:
                if r["term"].startswith("year_") or r["term"] == "const":
                    continue
                out.append({"outcome": k, "variable": D.OUTCOMES[k][2], "model": spec, "specification": SPECS[spec],
                            "sample": "primary (frozen inferential_use)", **r})
    return pd.DataFrame(out)


SENS = {
    "S0_primary": ("Primary eligible sample", lambda d, full: d),
    "S1_drop_fallback": ("Drop fallback comparative rows (sensitivity_drop)", lambda d, full: d[~d.sensitivity_drop]),
    "S2_add_exception_rows": ("Add back rows excluded as documented source exceptions", lambda d, full: full),
    "S3_drop_unity_negative_capital": ("Drop Unity negative-capital observations (2016-2022)", lambda d, full: d[~d.unity_negative_capital]),
    "S4_drop_2020": ("Drop 2020 (COVID-19 year)", lambda d, full: d[d.year != 2020]),
    "S5_drop_unity": ("Drop Unity entirely", lambda d, full: d[d.bank != "Unity"]),
}


def robustness(O, B=E.B_DEFAULT) -> tuple[pd.DataFrame, pd.DataFrame]:
    out, jk = [], []
    for k in D.CORE:
        full = O[k]; prim = D.inferential(full)
        for sid, (lab, f) in SENS.items():
            s = f(prim, full)
            if sid == "S2_add_exception_rows" and len(s) == len(prim):
                continue
            for spec in ("M1", "M4"):
                res, info, *_ = estimate(s, spec, B=B)
                r = next(x for x in res if x["term"] == KEY_TERM[spec])
                out.append({"outcome": k, "variable": D.OUTCOMES[k][2], "sensitivity": sid, "description": lab, "model": spec, **r})
        for spec in ("M1", "M4"):
            base = next(x for x in estimate(prim, spec, bootstrap=False)[0] if x["term"] == KEY_TERM[spec])["coef"]
            vals = []
            for b in sorted(prim.bank.unique()):
                res, *_ = estimate(prim[prim.bank != b], spec, bootstrap=False)
                r = next((x for x in res if x["term"] == KEY_TERM[spec]), None)
                if r is None:
                    continue
                vals.append(r["coef"])
                jk.append({"outcome": k, "model": spec, "term": KEY_TERM[spec], "dropped_bank": b, "coef": r["coef"], "full_sample_coef": base})
            v = np.array(vals); G = len(v)
            jk.append({"outcome": k, "model": spec, "term": KEY_TERM[spec], "dropped_bank": "SUMMARY", "coef": np.nan, "full_sample_coef": base,
                       "jackknife_min": v.min(), "jackknife_max": v.max(), "sign_changes": int((np.sign(v) != np.sign(base)).sum()),
                       "jackknife_se": math.sqrt((G - 1) / G * ((v - v.mean()) ** 2).sum())})
    return pd.DataFrame(out), pd.DataFrame(jk)


def _wooldridge_ar1(d: pd.DataFrame) -> float:
    """Wooldridge (2002) test for AR(1) in FE errors: FD regression, regress residual on its lag, H0 coef = -0.5."""
    d = d.sort_values(["bank", "year"]).copy()
    d["dy"] = d.groupby("bank")["value"].diff(); d["dpost"] = d.groupby("bank")["ifrs9_d"].diff()
    d["gap"] = d.groupby("bank")["year"].diff()
    f = d[(d.gap == 1)].dropna(subset=["dy", "dpost"])
    if len(f) < 15:
        return np.nan
    X = np.column_stack([np.ones(len(f)), f.dpost]); y = f.dy.to_numpy()
    b = np.linalg.pinv(X.T @ X) @ X.T @ y; f = f.assign(e=y - X @ b)
    f["elag"] = f.groupby("bank")["e"].shift(); f["ygap"] = f.groupby("bank")["year"].diff()
    h = f[(f.ygap == 1)].dropna(subset=["elag"])
    if len(h) < 10 or h.bank.nunique() < 3:
        return np.nan
    Xh = np.column_stack([np.ones(len(h)), h.elag]); yh = h.e.to_numpy()
    XtXi = np.linalg.pinv(Xh.T @ Xh); bh = XtXi @ Xh.T @ yh
    se, _ = E._cr1_se(Xh, yh - Xh @ bh, h.bank.to_numpy(), XtXi)
    t = (bh[1] + 0.5) / se[1]
    return float(2 * stats.t.sf(abs(t), h.bank.nunique() - 1))


def diagnostics(O) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows, infl = [], []
    for k in D.CORE:
        prim = D.inferential(O[k])
        for spec in ("M1", "M2", "M4"):
            res, info, d, X, y, names = estimate(prim, spec, bootstrap=False)
            kk = names.index(KEY_TERM[spec])
            h, cook, dfb = E.influence(X, y, info["XtXi"], info["b"], kk)
            v = E.vif(X, names)
            rt = E.residual_tests(info["resid"], X)
            tot = prim["value"].var(ddof=1)
            within = (prim["value"] - prim.groupby("bank")["value"].transform("mean")).var(ddof=1)
            n = len(d)
            thr = 4 / n
            top = np.argsort(-np.abs(dfb))[:3]
            for i in np.argsort(-cook)[:5]:
                infl.append({"outcome": k, "model": spec, "bank": d.bank[i], "year": int(d.year[i]), "value": d.value[i],
                             "cooks_d": cook[i], "dfbeta_key_term": dfb[i], "leverage_h": h[i], "flag_cooks_gt_4_over_N": cook[i] > thr})
            rows.append({"outcome": k, "model": spec, "N": n, "banks": d.bank.nunique(),
                         "within_share_of_variance": within / tot if tot > 0 else np.nan,
                         "banks_observed_both_regimes": int((d.groupby("bank")["ifrs9_d"].nunique() == 2).sum()),
                         "vif_" + KEY_TERM[spec]: v[KEY_TERM[spec]], "vif_ln_assets": v.get("ln_assets", np.nan),
                         "max_vif": max(v.values()), "condition_number": float(np.linalg.cond(X)),
                         "max_cooks_d": cook.max(), "max_cooks_obs": f"{d.bank[int(np.argmax(cook))]} {int(d.year[int(np.argmax(cook))])}",
                         "n_cooks_gt_4_over_N": int((cook > thr).sum()),
                         "largest_abs_dfbeta_obs": "; ".join(f"{d.bank[i]} {int(d.year[i])} ({dfb[i]:.2f})" for i in top),
                         "jarque_bera_p": rt["jarque_bera_p"], "breusch_pagan_p": rt["breusch_pagan_p"],
                         "wooldridge_ar1_p": _wooldridge_ar1(prim) if spec == "M1" else np.nan,
                         "ifrs9_d_with_year_fe": "not estimated: IFRS9_D is an exact linear combination of 2018-2022 year dummies" if spec == "M4" else ""})
    return pd.DataFrame(rows), pd.DataFrame(infl)


# ---------------------------------------------------------------- going concern
def going_concern(O) -> dict[str, pd.DataFrame]:
    g = O["gcu"]; p = D.panel()
    gcr = pd.read_csv(D.REL / "going_concern_reviews.csv")
    gcr["year"] = gcr["year"].astype(int)
    ev = g[g.value == 1].merge(gcr, on=["bank", "year"], how="left")
    keys = ["car", "eqta", "leverage", "roa", "allr", "impairment_assets", "ocf_ratio"]
    events = []
    for r in ev.itertuples():
        pr = p[(p.bank == r.bank) & (p.year == r.year)].iloc[0]
        same_year = p[(p.year == r.year) & (p.bank != r.bank)]
        row = {"bank": r.bank, "year": r.year, "tier": r.tier, "gcu": 1, "auditor": r.auditor, "report_date": r.report_date,
               "opinion_type": r.opinion_type, "material_uncertainty_section": str(r.mu_section)[:160],
               "management_disclosure": str(r.management_gc_disclosure)[:160]}
        for c in keys:
            row[f"{c}"] = pr[c]
            row[f"{c}_other_banks_median_same_year"] = same_year[c].median()
        events.append(row)
    events = pd.DataFrame(events)
    cov = []
    for lab, sub in (("All coded", g), ("Pre-IFRS 9", g[g.ifrs9_d == 0]), ("Post-IFRS 9", g[g.ifrs9_d == 1]),
                     ("Tier 1", g[g.tier1 == 1]), ("Tier 2", g[g.tier1 == 0]), ("Unity", g[g.bank == "Unity"])):
        cov.append({"group": lab, "coded_bank_years": len(sub), "events_gcu_1": int((sub.value == 1).sum()), "coded_0": int((sub.value == 0).sum()),
                    "banks": sub.bank.nunique(), "event_rate": (sub.value == 1).mean() if len(sub) else np.nan})
    cov = pd.DataFrame(cov)
    a = int((g[(g.ifrs9_d == 0)].value == 1).sum()); b = int((g[g.ifrs9_d == 0].value == 0).sum())
    c = int((g[(g.ifrs9_d == 1)].value == 1).sum()); dd = int((g[g.ifrs9_d == 1].value == 0).sum())
    fisher = stats.fisher_exact([[c, dd], [a, b]])
    cov = pd.concat([cov, pd.DataFrame([{"group": "Fisher exact (post vs pre event share; descriptive, events clustered in one bank)",
                                          "coded_bank_years": len(g), "events_gcu_1": a + c, "event_rate": fisher.pvalue}])], ignore_index=True)
    unity = p[p.bank == "Unity"][["bank", "year", "gcu", "car", "eqta", "leverage", "roa", "allr", "impairment_assets", "ocf_ratio", "regulatory_capital", "equity"]].copy()
    unity = unity.merge(gcr[gcr.bank == "Unity"][["year", "report_reviewed", "gcu_code", "mu_section", "key_audit_matters", "coding_basis"]], on="year", how="left")
    unity["event"] = unity["gcu"] == 1
    return {"events": events, "coverage": cov, "unity_profile": unity}
