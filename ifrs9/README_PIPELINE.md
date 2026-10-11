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
python -m pytest -q                      # tests/test_pipeline.py (synthetic) + tests/test_real_data.py (real data)
python -m ifrs9_recovery export          # rerun so the summary reports the test results
git commit ...                           # commit code/data, then export once more so the summary records that commit
python -m ifrs9_recovery freeze --release-id IFRS9_release_<date>   # copy outputs to releases/<id>/ with hashes
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
| export | `export.py`, `versions.py`, `eligibility.py`, `analysis.py`, `readiness.py`, `summary.py` | `outputs/IFRS9_Verified_Master.xlsx`, `outputs/reconciliation_summary.md`, `outputs/progress_table.csv`, `data/unresolved_gaps.csv`, `data/source_manifest.csv`, `data/missingness_by_outcome.csv`, `reports/index.csv`, `outputs/research_data_handoff.zip` |

## How a value is admitted

The machine never admits a number on its own. `extract` only lists candidate lines and renders the pages they came from. A value reaches the panel only after a reviewer has inspected the rendered page and added a row to `data/review/admissions.csv` (built from `specs.csv` by `python -m ifrs9_recovery.review`). `validate` rejects the row unless all of these hold:

- every evidence field is present;
- **structured scope**: `document_scope` (single_entity / consolidated_and_separate / separate_only / group_only), `column_scope` (an operating-bank column) with its verbatim heading in `column_scope_basis`, and for going-concern codes `opinion_applicability` showing that the auditor's opinion covers the operating bank. Narrative scope text is kept verbatim and is never pattern-matched; a holding-company `Company` column, a group-only document, or a bare "Bank" label without heading evidence is refused;
- **file identity**: SHA-256 is recomputed from the local PDF bytes and must equal the recorded hash and the download ledger; the page must exist; the saved PNG must be pixel-identical to a fresh 110-dpi render of that page;
- **sign**: the normalised value equals raw × unit factor. A sign flip is allowed only with `sign_transform=expense_presented_negative`, a `sign_reason`, and only for impairment/allowance variables. Negative PAT, equity and OCF are preserved;
- **derived values** (`derived_from_verified`) are recomputed from their accepted `component_ids`, which must share entity, year, reporting version, column scope and units;
- the status is `verified_reported` or `derived_from_verified`.

A new bank-year needs PAT, assets, liabilities and equity from one reporting version, and the balance check must pass. A value that differs from a selected one is logged as a conflict unless it is a logged correction.

## Controls

- **Nimble budget:** `MAX_NIMBLE_REQUESTS` is a hard, persistent cap that counts every attempt, retries included, and a stricter cap from an earlier run takes precedence. Concurrency comes from `MAX_NIMBLE_CONCURRENCY`, and 429/5xx responses back off, honouring Retry-After. A 401/403 stops without retrying. Results are cached, and keys are redacted from logs.
- **Downloads:** public https only; private, local and metadata hosts are refused, and every redirect is re-checked. A file is kept only if the bytes start with `%PDF-` and fit within `MAX_PDF_MB`. Each kept file gets a SHA-256.
- **Ratios:** the definitions are unchanged from the starting pack. A ratio is null when an input is missing or the denominator is not positive. Signs are kept.
- **Reconciliation tolerance:** half the rounding unit inferred from the recorded decimals, times the number of rounded components. Published CAR is compared within half its printed display step (from the evidence literal or `data/review/printed_literals.csv`) plus input rounding; there is no global tolerance. Check statuses are pass, fail or documented_source_exception (only for conflicts recorded in `reviewer_conflicts.csv`).
- **Version policy:** `data/review/version_policy.md`; each alternative presentation is classified in `version_decisions.csv`, printed alternatives are kept in `source_alternatives.csv`, and `data/denominator_compatibility.csv` documents average-asset pairs.
- **Field status:** `data/field_status.csv` labels every non-blank cell as baseline_inherited, reported_text_layer, manual_transcription, derived_from_verified (+restated_comparative) or recomputed_ratio.
- **Release record:** `outputs/reconciliation_summary.md` is generated from the CSVs by `summary.py`; `outputs/release_manifest.json` records commit, run ID and hashes; `outputs/test_results.json` reports synthetic and real-data tests separately.
- **Going concern:** auditor pages are queued for review and never coded automatically.

## Review workflow used in this run

1. **Find report pages:** `python -m ifrs9_recovery.locate find <job> "phrase"`. Then `rows <job> <page>` prints each table row with its column x-positions, and `render` saves the page image for inspection.
2. **Record each value as a spec:** add a row to `data/review/specs.csv` giving the job, PDF page, a row regex and the column's x-range. `python -m ifrs9_recovery.review` then reads the value from the PDF text layer. Anything ambiguous (zero or several matching cells) is refused.
3. **Image-only pages:** transcribe into `manual_value`. These values are labelled as manual transcriptions and must pass the balance and loan reconciliations.
4. **Derived totals:** use `derive_from` (for example, individual plus non-individual loans).
5. **Validate:** `python -m ifrs9_recovery validate` applies the admission rules and adds new bank-years only when PAT, assets, liabilities and equity are all present, come from one version, and balance.
6. **Supporting registers:**
   - `data/review/extra_sources.csv`: fallback leads (from the Nimble MCP plugin or web search) with their discovery method.
   - `data/review/nimble_calls.csv`: ledger of Nimble calls, with `channel` separating MCP plugin invocations from REST client requests (retries and failures included); `nimble_usage.json` summarises them.
   - `data/review/document_status.csv`: per-document type and audit-report coverage.
   - `data/review/privacy_inventory.md`: tracked research inputs and exposure.
   - `data/review/going_concern_reviews.csv`: auditor-report reviews behind each going-concern code.
   - `data/review/perimeter_decisions.csv`: entity and column decisions per bank.
   - `data/review/reviewer_conflicts.csv`: restatements and problems found within sources.

## Analytical eligibility (one ruleset)

`ifrs9_recovery/eligibility.py` is the only place that decides whether a value may be used. For every bank-year and
outcome it writes `data/outcome_eligibility.csv` with separate flags: `available`, `descriptive_use`,
`longitudinal_use`, `change_comparable` (year-on-year change is valid), `inferential_use` (primary pooled sample) and
`sensitivity_drop` (fallback presentation: keep in the primary sample, drop in a robustness run). Rules come from
`data/review/eligibility_rules.csv` (curated, each with a reason and source register) plus machine flags: panel
`allowance_pool_status`, panel `liquidity_admissible`, field_status `source_internal_inconsistency`, fallback classes and
unreconciled version mixes in `data/row_versions.csv`. The summary, workbook (Outcome_Eligibility, Outcome_Summary,
Row_Versions sheets), `outputs/analysis/*.csv` and `outputs/readiness/*` all read it through `eligibility.sample()`;
any future plotting or model code must do the same. Tests in `tests/test_real_data.py` check that the same rows are
excluded in every output.

## Reporting versions

`versions.py` writes `data/row_versions.csv`: the primary presentation per bank-year (original-year report; next-year
comparative only when the original is unavailable, flagged for sensitivity), labelled-restatement status, alternatives,
and any version mix with its reconciliation (`data/review/version_reconciliations.csv`). Investigations of open
exceptions are in `data/review/exception_investigations.md`.

## Model readiness

`readiness.py` writes matched pre/post bank trends, Tier 1/Tier 2 descriptives, volatility feasibility, within-bank
variation, model sample sizes and estimator recommendations to `outputs/readiness/`. It warns that IFRS9_D is collinear
with a full set of year fixed effects. No thesis regression is estimated.

## Thesis analysis (12-bank cohort)

`python -m thesis_analysis --B 9999` reads only the frozen release `releases/IFRS9_release_2026-10-11_v1` (every file
hash-verified against `RELEASE_MANIFEST.json` first; nothing is written there) and writes `thesis_results/`: sample
profile, descriptives, trends, matched pre/post, exploratory volatility, bank-FE models (conventional, CR1 bank-clustered
and wild-cluster-bootstrap p-values), robustness, diagnostics, going-concern event description, tables, figures,
`analysis_master.xlsx`, `analysis_report.md`, `interpretation.md` and `thesis_results_handoff.zip`. FCMB is formally
excluded from the cohort and not replaced. IFRS9_D is never combined with year fixed effects. Requires numpy, pandas,
scipy, statsmodels (>= 0.15), matplotlib and openpyxl. `tests/test_thesis_analysis.py` checks the outputs against the
release and the report against the CSVs.
