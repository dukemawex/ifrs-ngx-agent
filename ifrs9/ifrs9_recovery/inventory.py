"""Stage 1: verify the frozen inputs and describe the starting point."""
from __future__ import annotations

from collections import Counter
from pathlib import Path

from . import config as C
from .util import read_csv, read_json, safe_extract, sha256_file, utcnow, write_json


def verify_input_hashes() -> list[dict]:
    manifest = read_json(C.CHECKS / "snapshot_manifest.json", {})
    results = []
    for item in manifest.get("original_inputs", []):
        p = C.ROOT / item["relative_path"]
        actual = sha256_file(p) if p.is_file() else None
        results.append({
            "relative_path": item["relative_path"],
            "expected_sha256": item["sha256"],
            "actual_sha256": actual,
            "bytes": p.stat().st_size if p.is_file() else None,
            "unchanged": actual == item["sha256"],
        })
    return results


def extract_update_pack() -> list[str]:
    return safe_extract(C.UPDATE_PACK, C.WORK / "update_pack")


def selected_summary(rows: list[dict]) -> dict:
    keys = [(r["bank"], int(r["year"])) for r in rows]
    return {
        "rows": len(rows),
        "unique_bank_years": len(set(keys)),
        "banks": len({b for b, _ in keys}),
        "pre_adoption_2013_2017": sum(y < C.ADOPTION_YEAR for _, y in keys),
        "post_adoption_2018_2022": sum(y >= C.ADOPTION_YEAR for _, y in keys),
        "rows_per_bank": dict(sorted(Counter(b for b, _ in keys).items())),
    }


def run() -> dict:
    C.ensure_dirs()
    hashes = verify_input_hashes()
    if not all(h["unchanged"] for h in hashes):
        bad = [h["relative_path"] for h in hashes if not h["unchanged"]]
        raise SystemExit(f"Original inputs changed or missing: {bad}")
    members = extract_update_pack()
    selected = read_csv(C.SELECTED_CSV)
    gaps = read_csv(C.TASKS / "bank_year_gaps.csv")
    fgaps = read_csv(C.TASKS / "field_gaps_selected.csv")
    seeds = read_csv(C.SEEDS / "report_sources.csv")
    coverage = read_csv(C.TASKS / "coverage_before.csv")
    summary = selected_summary(selected)
    inv = {
        "generated_utc": utcnow(),
        "input_hashes": hashes,
        "update_pack_members": members,
        "selected": summary,
        "frame_positions": len(coverage),
        "frame_status_counts": dict(Counter(r["Evidence status"] for r in coverage)),
        "bank_year_gap_tasks": len(gaps),
        "bank_year_gap_status": dict(Counter(r["current_status"] for r in gaps)),
        "field_gap_requests": len(fgaps),
        "field_gap_by_field": dict(Counter(r["field"] for r in fgaps).most_common()),
        "seed_sources": len(seeds),
        "seed_unique_urls": len({s["url"] for s in seeds}),
    }
    checks = [
        ("baseline rows = 47", summary["rows"] == 47),
        ("unique bank-years = rows", summary["unique_bank_years"] == summary["rows"]),
        ("pre = 25", summary["pre_adoption_2013_2017"] == 25),
        ("post = 22", summary["post_adoption_2018_2022"] == 22),
        ("frame = 130", len(coverage) == 130),
        ("gaps = 83", len(gaps) == 83),
        ("selected + gaps = 130", summary["rows"] + len(gaps) == 130),
        ("field requests = 354", len(fgaps) == 354),
    ]
    inv["consistency_checks"] = [{"check": c, "passed": ok} for c, ok in checks]
    write_json(C.DATA / "inventory.json", inv)
    return inv
