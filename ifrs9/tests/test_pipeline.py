"""Tests for accounting controls, retrieval safety, budget handling and admission rules.

Synthetic PDFs and fake HTTP sessions below are test fixtures only; they never
enter data/ or the panel.
"""
from __future__ import annotations

import io
import json
import math
import zipfile

import pytest
import requests

from ifrs9_recovery import config as C
from ifrs9_recovery import download, extract, inventory, nimble, queue, validate
from ifrs9_recovery.ratios import DERIVED, calculate, rounding_unit_ngnm, same, tolerance
from ifrs9_recovery.util import number, read_csv, redact, safe_extract


@pytest.fixture(scope="session", autouse=True)
def _inventory():
    inventory.run()
    queue.build()


# ------------------------------------------------------------------ inputs

def test_original_inputs_unchanged():
    assert all(h["unchanged"] for h in inventory.verify_input_hashes())


def test_baseline_counts():
    s = inventory.selected_summary(read_csv(C.SELECTED_CSV))
    assert (s["rows"], s["unique_bank_years"], s["banks"]) == (47, 47, 11)
    assert (s["pre_adoption_2013_2017"], s["post_adoption_2018_2022"]) == (25, 22)


# ------------------------------------------------------------------ numbers and ratios

@pytest.mark.parametrize("raw,expected", [
    ("1,234.5", 1234.5), ("(504)", -504.0), ("−214.8", -214.8), ("", None), ("-", None),
    ("N/A", None), (0, 0.0), ("0", 0.0),
])
def test_number_parsing(raw, expected):
    assert number(raw) == expected


def test_blank_is_never_zero_and_zero_denominator_is_null():
    r = calculate({"pat": "10", "assets": "0", "liabilities": "", "equity": "5", "opening_assets": "100"})
    assert r["roa"] is None and r["eqta"] is None and r["leverage"] is None
    assert r["balance_residual"] is None
    assert all(v is None or math.isfinite(v) for v in r.values())


def test_negative_values_are_retained():
    r = calculate({"pat": "-50", "assets": "1000", "opening_assets": "1000", "equity": "-20", "liabilities": "1020"})
    assert r["roa"] == pytest.approx(-5.0)
    assert r["eqta"] == pytest.approx(-2.0)
    assert r["balance_residual"] == pytest.approx(0.0)


def test_recompute_reproduces_baseline_derived_values():
    for row in read_csv(C.SELECTED_CSV):
        calc = calculate(row)
        for f in DERIVED:
            stored = number(row.get(f))
            assert same(stored, calc[f]), (row["bank"], row["year"], f, stored, calc[f])


def test_tolerance_depends_on_rounding_unit():
    assert rounding_unit_ngnm("1704094.012", "1458912.014", "245181.998") == pytest.approx(0.001)
    assert rounding_unit_ngnm("1808503", "1587728", "220775") == 1.0
    assert tolerance(3, 1.0) == pytest.approx(1.5, abs=1e-6)


def test_car_tolerance_whole_percent_only_when_documented():
    assert validate.car_tolerance("20.0", "published whole-percent ratio")[0] == pytest.approx(0.51)
    assert validate.car_tolerance("20.0", "full impact basis")[0] == pytest.approx(0.06)
    assert validate.car_tolerance("15.91", "rounded published ratio")[0] == pytest.approx(0.015)


# ------------------------------------------------------------------ archive and URL safety

def test_safe_extract_rejects_traversal(tmp_path):
    z = tmp_path / "evil.zip"
    with zipfile.ZipFile(z, "w") as zf:
        zf.writestr("../escape.txt", "x")
    with pytest.raises(ValueError):
        safe_extract(z, tmp_path / "out")
    assert not (tmp_path / "escape.txt").exists()


@pytest.mark.parametrize("url,ok", [
    ("https://doclib.ngxgroup.com/x.pdf", True),
    ("http://doclib.ngxgroup.com/x.pdf", False),
    ("https://169.254.169.254/latest/meta-data", False),
    ("https://localhost/x.pdf", False),
    ("https://10.0.0.5/x.pdf", False),
    ("file:///etc/passwd", False),
    ("https://user:pw@example.com/x.pdf", False),
])
def test_url_safety(url, ok):
    assert download.url_is_public_https(url)[0] is ok


class FakeResp:
    def __init__(self, status=200, body=b"", headers=None):
        self.status_code, self._body, self.headers = status, body, headers or {}

    def iter_content(self, n):
        for i in range(0, len(self._body), n):
            yield self._body[i:i + n]

    def json(self):
        return json.loads(self._body)

    def close(self):
        pass

    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(str(self.status_code))


class FakeSession:
    def __init__(self, responses):
        self.responses = list(responses)
        self.calls = []

    def get(self, url, **kw):
        self.calls.append(url)
        r = self.responses.pop(0)
        if isinstance(r, Exception):
            raise r
        return r

    post = get


def test_fetch_rejects_html_saved_as_pdf(tmp_path):
    s = FakeSession([FakeResp(200, b"<html>error</html>", {"Content-Type": "text/html"})])
    rec = download.fetch_pdf("https://example.com/r.pdf", tmp_path, 100, s)
    assert rec["status"] == "not_pdf" and not list(tmp_path.glob("*.pdf"))


def test_fetch_rejects_oversize_stream(tmp_path):
    s = FakeSession([FakeResp(200, b"%PDF-1.7" + b"0" * (2 * 1024 * 1024))])
    rec = download.fetch_pdf("https://example.com/r.pdf", tmp_path, 1, s)
    assert rec["status"] == "too_large" and not list(tmp_path.iterdir())


def test_fetch_rejects_redirect_to_private_host(tmp_path):
    s = FakeSession([FakeResp(302, b"", {"Location": "https://127.0.0.1/r.pdf"})])
    rec = download.fetch_pdf("https://example.com/r.pdf", tmp_path, 10, s)
    assert rec["status"] == "rejected" and len(s.calls) == 1


def test_fetch_records_egress_denial(tmp_path):
    s = FakeSession([requests.exceptions.ProxyError("403 CONNECT")])
    assert download.fetch_pdf("https://example.com/r.pdf", tmp_path, 10, s)["status"] == "egress_denied"


def test_fetch_accepts_real_pdf_and_hashes(tmp_path):
    import hashlib
    body = b"%PDF-1.4\n" + b"x" * 5000
    s = FakeSession([FakeResp(200, body, {"Content-Type": "application/pdf"})])
    rec = download.fetch_pdf("https://example.com/r.pdf", tmp_path, 10, s, stem="t")
    assert rec["status"] == "downloaded" and rec["sha256"] == hashlib.sha256(body).hexdigest()
    assert rec["bytes"] == len(body)


# ------------------------------------------------------------------ Nimble client

def _settings(**kw):
    base = dict(max_requests=5, max_retries=2, dry_run=False, _key="sk-test-SECRET-123")
    base.update(kw)
    return C.Settings(**base)


def test_nimble_counts_retries_and_honours_retry_after(tmp_path, monkeypatch):
    monkeypatch.setattr(nimble, "LOG_FILE", tmp_path / "log.jsonl")
    waits = []
    s = FakeSession([FakeResp(429, b"{}", {"Retry-After": "7"}), FakeResp(200, b'{"results": [{"url": "https://a.ng/r.pdf"}]}')])
    b = nimble.Budget(5, path=tmp_path / "b.json")
    cl = nimble.NimbleClient(_settings(), b, s, sleep=waits.append, cache_dir=tmp_path / "c")
    res = cl.search("Wema Bank 2021")
    assert waits == [7.0] and b.attempted == 2
    assert nimble.result_urls(res["response"])[0]["url"] == "https://a.ng/r.pdf"
    again = cl.search("Wema Bank 2021")  # cached: no new paid call
    assert again["cached"] and b.attempted == 2
    log = (tmp_path / "log.jsonl").read_text()
    assert "SECRET" not in log and "SECRET" not in json.dumps(json.loads((tmp_path / "b.json").read_text()))


def test_nimble_auth_failure_is_not_retried(tmp_path, monkeypatch):
    monkeypatch.setattr(nimble, "LOG_FILE", tmp_path / "log.jsonl")
    s = FakeSession([FakeResp(401, b"{}"), FakeResp(200, b"{}")])
    b = nimble.Budget(5, path=tmp_path / "b.json")
    cl = nimble.NimbleClient(_settings(), b, s, sleep=lambda x: None, cache_dir=tmp_path / "c")
    with pytest.raises(nimble.AuthFailure):
        cl.search("q")
    assert b.attempted == 1 and len(s.calls) == 1


def test_budget_cap_is_hard_and_persistent(tmp_path):
    p = tmp_path / "b.json"
    b = nimble.Budget(2, path=p)
    b.take(); b.take()
    with pytest.raises(nimble.BudgetExhausted):
        b.take()
    assert nimble.Budget(10, path=p).cap == 2  # stricter persisted cap wins


def test_dry_run_makes_no_calls(tmp_path, monkeypatch):
    monkeypatch.setattr(nimble, "LOG_FILE", tmp_path / "log.jsonl")
    s = FakeSession([])
    b = nimble.Budget(5, path=tmp_path / "b.json")
    res = nimble.NimbleClient(_settings(dry_run=True), b, s, cache_dir=tmp_path / "c").search("q")
    assert res["dry_run"] and b.attempted == 0 and not s.calls


def test_redact():
    assert "abc123" not in redact("Authorization: Bearer abc123")


def test_key_absent_blocks_discovery_without_spending(tmp_path, monkeypatch):
    from ifrs9_recovery import discover
    monkeypatch.setattr(discover, "STATE_FILE", tmp_path / "d.json")
    res = discover.run(resume=False, settings=C.Settings(), preflight_fn=lambda: {"host": "x", "reachable": True})
    assert res["blocker"].startswith("auth_missing") and set(res["status_counts"]) == {"blocked"}


# ------------------------------------------------------------------ queue

def test_queue_accounts_for_all_83_positions():
    jobs = read_csv(C.DATA / "task_queue.csv")
    searched = {(j["bank"], j["target_years"]) for j in jobs if j["kind"] == "search"}
    gaps = read_csv(C.TASKS / "bank_year_gaps.csv")
    seeded = {(b, str(y)) for sid, ys in queue.SEED_YEAR_COVERAGE.items()
              for s in read_csv(C.SEEDS / "report_sources.csv") if s["source_id"] == sid for b, y in [(s["bank"], yy) for yy in ys]}
    for g in gaps:
        assert (g["bank"], g["year"]) in searched or (g["bank"], g["year"]) in seeded
    first = [j for j in jobs if j["priority"] == "1"]
    assert first and {j["bank"] for j in first} <= {"Wema", "Union"}


# ------------------------------------------------------------------ extraction

def _make_pdf(path):
    import fitz
    doc = fitz.open()
    p = doc.new_page()
    p.insert_text((50, 60), "Statement of financial position", fontsize=12)
    p.insert_text((50, 80), "In millions of Nigerian Naira        Group        Bank", fontsize=9)
    p.insert_text((50, 100), "Total assets   1,234,567   1,111,111", fontsize=9)
    p.insert_text((50, 115), "Total liabilities   1,000,000   900,000", fontsize=9)
    q = doc.new_page()
    q.insert_text((50, 60), "Independent auditor's report", fontsize=12)
    q.insert_text((50, 80), "Material uncertainty related to going concern", fontsize=9)
    doc.save(path)


def test_extract_emits_unreviewed_candidates_only(tmp_path):
    pdf = tmp_path / "t.pdf"
    _make_pdf(pdf)
    res = extract.process_pdf(pdf, tmp_path / "pages", render=True)
    assert res["page_count"] == 2
    assets = [c for c in res["candidates"] if c["variable"] == "assets"]
    assert assets and assets[0]["verification_status"] == "machine_extracted_unreviewed"
    assert "Bank" in assets[0]["scope_headings_on_page"] and "Group" in assets[0]["scope_headings_on_page"]
    assert "NGN million" in assets[0]["units_on_page"]
    gc = [g for g in res["gc"] if g["explicit_material_uncertainty_phrase"]]
    assert gc and gc[0]["gcu_code"] == ""  # flagged for review, never auto-coded
    assert (tmp_path / "pages" / "p0001.png").is_file()


# ------------------------------------------------------------------ admission rules

def _admission(**kw):
    r = {"bank_key": "Wema", "legal_entity": "Wema Bank Plc", "financial_year": "2021", "variable": "pat",
         "raw_value": "8,013,456", "raw_units": "NGN thousand", "currency": "NGN",
         "normalised_value_ngnm_or_pct": "8013.456", "scope": "Bank", "report_title": "Annual report 2022",
         "report_year": "2022", "source_url": "https://example.ng/r.pdf", "pdf_sha256": "abc",
         "local_pdf_path": "reports/wema/r.pdf", "pdf_page_1_based": "90", "printed_page": "88",
         "source_column_heading": "Bank 2021", "original_or_comparative": "comparative",
         "reporting_version": "2022 report comparative", "short_source_excerpt": "Profit for the year",
         "rendered_page_path": "reports/pages/x/p0090.png", "method": "visual table review",
         "verification_status": "verified_reported", "access_timestamp_utc": "2026-10-10T00:00:00Z"}
    r.update(kw)
    return r


@pytest.fixture
def fake_root(tmp_path, monkeypatch):
    (tmp_path / "reports/wema").mkdir(parents=True)
    (tmp_path / "reports/wema/r.pdf").write_bytes(b"%PDF-1.4")
    (tmp_path / "reports/pages/x").mkdir(parents=True)
    (tmp_path / "reports/pages/x/p0090.png").write_bytes(b"png")
    monkeypatch.setattr(C, "ROOT", tmp_path)
    return {"abc": {"local_pdf_path": "reports/wema/r.pdf"}}


def test_complete_admission_accepted(fake_root):
    assert validate.check_admission(_admission(), fake_root, {"Wema": {}}) == []


@pytest.mark.parametrize("kw,needle", [
    ({"scope": "Group"}, "Group or Consolidated"),
    ({"source_column_heading": "Consolidated 2021"}, "Group or Consolidated"),
    ({"legal_entity": "FCMB Group Plc"}, "holding company"),
    ({"legal_entity": "Stanbic IBTC Holdings Plc"}, "holding company"),
    ({"pdf_sha256": "zzz"}, "does not match"),
    ({"verification_status": "candidate"}, "not admissible"),
    ({"normalised_value_ngnm_or_pct": "8013456"}, "does not match raw value"),
    ({"short_source_excerpt": ""}, "missing short_source_excerpt"),
    ({"printed_page": "", "note_number": ""}, "printed_page or note_number"),
    ({"rendered_page_path": "reports/pages/x/missing.png"}, "rendered page image missing"),
])
def test_admission_rejections(fake_root, kw, needle):
    errs = validate.check_admission(_admission(**kw), fake_root, {"Wema": {}})
    assert any(needle in e for e in errs), errs


# ------------------------------------------------------------------ end-to-end controls on real inputs

def test_validate_retains_baseline_and_exceptions():
    res = validate.run()
    assert res["panel_rows"] >= 47 and res["exceptions_violated"] == []
    panel = {(r["bank"], int(r["year"])): r for r in read_csv(C.DATA / "verified_panel.csv")}
    base = {(r["bank"], int(r["year"])): r for r in read_csv(C.SELECTED_CSV)}
    assert set(base) <= set(panel)
    assert panel[("UBA", 2022)]["liquidity_used"] == ""            # excluded
    assert number(panel[("UBA", 2015)]["loan_allowance"]) == 13043  # not the candidate alternative
    assert number(panel[("UBA", 2016)]["loan_allowance"]) == 29741
    assert panel[("Union", 2022)]["stage3_coverage"] == ""
    for k, r in base.items():  # no admitted-input value changed without a logged correction
        for f in ("pat", "assets", "liabilities", "equity", "gcu"):
            assert same(number(r[f]), number(panel[k][f])), (k, f)
    assert sum(1 for k, r in panel.items() if k in base and r["gcu"] not in ("", None)) == 2
    # Every new going-concern code must come from a full original-year auditor-report review.
    reviewed = {(r["bank"], int(r["year"])) for r in read_csv(C.DATA / "review" / "going_concern_reviews.csv")
                if r["gcu_code"] != ""} if (C.DATA / "review" / "going_concern_reviews.csv").is_file() else set()
    for k, r in panel.items():
        if k not in base and r["gcu"] not in ("", None):
            assert k in reviewed, k


# ------------------------------------------------------------------ reviewer tooling

def test_read_value_picks_only_the_specified_column(tmp_path, monkeypatch):
    from ifrs9_recovery import review
    pdf = tmp_path / "t.pdf"
    _make_pdf(pdf)
    monkeypatch.setattr(review, "pdf_for", lambda job: (pdf, {}))
    import pymupdf
    words = [w for w in pymupdf.open(pdf)[0].get_text("words") if w[4] in ("1,234,567", "1,111,111")]
    xs = {w[4]: w[0] for w in words}
    raw, _ = review.read_value("j", 1, r"^Total assets", xs["1,111,111"] - 2, xs["1,111,111"] + 2)
    assert raw == "1,111,111"
    with pytest.raises(ValueError):  # a range covering two cells is ambiguous and refused
        review.read_value("j", 1, r"^Total assets", 0, 1000)


def test_panel_value_keeps_printed_percent_precision():
    assert validate.panel_value({"raw_units": "percent", "raw_value": "20 %", "normalised_value_ngnm_or_pct": "20.0"}) == "20"
    assert validate.panel_value({"raw_units": "NGN thousand", "raw_value": "1,500", "normalised_value_ngnm_or_pct": "1.5"}) == 1.5


def test_derived_admission_needs_no_raw_units_match(fake_root):
    r = _admission(raw_value="derived", verification_status="derived_from_verified", normalised_value_ngnm_or_pct="9177")
    assert validate.check_admission(r, fake_root, {"Wema": {}}) == []
