# Thesis analysis report (generated)

Generated 2026-10-11T11:30:37+00:00 by `python -m thesis_analysis` at code commit `9171cc7da3b6ffa69bb7b73d4ac38d0d5452545d`.
Input: frozen release `IFRS9_release_2026-10-11_v3` (42 files hash-verified against RELEASE_MANIFEST.json; release code commit `9171cc7da3b6ffa69bb7b73d4ac38d0d5452545d`).
Every number below is read back from the exported file named in brackets. No thesis prose; no data were changed.

## 1. Sample

- Cohort: 12 banks (5 Tier 1 / 7 Tier 2); FCMB formally excluded and not replaced [tables/table1_sample_coverage.csv].
- Selected bank-years: 114 of 120 positions (59 pre-IFRS 9, 55 post) [tables/table1_sample_coverage.csv].
- Eligible N by outcome [tables/table2_variables_eligible_n.csv]:

  - Allowance / gross loans: 92 (pre 45, post 47; Tier 1 38, Tier 2 54; 12 banks; excluded 1; role: inferential models)
  - Impairment / average assets: 87 (pre 44, post 43; Tier 1 33, Tier 2 54; 12 banks; excluded 2; role: inferential models)
  - CAR: 84 (pre 41, post 43; Tier 1 33, Tier 2 51; 12 banks; excluded 3; role: inferential models)
  - ROA: 94 (pre 48, post 46; Tier 1 37, Tier 2 57; 12 banks; excluded 0; role: inferential models)
  - OCF / average assets: 84 (pre 41, post 43; Tier 1 35, Tier 2 49; 12 banks; excluded 0; role: inferential models)
  - Equity / assets: 114 (pre 59, post 55; Tier 1 45, Tier 2 69; 12 banks; excluded 0; role: inferential models)
  - Leverage: 114 (pre 59, post 55; Tier 1 45, Tier 2 69; 12 banks; excluded 0; role: inferential models)
  - NPL ratio: 19 (pre 7, post 12; Tier 1 6, Tier 2 13; 4 banks; excluded 0; role: descriptive only (too sparse))
  - Broad NPL coverage: 18 (pre 7, post 11; Tier 1 6, Tier 2 12; 4 banks; excluded 1; role: descriptive only (too sparse))
  - Stage 3 coverage: 5 (pre 0, post 5; Tier 1 0, Tier 2 5; 2 banks; excluded 1; role: descriptive only (too sparse))
  - Liquidity ratio: 10 (pre 5, post 5; Tier 1 7, Tier 2 3; 3 banks; excluded 0; role: descriptive only (too sparse))
  - Going-concern uncertainty: 56 (pre 23, post 33; Tier 1 15, Tier 2 41; 11 banks; excluded 0; role: event description only)

## 2. Principal results (bank fixed effects, M1: y ~ IFRS9_D) [regression_results.csv]

| Outcome | Coef (pp) | CR1 SE | p conventional | p CR1 t(G-1) | p WCB | N | Banks |
|---|---|---|---|---|---|---|---|
| Allowance / gross loans | -0.397 | 1.657 | 0.619 | 0.815 | 0.951 | 92 | 12 |
| Impairment / average assets | -1.112 | 0.451 | 0.000 | 0.031 | 0.011 | 87 | 12 |
| CAR | -2.590 | 1.942 | 0.570 | 0.209 | 0.150 | 84 | 12 |
| ROA | -0.062 | 0.157 | 0.730 | 0.699 | 0.699 | 94 | 12 |
| OCF / average assets | 6.577 | 1.696 | 0.000 | 0.003 | 0.010 | 84 | 12 |
| Equity / assets | -8.480 | 5.210 | 0.021 | 0.132 | 0.012 | 114 | 12 |
| Leverage | 8.480 | 5.210 | 0.021 | 0.132 | 0.012 | 114 | 12 |

## 3. Tier 1 vs Tier 2 (M4: bank + year FE, Tier1 x IFRS9_D) [regression_results.csv]

| Outcome | Coef (pp) | CR1 SE | p CR1 | p WCB | N |
|---|---|---|---|---|---|
| Allowance / gross loans | 4.113 | 2.701 | 0.156 | 0.135 | 92 |
| Impairment / average assets | 1.178 | 0.700 | 0.120 | 0.111 | 87 |
| CAR | 6.032 | 5.200 | 0.271 | 0.270 | 84 |
| ROA | -0.480 | 0.223 | 0.055 | 0.055 | 94 |
| OCF / average assets | 3.609 | 3.398 | 0.311 | 0.320 | 84 |
| Equity / assets | 8.914 | 8.411 | 0.312 | 0.362 | 114 |
| Leverage | -8.914 | 8.411 | 0.312 | 0.362 | 114 |

## 4. Robustness of M1 (IFRS9_D) [robustness_results.csv, jackknife_results.csv]

| Outcome | S0 | S1 | S2 | S3 | S4 | S5 | S6 | Jackknife min | Jackknife max | Sign changes |
|---|---|---|---|---|---|---|---|---|---|---|
| Allowance / gross loans | -0.40 (p=0.951) | -0.34 (p=0.949) | -0.31 (p=0.969) | 1.18 (p=0.080) | -0.51 (p=0.938) | 1.18 (p=0.085) | -0.40 (p=0.951) | -0.82 | 1.18 | 1 |
| Impairment / average assets | -1.11 (p=0.011) | -1.15 (p=0.011) | -1.30 (p=0.015) | -0.74 (p=0.020) | -1.22 (p=0.010) | -0.74 (p=0.020) | -1.07 (p=0.024) | -1.28 | -0.74 | 0 |
| CAR | -2.59 (p=0.150) | -2.65 (p=0.159) | -2.47 (p=0.156) | -0.81 (p=0.288) | -2.97 (p=0.131) | -0.81 (p=0.288) | -2.59 (p=0.150) | -3.27 | -0.81 | 0 |
| ROA | -0.06 (p=0.699) | -0.03 (p=0.865) | n/a | -0.13 (p=0.389) | -0.03 (p=0.878) | -0.13 (p=0.393) | -0.07 (p=0.694) | -0.15 | 0.02 | 1 |
| OCF / average assets | 6.58 (p=0.010) | 7.25 (p=0.009) | n/a | 7.75 (p=0.000) | 7.17 (p=0.016) | 7.75 (p=0.001) | 6.58 (p=0.011) | 5.81 | 7.75 | 0 |
| Equity / assets | -8.48 (p=0.012) | -7.52 (p=0.011) | n/a | -3.32 (p=0.005) | -8.98 (p=0.012) | -3.32 (p=0.005) | -9.37 (p=0.014) | -9.33 | -3.32 | 0 |
| Leverage | 8.48 (p=0.012) | 7.52 (p=0.011) | n/a | 3.32 (p=0.005) | 8.98 (p=0.012) | 3.32 (p=0.005) | 9.37 (p=0.014) | 3.32 | 9.33 | 0 |

S0 primary; S1 drop fallback rows; S2 add exception rows (n/a where none); S3 drop Unity negative-capital rows; S4 drop 2020; S5 drop Unity; S6 drop HoldCo-disclosure rows. p = WCB.

## 5. Matched pre/post (bank means, banks in both regimes) [matched_prepost_summary.csv]

- Allowance / gross loans: 10 banks; mean difference -0.484 pp, median 1.491; 7 up / 3 down; Wilcoxon p = 0.375.
- Impairment / average assets: 11 banks; mean difference -1.190 pp, median -0.581; 1 up / 10 down; Wilcoxon p = 0.014.
- CAR: 10 banks; mean difference -3.289 pp, median -1.243; 3 up / 7 down; Wilcoxon p = 0.105.
- ROA: 11 banks; mean difference -0.035 pp, median -0.028; 5 up / 6 down; Wilcoxon p = 0.765.
- OCF / average assets: 10 banks; mean difference 6.342 pp, median 8.285; 9 up / 1 down; Wilcoxon p = 0.010.
- Equity / assets: 11 banks; mean difference -8.396 pp, median -4.203; 0 up / 11 down; Wilcoxon p = 0.001.
- Leverage: 11 banks; mean difference 8.396 pp, median 4.203; 11 up / 0 down; Wilcoxon p = 0.001.

## 6. Volatility (EXPLORATORY) [volatility_results_summary.csv]

- Allowance / gross loans: 10 banks; median SD pre 1.250, post 1.465, median ratio 1.30; 7 higher / 3 lower; Wilcoxon p = 0.492.
- Impairment / average assets: 11 banks; median SD pre 0.560, post 0.183, median ratio 0.33; 2 higher / 9 lower; Wilcoxon p = 0.014.
- CAR: 8 banks; median SD pre 2.346, post 2.034, median ratio 0.78; 3 higher / 5 lower; Wilcoxon p = 0.641.
- ROA: 11 banks; median SD pre 0.444, post 0.398, median ratio 0.99; 5 higher / 6 lower; Wilcoxon p = 0.638.
- OCF / average assets: 9 banks; median SD pre 5.819, post 5.557, median ratio 0.76; 4 higher / 5 lower; Wilcoxon p = 0.734.
- Equity / assets: 11 banks; median SD pre 1.006, post 1.482, median ratio 1.28; 7 higher / 4 lower; Wilcoxon p = 0.175.
- Leverage: 11 banks; median SD pre 1.006, post 1.482, median ratio 1.28; 7 higher / 4 lower; Wilcoxon p = 0.175.

## 7. Going concern (descriptive only) [going_concern_events.csv, going_concern_coverage.csv]

- Unity 2019 (Tier 2): auditor KPMG Professional Services, report 2020-05-20; CAR -201.59% (other banks' median 16.31%), equity/assets -95.16% (other banks 11.15%), ROA 1.34%.
- Unity 2021 (Tier 2): auditor KPMG Professional Services (Chartered Accountants), Lagos, report 6 May, 2022; CAR -86.18% (other banks' median 16.10%), equity/assets -51.25% (other banks 9.33%), ROA 0.62%.
- Unity 2022 (Tier 2): auditor KPMG Professional Services (Chartered Accountants), Lagos, Nigeria, report 25 May 2023; CAR -89.69% (other banks' median 17.85%), equity/assets -53.90% (other banks 9.15%), ROA 0.18%.
- Coded bank-years 56, events 3; pre-IFRS 9 events 0, post 3; descriptive Fisher exact p = 0.261. No logistic/probit model estimated.

## 8. Diagnostics [model_diagnostics.csv]

- Allowance / gross loans: within share of variance 0.75; max Cook's D 0.63 (Unity 2016); 2 obs > 4/N; JB p 0.000; BP p 0.166; Wooldridge AR(1) p 0.000.
- Impairment / average assets: within share of variance 0.72; max Cook's D 0.24 (Unity 2016); 4 obs > 4/N; JB p 0.000; BP p 0.481; Wooldridge AR(1) p 0.224.
- CAR: within share of variance 0.16; max Cook's D 0.64 (Unity 2016); 6 obs > 4/N; JB p 0.000; BP p 0.574; Wooldridge AR(1) p 0.000.
- ROA: within share of variance 0.29; max Cook's D 0.31 (Unity 2017); 3 obs > 4/N; JB p 0.000; BP p 0.444; Wooldridge AR(1) p 0.013.
- OCF / average assets: within share of variance 0.75; max Cook's D 0.07 (UBA 2019); 5 obs > 4/N; JB p 0.592; BP p 0.900; Wooldridge AR(1) p 0.643.
- Equity / assets: within share of variance 0.52; max Cook's D 0.36 (Unity 2017); 7 obs > 4/N; JB p 0.000; BP p 0.236; Wooldridge AR(1) p 0.000.
- Leverage: within share of variance 0.52; max Cook's D 0.36 (Unity 2017); 7 obs > 4/N; JB p 0.000; BP p 0.236; Wooldridge AR(1) p 0.000.
- Adding ln(total assets) (M2): VIF of IFRS9_D 2.23-2.45; max Cook's D rises to 1.63 (Unity 2016), which is why M1 is principal.

## 9. Objective-level interpretation [interpretation.csv]

| Obj | Outcome | Sample | Coef (pp) | p WCB | Decision | Robustness |
|---|---|---|---|---|---|---|
| O1 | Allowance / gross loans | N = 92 bank-years, 12 banks (45 pre / 47 post) | -0.397 | 0.951 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 4/6 sensitivities, WCB p < 0.05 in 0/6 (none); jackknife sign changes 1 |
| O1 | Impairment / average assets | N = 87 bank-years, 12 banks (44 pre / 43 post) | -1.112 | 0.011 | H0 rejected at 5% (WCB) | robust: same sign in 6/6 sensitivities, WCB p < 0.05 in 6/6, jackknife sign changes 0 |
| O2 | CAR | N = 84 bank-years, 12 banks (41 pre / 43 post) | -2.590 | 0.150 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 6/6 sensitivities, WCB p < 0.05 in 0/6 (none); jackknife sign changes 0 |
| O3 | ROA | N = 94 bank-years, 12 banks (48 pre / 46 post) | -0.062 | 0.699 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 5/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 1 |
| O3 | OCF / average assets | N = 84 bank-years, 12 banks (41 pre / 43 post) | 6.577 | 0.010 | H0 rejected at 5% (WCB) | robust: same sign in 5/5 sensitivities, WCB p < 0.05 in 5/5, jackknife sign changes 0 |
| O3 | Equity / assets | N = 114 bank-years, 12 banks (59 pre / 55 post) | -8.480 | 0.012 | H0 rejected at 5% (WCB); CR1 t(G-1) p = 0.132 gives the opposite decision | robust: same sign in 5/5 sensitivities, WCB p < 0.05 in 5/5, jackknife sign changes 0 |
| O3 | Leverage | N = 114 bank-years, 12 banks (59 pre / 55 post) | 8.480 | 0.012 | H0 rejected at 5% (WCB); CR1 t(G-1) p = 0.132 gives the opposite decision | robust: same sign in 5/5 sensitivities, WCB p < 0.05 in 5/5, jackknife sign changes 0 |
| O5 | Allowance / gross loans | N = 92 bank-years, 12 banks (45 pre / 47 post) | 4.113 | 0.135 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 6/6 sensitivities, WCB p < 0.05 in 0/6 (none); jackknife sign changes 0 |
| O5 | Impairment / average assets | N = 87 bank-years, 12 banks (44 pre / 43 post) | 1.178 | 0.111 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 6/6 sensitivities, WCB p < 0.05 in 0/6 (none); jackknife sign changes 0 |
| O5 | CAR | N = 84 bank-years, 12 banks (41 pre / 43 post) | 6.032 | 0.270 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 6/6 sensitivities, WCB p < 0.05 in 0/6 (none); jackknife sign changes 0 |
| O5 | ROA | N = 94 bank-years, 12 banks (48 pre / 46 post) | -0.480 | 0.055 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 5/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 0 |
| O5 | OCF / average assets | N = 84 bank-years, 12 banks (41 pre / 43 post) | 3.609 | 0.320 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 5/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 0 |
| O5 | Equity / assets | N = 114 bank-years, 12 banks (59 pre / 55 post) | 8.914 | 0.362 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 5/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 0 |
| O5 | Leverage | N = 114 bank-years, 12 banks (59 pre / 55 post) | -8.914 | 0.362 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 5/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 0 |
| O4 | Going-concern uncertainty | 56 coded bank-years, 11 banks; 3 events |  |  | not tested (3 events in one bank; a model would be unidentified/separation-prone) | not applicable |
| O6 | ROA | 11 banks with >= 3 comparable observations per regime |  | 0.638 | H0 not rejected (exploratory) | exploratory; SDs from 3-5 points |
| O6 | CAR | 8 banks with >= 3 comparable observations per regime |  | 0.641 | H0 not rejected (exploratory) | exploratory; SDs from 3-5 points |
| O6 | Allowance / gross loans | 10 banks with >= 3 comparable observations per regime |  | 0.492 | H0 not rejected (exploratory) | exploratory; SDs from 3-5 points |
| O6 | Impairment / average assets | 11 banks with >= 3 comparable observations per regime |  | 0.014 | H0 rejected (exploratory) | exploratory; SDs from 3-5 points |

## 10. Files

Figures: figures/*.png|pdf; tables: tables/*.csv|md; workbook: analysis_master.xlsx; archive: thesis_results_handoff.zip.
