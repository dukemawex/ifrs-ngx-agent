# Comparison: release v3 vs v4 (current)

v3: `IFRS9_release_2026-10-11_v3`, results in `thesis_results_v3/`. v4: `IFRS9_release_2026-10-11_v4`, results in `thesis_results/`. Same code, estimators, seed and B = 9,999. Every number below is read from the comparison_*.csv files named in brackets.

Material-change rule (set before comparing): the 5% decision changes under WCB or CR1, the sign changes, or the coefficient moves by at least 0.5 previous CR1 standard errors.

## 1. Rows added [comparison_rows_added.csv]

- added: Stanbic 2014 (Tier 2); Stanbic IBTC Holdings 2014 annual report: audited HoldCo package - explicit operating-bank subsidiary disclosure (note 13.4, Stanbic IBTC Bank PLC); source https://thevault.exchange/?get_group_doc=18/1447238694-StanbicIBTCFY14Annualreport.pdf

## 2. Eligible N by outcome [comparison_eligible_n.csv]

| Outcome | v3 | v4 | Change | Pre v3→v4 | Post v3→v4 | Banks v3→v4 |
|---|---|---|---|---|---|---|
| Allowance / gross loans | 92 | 92 | +0 | 45→45 | 47→47 | 12→12 |
| Impairment / average assets | 87 | 88 | +1 | 44→45 | 43→43 | 12→12 |
| CAR | 84 | 84 | +0 | 41→41 | 43→43 | 12→12 |
| ROA | 94 | 95 | +1 | 48→49 | 46→46 | 12→12 |
| OCF / average assets | 84 | 84 | +0 | 41→41 | 43→43 | 12→12 |
| Equity / assets | 114 | 115 | +1 | 59→60 | 55→55 | 12→12 |
| Leverage | 114 | 115 | +1 | 59→60 | 55→55 | 12→12 |
| NPL ratio | 19 | 19 | +0 | 7→7 | 12→12 | 4→4 |
| Broad NPL coverage | 18 | 18 | +0 | 7→7 | 11→11 | 4→4 |
| Stage 3 coverage | 5 | 5 | +0 | 0→0 | 5→5 | 2→2 |
| Liquidity ratio | 10 | 10 | +0 | 5→5 | 5→5 | 3→3 |
| Going-concern uncertainty | 56 | 56 | +0 | 23→23 | 33→33 | 11→11 |

## 3. Principal model M1 (bank FE, IFRS9_D) [comparison_regression.csv]

| Outcome | Coef v3 | Coef v4 | Δ in v3 SE | p CR1 v3→v4 | p WCB v3→v4 | WCB decision change | CR1 decision change | Material |
|---|---|---|---|---|---|---|---|---|
| Allowance / gross loans | -0.397 | -0.397 | 0.00 | 0.815→0.815 | 0.951→0.951 | no | no | no |
| CAR | -2.590 | -2.590 | 0.00 | 0.209→0.209 | 0.150→0.150 | no | no | no |
| Equity / assets | -8.480 | -8.370 | 0.02 | 0.132→0.134 | 0.012→0.012 | no | no | no |
| Impairment / average assets | -1.112 | -1.091 | 0.05 | 0.031→0.032 | 0.011→0.011 | no | no | no |
| Leverage | 8.480 | 8.370 | -0.02 | 0.132→0.134 | 0.012→0.012 | no | no | no |
| OCF / average assets | 6.577 | 6.577 | 0.00 | 0.003→0.003 | 0.010→0.010 | no | no | no |
| ROA | -0.062 | -0.069 | -0.04 | 0.699→0.656 | 0.699→0.657 | no | no | no |

## 4. Tier model M4 (bank + year FE, Tier1 x IFRS9_D) [comparison_regression.csv]

| Outcome | Coef v3 | Coef v4 | Δ in v3 SE | p CR1 v3→v4 | p WCB v3→v4 | WCB decision change | CR1 decision change | Material |
|---|---|---|---|---|---|---|---|---|
| Allowance / gross loans | 4.113 | 4.113 | 0.00 | 0.156→0.156 | 0.135→0.135 | no | no | no |
| CAR | 6.032 | 6.032 | 0.00 | 0.271→0.271 | 0.270→0.270 | no | no | no |
| Equity / assets | 8.914 | 8.582 | -0.04 | 0.312→0.320 | 0.362→0.373 | no | no | no |
| Impairment / average assets | 1.178 | 1.161 | -0.02 | 0.120→0.122 | 0.111→0.111 | no | no | no |
| Leverage | -8.914 | -8.582 | 0.04 | 0.312→0.320 | 0.362→0.373 | no | no | no |
| OCF / average assets | 3.609 | 3.609 | 0.00 | 0.311→0.311 | 0.320→0.320 | no | no | no |
| ROA | -0.480 | -0.488 | -0.04 | 0.055→0.055 | 0.055→0.056 | no | no | no |

## 5. Other specifications (M0, M2, M3, M4s, M5) flagged material [comparison_regression.csv]

All terms are listed, including controls (ln_assets, trend, Tier1 in M0).

- Equity / assets M5 IFRS9_D: -11.716 → -11.490 (0.03 prev SE); WCB p 0.049 → 0.052; CR1 p 0.169 → 0.173
- Impairment / average assets M4s ln_assets: 3.251 → 3.252 (0.00 prev SE); WCB p 0.050 → 0.050; CR1 p 0.023 → 0.021
- Leverage M5 IFRS9_D: 11.716 → 11.490 (-0.03 prev SE); WCB p 0.049 → 0.052; CR1 p 0.169 → 0.173

## 6. Sensitivity runs whose WCB decision or sign changed (sensitivities present in both releases) [comparison_robustness.csv]

- none

New sensitivity in this release (no previous counterpart):
- none

## 7. Hypothesis decisions by objective [comparison_interpretation.csv]

- O1 Allowance / gross loans: v3 'H0 not rejected at 5% (WCB)' → v4 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O1 Impairment / average assets: v3 'H0 rejected at 5% (WCB)' → v4 'H0 rejected at 5% (WCB)' (unchanged); robustness label unchanged ('robust: same sign in 6/6 sensitivities, WCB p < 0.05 in 6/6, jackknife sign changes 0')
- O2 CAR: v3 'H0 not rejected at 5% (WCB)' → v4 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O3 Equity / assets: v3 'H0 rejected at 5% (WCB); CR1 t(G-1) p = 0.132 gives the opposite decision' → v4 'H0 rejected at 5% (WCB); CR1 t(G-1) p = 0.134 gives the opposite decision' (unchanged); robustness label unchanged ('robust: same sign in 5/5 sensitivities, WCB p < 0.05 in 5/5, jackknife sign changes 0')
- O3 Leverage: v3 'H0 rejected at 5% (WCB); CR1 t(G-1) p = 0.132 gives the opposite decision' → v4 'H0 rejected at 5% (WCB); CR1 t(G-1) p = 0.134 gives the opposite decision' (unchanged); robustness label unchanged ('robust: same sign in 5/5 sensitivities, WCB p < 0.05 in 5/5, jackknife sign changes 0')
- O3 OCF / average assets: v3 'H0 rejected at 5% (WCB)' → v4 'H0 rejected at 5% (WCB)' (unchanged); robustness label unchanged ('robust: same sign in 5/5 sensitivities, WCB p < 0.05 in 5/5, jackknife sign changes 0')
- O3 ROA: v3 'H0 not rejected at 5% (WCB)' → v4 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O4 Going-concern uncertainty: v3 'not tested (3 events in one bank; a model would be unidentified/separation-prone)' → v4 'not tested (3 events in one bank; a model would be unidentified/separation-prone)' (unchanged); robustness label unchanged ('not applicable')
- O5 Allowance / gross loans: v3 'H0 not rejected at 5% (WCB)' → v4 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O5 CAR: v3 'H0 not rejected at 5% (WCB)' → v4 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O5 Equity / assets: v3 'H0 not rejected at 5% (WCB)' → v4 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O5 Impairment / average assets: v3 'H0 not rejected at 5% (WCB)' → v4 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O5 Leverage: v3 'H0 not rejected at 5% (WCB)' → v4 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O5 OCF / average assets: v3 'H0 not rejected at 5% (WCB)' → v4 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O5 ROA: v3 'H0 not rejected at 5% (WCB)' → v4 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O6 Allowance / gross loans: v3 'H0 not rejected (exploratory)' → v4 'H0 not rejected (exploratory)' (unchanged); robustness label unchanged ('exploratory')
- O6 CAR: v3 'H0 not rejected (exploratory)' → v4 'H0 not rejected (exploratory)' (unchanged); robustness label unchanged ('exploratory')
- O6 Impairment / average assets: v3 'H0 rejected (exploratory)' → v4 'H0 rejected (exploratory)' (unchanged); robustness label unchanged ('exploratory')
- O6 ROA: v3 'H0 not rejected (exploratory)' → v4 'H0 not rejected (exploratory)' (unchanged); robustness label unchanged ('exploratory')

## 8. Matched pre/post and volatility [comparison_matched_prepost.csv, comparison_volatility.csv]

- Matched Allowance / gross loans (All matched banks): banks 10→10; mean diff -0.484→-0.484; Wilcoxon p 0.375→0.375
- Matched Allowance / gross loans (Tier 1): banks 4→4; mean diff 1.829→1.829; Wilcoxon p n/a→n/a
- Matched Allowance / gross loans (Tier 2): banks 6→6; mean diff -2.026→-2.026; Wilcoxon p 1.000→1.000
- Matched CAR (All matched banks): banks 10→10; mean diff -3.289→-3.289; Wilcoxon p 0.105→0.105
- Matched CAR (Tier 1): banks 4→4; mean diff 0.061→0.061; Wilcoxon p n/a→n/a
- Matched CAR (Tier 2): banks 6→6; mean diff -5.523→-5.523; Wilcoxon p 0.094→0.094
- Matched Equity / assets (All matched banks): banks 11→11; mean diff -8.396→-8.370; Wilcoxon p 0.001→0.003
- Matched Equity / assets (Tier 1): banks 4→4; mean diff -2.908→-2.908; Wilcoxon p n/a→n/a
- Matched Equity / assets (Tier 2): banks 7→7; mean diff -11.532→-11.490; Wilcoxon p 0.016→0.047
- Matched Impairment / average assets (All matched banks): banks 11→11; mean diff -1.190→-1.169; Wilcoxon p 0.014→0.014
- Matched Impairment / average assets (Tier 1): banks 4→4; mean diff -0.438→-0.438; Wilcoxon p n/a→n/a
- Matched Impairment / average assets (Tier 2): banks 7→7; mean diff -1.620→-1.586; Wilcoxon p 0.078→0.078
- Matched Leverage (All matched banks): banks 11→11; mean diff 8.396→8.370; Wilcoxon p 0.001→0.003
- Matched Leverage (Tier 1): banks 4→4; mean diff 2.908→2.908; Wilcoxon p n/a→n/a
- Matched Leverage (Tier 2): banks 7→7; mean diff 11.532→11.490; Wilcoxon p 0.016→0.047
- Matched OCF / average assets (All matched banks): banks 10→10; mean diff 6.342→6.342; Wilcoxon p 0.010→0.010
- Matched OCF / average assets (Tier 1): banks 4→4; mean diff 8.477→8.477; Wilcoxon p n/a→n/a
- Matched OCF / average assets (Tier 2): banks 6→6; mean diff 4.919→4.919; Wilcoxon p 0.094→0.094
- Matched ROA (All matched banks): banks 11→11; mean diff -0.035→-0.050; Wilcoxon p 0.765→0.700
- Matched ROA (Tier 1): banks 4→4; mean diff -0.368→-0.368; Wilcoxon p n/a→n/a
- Matched ROA (Tier 2): banks 7→7; mean diff 0.155→0.132; Wilcoxon p 0.578→0.578
- Volatility Allowance / gross loans: banks 10→10; median SD ratio 1.30→1.30; Wilcoxon p 0.492→0.492
- Volatility CAR: banks 8→8; median SD ratio 0.78→0.78; Wilcoxon p 0.641→0.641
- Volatility Equity / assets: banks 11→11; median SD ratio 1.28→1.28; Wilcoxon p 0.175→0.278
- Volatility Impairment / average assets: banks 11→11; median SD ratio 0.33→0.33; Wilcoxon p 0.014→0.014
- Volatility Leverage: banks 11→11; median SD ratio 1.28→1.28; Wilcoxon p 0.175→0.278
- Volatility OCF / average assets: banks 9→9; median SD ratio 0.76→0.76; Wilcoxon p 0.734→0.734
- Volatility ROA: banks 11→11; median SD ratio 0.99→0.99; Wilcoxon p 0.638→0.638

## 9. Bank-level direction (matched post-minus-pre bank means) [comparison_bank_classification.csv]

- Direction reversed (increase <-> decrease): 2
  - Stanbic eqta: decrease (-0.148) -> increase (0.146); n post 5->5, n pre 4->5
  - Stanbic leverage: increase (0.148) -> decrease (-0.146); n post 5->5, n pre 4->5
- Newly classifiable (bank now observed in both regimes): 0
- No longer classifiable: 0
- Unchanged direction: 72 bank-outcome pairs

## 10. Going-concern events [comparison_going_concern.csv]

- Events 3 -> 3 (Unity 2019; Unity 2021; Unity 2022); coded bank-years 56 -> 56.

## 11. Summary

- Principal (M1) and tier (M4) estimates flagged material under the rule: 0 of 14 [comparison_regression.csv].
- Objective-level H0 decisions changed: 0 of 19 [comparison_interpretation.csv].
- Bank direction reversals: 2; newly classified bank-outcome pairs: 0 [comparison_bank_classification.csv].
