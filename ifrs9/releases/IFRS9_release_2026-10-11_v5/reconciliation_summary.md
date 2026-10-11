# Reconciliation summary

Generated 2026-10-11T12:47:13+00:00 from the saved outputs (code commit `08ee95fbe8ed059dc205056133f4058709aca764`, branch `claude/zen-hamilton-v2s80b`).
Every number below is computed by `ifrs9_recovery.summary.release_stats()`; see `outputs/release_stats.json`.

## Panel

- Selected bank-years: **118** across 12 banks (60 pre-adoption, 58 post-adoption).
- Baseline rows: 47 (all 47 retained); additional rows admitted: 71.
- These are selected rows, not complete observations for every endpoint (see endpoint table).

## What changed relative to the frozen baseline

- Raw input files: unchanged (SHA-256 checked by `inventory`).
- Non-blank baseline measurements changed: 0 (corrections are the only route).
- Authorised fills of blank baseline cells: 9 (gcu 9).
- Recomputed derived values that differ from stored: 0.
- Additional bank-years: 71.
- Field basis of all non-blank cells: baseline_inherited 615, derived_from_verified 28, derived_from_verified+restated_comparative 5, manual_transcription 139, manual_transcription+restated_comparative 6, recomputed_ratio 1254, reported_text_layer 838, reported_text_layer+restated_comparative 48.

## Admission and reconciliation

- Admissions: 1135 accepted, 0 rejected (file hash recomputed, page and rendered image re-verified, structured scope, explicit sign transform, derived values recomputed).
- Reconciliation checks run: 264; pass 262; fail 0; documented source exception 2.
- Evidence lineage: 1679 of 1679 non-blank inputs matched to an evidence record; 6 carry an explicit qualification.
- Average-asset denominators: 92 checked against prior-year closing assets; 8 differ (listed in `data/denominator_compatibility.csv`). Each ratio uses the opening balance from the same report as its closing balance; differing pairs are not smoothed.
  - Access 2020 (opening 6307588.216 from 2020 annual report, as originally reported; prior closing 6311041.282 from 2019 annual report, as originally reported)
  - Ecobank Nigeria 2019 (opening 1927889.0 from 2019 annual report, as originally reported; prior closing 1956830.0 from 2018 annual report, as originally reported)
  - Ecobank Nigeria 2021 (opening 2186711.0 from 2021 annual report, as originally reported; prior closing 2186712.0 from 2020 annual report, as originally reported)
  - Stanbic 2015 (opening 908429.0 from Stanbic IBTC Holdings 2015 annual report: audited HoldCo package - explicit operating-bank subsidiary disclosure (note 13.4, Stanbic IBTC Bank PLC); prior closing 911052.0 from Stanbic IBTC Holdings 2014 annual report: audited HoldCo package - explicit operating-bank subsidiary disclosure (note 13.4, Stanbic IBTC Bank PLC))
  - Stanbic 2018 (opening 1332723.0 from 2018 audited financial statements, as originally reported (issuer-hosted scanned extract); prior closing 1332669.0 from Stanbic IBTC Holdings 2017 annual report: audited HoldCo package - explicit operating-bank subsidiary disclosure (note 13.4, Stanbic IBTC Bank PLC))
  - Sterling 2017 (opening 830805.0 from 2017 annual report, as originally reported; prior closing 830802.224 from 2016 annual report, as originally reported)
  - Sterling 2022 (opening 1606898.0 from 2022 annual report, as originally reported; prior closing 1611749.0 from 2021 annual report, as originally reported)
  - Union 2015 (opening 922755.0 from 2016 annual report; 2015 restated comparative; prior closing 920936.0 from Prior source-selection policy retained; original evidence preserved in accompanying pack.)

## Outcome eligibility (one ruleset: `ifrs9_recovery.eligibility`, `data/outcome_eligibility.csv`)

Available = value present; descriptive/longitudinal/inferential uses are distinct; change pairs = year-on-year changes that are comparable; fallback rows stay in the primary sample but are dropped in sensitivity runs.

| Outcome | Available | Descriptive | Longitudinal | Change pairs | Eligible (inferential) | Excluded from inference | Banks | Pre | Post | Tier 1 | Tier 2 | Fallback rows |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| gcu | 58 | 58 | 58 | 30 | 58 | 0 | 11 | 23 | 35 | 17 | 41 | 0 |
| car | 89 | 89 | 89 | 67 | 86 | 3 | 12 | 41 | 45 | 35 | 51 | 2 |
| car_computed | 70 | 70 | 70 | 48 | 67 | 3 | 12 | 28 | 39 | 30 | 37 | 2 |
| roa | 97 | 97 | 97 | 70 | 97 | 0 | 12 | 49 | 48 | 39 | 58 | 3 |
| eqta | 118 | 118 | 118 | 101 | 118 | 0 | 12 | 60 | 58 | 48 | 70 | 8 |
| ocf_ratio | 86 | 86 | 86 | 60 | 86 | 0 | 12 | 41 | 45 | 37 | 49 | 3 |
| allr | 95 | 95 | 94 | 72 | 93 | 2 | 12 | 45 | 48 | 39 | 54 | 5 |
| impairment_assets | 92 | 92 | 90 | 64 | 90 | 2 | 12 | 45 | 45 | 35 | 55 | 2 |
| npl_calc | 19 | 19 | 19 | 13 | 19 | 0 | 4 | 7 | 12 | 6 | 13 | 1 |
| broad_coverage | 19 | 19 | 18 | 11 | 18 | 1 | 4 | 7 | 11 | 6 | 12 | 1 |
| stage3_coverage | 6 | 6 | 5 | 3 | 5 | 1 | 2 | 0 | 5 | 0 | 5 | 0 |
| liquidity | 10 | 10 | 10 | 7 | 10 | 0 | 3 | 5 | 5 | 7 | 3 | 0 |
| leverage | 118 | 118 | 118 | 101 | 118 | 0 | 12 | 60 | 58 | 48 | 70 | 8 |

Rows excluded from inference (rule ids in `data/outcome_eligibility.csv`, reasons in `data/review/eligibility_rules.csv`):

- car: Fidelity 2016 (AUTO-FLAG;EL-FID16-CAR); GTBank 2015 (AUTO-FLAG); Wema 2021 (AUTO-FALLBACK;AUTO-FLAG;EL-WEMA21-CAR)
- car_computed: Fidelity 2016 (EL-FID16-CAR); Stanbic 2020 (AUTO-FLAG;EL-STAN20-CAPITAL); Wema 2021 (AUTO-FALLBACK;EL-WEMA21-CAR)
- allr: First Bank 2018 (AUTO-FLAG); Union 2018 (AUTO-POOL;EL-UNION18-ALLOWANCE)
- impairment_assets: Unity 2017 (EL-UNITY17-IMP); Wema 2021 (AUTO-FALLBACK;EL-WEMA21-IMP)
- broad_coverage: Union 2018 (AUTO-POOL;EL-UNION18-ALLOWANCE)
- stage3_coverage: Unity 2021 (EL-UNITY21-S3)

## Going concern

- Full original-year auditor reports reviewed and recorded: 57 (3 coded 1); partially available reports (left uncoded): 1; HoldCo-derived bank-years with no opinion on the operating bank (left uncoded): 8.
- Bank-years explicitly listed as not reviewed: 24.
- Panel rows coded: 58 (3 coded 1); unknown: 60. Unknown is not zero.
- Of the coded rows: 2 baseline codes retained (1 confirmed by this review), 9 filled in baseline rows, 47 on additional rows.
- A zero means no material-uncertainty section or going-concern emphasis was found after the recorded review; it does not certify survival.
- With 3 positive event(s), a multivariable going-concern model is not supported; report event counts before choosing an estimator.

## Version decisions and conflicts

- Version classifications: confirmed scope difference with 2022 selected basis 1, corroborated by original-year net loans + allowance (field-level comparative) 1, corroborated by original-year report 1, corroborated by original-year summary 1, fallback: comparative 4, fallback: labelled restatement 3, fallback: unlabelled comparative 1, labelled reclassification 2, labelled restatement 5, source internal inconsistency 4, unexplained difference 8 (`data/review/version_decisions.csv`).
- Conflicts recorded: candidate_vs_selected 283, later_comparative 3, restated_comparative 6, source_internal_inconsistency 5, source_internal_inconsistency_cross_report 1, source_unit_label_error 1, source_vs_selected 1.

## Reporting versions (`data/row_versions.csv`)

- primary (baseline selection retained): 47
- primary (original-year presentation): 63
- primary; drop in sensitivity (fallback: original-year report unavailable): 8
- Fallback rows (primary, dropped in sensitivity): Access 2018 (fallback: comparative; source xs-6951b12082; labelled restated: no); Fidelity 2021 (fallback: labelled restatement; source pdf-0960512f5d; labelled restated: yes); First Bank 2022 (fallback: unlabelled comparative; source xs-8f94f07a8d; labelled restated: no); GTBank 2017 (fallback: labelled restatement; source xs-21e7fbfbf9; labelled restated: yes); Union 2015 (fallback: labelled restatement; source xs-15d472ad0d; labelled restated: yes); Unity 2013 (fallback: comparative; source xs-901cfd21b1; labelled restated: no); Unity 2020 (fallback: comparative; source xs-848eb8a062; labelled restated: no); Wema 2021 (fallback: comparative; source pdf-2b23016b97; labelled restated: no).
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
- Ecobank Nigeria 2020 regulatory_capital / rwa / car: unexplained difference
- Ecobank Nigeria 2020 ocf: unexplained difference
- Stanbic 2014 pat / assets: unexplained difference
- First Bank 2018 ocf: unexplained difference
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

- Bank-year positions not admitted: 12; field requests in selected rows outstanding: 345.
  - FCMB: 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022
  - First Bank: 2020, 2021

## Tests

- synthetic/mock unit tests: 62 passed, 0 failed, 0 skipped.
- real-data regression tests: 44 passed, 0 failed, 0 skipped.
- Test run: 2026-10-11T12:46:46+00:00.

## Nimble usage

- REST client attempted requests: 0 (cap 100, unchanged).
- Plugin invocations: 65 (nimble_search 53, nimble_agents_list 1, nimble_agents_run 1, nimble_agents_run_status 9, nimble_agents_run_result 1). Provider-billed requests: not available.

## Workbook and handoff

- Formula audit after LibreOffice recalculation: {'cells_checked': 2006, 'numeric_differences': 0, 'mismatches': 0, 'excel_errors': 0}.
- Handoff zip: 486 files; rendered evidence page images included: 363; admission image paths without an included image: 0.
- Source PDFs are NOT included (103 files); each is listed with URL and SHA-256 in `reports/index.csv`. Manual and image-only transcriptions cannot be reproduced from a hash alone: re-inspect the cited page.

## Not done

- No regression, hypothesis test or volatility estimate was run, and the thesis was not updated.
- No candidate (unverified) amount was promoted to the panel.
- Going-concern codes remain unknown for 60 panel rows.
