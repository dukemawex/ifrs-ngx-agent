# Comparison: release v2 vs v3 (current)

v2: `IFRS9_release_2026-10-11_v2`, results in `thesis_results_v2/`. v3: `IFRS9_release_2026-10-11_v3`, results in `thesis_results/`. Same code, estimators, seed and B = 9,999. Every number below is read from the comparison_*.csv files named in brackets.

Material-change rule (set before comparing): the 5% decision changes under WCB or CR1, the sign changes, or the coefficient moves by at least 0.5 previous CR1 standard errors.

## 1. Rows added [comparison_rows_added.csv]

- added: Ecobank Nigeria 2013 (Tier 2); 2013 annual report, as originally reported; source https://www.ecobank.com/upload/publication/20160603050431876MVJZ65QMD2/20140717070804117617CS9N8RVrc92013.pdf
- added: Ecobank Nigeria 2014 (Tier 2); 2014 annual report, as originally reported; source https://www.ecobank.com/upload/publication/20160603050328266BV9KK3KMGZ/20150424114643650413NqzAyDndnW2014.PDF
- added: Ecobank Nigeria 2015 (Tier 2); 2015 annual report, as originally reported; source https://www.ecobank.com/upload/publication/20160810051714162FAUN9WFV76/20160810051700933X.pdf
- added: Ecobank Nigeria 2018 (Tier 2); 2018 annual report, as originally reported; source https://www.ecobank.com/upload/publication/201908161135521993YH9XK3GUU/201908161135142514.pdf
- added: Ecobank Nigeria 2019 (Tier 2); 2019 annual report, as originally reported; source https://www.ecobank.com/upload/publication/20200901042621276B6RH5TBQ22/20200901042502327T.pdf
- added: Ecobank Nigeria 2020 (Tier 2); 2020 annual report, as originally reported; source https://www.ecobank.com/upload/publication/20210803011222677VJB2VFNZ2Y/20210803011214097V.pdf
- added: Ecobank Nigeria 2021 (Tier 2); 2021 annual report, as originally reported; source https://www.ecobank.com/upload/publication/20220707035014829GBVPAXGW87/20220707034953065D.pdf
- added: Ecobank Nigeria 2022 (Tier 2); 2022 annual report, as originally reported; source https://www.ecobank.com/upload/publication/20240318051756025XSA3RCX9NN/20240318051750118B.pdf
- added: GTBank 2015 (Tier 1); 2015 annual report, as originally reported; source https://gtbank-plc.files.svdcdn.com/production/financial-information/2015-Year-End-Audited-Results.pdf
- added: GTBank 2016 (Tier 1); 2016 annual report, as originally reported (public mirror copy); source https://www.annualreports.com/HostedData/AnnualReportArchive/g/guaranty-trust-bank-ltd_2016.pdf
- added: GTBank 2021 (Tier 1); GTCO 2021 annual report: audited HoldCo package - explicit operating-bank subsidiary disclosure (GT Bank Nigeria condensed results); source https://gtco-plc.files.svdcdn.com/production/financial-information/2021-ANNUAL-REPORT.pdf?dm=1648469779
- added: GTBank 2022 (Tier 1); GTCO 2022 annual report: audited HoldCo package - explicit operating-bank subsidiary disclosure (GT Bank Nigeria condensed results); source https://gtco-plc.files.svdcdn.com/production/financial-information/2022-Annual-Report.pdf?dm=1687801902
- added: Stanbic 2013 (Tier 2); Stanbic IBTC Holdings 2013 annual report: audited HoldCo package - explicit operating-bank subsidiary disclosure (note 13.4, Stanbic IBTC Bank PLC); source https://thevault.exchange/?get_group_doc=18%2F1447238936-StanbicIBTCannualreport2013.pdf
- added: Stanbic 2015 (Tier 2); Stanbic IBTC Holdings 2015 annual report: audited HoldCo package - explicit operating-bank subsidiary disclosure (note 13.4, Stanbic IBTC Bank PLC); source https://www.thevault.exchange/?get_group_doc=635%2F1484830056-Annualreport2015final.pdf
- added: Stanbic 2016 (Tier 2); Stanbic IBTC Holdings 2016 annual report: audited HoldCo package - explicit operating-bank subsidiary disclosure (note 13.4, Stanbic IBTC Bank PLC); source https://thevault.exchange?get_group_doc=635/1502962292-2016AnnualReport.pdf
- added: Stanbic 2017 (Tier 2); Stanbic IBTC Holdings 2017 annual report: audited HoldCo package - explicit operating-bank subsidiary disclosure (note 13.4, Stanbic IBTC Bank PLC); source https://www.thevault.exchange/?get_group_doc=635%2F1526287152-2017AnnualReport-StanbicIBTCHoldingsPLC.pdf

## 2. Eligible N by outcome [comparison_eligible_n.csv]

| Outcome | v2 | v3 | Change | Pre v2→v3 | Post v2→v3 | Banks v2→v3 |
|---|---|---|---|---|---|---|
| Allowance / gross loans | 82 | 92 | +10 | 40→45 | 42→47 | 11→12 |
| Impairment / average assets | 73 | 87 | +14 | 35→44 | 38→43 | 12→12 |
| CAR | 75 | 84 | +9 | 37→41 | 38→43 | 11→12 |
| ROA | 78 | 94 | +16 | 39→48 | 39→46 | 12→12 |
| OCF / average assets | 72 | 84 | +12 | 36→41 | 36→43 | 11→12 |
| Equity / assets | 98 | 114 | +16 | 50→59 | 48→55 | 12→12 |
| Leverage | 98 | 114 | +16 | 50→59 | 48→55 | 12→12 |
| NPL ratio | 14 | 19 | +5 | 7→7 | 7→12 | 3→4 |
| Broad NPL coverage | 13 | 18 | +5 | 7→7 | 6→11 | 3→4 |
| Stage 3 coverage | 5 | 5 | +0 | 0→0 | 5→5 | 2→2 |
| Liquidity ratio | 10 | 10 | +0 | 5→5 | 5→5 | 3→3 |
| Going-concern uncertainty | 46 | 56 | +10 | 18→23 | 28→33 | 10→11 |

## 3. Principal model M1 (bank FE, IFRS9_D) [comparison_regression.csv]

| Outcome | Coef v2 | Coef v3 | Δ in v2 SE | p CR1 v2→v3 | p WCB v2→v3 | WCB decision change | CR1 decision change | Material |
|---|---|---|---|---|---|---|---|---|
| Allowance / gross loans | -0.908 | -0.397 | 0.28 | 0.635→0.815 | 0.880→0.951 | no | no | no |
| CAR | -2.784 | -2.590 | 0.09 | 0.247→0.209 | 0.206→0.150 | no | no | no |
| Equity / assets | -10.626 | -8.480 | 0.34 | 0.123→0.132 | 0.013→0.012 | no | no | no |
| Impairment / average assets | -0.882 | -1.112 | -0.41 | 0.144→0.031 | 0.080→0.011 | yes | yes | YES |
| Leverage | 10.626 | 8.480 | -0.34 | 0.123→0.132 | 0.013→0.012 | no | no | no |
| OCF / average assets | 7.332 | 6.577 | -0.42 | 0.002→0.003 | 0.017→0.010 | no | no | no |
| ROA | -0.042 | -0.062 | -0.13 | 0.798→0.699 | 0.800→0.699 | no | no | no |

## 4. Tier model M4 (bank + year FE, Tier1 x IFRS9_D) [comparison_regression.csv]

| Outcome | Coef v2 | Coef v3 | Δ in v2 SE | p CR1 v2→v3 | p WCB v2→v3 | WCB decision change | CR1 decision change | Material |
|---|---|---|---|---|---|---|---|---|
| Allowance / gross loans | 4.742 | 4.113 | -0.22 | 0.130→0.156 | 0.114→0.135 | no | no | no |
| CAR | 5.131 | 6.032 | 0.20 | 0.290→0.271 | 0.307→0.270 | no | no | no |
| Equity / assets | 12.837 | 8.914 | -0.37 | 0.256→0.312 | 0.282→0.362 | no | no | no |
| Impairment / average assets | 1.142 | 1.178 | 0.04 | 0.246→0.120 | 0.255→0.111 | no | no | no |
| Leverage | -12.837 | -8.914 | 0.37 | 0.256→0.312 | 0.282→0.362 | no | no | no |
| OCF / average assets | 3.887 | 3.609 | -0.08 | 0.285→0.311 | 0.285→0.320 | no | no | no |
| ROA | -0.437 | -0.480 | -0.16 | 0.138→0.055 | 0.160→0.055 | no | no | no |

## 5. Other specifications (M0, M2, M3, M4s, M5) flagged material [comparison_regression.csv]

All terms are listed, including controls (ln_assets, trend, Tier1 in M0).

- Allowance / gross loans M4s ln_assets: 12.720 → 9.639 (-0.78 prev SE); WCB p 0.306 → 0.547; CR1 p 0.009 → 0.095
- Equity / assets M4s ln_assets: 73.581 → 61.086 (-0.39 prev SE); WCB p 0.798 → 0.731; CR1 p 0.041 → 0.109
- Equity / assets M5 IFRS9_D: -16.096 → -11.716 (0.43 prev SE); WCB p 0.052 → 0.049; CR1 p 0.146 → 0.169
- Impairment / average assets M0 IFRS9_D: -1.022 → -1.110 (-0.16 prev SE); WCB p 0.024 → 0.011; CR1 p 0.085 → 0.032
- Impairment / average assets M2 IFRS9_D: -1.869 → -2.086 (-0.23 prev SE); WCB p 0.038 → 0.009; CR1 p 0.072 → 0.013
- Impairment / average assets M2 ln_assets: 1.617 → 1.666 (0.06 prev SE); WCB p 0.073 → 0.013; CR1 p 0.072 → 0.023
- Impairment / average assets M3 IFRS9_D: -1.196 → -1.510 (-0.77 prev SE); WCB p 0.011 → 0.002; CR1 p 0.013 → 0.002
- Impairment / average assets M4s ln_assets: 3.606 → 3.251 (-0.23 prev SE); WCB p 0.250 → 0.050; CR1 p 0.040 → 0.023
- Impairment / average assets M5 IFRS9_D: -1.379 → -1.531 (-0.16 prev SE); WCB p 0.184 → 0.043; CR1 p 0.174 → 0.040
- Leverage M4s ln_assets: -73.581 → -61.086 (0.39 prev SE); WCB p 0.798 → 0.731; CR1 p 0.041 → 0.109
- Leverage M5 IFRS9_D: 16.096 → 11.716 (-0.43 prev SE); WCB p 0.052 → 0.049; CR1 p 0.146 → 0.169
- OCF / average assets M0 IFRS9_D: 7.165 → 6.395 (-0.50 prev SE); WCB p 0.009 → 0.003; CR1 p 0.001 → 0.001
- OCF / average assets M3 trend: 0.035 → -0.111 (-0.22 prev SE); WCB p 0.958 → 0.864; CR1 p 0.959 → 0.861
- OCF / average assets M4s ln_assets: 7.976 → 8.791 (0.30 prev SE); WCB p 0.077 → 0.035; CR1 p 0.016 → 0.017
- ROA M0 IFRS9_D: 0.283 → 0.074 (-0.74 prev SE); WCB p 0.342 → 0.718; CR1 p 0.336 → 0.723
- ROA M3 trend: -0.176 → -0.179 (-0.03 prev SE); WCB p 0.049 → 0.014; CR1 p 0.108 → 0.049
- ROA M4s ln_assets: 1.679 → 1.819 (0.15 prev SE); WCB p 0.907 → 0.191; CR1 p 0.107 → 0.042

## 6. Sensitivity runs whose WCB decision or sign changed (sensitivities present in both releases) [comparison_robustness.csv]

- Impairment / average assets M1 S0_primary: coef -0.882 → -1.112; WCB p 0.080 → 0.011
- Impairment / average assets M1 S1_drop_fallback: coef -0.919 → -1.145; WCB p 0.089 → 0.011
- Impairment / average assets M1 S2_add_exception_rows: coef -1.140 → -1.304; WCB p 0.081 → 0.015
- Impairment / average assets M1 S3_drop_unity_negative_capital: coef -0.362 → -0.743; WCB p 0.157 → 0.020
- Impairment / average assets M1 S4_drop_2020: coef -1.011 → -1.220; WCB p 0.064 → 0.010
- Impairment / average assets M1 S5_drop_unity: coef -0.362 → -0.743; WCB p 0.156 → 0.020
- ROA M1 S4_drop_2020: coef 0.019 → -0.027; WCB p 0.913 → 0.878

New sensitivity in this release (no previous counterpart):
- Allowance / gross loans M1 S6_drop_holdco_rows: coef -0.397; WCB p 0.951; N 92
- Allowance / gross loans M4 S6_drop_holdco_rows: coef 4.113; WCB p 0.135; N 92
- CAR M1 S6_drop_holdco_rows: coef -2.590; WCB p 0.150; N 84
- CAR M4 S6_drop_holdco_rows: coef 6.032; WCB p 0.270; N 84
- Equity / assets M1 S6_drop_holdco_rows: coef -9.369; WCB p 0.014; N 108
- Equity / assets M4 S6_drop_holdco_rows: coef 10.747; WCB p 0.333; N 108
- Impairment / average assets M1 S6_drop_holdco_rows: coef -1.067; WCB p 0.024; N 83
- Impairment / average assets M4 S6_drop_holdco_rows: coef 1.189; WCB p 0.170; N 83
- Leverage M1 S6_drop_holdco_rows: coef 9.369; WCB p 0.014; N 108
- Leverage M4 S6_drop_holdco_rows: coef -10.747; WCB p 0.333; N 108
- OCF / average assets M1 S6_drop_holdco_rows: coef 6.583; WCB p 0.011; N 82
- OCF / average assets M4 S6_drop_holdco_rows: coef 3.799; WCB p 0.295; N 82
- ROA M1 S6_drop_holdco_rows: coef -0.066; WCB p 0.694; N 88
- ROA M4 S6_drop_holdco_rows: coef -0.217; WCB p 0.509; N 88

## 7. Hypothesis decisions by objective [comparison_interpretation.csv]

- O1 Allowance / gross loans: v2 'H0 not rejected at 5% (WCB)' → v3 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O1 Impairment / average assets: v2 'H0 not rejected at 5% (WCB)' → v3 'H0 rejected at 5% (WCB)' (CHANGED); robustness label changed ('robust: same sign in 6/6 sensitivities, WCB p < 0.05 in 6/6, jackknife sign changes 0')
- O2 CAR: v2 'H0 not rejected at 5% (WCB)' → v3 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O3 Equity / assets: v2 'H0 rejected at 5% (WCB); CR1 t(G-1) p = 0.123 gives the opposite decision' → v3 'H0 rejected at 5% (WCB); CR1 t(G-1) p = 0.132 gives the opposite decision' (unchanged); robustness label unchanged ('robust: same sign in 5/5 sensitivities, WCB p < 0.05 in 5/5, jackknife sign changes 0')
- O3 Leverage: v2 'H0 rejected at 5% (WCB); CR1 t(G-1) p = 0.123 gives the opposite decision' → v3 'H0 rejected at 5% (WCB); CR1 t(G-1) p = 0.132 gives the opposite decision' (unchanged); robustness label unchanged ('robust: same sign in 5/5 sensitivities, WCB p < 0.05 in 5/5, jackknife sign changes 0')
- O3 OCF / average assets: v2 'H0 rejected at 5% (WCB)' → v3 'H0 rejected at 5% (WCB)' (unchanged); robustness label unchanged ('robust: same sign in 5/5 sensitivities, WCB p < 0.05 in 5/5, jackknife sign changes 0')
- O3 ROA: v2 'H0 not rejected at 5% (WCB)' → v3 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O4 Going-concern uncertainty: v2 'not tested (3 events in one bank; a model would be unidentified/separation-prone)' → v3 'not tested (3 events in one bank; a model would be unidentified/separation-prone)' (unchanged); robustness label unchanged ('not applicable')
- O5 Allowance / gross loans: v2 'H0 not rejected at 5% (WCB)' → v3 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O5 CAR: v2 'H0 not rejected at 5% (WCB)' → v3 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O5 Equity / assets: v2 'H0 not rejected at 5% (WCB)' → v3 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O5 Impairment / average assets: v2 'H0 not rejected at 5% (WCB)' → v3 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O5 Leverage: v2 'H0 not rejected at 5% (WCB)' → v3 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O5 OCF / average assets: v2 'H0 not rejected at 5% (WCB)' → v3 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O5 ROA: v2 'H0 not rejected at 5% (WCB)' → v3 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O6 Allowance / gross loans: v2 'H0 not rejected (exploratory)' → v3 'H0 not rejected (exploratory)' (unchanged); robustness label unchanged ('exploratory')
- O6 CAR: v2 'H0 not rejected (exploratory)' → v3 'H0 not rejected (exploratory)' (unchanged); robustness label unchanged ('exploratory')
- O6 Impairment / average assets: v2 'H0 not rejected (exploratory)' → v3 'H0 rejected (exploratory)' (CHANGED); robustness label unchanged ('exploratory')
- O6 ROA: v2 'H0 not rejected (exploratory)' → v3 'H0 not rejected (exploratory)' (unchanged); robustness label unchanged ('exploratory')

## 8. Matched pre/post and volatility [comparison_matched_prepost.csv, comparison_volatility.csv]

- Matched Allowance / gross loans (All matched banks): banks 9→10; mean diff -0.992→-0.484; Wilcoxon p 0.570→0.375
- Matched Allowance / gross loans (Tier 1): banks 4→4; mean diff 1.654→1.829; Wilcoxon p n/a→n/a
- Matched Allowance / gross loans (Tier 2): banks 5→6; mean diff -3.109→-2.026; Wilcoxon p 0.625→1.000
- Matched CAR (All matched banks): banks 8→10; mean diff -3.904→-3.289; Wilcoxon p 0.195→0.105
- Matched CAR (Tier 1): banks 3→4; mean diff -0.023→0.061; Wilcoxon p n/a→n/a
- Matched CAR (Tier 2): banks 5→6; mean diff -6.233→-5.523; Wilcoxon p 0.188→0.094
- Matched Equity / assets (All matched banks): banks 9→11; mean diff -10.146→-8.396; Wilcoxon p 0.008→0.001
- Matched Equity / assets (Tier 1): banks 4→4; mean diff -2.708→-2.908; Wilcoxon p n/a→n/a
- Matched Equity / assets (Tier 2): banks 5→7; mean diff -16.096→-11.532; Wilcoxon p 0.062→0.016 (crosses 0.05)
- Matched Impairment / average assets (All matched banks): banks 9→11; mean diff -0.962→-1.190; Wilcoxon p 0.074→0.014 (crosses 0.05)
- Matched Impairment / average assets (Tier 1): banks 4→4; mean diff -0.248→-0.438; Wilcoxon p n/a→n/a
- Matched Impairment / average assets (Tier 2): banks 5→7; mean diff -1.533→-1.620; Wilcoxon p 0.312→0.078
- Matched Leverage (All matched banks): banks 9→11; mean diff 10.146→8.396; Wilcoxon p 0.008→0.001
- Matched Leverage (Tier 1): banks 4→4; mean diff 2.708→2.908; Wilcoxon p n/a→n/a
- Matched Leverage (Tier 2): banks 5→7; mean diff 16.096→11.532; Wilcoxon p 0.062→0.016 (crosses 0.05)
- Matched OCF / average assets (All matched banks): banks 9→10; mean diff 6.264→6.342; Wilcoxon p 0.020→0.010
- Matched OCF / average assets (Tier 1): banks 4→4; mean diff 6.995→8.477; Wilcoxon p n/a→n/a
- Matched OCF / average assets (Tier 2): banks 5→6; mean diff 5.679→4.919; Wilcoxon p 0.125→0.094
- Matched ROA (All matched banks): banks 9→11; mean diff 0.004→-0.035; Wilcoxon p 0.910→0.765
- Matched ROA (Tier 1): banks 4→4; mean diff -0.189→-0.368; Wilcoxon p n/a→n/a
- Matched ROA (Tier 2): banks 5→7; mean diff 0.158→0.155; Wilcoxon p 0.625→0.578
- Volatility Allowance / gross loans: banks 8→10; median SD ratio 1.19→1.30; Wilcoxon p 0.844→0.492
- Volatility CAR: banks 7→8; median SD ratio 0.77→0.78; Wilcoxon p 0.297→0.641
- Volatility Equity / assets: banks 9→11; median SD ratio 1.39→1.28; Wilcoxon p 0.359→0.175
- Volatility Impairment / average assets: banks 8→11; median SD ratio 0.34→0.33; Wilcoxon p 0.055→0.014 (crosses 0.05)
- Volatility Leverage: banks 9→11; median SD ratio 1.39→1.28; Wilcoxon p 0.359→0.175
- Volatility OCF / average assets: banks 7→9; median SD ratio 1.40→0.76; Wilcoxon p 0.688→0.734
- Volatility ROA: banks 8→11; median SD ratio 0.60→0.99; Wilcoxon p 0.383→0.638

## 9. Bank-level direction (matched post-minus-pre bank means) [comparison_bank_classification.csv]

- Direction reversed (increase <-> decrease): 4
  - GTBank eqta: increase (0.186) -> decrease (-0.615); n post 3->5, n pre 3->5
  - GTBank leverage: decrease (-0.186) -> increase (0.615); n post 3->5, n pre 3->5
  - GTBank ocf_ratio: decrease (-4.969) -> increase (0.956); n post 3->5, n pre 1->3
  - GTBank roa: increase (0.442) -> decrease (-0.276); n post 3->5, n pre 2->4
- Newly classifiable (bank now observed in both regimes): 12
  - Ecobank Nigeria allr: increase (3.394)
  - Ecobank Nigeria car: decrease (-1.973)
  - GTBank car: increase (0.315)
  - Ecobank Nigeria eqta: decrease (-0.097)
  - Stanbic eqta: decrease (-0.148)
  - Ecobank Nigeria impairment_assets: decrease (-2.143)
  - Stanbic impairment_assets: decrease (-1.533)
  - Ecobank Nigeria leverage: increase (0.097)
  - Stanbic leverage: increase (0.148)
  - Ecobank Nigeria ocf_ratio: increase (1.117)
  - Ecobank Nigeria roa: decrease (-0.567)
  - Stanbic roa: increase (0.863)
- No longer classifiable: 0
- Unchanged direction: 58 bank-outcome pairs

## 10. Going-concern events [comparison_going_concern.csv]

- Events 3 -> 3 (Unity 2019; Unity 2021; Unity 2022); coded bank-years 46 -> 56.

## 11. Summary

- Principal (M1) and tier (M4) estimates flagged material under the rule: 1 of 14 [comparison_regression.csv].
- Objective-level H0 decisions changed: 2 of 19 [comparison_interpretation.csv].
- Bank direction reversals: 4; newly classified bank-outcome pairs: 12 [comparison_bank_classification.csv].
