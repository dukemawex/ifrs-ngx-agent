"""Long-form evidence: inherited records from the starting pack plus reviewed admissions.

Inherited records keep their original status text. They are labelled as inherited
and not re-checked in this run, because their PDFs were not re-downloaded here.
"""
from __future__ import annotations

from . import config as C
from .util import number, read_csv

EVIDENCE_COLUMNS = [
    "evidence_id", "bank_key", "legal_entity", "financial_year", "variable", "raw_value", "raw_units",
    "currency", "normalised_value_ngnm_or_pct", "scope", "report_title", "report_year", "source_id",
    "source_url", "pdf_sha256", "local_pdf_path", "pdf_page_1_based", "printed_page", "note_number",
    "source_column_heading", "original_or_comparative", "reporting_version", "short_source_excerpt",
    "rendered_page_path", "method", "verification_status", "review_reason", "access_timestamp_utc",
    "evidence_origin", "document_scope", "column_scope", "column_scope_basis", "opinion_applicability",
    "sign_transform", "sign_reason", "derive_formula", "component_ids", "value_basis",
]

PRIOR_NAME_MAP = {
    "Total_assets": "assets", "Total_liabilities": "liabilities", "Equity": "equity", "PAT": "pat",
    "Operating_cash_flow": "ocf", "Opening_total_assets": "opening_assets", "Gross_loans": "gross_loans",
    "Loan_allowance": "loan_allowance", "Net_customer_loans": "net_loans",
    "Impairment_expense": "total_impairment", "Impairment_expense_loans": "loan_impairment",
    "Impairment_expense_other_assets": "other_impairment", "NPL_amount": "npl_amount",
    "NPL_ratio_reported": "npl_reported", "CAR_reported": "car", "CAR_minimum_pct": "car_minimum",
    "CAR_transition_adjusted_pct": "car_transitional", "Regulatory_capital": "regulatory_capital",
    "RWA": "rwa", "Liquidity_ratio_pct": "liquidity", "Stage3_gross_customer_loans": "stage3_gross",
    "Stage3_loan_allowance": "stage3_allowance", "Specific_allowance": "specific_allowance",
    "Collective_allowance": "collective_allowance", "Gross_earnings": "gross_earnings",
    "GC_material_uncertainty": "gcu", "Regulatory_capital_transition_adjusted": "capital_transitional",
    "IFRS9_regulatory_addback": "capital_addback",
}

LEGAL_ENTITY = {
    "Access": "Access Bank Plc", "Zenith": "Zenith Bank Plc", "First Bank": "First Bank of Nigeria Limited",
    "UBA": "United Bank for Africa Plc", "GTBank": "Guaranty Trust Bank (Nigeria)", "Fidelity": "Fidelity Bank Plc",
    "Stanbic": "Stanbic IBTC Bank", "Sterling": "Sterling Bank", "Wema": "Wema Bank Plc",
    "FCMB": "First City Monument Bank Limited", "Ecobank Nigeria": "Ecobank Nigeria Limited",
    "Unity": "Unity Bank Plc", "Union": "Union Bank of Nigeria Plc",
}


def canonical(name: str) -> str:
    return PRIOR_NAME_MAP.get(name, name)


def _row(prefix, i, r, var_key, unit_key, page_key, status_key, version_key, report_year_key, origin):
    raw_unit = r.get("raw_unit") or r.get(unit_key) or ""
    status = r.get(status_key, "")
    return {
        "evidence_id": r.get("evidence_id") or f"{prefix}{i:04d}",
        "bank_key": r["bank"], "legal_entity": LEGAL_ENTITY.get(r["bank"], r["bank"]) + " (as recorded by prior pack)",
        "financial_year": r["year"], "variable": canonical(r[var_key]),
        "raw_value": r.get("raw_value") or r.get("value", ""), "raw_units": raw_unit,
        "currency": "NGN" if "NGN" in raw_unit else "",
        "normalised_value_ngnm_or_pct": r.get("value", ""), "scope": r.get("scope", ""),
        "report_title": "", "report_year": r.get(report_year_key, "") if report_year_key else "",
        "source_id": r.get("source_id", ""), "source_url": r.get("source_url", ""),
        "pdf_sha256": "", "local_pdf_path": "", "pdf_page_1_based": r.get(page_key, ""),
        "printed_page": r.get("printed_page", ""), "note_number": "",
        "source_column_heading": "", "original_or_comparative": r.get(version_key, "") if version_key else "",
        "reporting_version": r.get(version_key, "") if version_key else "",
        "short_source_excerpt": "", "rendered_page_path": "",
        "method": "inherited from starting pack",
        "verification_status": "inherited_not_rechecked_this_run",
        "review_reason": f"Prior status: {status}. {r.get('note', '')}".strip()
                         + " PDF not re-downloaded or hashed in this run.",
        "access_timestamp_utc": "", "evidence_origin": origin,
    }


def inherited() -> list[dict]:
    P = C.WORK / "update_pack"
    rows = []
    for i, r in enumerate(read_csv(P / "prior_evidence" / "prior_selected_evidence.csv"), 1):
        rows.append(_row("EV", i, r, "metric", "unit", "pdf_page", "status", "vintage", None, "prior_selected_evidence.csv"))
    for i, r in enumerate(read_csv(P / "prior_evidence" / "new_evidence.csv"), 1):
        rows.append(_row("NI", i, r, "metric", "unit", "pdf_page", "status", "vintage", None, "new_evidence.csv"))
    for i, r in enumerate(read_csv(P / "prior_evidence" / "Union_Verified_Evidence.csv"), 1):
        rows.append(_row("U", i, r, "field", "units", "pdf_page_1_based", "status", "version", "report_year", "Union_Verified_Evidence.csv"))
    for i, r in enumerate(read_csv(P / "New_Primary_Evidence.csv"), 1):
        rows.append(_row("NP", i, r, "field", "unit", "pdf_page", "source_status", "version", "report_year", "New_Primary_Evidence.csv"))
    return rows


def backing_index(rows: list[dict]) -> dict[tuple[str, int, str], list[dict]]:
    idx: dict[tuple[str, int, str], list[dict]] = {}
    for r in rows:
        try:
            key = (r["bank_key"], int(r["financial_year"]), r["variable"])
        except ValueError:
            continue
        idx.setdefault(key, []).append(r)
    return idx


def evidence_matches(value, records: list[dict]) -> bool:
    v = number(value)
    if v is None:
        return False
    for r in records:
        try:
            e = number(r["normalised_value_ngnm_or_pct"])
        except ValueError:
            continue
        if e is not None and abs(e - v) <= max(0.0005, 1e-9 * abs(v)):
            return True
    return False


COMPONENT_SUMS = {
    "loan_allowance": [("specific_allowance", "collective_allowance"),
                       ("Corporate_loan_allowance", "Retail_loan_allowance")],
    "total_impairment": [("loan_impairment", "other_impairment")],
}


def component_match(value, field: str, bank: str, year: int, idx) -> tuple[list[dict], str]:
    """Match a selected total against the sum of separately evidenced components."""
    v = number(value)
    if v is None:
        return [], ""
    for parts in COMPONENT_SUMS.get(field, []):
        recs = [idx.get((bank, year, p), []) for p in parts]
        if not all(recs):
            continue
        vals = [number(r[0]["normalised_value_ngnm_or_pct"]) for r in recs]
        if None not in vals and abs(sum(vals) - v) <= 0.0005 * len(vals) + 1e-9:
            return [r[0] for r in recs], "sum of " + " + ".join(parts)
    return [], ""


# Inherited evidence named with a more specific CAR label than the panel column.
CAR_ALIASES = ("CAR_Basel_II", "CAR_full_IFRS9_pct", "CAR_reported")
QUALIFICATIONS = {
    ("First Bank", 2013, "car"): "Basel II comparator reconstructed in the 2014 report (DS0036); the original 2013 "
                                 "report's Basel I CAR was 16.76% (DS0037). Not the originally published 2013 ratio.",
    ("First Bank", 2014, "car"): "Basel II CAR from the 2014 report regulatory table (DS0033).",
    ("Unity", 2018, "car"): "Full IFRS 9 impact CAR from the 2019 report's restated 2018 comparative (EV0224); "
                            "transition-adjusted -213.68% held separately (EV0226).",
    ("Unity", 2019, "car"): "Full IFRS 9 impact CAR, 2019 report current year (EV0247); transition-adjusted -200.88% (EV0249).",
    ("Wema", 2022, "total_impairment"): "2023 report comparative: litigation claim reclassified out of impairment "
                                        "(2023 report note 11); original 2022 presentation 4,808.387 held as an alternative.",
    ("Stanbic", 2020, "regulatory_capital"): "Derived: eligible Tier I + Tier II; printed subtotal 176,542 conflicts "
                                             "(held as a source alternative, unresolved).",
}


def alias_match(value, field: str, bank: str, year: int, idx) -> tuple[list[dict], str]:
    """Match evidence recorded under the original CAR naming (still a direct source value)."""
    if field != "car":
        return [], ""
    for name in CAR_ALIASES:
        recs = idx.get((bank, year, name), [])
        if evidence_matches(value, recs):
            return recs, f"evidence recorded as {name}"
    return [], ""
