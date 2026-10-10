"""Paths, limits and secret handling.

NIMBLE_API_KEY is read from the process environment or a gitignored local .env.
It is never printed, logged, cached or written to any output.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

INPUTS = ROOT / "inputs"
TASKS = ROOT / "tasks"
SEEDS = ROOT / "seeds"
CHECKS = ROOT / "checks"
DATA = ROOT / "data"
OUTPUTS = ROOT / "outputs"
STATE = ROOT / "state"
CACHE = ROOT / "cache"
LOGS = ROOT / "logs"
REPORTS = ROOT / "reports"
WORK = ROOT / "work"  # safe extraction of the update-pack archive

SELECTED_CSV = INPUTS / "IFRS9_Selected_Data_Updated_20261010.csv"
MASTER_XLSX = INPUTS / "IFRS9_Master_Data_Updated_20261010.xlsx"
UPDATE_PACK = INPUTS / "IFRS9_Data_Update_Pack_20261010.zip"
RAW_CSV = INPUTS / "extract_nigerian_bank_ifrs_9_financial_data_6085ddb6.csv"
RAW_DOCX = INPUTS / "nigerian_banks_ifrs9_thesis_data.docx"

NIMBLE_BASE = "https://sdk.nimbleway.com/v2"
# The handoff contract (checked 10 Oct 2026) shows "standard"; the docs overview
# found via search lists lite|fast|deep. Keep it configurable and confirm before use.
NIMBLE_SEARCH_DEPTH_DEFAULT = "standard"
NIMBLE_DOCS = [
    "https://docs.nimbleway.com/home",
    "https://docs.nimbleway.com/nimble-sdk/web-tools/search",
    "https://docs.nimbleway.com/nimble-sdk/web-tools/extract/quickstart",
    "https://docs.nimbleway.com/nimble-sdk/sdks/python",
]

STUDY_YEARS = range(2013, 2023)
ADOPTION_YEAR = 2018


def _read_dotenv(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    if not path.is_file():
        return values
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        values[k.strip()] = v.strip().strip('"').strip("'")
    return values


@dataclass(frozen=True)
class Settings:
    max_requests: int = 100
    max_concurrency: int = 2
    max_pdf_mb: int = 100
    dry_run: bool = False
    search_depth: str = NIMBLE_SEARCH_DEPTH_DEFAULT
    timeout_s: float = 60.0
    max_retries: int = 3
    _key: str | None = field(default=None, repr=False)

    @property
    def has_key(self) -> bool:
        return bool(self._key)

    def auth_header(self) -> dict[str, str]:
        if not self._key:
            raise RuntimeError("NIMBLE_API_KEY is not configured")
        return {"Authorization": f"Bearer {self._key}"}


def load_settings(env: dict[str, str] | None = None, dotenv: Path | None = None) -> Settings:
    merged = _read_dotenv(dotenv if dotenv is not None else ROOT / ".env")
    merged.update({k: v for k, v in (env if env is not None else os.environ).items()})
    def _int(name: str, default: int) -> int:
        try:
            return int(merged.get(name, default))
        except ValueError:
            return default
    return Settings(
        max_requests=_int("MAX_NIMBLE_REQUESTS", 100),
        max_concurrency=max(1, _int("MAX_NIMBLE_CONCURRENCY", 2)),
        max_pdf_mb=_int("MAX_PDF_MB", 100),
        dry_run=str(merged.get("NIMBLE_DRY_RUN", "0")).strip() in ("1", "true", "yes"),
        search_depth=merged.get("NIMBLE_SEARCH_DEPTH", NIMBLE_SEARCH_DEPTH_DEFAULT),
        _key=(merged.get("NIMBLE_API_KEY") or None),
    )


def ensure_dirs() -> None:
    for d in (DATA, OUTPUTS, STATE, CACHE, LOGS, REPORTS, WORK):
        d.mkdir(parents=True, exist_ok=True)
