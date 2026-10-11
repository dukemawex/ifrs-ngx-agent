# Thesis analysis report (generated)

Generated 2026-10-11T12:48:32+00:00 by `python -m thesis_analysis` at code commit `08ee95fbe8ed059dc205056133f4058709aca764`.
Input: frozen release `IFRS9_release_2026-10-11_v5` (42 files hash-verified against RELEASE_MANIFEST.json; release code commit `08ee95fbe8ed059dc205056133f4058709aca764`).
Every number below is read back from the exported file named in brackets. No thesis prose; no data were changed.

## 1. Sample

- Cohort: 12 banks (5 Tier 1 / 7 Tier 2); FCMB formally excluded and not replaced [tables/table1_sample_coverage.csv].
- Selected bank-years: 118 of 120 positions (60 pre-IFRS 9, 58 post) [tables/table1_sample_coverage.csv].
- Eligible N by outcome [tables/table2_variables_eligible_n.csv]:

  - Allowance / gross loans: 93 (pre 45, post 48; Tier 1 39, Tier 2 54; 12 banks; excluded 2; role: inferential models)
  - Impairment / average assets: 90 (pre 45, post 45; Tier 1 35, Tier 2 55; 12 banks; excluded 2; role: inferential models)
  - CAR: 86 (pre 41, post 45; Tier 1 35, Tier 2 51; 12 banks; excluded 3; role: inferential models)
  - ROA: 97 (pre 49, post 48; Tier 1 39, Tier 2 58; 12 banks; excluded 0; role: inferential models)
  - OCF / average assets: 86 (pre 41, post 45; Tier 1 37, Tier 2 49; 12 banks; excluded 0; role: inferential models)
  - Equity / assets: 118 (pre 60, post 58; Tier 1 48, Tier 2 70; 12 banks; excluded 0; role: inferential models)
  - Leverage: 118 (pre 60, post 58; Tier 1 48, Tier 2 70; 12 banks; excluded 0; role: inferential models)
  - NPL ratio: 19 (pre 7, post 12; Tier 1 6, Tier 2 13; 4 banks; excluded 0; role: descriptive only (too sparse))
  - Broad NPL coverage: 18 (pre 7, post 11; Tier 1 6, Tier 2 12; 4 banks; excluded 1; role: descriptive only (too sparse))
  - Stage 3 coverage: 5 (pre 0, post 5; Tier 1 0, Tier 2 5; 2 banks; excluded 1; role: descriptive only (too sparse))
  - Liquidity ratio: 10 (pre 5, post 5; Tier 1 7, Tier 2 3; 3 banks; excluded 0; role: descriptive only (too sparse))
  - Going-concern uncertainty: 58 (pre 23, post 35; Tier 1 17, Tier 2 41; 11 banks; excluded 0; role: event description only)

## 2. Principal results (bank fixed effects, M1: y ~ IFRS9_D) [regression_results.csv]

| Outcome | Coef (pp) | CR1 SE | p conventional | p CR1 t(G-1) | p WCB | N | Banks |
|---|---|---|---|---|---|---|---|
| Allowance / gross loans | -0.517 | 1.598 | 0.508 | 0.752 | 0.916 | 93 | 12 |
| Impairment / average assets | -1.075 | 0.425 | 0.000 | 0.028 | 0.008 | 90 | 12 |
| CAR | -2.797 | 1.823 | 0.519 | 0.153 | 0.082 | 86 | 12 |
| ROA | -0.064 | 0.144 | 0.709 | 0.664 | 0.665 | 97 | 12 |
| OCF / average assets | 6.347 | 1.617 | 0.000 | 0.002 | 0.008 | 86 | 12 |
| Equity / assets | -7.995 | 4.859 | 0.021 | 0.128 | 0.009 | 118 | 12 |
| Leverage | 7.995 | 4.859 | 0.021 | 0.128 | 0.009 | 118 | 12 |

## 3. Tier 1 vs Tier 2 (M4: bank + year FE, Tier1 x IFRS9_D) [regression_results.csv]

| Outcome | Coef (pp) | CR1 SE | p CR1 | p WCB | N |
|---|---|---|---|---|---|
| Allowance / gross loans | 3.566 | 2.719 | 0.216 | 0.217 | 93 |
| Impairment / average assets | 1.075 | 0.687 | 0.146 | 0.133 | 90 |
| CAR | 6.431 | 6.282 | 0.328 | 0.369 | 86 |
| ROA | -0.482 | 0.229 | 0.059 | 0.059 | 97 |
| OCF / average assets | 2.610 | 3.330 | 0.450 | 0.456 | 86 |
| Equity / assets | 8.839 | 8.448 | 0.318 | 0.369 | 118 |
| Leverage | -8.839 | 8.448 | 0.318 | 0.369 | 118 |

## 4. Robustness of M1 (IFRS9_D) [robustness_results.csv, jackknife_results.csv]

| Outcome | S0 | S1 | S2 | S3 | S4 | S5 | S6 | Jackknife min | Jackknife max | Sign changes |
|---|---|---|---|---|---|---|---|---|---|---|
| Allowance / gross loans | -0.52 (p=0.916) | -0.47 (p=0.910) | -0.11 (p=0.987) | 0.98 (p=0.135) | -0.65 (p=0.892) | 0.98 (p=0.136) | -0.52 (p=0.916) | -0.94 | 0.98 | 1 |
| Impairment / average assets | -1.08 (p=0.008) | -1.11 (p=0.008) | -1.26 (p=0.011) | -0.73 (p=0.014) | -1.17 (p=0.007) | -0.73 (p=0.013) | -1.05 (p=0.017) | -1.23 | -0.73 | 0 |
| CAR | -2.80 (p=0.082) | -2.86 (p=0.088) | -2.68 (p=0.085) | -1.17 (p=0.155) | -3.17 (p=0.068) | -1.17 (p=0.155) | -2.80 (p=0.082) | -3.45 | -1.17 | 0 |
| ROA | -0.06 (p=0.665) | -0.03 (p=0.831) | n/a | -0.13 (p=0.354) | -0.03 (p=0.840) | -0.13 (p=0.356) | -0.06 (p=0.702) | -0.14 | 0.01 | 1 |
| OCF / average assets | 6.35 (p=0.008) | 6.97 (p=0.007) | n/a | 7.42 (p=0.000) | 6.87 (p=0.014) | 7.42 (p=0.000) | 6.35 (p=0.009) | 5.61 | 7.42 | 0 |
| Equity / assets | -8.00 (p=0.009) | -7.11 (p=0.010) | n/a | -3.21 (p=0.004) | -8.42 (p=0.009) | -3.21 (p=0.003) | -8.88 (p=0.010) | -8.75 | -3.21 | 0 |
| Leverage | 8.00 (p=0.009) | 7.11 (p=0.010) | n/a | 3.21 (p=0.004) | 8.42 (p=0.009) | 3.21 (p=0.003) | 8.88 (p=0.010) | 3.21 | 8.75 | 0 |

S0 primary; S1 drop fallback rows; S2 add exception rows (n/a where none); S3 drop Unity negative-capital rows; S4 drop 2020; S5 drop Unity; S6 drop HoldCo-disclosure rows. p = WCB.

## 5. Matched pre/post (bank means, banks in both regimes) [matched_prepost_summary.csv]

- Allowance / gross loans: 11 banks; mean difference -0.754 pp, median 1.406; 7 up / 4 down; Wilcoxon p = 0.765.
- Impairment / average assets: 12 banks; mean difference -1.132 pp, median -0.658; 1 up / 11 down; Wilcoxon p = 0.009.
- CAR: 11 banks; mean difference -3.488 pp, median -1.450; 3 up / 8 down; Wilcoxon p = 0.054.
- ROA: 12 banks; mean difference -0.043 pp, median 0.001; 6 up / 6 down; Wilcoxon p = 0.791.
- OCF / average assets: 11 banks; mean difference 6.010 pp, median 7.523; 10 up / 1 down; Wilcoxon p = 0.007.
- Equity / assets: 12 banks; mean difference -7.881 pp, median -3.353; 1 up / 11 down; Wilcoxon p = 0.001.
- Leverage: 12 banks; mean difference 7.881 pp, median 3.353; 11 up / 1 down; Wilcoxon p = 0.001.

## 6. Volatility (EXPLORATORY) [volatility_results_summary.csv]

- Allowance / gross loans: 10 banks; median SD pre 1.250, post 1.465, median ratio 1.30; 7 higher / 3 lower; Wilcoxon p = 0.492.
- Impairment / average assets: 11 banks; median SD pre 0.560, post 0.183, median ratio 0.33; 2 higher / 9 lower; Wilcoxon p = 0.014.
- CAR: 8 banks; median SD pre 2.346, post 2.034, median ratio 0.78; 3 higher / 5 lower; Wilcoxon p = 0.641.
- ROA: 11 banks; median SD pre 0.444, post 0.398, median ratio 0.99; 5 higher / 6 lower; Wilcoxon p = 0.638.
- OCF / average assets: 9 banks; median SD pre 5.819, post 5.557, median ratio 0.76; 4 higher / 5 lower; Wilcoxon p = 0.734.
- Equity / assets: 12 banks; median SD pre 1.059, post 1.347, median ratio 1.13; 6 higher / 6 lower; Wilcoxon p = 0.424.
- Leverage: 12 banks; median SD pre 1.059, post 1.347, median ratio 1.13; 6 higher / 6 lower; Wilcoxon p = 0.424.

## 7. Going concern (descriptive only) [going_concern_events.csv, going_concern_coverage.csv]

- Unity 2019 (Tier 2): auditor KPMG Professional Services, report 2020-05-20; CAR -201.59% (other banks' median 16.11%), equity/assets -95.16% (other banks 11.23%), ROA 1.34%.
- Unity 2021 (Tier 2): auditor KPMG Professional Services (Chartered Accountants), Lagos, report 6 May, 2022; CAR -86.18% (other banks' median 16.10%), equity/assets -51.25% (other banks 9.33%), ROA 0.62%.
- Unity 2022 (Tier 2): auditor KPMG Professional Services (Chartered Accountants), Lagos, Nigeria, report 25 May 2023; CAR -89.69% (other banks' median 17.85%), equity/assets -53.90% (other banks 9.27%), ROA 0.18%.
- Coded bank-years 58, events 3; pre-IFRS 9 events 0, post 3; descriptive Fisher exact p = 0.270. No logistic/probit model estimated.

## 8. Diagnostics [model_diagnostics.csv]

- Allowance / gross loans: within share of variance 0.76; max Cook's D 0.60 (Unity 2016); 2 obs > 4/N; JB p 0.000; BP p 0.156; Wooldridge AR(1) p 0.000.
- Impairment / average assets: within share of variance 0.73; max Cook's D 0.23 (Unity 2016); 4 obs > 4/N; JB p 0.000; BP p 0.358; Wooldridge AR(1) p 0.195.
- CAR: within share of variance 0.16; max Cook's D 0.60 (Unity 2016); 5 obs > 4/N; JB p 0.000; BP p 0.584; Wooldridge AR(1) p 0.000.
- ROA: within share of variance 0.29; max Cook's D 0.30 (Unity 2017); 4 obs > 4/N; JB p 0.000; BP p 0.409; Wooldridge AR(1) p 0.034.
- OCF / average assets: within share of variance 0.75; max Cook's D 0.06 (UBA 2019); 5 obs > 4/N; JB p 0.575; BP p 0.674; Wooldridge AR(1) p 0.646.
- Equity / assets: within share of variance 0.52; max Cook's D 0.34 (Unity 2017); 7 obs > 4/N; JB p 0.000; BP p 0.248; Wooldridge AR(1) p 0.000.
- Leverage: within share of variance 0.52; max Cook's D 0.34 (Unity 2017); 7 obs > 4/N; JB p 0.000; BP p 0.248; Wooldridge AR(1) p 0.000.
- Adding ln(total assets) (M2): VIF of IFRS9_D 2.23-2.39; max Cook's D rises to 1.54 (Unity 2016), which is why M1 is principal.

## 9. Objective-level interpretation [interpretation.csv]

| Obj | Outcome | Sample | Coef (pp) | p WCB | Decision | Robustness |
|---|---|---|---|---|---|---|
| O1 | Allowance / gross loans | N = 93 bank-years, 12 banks (45 pre / 48 post) | -0.517 | 0.916 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 4/6 sensitivities, WCB p < 0.05 in 0/6 (none); jackknife sign changes 1 |
| O1 | Impairment / average assets | N = 90 bank-years, 12 banks (45 pre / 45 post) | -1.075 | 0.008 | H0 rejected at 5% (WCB) | robust: same sign in 6/6 sensitivities, WCB p < 0.05 in 6/6, jackknife sign changes 0 |
| O2 | CAR | N = 86 bank-years, 12 banks (41 pre / 45 post) | -2.797 | 0.082 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 6/6 sensitivities, WCB p < 0.05 in 0/6 (none); jackknife sign changes 0 |
| O3 | ROA | N = 97 bank-years, 12 banks (49 pre / 48 post) | -0.064 | 0.665 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 5/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 1 |
| O3 | OCF / average assets | N = 86 bank-years, 12 banks (41 pre / 45 post) | 6.347 | 0.008 | H0 rejected at 5% (WCB) | robust: same sign in 5/5 sensitivities, WCB p < 0.05 in 5/5, jackknife sign changes 0 |
| O3 | Equity / assets | N = 118 bank-years, 12 banks (60 pre / 58 post) | -7.995 | 0.009 | H0 rejected at 5% (WCB); CR1 t(G-1) p = 0.128 gives the opposite decision | robust: same sign in 5/5 sensitivities, WCB p < 0.05 in 5/5, jackknife sign changes 0 |
| O3 | Leverage | N = 118 bank-years, 12 banks (60 pre / 58 post) | 7.995 | 0.009 | H0 rejected at 5% (WCB); CR1 t(G-1) p = 0.128 gives the opposite decision | robust: same sign in 5/5 sensitivities, WCB p < 0.05 in 5/5, jackknife sign changes 0 |
| O5 | Allowance / gross loans | N = 93 bank-years, 12 banks (45 pre / 48 post) | 3.566 | 0.217 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 6/6 sensitivities, WCB p < 0.05 in 0/6 (none); jackknife sign changes 0 |
| O5 | Impairment / average assets | N = 90 bank-years, 12 banks (45 pre / 45 post) | 1.075 | 0.133 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 6/6 sensitivities, WCB p < 0.05 in 0/6 (none); jackknife sign changes 0 |
| O5 | CAR | N = 86 bank-years, 12 banks (41 pre / 45 post) | 6.431 | 0.369 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 6/6 sensitivities, WCB p < 0.05 in 0/6 (none); jackknife sign changes 0 |
| O5 | ROA | N = 97 bank-years, 12 banks (49 pre / 48 post) | -0.482 | 0.059 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 5/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 0 |
| O5 | OCF / average assets | N = 86 bank-years, 12 banks (41 pre / 45 post) | 2.610 | 0.456 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 5/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 0 |
| O5 | Equity / assets | N = 118 bank-years, 12 banks (60 pre / 58 post) | 8.839 | 0.369 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 5/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 0 |
| O5 | Leverage | N = 118 bank-years, 12 banks (60 pre / 58 post) | -8.839 | 0.369 | H0 not rejected at 5% (WCB) | primary not significant; same sign in 5/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 0 |
| O4 | Going-concern uncertainty | 58 coded bank-years, 11 banks; 3 events |  |  | not tested (3 events in one bank; a model would be unidentified/separation-prone) | not applicable |
| O6 | ROA | 11 banks with >= 3 comparable observations per regime |  | 0.638 | H0 not rejected (exploratory) | exploratory; SDs from 3-5 points |
| O6 | CAR | 8 banks with >= 3 comparable observations per regime |  | 0.641 | H0 not rejected (exploratory) | exploratory; SDs from 3-5 points |
| O6 | Allowance / gross loans | 10 banks with >= 3 comparable observations per regime |  | 0.492 | H0 not rejected (exploratory) | exploratory; SDs from 3-5 points |
| O6 | Impairment / average assets | 11 banks with >= 3 comparable observations per regime |  | 0.014 | H0 rejected (exploratory) | exploratory; SDs from 3-5 points |

## 10. Files

Figures: figures/*.png|pdf; tables: tables/*.csv|md; workbook: analysis_master.xlsx; archive: thesis_results_handoff.zip.
