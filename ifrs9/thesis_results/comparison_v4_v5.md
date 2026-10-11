# Comparison: release v4 vs v5 (current)

v4: `IFRS9_release_2026-10-11_v4`, results in `thesis_results_v4/`. v5: `IFRS9_release_2026-10-11_v5`, results in `thesis_results/`. Same code, estimators, seed and B = 9,999. Every number below is read from the comparison_*.csv files named in brackets.

Material-change rule (set before comparing): the 5% decision changes under WCB or CR1, the sign changes, or the coefficient moves by at least 0.5 previous CR1 standard errors.

## 1. Rows added [comparison_rows_added.csv]

- added: First Bank 2018 (Tier 1); FY2018 financial statements, as originally reported (reproduced in FBN Finance prospectus); source https://ise-prodnr-eu-west-1-data-integration.s3-eu-west-1.amazonaws.com/legacy/Prospectus+-+Standalone_bccce739-ac65-4a0d-82bc-7ef4406d2573.PDF
- added: First Bank 2019 (Tier 1); FY2019 financial statements, as originally reported (reproduced in FBN Finance prospectus); source https://ise-prodnr-eu-west-1-data-integration.s3-eu-west-1.amazonaws.com/legacy/Prospectus+-+Standalone_bccce739-ac65-4a0d-82bc-7ef4406d2573.PDF
- added: First Bank 2022 (Tier 1); FY2023 audited summary financial statements, 2022 comparative (later-year presentation; not the 2022 annual report); source https://cdn.businessday.ng/wp-content/uploads/2024/05/BD_20240529.pdf

## 2. Eligible N by outcome [comparison_eligible_n.csv]

| Outcome | v4 | v5 | Change | Pre v4→v5 | Post v4→v5 | Banks v4→v5 |
|---|---|---|---|---|---|---|
| Allowance / gross loans | 92 | 93 | +1 | 45→45 | 47→48 | 12→12 |
| Impairment / average assets | 88 | 90 | +2 | 45→45 | 43→45 | 12→12 |
| CAR | 84 | 86 | +2 | 41→41 | 43→45 | 12→12 |
| ROA | 95 | 97 | +2 | 49→49 | 46→48 | 12→12 |
| OCF / average assets | 84 | 86 | +2 | 41→41 | 43→45 | 12→12 |
| Equity / assets | 115 | 118 | +3 | 60→60 | 55→58 | 12→12 |
| Leverage | 115 | 118 | +3 | 60→60 | 55→58 | 12→12 |
| NPL ratio | 19 | 19 | +0 | 7→7 | 12→12 | 4→4 |
| Broad NPL coverage | 18 | 18 | +0 | 7→7 | 11→11 | 4→4 |
| Stage 3 coverage | 5 | 5 | +0 | 0→0 | 5→5 | 2→2 |
| Liquidity ratio | 10 | 10 | +0 | 5→5 | 5→5 | 3→3 |
| Going-concern uncertainty | 56 | 58 | +2 | 23→23 | 33→35 | 11→11 |

## 3. Principal model M1 (bank FE, IFRS9_D) [comparison_regression.csv]

| Outcome | Coef v4 | Coef v5 | Δ in v4 SE | p CR1 v4→v5 | p WCB v4→v5 | WCB decision change | CR1 decision change | Material |
|---|---|---|---|---|---|---|---|---|
| Allowance / gross loans | -0.397 | -0.517 | -0.07 | 0.815→0.752 | 0.951→0.916 | no | no | no |
| CAR | -2.590 | -2.797 | -0.11 | 0.209→0.153 | 0.150→0.082 | no | no | no |
| Equity / assets | -8.370 | -7.995 | 0.07 | 0.134→0.128 | 0.012→0.009 | no | no | no |
| Impairment / average assets | -1.091 | -1.075 | 0.04 | 0.032→0.028 | 0.011→0.008 | no | no | no |
| Leverage | 8.370 | 7.995 | -0.07 | 0.134→0.128 | 0.012→0.009 | no | no | no |
| OCF / average assets | 6.577 | 6.347 | -0.14 | 0.003→0.002 | 0.010→0.008 | no | no | no |
| ROA | -0.069 | -0.064 | 0.03 | 0.656→0.664 | 0.657→0.665 | no | no | no |

## 4. Tier model M4 (bank + year FE, Tier1 x IFRS9_D) [comparison_regression.csv]

| Outcome | Coef v4 | Coef v5 | Δ in v4 SE | p CR1 v4→v5 | p WCB v4→v5 | WCB decision change | CR1 decision change | Material |
|---|---|---|---|---|---|---|---|---|
| Allowance / gross loans | 4.113 | 3.566 | -0.20 | 0.156→0.216 | 0.135→0.217 | no | no | no |
| CAR | 6.032 | 6.431 | 0.08 | 0.271→0.328 | 0.270→0.369 | no | no | no |
| Equity / assets | 8.582 | 8.839 | 0.03 | 0.320→0.318 | 0.373→0.369 | no | no | no |
| Impairment / average assets | 1.161 | 1.075 | -0.12 | 0.122→0.146 | 0.111→0.133 | no | no | no |
| Leverage | -8.582 | -8.839 | -0.03 | 0.320→0.318 | 0.373→0.369 | no | no | no |
| OCF / average assets | 3.609 | 2.610 | -0.29 | 0.311→0.450 | 0.320→0.456 | no | no | no |
| ROA | -0.488 | -0.482 | 0.03 | 0.055→0.059 | 0.056→0.059 | no | no | no |

## 5. Other specifications (M0, M2, M3, M4s, M5) flagged material [comparison_regression.csv]

All terms are listed, including controls (ln_assets, trend, Tier1 in M0).

- Equity / assets M3 trend: -0.675 → -0.684 (-0.02 prev SE); WCB p 0.063 → 0.033; CR1 p 0.212 → 0.200
- Equity / assets M4s Tier1_x_IFRS9_D: -1.694 → 0.878 (0.27 prev SE); WCB p 0.861 → 0.916; CR1 p 0.861 → 0.917
- Impairment / average assets M4s ln_assets: 3.252 → 3.238 (-0.01 prev SE); WCB p 0.050 → 0.039; CR1 p 0.021 → 0.021
- Leverage M3 trend: 0.675 → 0.684 (0.02 prev SE); WCB p 0.063 → 0.033; CR1 p 0.212 → 0.200
- Leverage M4s Tier1_x_IFRS9_D: 1.694 → -0.878 (-0.27 prev SE); WCB p 0.861 → 0.916; CR1 p 0.861 → 0.917
- OCF / average assets M2 IFRS9_D: 4.756 → 4.586 (-0.08 prev SE); WCB p 0.033 → 0.020; CR1 p 0.058 → 0.045
- ROA M0 IFRS9_D: 0.046 → -0.014 (-0.32 prev SE); WCB p 0.813 → 0.929; CR1 p 0.814 → 0.926

## 6. Sensitivity runs whose WCB decision or sign changed (sensitivities present in both releases) [comparison_robustness.csv]

- none

New sensitivity in this release (no previous counterpart):
- none

## 7. Hypothesis decisions by objective [comparison_interpretation.csv]

- O1 Allowance / gross loans: v4 'H0 not rejected at 5% (WCB)' → v5 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O1 Impairment / average assets: v4 'H0 rejected at 5% (WCB)' → v5 'H0 rejected at 5% (WCB)' (unchanged); robustness label unchanged ('robust: same sign in 6/6 sensitivities, WCB p < 0.05 in 6/6, jackknife sign changes 0')
- O2 CAR: v4 'H0 not rejected at 5% (WCB)' → v5 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O3 Equity / assets: v4 'H0 rejected at 5% (WCB); CR1 t(G-1) p = 0.134 gives the opposite decision' → v5 'H0 rejected at 5% (WCB); CR1 t(G-1) p = 0.128 gives the opposite decision' (unchanged); robustness label unchanged ('robust: same sign in 5/5 sensitivities, WCB p < 0.05 in 5/5, jackknife sign changes 0')
- O3 Leverage: v4 'H0 rejected at 5% (WCB); CR1 t(G-1) p = 0.134 gives the opposite decision' → v5 'H0 rejected at 5% (WCB); CR1 t(G-1) p = 0.128 gives the opposite decision' (unchanged); robustness label unchanged ('robust: same sign in 5/5 sensitivities, WCB p < 0.05 in 5/5, jackknife sign changes 0')
- O3 OCF / average assets: v4 'H0 rejected at 5% (WCB)' → v5 'H0 rejected at 5% (WCB)' (unchanged); robustness label unchanged ('robust: same sign in 5/5 sensitivities, WCB p < 0.05 in 5/5, jackknife sign changes 0')
- O3 ROA: v4 'H0 not rejected at 5% (WCB)' → v5 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O4 Going-concern uncertainty: v4 'not tested (3 events in one bank; a model would be unidentified/separation-prone)' → v5 'not tested (3 events in one bank; a model would be unidentified/separation-prone)' (unchanged); robustness label unchanged ('not applicable')
- O5 Allowance / gross loans: v4 'H0 not rejected at 5% (WCB)' → v5 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O5 CAR: v4 'H0 not rejected at 5% (WCB)' → v5 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O5 Equity / assets: v4 'H0 not rejected at 5% (WCB)' → v5 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O5 Impairment / average assets: v4 'H0 not rejected at 5% (WCB)' → v5 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O5 Leverage: v4 'H0 not rejected at 5% (WCB)' → v5 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O5 OCF / average assets: v4 'H0 not rejected at 5% (WCB)' → v5 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O5 ROA: v4 'H0 not rejected at 5% (WCB)' → v5 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O6 Allowance / gross loans: v4 'H0 not rejected (exploratory)' → v5 'H0 not rejected (exploratory)' (unchanged); robustness label unchanged ('exploratory')
- O6 CAR: v4 'H0 not rejected (exploratory)' → v5 'H0 not rejected (exploratory)' (unchanged); robustness label unchanged ('exploratory')
- O6 Impairment / average assets: v4 'H0 rejected (exploratory)' → v5 'H0 rejected (exploratory)' (unchanged); robustness label unchanged ('exploratory')
- O6 ROA: v4 'H0 not rejected (exploratory)' → v5 'H0 not rejected (exploratory)' (unchanged); robustness label unchanged ('exploratory')

## 8. Matched pre/post and volatility [comparison_matched_prepost.csv, comparison_volatility.csv]

- Matched Allowance / gross loans (All matched banks): banks 10→11; mean diff -0.484→-0.754; Wilcoxon p 0.375→0.765
- Matched Allowance / gross loans (Tier 1): banks 4→5; mean diff 1.829→0.771; Wilcoxon p n/a→0.625
- Matched Allowance / gross loans (Tier 2): banks 6→6; mean diff -2.026→-2.026; Wilcoxon p 1.000→1.000
- Matched CAR (All matched banks): banks 10→11; mean diff -3.289→-3.488; Wilcoxon p 0.105→0.054
- Matched CAR (Tier 1): banks 4→5; mean diff 0.061→-1.046; Wilcoxon p n/a→0.625
- Matched CAR (Tier 2): banks 6→6; mean diff -5.523→-5.523; Wilcoxon p 0.094→0.094
- Matched Equity / assets (All matched banks): banks 11→12; mean diff -8.370→-7.881; Wilcoxon p 0.003→0.001
- Matched Equity / assets (Tier 1): banks 4→5; mean diff -2.908→-2.827; Wilcoxon p n/a→0.062
- Matched Equity / assets (Tier 2): banks 7→7; mean diff -11.490→-11.490; Wilcoxon p 0.047→0.047
- Matched Impairment / average assets (All matched banks): banks 11→12; mean diff -1.169→-1.132; Wilcoxon p 0.014→0.009
- Matched Impairment / average assets (Tier 1): banks 4→5; mean diff -0.438→-0.497; Wilcoxon p n/a→0.062
- Matched Impairment / average assets (Tier 2): banks 7→7; mean diff -1.586→-1.586; Wilcoxon p 0.078→0.078
- Matched Leverage (All matched banks): banks 11→12; mean diff 8.370→7.881; Wilcoxon p 0.003→0.001
- Matched Leverage (Tier 1): banks 4→5; mean diff 2.908→2.827; Wilcoxon p n/a→0.062
- Matched Leverage (Tier 2): banks 7→7; mean diff 11.490→11.490; Wilcoxon p 0.047→0.047
- Matched OCF / average assets (All matched banks): banks 10→11; mean diff 6.342→6.010; Wilcoxon p 0.010→0.007
- Matched OCF / average assets (Tier 1): banks 4→5; mean diff 8.477→7.319; Wilcoxon p n/a→0.062
- Matched OCF / average assets (Tier 2): banks 6→6; mean diff 4.919→4.919; Wilcoxon p 0.094→0.094
- Matched ROA (All matched banks): banks 11→12; mean diff -0.050→-0.043; Wilcoxon p 0.700→0.791
- Matched ROA (Tier 1): banks 4→5; mean diff -0.368→-0.289; Wilcoxon p n/a→0.312
- Matched ROA (Tier 2): banks 7→7; mean diff 0.132→0.132; Wilcoxon p 0.578→0.578
- Volatility Allowance / gross loans: banks 10→10; median SD ratio 1.30→1.30; Wilcoxon p 0.492→0.492
- Volatility CAR: banks 8→8; median SD ratio 0.78→0.78; Wilcoxon p 0.641→0.641
- Volatility Equity / assets: banks 11→12; median SD ratio 1.28→1.13; Wilcoxon p 0.278→0.424
- Volatility Impairment / average assets: banks 11→11; median SD ratio 0.33→0.33; Wilcoxon p 0.014→0.014
- Volatility Leverage: banks 11→12; median SD ratio 1.28→1.13; Wilcoxon p 0.278→0.424
- Volatility OCF / average assets: banks 9→9; median SD ratio 0.76→0.76; Wilcoxon p 0.734→0.734
- Volatility ROA: banks 11→11; median SD ratio 0.99→0.99; Wilcoxon p 0.638→0.638

## 9. Bank-level direction (matched post-minus-pre bank means) [comparison_bank_classification.csv]

- Direction reversed (increase <-> decrease): 0
- Newly classifiable (bank now observed in both regimes): 7
  - First Bank allr: decrease (-3.460)
  - First Bank car: decrease (-5.476)
  - First Bank eqta: decrease (-2.504)
  - First Bank impairment_assets: decrease (-0.734)
  - First Bank leverage: increase (2.504)
  - First Bank ocf_ratio: increase (2.686)
  - First Bank roa: increase (0.029)
- No longer classifiable: 0
- Unchanged direction: 74 bank-outcome pairs

## 10. Going-concern events [comparison_going_concern.csv]

- Events 3 -> 3 (Unity 2019; Unity 2021; Unity 2022); coded bank-years 56 -> 58.

## 11. Summary

- Principal (M1) and tier (M4) estimates flagged material under the rule: 0 of 14 [comparison_regression.csv].
- Objective-level H0 decisions changed: 0 of 19 [comparison_interpretation.csv].
- Bank direction reversals: 0; newly classified bank-outcome pairs: 7 [comparison_bank_classification.csv].
