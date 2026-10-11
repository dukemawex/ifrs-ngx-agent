"""Compare the current thesis results (thesis_results/, latest frozen release) with the archived results of the
previous release (thesis_results_<PREV>/). Column suffixes: _prev = previous release, _new = current release.

Writes thesis_results/comparison_*.csv and comparison_<PREV>_<NEW>.md. Every number in the markdown is read from those CSVs.

Material-change rule (fixed before looking at the results):
  - the 5% hypothesis decision changes under the wild-cluster bootstrap (WCB) or under CR1 t(G-1); or
  - the coefficient changes sign; or
  - |coefficient change| >= 0.5 x the previous CR1 standard error; or
  - a bank's post-minus-pre direction (increase / decrease) for an outcome changes or appears/disappears.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from . import data as D

PREV = "v2"  # release compared against; its results are archived in thesis_results_<PREV>/
NEW = "v3"
V1_DIR = D.ROOT / f"thesis_results_{PREV}"
V1_REL = D.ROOT / "releases" / f"IFRS9_release_2026-10-11_{PREV}"
ALPHA = 0.05
KEYS = ["outcome", "variable", "model", "term"]


def _panel_rows():
    a = pd.read_csv(V1_REL / "verified_panel.csv")[["bank", "year"]]
    b = pd.read_csv(D.REL / "verified_panel.csv")
    m = b.merge(a.assign(_prev=1), on=["bank", "year"], how="left")
    added = m[m["_prev"].isna()].drop(columns="_prev")
    removed = a.merge(b[["bank", "year"]].assign(_new=1), on=["bank", "year"], how="left")
    removed = removed[removed["_new"].isna()]
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
    out = a[["variable"] + cols].join(b[cols], lsuffix="_prev", rsuffix="_new")
    for c in cols:
        out[f"{c}_change"] = out[f"{c}_new"] - out[f"{c}_prev"]
    return out.reset_index()


def _decision(p):
    return np.where(p < ALPHA, "reject H0", "do not reject H0")


def _regression():
    a = pd.read_csv(V1_DIR / "regression_results.csv")
    b = pd.read_csv(D.OUT / "regression_results.csv")
    cols = ["coef", "se_cr1", "p_conventional", "p_cr1_tG1", "p_wild_cluster_bootstrap", "N", "banks"]
    m = a[KEYS + ["specification"] + cols].merge(b[KEYS + cols], on=KEYS, suffixes=("_prev", "_new"), how="outer")
    m["coef_change"] = m["coef_new"] - m["coef_prev"]
    m["coef_change_in_prev_se"] = m["coef_change"] / m["se_cr1_prev"]
    m["sign_change"] = np.sign(m["coef_prev"]) != np.sign(m["coef_new"])
    for t, c in (("wcb", "p_wild_cluster_bootstrap"), ("cr1", "p_cr1_tG1"), ("conventional", "p_conventional")):
        m[f"decision_{t}_prev"] = _decision(m[f"{c}_prev"])
        m[f"decision_{t}_new"] = _decision(m[f"{c}_new"])
        m[f"decision_{t}_changed"] = m[f"decision_{t}_prev"] != m[f"decision_{t}_new"]
    m["material_change"] = m["decision_wcb_changed"] | m["decision_cr1_changed"] | m["sign_change"] | (m["coef_change_in_prev_se"].abs() >= 0.5)
    return m


def _robustness():
    a = pd.read_csv(V1_DIR / "robustness_results.csv")
    b = pd.read_csv(D.OUT / "robustness_results.csv")
    k = ["outcome", "variable", "sensitivity", "model", "term"]
    m = a[k + ["coef", "p_wild_cluster_bootstrap", "N"]].merge(b[k + ["coef", "p_wild_cluster_bootstrap", "N"]], on=k, how="outer",
                                                              suffixes=("_prev", "_new"))
    m["decision_wcb_changed"] = (m["p_wild_cluster_bootstrap_prev"] < ALPHA) != (m["p_wild_cluster_bootstrap_new"] < ALPHA)
    m["sign_change"] = np.sign(m["coef_prev"]) != np.sign(m["coef_new"])
    return m


def _interpretation():
    a = pd.read_csv(V1_DIR / "interpretation.csv")
    b = pd.read_csv(D.OUT / "interpretation.csv")
    k = ["objective", "outcome", "variable", "term"]
    cols = ["usable_sample", "coefficient_pp", "p_wild_cluster_bootstrap", "p_cr1_tG1", "robustness", "h0_decision"]
    m = a[k + cols].merge(b[k + cols], on=k, suffixes=("_prev", "_new"), how="outer")
    m["h0_decision_changed"] = m["h0_decision_prev"].str.split(";").str[0] != m["h0_decision_new"].str.split(";").str[0]
    cat = lambda x: x.fillna("").str.split(r"[:;]", regex=True).str[0].str.strip()  # category only (robust / not fully robust / primary not significant)
    m["robustness_label_changed"] = cat(m["robustness_prev"]) != cat(m["robustness_new"])
    return m


def _summaries():
    out = []
    for name, key in (("matched_prepost_summary.csv", ["outcome", "variable", "group"]),
                      ("volatility_results_summary.csv", ["outcome", "variable"])):
        a, b = pd.read_csv(V1_DIR / name), pd.read_csv(D.OUT / name)
        num = [c for c in a.columns if c not in key and pd.api.types.is_numeric_dtype(a[c])]
        m = a[key + num].merge(b[key + num], on=key, suffixes=("_prev", "_new"), how="outer")
        m.insert(0, "table", name.replace(".csv", ""))
        pcol = "wilcoxon_signed_rank_p" if "wilcoxon_signed_rank_p" in num else "wilcoxon_log_sd_ratio_p"
        m["p_crosses_0.05"] = (m[f"{pcol}_prev"] < ALPHA) != (m[f"{pcol}_new"] < ALPHA)
        out.append(m)
    return out


def _bank_level(banks):
    rows = []
    for name, key in (("matched_prepost.csv", ["outcome", "bank"]), ("trend_slopes.csv", ["outcome", "bank", "period"]),
                      ("volatility_results.csv", ["outcome", "bank"])):
        a, b = pd.read_csv(V1_DIR / name), pd.read_csv(D.OUT / name)
        a, b = a[a.bank.isin(banks)], b[b.bank.isin(banks)]
        m = a.merge(b, on=key, suffixes=("_prev", "_new"), how="outer")
        m.insert(0, "table", name.replace(".csv", ""))
        rows.append(m)
    return pd.concat(rows, ignore_index=True)


def _bank_classification():
    """Direction of each bank's matched post-minus-pre mean difference, previous vs current release."""
    a, b = pd.read_csv(V1_DIR / "matched_prepost.csv"), pd.read_csv(D.OUT / "matched_prepost.csv")
    m = a[["outcome", "bank", "tier", "n_pre", "n_post", "diff_post_minus_pre"]].merge(
        b[["outcome", "bank", "tier", "n_pre", "n_post", "diff_post_minus_pre"]], on=["outcome", "bank", "tier"], how="outer", suffixes=("_prev", "_new"))
    lab = lambda x: "not classifiable" if pd.isna(x) else ("increase" if x > 0 else ("decrease" if x < 0 else "no change"))
    m["direction_prev"] = m["diff_post_minus_pre_prev"].map(lab)
    m["direction_new"] = m["diff_post_minus_pre_new"].map(lab)
    m["classification_changed"] = m["direction_prev"] != m["direction_new"]
    return m.sort_values(["outcome", "bank"])


def _going_concern():
    out = []
    for tag, d in (("prev", V1_DIR), ("new", D.OUT)):
        cov = pd.read_csv(d / "going_concern_coverage.csv")
        ev = pd.read_csv(d / "going_concern_events.csv")
        out.append({"release": tag, "events": len(ev), "event_bank_years": "; ".join(f"{r.bank} {r.year}" for r in ev.itertuples()),
                    "coded_bank_years": int(pd.read_csv(d / "variables_eligible_n.csv").set_index("outcome").loc["gcu", "eligible_N"])})
    return pd.DataFrame(out)


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
    cls = _bank_classification()
    gc = _going_concern()
    files = {"comparison_rows_added.csv": added, "comparison_eligible_n.csv": elig, "comparison_regression.csv": reg,
             "comparison_robustness.csv": rob, "comparison_interpretation.csv": interp,
             "comparison_matched_prepost.csv": matched, "comparison_volatility.csv": vol, "comparison_bank_level.csv": bank,
             "comparison_bank_classification.csv": cls, "comparison_going_concern.csv": gc}
    for f, df in files.items():
        df.to_csv(D.OUT / f, index=False)
    files = {f: pd.read_csv(D.OUT / f) for f in files}  # every number below is read back from the export
    (D.OUT / f"comparison_{PREV}_{NEW}.md").write_text(_md(files), encoding="utf-8")
    return {"previous_release": PREV, "rows_added": int((added["change"] == "added").sum()), "material_changes": int(reg["material_change"].sum()),
            "bank_classification_changes": int(cls["classification_changed"].sum())}


def _f(x, d=3):
    return "n/a" if pd.isna(x) else f"{x:.{d}f}"


def _md(F) -> str:
    add, el, reg, rob, it = (F["comparison_rows_added.csv"], F["comparison_eligible_n.csv"], F["comparison_regression.csv"],
                             F["comparison_robustness.csv"], F["comparison_interpretation.csv"])
    L = [f"# Comparison: release {PREV} vs {NEW} (current)", "",
         f"{PREV}: `IFRS9_release_2026-10-11_{PREV}`, results in `thesis_results_{PREV}/`. {NEW}: `{D.RELEASE_ID}`, results in `thesis_results/`. "
         "Same code, estimators, seed and B = 9,999. Every number below is read from the comparison_*.csv files named in brackets.", "",
         "Material-change rule (set before comparing): the 5% decision changes under WCB or CR1, the sign changes, or the coefficient "
         "moves by at least 0.5 previous CR1 standard errors.", "", "## 1. Rows added [comparison_rows_added.csv]", ""]
    for r in add.itertuples():
        L.append(f"- {r.change}: {r.bank} {r.year} ({r.tier}); {r.version_note}; source {r.source_url}")
    L += ["", "## 2. Eligible N by outcome [comparison_eligible_n.csv]", "", f"| Outcome | {PREV} | {NEW} | Change | Pre {PREV}→{NEW} | Post {PREV}→{NEW} | Banks {PREV}→{NEW} |",
          "|---|---|---|---|---|---|---|"]
    for r in el.itertuples():
        L.append(f"| {r.variable} | {r.eligible_N_prev} | {r.eligible_N_new} | {r.eligible_N_change:+d} | {r.pre_prev}→{r.pre_new} | "
                 f"{r.post_prev}→{r.post_new} | {r.banks_prev}→{r.banks_new} |")
    for title, model, term in (("3. Principal model M1 (bank FE, IFRS9_D)", "M1", "IFRS9_D"),
                               ("4. Tier model M4 (bank + year FE, Tier1 x IFRS9_D)", "M4", "Tier1_x_IFRS9_D")):
        s = reg[(reg.model == model) & (reg.term == term)]
        L += ["", f"## {title} [comparison_regression.csv]", "",
              f"| Outcome | Coef {PREV} | Coef {NEW} | Δ in {PREV} SE | p CR1 {PREV}→{NEW} | p WCB {PREV}→{NEW} | WCB decision change | CR1 decision change | Material |",
              "|---|---|---|---|---|---|---|---|---|"]
        for r in s.itertuples():
            L.append(f"| {r.variable} | {_f(r.coef_prev)} | {_f(r.coef_new)} | {_f(r.coef_change_in_prev_se, 2)} | {_f(r.p_cr1_tG1_prev)}→{_f(r.p_cr1_tG1_new)} | "
                     f"{_f(r.p_wild_cluster_bootstrap_prev)}→{_f(r.p_wild_cluster_bootstrap_new)} | {'yes' if r.decision_wcb_changed else 'no'} | "
                     f"{'yes' if r.decision_cr1_changed else 'no'} | {'YES' if r.material_change else 'no'} |")
    other = reg[~reg.model.isin(["M1", "M4"]) & reg.material_change]
    L += ["", "## 5. Other specifications (M0, M2, M3, M4s, M5) flagged material [comparison_regression.csv]", "",
          "All terms are listed, including controls (ln_assets, trend, Tier1 in M0).", ""]
    L += [f"- {r.variable} {r.model} {r.term}: {_f(r.coef_prev)} → {_f(r.coef_new)} ({_f(r.coef_change_in_prev_se, 2)} prev SE); WCB p "
          f"{_f(r.p_wild_cluster_bootstrap_prev)} → {_f(r.p_wild_cluster_bootstrap_new)}; CR1 p {_f(r.p_cr1_tG1_prev)} → {_f(r.p_cr1_tG1_new)}"
          for r in other.itertuples()] or ["- none"]
    both = rob.coef_prev.notna() & rob.coef_new.notna()
    rc = rob[both & (rob.decision_wcb_changed | rob.sign_change)]
    L += ["", "## 6. Sensitivity runs whose WCB decision or sign changed (sensitivities present in both releases) [comparison_robustness.csv]", ""]
    L += [f"- {r.variable} {r.model} {r.sensitivity}: coef {_f(r.coef_prev)} → {_f(r.coef_new)}; WCB p {_f(r.p_wild_cluster_bootstrap_prev)} → "
          f"{_f(r.p_wild_cluster_bootstrap_new)}" for r in rc.itertuples()] or ["- none"]
    s6 = rob[rob.coef_prev.isna() & rob.coef_new.notna()]
    L += ["", "New sensitivity in this release (no previous counterpart):"]
    L += [f"- {r.variable} {r.model} {r.sensitivity}: coef {_f(r.coef_new)}; WCB p {_f(r.p_wild_cluster_bootstrap_new)}; N {_f(r.N_new, 0)}" for r in s6.itertuples()] or ["- none"]
    L += ["", "## 7. Hypothesis decisions by objective [comparison_interpretation.csv]", ""]
    for r in it.itertuples():
        L.append(f"- {r.objective} {r.variable}: {PREV} '{r.h0_decision_prev}' → {NEW} '{r.h0_decision_new}' "
                 f"({'CHANGED' if r.h0_decision_changed else 'unchanged'}); robustness label "
                 f"{'changed' if r.robustness_label_changed else 'unchanged'} ('{str(r.robustness_new).split(';')[0]}')")
    m, v = F["comparison_matched_prepost.csv"], F["comparison_volatility.csv"]
    L += ["", "## 8. Matched pre/post and volatility [comparison_matched_prepost.csv, comparison_volatility.csv]", ""]
    for r in m.itertuples():
        L.append(f"- Matched {r.variable} ({r.group}): banks {r.banks_prev:.0f}→{r.banks_new:.0f}; mean diff {_f(r.mean_diff_prev)}→{_f(r.mean_diff_new)}; "
                 f"Wilcoxon p {_f(r.wilcoxon_signed_rank_p_prev)}→{_f(r.wilcoxon_signed_rank_p_new)}"
                 f"{' (crosses 0.05)' if r[-1] is True else ''}")
    for r in v.itertuples():
        L.append(f"- Volatility {r.variable}: banks {r.banks_with_3_plus_each_regime_prev:.0f}→{r.banks_with_3_plus_each_regime_new:.0f}; "
                 f"median SD ratio {_f(r.median_sd_ratio_prev, 2)}→{_f(r.median_sd_ratio_new, 2)}; Wilcoxon p "
                 f"{_f(r.wilcoxon_log_sd_ratio_p_prev)}→{_f(r.wilcoxon_log_sd_ratio_p_new)}{' (crosses 0.05)' if r[-1] is True else ''}")
    cls = F["comparison_bank_classification.csv"]
    flip = cls[(cls.direction_prev.isin(["increase", "decrease"])) & (cls.direction_new.isin(["increase", "decrease"])) & cls.classification_changed]
    newc = cls[(cls.direction_prev == "not classifiable") & (cls.direction_new != "not classifiable")]
    lost = cls[(cls.direction_prev != "not classifiable") & (cls.direction_new == "not classifiable")]
    L += ["", "## 9. Bank-level direction (matched post-minus-pre bank means) [comparison_bank_classification.csv]", "",
          f"- Direction reversed (increase <-> decrease): {len(flip)}"]
    L += [f"  - {r.bank} {r.outcome}: {r.direction_prev} ({_f(r.diff_post_minus_pre_prev)}) -> {r.direction_new} ({_f(r.diff_post_minus_pre_new)}); "
          f"n post {_f(r.n_post_prev, 0)}->{_f(r.n_post_new, 0)}, n pre {_f(r.n_pre_prev, 0)}->{_f(r.n_pre_new, 0)}" for r in flip.itertuples()]
    L += [f"- Newly classifiable (bank now observed in both regimes): {len(newc)}"]
    L += [f"  - {r.bank} {r.outcome}: {r.direction_new} ({_f(r.diff_post_minus_pre_new)})" for r in newc.itertuples()]
    L += [f"- No longer classifiable: {len(lost)}"] + [f"  - {r.bank} {r.outcome}" for r in lost.itertuples()]
    unchanged = cls[~cls.classification_changed & (cls.direction_new != "not classifiable")]
    L += [f"- Unchanged direction: {len(unchanged)} bank-outcome pairs"]
    gc = F["comparison_going_concern.csv"].set_index("release")
    L += ["", "## 10. Going-concern events [comparison_going_concern.csv]", "",
          f"- Events {int(gc.loc['prev', 'events'])} -> {int(gc.loc['new', 'events'])} ({gc.loc['new', 'event_bank_years']}); "
          f"coded bank-years {int(gc.loc['prev', 'coded_bank_years'])} -> {int(gc.loc['new', 'coded_bank_years'])}."]
    n_mat = int(reg[reg.model.isin(["M1", "M4"])].material_change.sum())
    n_dec = int(it.h0_decision_changed.sum())
    L += ["", "## 11. Summary", "",
          f"- Principal (M1) and tier (M4) estimates flagged material under the rule: {n_mat} of "
          f"{int(reg.model.isin(['M1', 'M4']).sum())} [comparison_regression.csv].",
          f"- Objective-level H0 decisions changed: {n_dec} of {len(it)} [comparison_interpretation.csv].",
          f"- Bank direction reversals: {len(flip)}; newly classified bank-outcome pairs: {len(newc)} [comparison_bank_classification.csv].", ""]
    return "\n".join(L)
