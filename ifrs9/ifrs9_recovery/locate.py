"""Reviewer aid: find pages by phrase, rebuild table rows from word positions, render pages.

Usage:
  python -m ifrs9_recovery.locate find <job_id> "statement of financial position" [more phrases]
  python -m ifrs9_recovery.locate rows <job_id> <page_1_based> [filter-regex]
  python -m ifrs9_recovery.locate render <job_id> <page_1_based> [dpi]

Output is for a human/visual check; it never writes to the panel.
"""
from __future__ import annotations

import re
import sys

from . import config as C
from .util import read_json


def pdf_for(job_id: str):
    rec = read_json(C.STATE / "download_state.json", {})["reports"][job_id]
    return C.ROOT / rec["local_pdf_path"], rec


def find(job_id: str, phrases: list[str]) -> list[tuple[int, str]]:
    import pymupdf
    path, _ = pdf_for(job_id)
    out = []
    with pymupdf.open(path) as doc:
        for i, page in enumerate(doc, 1):
            low = page.get_text().lower()
            if all(p.lower() in low for p in phrases):
                first = " ".join(low.split())[:110]
                out.append((i, first))
    return out


def rows(job_id: str, page_no: int, pattern: str | None = None, tol: float = 3.0) -> list[str]:
    import pymupdf
    path, _ = pdf_for(job_id)
    with pymupdf.open(path) as doc:
        words = doc[page_no - 1].get_text("words")
    words.sort(key=lambda w: (round(w[1]), w[0]))
    lines: list[list] = []
    for w in words:
        if lines and abs(lines[-1][0] - w[1]) <= tol:
            lines[-1][1].append(w)
        else:
            lines.append([w[1], [w]])
    out = []
    rx = re.compile(pattern, re.I) if pattern else None
    for y, ws in lines:
        ws.sort(key=lambda w: w[0])
        text = "  ".join(f"{w[4]}@{int(w[0])}" for w in ws)
        plain = " ".join(w[4] for w in ws)
        if rx is None or rx.search(plain):
            out.append(f"y={int(y):4d} | {text}")
    return out


def render(job_id: str, page_no: int, dpi: int = 120) -> str:
    import pymupdf
    path, rec = pdf_for(job_id)
    out = C.REPORTS / "pages" / rec["sha256"][:12] / f"p{page_no:04d}.png"
    out.parent.mkdir(parents=True, exist_ok=True)
    with pymupdf.open(path) as doc:
        doc[page_no - 1].get_pixmap(dpi=dpi).save(out)
    return str(out.relative_to(C.ROOT))


if __name__ == "__main__":
    cmd, job = sys.argv[1], sys.argv[2]
    if cmd == "find":
        for p, t in find(job, sys.argv[3:]):
            print(p, t)
    elif cmd == "rows":
        print("\n".join(rows(job, int(sys.argv[3]), sys.argv[4] if len(sys.argv) > 4 else None)))
    elif cmd == "render":
        print(render(job, int(sys.argv[3]), int(sys.argv[4]) if len(sys.argv) > 4 else 120))
