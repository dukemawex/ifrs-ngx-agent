"""Turn reviewer specs into admission rows, reading each value from the PDF itself.

data/review/specs.csv names, for every value, the report job, 1-based PDF page,
a regex that identifies the table row, and the x-range of the column (taken from
the column heading position). The value is read from the PDF text layer at that
position, so nothing is retyped. The rendered page is saved and must have been
inspected by the reviewer before 'admit' is set to yes.

python -m ifrs9_recovery.review          # build data/review/admissions.csv from specs
"""
from __future__ import annotations

import re

from . import config as C
from .evidence import EVIDENCE_COLUMNS, LEGAL_ENTITY
from .locate import pdf_for, render
from .util import number, read_csv, utcnow, write_csv

SPECS = C.DATA / "review" / "specs.csv"
SPEC_COLUMNS = ["spec_id", "bank", "year", "variable", "job_id", "page", "printed_page", "row_regex", "x_min",
                "x_max", "row_occurrence", "sign", "raw_units", "scope", "column_heading", "report_title", "report_year",
                "original_or_comparative", "reporting_version", "note_number", "admit", "is_correction",
                "correction_reason", "reviewer_note", "manual_value", "derive_from"]
NUM = re.compile(r"^\(?-?[\d,]+(\.\d+)?\)?%?$")
FACTOR = {"NGN thousand": 0.001, "NGN million": 1.0, "NGN billion": 1000.0, "percent": 1.0, "indicator": 1.0}


def read_value(job_id: str, page: int, row_regex: str, x_min: float, x_max: float, occurrence: int = 1,
               tol: float = 3.0) -> tuple[str, str]:
    import pymupdf
    path, _ = pdf_for(job_id)
    with pymupdf.open(path) as doc:
        words = doc[page - 1].get_text("words")
    words.sort(key=lambda w: (round(w[1]), w[0]))
    lines: list[list] = []
    for w in words:
        if lines and abs(lines[-1][0] - w[1]) <= tol:
            lines[-1][1].append(w)
        else:
            lines.append([w[1], [w]])
    rx = re.compile(row_regex, re.I)
    hits = 0
    for _, ws in lines:
        ws.sort(key=lambda w: w[0])
        plain = " ".join(w[4] for w in ws)
        if not rx.search(plain):
            continue
        hits += 1
        if hits != occurrence:
            continue
        cells = [w[4] for w in ws if x_min <= w[0] <= x_max and (NUM.match(w[4]) or w[4] in ("-", "–"))]
        if len(cells) != 1:
            raise ValueError(f"{job_id} p{page} /{row_regex}/ x[{x_min},{x_max}] -> {cells!r} in: {plain}")
        return cells[0], plain[:240]
    raise ValueError(f"{job_id} p{page}: row /{row_regex}/ occurrence {occurrence} not found")


def build() -> dict:
    specs = read_csv(SPECS) if SPECS.is_file() else []
    downloads = {}
    out, errors = [], []
    built: dict[str, float] = {}
    for s in specs:
        method = "value read from PDF text layer at reviewer-specified row/column; rendered page inspected"
        status = "verified_reported"
        try:
            if (s.get("derive_from") or "").strip():
                # Sum of already-built specs, e.g. "UNION16-LI+UNION16-OI".
                parts = [p.strip() for p in s["derive_from"].split("+")]
                missing = [p for p in parts if p not in built]
                if missing:
                    raise ValueError(f"derive_from components not built: {missing}")
                raw, excerpt = "derived", "sum of " + " + ".join(parts)
                method, status = "sum of verified components", "derived_from_verified"
            elif (s.get("manual_value") or "").strip():
                raw = s["manual_value"].strip()
                excerpt = f"Manual transcription of row /{s['row_regex']}/ from rendered page image."
                method = "manual transcription from rendered page image (page has no text layer); checked by reconciliation"
            else:
                raw, excerpt = read_value(s["job_id"], int(s["page"]), s["row_regex"], float(s["x_min"]),
                                          float(s["x_max"]), int(s.get("row_occurrence") or 1))
        except ValueError as e:
            errors.append({"spec_id": s["spec_id"], "error": str(e)})
            continue
        path, rec = pdf_for(s["job_id"])
        downloads[rec["sha256"]] = rec
        val = sum(built[p] for p in parts) if raw == "derived" else number(raw.rstrip("%"))
        # sign: 1 keeps the printed sign; -1 converts a bracketed expense to the panel's
        # expense-positive convention. Recorded per value so the conversion is auditable.
        mult = int(s.get("sign") or 1)
        if raw == "derived":
            norm = round(val, 6)  # components are already normalised and signed
        else:
            norm = None if val is None else round(mult * val * FACTOR[s["raw_units"]], 6)
        if norm is not None:
            built[s["spec_id"]] = norm
        out.append({
            "evidence_id": s["spec_id"], "bank_key": s["bank"],
            "legal_entity": LEGAL_ENTITY.get(s["bank"], s["bank"]), "financial_year": s["year"],
            "variable": s["variable"], "raw_value": raw, "raw_units": s["raw_units"],
            "currency": "" if s["raw_units"] in ("percent", "indicator") else "NGN",
            "normalised_value_ngnm_or_pct": "" if norm is None else norm, "scope": s["scope"],
            "report_title": s["report_title"], "report_year": s["report_year"], "source_id": s["job_id"],
            "source_url": rec["final_url"], "pdf_sha256": rec["sha256"], "local_pdf_path": rec["local_pdf_path"],
            "pdf_page_1_based": s["page"], "printed_page": s["printed_page"], "note_number": s["note_number"],
            "source_column_heading": s["column_heading"], "original_or_comparative": s["original_or_comparative"],
            "reporting_version": s["reporting_version"], "short_source_excerpt": excerpt,
            "rendered_page_path": render(s["job_id"], int(s["page"]), 110),
            "method": method,
            "verification_status": status if s["admit"].lower() == "yes" else "candidate",
            "review_reason": (s["reviewer_note"] + (" Sign converted to expense-positive." if mult == -1 else "")).strip(), "access_timestamp_utc": rec["accessed_utc"],
            "evidence_origin": "review/specs.csv", "admit": s["admit"], "is_correction": s["is_correction"],
            "correction_reason": s["correction_reason"],
        })
    write_csv(C.DATA / "review" / "admissions.csv", out, EVIDENCE_COLUMNS + ["admit", "is_correction", "correction_reason"])
    write_csv(C.DATA / "review" / "spec_errors.csv", errors, ["spec_id", "error"])
    return {"specs": len(specs), "admission_rows": len(out), "errors": len(errors), "built_utc": utcnow()}


if __name__ == "__main__":
    print(build())
