"""Unverified candidate amounts from the raw CSV and Word tables, kept apart from the panel."""
from __future__ import annotations

from . import config as C
from .util import number, read_json

FIELDS = ["pat", "gross_earnings", "assets", "gross_loans", "loan_allowance", "total_impairment",
          "npl_reported", "car", "gcu", "auditor"]


def load() -> list[dict]:
    P = C.WORK / "update_pack" / "current_uploads"
    out = []
    for fname, src in (("csv_parsed.json", "raw CSV extract"), ("word_tables_parsed.json", "raw Word tables")):
        for r in read_json(P / fname, []):
            for f in FIELDS:
                v = r.get(f)
                if v is None or v == "":
                    continue
                out.append({"bank": r["bank"], "year": int(r["year"]), "field": f, "value": v,
                            "candidate_source": src, "locator": r.get("locator", ""),
                            "status": "candidate_unverified",
                            "note": "Unverified extraction; scope, version and units unconfirmed. Never admitted directly."})
    return out


def compare(cands: list[dict], panel: dict[tuple[str, int], dict]) -> list[dict]:
    conflicts = []
    by_key: dict[tuple[str, int, str], dict[str, object]] = {}
    for c in cands:
        if c["field"] == "auditor":
            continue
        by_key.setdefault((c["bank"], c["year"], c["field"]), {})[c["candidate_source"]] = c["value"]
    for (b, y, f), srcs in sorted(by_key.items()):
        row = panel.get((b, y))
        sel = number(row.get(f)) if row else None
        tol = 0.05 if f in ("npl_reported", "car") else 0.5
        if sel is not None:
            for s, v in srcs.items():
                if abs(float(v) - sel) > tol:  # candidate tables are rounded to NGN m / 0.01pp
                    conflicts.append({"type": "candidate_vs_selected", "bank": b, "year": y, "field": f,
                                      "value_a": sel, "value_b": v,
                                      "detail": f"selected retained; {s} differs (scope/version/rounding unresolved)"})
        elif len(srcs) == 2:
            a, bb = (float(x) for x in srcs.values())
            if abs(a - bb) > tol:
                conflicts.append({"type": "candidate_vs_candidate", "bank": b, "year": y, "field": f,
                                  "value_a": a, "value_b": bb, "detail": "raw CSV and Word tables disagree; neither verified"})
    return conflicts
