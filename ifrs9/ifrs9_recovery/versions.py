"""Reporting-version register: one row per selected bank-year stating which presentation is primary.

Hierarchy (data/review/version_policy.md):
  1. original-year audited report (primary);
  2. if the original is unavailable, the next-year comparative column (labelled restatement > unlabelled comparative),
     kept as primary but flagged so it can be dropped in sensitivity analysis;
  3. later labelled restatements / reclassifications / unexplained differences of an available original are never
     substituted: they are retained in version_decisions.csv and source_alternatives.csv as sensitivity-only values.
Inputs are the saved panel, admissions and version decisions; nothing is typed here.
"""
from __future__ import annotations

from collections import Counter, defaultdict

from . import config as C
from .util import read_csv, write_csv

CORE = ("pat", "assets", "liabilities", "equity")
COLUMNS = ["bank", "year", "row_origin", "primary_source", "primary_report", "primary_version", "comparative_status",
           "labelled_restated", "original_report_unavailable", "treatment", "fallback_class", "alternatives",
           "alternative_fields", "version_mix", "version_mix_reconciliation"]


def _class_of(decisions: list[dict]) -> str:
    for d in decisions:
        if d["classification"].startswith("fallback"):
            return d["classification"]
    return ""


def build() -> list[dict]:
    panel = read_csv(C.DATA / "verified_panel.csv")
    adm = [a for a in read_csv(C.DATA / "review" / "admissions.csv") if a.get("admit", "").lower() == "yes"]
    vdec = read_csv(C.DATA / "review" / "version_decisions.csv")
    alts = read_csv(C.DATA / "review" / "source_alternatives.csv")
    recon = read_csv(C.DATA / "review" / "version_reconciliations.csv") if (C.DATA / "review" / "version_reconciliations.csv").is_file() else []
    base_keys = {(r["bank"], r["year"]) for r in read_csv(C.SELECTED_CSV)}
    by_key: dict = defaultdict(dict)
    for a in adm:
        by_key[(a["bank_key"], a["financial_year"])][a["variable"]] = a
    dec_by: dict = defaultdict(list)
    for d in vdec:
        dec_by[(d["bank"], d["year"])].append(d)
    alt_by = Counter((a["bank_key"], a["financial_year"]) for a in alts)
    rec_by = {(r["bank"], r["year"]): r for r in recon}
    out = []
    for r in panel:
        k = (r["bank"], r["year"])
        core = [by_key[k][f] for f in CORE if f in by_key[k]]
        decs = dec_by.get(k, [])
        fb = _class_of(decs)
        if core and k not in base_keys:
            origin = "admitted"
            versions = Counter(c["reporting_version"] for c in core)
            primary_version = versions.most_common(1)[0][0]
            comp = Counter(c["original_or_comparative"].split(" ")[0] for c in core).most_common(1)[0][0]
            src = core[0]["source_id"]; report = core[0]["report_title"]
            mix_inputs = {f: by_key[k][f]["reporting_version"] for f in CORE + ("ocf", "total_impairment", "opening_assets")
                          if f in by_key[k]}
            mix = len(set(mix_inputs.values())) > 1
        else:
            origin = "baseline_inherited" if k in base_keys else "admitted"
            primary_version = r.get("version_note", "") or "baseline/inherited"
            comp = "comparative" if "comparative" in primary_version.lower() else "original"
            src = r.get("source_id", ""); report = r.get("sources", "")[:120]
            mix_inputs, mix = {}, False
        labelled = fb == "fallback: labelled restatement" or "restated" in primary_version.lower() and "not labelled" not in primary_version.lower()
        unavailable = bool(fb)
        treatment = ("primary; drop in sensitivity (fallback: original-year report unavailable)" if fb
                     else "primary (original-year presentation)" if origin == "admitted"
                     else "primary (baseline selection retained)")
        alt_fields = sorted({d["field"] for d in decs if not d["classification"].startswith("fallback")})
        out.append({"bank": r["bank"], "year": r["year"], "row_origin": origin, "primary_source": src,
                    "primary_report": report, "primary_version": primary_version, "comparative_status": comp,
                    "labelled_restated": "yes" if labelled else "no", "original_report_unavailable": "yes" if unavailable else "no",
                    "treatment": treatment, "fallback_class": fb, "alternatives": len(decs) - (1 if fb else 0) + alt_by.get(k, 0),
                    "alternative_fields": ";".join(alt_fields),
                    "version_mix": "; ".join(f"{f}: {v}" for f, v in mix_inputs.items()) if mix else "",
                    "version_mix_reconciliation": (rec_by[k]["reconciliation"] if k in rec_by else ("UNRECONCILED" if mix else ""))})
    write_csv(C.DATA / "row_versions.csv", out, COLUMNS)
    return out
