"""Record test outcomes per suite so the release summary reports what actually ran."""
import json
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

SUITES = {"test_pipeline.py": "synthetic/mock unit tests", "test_real_data.py": "real-data regression tests"}
_results = defaultdict(lambda: defaultdict(int))


def pytest_runtest_logreport(report):
    if report.when == "call" or (report.when == "setup" and report.outcome != "passed"):
        suite = SUITES.get(Path(report.nodeid.split("::")[0]).name, "other")
        _results[suite][report.outcome] += 1


def pytest_sessionfinish(session, exitstatus):
    out = Path(__file__).resolve().parent.parent / "outputs" / "test_results.json"
    if not _results:
        return
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"run_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
                               "exit_status": int(exitstatus),
                               "suites": {k: dict(v) for k, v in _results.items()}}, indent=2))
