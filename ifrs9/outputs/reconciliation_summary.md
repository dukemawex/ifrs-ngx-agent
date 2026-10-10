# Reconciliation summary

Generated 2026-10-10T21:42:03+00:00 from the saved outputs (commit `1b5ce89c0114`).
Every number below is computed by `ifrs9_recovery.summary.release_stats()`; see `outputs/release_stats.json`.

## Panel

- Selected bank-years: **87** across 12 banks (45 pre-adoption, 42 post-adoption).
- Baseline rows: 47 (all 47 retained); additional rows admitted: 40.
- These are selected rows, not complete observations for every endpoint (see endpoint table).

## What changed relative to the frozen baseline

- Raw input files: unchanged (SHA-256 checked by `inventory`).
- Non-blank baseline measurements changed: 0 (corrections are the only route).
- Authorised fills of blank baseline cells: 9 (gcu 9).
- Recomputed derived values that differ from stored: 0.
- Additional bank-years: 40.
- Field basis of all non-blank cells: baseline_inherited 615, derived_from_verified 15, derived_from_verified+restated_comparative 4, manual_transcription 77, manual_transcription+restated_comparative 4, recomputed_ratio 924, reported_text_layer 507, reported_text_layer+restated_comparative 37.

## Admission and reconciliation

- Admissions: 667 accepted, 0 rejected (file hash recomputed, page and rendered image re-verified, structured scope, explicit sign transform, derived values recomputed).
- Reconciliation checks run: 192; pass 190; fail 0; documented source exception 2.
- Evidence lineage: 1259 of 1259 non-blank inputs matched to an evidence record; 6 carry an explicit qualification.
- Average-asset denominators: 62 checked against prior-year closing assets; 2 differ (listed in `data/denominator_compatibility.csv`). Each ratio uses the opening balance from the same report as its closing balance; differing pairs are not smoothed.
  - Access 2020 (opening 6307588.216 from 2020 annual report, as originally reported; prior closing 6311041.282 from 2019 annual report, as originally reported)
  - Union 2015 (opening 922755.0 from 2016 annual report; 2015 restated comparative; prior closing 920936.0 from Prior source-selection policy retained; original evidence preserved in accompanying pack.)

## Endpoint coverage (selected rows)

| Outcome | Available | Eligible | Excluded by flag | Pre | Post |
|---|---|---|---|---|---|
| roa | 70 | 70 | 0 | 35 | 35 |
| eqta | 87 | 87 | 0 | 45 | 42 |
| ocf_ratio | 64 | 64 | 0 | 32 | 32 |
| allr | 74 | 74 | 0 | 36 | 38 |
| leverage | 87 | 87 | 0 | 45 | 42 |
| car | 69 | 67 | 2 | 33 | 34 |
| car_computed | 50 | 49 | 1 | 20 | 29 |
| npl_calc | 14 | 14 | 0 | 7 | 7 |
| broad_coverage | 14 | 14 | 0 | 7 | 7 |
| stage3_coverage | 5 | 5 | 0 | 0 | 5 |
| impairment_assets | 67 | 67 | 0 | 32 | 35 |
| liquidity_used | 10 | 10 | 0 | 5 | 5 |
| gcu | 39 | 39 | 0 | 14 | 25 |

## Going concern

- Full original-year auditor reports reviewed and recorded: 38 (2 coded 1).
- Bank-years explicitly listed as not reviewed: 12.
- Panel rows coded: 39 (2 coded 1); unknown: 48. Unknown is not zero.
- Of the coded rows: 2 baseline codes retained (1 confirmed by this review), 9 filled in baseline rows, 28 on additional rows.
- A zero means no material-uncertainty section or going-concern emphasis was found after the recorded review; it does not certify survival.
- With 2 positive event(s), a multivariable going-concern model is not supported; report event counts before choosing an estimator.

## Version decisions and conflicts

- Version classifications: fallback: comparative 1, fallback: labelled restatement 3, labelled reclassification 1, labelled restatement 2, possible scope incompatibility with 2022 1, source internal inconsistency 4, unexplained difference 1 (`data/review/version_decisions.csv`).
- Conflicts recorded: candidate_vs_selected 179, restated_comparative 4, source_internal_inconsistency 3, source_unit_label_error 1, source_vs_selected 1.

## Remaining

- Bank-year positions not admitted: 43; field requests in selected rows outstanding: 345.

## Tests

- synthetic/mock unit tests: 62 passed, 0 failed, 0 skipped.
- real-data regression tests: 30 passed, 0 failed, 0 skipped.
- Test run: 2026-10-10T21:41:58+00:00.

## Nimble usage

- REST client attempted requests: 0 (cap 100, unchanged).
- Plugin invocations: 23 (nimble_agents_list 1, nimble_agents_run 1, nimble_agents_run_status 7, nimble_search 14). Provider-billed requests: not available.

## Workbook and handoff

- Formula audit after LibreOffice recalculation: {'cells_checked': 1479, 'numeric_differences': 0, 'mismatches': 0, 'excel_errors': 0}.
- Handoff zip: 300 files; rendered evidence page images included: 211; admission image paths without an included image: 0.
- Source PDFs are NOT included (64 files); each is listed with URL and SHA-256 in `reports/index.csv`. Manual and image-only transcriptions cannot be reproduced from a hash alone: re-inspect the cited page.

## Not done

- No regression, hypothesis test or volatility estimate was run, and the thesis was not updated.
- No candidate (unverified) amount was promoted to the panel.
- Going-concern codes remain unknown for 48 panel rows.
