"""Run the thesis analysis on the frozen release: python -m thesis_analysis [--B 9999]."""
from __future__ import annotations

import argparse
import json
import platform
import shutil
import subprocess
import zipfile
from datetime import datetime, timezone

import numpy as np
import pandas as pd

from . import compute as C
from . import compare as CMP
from . import data as D
from . import econ as E
from . import figures as F

OUT = D.OUT
ALPHA = 0.05


def _w(df: pd.DataFrame, name: str) -> pd.DataFrame:
    df.to_csv(OUT / name, index=False)
    return pd.read_csv(OUT / name)          # always continue from the exported file


def _fmt(x, nd=3):
    if x is None or (isinstance(x, float) and np.isnan(x)):
        return ""
    if isinstance(x, (int, np.integer)):
        return str(int(x))
    if isinstance(x, (float, np.floating)):
        return f"{x:.{nd}f}"
    return str(x)


def _table(df: pd.DataFrame, name: str, title: str, note: str, nd=3):
    (OUT / "tables").mkdir(exist_ok=True)
    df.to_csv(OUT / "tables" / f"{name}.csv", index=False)
    cols = list(df.columns)
    lines = [f"**{title}**", "", "| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for r in df.itertuples(index=False):
        lines.append("| " + " | ".join(_fmt(v, nd) for v in r) + " |")
    lines += ["", f"*Note.* {note}", ""]
    (OUT / "tables" / f"{name}.md").write_text("\n".join(lines), encoding="utf-8")
    return df


def stars(p):
    return "***" if p < 0.01 else "**" if p < 0.05 else "*" if p < 0.10 else ""


def build_tables(res):
    T = {}
    T["table1_sample_coverage"] = _table(res["sample"]["coverage"][["bank", "tier", "cohort_status", "selected_bank_years", "pre_2018", "post_2018", "years_missing"]],
                                         "table1_sample_coverage", "Table 1. Sample coverage of the 12-bank cohort, 2013-2022",
                                         "FCMB is formally excluded (no consistent standalone First City Monument Bank Limited series); it is not replaced. Source: verified_panel.csv of the frozen release.")
    T["table2_variables_eligible_n"] = _table(res["sample"]["eligibility"][["variable", "definition", "units", "available_N", "eligible_N", "excluded_N", "banks", "pre", "post", "tier1", "tier2", "fallback_rows_in_eligible", "analysis_role", "excluded_rows"]],
                                              "table2_variables_eligible_n", "Table 2. Variable definitions and eligible sample sizes",
                                              "Eligible = inferential_use in the frozen outcome_eligibility.csv. Fallback rows are original-year-unavailable comparatives kept in the primary sample.")
    d = res["desc"]
    T["table3_descriptive_statistics"] = _table(d[d.group == "Full sample"][["variable", "N", "banks", "mean", "sd", "min", "p25", "median", "p75", "max"]],
                                                "table3_descriptive_statistics", "Table 3. Descriptive statistics, eligible sample (percent)",
                                                "Unity's negative-capital years (2016-2022) produce the extreme minima for CAR and equity/assets and the maxima for leverage. Source: descriptive_statistics.csv.", 2)
    pp = res["prepost"].merge(res["matched"][res["matched"].group == "All matched banks"][["outcome", "banks", "mean_diff", "median_diff", "banks_increase", "banks_decrease", "wilcoxon_signed_rank_p"]],
                              on="outcome", how="left")
    T["table4_prepost"] = _table(pp[["variable", "N_pre", "N_post", "mean_pre", "mean_post", "median_pre", "median_post", "mann_whitney_p_naive",
                                     "banks", "mean_diff", "median_diff", "banks_increase", "banks_decrease", "wilcoxon_signed_rank_p"]],
                                 "table4_prepost", "Table 4. Pre- versus post-IFRS 9 comparison (pooled and matched banks)",
                                 "Pooled tests ignore repeated observations (descriptive). Matched columns use bank means for banks observed in both regimes; Wilcoxon signed-rank on bank differences. Sources: descriptive_statistics.csv, matched_prepost.csv.", 2)
    t = res["tiers"]
    T["table5_tier_comparison"] = _table(t[["variable", "period", "N_tier1", "N_tier2", "mean_tier1", "mean_tier2", "median_tier1", "median_tier2", "diff_mean_t1_minus_t2", "mann_whitney_p_naive"]],
                                         "table5_tier_comparison", "Table 5. Tier 1 versus Tier 2 comparison by regime",
                                         "Difference-in-means row = (Tier 1 post - pre) - (Tier 2 post - pre). Naive tests ignore clustering. Source: tier_comparisons.csv.", 2)
    reg = res["reg"]
    rows = []
    for k in D.CORE:
        for m in ("M1", "M2", "M3", "M0"):
            r = reg[(reg.outcome == k) & (reg.model == m) & (reg.term == "IFRS9_D")].iloc[0]
            rows.append({"variable": D.OUTCOMES[k][2], "model": m, "coef_IFRS9_D": r.coef, "se_conventional": r.se_conventional, "p_conventional": r.p_conventional,
                         "se_cr1": r.se_cr1, "p_cr1": r.p_cr1_tG1, "ci95_cr1": f"[{r.ci95_low_cr1:.2f}, {r.ci95_high_cr1:.2f}]",
                         "p_wcb": r.p_wild_cluster_bootstrap, "sig_wcb": stars(r.p_wild_cluster_bootstrap), "N": int(r.N), "banks": int(r.banks),
                         "r2": r.r2_within if m != "M0" else r.r2})
    T["table6_regression_ifrs9"] = _table(pd.DataFrame(rows), "table6_regression_ifrs9", "Table 6. Effect of IFRS 9 adoption (IFRS9_D) on bank outcomes",
                                          "M1 principal (bank FE); M2 adds ln(total assets); M3 adds a linear trend; M0 pooled OLS. No year FE with IFRS9_D (perfect collinearity). "
                                          "CR1 = bank-clustered SE, t(G-1); WCB = wild-cluster restricted bootstrap (Webb weights, B = 9,999). Stars from WCB p: * 0.10, ** 0.05, *** 0.01. Source: regression_results.csv.")
    rows = []
    for k in D.CORE:
        for m, term in (("M4", "Tier1_x_IFRS9_D"), ("M4s", "Tier1_x_IFRS9_D"), ("M5", "IFRS9_D"), ("M5", "Tier1_x_IFRS9_D")):
            r = reg[(reg.outcome == k) & (reg.model == m) & (reg.term == term)].iloc[0]
            rows.append({"variable": D.OUTCOMES[k][2], "model": m, "term": term, "coef": r.coef, "se_cr1": r.se_cr1, "p_cr1": r.p_cr1_tG1,
                         "p_conventional": r.p_conventional, "p_wcb": r.p_wild_cluster_bootstrap, "sig_wcb": stars(r.p_wild_cluster_bootstrap), "N": int(r.N), "banks": int(r.banks)})
    T["table7_tier_interaction"] = _table(pd.DataFrame(rows), "table7_tier_interaction", "Table 7. Tier 1 versus Tier 2 differences in the IFRS 9 effect",
                                          "M4: bank and year FE, Tier1 x IFRS9_D (principal tier model); M4s adds ln(total assets); M5: bank FE, IFRS9_D = Tier 2 change, interaction = Tier 1 minus Tier 2. Source: regression_results.csv.")
    rob = res["rob"]; jk = res["jk"]
    rows = []
    for k in D.CORE:
        for m in ("M1", "M4"):
            s = rob[(rob.outcome == k) & (rob.model == m)]
            row = {"variable": D.OUTCOMES[k][2], "model": m}
            for r in s.itertuples():
                row[r.sensitivity.split("_", 1)[0] + "_coef"] = r.coef
                row[r.sensitivity.split("_", 1)[0] + "_p_wcb"] = r.p_wild_cluster_bootstrap
            j = jk[(jk.outcome == k) & (jk.model == m) & (jk.dropped_bank == "SUMMARY")].iloc[0]
            row.update({"jackknife_min": j.jackknife_min, "jackknife_max": j.jackknife_max, "jackknife_sign_changes": int(j.sign_changes)})
            rows.append(row)
    T["table8_robustness"] = _table(pd.DataFrame(rows), "table8_robustness", "Table 8. Robustness of the key coefficients",
                                    "S0 primary; S1 drop fallback comparative rows; S2 add back documented-exception rows; S3 drop Unity negative-capital observations; S4 drop 2020; S5 drop Unity. "
                                    "Jackknife = leave-one-bank-out. M1 key term IFRS9_D; M4 key term Tier1 x IFRS9_D. Sources: robustness_results.csv, jackknife_results.csv.")
    ev = res["gc"]["events"]
    T["table9_going_concern_events"] = _table(ev[["bank", "year", "tier", "auditor", "report_date", "car", "car_other_banks_median_same_year", "eqta", "eqta_other_banks_median_same_year",
                                                   "roa", "roa_other_banks_median_same_year", "leverage", "material_uncertainty_section"]],
                                              "table9_going_concern_events", "Table 9. Going-concern events (auditor material-uncertainty sections)",
                                              "All three events are Unity Bank Plc. No multivariable model is estimated (3 events). Source: going_concern_events.csv.", 2)
    vs = res["vol"]
    T["table10_volatility"] = _table(vs[[c for c in ["variable", "banks_with_3_plus_each_regime", "median_sd_pre", "median_sd_post", "median_sd_ratio", "banks_sd_increase", "banks_sd_decrease", "wilcoxon_log_sd_ratio_p", "status"] if c in vs.columns]],
                                     "table10_volatility", "Table 10. Within-bank volatility before and after IFRS 9 (exploratory)",
                                     "Sample SD per bank and regime, banks with >= 3 comparable observations in each regime. Wilcoxon signed-rank on log(SD post / SD pre). Source: volatility_results.csv.")
    dg = res["diag"]
    T["table11_diagnostics"] = _table(dg[["outcome", "model", "N", "banks", "banks_observed_both_regimes", "within_share_of_variance", "max_vif", "condition_number", "max_cooks_d", "max_cooks_obs",
                                          "n_cooks_gt_4_over_N", "jarque_bera_p", "breusch_pagan_p", "wooldridge_ar1_p"]],
                                      "table11_diagnostics", "Table 11. Model diagnostics",
                                      "VIF/condition number on the within-transformed design. Cook's D threshold 4/N. Wooldridge AR(1) test on first-differenced residuals (H0 no serial correlation). Source: model_diagnostics.csv.")
    gcov = res["gc"]["coverage"]
    T["table12_going_concern_coverage"] = _table(gcov, "table12_going_concern_coverage", "Table 12. Going-concern coding coverage and event counts",
                                                 "Unknown codes are not zero. Last row reports a descriptive Fisher exact p-value in the event_rate column. Source: going_concern_coverage.csv.")
    return T


def interpretation(res) -> pd.DataFrame:
    reg, rob, jk, desc = res["reg"], res["rob"], res["jk"], res["desc"]
    objectives = [("O1", "IFRS 9 adoption and loan-loss provisioning", ["allr", "impairment_assets"], "M1", "IFRS9_D"),
                  ("O2", "IFRS 9 adoption and capital adequacy", ["car"], "M1", "IFRS9_D"),
                  ("O3", "IFRS 9 adoption, profitability, cash generation and balance-sheet stability", ["roa", "ocf_ratio", "eqta", "leverage"], "M1", "IFRS9_D"),
                  ("O5", "Tier 1 versus Tier 2 difference in the IFRS 9 effect", D.CORE, "M4", "Tier1_x_IFRS9_D")]
    rows = []
    for oid, label, ks, m, term in objectives:
        for k in ks:
            r = reg[(reg.outcome == k) & (reg.model == m) & (reg.term == term)].iloc[0]
            pre_mean = desc[(desc.outcome == k) & (desc.group == "Pre-IFRS 9 (2013-2017)")]["mean"].iloc[0]
            pre_med = desc[(desc.outcome == k) & (desc.group == "Pre-IFRS 9 (2013-2017)")]["median"].iloc[0]
            s = rob[(rob.outcome == k) & (rob.model == m) & (rob.sensitivity != "S0_primary")]
            j = jk[(jk.outcome == k) & (jk.model == m) & (jk.dropped_bank == "SUMMARY")].iloc[0]
            same_sign = int((np.sign(s.coef) == np.sign(r.coef)).sum())
            sig = int((s.p_wild_cluster_bootstrap < ALPHA).sum())
            if r.p_wild_cluster_bootstrap < ALPHA:
                rob_txt = ("robust: " if same_sign == len(s) and sig == len(s) and j.sign_changes == 0 else "not fully robust: ") + \
                          f"same sign in {same_sign}/{len(s)} sensitivities, WCB p < 0.05 in {sig}/{len(s)}, jackknife sign changes {int(j.sign_changes)}"
            else:
                rob_txt = f"primary not significant; same sign in {same_sign}/{len(s)} sensitivities, WCB p < 0.05 in {sig}/{len(s)} ({', '.join(x.split('_',1)[0] for x in s[s.p_wild_cluster_bootstrap < ALPHA].sensitivity) or 'none'}); jackknife sign changes {int(j.sign_changes)}"
            decision = "H0 rejected at 5% (WCB)" if r.p_wild_cluster_bootstrap < ALPHA else "H0 not rejected at 5% (WCB)"
            if (r.p_wild_cluster_bootstrap < ALPHA) != (r.p_cr1_tG1 < ALPHA):
                decision += f"; CR1 t(G-1) p = {r.p_cr1_tG1:.3f} gives the opposite decision"
            lim = [f"{int(r.banks)} bank clusters (few-cluster inference)"]
            lim.append("IFRS9_D is a single common adoption date: without year FE it also absorbs 2018-2022 macro shocks (2020 pandemic, FX reforms)"
                       if m == "M1" else "year FE absorb common shocks; identification rests on Tier 1 vs Tier 2 differences only")
            if k in ("car", "eqta", "leverage"):
                lim.append("Unity's negative-capital years dominate the variance (see S3/S5)")
            if k == "leverage":
                lim.append("leverage = 100 - equity/assets, so results mirror equity/assets")
            if r.sensitivity_drop_rows if hasattr(r, "sensitivity_drop_rows") else False:
                pass
            if m == "M4":
                lim.append("only 5 Tier 1 banks")
            rows.append({"objective": oid, "objective_label": label, "outcome": k, "variable": D.OUTCOMES[k][2],
                         "usable_sample": f"N = {int(r.N)} bank-years, {int(r.banks)} banks ({int(r.pre)} pre / {int(r.post)} post)",
                         "estimator": C.SPECS[m], "term": term, "coefficient_pp": r.coef, "direction": "increase" if r.coef > 0 else "decrease",
                         "magnitude": f"{r.coef:+.2f} pp vs pre-period mean {pre_mean:.2f} / median {pre_med:.2f}",
                         "p_conventional": r.p_conventional, "p_cr1_tG1": r.p_cr1_tG1, "p_wild_cluster_bootstrap": r.p_wild_cluster_bootstrap,
                         "robustness": rob_txt, "h0_decision": decision, "limitations": "; ".join(lim)})
    gc = res["gc"]["coverage"]
    ev = res["gc"]["events"]
    rows.append({"objective": "O4", "objective_label": "Going-concern indicators before and after IFRS 9", "outcome": "gcu", "variable": "Going-concern uncertainty",
                 "usable_sample": f"{int(gc.iloc[0].coded_bank_years)} coded bank-years, {int(gc.iloc[0].banks)} banks; {int(gc.iloc[0].events_gcu_1)} events",
                 "estimator": "descriptive only (event table, coverage, Fisher exact share comparison)", "term": "",
                 "coefficient_pp": np.nan, "direction": "events only after adoption" if (ev.year >= D.ADOPTION).all() else "mixed",
                 "magnitude": "events: " + ", ".join(f"{r.bank} {r.year}" for r in ev.itertuples()),
                 "p_conventional": np.nan, "p_cr1_tG1": np.nan, "p_wild_cluster_bootstrap": np.nan,
                 "robustness": "not applicable", "h0_decision": "not tested (3 events in one bank; a model would be unidentified/separation-prone)",
                 "limitations": "events concentrated in Unity; 51 panel rows have unknown (not zero) codes; Unity 2020 uncoded"})
    vs = res["vol"]
    for k in ("roa", "car", "allr", "impairment_assets"):
        v = vs[vs.outcome == k].iloc[0]
        p = v.get("wilcoxon_log_sd_ratio_p", np.nan)
        rows.append({"objective": "O6", "objective_label": "Volatility before and after IFRS 9 (exploratory)", "outcome": k, "variable": D.OUTCOMES[k][2],
                     "usable_sample": f"{int(v.banks_with_3_plus_each_regime)} banks with >= 3 comparable observations per regime",
                     "estimator": "within-bank sample SD by regime; Wilcoxon signed-rank on log SD ratio", "term": "",
                     "coefficient_pp": np.nan, "direction": "higher after" if v.median_sd_ratio > 1 else "lower after",
                     "magnitude": f"median SD ratio post/pre {v.median_sd_ratio:.2f} ({int(v.banks_sd_increase)} up, {int(v.banks_sd_decrease)} down)",
                     "p_conventional": np.nan, "p_cr1_tG1": np.nan, "p_wild_cluster_bootstrap": p,
                     "robustness": "exploratory; SDs from 3-5 points", "h0_decision": ("H0 rejected (exploratory)" if p == p and p < ALPHA else "H0 not rejected (exploratory)"),
                     "limitations": "few observations per regime; SD sensitive to single years; not definitive"})
    return pd.DataFrame(rows)


def workbook(T, files: dict[str, pd.DataFrame], interp):
    path = OUT / "analysis_master.xlsx"
    with pd.ExcelWriter(path, engine="openpyxl") as xw:
        pd.DataFrame({"item": ["Source", "Cohort", "Principal estimator", "Tier model", "Inference", "Not modelled", "Files"],
                      "value": [f"Frozen release {D.RELEASE_ID} (hash-verified, unaltered)", "12 banks; FCMB formally excluded",
                                "Bank fixed effects, y ~ IFRS9_D (M1)", "Bank + year FE, y ~ Tier1 x IFRS9_D (M4)",
                                "Conventional, CR1 bank-clustered t(G-1), wild-cluster restricted bootstrap (Webb, B = 9,999)",
                                "Going concern (3 events), NPL, broad coverage, Stage 3, liquidity: descriptive only",
                                "Each sheet mirrors a CSV in thesis_results/"]}).to_excel(xw, sheet_name="README", index=False)
        for name, df in T.items():
            df.to_excel(xw, sheet_name=name.replace("table", "T")[:31], index=False)
        interp.to_excel(xw, sheet_name="interpretation", index=False)
        for name, df in files.items():
            df.to_excel(xw, sheet_name=name[:31], index=False)
    return path


def report(meta) -> str:
    r = lambda f: pd.read_csv(OUT / f)  # noqa: E731
    elig = r("tables/table2_variables_eligible_n.csv"); cov = r("tables/table1_sample_coverage.csv")
    reg = r("regression_results.csv"); rob = r("robustness_results.csv"); interp = r("interpretation.csv")
    mt = r("matched_prepost_summary.csv"); vol = r("volatility_results_summary.csv"); ev = r("going_concern_events.csv")
    gcov = r("going_concern_coverage.csv"); dg = r("model_diagnostics.csv"); jk = r("jackknife_results.csv")
    tot = cov[cov.bank.str.startswith("Total")].iloc[0]
    L = [f"# Thesis analysis report (generated)", "",
         f"Generated {meta['generated_utc']} by `python -m thesis_analysis` at code commit `{meta['code_commit']}`.",
         f"Input: frozen release `{meta['release']['release_id']}` ({meta['release']['files_verified']} files hash-verified against RELEASE_MANIFEST.json; release code commit `{meta['release']['code_commit']}`).",
         "Every number below is read back from the exported file named in brackets. No thesis prose; no data were changed.", "",
         "## 1. Sample", "",
         f"- Cohort: 12 banks ({tot.tier}); FCMB formally excluded and not replaced [tables/table1_sample_coverage.csv].",
         f"- Selected bank-years: {int(tot.selected_bank_years)} of 120 positions ({int(tot.pre_2018)} pre-IFRS 9, {int(tot.post_2018)} post) [tables/table1_sample_coverage.csv].",
         "- Eligible N by outcome [tables/table2_variables_eligible_n.csv]:", ""]
    L += [f"  - {x.variable}: {int(x.eligible_N)} (pre {int(x.pre)}, post {int(x.post)}; Tier 1 {int(x.tier1)}, Tier 2 {int(x.tier2)}; {int(x.banks)} banks; excluded {int(x.excluded_N)}; role: {x.analysis_role})" for x in elig.itertuples()]
    L += ["", "## 2. Principal results (bank fixed effects, M1: y ~ IFRS9_D) [regression_results.csv]", "",
          "| Outcome | Coef (pp) | CR1 SE | p conventional | p CR1 t(G-1) | p WCB | N | Banks |", "|---|---|---|---|---|---|---|---|"]
    for k in D.CORE:
        x = reg[(reg.outcome == k) & (reg.model == "M1") & (reg.term == "IFRS9_D")].iloc[0]
        L.append(f"| {x.variable} | {x.coef:.3f} | {x.se_cr1:.3f} | {x.p_conventional:.3f} | {x.p_cr1_tG1:.3f} | {x.p_wild_cluster_bootstrap:.3f} | {int(x.N)} | {int(x.banks)} |")
    L += ["", "## 3. Tier 1 vs Tier 2 (M4: bank + year FE, Tier1 x IFRS9_D) [regression_results.csv]", "",
          "| Outcome | Coef (pp) | CR1 SE | p CR1 | p WCB | N |", "|---|---|---|---|---|---|"]
    for k in D.CORE:
        x = reg[(reg.outcome == k) & (reg.model == "M4") & (reg.term == "Tier1_x_IFRS9_D")].iloc[0]
        L.append(f"| {x.variable} | {x.coef:.3f} | {x.se_cr1:.3f} | {x.p_cr1_tG1:.3f} | {x.p_wild_cluster_bootstrap:.3f} | {int(x.N)} |")
    L += ["", "## 4. Robustness of M1 (IFRS9_D) [robustness_results.csv, jackknife_results.csv]", "",
          "| Outcome | " + " | ".join(s.split("_", 1)[0] for s in C.SENS) + " | Jackknife min | Jackknife max | Sign changes |", "|---" * (len(C.SENS) + 4) + "|"]
    for k in D.CORE:
        s = rob[(rob.outcome == k) & (rob.model == "M1")].set_index("sensitivity")
        j = jk[(jk.outcome == k) & (jk.model == "M1") & (jk.dropped_bank == "SUMMARY")].iloc[0]
        cells = [f"{s.loc[sid, 'coef']:.2f} (p={s.loc[sid, 'p_wild_cluster_bootstrap']:.3f})" if sid in s.index else "n/a" for sid in C.SENS]
        L.append(f"| {D.OUTCOMES[k][2]} | " + " | ".join(cells) + f" | {j.jackknife_min:.2f} | {j.jackknife_max:.2f} | {int(j.sign_changes)} |")
    L += ["", "S0 primary; S1 drop fallback rows; S2 add exception rows (n/a where none); S3 drop Unity negative-capital rows; S4 drop 2020; S5 drop Unity. p = WCB.", "",
          "## 5. Matched pre/post (bank means, banks in both regimes) [matched_prepost_summary.csv]", ""]
    for x in mt[mt.group == "All matched banks"].itertuples():
        L.append(f"- {x.variable}: {int(x.banks)} banks; mean difference {x.mean_diff:.3f} pp, median {x.median_diff:.3f}; {int(x.banks_increase)} up / {int(x.banks_decrease)} down; Wilcoxon p = {x.wilcoxon_signed_rank_p:.3f}.")
    L += ["", "## 6. Volatility (EXPLORATORY) [volatility_results_summary.csv]", ""]
    for x in vol.itertuples():
        p = getattr(x, "wilcoxon_log_sd_ratio_p", np.nan)
        L.append(f"- {x.variable}: {int(x.banks_with_3_plus_each_regime)} banks; median SD pre {x.median_sd_pre:.3f}, post {x.median_sd_post:.3f}, median ratio {x.median_sd_ratio:.2f}; "
                 f"{int(x.banks_sd_increase)} higher / {int(x.banks_sd_decrease)} lower; Wilcoxon p = {p:.3f}.")
    L += ["", "## 7. Going concern (descriptive only) [going_concern_events.csv, going_concern_coverage.csv]", ""]
    for x in ev.itertuples():
        L.append(f"- {x.bank} {x.year} ({x.tier}): auditor {x.auditor}, report {x.report_date}; CAR {x.car:.2f}% (other banks' median {x.car_other_banks_median_same_year:.2f}%), "
                 f"equity/assets {x.eqta:.2f}% (other banks {x.eqta_other_banks_median_same_year:.2f}%), ROA {x.roa if x.roa == x.roa else float('nan'):.2f}%.")
    a = gcov.iloc[0]
    L += [f"- Coded bank-years {int(a.coded_bank_years)}, events {int(a.events_gcu_1)}; pre-IFRS 9 events {int(gcov[gcov.group == 'Pre-IFRS 9'].events_gcu_1.iloc[0])}, "
          f"post {int(gcov[gcov.group == 'Post-IFRS 9'].events_gcu_1.iloc[0])}; descriptive Fisher exact p = {gcov.iloc[-1].event_rate:.3f}. No logistic/probit model estimated.", "",
          "## 8. Diagnostics [model_diagnostics.csv]", ""]
    for x in dg[dg.model == "M1"].itertuples():
        L.append(f"- {D.OUTCOMES[x.outcome][2]}: within share of variance {x.within_share_of_variance:.2f}; max Cook's D {x.max_cooks_d:.2f} ({x.max_cooks_obs}); "
                 f"{int(x.n_cooks_gt_4_over_N)} obs > 4/N; JB p {x.jarque_bera_p:.3f}; BP p {x.breusch_pagan_p:.3f}; Wooldridge AR(1) p {x.wooldridge_ar1_p:.3f}.")
    m2 = dg[dg.model == "M2"]
    L += [f"- Adding ln(total assets) (M2): VIF of IFRS9_D {m2.vif_IFRS9_D.min():.2f}-{m2.vif_IFRS9_D.max():.2f}; max Cook's D rises to {m2.max_cooks_d.max():.2f} "
          f"({m2.loc[m2.max_cooks_d.idxmax(), 'max_cooks_obs']}), which is why M1 is principal.", "",
          "## 9. Objective-level interpretation [interpretation.csv]", "",
          "| Obj | Outcome | Sample | Coef (pp) | p WCB | Decision | Robustness |", "|---|---|---|---|---|---|---|"]
    for x in interp.itertuples():
        c = "" if x.coefficient_pp != x.coefficient_pp else f"{x.coefficient_pp:.3f}"
        p = "" if x.p_wild_cluster_bootstrap != x.p_wild_cluster_bootstrap else f"{x.p_wild_cluster_bootstrap:.3f}"
        L.append(f"| {x.objective} | {x.variable} | {x.usable_sample} | {c} | {p} | {x.h0_decision} | {x.robustness} |")
    L += ["", "## 10. Files", "", "Figures: figures/*.png|pdf; tables: tables/*.csv|md; workbook: analysis_master.xlsx; archive: thesis_results_handoff.zip.", ""]
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="thesis_analysis")
    ap.add_argument("--B", type=int, default=E.B_DEFAULT)
    a = ap.parse_args(argv)
    OUT.mkdir(parents=True, exist_ok=True)
    rel = D.verify_release()
    O = D.all_outcomes()
    res = {"O": O, "sample": C.sample_profile(O)}
    res["desc"] = _w(C.descriptives(O), "descriptive_statistics.csv")
    res["prepost"] = _w(C.prepost(O), "prepost_pooled.csv")
    res["tiers"] = _w(C.tiers(O), "tier_comparisons.csv")
    tl, sl = C.trends(O)
    _w(tl, "trend_values.csv"); _w(sl, "trend_slopes.csv")
    mb, ms = C.matched(O)
    res["matched_banks"] = _w(mb, "matched_prepost.csv"); res["matched"] = _w(ms, "matched_prepost_summary.csv")
    vb, vs = C.volatility(O)
    res["vol_banks"] = _w(vb, "volatility_results.csv"); res["vol"] = _w(vs, "volatility_results_summary.csv")
    res["reg"] = _w(C.models(O, B=a.B), "regression_results.csv")
    rob, jk = C.robustness(O, B=a.B)
    res["rob"] = _w(rob, "robustness_results.csv"); res["jk"] = _w(jk, "jackknife_results.csv")
    dg, infl = C.diagnostics(O)
    res["diag"] = _w(dg, "model_diagnostics.csv"); res["influence"] = _w(infl, "influential_observations.csv")
    gc = C.going_concern(O)
    res["gc"] = {"events": _w(gc["events"], "going_concern_events.csv"), "coverage": _w(gc["coverage"], "going_concern_coverage.csv"),
                 "unity_profile": _w(gc["unity_profile"], "going_concern_unity_profile.csv")}
    res["gc"]["unity_profile"]["event"] = res["gc"]["unity_profile"]["event"].astype(bool)
    _w(res["sample"]["coverage"], "sample_coverage.csv"); _w(res["sample"]["eligibility"], "variables_eligible_n.csv")
    T = build_tables(res)
    interp = _w(interpretation(res), "interpretation.csv")
    (OUT / "interpretation.md").write_text(_interp_md(interp), encoding="utf-8")
    figs = F.all_figures(res, OUT / "figures")
    files = {k: pd.read_csv(OUT / f"{k}.csv") for k in ["descriptive_statistics", "matched_prepost", "matched_prepost_summary", "tier_comparisons", "regression_results",
                                                       "robustness_results", "jackknife_results", "volatility_results", "volatility_results_summary",
                                                       "going_concern_events", "going_concern_unity_profile", "model_diagnostics", "influential_observations", "trend_slopes"]}
    workbook(T, files, interp)
    commit = subprocess.run(["git", "rev-parse", "HEAD"], cwd=D.ROOT, capture_output=True, text=True).stdout.strip()
    import scipy, statsmodels, matplotlib  # noqa: E401
    meta = {"generated_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(), "code_commit": commit, "release": rel,
            "bootstrap": {"B": a.B, "weights": "Webb six-point", "seed": E.SEED, "type": "wild cluster restricted (WCR) bootstrap-t"},
            "software": {"python": platform.python_version(), "numpy": np.__version__, "pandas": pd.__version__, "scipy": scipy.__version__,
                         "statsmodels": statsmodels.__version__, "matplotlib": matplotlib.__version__},
            "figures": figs, "tables": sorted(T)}
    (OUT / "analysis_manifest.json").write_text(json.dumps(meta, indent=2))
    (OUT / "analysis_report.md").write_text(report(meta), encoding="utf-8")
    meta["comparison_v1"] = CMP.run()
    (OUT / "analysis_manifest.json").write_text(json.dumps(meta, indent=2))
    z = OUT / "thesis_results_handoff.zip"
    with zipfile.ZipFile(z, "w", zipfile.ZIP_DEFLATED) as zf:
        for p in sorted(OUT.rglob("*")):
            if p.is_file() and p != z:
                zf.write(p, f"thesis_results/{p.relative_to(OUT).as_posix()}")
        for p in sorted((D.ROOT / "thesis_analysis").glob("*.py")):
            zf.write(p, f"code/thesis_analysis/{p.name}")
        for rel_path in ["RELEASE_MANIFEST.json", "verified_panel.csv", "outcome_eligibility.csv", "going_concern_reviews.csv", "row_versions.csv", "eligibility_rules.csv"] + \
                        [f"analysis/{x.name}" for x in (D.REL / "analysis").glob("*.csv")]:
            zf.write(D.REL / rel_path, f"frozen_release_inputs/{rel_path}")
    print(json.dumps({"figures": len(figs), "tables": len(T), "zip": str(z.relative_to(D.ROOT))}, indent=2))


def _interp_md(df):
    L = ["# Interpretation by objective (no thesis prose)", "", "Decision rule: H0 (no effect) rejected when the wild-cluster-bootstrap p < 0.05 for the principal model; "
         "CR1 and conventional p-values reported for transparency. Source: interpretation.csv.", ""]
    for o, g in df.groupby("objective", sort=False):
        L += [f"## {o}. {g.objective_label.iloc[0]}", ""]
        for x in g.itertuples():
            L += [f"### {x.variable}", f"- Usable sample: {x.usable_sample}", f"- Estimator: {x.estimator}" + (f" (term {x.term})" if isinstance(x.term, str) and x.term else ""),
                  f"- Direction: {x.direction}; magnitude: {x.magnitude}",
                  f"- Significance: p conventional {_fmt(x.p_conventional)}, p CR1 {_fmt(x.p_cr1_tG1)}, p WCB {_fmt(x.p_wild_cluster_bootstrap)}",
                  f"- Robustness: {x.robustness}", f"- Decision: {x.h0_decision}", f"- Limitations: {x.limitations}", ""]
    return "\n".join(L)


if __name__ == "__main__":
    main()
