# Reconciliation summary

Generated 2026-10-10T16:35:51+00:00 by `python -m ifrs9_recovery export`.

## Headline

- Baseline: **47** selected bank-years (25 pre / 22 post). Original inputs are unchanged (SHA-256 verified).
- New bank-years admitted this run: **0**.
- Panel after run: **47** unique bank-years, 11 banks; 25 pre-adoption, 22 post-adoption.
- Blank fields filled: 0. Corrections to selected values: 0. Derived values changed by recomputation: 0.
- Remaining: 83 bank-year positions and 354 field requests in selected rows.
- Nimble discovery blocker: `auth_missing: NIMBLE_API_KEY not set in environment or local .env`.
- Report hosts refused by the session's network egress policy: arthursteven.com, doclib.ngxgroup.com, first-holdco.com, greenwichregistrars.com, gtbank-plc.files.svdcdn.com, sterling.ng, www.accessbankplc.com, www.annualreports.com, www.fidelitybank.ng, www.financialafrik.com, www.stanbicibtcbank.com, www.ubagroup.com.
- Nimble requests attempted: 0 of the 100 cap. Report downloads: egress_denied 31.

This is not 130 observations. Report links are leads and candidate amounts are unverified.

## Progress table

| Measure | Value |
|---|---|
| Baseline selected bank-years | 47 |
| New bank-years admitted | 0 |
| Panel bank-years after run | 47 |
| pre-adoption (2013-2017) | 25 |
| post-adoption (2018-2022) | 22 |
| Banks represented | 11 |
| Blank fields filled from reviewed evidence | 0 |
| Evidence-backed corrections to selected values | 0 |
| Derived values changed by recomputation | 0 |
| Exclusions enforced (documented exceptions) | 0 |
| Checked exceptions retained / violated | 8 / 0 |
| Inherited Union exceptions carried (U01-U15) | 15 |
| Reconciliation checks passed / run | 84 / 85 |
| Selected values matching an inherited evidence record | 611 / 615 |
| Nimble requests attempted (budget cap) | 0 (100) |
| Discovery jobs by status | blocked=76 |
| Report downloads by status | egress_denied=31 |
| PDFs archived and hashed | 0 |
| Remaining bank-year positions | 83 |
| Remaining field requests in selected rows | 354 |
| Conflicts recorded | 62 |

## Missingness by outcome (panel rows)

| Outcome | Available | Missing | Pre | Post | Banks |
|---|---|---|---|---|---|
| ROA on average assets (%) | 33 | 14 | 16 | 17 | 11 |
| Equity / assets (%) | 47 | 0 | 25 | 22 | 11 |
| OCF / average assets (%) | 29 | 18 | 13 | 16 | 8 |
| Loan allowance / gross loans (%) | 38 | 9 | 18 | 20 | 8 |
| Liabilities / assets (%) | 47 | 0 | 25 | 22 | 11 |
| Reported CAR (%) | 38 | 9 | 18 | 20 | 8 |
| Capital / RWA (%) | 19 | 28 | 4 | 15 | 4 |
| Reported NPL ratio (%) | 14 | 33 | 13 | 1 | 6 |
| NPL amount / gross loans (%) | 9 | 38 | 5 | 4 | 2 |
| Broad NPL coverage (%) | 9 | 38 | 5 | 4 | 2 |
| Stage 3 coverage (%) | 4 | 43 | 0 | 4 | 1 |
| Total impairment / average assets (%) | 31 | 16 | 14 | 17 | 10 |
| Admitted domestic liquidity ratio (%) | 10 | 37 | 5 | 5 | 3 |
| Going-concern uncertainty code | 2 | 45 | 0 | 2 | 2 |

## Reconciliation

84 of 85 checks pass at rounding-based tolerance. Failures:

- UBA 2018: reported CAR vs capital/RWA residual 0.338 (tolerance 0.06) rounding from recorded decimals; basis=2018 full impact / reported-vintage Basel basis; see notes; transitional=22.08

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

611 of 615 non-blank selected input values match an inherited evidence record. Values with no match are listed in `data/evidence_backing.csv`. That is a lineage gap, not proof of error.

## Conflicts

- candidate_vs_selected: 62

## Workbook

Formula audit after LibreOffice recalculation: {'cells_checked': 799, 'numeric_differences': 0, 'mismatches': 0, 'excel_errors': 0}.

## Not done

- No regression, hypothesis test or volatility estimate was run.
- No going-concern code was added: no original-year auditor report was reviewed in this run.
- No candidate amount was promoted to the panel.
