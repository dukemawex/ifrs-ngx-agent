"""Real-data regression tests: the saved release outputs and the actual edge cases found during review.

These read the committed data registers (not synthetic fixtures). Tests that need the downloaded
source PDFs are skipped, and reported as not run, when those files are absent from the checkout.
"""
import csv
import json
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
REVIEW = DATA / "review"
OUT = ROOT / "outputs"


def rows(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def num(x):
    try:
        return float(str(x).replace(",", ""))
    except ValueError:
        return None


@pytest.fixture(scope="module")
def panel():
    return {(r["bank"], int(r["year"])): r for r in rows(DATA / "verified_panel.csv")}


@pytest.fixture(scope="module")
def admissions():
    return rows(REVIEW / "admissions.csv")


@pytest.fixture(scope="module")
def checks():
    return {(r["bank"], int(r["year"]), r["check"]): r for r in rows(DATA / "reconciliation_checks.csv")}


@pytest.fixture(scope="module")
def stats():
    from ifrs9_recovery import summary
    return summary.release_stats()


# 1. Release snapshot: the narrative is generated from the saved CSVs and agrees with them.

def test_summary_counts_reconcile_with_csvs(panel, stats):
    changes = rows(DATA / "change_register.csv")
    pre = sum(1 for r in panel.values() if r["regime"] == "IAS 39")
    assert stats["panel"]["rows"] == len(panel)
    assert stats["panel"]["pre_adoption"] == pre and stats["panel"]["post_adoption"] == len(panel) - pre
    assert stats["changes"]["new_bank_year"] == sum(c["kind"] == "new_bank_year" for c in changes)
    assert stats["changes"]["fill_blank"] == sum(c["kind"] == "fill_blank" for c in changes)
    assert set(stats["changes"]) <= {"new_bank_year", "fill_blank", "correction"}
    coded = [r for r in panel.values() if r["gcu"].strip() != ""]
    assert stats["going_concern"]["panel_coded"] == len(coded)
    assert stats["going_concern"]["panel_unknown"] == len(panel) - len(coded)
    recon = rows(DATA / "reconciliation_checks.csv")
    assert stats["reconciliation"]["run"] == len(recon)
    assert stats["reconciliation"].get("fail", 0) == sum(r["status"] == "fail" for r in recon)
    assert stats["reconciliation"]["pass"] == sum(r["status"] == "pass" for r in recon)


def test_summary_text_does_not_contradict_going_concern_fills(stats):
    text = (OUT / "reconciliation_summary.md").read_text(encoding="utf-8")
    fills = sum(c["kind"] == "fill_blank" and c["field"] == "gcu" for c in rows(DATA / "change_register.csv"))
    assert fills > 0
    assert "No going-concern code was added" not in text
    assert "no original-year auditor report was reviewed" not in text.lower()
    assert f"{fills} filled in baseline rows" in text
    reviews = sum(r["report_reviewed"] != "not reviewed" for r in rows(REVIEW / "going_concern_reviews.csv"))
    assert f"auditor reports reviewed and recorded: {reviews}" in text


def test_every_changed_baseline_cell_is_in_the_change_register(panel):
    baseline = rows(ROOT / "inputs" / "IFRS9_Selected_Data_Updated_20261010.csv")
    logged = {(c["bank"], int(c["year"]), c["field"]) for c in rows(DATA / "change_register.csv")}
    unlogged = []
    for b in baseline:
        key = (b["bank"], int(b["year"]))
        p = panel[key]
        for f, old in b.items():
            new = p.get(f, "")
            if old == new or (num(old) is not None and num(new) is not None and abs(num(old) - num(new)) < 1e-9):
                continue
            if (*key, f) not in logged:
                unlogged.append((*key, f, old, new))
    assert unlogged == []


def test_all_baseline_rows_retained_and_no_value_cleared(panel):
    for b in rows(ROOT / "inputs" / "IFRS9_Selected_Data_Updated_20261010.csv"):
        p = panel[(b["bank"], int(b["year"]))]
        cleared = [f for f, v in b.items() if v.strip() and not p.get(f, "").strip()]
        assert cleared == [], (b["bank"], b["year"], cleared)


def test_lineage_every_nonblank_input_matched_or_qualified():
    backing = rows(DATA / "evidence_backing.csv")
    assert backing and all(r["value_matches_evidence"] == "True" for r in backing)
    aliased = [r for r in backing if r["match_basis"].startswith("evidence recorded as")]
    assert aliased and all(r["qualification"].strip() for r in aliased)
    # The four alias matches investigated in this run are qualified, not given invented citations.
    named = {(r["bank"], r["year"], r["field"]) for r in backing if r["qualification"].strip()}
    for k in [("First Bank", "2013", "car"), ("First Bank", "2014", "car"), ("Unity", "2018", "car"), ("Unity", "2019", "car")]:
        assert k in named


# 3. Individual reconciliation exceptions.

def test_uba_2018_car_passes_on_display_precision_only(panel, checks):
    c = checks[("UBA", 2018, "reported CAR vs capital/RWA")]
    assert c["status"] == "pass"
    assert num(c["tolerance"]) < 0.51  # half a whole-percent step plus input rounding, not a global tolerance
    assert "printed literal '20'" in c["note"]
    p = panel[("UBA", 2018)]
    assert num(p["car"]) == 20 and num(p["car_transitional"]) == 22.08
    assert num(p["regulatory_capital"]) == 245482 and num(p["rwa"]) == 1248509
    assert abs(100 * 245482 / 1248509 - 19.66201285) < 1e-6


def test_wema_2021_car_stays_a_documented_source_exception(panel, checks):
    c = checks[("Wema", 2021, "reported CAR vs capital/RWA")]
    assert c["status"] == "documented_source_exception" and c["passed"] == "False"
    assert num(c["tolerance"]) <= 0.0051  # the UBA precision rule does not relax a 2-dp printed ratio
    assert num(panel[("Wema", 2021)]["car"]) == 11.71
    stats_eligible = json.loads((OUT / "release_stats.json").read_text())["endpoints"]["car"]
    assert stats_eligible["excluded_by_flag"] >= 1


def test_stanbic_2020_capital_is_derived_and_printed_subtotal_preserved(panel, admissions):
    rc = next(r for r in admissions if r["evidence_id"] == "STAN20-RC")
    assert rc["value_basis"] == "derived_from_verified" and rc["raw_value"] == "derived"
    assert rc["derive_formula"] == "sum" and set(rc["component_ids"].split(";")) == {"STAN20-T1", "STAN20-T2"}
    assert num(panel[("Stanbic", 2020)]["regulatory_capital"]) == 221408
    alts = {r["evidence_id"]: r for r in rows(REVIEW / "source_alternatives.csv")}
    assert alts["ALT-STAN20-RC-PRINTED"]["raw_value"] == "176,542"
    assert alts["ALT-STAN20-RCT-PRINTED"]["raw_value"] == "182,720"
    dec = [d for d in rows(REVIEW / "version_decisions.csv") if (d["bank"], d["year"]) == ("Stanbic", "2020")]
    assert dec and all("unresolved" in d["decision"] for d in dec)
    fs = {(r["bank"], r["year"], r["field"]): r for r in rows(DATA / "field_status.csv")}
    assert fs[("Stanbic", "2020", "regulatory_capital")]["value_basis"].startswith("derived_from_verified")


# 4. First Bank: numbers supported, audit coverage unverified, gcu unknown.

def test_first_bank_2016_2017_audit_coverage_unverified_and_gcu_unknown(panel):
    doc = next(d for d in rows(REVIEW / "document_status.csv") if d["job_id"] == "xs-809800e65f")
    assert doc["document_type"] == "issuer-hosted financial-statement extract"
    assert doc["audit_report_reviewed_for_gcu"] == "unverified"
    assert doc["audit_report_in_file"].lower().startswith("no")
    for y in (2016, 2017):
        assert panel[("First Bank", y)]["gcu"].strip() == ""
        assert num(panel[("First Bank", y)]["assets"]) > 0


# 6. Version policy.

def test_wema_2022_impairment_retained_with_reclassification_decision(panel):
    assert num(panel[("Wema", 2022)]["total_impairment"]) == 4762.274
    d = next(d for d in rows(REVIEW / "version_decisions.csv")
             if (d["bank"], d["year"], d["field"]) == ("Wema", "2022", "total_impairment"))
    assert d["classification"] == "labelled reclassification" and "4808.387" in d["alternative_value"]


def test_every_version_decision_is_classified():
    allowed = re.compile(r"^(labelled restatement|labelled reclassification|unexplained difference|source internal inconsistency"
                         r"|possible scope incompatibility.*|fallback: .+)$")
    for d in rows(REVIEW / "version_decisions.csv"):
        assert allowed.match(d["classification"]), d


def test_denominator_pairs_documented_not_smoothed():
    for d in rows(DATA / "denominator_compatibility.csv"):
        if d["compatible"] != "True":
            assert d["opening_version"] and d["prior_closing_version"]


# 7. Going concern.

def test_unity_2019_material_uncertainty_confirmed_against_note(panel):
    r = next(r for r in rows(REVIEW / "going_concern_reviews.csv") if (r["bank"], r["year"]) == ("Unity", "2019"))
    assert r["gcu_code"] == "1" and r["mu_section"].lower().startswith("yes")
    assert "35" in r["management_gc_disclosure"]
    assert panel[("Unity", 2019)]["gcu"].strip() in ("1", "1.0")


def test_gc_codes_only_from_reviews_covering_the_bank(panel):
    reviews = {(r["bank"], int(r["year"])): r for r in rows(REVIEW / "going_concern_reviews.csv")}
    for c in rows(DATA / "change_register.csv"):
        if c["field"] == "gcu":
            rv = reviews[(c["bank"], int(c["year"]))]
            from ifrs9_recovery.validate import GC_APPLICABLE
            assert rv["report_reviewed"] != "not reviewed" and rv["opinion_applicability"] in GC_APPLICABLE
            assert rv["auditor"].strip() and rv["report_date"].strip() and rv["signature_page_pdf"].strip()


def test_not_reviewed_is_unknown_not_zero(panel):
    for r in rows(REVIEW / "going_concern_reviews.csv"):
        if r["report_reviewed"] == "not reviewed":
            assert r["gcu_code"] == ""


# 5. Admission boundary on real admissions.

def test_sign_transforms_only_for_expense_variables_with_reason(admissions):
    from ifrs9_recovery.validate import SIGN_CONVERTIBLE
    for r in admissions:
        if r["sign_transform"] not in ("", "none"):
            assert SIGN_CONVERTIBLE.match(r["variable"]) and r["sign_reason"].strip(), r["evidence_id"]


def test_negative_pat_equity_ocf_are_preserved(admissions, panel):
    for r in admissions:
        if r["variable"] in ("pat", "equity", "ocf") and r["raw_value"] not in ("derived", ""):
            raw_neg = r["raw_value"].strip().startswith(("(", "-"))
            assert raw_neg == (num(r["normalised_value_ngnm_or_pct"]) < 0), r["evidence_id"]
    assert num(panel[("Unity", 2019)]["equity"]) < 0


def test_derived_admissions_recompute_from_components(admissions):
    from ifrs9_recovery.validate import check_derived
    by_id = {r["evidence_id"]: r for r in admissions if r.get("admit", "").lower() in ("yes", "true", "1")}
    derived = [r for r in by_id.values() if r["value_basis"] == "derived_from_verified"]
    assert derived
    for r in derived:
        assert check_derived(r, by_id) == [], r["evidence_id"]


def test_structured_scope_on_every_admission(admissions):
    from ifrs9_recovery.validate import check_scope
    for r in admissions:
        assert check_scope(r) == [], r["evidence_id"]


def _pdfs_present(admissions):
    return all((ROOT / r["local_pdf_path"]).is_file() for r in admissions)


def test_all_admissions_hash_page_and_image_verified(admissions):
    if not _pdfs_present(admissions):
        pytest.skip("source PDFs not in this checkout (retrieve via reports/index.csv)")
    from ifrs9_recovery import config as C
    from ifrs9_recovery.util import read_json
    from ifrs9_recovery.validate import check_admission
    dl = read_json(C.STATE / "download_state.json", {}).get("reports", {})
    downloads = {v["sha256"]: v for v in dl.values() if v.get("status") == "downloaded"}
    cohort = {r["bank"]: r for r in rows(C.TASKS / "cohort.csv")}
    bad = {r["evidence_id"]: errs for r in admissions if (errs := check_admission(r, downloads, cohort))}
    assert bad == {}


def test_handoff_includes_every_evidence_image():
    import zipfile
    z = OUT / "research_data_handoff.zip"
    names = set(zipfile.ZipFile(z).namelist())
    manifest = zipfile.ZipFile(z).read("MANIFEST.txt").decode()
    assert "SOURCE PDFs ARE NOT INCLUDED" in manifest and "MISSING IMAGE" not in manifest
    assert not any(n.endswith(".pdf") for n in names)


def test_no_secret_in_tracked_outputs():
    pat = re.compile(r"(?i)nimble[_-]?api[_-]?key\s*[=:]\s*['\"]?[A-Za-z0-9_\-]{16,}")
    for d in (DATA, OUT):
        for p in d.rglob("*"):
            if p.suffix in (".csv", ".json", ".md", ".txt"):
                assert not pat.search(p.read_text(encoding="utf-8", errors="ignore")), p


def test_fidelity_2016_car_documented_exception_not_resolved(panel, checks):
    c = checks[("Fidelity", 2016, "reported CAR vs capital/RWA")]
    assert c["status"] == "documented_source_exception" and c["passed"] == "False"
    assert num(panel[("Fidelity", 2016)]["car"]) == 17.22
    assert abs(100 * 196913 / 1138258 - 17.30) < 0.005


def test_stanbic_2018_writeback_stored_as_negative_charge(admissions, panel):
    r = next(a for a in admissions if a["evidence_id"] == "STAN18-TI")
    assert r["raw_value"] == "2,988" and num(r["normalised_value_ngnm_or_pct"]) == -2988
    assert r["sign_transform"] == "expense_presented_negative" and "write-back" in r["sign_reason"]


def test_npl_only_from_explicit_labels(admissions):
    # 'Individually impaired' (IAS 39) amounts were not admitted as NPL for the 2014-2020 Fidelity additions.
    assert not [a for a in admissions if a["evidence_id"] in ("FID14-NPL", "FID15-NPL", "FID16-NPL", "FID17-NPL", "FID20-NPL")]
