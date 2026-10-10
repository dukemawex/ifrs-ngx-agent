"""Stage 5: locate statement, note and auditor pages in downloaded PDFs; emit candidates only.

Output is a review queue. A machine-read number is never admitted: admission happens
only through data/review/admissions.csv after the rendered page has been inspected
and the column heading, scope, units and version are confirmed.
"""
from __future__ import annotations

import re

from . import config as C
from .util import read_csv, read_json, utcnow, write_csv, write_json

STATE_FILE = C.STATE / "extract_state.json"

PAGE_TAGS = {
    "sofp": [r"statements? of financial position", r"balance sheet"],
    "income": [r"statements? of (comprehensive income|profit or loss)", r"income statement"],
    "cash_flow": [r"statements? of cash flows?"],
    "auditor_report": [r"independent auditors?'? report", r"report of the independent auditors?"],
    "going_concern": [r"material uncertainty related to going concern", r"going concern"],
    "loans_note": [r"loans and advances to customers"],
    "capital": [r"capital adequacy ratio", r"risk[- ]weighted assets"],
    "liquidity": [r"liquidity ratio", r"liquidity coverage ratio"],
    "ifrs9_transition": [r"transition to ifrs 9", r"ifrs 9 transition", r"opening (ifrs 9 )?(ecl|impairment) allowance"],
    "stage3": [r"stage 3"],
}
SCOPE_HEADINGS = re.compile(r"\b(Group|Bank|Company|Parent|Consolidated|Separate)\b")
UNIT_PATTERNS = [
    (re.compile(r"(N|₦|NGN)\s*'?\s*000\b|in thousands of (nigerian )?naira", re.I), "NGN thousand"),
    (re.compile(r"(N|₦|NGN)\s*'?\s*(million|mn|m)\b|in millions of (nigerian )?naira", re.I), "NGN million"),
    (re.compile(r"(N|₦|NGN)\s*'?\s*(billion|bn)\b|in billions of (nigerian )?naira", re.I), "NGN billion"),
]
LINE_ITEMS = {
    "assets": r"^total assets\b",
    "liabilities": r"^total liabilities\b",
    "equity": r"^total equity\b",
    "pat": r"^profit (for the year|after tax)\b",
    "pbt": r"^profit before (income )?tax\b",
    "ocf": r"^net cash (flows? )?(from|used in|generated from) operating activities\b",
    "net_loans": r"^loans and advances to customers\b",
    "total_impairment": r"^(net )?impairment (charge|loss|writeback)",
}
NUM_RE = re.compile(r"\(?-?\d{1,3}(?:,\d{3})+(?:\.\d+)?\)?|\(?-?\d+\.\d+\)?")
GC_STRONG = re.compile(r"material uncertainty related to going concern", re.I)


def detect_units(text: str) -> list[str]:
    return [label for rx, label in UNIT_PATTERNS if rx.search(text)]


def tag_page(text: str) -> list[str]:
    low = text.lower()
    return [t for t, pats in PAGE_TAGS.items() if any(re.search(p, low) for p in pats)]


def line_candidates(text: str) -> list[dict]:
    out = []
    for line in text.splitlines():
        s = line.strip()
        for var, rx in LINE_ITEMS.items():
            if re.search(rx, s, re.I):
                nums = NUM_RE.findall(s)
                if nums:
                    out.append({"variable": var, "line_text": s[:200], "numbers_in_line": " | ".join(nums)})
    return out


def process_pdf(pdf_path, render_dir, render: bool = True) -> dict:
    import fitz  # PyMuPDF

    doc = fitz.open(pdf_path)
    pages, cands, gc = [], [], []
    for i, page in enumerate(doc, 1):
        text = page.get_text("text") or ""
        tags = tag_page(text)
        has_text = len(text.strip()) > 50
        rendered = ""
        if tags and render and ({"sofp", "income", "cash_flow", "auditor_report", "loans_note"} & set(tags)):
            render_dir.mkdir(parents=True, exist_ok=True)
            out = render_dir / f"p{i:04d}.png"
            if not out.exists():
                page.get_pixmap(dpi=110).save(out)
            rendered = str(out.relative_to(C.ROOT)) if C.ROOT in out.parents else str(out)
        headings = sorted(set(SCOPE_HEADINGS.findall(text)))
        pages.append({"pdf_page_1_based": i, "tags": ";".join(tags), "text_layer": has_text,
                      "scope_headings": ";".join(headings), "units": ";".join(detect_units(text)),
                      "rendered_page_path": rendered})
        if {"sofp", "income", "cash_flow"} & set(tags):
            for c in line_candidates(text):
                cands.append({"pdf_page_1_based": i, "scope_headings_on_page": ";".join(headings),
                              "units_on_page": ";".join(detect_units(text)), "rendered_page_path": rendered,
                              "verification_status": "machine_extracted_unreviewed", **c})
        if "auditor_report" in tags or "going_concern" in tags:
            m = GC_STRONG.search(text)
            gc.append({"pdf_page_1_based": i, "tags": ";".join(tags),
                       "explicit_material_uncertainty_phrase": bool(m),
                       "excerpt": text[max(0, m.start() - 150): m.end() + 150].replace("\n", " ") if m else "",
                       "gcu_code": "", "status": "needs_full_auditor_report_review"})
    return {"page_count": doc.page_count, "pages": pages, "candidates": cands, "gc": gc,
            "text_pages": sum(p["text_layer"] for p in pages)}


def run(resume: bool = True, render: bool = True) -> dict:
    dl = read_json(C.STATE / "download_state.json", {}).get("reports", {})
    state = read_json(STATE_FILE, {}) if resume else {}
    state.setdefault("reports", {})
    all_pages, all_cands, all_gc = [], [], []
    for job_id, rec in dl.items():
        if rec.get("status") != "downloaded":
            continue
        key = rec["sha256"]
        if key not in state["reports"]:
            res = process_pdf(C.ROOT / rec["local_pdf_path"], C.REPORTS / "pages" / key[:12], render)
            state["reports"][key] = {"job_id": job_id, "at": utcnow(), **res}
            write_json(STATE_FILE, state)
        res = state["reports"][key]
        base = {"job_id": job_id, "bank": rec["bank"], "source_url": rec["final_url"], "pdf_sha256": key,
                "local_pdf_path": rec["local_pdf_path"]}
        all_pages += [{**base, **p} for p in res["pages"]]
        all_cands += [{**base, **c} for c in res["candidates"]]
        all_gc += [{**base, **g} for g in res["gc"]]
    write_csv(C.DATA / "page_index.csv", all_pages,
              ["job_id", "bank", "source_url", "pdf_sha256", "local_pdf_path", "pdf_page_1_based", "tags",
               "text_layer", "scope_headings", "units", "rendered_page_path"])
    write_csv(C.DATA / "pdf_candidates.csv", all_cands,
              ["job_id", "bank", "source_url", "pdf_sha256", "local_pdf_path", "pdf_page_1_based", "variable",
               "line_text", "numbers_in_line", "scope_headings_on_page", "units_on_page", "rendered_page_path",
               "verification_status"])
    write_csv(C.DATA / "going_concern_review_queue.csv", all_gc,
              ["job_id", "bank", "source_url", "pdf_sha256", "pdf_page_1_based", "tags",
               "explicit_material_uncertainty_phrase", "excerpt", "gcu_code", "status"])
    return {"pdfs_processed": len(state["reports"]), "pages_indexed": len(all_pages),
            "machine_candidates": len(all_cands), "auditor_pages_queued": len(all_gc)}
