# IFRS 9 data recovery pipeline

This folder recovers and verifies data for the Nigerian IFRS 9 bank panel (2013–2022, 13 banks, a 130-position frame). The starting point is the 47 selected bank-years in `inputs/`. `CLAUDE_PROMPT.md` sets the rules.

## Run

```bash
cd ifrs9
python -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt          # exact versions used: requirements.lock (Python 3.13)
cp .env.example .env                     # put NIMBLE_API_KEY in .env (gitignored); never commit it
python -m ifrs9_recovery inventory       # verify input hashes, extract the update pack safely
python -m ifrs9_recovery plan            # build data/task_queue.csv and estimate Nimble requests
python -m ifrs9_recovery pilot           # priority-1 jobs (Wema, Union) end to end
python -m ifrs9_recovery discover --resume
python -m ifrs9_recovery download --resume
python -m ifrs9_recovery extract --resume
python -m ifrs9_recovery validate
python -m ifrs9_recovery export
python -m pytest -q
```

`python -m ifrs9_recovery all` runs every stage in order. `--max-priority N` limits discovery and downloads to the first N priority batches. Every stage checkpoints to `state/` after each job, so a rerun resumes where the last one stopped.

## Stages

| Stage | Module | Output |
|---|---|---|
| inventory | `inventory.py` | `data/inventory.json`; refuses to run if an input hash changed |
| plan | `queue.py` | `data/task_queue.csv` (seed PDFs, archive pages, one search per uncovered bank-year), `data/queue_plan.json` |
| discover | `discover.py`, `nimble.py` | `data/discovery_leads.csv` (unverified leads), `state/discover_state.json`, `state/nimble_budget.json` |
| download | `download.py` | `reports/<bank>/*.pdf`, `data/download_log.csv`, `state/download_state.json` |
| extract | `extract.py` | `data/page_index.csv`, `data/pdf_candidates.csv`, `data/going_concern_review_queue.csv`, rendered pages in `reports/pages/` |
| validate | `validate.py`, `evidence.py`, `candidates.py`, `ratios.py` | `data/verified_panel.csv`, `evidence_long.csv`, `change_register.csv`, `reconciliation_checks.csv`, `exceptions_register.csv`, `conflicts.csv`, `candidates.csv`, `evidence_backing.csv` |
| export | `export.py` | `outputs/IFRS9_Verified_Master.xlsx`, `outputs/reconciliation_summary.md`, `outputs/progress_table.csv`, `data/unresolved_gaps.csv`, `data/source_manifest.csv`, `data/missingness_by_outcome.csv`, `reports/index.csv`, `outputs/research_data_handoff.zip` |

## How a value is admitted

The machine never admits a number on its own. `extract` only lists candidate lines and renders the pages they came from. A value reaches the panel only after a reviewer has inspected the rendered page and added a row to `data/review/admissions.csv`. That file has the full evidence schema plus `admit`, `is_correction` and `correction_reason`. `validate` then rejects the row if any of these hold:

- an evidence field is missing;
- the scope or column heading is Group or Consolidated;
- the legal entity looks like a holding company, group or foreign subsidiary;
- the PDF hash does not match a downloaded report;
- the rendered page image is missing;
- the normalised value does not equal the raw value times the unit factor;
- the status is not `verified_reported` or `derived_from_verified`.

A new bank-year needs PAT, assets, liabilities and equity, all from one reporting version, and the balance check must pass. A value that differs from a selected one is logged as a conflict unless the row is marked as a correction with a reason.

## Controls

- **Nimble budget:** `MAX_NIMBLE_REQUESTS` is a hard, persistent cap that counts every attempt, retries included, and a stricter cap from an earlier run takes precedence. Concurrency comes from `MAX_NIMBLE_CONCURRENCY`, and 429/5xx responses back off, honouring Retry-After. A 401/403 stops without retrying. Results are cached, and keys are redacted from logs.
- **Downloads:** public https only; private, local and metadata hosts are refused, and every redirect is re-checked. A file is kept only if the bytes start with `%PDF-` and fit within `MAX_PDF_MB`. Each kept file gets a SHA-256.
- **Ratios:** the definitions are unchanged from the starting pack. A ratio is null when an input is missing or the denominator is not positive. Signs are kept.
- **Reconciliation tolerance:** half the rounding unit inferred from the recorded decimals, multiplied by the number of rounded components. Published CAR is allowed a whole-percent step only where the basis note documents a whole or rounded ratio.
- **Going concern:** auditor pages are queued for review and never coded automatically.
