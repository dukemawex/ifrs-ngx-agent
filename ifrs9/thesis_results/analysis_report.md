# Thesis analysis report (generated)

Generated 2026-10-11T07:55:51+00:00 by `python -m thesis_analysis` at code commit `1d69f9db8fa3fe7daf210715a0e08e16276f139c`.
Input: frozen release `IFRS9_release_2026-10-11_v2` (42 files hash-verified against RELEASE_MANIFEST.json; release code commit `1d69f9db8fa3fe7daf210715a0e08e16276f139c`).
Every number below is read back from the exported file named in brackets. No thesis prose; no data were changed.

## 1. Sample

- Cohort: 12 banks (5 Tier 1 / 7 Tier 2); FCMB formally excluded and not replaced [tables/table1_sample_coverage.csv].
- Selected bank-years: 98 of 120 positions (50 pre-IFRS 9, 48 post) [tables/table1_sample_coverage.csv].
- Eligible N by outcome [tables/table2_variables_eligible_n.csv]:

  - Allowance / gross loans: 82 (pre 40, post 42; Tier 1 36, Tier 2 46; 11 banks; excluded 1; role: inferential models)
  - Impairment / average assets: 73 (pre 35, post 38; Tier 1 31, Tier 2 42; 12 banks; excluded 2; role: inferential models)
  - CAR: 75 (pre 37, post 38; Tier 1 32, Tier 2 43; 11 banks; excluded 2; role: inferential models)
  - ROA: 78 (pre 39, post 39; Tier 1 33, Tier 2 45; 12 banks; excluded 0; role: inferential models)
  - OCF / average assets: 72 (pre 36, post 36; Tier 1 31, Tier 2 41; 11 banks; excluded 0; role: inferential models)
  - Equity / assets: 98 (pre 50, post 48; Tier 1 41, Tier 2 57; 12 banks; excluded 0; role: inferential models)
  - Leverage: 98 (pre 50, post 48; Tier 1 41, Tier 2 57; 12 banks; excluded 0; role: inferential models)
  - NPL ratio: 14 (pre 7, post 7; Tier 1 6, Tier 2 8; 3 banks; excluded 0; role: descriptive only (too sparse))
  - Broad NPL coverage: 13 (pre 7, post 6; Tier 1 6, Tier 2 7; 3 banks; excluded 1; role: descriptive only (too sparse))
  - Stage 3 coverage: 5 (pre 0, post 5; Tier 1 0, Tier 2 5; 2 banks; excluded 1; role: descriptive only (too sparse))
  - Liquidity ratio: 10 (pre 5, post 5; Tier 1 7, Tier 2 3; 3 banks; excluded 0; role: descriptive only (too sparse))
  - Going-concern uncertainty: 46 (pre 18, post 28; Tier 1 13, Tier 2 33; 10 banks; excluded 0; role: event description only)

## 2. Principal results (bank fixed effects, M1: y ~ IFRS9_D) [regression_results.csv]

| Outcome | Coef (pp) | CR1 SE | p conventional | p CR1 t(G-1) | p WCB | N | Banks |
|---|---|---|---|---|---|---|---|
| Allowance / gross loans | -0.908 | 1.853 | 0.301 | 0.635 | 0.880 | 82 | 11 |
| Impairment / average assets | -0.882 | 0.561 | 0.001 | 0.144 | 0.080 | 73 | 12 |
| CAR | -2.784 | 2.265 | 0.593 | 0.247 | 0.206 | 75 | 11 |
| ROA | -0.042 | 0.159 | 0.837 | 0.798 | 0.800 | 78 | 12 |
| OCF / average assets | 7.332 | 1.814 | 0.000 | 0.002 | 0.017 | 72 | 11 |
| Equity / assets | -10.626 | 6.358 | 0.018 | 0.123 | 0.013 | 98 | 12 |
| Leverage | 10.626 | 6.358 | 0.018 | 0.123 | 0.013 | 98 | 12 |

## 3. Tier 1 vs Tier 2 (M4: bank + year FE, Tier1 x IFRS9_D) [regression_results.csv]

| Outcome | Coef (pp) | CR1 SE | p CR1 | p WCB | N |
|---|---|---|---|---|---|
| Allowance / gross loans | 4.742 | 2.871 | 0.130 | 0.114 | 82 |
| Impairment / average assets | 1.142 | 0.931 | 0.246 | 0.255 | 73 |
| CAR | 5.131 | 4.597 | 0.290 | 0.307 | 75 |
| ROA | -0.437 | 0.273 | 0.138 | 0.160 | 78 |
| OCF / average assets | 3.887 | 3.440 | 0.285 | 0.285 | 72 |
| Equity / assets | 12.837 | 10.711 | 0.256 | 0.282 | 98 |
| Leverage | -12.837 | 10.711 | 0.256 | 0.282 | 98 |

## 4. Robustness of M1 (IFRS9_D) [robustness_results.csv, jackknife_results.csv]

| Outcome | S0 | S1 | S2 | S3 | S4 | S5 | Jackknife min | Jackknife max | Sign changes |
|---|---|---|---|---|---|---|---|---|---|
| Allowance / gross loans | -0.91 (p=0.880) | -0.95 (p=0.855) | -0.80 (p=0.920) | 0.87 (p=0.207) | -1.01 (p=0.863) | 0.87 (p=0.209) | -1.49 | 0.87 | 1 |
| Impairment / average assets | -0.88 (p=0.080) | -0.92 (p=0.089) | -1.14 (p=0.081) | -0.36 (p=0.157) | -1.01 (p=0.064) | -0.36 (p=0.156) | -1.09 | -0.36 | 0 |
| CAR | -2.78 (p=0.206) | -2.87 (p=0.222) | -2.74 (p=0.204) | -0.71 (p=0.402) | -3.04 (p=0.223) | -0.71 (p=0.402) | -3.62 | -0.71 | 0 |
| ROA | -0.04 (p=0.800) | -0.02 (p=0.921) | n/a | -0.14 (p=0.379) | 0.02 (p=0.913) | -0.14 (p=0.381) | -0.14 | 0.07 | 3 |
| OCF / average assets | 7.33 (p=0.017) | 8.42 (p=0.013) | n/a | 8.84 (p=0.007) | 8.07 (p=0.021) | 8.84 (p=0.006) | 6.52 | 8.84 | 0 |
| Equity / assets | -10.63 (p=0.013) | -9.61 (p=0.013) | n/a | -4.20 (p=0.008) | -11.28 (p=0.015) | -4.20 (p=0.009) | -11.91 | -4.20 | 0 |
| Leverage | 10.63 (p=0.013) | 9.61 (p=0.013) | n/a | 4.20 (p=0.008) | 11.28 (p=0.015) | 4.20 (p=0.009) | 4.20 | 11.91 | 0 |

S0 primary; S1 drop fallback rows; S2 add exception rows (n/a where none); S3 drop Unity negative-capital rows; S4 drop 2020; S5 drop Unity. p = WCB.

## 5. Matched pre/post (bank means, banks in both regimes) [matched_prepost_summary.csv]

- Allowance / gross loans: 9 banks; mean difference -0.992 pp, median 0.877; 6 up / 3 down; Wilcoxon p = 0.570.
- Impairment / average assets: 9 banks; mean difference -0.962 pp, median -0.350; 1 up / 8 down; Wilcoxon p = 0.074.
- CAR: 8 banks; mean difference -3.904 pp, median -1.243; 2 up / 6 down; Wilcoxon p = 0.195.
- ROA: 9 banks; mean difference 0.004 pp, median 0.048; 5 up / 4 down; Wilcoxon p = 0.910.
- OCF / average assets: 9 banks; mean difference 6.264 pp, median 9.048; 7 up / 2 down; Wilcoxon p = 0.020.
- Equity / assets: 9 banks; mean difference -10.146 pp, median -4.707; 1 up / 8 down; Wilcoxon p = 0.008.
- Leverage: 9 banks; mean difference 10.146 pp, median 4.707; 8 up / 1 down; Wilcoxon p = 0.008.

## 6. Volatility (EXPLORATORY) [volatility_results_summary.csv]

- Allowance / gross loans: 8 banks; median SD pre 0.913, post 0.735, median ratio 1.19; 5 higher / 3 lower; Wilcoxon p = 0.844.
- Impairment / average assets: 8 banks; median SD pre 0.480, post 0.172, median ratio 0.34; 2 higher / 6 lower; Wilcoxon p = 0.055.
- CAR: 7 banks; median SD pre 2.626, post 1.850, median ratio 0.77; 2 higher / 5 lower; Wilcoxon p = 0.297.
- ROA: 8 banks; median SD pre 0.290, post 0.246, median ratio 0.60; 3 higher / 5 lower; Wilcoxon p = 0.383.
- OCF / average assets: 7 banks; median SD pre 5.819, post 6.391, median ratio 1.40; 4 higher / 3 lower; Wilcoxon p = 0.688.
- Equity / assets: 9 banks; median SD pre 1.006, post 1.162, median ratio 1.39; 5 higher / 4 lower; Wilcoxon p = 0.359.
- Leverage: 9 banks; median SD pre 1.006, post 1.162, median ratio 1.39; 5 higher / 4 lower; Wilcoxon p = 0.359.

## 7. Going concern (descriptive only) [going_concern_events.csv, going_concern_coverage.csv]

- Unity 2019 (Tier 2): auditor KPMG Professional Services, report 2020-05-20; CAR -201.59% (other banks' median 17.95%), equity/assets -95.16% (other banks 11.07%), ROA 1.34%.
- Unity 2021 (Tier 2): auditor KPMG Professional Services (Chartered Accountants), Lagos, report 6 May, 2022; CAR -86.18% (other banks' median 17.62%), equity/assets -51.25% (other banks 9.01%), ROA 0.62%.
- Unity 2022 (Tier 2): auditor KPMG Professional Services (Chartered Accountants), Lagos, Nigeria, report 25 May 2023; CAR -89.69% (other banks' median 18.00%), equity/assets -53.90% (other banks 8.43%), ROA 0.18%.
- Coded bank-years 46, events 3; pre-IFRS 9 events 0, post 3; descriptive Fisher exact p = 0.270. No logistic/probit model estimated.

## 8. Diagnostics [model_diagnostics.csv]

- Allowance / gross loans: within share of variance 0.79; max Cook's D 0.67 (Unity 2016); 2 obs > 4/N; JB p 0.000; BP p 0.157; Wooldridge AR(1) p 0.000.
- Impairment / average assets: within share of variance 0.63; max Cook's D 0.32 (Unity 2016); 4 obs > 4/N; JB p 0.000; BP p 0.635; Wooldridge AR(1) p 0.005.
- CAR: within share of variance 0.17; max Cook's D 0.66 (Unity 2016); 5 obs > 4/N; JB p 0.000; BP p 0.563; Wooldridge AR(1) p 0.000.
- ROA: within share of variance 0.27; max Cook's D 0.44 (Unity 2017); 2 obs > 4/N; JB p 0.000; BP p 0.258; Wooldridge AR(1) p 0.059.
- OCF / average assets: within share of variance 0.77; max Cook's D 0.07 (UBA 2019); 5 obs > 4/N; JB p 0.520; BP p 0.945; Wooldridge AR(1) p 0.563.
- Equity / assets: within share of variance 0.53; max Cook's D 0.40 (Unity 2017); 7 obs > 4/N; JB p 0.000; BP p 0.215; Wooldridge AR(1) p 0.000.
- Leverage: within share of variance 0.53; max Cook's D 0.40 (Unity 2017); 7 obs > 4/N; JB p 0.000; BP p 0.215; Wooldridge AR(1) p 0.000.
- Adding ln(total assets) (M2): VIF of IFRS9_D 2.14-2.61; max Cook's D rises to 1.81 (Unity 2017), which is why M1 is principal.

## 9. Objective-level interpretation [interpretation.csv]

| Obj | Outcome | Sample | Coef (pp) | p WCB | Decision | Robustness |
|---|---|---|---|---|---|---|
| O1 | Allowance / gross loans | N = 82 bank-years, 11 banks (40 pre / 42 post) | -0.908 | 0.880 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 3/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 1 |
| O1 | Impairment / average assets | N = 73 bank-years, 12 banks (35 pre / 38 post) | -0.882 | 0.080 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 5/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 0 |
| O2 | CAR | N = 75 bank-years, 11 banks (37 pre / 38 post) | -2.784 | 0.206 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 5/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 0 |
| O3 | ROA | N = 78 bank-years, 12 banks (39 pre / 39 post) | -0.042 | 0.800 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 3/4 sensitivities, WCB p < 0.05 in 0/4 (none); jackknife sign changes 3 |
| O3 | OCF / average assets | N = 72 bank-years, 11 banks (36 pre / 36 post) | 7.332 | 0.017 | H0 rejected at 5% (WCB) | robust: same sign in 4/4 sensitivities, WCB p < 0.05 in 4/4, jackknife sign changes 0 |
| O3 | Equity / assets | N = 98 bank-years, 12 banks (50 pre / 48 post) | -10.626 | 0.013 | H0 rejected at 5% (WCB); CR1 t(G-1) p = 0.123 gives the opposite decision | robust: same sign in 4/4 sensitivities, WCB p < 0.05 in 4/4, jackknife sign changes 0 |
| O3 | Leverage | N = 98 bank-years, 12 banks (50 pre / 48 post) | 10.626 | 0.013 | H0 rejected at 5% (WCB); CR1 t(G-1) p = 0.123 gives the opposite decision | robust: same sign in 4/4 sensitivities, WCB p < 0.05 in 4/4, jackknife sign changes 0 |
| O5 | Allowance / gross loans | N = 82 bank-years, 11 banks (40 pre / 42 post) | 4.742 | 0.114 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 5/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 0 |
| O5 | Impairment / average assets | N = 73 bank-years, 12 banks (35 pre / 38 post) | 1.142 | 0.255 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 5/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 0 |
| O5 | CAR | N = 75 bank-years, 11 banks (37 pre / 38 post) | 5.131 | 0.307 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 5/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 0 |
| O5 | ROA | N = 78 bank-years, 12 banks (39 pre / 39 post) | -0.437 | 0.160 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 4/4 sensitivities, WCB p < 0.05 in 0/4 (none); jackknife sign changes 0 |
| O5 | OCF / average assets | N = 72 bank-years, 11 banks (36 pre / 36 post) | 3.887 | 0.285 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 4/4 sensitivities, WCB p < 0.05 in 0/4 (none); jackknife sign changes 0 |
| O5 | Equity / assets | N = 98 bank-years, 12 banks (50 pre / 48 post) | 12.837 | 0.282 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 4/4 sensitivities, WCB p < 0.05 in 0/4 (none); jackknife sign changes 0 |
| O5 | Leverage | N = 98 bank-years, 12 banks (50 pre / 48 post) | -12.837 | 0.282 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 4/4 sensitivities, WCB p < 0.05 in 0/4 (none); jackknife sign changes 0 |
| O4 | Going-concern uncertainty | 46 coded bank-years, 10 banks; 3 events |  |  | not tested (3 events in one bank; a model would be unidentified/separation-prone) | not applicable |
| O6 | ROA | 8 banks with >= 3 comparable observations per regime |  | 0.383 | H0 not rejected (exploratory) | exploratory; SDs from 3-5 points |
| O6 | CAR | 7 banks with >= 3 comparable observations per regime |  | 0.297 | H0 not rejected (exploratory) | exploratory; SDs from 3-5 points |
| O6 | Allowance / gross loans | 8 banks with >= 3 comparable observations per regime |  | 0.844 | H0 not rejected (exploratory) | exploratory; SDs from 3-5 points |
| O6 | Impairment / average assets | 8 banks with >= 3 comparable observations per regime |  | 0.055 | H0 not rejected (exploratory) | exploratory; SDs from 3-5 points |

## 10. Files

Figures: figures/*.png|pdf; tables: tables/*.csv|md; workbook: analysis_master.xlsx; archive: thesis_results_handoff.zip.
