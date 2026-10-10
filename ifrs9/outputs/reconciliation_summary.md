# Reconciliation summary

Generated 2026-10-10T21:27:57+00:00 from the saved outputs (commit `5a209c1ca855`).
Every number below is computed by `ifrs9_recovery.summary.release_stats()`; see `outputs/release_stats.json`.

## Panel

- Selected bank-years: **73** across 12 banks (37 pre-adoption, 36 post-adoption).
- Baseline rows: 47 (all 47 retained); additional rows admitted: 26.
- These are selected rows, not complete observations for every endpoint (see endpoint table).

## What changed relative to the frozen baseline

- Raw input files: unchanged (SHA-256 checked by `inventory`).
- Non-blank baseline measurements changed: 0 (corrections are the only route).
- Authorised fills of blank baseline cells: 9 (gcu 9).
- Recomputed derived values that differ from stored: 0.
- Additional bank-years: 26.
- Field basis of all non-blank cells: baseline_inherited 615, derived_from_verified 13, derived_from_verified+restated_comparative 4, manual_transcription 51, manual_transcription+restated_comparative 4, recomputed_ratio 759, reported_text_layer 312, reported_text_layer+restated_comparative 37.

## Admission and reconciliation

- Admissions: 442 accepted, 0 rejected (file hash recomputed, page and rendered image re-verified, structured scope, explicit sign transform, derived values recomputed).
- Reconciliation checks run: 154; pass 152; fail 0; documented source exception 2.
- Evidence lineage: 1036 of 1036 non-blank inputs matched to an evidence record; 6 carry an explicit qualification.
- Average-asset denominators: 52 checked against prior-year closing assets; 1 differ (listed in `data/denominator_compatibility.csv`). Each ratio uses the opening balance from the same report as its closing balance; differing pairs are not smoothed.
  - Union 2015 (opening 922755.0 from 2016 annual report; 2015 restated comparative; prior closing 920936.0 from Prior source-selection policy retained; original evidence preserved in accompanying pack.)

## Endpoint coverage (selected rows)

| Outcome | Available | Eligible | Excluded by flag | Pre | Post |
|---|---|---|---|---|---|
| roa | 56 | 56 | 0 | 27 | 29 |
| eqta | 73 | 73 | 0 | 37 | 36 |
| ocf_ratio | 50 | 50 | 0 | 24 | 26 |
| allr | 61 | 61 | 0 | 29 | 32 |
| leverage | 73 | 73 | 0 | 37 | 36 |
| car | 58 | 56 | 2 | 27 | 29 |
| car_computed | 39 | 38 | 1 | 14 | 24 |
| npl_calc | 14 | 14 | 0 | 7 | 7 |
| broad_coverage | 14 | 14 | 0 | 7 | 7 |
| stage3_coverage | 4 | 4 | 0 | 0 | 4 |
| impairment_assets | 53 | 53 | 0 | 24 | 29 |
| liquidity_used | 10 | 10 | 0 | 5 | 5 |
| gcu | 26 | 26 | 0 | 7 | 19 |

## Going concern

- Full original-year auditor reports reviewed and recorded: 25 (1 coded 1).
- Bank-years explicitly listed as not reviewed: 11.
- Panel rows coded: 26 (1 coded 1); unknown: 47. Unknown is not zero.
- Of the coded rows: 2 baseline codes retained (1 confirmed by this review), 9 filled in baseline rows, 15 on additional rows.
- A zero means no material-uncertainty section or going-concern emphasis was found after the recorded review; it does not certify survival.
- With 1 positive event(s), a multivariable going-concern model is not supported; report event counts before choosing an estimator.

## Version decisions and conflicts

- Version classifications: fallback: comparative 1, fallback: labelled restatement 3, labelled reclassification 1, labelled restatement 2, possible scope incompatibility with 2022 1, source internal inconsistency 4, unexplained difference 1 (`data/review/version_decisions.csv`).
- Conflicts recorded: candidate_vs_selected 141, restated_comparative 4, source_internal_inconsistency 3, source_unit_label_error 1, source_vs_selected 1.

## Remaining

- Bank-year positions not admitted: 57; field requests in selected rows outstanding: 345.

## Tests

- synthetic/mock unit tests: 62 passed, 0 failed, 0 skipped.
- real-data regression tests: 27 passed, 0 failed, 0 skipped.
- Test run: 2026-10-10T21:27:53+00:00.

## Nimble usage

- REST client attempted requests: 0 (cap 100, unchanged).
- Plugin invocations: 23 (nimble_agents_list 1, nimble_agents_run 1, nimble_agents_run_status 7, nimble_search 14). Provider-billed requests: not available.

## Workbook and handoff

- Formula audit after LibreOffice recalculation: {'cells_checked': 1241, 'numeric_differences': 0, 'mismatches': 0, 'excel_errors': 0}.
- Handoff zip: 215 files; rendered evidence page images included: 126; admission image paths without an included image: 0.
- Source PDFs are NOT included (48 files); each is listed with URL and SHA-256 in `reports/index.csv`. Manual and image-only transcriptions cannot be reproduced from a hash alone: re-inspect the cited page.

## Not done

- No regression, hypothesis test or volatility estimate was run, and the thesis was not updated.
- No candidate (unverified) amount was promoted to the panel.
- Going-concern codes remain unknown for 47 panel rows.
