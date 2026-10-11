# Thesis analysis report (generated)

Generated 2026-10-11T06:48:33+00:00 by `python -m thesis_analysis` at code commit `e51e4d0c6150f96a9da657f9cdc7a7ebb8911cdb`.
Input: frozen release `IFRS9_release_2026-10-11_v1` (42 files hash-verified against RELEASE_MANIFEST.json; release code commit `8d503d9a124b21e235c9c922fe7425f994cc2e75`).
Every number below is read back from the exported file named in brackets. No thesis prose; no data were changed.

## 1. Sample

- Cohort: 12 banks (5 Tier 1 / 7 Tier 2); FCMB formally excluded and not replaced [tables/table1_sample_coverage.csv].
- Selected bank-years: 97 of 120 positions (50 pre-IFRS 9, 47 post) [tables/table1_sample_coverage.csv].
- Eligible N by outcome [tables/table2_variables_eligible_n.csv]:

  - Allowance / gross loans: 81 (pre 40, post 41; Tier 1 35, Tier 2 46; 11 banks; excluded 1; role: inferential models)
  - Impairment / average assets: 72 (pre 35, post 37; Tier 1 30, Tier 2 42; 12 banks; excluded 2; role: inferential models)
  - CAR: 74 (pre 37, post 37; Tier 1 31, Tier 2 43; 11 banks; excluded 2; role: inferential models)
  - ROA: 77 (pre 39, post 38; Tier 1 32, Tier 2 45; 12 banks; excluded 0; role: inferential models)
  - OCF / average assets: 71 (pre 36, post 35; Tier 1 30, Tier 2 41; 11 banks; excluded 0; role: inferential models)
  - Equity / assets: 97 (pre 50, post 47; Tier 1 40, Tier 2 57; 12 banks; excluded 0; role: inferential models)
  - Leverage: 97 (pre 50, post 47; Tier 1 40, Tier 2 57; 12 banks; excluded 0; role: inferential models)
  - NPL ratio: 14 (pre 7, post 7; Tier 1 6, Tier 2 8; 3 banks; excluded 0; role: descriptive only (too sparse))
  - Broad NPL coverage: 13 (pre 7, post 6; Tier 1 6, Tier 2 7; 3 banks; excluded 1; role: descriptive only (too sparse))
  - Stage 3 coverage: 5 (pre 0, post 5; Tier 1 0, Tier 2 5; 2 banks; excluded 1; role: descriptive only (too sparse))
  - Liquidity ratio: 10 (pre 5, post 5; Tier 1 7, Tier 2 3; 3 banks; excluded 0; role: descriptive only (too sparse))
  - Going-concern uncertainty: 46 (pre 18, post 28; Tier 1 13, Tier 2 33; 10 banks; excluded 0; role: event description only)

## 2. Principal results (bank fixed effects, M1: y ~ IFRS9_D) [regression_results.csv]

| Outcome | Coef (pp) | CR1 SE | p conventional | p CR1 t(G-1) | p WCB | N | Banks |
|---|---|---|---|---|---|---|---|
| Allowance / gross loans | -0.874 | 1.880 | 0.326 | 0.652 | 0.889 | 81 | 11 |
| Impairment / average assets | -0.913 | 0.566 | 0.001 | 0.135 | 0.070 | 72 | 12 |
| CAR | -2.816 | 2.307 | 0.596 | 0.250 | 0.213 | 74 | 11 |
| ROA | -0.033 | 0.156 | 0.871 | 0.835 | 0.837 | 77 | 12 |
| OCF / average assets | 7.336 | 1.839 | 0.000 | 0.003 | 0.017 | 71 | 11 |
| Equity / assets | -10.685 | 6.435 | 0.019 | 0.125 | 0.013 | 97 | 12 |
| Leverage | 10.685 | 6.435 | 0.019 | 0.125 | 0.013 | 97 | 12 |

## 3. Tier 1 vs Tier 2 (M4: bank + year FE, Tier1 x IFRS9_D) [regression_results.csv]

| Outcome | Coef (pp) | CR1 SE | p CR1 | p WCB | N |
|---|---|---|---|---|---|
| Allowance / gross loans | 4.832 | 2.869 | 0.123 | 0.110 | 81 |
| Impairment / average assets | 1.081 | 0.915 | 0.262 | 0.286 | 72 |
| CAR | 5.576 | 4.807 | 0.273 | 0.304 | 74 |
| ROA | -0.433 | 0.277 | 0.146 | 0.160 | 77 |
| OCF / average assets | 4.084 | 3.579 | 0.281 | 0.284 | 71 |
| Equity / assets | 13.059 | 10.922 | 0.257 | 0.284 | 97 |
| Leverage | -13.059 | 10.922 | 0.257 | 0.284 | 97 |

## 4. Robustness of M1 (IFRS9_D) [robustness_results.csv, jackknife_results.csv]

| Outcome | S0 | S1 | S2 | S3 | S4 | S5 | Jackknife min | Jackknife max | Sign changes |
|---|---|---|---|---|---|---|---|---|---|
| Allowance / gross loans | -0.87 (p=0.889) | -0.91 (p=0.865) | -0.77 (p=0.926) | 0.93 (p=0.197) | -0.97 (p=0.872) | 0.93 (p=0.198) | -1.46 | 0.93 | 1 |
| Impairment / average assets | -0.91 (p=0.070) | -0.95 (p=0.078) | -1.17 (p=0.072) | -0.39 (p=0.139) | -1.06 (p=0.055) | -0.39 (p=0.137) | -1.12 | -0.39 | 0 |
| CAR | -2.82 (p=0.213) | -2.90 (p=0.230) | -2.78 (p=0.210) | -0.70 (p=0.415) | -3.08 (p=0.240) | -0.70 (p=0.415) | -3.68 | -0.70 | 0 |
| ROA | -0.03 (p=0.837) | -0.01 (p=0.962) | n/a | -0.13 (p=0.384) | 0.04 (p=0.837) | -0.13 (p=0.386) | -0.13 | 0.07 | 3 |
| OCF / average assets | 7.34 (p=0.017) | 8.44 (p=0.013) | n/a | 8.86 (p=0.008) | 8.14 (p=0.022) | 8.86 (p=0.007) | 6.52 | 8.86 | 0 |
| Equity / assets | -10.68 (p=0.013) | -9.68 (p=0.013) | n/a | -4.17 (p=0.008) | -11.37 (p=0.015) | -4.17 (p=0.009) | -12.00 | -4.17 | 0 |
| Leverage | 10.68 (p=0.013) | 9.68 (p=0.013) | n/a | 4.17 (p=0.008) | 11.37 (p=0.015) | 4.17 (p=0.009) | 4.17 | 12.00 | 0 |

S0 primary; S1 drop fallback rows; S2 add exception rows (n/a where none); S3 drop Unity negative-capital rows; S4 drop 2020; S5 drop Unity. p = WCB.

## 5. Matched pre/post (bank means, banks in both regimes) [matched_prepost_summary.csv]

- Allowance / gross loans: 9 banks; mean difference -0.911 pp, median 0.877; 6 up / 3 down; Wilcoxon p = 0.496.
- Impairment / average assets: 9 banks; mean difference -0.977 pp, median -0.350; 1 up / 8 down; Wilcoxon p = 0.074.
- CAR: 8 banks; mean difference -3.881 pp, median -1.243; 2 up / 6 down; Wilcoxon p = 0.195.
- ROA: 9 banks; mean difference -0.002 pp, median 0.048; 5 up / 4 down; Wilcoxon p = 0.910.
- OCF / average assets: 9 banks; mean difference 6.332 pp, median 9.048; 7 up / 2 down; Wilcoxon p = 0.020.
- Equity / assets: 9 banks; mean difference -10.128 pp, median -4.707; 1 up / 8 down; Wilcoxon p = 0.008.
- Leverage: 9 banks; mean difference 10.128 pp, median 4.707; 8 up / 1 down; Wilcoxon p = 0.008.

## 6. Volatility (EXPLORATORY) [volatility_results_summary.csv]

- Allowance / gross loans: 8 banks; median SD pre 0.913, post 0.735, median ratio 1.19; 5 higher / 3 lower; Wilcoxon p = 0.844.
- Impairment / average assets: 8 banks; median SD pre 0.480, post 0.160, median ratio 0.34; 1 higher / 7 lower; Wilcoxon p = 0.039.
- CAR: 6 banks; median SD pre 2.745, post 1.812, median ratio 0.74; 1 higher / 5 lower; Wilcoxon p = 0.062.
- ROA: 8 banks; median SD pre 0.290, post 0.246, median ratio 0.60; 3 higher / 5 lower; Wilcoxon p = 0.383.
- OCF / average assets: 7 banks; median SD pre 5.819, post 6.391, median ratio 1.40; 4 higher / 3 lower; Wilcoxon p = 0.578.
- Equity / assets: 9 banks; median SD pre 1.006, post 1.205, median ratio 1.39; 5 higher / 4 lower; Wilcoxon p = 0.359.
- Leverage: 9 banks; median SD pre 1.006, post 1.205, median ratio 1.39; 5 higher / 4 lower; Wilcoxon p = 0.359.

## 7. Going concern (descriptive only) [going_concern_events.csv, going_concern_coverage.csv]

- Unity 2019 (Tier 2): auditor KPMG Professional Services, report 2020-05-20; CAR -201.59% (other banks' median 17.95%), equity/assets -95.16% (other banks 11.07%), ROA 1.34%.
- Unity 2021 (Tier 2): auditor KPMG Professional Services (Chartered Accountants), Lagos, report 6 May, 2022; CAR -86.18% (other banks' median 17.62%), equity/assets -51.25% (other banks 9.01%), ROA 0.62%.
- Unity 2022 (Tier 2): auditor KPMG Professional Services (Chartered Accountants), Lagos, Nigeria, report 25 May 2023; CAR -89.69% (other banks' median 18.14%), equity/assets -53.90% (other banks 8.34%), ROA 0.18%.
- Coded bank-years 46, events 3; pre-IFRS 9 events 0, post 3; descriptive Fisher exact p = 0.270. No logistic/probit model estimated.

## 8. Diagnostics [model_diagnostics.csv]

- Allowance / gross loans: within share of variance 0.79; max Cook's D 0.67 (Unity 2016); 2 obs > 4/N; JB p 0.000; BP p 0.156; Wooldridge AR(1) p 0.000.
- Impairment / average assets: within share of variance 0.63; max Cook's D 0.33 (Unity 2016); 4 obs > 4/N; JB p 0.000; BP p 0.637; Wooldridge AR(1) p 0.005.
- CAR: within share of variance 0.17; max Cook's D 0.67 (Unity 2016); 5 obs > 4/N; JB p 0.000; BP p 0.563; Wooldridge AR(1) p 0.000.
- ROA: within share of variance 0.27; max Cook's D 0.44 (Unity 2017); 2 obs > 4/N; JB p 0.000; BP p 0.264; Wooldridge AR(1) p 0.066.
- OCF / average assets: within share of variance 0.78; max Cook's D 0.08 (Access 2019); 5 obs > 4/N; JB p 0.497; BP p 0.852; Wooldridge AR(1) p 0.507.
- Equity / assets: within share of variance 0.53; max Cook's D 0.41 (Unity 2017); 7 obs > 4/N; JB p 0.000; BP p 0.215; Wooldridge AR(1) p 0.000.
- Leverage: within share of variance 0.53; max Cook's D 0.41 (Unity 2017); 7 obs > 4/N; JB p 0.000; BP p 0.215; Wooldridge AR(1) p 0.000.
- Adding ln(total assets) (M2): VIF of IFRS9_D 2.15-2.59; max Cook's D rises to 2.01 (Unity 2017), which is why M1 is principal.

## 9. Objective-level interpretation [interpretation.csv]

| Obj | Outcome | Sample | Coef (pp) | p WCB | Decision | Robustness |
|---|---|---|---|---|---|---|
| O1 | Allowance / gross loans | N = 81 bank-years, 11 banks (40 pre / 41 post) | -0.874 | 0.889 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 3/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 1 |
| O1 | Impairment / average assets | N = 72 bank-years, 12 banks (35 pre / 37 post) | -0.913 | 0.070 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 5/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 0 |
| O2 | CAR | N = 74 bank-years, 11 banks (37 pre / 37 post) | -2.816 | 0.213 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 5/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 0 |
| O3 | ROA | N = 77 bank-years, 12 banks (39 pre / 38 post) | -0.033 | 0.837 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 3/4 sensitivities, WCB p < 0.05 in 0/4 (none); jackknife sign changes 3 |
| O3 | OCF / average assets | N = 71 bank-years, 11 banks (36 pre / 35 post) | 7.336 | 0.017 | H0 rejected at 5% (WCB) | robust: same sign in 4/4 sensitivities, WCB p < 0.05 in 4/4, jackknife sign changes 0 |
| O3 | Equity / assets | N = 97 bank-years, 12 banks (50 pre / 47 post) | -10.685 | 0.013 | H0 rejected at 5% (WCB); CR1 t(G-1) p = 0.125 gives the opposite decision | robust: same sign in 4/4 sensitivities, WCB p < 0.05 in 4/4, jackknife sign changes 0 |
| O3 | Leverage | N = 97 bank-years, 12 banks (50 pre / 47 post) | 10.685 | 0.013 | H0 rejected at 5% (WCB); CR1 t(G-1) p = 0.125 gives the opposite decision | robust: same sign in 4/4 sensitivities, WCB p < 0.05 in 4/4, jackknife sign changes 0 |
| O5 | Allowance / gross loans | N = 81 bank-years, 11 banks (40 pre / 41 post) | 4.832 | 0.110 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 5/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 0 |
| O5 | Impairment / average assets | N = 72 bank-years, 12 banks (35 pre / 37 post) | 1.081 | 0.286 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 5/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 0 |
| O5 | CAR | N = 74 bank-years, 11 banks (37 pre / 37 post) | 5.576 | 0.304 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 5/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 0 |
| O5 | ROA | N = 77 bank-years, 12 banks (39 pre / 38 post) | -0.433 | 0.160 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 4/4 sensitivities, WCB p < 0.05 in 0/4 (none); jackknife sign changes 0 |
| O5 | OCF / average assets | N = 71 bank-years, 11 banks (36 pre / 35 post) | 4.084 | 0.284 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 4/4 sensitivities, WCB p < 0.05 in 0/4 (none); jackknife sign changes 0 |
| O5 | Equity / assets | N = 97 bank-years, 12 banks (50 pre / 47 post) | 13.059 | 0.284 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 4/4 sensitivities, WCB p < 0.05 in 0/4 (none); jackknife sign changes 0 |
| O5 | Leverage | N = 97 bank-years, 12 banks (50 pre / 47 post) | -13.059 | 0.284 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 4/4 sensitivities, WCB p < 0.05 in 0/4 (none); jackknife sign changes 0 |
| O4 | Going-concern uncertainty | 46 coded bank-years, 10 banks; 3 events |  |  | not tested (3 events in one bank; a model would be unidentified/separation-prone) | not applicable |
| O6 | ROA | 8 banks with >= 3 comparable observations per regime |  | 0.383 | H0 not rejected (exploratory) | exploratory; SDs from 3-5 points |
| O6 | CAR | 6 banks with >= 3 comparable observations per regime |  | 0.062 | H0 not rejected (exploratory) | exploratory; SDs from 3-5 points |
| O6 | Allowance / gross loans | 8 banks with >= 3 comparable observations per regime |  | 0.844 | H0 not rejected (exploratory) | exploratory; SDs from 3-5 points |
| O6 | Impairment / average assets | 8 banks with >= 3 comparable observations per regime |  | 0.039 | H0 rejected (exploratory) | exploratory; SDs from 3-5 points |

## 10. Files

Figures: figures/*.png|pdf; tables: tables/*.csv|md; workbook: analysis_master.xlsx; archive: thesis_results_handoff.zip.
