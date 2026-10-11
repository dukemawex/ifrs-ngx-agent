"""Compare the current thesis results (thesis_results/, latest frozen release) with the archived v1 results
(thesis_results_v1/, release IFRS9_release_2026-10-11_v1, 97 bank-years).

Writes thesis_results/comparison_*.csv and comparison_v1_v2.md. Every number in the markdown is read from those CSVs.

Material-change rule (fixed before looking at the results):
  - the 5% hypothesis decision changes under the wild-cluster bootstrap (WCB) or under CR1 t(G-1); or
  - the coefficient changes sign; or
  - |coefficient change| >= 0.5 x the v1 CR1 standard error.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import data as D

V1_DIR = D.ROOT / "thesis_results_v1"
V1_REL = D.ROOT / "releases" / "IFRS9_release_2026-10-11_v1"
ALPHA = 0.05
KEYS = ["outcome", "variable", "model", "term"]


def _panel_rows():
    a = pd.read_csv(V1_REL / "verified_panel.csv")[["bank", "year"]]
    b = pd.read_csv(D.REL / "verified_panel.csv")
    m = b.merge(a.assign(_v1=1), on=["bank", "year"], how="left")
    added = m[m["_v1"].isna()].drop(columns="_v1")
    removed = a.merge(b[["bank", "year"]].assign(_v2=1), on=["bank", "year"], how="left")
    removed = removed[removed["_v2"].isna()]
    cols = ["bank", "year", "tier", "pat", "assets", "liabilities", "equity", "ocf", "gross_loans", "loan_allowance",
            "total_impairment", "car", "regulatory_capital", "rwa", "gcu", "version_note", "source_url"]
    out = added[[c for c in cols if c in added.columns]].copy()
    out["change"] = "added"
    if len(removed):
        out = pd.concat([out, removed.assign(change="removed")], ignore_index=True)
    return out


def _eligible():
    a = pd.read_csv(V1_DIR / "variables_eligible_n.csv").set_index("outcome")
    b = pd.read_csv(D.OUT / "variables_eligible_n.csv").set_index("outcome")
    cols = ["eligible_N", "pre", "post", "tier1", "tier2", "banks"]
    out = a[["variable"] + cols].join(b[cols], lsuffix="_v1", rsuffix="_v2")
    for c in cols:
        out[f"{c}_change"] = out[f"{c}_v2"] - out[f"{c}_v1"]
    return out.reset_index()


def _decision(p):
    return np.where(p < ALPHA, "reject H0", "do not reject H0")


def _regression():
    a = pd.read_csv(V1_DIR / "regression_results.csv")
    b = pd.read_csv(D.OUT / "regression_results.csv")
    cols = ["coef", "se_cr1", "p_conventional", "p_cr1_tG1", "p_wild_cluster_bootstrap", "N", "banks"]
    m = a[KEYS + ["specification"] + cols].merge(b[KEYS + cols], on=KEYS, suffixes=("_v1", "_v2"), how="outer")
    m["coef_change"] = m["coef_v2"] - m["coef_v1"]
    m["coef_change_in_v1_se"] = m["coef_change"] / m["se_cr1_v1"]
    m["sign_change"] = np.sign(m["coef_v1"]) != np.sign(m["coef_v2"])
    for t, c in (("wcb", "p_wild_cluster_bootstrap"), ("cr1", "p_cr1_tG1"), ("conventional", "p_conventional")):
        m[f"decision_{t}_v1"] = _decision(m[f"{c}_v1"])
        m[f"decision_{t}_v2"] = _decision(m[f"{c}_v2"])
        m[f"decision_{t}_changed"] = m[f"decision_{t}_v1"] != m[f"decision_{t}_v2"]
    m["material_change"] = m["decision_wcb_changed"] | m["decision_cr1_changed"] | m["sign_change"] | (m["coef_change_in_v1_se"].abs() >= 0.5)
    return m


def _robustness():
    a = pd.read_csv(V1_DIR / "robustness_results.csv")
    b = pd.read_csv(D.OUT / "robustness_results.csv")
    k = ["outcome", "variable", "sensitivity", "model", "term"]
    m = a[k + ["coef", "p_wild_cluster_bootstrap", "N"]].merge(b[k + ["coef", "p_wild_cluster_bootstrap", "N"]], on=k, how="outer",
                                                              suffixes=("_v1", "_v2"))
    m["decision_wcb_changed"] = (m["p_wild_cluster_bootstrap_v1"] < ALPHA) != (m["p_wild_cluster_bootstrap_v2"] < ALPHA)
    m["sign_change"] = np.sign(m["coef_v1"]) != np.sign(m["coef_v2"])
    return m


def _interpretation():
    a = pd.read_csv(V1_DIR / "interpretation.csv")
    b = pd.read_csv(D.OUT / "interpretation.csv")
    k = ["objective", "outcome", "variable", "term"]
    cols = ["usable_sample", "coefficient_pp", "p_wild_cluster_bootstrap", "p_cr1_tG1", "robustness", "h0_decision"]
    m = a[k + cols].merge(b[k + cols], on=k, suffixes=("_v1", "_v2"), how="outer")
    m["h0_decision_changed"] = m["h0_decision_v1"].str.split(";").str[0] != m["h0_decision_v2"].str.split(";").str[0]
    m["robustness_label_changed"] = m["robustness_v1"].str.split(":").str[0] != m["robustness_v2"].str.split(":").str[0]
    return m


def _summaries():
    out = []
    for name, key in (("matched_prepost_summary.csv", ["outcome", "variable", "group"]),
                      ("volatility_results_summary.csv", ["outcome", "variable"])):
        a, b = pd.read_csv(V1_DIR / name), pd.read_csv(D.OUT / name)
        num = [c for c in a.columns if c not in key and pd.api.types.is_numeric_dtype(a[c])]
        m = a[key + num].merge(b[key + num], on=key, suffixes=("_v1", "_v2"), how="outer")
        m.insert(0, "table", name.replace(".csv", ""))
        pcol = "wilcoxon_signed_rank_p" if "wilcoxon_signed_rank_p" in num else "wilcoxon_log_sd_ratio_p"
        m["p_crosses_0.05"] = (m[f"{pcol}_v1"] < ALPHA) != (m[f"{pcol}_v2"] < ALPHA)
        out.append(m)
    return out


def _bank_level(banks):
    rows = []
    for name, key in (("matched_prepost.csv", ["outcome", "bank"]), ("trend_slopes.csv", ["outcome", "bank", "period"]),
                      ("volatility_results.csv", ["outcome", "bank"])):
        a, b = pd.read_csv(V1_DIR / name), pd.read_csv(D.OUT / name)
        a, b = a[a.bank.isin(banks)], b[b.bank.isin(banks)]
        m = a.merge(b, on=key, suffixes=("_v1", "_v2"), how="outer")
        m.insert(0, "table", name.replace(".csv", ""))
        rows.append(m)
    return pd.concat(rows, ignore_index=True)


def run() -> dict:
    if not V1_DIR.is_dir():
        return {}
    added = _panel_rows()
    elig = _eligible()
    reg = _regression()
    rob = _robustness()
    interp = _interpretation()
    matched, vol = _summaries()
    banks = sorted(set(added["bank"])) if len(added) else []
    bank = _bank_level(banks) if banks else pd.DataFrame()
    files = {"comparison_rows_added.csv": added, "comparison_eligible_n.csv": elig, "comparison_regression.csv": reg,
             "comparison_robustness.csv": rob, "comparison_interpretation.csv": interp,
             "comparison_matched_prepost.csv": matched, "comparison_volatility.csv": vol, "comparison_bank_level.csv": bank}
    for f, df in files.items():
        df.to_csv(D.OUT / f, index=False)
    files = {f: pd.read_csv(D.OUT / f) for f in files}  # every number below is read back from the export
    (D.OUT / "comparison_v1_v2.md").write_text(_md(files), encoding="utf-8")
    return {"rows_added": len(added), "material_changes": int(reg["material_change"].sum())}


def _f(x, d=3):
    return "n/a" if pd.isna(x) else f"{x:.{d}f}"


def _md(F) -> str:
    add, el, reg, rob, it = (F["comparison_rows_added.csv"], F["comparison_eligible_n.csv"], F["comparison_regression.csv"],
                             F["comparison_robustness.csv"], F["comparison_interpretation.csv"])
    L = ["# Comparison: release v1 (97 bank-years) vs v2 (current)", "",
         f"v1: `IFRS9_release_2026-10-11_v1`, results in `thesis_results_v1/`. v2: `{D.RELEASE_ID}`, results in `thesis_results/`. "
         "Same code, estimators, seed and B = 9,999. Every number below is read from the comparison_*.csv files named in brackets.", "",
         "Material-change rule (set before comparing): the 5% decision changes under WCB or CR1, the sign changes, or the coefficient "
         "moves by at least 0.5 v1 CR1 standard errors.", "", "## 1. Rows added [comparison_rows_added.csv]", ""]
    for r in add.itertuples():
        L.append(f"- {r.change}: {r.bank} {r.year} ({r.tier}); {r.version_note}; source {r.source_url}")
    L += ["", "## 2. Eligible N by outcome [comparison_eligible_n.csv]", "", "| Outcome | v1 | v2 | Change | Pre v1→v2 | Post v1→v2 | Banks v1→v2 |",
          "|---|---|---|---|---|---|---|"]
    for r in el.itertuples():
        L.append(f"| {r.variable} | {r.eligible_N_v1} | {r.eligible_N_v2} | {r.eligible_N_change:+d} | {r.pre_v1}→{r.pre_v2} | "
                 f"{r.post_v1}→{r.post_v2} | {r.banks_v1}→{r.banks_v2} |")
    for title, model, term in (("3. Principal model M1 (bank FE, IFRS9_D)", "M1", "IFRS9_D"),
                               ("4. Tier model M4 (bank + year FE, Tier1 x IFRS9_D)", "M4", "Tier1_x_IFRS9_D")):
        s = reg[(reg.model == model) & (reg.term == term)]
        L += ["", f"## {title} [comparison_regression.csv]", "",
              "| Outcome | Coef v1 | Coef v2 | Δ in v1 SE | p CR1 v1→v2 | p WCB v1→v2 | WCB decision change | CR1 decision change | Material |",
              "|---|---|---|---|---|---|---|---|---|"]
        for r in s.itertuples():
            L.append(f"| {r.variable} | {_f(r.coef_v1)} | {_f(r.coef_v2)} | {_f(r.coef_change_in_v1_se, 2)} | {_f(r.p_cr1_tG1_v1)}→{_f(r.p_cr1_tG1_v2)} | "
                     f"{_f(r.p_wild_cluster_bootstrap_v1)}→{_f(r.p_wild_cluster_bootstrap_v2)} | {'yes' if r.decision_wcb_changed else 'no'} | "
                     f"{'yes' if r.decision_cr1_changed else 'no'} | {'YES' if r.material_change else 'no'} |")
    other = reg[~reg.model.isin(["M1", "M4"]) & reg.material_change]
    L += ["", "## 5. Other specifications (M0, M2, M3, M4s, M5) flagged material [comparison_regression.csv]", "",
          "All terms are listed, including controls (ln_assets, trend, Tier1 in M0).", ""]
    L += [f"- {r.variable} {r.model} {r.term}: {_f(r.coef_v1)} → {_f(r.coef_v2)} ({_f(r.coef_change_in_v1_se, 2)} v1 SE); WCB p "
          f"{_f(r.p_wild_cluster_bootstrap_v1)} → {_f(r.p_wild_cluster_bootstrap_v2)}; CR1 p {_f(r.p_cr1_tG1_v1)} → {_f(r.p_cr1_tG1_v2)}"
          for r in other.itertuples()] or ["- none"]
    rc = rob[rob.decision_wcb_changed | rob.sign_change]
    L += ["", "## 6. Sensitivity runs whose WCB decision or sign changed [comparison_robustness.csv]", ""]
    L += [f"- {r.variable} {r.model} {r.sensitivity}: coef {_f(r.coef_v1)} → {_f(r.coef_v2)}; WCB p {_f(r.p_wild_cluster_bootstrap_v1)} → "
          f"{_f(r.p_wild_cluster_bootstrap_v2)}" for r in rc.itertuples()] or ["- none"]
    L += ["", "## 7. Hypothesis decisions by objective [comparison_interpretation.csv]", ""]
    for r in it.itertuples():
        L.append(f"- {r.objective} {r.variable}: v1 '{r.h0_decision_v1}' → v2 '{r.h0_decision_v2}' "
                 f"({'CHANGED' if r.h0_decision_changed else 'unchanged'}); robustness label "
                 f"{'changed' if r.robustness_label_changed else 'unchanged'} ('{str(r.robustness_v2).split(';')[0]}')")
    m, v = F["comparison_matched_prepost.csv"], F["comparison_volatility.csv"]
    L += ["", "## 8. Matched pre/post and volatility [comparison_matched_prepost.csv, comparison_volatility.csv]", ""]
    for r in m.itertuples():
        L.append(f"- Matched {r.variable} ({r.group}): banks {r.banks_v1:.0f}→{r.banks_v2:.0f}; mean diff {_f(r.mean_diff_v1)}→{_f(r.mean_diff_v2)}; "
                 f"Wilcoxon p {_f(r.wilcoxon_signed_rank_p_v1)}→{_f(r.wilcoxon_signed_rank_p_v2)}"
                 f"{' (crosses 0.05)' if r[-1] is True else ''}")
    for r in v.itertuples():
        L.append(f"- Volatility {r.variable}: banks {r.banks_with_3_plus_each_regime_v1:.0f}→{r.banks_with_3_plus_each_regime_v2:.0f}; "
                 f"median SD ratio {_f(r.median_sd_ratio_v1, 2)}→{_f(r.median_sd_ratio_v2, 2)}; Wilcoxon p "
                 f"{_f(r.wilcoxon_log_sd_ratio_p_v1)}→{_f(r.wilcoxon_log_sd_ratio_p_v2)}{' (crosses 0.05)' if r[-1] is True else ''}")
    b = F["comparison_bank_level.csv"]
    L += ["", "## 9. Bank-level results for the banks with added rows [comparison_bank_level.csv]", ""]
    if len(b):
        mp = b[b.table == "matched_prepost"]
        for r in mp.itertuples():
            L.append(f"- {r.bank} {r.outcome}: n post {_f(r.n_post_v1, 0)}→{_f(r.n_post_v2, 0)}; post-minus-pre "
                     f"{_f(r.diff_post_minus_pre_v1)}→{_f(r.diff_post_minus_pre_v2)}"
                     f"{' (sign change)' if np.sign(r.diff_post_minus_pre_v1) != np.sign(r.diff_post_minus_pre_v2) else ''}")
    n_mat = int(reg[reg.model.isin(["M1", "M4"])].material_change.sum())
    n_dec = int(it.h0_decision_changed.sum())
    L += ["", "## 10. Summary", "",
          f"- Principal (M1) and tier (M4) estimates flagged material under the rule: {n_mat} of "
          f"{int(reg.model.isin(['M1', 'M4']).sum())} [comparison_regression.csv].",
          f"- Objective-level H0 decisions changed: {n_dec} of {len(it)} [comparison_interpretation.csv].", ""]
    return "\n".join(L)
