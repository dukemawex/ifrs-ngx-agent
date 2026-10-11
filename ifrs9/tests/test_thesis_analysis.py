"""Reproducibility checks for the thesis analysis outputs (thesis_results/) against the frozen release."""
import csv
import re
from pathlib import Path

import numpy as np
import pytest

ROOT = Path(__file__).resolve().parent.parent
RES = ROOT / "thesis_results"

pytestmark = pytest.mark.skipif(not (RES / "regression_results.csv").exists(),
                                reason="run `python -m thesis_analysis` first")


def rows(name):
    with (RES / name).open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def test_frozen_release_unchanged():
    from thesis_analysis import data as D
    meta = D.verify_release()
    assert meta["release_id"] == "IFRS9_release_2026-10-11_v1"
    assert meta["files_verified"] == 42


def test_required_exports_exist():
    for f in ["analysis_master.xlsx", "descriptive_statistics.csv", "matched_prepost.csv", "tier_comparisons.csv",
              "regression_results.csv", "robustness_results.csv", "volatility_results.csv", "going_concern_events.csv",
              "model_diagnostics.csv", "analysis_report.md", "interpretation.md", "thesis_results_handoff.zip"]:
        assert (RES / f).exists(), f
    assert len(list((RES / "figures").glob("*.png"))) >= 10
    assert len(list((RES / "tables").glob("*.csv"))) >= 9


def test_cohort_is_12_banks_without_fcmb():
    from thesis_analysis import data as D
    assert len(D.COHORT) == 12 and "FCMB" not in D.COHORT
    for name in ("descriptive_statistics.csv", "regression_results.csv", "trend_values.csv"):
        text = (RES / name).read_text()
        assert "FCMB" not in text, name


def test_regression_n_matches_eligible_n():
    elig = {r["outcome"]: int(r["eligible_N"]) for r in rows("variables_eligible_n.csv")}
    for r in rows("regression_results.csv"):
        if r["model"] in ("M1", "M4"):
            assert int(r["N"]) == elig[r["outcome"]], (r["outcome"], r["model"])


def test_no_ifrs9_dummy_with_year_fe():
    for r in rows("regression_results.csv"):
        if "+ year FE" in r["specification"] or r["model"] in ("M4", "M4s"):
            assert r["term"] != "IFRS9_D", r


def test_no_models_for_sparse_or_going_concern():
    outs = {r["outcome"] for r in rows("regression_results.csv")}
    assert outs.isdisjoint({"npl_calc", "broad_coverage", "stage3_coverage", "liquidity", "gcu"})
    ev = rows("going_concern_events.csv")
    assert sorted((e["bank"], int(e["year"])) for e in ev) == [("Unity", 2019), ("Unity", 2021), ("Unity", 2022)]


def test_report_m1_table_matches_csv():
    reg = {r["variable"]: r for r in rows("regression_results.csv") if r["model"] == "M1" and r["term"] == "IFRS9_D"}
    rep = (RES / "analysis_report.md").read_text()
    sec = rep.split("## 2.")[1].split("## 3.")[0]
    lines = [l for l in sec.splitlines() if l.startswith("| ") and not l.startswith("| Outcome") and not l.startswith("|---")]
    assert len(lines) == 7
    for l in lines:
        cells = [c.strip() for c in l.strip("|").split("|")]
        r = reg[cells[0]]
        assert float(cells[1]) == pytest.approx(float(r["coef"]), abs=5e-4)
        assert float(cells[2]) == pytest.approx(float(r["se_cr1"]), abs=5e-4)
        assert float(cells[5]) == pytest.approx(float(r["p_wild_cluster_bootstrap"]), abs=5e-4)
        assert int(cells[6]) == int(r["N"])


def test_cr1_matches_statsmodels():
    sm = pytest.importorskip("statsmodels.api")
    from thesis_analysis import data as D, econ as E
    d = D.inferential(D.outcome("roa"))
    g = d["bank"].to_numpy()
    X = E.demean(d[["ifrs9_d"]].to_numpy(float), g)
    y = E.demean(d["value"].to_numpy(float), g)
    out, info = E.fit(X, y, g, ["IFRS9_D"], absorbed_groups=info_g(g), bootstrap=False)
    ref = sm.OLS(y, X).fit(cov_type="cluster", cov_kwds={"groups": np.unique(g, return_inverse=True)[1]})
    assert out[0]["coef"] == pytest.approx(ref.params[0])
    assert out[0]["se_cr1"] == pytest.approx(ref.bse[0], rel=1e-6)


def info_g(g):
    return len(np.unique(g))
