"""Thesis figures (static, print). Palette: validated reference categorical slots 1-2 (Tier 1 blue, Tier 2 orange;
all-pairs CVD dE 9.2 / normal 24.0 with slot 3), blue ordinal ramp for pre/post counts, grey context lines.
One y-axis per panel, solid hairline grid, selective direct labels, legend for >= 2 series."""
from __future__ import annotations

import numpy as np
import pandas as pd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from . import data as D  # noqa: E402

T1, T2 = "#2a78d6", "#eb6834"
PRE, POST = "#86b6ef", "#1c5cab"
INK, INK2, MUTED, GRID, CONTEXT, SURF = "#0b0b0b", "#52514e", "#8a8984", "#e6e5e0", "#c9c8c2", "#ffffff"
TIERC = {"Tier 1": T1, "Tier 2": T2}
plt.rcParams.update({
    "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF, "font.size": 9,
    "axes.edgecolor": GRID, "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2, "text.color": INK,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6, "grid.linestyle": "-", "axes.axisbelow": True,
    "axes.spines.top": False, "axes.spines.right": False, "axes.titleweight": "bold", "axes.titlesize": 10,
    "axes.titlelocation": "left", "legend.frameon": False, "legend.fontsize": 8,
})


def _save(fig, out, name, note):
    fig.text(0.01, -0.01, note, fontsize=7, color=MUTED, ha="left", va="top", wrap=True)
    for ext in ("png", "pdf"):
        fig.savefig(out / f"{name}.{ext}", dpi=300, bbox_inches="tight")
    plt.close(fig)
    return name


def _adopt(ax):
    ax.axvline(2017.5, color=MUTED, lw=0.8)
    ax.text(2017.55, 1.0, "IFRS 9 (2018)", transform=ax.get_xaxis_transform(), fontsize=7, color=INK2, va="top")


def coverage(sp, out):
    grid = sp["grid"]
    fig, ax = plt.subplots(figsize=(7.2, 4.6))
    banks = D.COHORT + ["FCMB"]
    tiers = {r.bank: r.tier for r in sp["coverage"].itertuples()}
    order = [b for b in banks if tiers.get(b) == "Tier 1"] + [b for b in banks if tiers.get(b) == "Tier 2"]
    for i, b in enumerate(order):
        for j, y in enumerate(D.YEARS):
            if b == "FCMB":
                ax.add_patch(plt.Rectangle((j, i), 0.92, 0.88, color="#f0efec", lw=0))
                continue
            sel = b in grid.index and y in grid.columns and isinstance(grid.loc[b, y], str)
            ax.add_patch(plt.Rectangle((j, i), 0.92, 0.88, color=TIERC[tiers[b]] if sel else "#f0efec", lw=0))
    ax.text(2.5, order.index("FCMB") + 0.45, "excluded from cohort (no standalone bank series)", ha="center", va="center", fontsize=7, color=INK2,
            bbox=dict(facecolor="#f0efec", edgecolor="none", pad=1))
    ax.set_xlim(0, 10); ax.set_ylim(len(order), 0)
    ax.set_xticks(np.arange(10) + 0.46, D.YEARS); ax.set_yticks(np.arange(len(order)) + 0.44, [f"{b} ({tiers[b][-1]})" for b in order])
    ax.grid(False); ax.tick_params(length=0)
    ax.axvline(5 - 0.04, color=INK, lw=1)
    handles = [plt.Rectangle((0, 0), 1, 1, color=T1), plt.Rectangle((0, 0), 1, 1, color=T2), plt.Rectangle((0, 0), 1, 1, color="#f0efec")]
    ax.legend(handles, ["Selected, Tier 1", "Selected, Tier 2", "Not available / excluded"], loc="lower left", bbox_to_anchor=(0, 1.0), ncol=3)
    n_sel = sum(b in grid.index and y in grid.columns and isinstance(grid.loc[b, y], str) for b in D.COHORT for y in D.YEARS)
    ax.set_title(f"Figure 1. Selected bank-years in the frozen release\n(12-bank cohort; {n_sel} of {len(D.COHORT) * len(D.YEARS)} positions)", pad=26)
    return _save(fig, out, "fig01_sample_coverage", f"Source: releases/{D.RELEASE_ID}/verified_panel.csv. Vertical rule: IFRS 9 adoption (2018).")


def eligible_n(sp, out):
    e = sp["eligibility"].iloc[::-1]
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    y = np.arange(len(e))
    ax.barh(y, e["pre"], color=PRE, height=0.6, label="Pre-IFRS 9 (2013-2017)")
    ax.barh(y, e["post"], left=e["pre"] + 0.4, color=POST, height=0.6, label="Post-IFRS 9 (2018-2022)")
    for yi, r in zip(y, e.itertuples()):
        ax.text(r.pre + r.post + 1.2, yi, f"N = {r.eligible_N}  ({r.banks} banks; {r.analysis_role})", va="center", fontsize=7, color=INK2)
    ax.set_yticks(y, e["variable"]); ax.set_xlim(0, 140); ax.set_xlabel("Eligible bank-years (inferential sample)")
    ax.grid(axis="y", visible=False)
    ax.set_title("Figure 2. Eligible observations by outcome and regime")
    ax.legend(loc="lower right")
    return _save(fig, out, "fig02_eligible_n", "Source: thesis_results/tables/table2_variables_eligible_n.csv.")


def trend(O, k, num, out):
    d = O[k]
    inf = d[d.inferential_use]
    fig, ax = plt.subplots(figsize=(7.2, 4.0))
    extreme = inf[inf.unity_negative_capital] if k in ("car", "eqta", "leverage") else inf.iloc[0:0]
    body = inf.drop(extreme.index)
    for b, g in body.groupby("bank"):
        ax.plot(g.year, g.value, color=CONTEXT, lw=0.8, zorder=1)
    for t, c in TIERC.items():
        m = inf[inf.tier == t].groupby("year")["value"].median()
        ax.plot(m.index, m.values, color=c, lw=2.2, marker="o", ms=4.5, zorder=3, label=f"{t} median",
                markeredgecolor=SURF, markeredgewidth=1)
    _adopt(ax)
    lab, short, units = D.OUTCOMES[k][1], D.OUTCOMES[k][2], D.OUTCOMES[k][3]
    ax.set_xlim(2012.6, 2023.2); ax.set_xticks(D.YEARS); ax.set_ylabel(f"{short} ({units})")
    ax.plot([], [], color=CONTEXT, lw=0.8, label="Individual banks")
    ax.legend(loc="best")
    note = f"Medians use all eligible rows (incl. Unity). Source: thesis_results/trend_values.csv (outcome = {k})."
    if len(extreme):
        lo, hi = body.value.min(), body.value.max()
        pad = (hi - lo) * 0.08
        ax.set_ylim(lo - pad, hi + pad)
        note = (f"Not drawn: Unity rows flagged negative capital (equity, CAR or regulatory capital < 0) {', '.join(f'{int(r.year)}: {r.value:.1f}' for r in extreme.itertuples())}. " + note)
    ax.set_title(f"Figure {num}. {short}: bank paths and tier medians, 2013-2022")
    return _save(fig, out, f"fig{num:02d}_trend_{k}", note)


def dumbbell(mb, out):
    ks = ["allr", "impairment_assets", "car", "roa", "ocf_ratio", "eqta"]
    fig, axes = plt.subplots(2, 3, figsize=(10, 7.2))
    for ax, k in zip(axes.flat, ks):
        s = mb[mb.outcome == k].sort_values("diff_post_minus_pre").reset_index(drop=True)
        title = D.OUTCOMES[k][2] + " (%)"
        if k in ("car", "eqta"):
            u = s[s.bank == "Unity"]
            if len(u):
                title += f"\nUnity omitted (pre {u.mean_pre.iloc[0]:.1f}, post {u.mean_post.iloc[0]:.1f})"
            s = s[s.bank != "Unity"].reset_index(drop=True)
        for i, r in s.iterrows():
            c = TIERC[r.tier]
            ax.plot([r.mean_pre, r.mean_post], [i, i], color=CONTEXT, lw=1.2, zorder=1)
            ax.scatter(r.mean_pre, i, s=30, facecolor=SURF, edgecolor=c, lw=1.5, zorder=3)
            ax.scatter(r.mean_post, i, s=30, color=c, edgecolor=SURF, lw=0.8, zorder=4)
        ax.set_yticks(range(len(s)), s.bank, fontsize=7.5)
        ax.set_title(title, fontsize=9)
        ax.grid(axis="y", visible=False)
    h = [plt.Line2D([], [], marker="o", ls="", mfc=SURF, mec=INK2, label="Pre-IFRS 9 bank mean"),
         plt.Line2D([], [], marker="o", ls="", color=INK2, label="Post-IFRS 9 bank mean"),
         plt.Line2D([], [], marker="s", ls="", color=T1, label="Tier 1"), plt.Line2D([], [], marker="s", ls="", color=T2, label="Tier 2")]
    fig.suptitle("Figure 10. Matched pre/post comparison: bank means before and after IFRS 9 adoption", x=0.01, ha="left", fontweight="bold")
    fig.legend(handles=h, loc="upper left", ncol=4, bbox_to_anchor=(0.01, 0.955))
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    return _save(fig, out, "fig10_matched_prepost", "Banks observed in both regimes; rows flagged non-comparable removed. Source: thesis_results/matched_prepost.csv.")


def forest(reg, desc, out, model, term, num, title, name):
    ks = D.CORE
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    for i, k in enumerate(ks):
        r = reg[(reg.outcome == k) & (reg.model == model) & (reg.term == term)].iloc[0]
        sd = desc[(desc.outcome == k) & (desc.group == "Pre-IFRS 9 (2013-2017)")]["sd"].iloc[0]
        c, lo, hi = r.coef / sd, r.ci95_low_cr1 / sd, r.ci95_high_cr1 / sd
        col = T1 if r.p_wild_cluster_bootstrap < 0.05 else INK2
        ax.plot([lo, hi], [i, i], color=col, lw=2)
        ax.scatter(c, i, s=40, color=col, edgecolor=SURF, lw=1, zorder=3)
        ax.text(1.02, i, f"{r.coef:+.2f} pp; WCB p = {r.p_wild_cluster_bootstrap:.3f}; N = {int(r.N)}", transform=ax.get_yaxis_transform(), va="center", fontsize=7, color=INK2)
    ax.axvline(0, color=INK, lw=0.8)
    ax.set_yticks(range(len(ks)), [D.OUTCOMES[k][2] for k in ks]); ax.invert_yaxis()
    ax.set_xlabel("Coefficient / SD of the outcome in the pre-IFRS 9 period (bars: 95% CI, CR1 with t(G-1))")
    ax.grid(axis="y", visible=False)
    ax.legend(handles=[plt.Line2D([], [], color=T1, lw=2, label="Wild-cluster-bootstrap p < 0.05"),
                       plt.Line2D([], [], color=INK2, lw=2, label="p >= 0.05")], loc="lower left", bbox_to_anchor=(0, 1.0), ncol=2)
    ax.set_title(f"Figure {num}. {title}", pad=24)
    return _save(fig, out, name, "Colour follows the wild-cluster-bootstrap p; bars are CR1 t(G-1) intervals, so the two can disagree (equity/assets, leverage). "
                 "Raw coefficients (percentage points) at right. Source: thesis_results/regression_results.csv.")


def robustness_fig(rob, out, model, num, name, title):
    ks = D.CORE
    sens = list(dict.fromkeys(rob["sensitivity"]))
    fig, axes = plt.subplots(len(ks), 1, figsize=(7.2, 1.15 * len(ks) + 0.6), sharex=False)
    for ax, k in zip(axes, ks):
        s = rob[(rob.outcome == k) & (rob.model == model)].set_index("sensitivity").reindex(sens).dropna(subset=["coef"])
        for i, (sid, r) in enumerate(s.iterrows()):
            col = T1 if r.p_wild_cluster_bootstrap < 0.05 else INK2
            ax.plot([r.ci95_low_cr1, r.ci95_high_cr1], [i, i], color=col, lw=1.6)
            ax.scatter(r.coef, i, s=22, color=col, zorder=3, edgecolor=SURF, lw=0.8)
        ax.axvline(0, color=INK, lw=0.7)
        ax.set_yticks(range(len(s)), [x.split("_", 1)[0] for x in s.index], fontsize=7)
        ax.invert_yaxis(); ax.grid(axis="y", visible=False)
        ax.set_title(D.OUTCOMES[k][2] + " (pp)", fontsize=8.5)
    fig.suptitle(f"Figure {num}. {title}", x=0.01, ha="left", fontweight="bold")
    fig.legend(handles=[plt.Line2D([], [], color=T1, lw=2, label="WCB p < 0.05"), plt.Line2D([], [], color=INK2, lw=2, label="p >= 0.05 (bars: CR1 95% CI)")],
               loc="upper left", bbox_to_anchor=(0.01, 0.975), ncol=2, fontsize=7.5)
    fig.tight_layout(rect=(0, 0.0, 1, 0.955))
    return _save(fig, out, name, "S0 primary; S1 drop fallback rows; S2 add exception rows; S3 drop Unity negative capital; S4 drop 2020; S5 drop Unity. "
                 "Source: thesis_results/robustness_results.csv.")


def jackknife_fig(jk, out, num):
    ks = D.CORE
    fig, ax = plt.subplots(figsize=(7.2, 4.2))
    for i, k in enumerate(ks):
        s = jk[(jk.outcome == k) & (jk.model == "M1") & (jk.dropped_bank != "SUMMARY")]
        full = s.full_sample_coef.iloc[0]
        sc = s.coef / abs(full) if full else s.coef
        ax.scatter(sc, np.full(len(s), i), s=18, color=CONTEXT, zorder=2)
        uni = s[s.dropped_bank == "Unity"]
        if len(uni):
            ax.scatter(uni.coef / abs(full), [i], s=30, color=T2, zorder=3)
        ax.scatter([np.sign(full)], [i], s=40, marker="D", color=T1, zorder=4)
    ax.axvline(0, color=INK, lw=0.8)
    ax.set_yticks(range(len(ks)), [D.OUTCOMES[k][2] for k in ks]); ax.invert_yaxis(); ax.grid(axis="y", visible=False)
    ax.set_xlabel("Leave-one-bank-out IFRS9_D coefficient / |full-sample coefficient| (principal model M1)")
    ax.legend(handles=[plt.Line2D([], [], marker="D", ls="", color=T1, label="Full sample"),
                       plt.Line2D([], [], marker="o", ls="", color=CONTEXT, label="One bank dropped"),
                       plt.Line2D([], [], marker="o", ls="", color=T2, label="Unity dropped")], loc="lower left")
    ax.set_title(f"Figure {num}. Influence of individual banks on the IFRS 9 coefficient")
    return _save(fig, out, f"fig{num:02d}_jackknife", "Values left of 0 indicate a sign reversal when that bank is dropped. Source: thesis_results/jackknife_results.csv.")


def volatility_fig(vb, out, num):
    ks = ["allr", "impairment_assets", "car", "roa", "ocf_ratio", "eqta"]
    fig, axes = plt.subplots(2, 3, figsize=(10, 6.6))
    for ax, k in zip(axes.flat, ks):
        s = vb[vb.outcome == k]
        if s.empty:
            ax.set_visible(False); continue
        for r in s.itertuples():
            ax.scatter(r.sd_pre, r.sd_post, s=30, color=TIERC[r.tier], edgecolor=SURF, lw=0.8, zorder=3)
        lim = max(s.sd_pre.max(), s.sd_post.max()) * 1.15
        lo = min(s.sd_pre.min(), s.sd_post.min()) * 0.8
        ax.plot([lo, lim], [lo, lim], color=MUTED, lw=0.8)
        ax.set_xscale("log"); ax.set_yscale("log")
        from matplotlib.ticker import FuncFormatter, LogLocator
        fmt = FuncFormatter(lambda v, _: f"{v:g}")
        for axis in (ax.xaxis, ax.yaxis):
            axis.set_major_locator(LogLocator(base=10, subs=(1.0, 2.0, 5.0)))
            axis.set_major_formatter(fmt); axis.set_minor_formatter(FuncFormatter(lambda v, _: ""))
        ax.set_title(f"{D.OUTCOMES[k][2]} ({len(s)} banks)", fontsize=9)
        ax.set_xlabel("SD pre (pp)", fontsize=7.5); ax.set_ylabel("SD post (pp)", fontsize=7.5)
        top = s.loc[(np.log(s.sd_post / s.sd_pre)).abs().idxmax()]
        ax.annotate(top.bank, (top.sd_pre, top.sd_post), fontsize=6.5, color=INK2, xytext=(4, 2), textcoords="offset points")
    h = [plt.Line2D([], [], marker="o", ls="", color=T1, label="Tier 1"), plt.Line2D([], [], marker="o", ls="", color=T2, label="Tier 2"),
         plt.Line2D([], [], color=MUTED, label="Equal volatility")]
    fig.suptitle(f"Figure {num}. Within-bank volatility before and after IFRS 9 (exploratory; >= 3 observations per regime)", x=0.01, ha="left", fontweight="bold")
    fig.legend(handles=h, loc="upper left", ncol=3, bbox_to_anchor=(0.01, 0.955))
    fig.tight_layout(rect=(0, 0, 1, 0.92))
    return _save(fig, out, f"fig{num:02d}_volatility", "Points above the line: higher SD after adoption. Source: thesis_results/volatility_results.csv.")


def unity_gc(up, O, out, num):
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.9))
    p = D.panel()
    for ax, (col, lab) in zip(axes, (("car", "CAR (%)"), ("eqta", "Equity / assets (%)"))):
        others = p[p.bank != "Unity"].groupby("year")[col].median()
        ax.plot(others.index, others.values, color=CONTEXT, lw=2, label="Other banks, median")
        full = up.set_index("year").reindex(D.YEARS)
        ax.plot(full.index, full[col], color=T2, lw=2, marker="o", ms=4.5, label="Unity (gap = no value)", markeredgecolor=SURF)
        u = up.dropna(subset=[col])
        ev = u[u.event]
        ax.scatter(ev.year, ev[col], s=90, facecolor="none", edgecolor=INK, lw=1.5, zorder=4, label="Going-concern MU event")
        for r in ev.itertuples():
            ax.annotate(f"{r.year}", (r.year, getattr(r, col)), xytext=(0, -14), textcoords="offset points", ha="center", fontsize=7, color=INK)
        _adopt(ax); ax.axhline(0, color=INK, lw=0.6)
        ax.set_xticks(D.YEARS); ax.set_ylabel(lab); ax.set_xlim(2012.6, 2022.6)
    axes[0].legend(loc="lower left", fontsize=7)
    fig.suptitle(f"Figure {num}. Unity Bank: capital indicators around the three going-concern events (2019, 2021, 2022)", x=0.01, ha="left", fontweight="bold")
    fig.tight_layout(rect=(0, 0.03, 1, 0.95))
    return _save(fig, out, f"fig{num:02d}_going_concern_unity", "Events = auditor 'Material Uncertainty Related to Going Concern' section. Unity 2020 not coded (no original report). "
                 "Source: thesis_results/going_concern_unity_profile.csv.")


def all_figures(res, out) -> list[str]:
    out.mkdir(parents=True, exist_ok=True)
    names = [coverage(res["sample"], out), eligible_n(res["sample"], out)]
    for i, k in enumerate(D.CORE, start=3):
        names.append(trend(res["O"], k, i, out))
    names.append(dumbbell(res["matched_banks"], out))
    names.append(forest(res["reg"], res["desc"], out, "M1", "IFRS9_D", 11, "Within-bank change after IFRS 9 adoption (principal bank-FE model M1)", "fig11_ifrs9_effects"))
    names.append(forest(res["reg"], res["desc"], out, "M4", "Tier1_x_IFRS9_D", 12, "Tier 1 minus Tier 2 change after adoption (bank and year FE, M4)", "fig12_tier_interaction"))
    names.append(robustness_fig(res["rob"], out, "M1", 13, "fig13_robustness_m1", "Robustness of the IFRS 9 coefficient (M1) across samples"))
    names.append(jackknife_fig(res["jk"], out, 14))
    names.append(volatility_fig(res["vol_banks"], out, 15))
    names.append(unity_gc(res["gc"]["unity_profile"], res["O"], out, 16))
    return names
