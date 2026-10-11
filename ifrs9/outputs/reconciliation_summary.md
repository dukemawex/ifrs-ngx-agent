# Reconciliation summary

Generated 2026-10-11T06:01:40+00:00 from the saved outputs (code commit `3e764fd0a9c5b2f3644fcfdf51b1137fd34dd978`, branch `claude/zen-hamilton-v2s80b`).
Every number below is computed by `ifrs9_recovery.summary.release_stats()`; see `outputs/release_stats.json`.

## Panel

- Selected bank-years: **97** across 12 banks (50 pre-adoption, 47 post-adoption).
- Baseline rows: 47 (all 47 retained); additional rows admitted: 50.
- These are selected rows, not complete observations for every endpoint (see endpoint table).

## What changed relative to the frozen baseline

- Raw input files: unchanged (SHA-256 checked by `inventory`).
- Non-blank baseline measurements changed: 0 (corrections are the only route).
- Authorised fills of blank baseline cells: 9 (gcu 9).
- Recomputed derived values that differ from stored: 0.
- Additional bank-years: 50.
- Field basis of all non-blank cells: baseline_inherited 615, derived_from_verified 18, derived_from_verified+restated_comparative 4, manual_transcription 95, manual_transcription+restated_comparative 4, recomputed_ratio 1027, reported_text_layer 637, reported_text_layer+restated_comparative 37.

## Admission and reconciliation

- Admissions: 820 accepted, 0 rejected (file hash recomputed, page and rendered image re-verified, structured scope, explicit sign transform, derived values recomputed).
- Reconciliation checks run: 217; pass 215; fail 0; documented source exception 2.
- Evidence lineage: 1410 of 1410 non-blank inputs matched to an evidence record; 6 carry an explicit qualification.
- Average-asset denominators: 72 checked against prior-year closing assets; 4 differ (listed in `data/denominator_compatibility.csv`). Each ratio uses the opening balance from the same report as its closing balance; differing pairs are not smoothed.
  - Access 2020 (opening 6307588.216 from 2020 annual report, as originally reported; prior closing 6311041.282 from 2019 annual report, as originally reported)
  - Sterling 2017 (opening 830805.0 from 2017 annual report, as originally reported; prior closing 830802.224 from 2016 annual report, as originally reported)
  - Sterling 2022 (opening 1606898.0 from 2022 annual report, as originally reported; prior closing 1611749.0 from 2021 annual report, as originally reported)
  - Union 2015 (opening 922755.0 from 2016 annual report; 2015 restated comparative; prior closing 920936.0 from Prior source-selection policy retained; original evidence preserved in accompanying pack.)

## Outcome eligibility (one ruleset: `ifrs9_recovery.eligibility`, `data/outcome_eligibility.csv`)

Available = value present; descriptive/longitudinal/inferential uses are distinct; change pairs = year-on-year changes that are comparable; fallback rows stay in the primary sample but are dropped in sensitivity runs.

| Outcome | Available | Descriptive | Longitudinal | Change pairs | Eligible (inferential) | Excluded from inference | Banks | Pre | Post | Tier 1 | Tier 2 | Fallback rows |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gcu | 46 | 46 | 46 | 22 | 46 | 0 | 10 | 18 | 28 | 13 | 33 | 0 |
| car | 76 | 76 | 76 | 57 | 74 | 2 | 11 | 37 | 37 | 31 | 43 | 2 |
| car_computed | 57 | 57 | 57 | 38 | 54 | 3 | 11 | 23 | 31 | 25 | 29 | 2 |
| roa | 77 | 77 | 77 | 51 | 77 | 0 | 12 | 39 | 38 | 32 | 45 | 3 |
| eqta | 97 | 97 | 97 | 81 | 97 | 0 | 12 | 50 | 47 | 40 | 57 | 7 |
| ocf_ratio | 71 | 71 | 71 | 48 | 71 | 0 | 11 | 36 | 35 | 30 | 41 | 3 |
| allr | 82 | 82 | 81 | 62 | 81 | 1 | 11 | 40 | 41 | 35 | 46 | 5 |
| impairment_assets | 74 | 74 | 72 | 49 | 72 | 2 | 12 | 35 | 37 | 30 | 42 | 2 |
| npl_calc | 14 | 14 | 14 | 9 | 14 | 0 | 3 | 7 | 7 | 6 | 8 | 1 |
| broad_coverage | 14 | 14 | 13 | 7 | 13 | 1 | 3 | 7 | 6 | 6 | 7 | 1 |
| stage3_coverage | 6 | 6 | 5 | 3 | 5 | 1 | 2 | 0 | 5 | 0 | 5 | 0 |
| liquidity | 10 | 10 | 10 | 7 | 10 | 0 | 3 | 5 | 5 | 7 | 3 | 0 |
| leverage | 97 | 97 | 97 | 81 | 97 | 0 | 12 | 50 | 47 | 40 | 57 | 7 |

Rows excluded from inference (rule ids in `data/outcome_eligibility.csv`, reasons in `data/review/eligibility_rules.csv`):

- car: Fidelity 2016 (AUTO-FLAG;EL-FID16-CAR); Wema 2021 (AUTO-FALLBACK;AUTO-FLAG;EL-WEMA21-CAR)
- car_computed: Fidelity 2016 (EL-FID16-CAR); Stanbic 2020 (AUTO-FLAG;EL-STAN20-CAPITAL); Wema 2021 (AUTO-FALLBACK;EL-WEMA21-CAR)
- allr: Union 2018 (AUTO-POOL;EL-UNION18-ALLOWANCE)
- impairment_assets: Unity 2017 (EL-UNITY17-IMP); Wema 2021 (AUTO-FALLBACK;EL-WEMA21-IMP)
- broad_coverage: Union 2018 (AUTO-POOL;EL-UNION18-ALLOWANCE)
- stage3_coverage: Unity 2021 (EL-UNITY21-S3)

## Going concern

- Full original-year auditor reports reviewed and recorded: 45 (3 coded 1).
- Bank-years explicitly listed as not reviewed: 15.
- Panel rows coded: 46 (3 coded 1); unknown: 51. Unknown is not zero.
- Of the coded rows: 2 baseline codes retained (1 confirmed by this review), 9 filled in baseline rows, 35 on additional rows.
- A zero means no material-uncertainty section or going-concern emphasis was found after the recorded review; it does not certify survival.
- With 3 positive event(s), a multivariable going-concern model is not supported; report event counts before choosing an estimator.

## Version decisions and conflicts

- Version classifications: confirmed scope difference with 2022 selected basis 1, corroborated by original-year report 1, corroborated by original-year summary 1, fallback: comparative 4, fallback: labelled restatement 3, labelled reclassification 1, labelled restatement 3, source internal inconsistency 4, unexplained difference 4 (`data/review/version_decisions.csv`).
- Conflicts recorded: candidate_vs_selected 199, restated_comparative 4, source_internal_inconsistency 3, source_internal_inconsistency_cross_report 1, source_unit_label_error 1, source_vs_selected 1.

## Reporting versions (`data/row_versions.csv`)

- primary (baseline selection retained): 47
- primary (original-year presentation): 43
- primary; drop in sensitivity (fallback: original-year report unavailable): 7
- Fallback rows (primary, dropped in sensitivity): Access 2018 (fallback: comparative; source xs-6951b12082; labelled restated: no); Fidelity 2021 (fallback: labelled restatement; source pdf-0960512f5d; labelled restated: yes); GTBank 2017 (fallback: labelled restatement; source xs-21e7fbfbf9; labelled restated: yes); Union 2015 (fallback: labelled restatement; source xs-15d472ad0d; labelled restated: yes); Unity 2013 (fallback: comparative; source xs-901cfd21b1; labelled restated: no); Unity 2020 (fallback: comparative; source xs-848eb8a062; labelled restated: no); Wema 2021 (fallback: comparative; source pdf-2b23016b97; labelled restated: no).
- Unreconciled version mixes: 0.

## Unresolved exceptions

- Fidelity 2016 reported CAR vs capital/RWA: documented source exception
- Wema 2021 reported CAR vs capital/RWA: documented source exception
- Stanbic 2021 regulatory_capital: unexplained difference
- Wema 2021 total_impairment: confirmed scope difference with 2022 selected basis
- Stanbic 2020 regulatory_capital: source internal inconsistency
- Stanbic 2020 capital_transitional: source internal inconsistency
- Wema 2021 car: source internal inconsistency
- Fidelity 2016 car: source internal inconsistency
- Sterling 2016 assets/equity/pat: unexplained difference
- First Bank 2016 pbt: unexplained difference; OWNER DECISION PENDING
- Stanbic 2020 total_impairment: unexplained difference; OWNER DECISION PENDING
- Unity 2021 stage3_gross: source_internal_inconsistency_cross_report

## Model readiness (`outputs/readiness/readiness.md`; no thesis regressions run)

- O1 Effect of IFRS 9 adoption on loan-loss provisioning: testable (testable: allr;impairment_assets)
- O2 Effect of IFRS 9 adoption on capital adequacy: testable (testable: car;car_computed)
- O3 Effect of IFRS 9 adoption on profitability, cash generation and balance-sheet stability: testable (testable: roa;ocf_ratio;eqta;leverage)
- O4 Going-concern indicators before and after IFRS 9: descriptive only (testable: none)
- O5 Tier 1 versus Tier 2 differences in the IFRS 9 effect: testable (testable: allr;car;roa;eqta)
- O6 Change in volatility of key indicators after IFRS 9: exploratory test only (bank-level SDs from >=3 observations per regime) (testable: roa;car;allr;impairment_assets)
- IFRS9_D is perfectly collinear with a full set of year fixed effects.

## Remaining

- Bank-year positions not admitted: 33; field requests in selected rows outstanding: 345.
  - Access: 2022
  - Ecobank Nigeria: 2013, 2014, 2015, 2018, 2019, 2020, 2021, 2022
  - FCMB: 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022
  - First Bank: 2018, 2019, 2020, 2021, 2022
  - GTBank: 2015, 2016, 2021, 2022
  - Stanbic: 2013, 2014, 2015, 2016, 2017

## Tests

- synthetic/mock unit tests: 62 passed, 0 failed, 0 skipped.
- real-data regression tests: 30 passed, 0 failed, 0 skipped.
- Test run: 2026-10-10T21:47:02+00:00.

## Nimble usage

- REST client attempted requests: 0 (cap 100, unchanged).
- Plugin invocations: 48 (nimble_search 36, nimble_agents_list 1, nimble_agents_run 1, nimble_agents_run_status 9, nimble_agents_run_result 1). Provider-billed requests: not available.

## Workbook and handoff

- Formula audit after LibreOffice recalculation: {'cells_checked': 1649, 'numeric_differences': 0, 'mismatches': 0, 'excel_errors': 0}.
- Handoff zip: 381 files; rendered evidence page images included: 263; admission image paths without an included image: 0.
- Source PDFs are NOT included (73 files); each is listed with URL and SHA-256 in `reports/index.csv`. Manual and image-only transcriptions cannot be reproduced from a hash alone: re-inspect the cited page.

## Not done

- No regression, hypothesis test or volatility estimate was run, and the thesis was not updated.
- No candidate (unverified) amount was promoted to the panel.
- Going-concern codes remain unknown for 51 panel rows.
