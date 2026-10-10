# Reconciliation summary

Generated 2026-10-10T17:19:14+00:00 by `python -m ifrs9_recovery export`.

## Headline

- Baseline: **47** selected bank-years (25 pre / 22 post). Original inputs are unchanged (SHA-256 verified).
- New bank-years admitted this run: **18** — Wema 2021, Union 2016, Union 2015, Stanbic 2022, Stanbic 2021, Stanbic 2020, Zenith 2016, Zenith 2017, Zenith 2018, Zenith 2019, Zenith 2020, GTBank 2019, GTBank 2018, GTBank 2017, First Bank 2017, First Bank 2016, Fidelity 2022, Fidelity 2021.
- Panel after run: **65** unique bank-years, 12 banks; 32 pre-adoption, 33 post-adoption.
- Blank fields filled: 9. Corrections to selected values: 0. Derived values changed by recomputation: 0.
- Remaining: 65 bank-year positions and 345 field requests in selected rows.
- Nimble: REST client blocked (`auth_missing: NIMBLE_API_KEY not set in environment or local .env`); discovery ran through the Nimble MCP plugin instead: 15 search calls logged in `data/review/nimble_mcp_calls.csv`, within the 100-request cap.
- Report hosts still refused by egress policy at last attempt: none.
- Report downloads: downloaded 40, http_error 5.

This is not 130 observations. Report links are leads and candidate amounts are unverified.

## Progress table

| Measure | Value |
|---|---|
| Baseline selected bank-years | 47 |
| New bank-years admitted | 18 |
| Panel bank-years after run | 65 |
| pre-adoption (2013-2017) | 32 |
| post-adoption (2018-2022) | 33 |
| Banks represented | 12 |
| Blank fields filled from reviewed evidence | 9 |
| Evidence-backed corrections to selected values | 0 |
| Derived values changed by recomputation | 0 |
| Exclusions enforced (documented exceptions) | 0 |
| Checked exceptions retained / violated | 8 / 0 |
| Inherited Union exceptions carried (U01-U15) | 15 |
| Reconciliation checks passed / run | 134 / 136 |
| Selected values matching an inherited evidence record | 917 / 921 |
| Nimble requests: REST client / MCP plugin (shared cap) | 0 / 15 (cap 100) |
| Going-concern codes from full original-year auditor reports (this run) | 18 |
| Discovery jobs by status | blocked=76 |
| Report downloads by status | downloaded=40; http_error=5 |
| PDFs archived and hashed | 40 |
| Remaining bank-year positions | 65 |
| Remaining field requests in selected rows | 345 |
| Conflicts recorded | 139 |

## Missingness by outcome (panel rows)

| Outcome | Available | Missing | Pre | Post | Banks |
|---|---|---|---|---|---|
| ROA on average assets (%) | 48 | 17 | 22 | 26 | 12 |
| Equity / assets (%) | 65 | 0 | 32 | 33 | 12 |
| OCF / average assets (%) | 44 | 21 | 19 | 25 | 10 |
| Loan allowance / gross loans (%) | 56 | 9 | 25 | 31 | 10 |
| Liabilities / assets (%) | 65 | 0 | 32 | 33 | 12 |
| Reported CAR (%) | 53 | 12 | 24 | 29 | 10 |
| Capital / RWA (%) | 34 | 31 | 10 | 24 | 8 |
| Reported NPL ratio (%) | 14 | 51 | 13 | 1 | 6 |
| NPL amount / gross loans (%) | 14 | 51 | 7 | 7 | 3 |
| Broad NPL coverage (%) | 14 | 51 | 7 | 7 | 3 |
| Stage 3 coverage (%) | 4 | 61 | 0 | 4 | 1 |
| Total impairment / average assets (%) | 45 | 20 | 19 | 26 | 12 |
| Admitted domestic liquidity ratio (%) | 10 | 55 | 5 | 5 | 3 |
| Going-concern uncertainty code | 19 | 46 | 3 | 16 | 8 |

## Reconciliation

134 of 136 checks pass at rounding-based tolerance. Failures:

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

917 of 921 non-blank selected input values match an inherited evidence record. Values with no match are listed in `data/evidence_backing.csv`. That is a lineage gap, not proof of error.

## Conflicts

- candidate_vs_selected: 131
- restated_comparative: 4
- source_internal_inconsistency: 2
- source_unit_label_error: 1
- source_vs_selected: 1

## Workbook

Formula audit after LibreOffice recalculation: {'cells_checked': 1105, 'numeric_differences': 0, 'mismatches': 0, 'excel_errors': 0}.

## Not done

- No regression, hypothesis test or volatility estimate was run.
- No going-concern code was added: no original-year auditor report was reviewed in this run.
- No candidate amount was promoted to the panel.
