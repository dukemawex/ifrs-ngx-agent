"""Command line: python -m ifrs9_recovery <stage> [--resume] [--max-priority N]."""
from __future__ import annotations

import argparse
import json
import sys

from . import config as C


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="ifrs9_recovery", description=__doc__)
    ap.add_argument("stage", choices=["inventory", "plan", "discover", "download", "extract", "validate", "export",
                                      "pilot", "all", "freeze"])
    ap.add_argument("--release-id", default=None)
    ap.add_argument("--resume", action="store_true", default=True)
    ap.add_argument("--fresh", action="store_true", help="ignore saved stage state")
    ap.add_argument("--max-priority", type=int, default=None)
    ap.add_argument("--no-render", action="store_true")
    a = ap.parse_args(argv)
    resume = not a.fresh
    C.ensure_dirs()
    settings = C.load_settings()
    print(f"settings: cap={settings.max_requests} concurrency={settings.max_concurrency} max_pdf_mb={settings.max_pdf_mb} "
          f"dry_run={settings.dry_run} search_depth={settings.search_depth} key_configured={settings.has_key}")

    from . import discover, download, export, extract, freeze, inventory, queue, validate

    def show(name, res):
        print(f"[{name}] " + json.dumps(res, indent=2, default=str))

    stages = {
        "inventory": lambda: inventory.run(),
        "plan": lambda: queue.build(),
        "discover": lambda: discover.run(resume, settings, max_priority=a.max_priority),
        "download": lambda: download.run(resume, settings, max_priority=a.max_priority),
        "extract": lambda: extract.run(resume, render=not a.no_render),
        "validate": lambda: validate.run(),
        "export": lambda: export.run(),
    }
    if a.stage == "freeze":
        show("freeze", freeze.run(a.release_id or "release"))
        return 0
    if a.stage == "pilot":
        order, a.max_priority = list(stages), a.max_priority or 1
    elif a.stage == "all":
        order = list(stages)
    else:
        order = [a.stage]
    for name in order:
        show(name, stages[name]())
    return 0


if __name__ == "__main__":
    sys.exit(main())
