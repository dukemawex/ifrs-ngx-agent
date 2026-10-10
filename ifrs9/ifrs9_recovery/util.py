"""Small, dependency-free helpers: numbers, CSV, hashing, atomic writes, checkpoints."""
from __future__ import annotations

import csv
import hashlib
import json
import math
import os
import re
import tempfile
import zipfile
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Iterable

MISSING = ("", "none", "na", "n/a", "nan", "null")
SECRET_RE = re.compile(r"(Bearer\s+)[A-Za-z0-9._\-]+|(api[_-]?key[\"'=:\s]+)[A-Za-z0-9._\-]+", re.I)


def utcnow() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def number(value: Any) -> float | None:
    """Parse a reported amount. Blank stays None (never zero); (x) and unicode minus are negative.

    A bare dash is ambiguous (nil or not applicable) and is returned as None for a
    human to resolve from context.
    """
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value) if math.isfinite(float(value)) else None
    s = str(value).strip().replace(",", "").replace("−", "-").replace("–", "-")
    if s.lower() in MISSING or s in ("-", "--"):
        return None
    neg = s.startswith("(") and s.endswith(")")
    if neg:
        s = s[1:-1].strip()
    out = float(s)
    if not math.isfinite(out):
        raise ValueError(f"Non-finite numeric input: {value!r}")
    return -abs(out) if neg else out


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: Iterable[dict[str, Any]], fieldnames: list[str] | None = None) -> int:
    rows = list(rows)
    if fieldnames is None:
        fieldnames = []
        for r in rows:
            fieldnames += [k for k in r if k not in fieldnames]
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: ("" if r.get(k) is None else r.get(k)) for k in fieldnames})
    os.replace(tmp, path)
    return len(rows)


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, suffix=".tmp")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False, default=str)
    os.replace(tmp, path)


def read_json(path: Path, default: Any = None) -> Any:
    if not path.is_file():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def redact(text: str, secrets: Iterable[str] = ()) -> str:
    text = SECRET_RE.sub(lambda m: (m.group(1) or m.group(2)) + "[REDACTED]", text)
    for s in secrets:
        if s:
            text = text.replace(s, "[REDACTED]")
    return text


def append_log(path: Path, record: dict[str, Any], secrets: Iterable[str] = ()) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    line = redact(json.dumps({"ts": utcnow(), **record}, default=str), secrets)
    with path.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


def safe_extract(zip_path: Path, dest: Path) -> list[str]:
    """Extract an archive, refusing absolute paths, '..' segments and symlinks."""
    dest = dest.resolve()
    dest.mkdir(parents=True, exist_ok=True)
    names = []
    with zipfile.ZipFile(zip_path) as zf:
        for info in zf.infolist():
            p = PurePosixPath(info.filename.replace("\\", "/"))
            if p.is_absolute() or ".." in p.parts or (p.parts and ":" in p.parts[0]):
                raise ValueError(f"Unsafe archive member rejected: {info.filename!r}")
            if (info.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError(f"Symlink archive member rejected: {info.filename!r}")
            target = (dest / Path(*p.parts)).resolve()
            if dest not in target.parents and target != dest:
                raise ValueError(f"Archive member escapes destination: {info.filename!r}")
            if info.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            with zf.open(info) as src, target.open("wb") as out:
                out.write(src.read())
            names.append(str(PurePosixPath(*p.parts)))
    return names


def bank_slug(bank: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", bank.lower()).strip("_")
