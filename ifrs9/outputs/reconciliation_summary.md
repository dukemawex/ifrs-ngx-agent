# Reconciliation summary

Generated 2026-10-10T17:02:04+00:00 by `python -m ifrs9_recovery export`.

## Headline

- Baseline: **47** selected bank-years (25 pre / 22 post). Original inputs are unchanged (SHA-256 verified).
- New bank-years admitted this run: **14** — Wema 2021, Union 2016, Union 2015, Stanbic 2022, Stanbic 2021, Stanbic 2020, Zenith 2016, Zenith 2017, Zenith 2018, Zenith 2019, Zenith 2020, GTBank 2019, GTBank 2018, GTBank 2017.
- Panel after run: **61** unique bank-years, 12 banks; 30 pre-adoption, 31 post-adoption.
- Blank fields filled: 0. Corrections to selected values: 0. Derived values changed by recomputation: 0.
- Remaining: 69 bank-year positions and 354 field requests in selected rows.
- Nimble discovery blocker: `auth_missing: NIMBLE_API_KEY not set in environment or local .env`.
- Report hosts refused by the session's network egress policy: none.
- Nimble requests attempted: 0 of the 100 cap. Report downloads: downloaded 39, http_error 5.

This is not 130 observations. Report links are leads and candidate amounts are unverified.

## Progress table

| Measure | Value |
|---|---|
| Baseline selected bank-years | 47 |
| New bank-years admitted | 14 |
| Panel bank-years after run | 61 |
| pre-adoption (2013-2017) | 30 |
| post-adoption (2018-2022) | 31 |
| Banks represented | 12 |
| Blank fields filled from reviewed evidence | 0 |
| Evidence-backed corrections to selected values | 0 |
| Derived values changed by recomputation | 0 |
| Exclusions enforced (documented exceptions) | 0 |
| Checked exceptions retained / violated | 8 / 0 |
| Inherited Union exceptions carried (U01-U15) | 15 |
| Reconciliation checks passed / run | 121 / 123 |
| Selected values matching an inherited evidence record | 836 / 840 |
| Nimble requests attempted (budget cap) | 0 (100) |
| Discovery jobs by status | blocked=76 |
| Report downloads by status | downloaded=39; http_error=5 |
| PDFs archived and hashed | 39 |
| Remaining bank-year positions | 69 |
| Remaining field requests in selected rows | 354 |
| Conflicts recorded | 128 |

## Missingness by outcome (panel rows)

| Outcome | Available | Missing | Pre | Post | Banks |
|---|---|---|---|---|---|
| ROA on average assets (%) | 46 | 15 | 21 | 25 | 12 |
| Equity / assets (%) | 61 | 0 | 30 | 31 | 12 |
| OCF / average assets (%) | 42 | 19 | 18 | 24 | 10 |
| Loan allowance / gross loans (%) | 52 | 9 | 23 | 29 | 10 |
| Liabilities / assets (%) | 61 | 0 | 30 | 31 | 12 |
| Reported CAR (%) | 48 | 13 | 22 | 26 | 9 |
| Capital / RWA (%) | 29 | 32 | 8 | 21 | 5 |
| Reported NPL ratio (%) | 14 | 47 | 13 | 1 | 6 |
| NPL amount / gross loans (%) | 14 | 47 | 7 | 7 | 3 |
| Broad NPL coverage (%) | 14 | 47 | 7 | 7 | 3 |
| Stage 3 coverage (%) | 4 | 57 | 0 | 4 | 1 |
| Total impairment / average assets (%) | 44 | 17 | 19 | 25 | 12 |
| Admitted domestic liquidity ratio (%) | 10 | 51 | 5 | 5 | 3 |
| Going-concern uncertainty code | 5 | 56 | 1 | 4 | 4 |

## Reconciliation

121 of 123 checks pass at rounding-based tolerance. Failures:

- UBA 2018: reported CAR vs capital/RWA residual 0.338 (tolerance 0.06) rounding from recorded decimals; basis=2018 full impact / reported-vintage Basel basis; see notes; transitional=22.08
- Wema 2021: reported CAR vs capital/RWA residual 0.1469 (tolerance 0.015) rounding from recorded decimals; basis=; transitional=

## Exceptions

- X-UBA-2015-ALW (UBA 2015 loan_allowance): retained
- X-UBA-2016-ALW (UBA 2016 loan_allowance): retained
- X-UBA-2022-LIQ (UBA 2022 liquidity_admissible): retained
- X-UNION-2017-PAT (Union 2017 pat): retained
- X-UNION-2018-ALW (Union 2018 loan_allowance): retained
- X-UNION-2022-S3 (Union 2022 stage3_coverage): retained (documented; value not altered)
- X-STERLING-2018-19 (Sterling 2018 scope): retained (documented; value not altered)
- X-WEMA-2015-PAT (Wema 2015 pat): retained (documented; value not altered)

15 inherited Union exceptions (U01–U15) are carried in the exceptions register.

## Evidence lineage of selected values

836 of 840 non-blank selected input values match an inherited evidence record. Values with no match are listed in `data/evidence_backing.csv`. That is a lineage gap, not proof of error.

## Conflicts

- candidate_vs_selected: 119
- not_admitted_basis_unclear: 1
- restated_comparative: 4
- source_internal_inconsistency: 2
- source_unit_label_error: 1
- source_vs_selected: 1

## Workbook

Formula audit after LibreOffice recalculation: {'cells_checked': 1037, 'numeric_differences': 0, 'mismatches': 0, 'excel_errors': 0}.

## Not done

- No regression, hypothesis test or volatility estimate was run.
- No going-concern code was added: no original-year auditor report was reviewed in this run.
- No candidate amount was promoted to the panel.
