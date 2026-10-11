# Comparison: release v1 (97 bank-years) vs v2 (current)

v1: `IFRS9_release_2026-10-11_v1`, results in `thesis_results_v1/`. v2: `IFRS9_release_2026-10-11_v2`, results in `thesis_results/`. Same code, estimators, seed and B = 9,999. Every number below is read from the comparison_*.csv files named in brackets.

Material-change rule (set before comparing): the 5% decision changes under WCB or CR1, the sign changes, or the coefficient moves by at least 0.5 v1 CR1 standard errors.

## 1. Rows added [comparison_rows_added.csv]

- added: Access 2022 (Tier 1); 2022 financial statements, as originally reported; source https://www.accessbankplc.com/access/media/Media-PDF-Attachment/2022-FY-Financial-Statement.pdf?ext=.pdf

## 2. Eligible N by outcome [comparison_eligible_n.csv]

| Outcome | v1 | v2 | Change | Pre v1→v2 | Post v1→v2 | Banks v1→v2 |
|---|---|---|---|---|---|---|
| Allowance / gross loans | 81 | 82 | +1 | 40→40 | 41→42 | 11→11 |
| Impairment / average assets | 72 | 73 | +1 | 35→35 | 37→38 | 12→12 |
| CAR | 74 | 75 | +1 | 37→37 | 37→38 | 11→11 |
| ROA | 77 | 78 | +1 | 39→39 | 38→39 | 12→12 |
| OCF / average assets | 71 | 72 | +1 | 36→36 | 35→36 | 11→11 |
| Equity / assets | 97 | 98 | +1 | 50→50 | 47→48 | 12→12 |
| Leverage | 97 | 98 | +1 | 50→50 | 47→48 | 12→12 |
| NPL ratio | 14 | 14 | +0 | 7→7 | 7→7 | 3→3 |
| Broad NPL coverage | 13 | 13 | +0 | 7→7 | 6→6 | 3→3 |
| Stage 3 coverage | 5 | 5 | +0 | 0→0 | 5→5 | 2→2 |
| Liquidity ratio | 10 | 10 | +0 | 5→5 | 5→5 | 3→3 |
| Going-concern uncertainty | 46 | 46 | +0 | 18→18 | 28→28 | 10→10 |

## 3. Principal model M1 (bank FE, IFRS9_D) [comparison_regression.csv]

| Outcome | Coef v1 | Coef v2 | Δ in v1 SE | p CR1 v1→v2 | p WCB v1→v2 | WCB decision change | CR1 decision change | Material |
|---|---|---|---|---|---|---|---|---|
| Allowance / gross loans | -0.874 | -0.908 | -0.02 | 0.652→0.635 | 0.889→0.880 | no | no | no |
| CAR | -2.816 | -2.784 | 0.01 | 0.250→0.247 | 0.213→0.206 | no | no | no |
| Equity / assets | -10.685 | -10.626 | 0.01 | 0.125→0.123 | 0.013→0.013 | no | no | no |
| Impairment / average assets | -0.913 | -0.882 | 0.05 | 0.135→0.144 | 0.070→0.080 | no | no | no |
| Leverage | 10.685 | 10.626 | -0.01 | 0.125→0.123 | 0.013→0.013 | no | no | no |
| OCF / average assets | 7.336 | 7.332 | -0.00 | 0.003→0.002 | 0.017→0.017 | no | no | no |
| ROA | -0.033 | -0.042 | -0.05 | 0.835→0.798 | 0.837→0.800 | no | no | no |

## 4. Tier model M4 (bank + year FE, Tier1 x IFRS9_D) [comparison_regression.csv]

| Outcome | Coef v1 | Coef v2 | Δ in v1 SE | p CR1 v1→v2 | p WCB v1→v2 | WCB decision change | CR1 decision change | Material |
|---|---|---|---|---|---|---|---|---|
| Allowance / gross loans | 4.832 | 4.742 | -0.03 | 0.123→0.130 | 0.110→0.114 | no | no | no |
| CAR | 5.576 | 5.131 | -0.09 | 0.273→0.290 | 0.304→0.307 | no | no | no |
| Equity / assets | 13.059 | 12.837 | -0.02 | 0.257→0.256 | 0.284→0.282 | no | no | no |
| Impairment / average assets | 1.081 | 1.142 | 0.07 | 0.262→0.246 | 0.286→0.255 | no | no | no |
| Leverage | -13.059 | -12.837 | 0.02 | 0.257→0.256 | 0.284→0.282 | no | no | no |
| OCF / average assets | 4.084 | 3.887 | -0.05 | 0.281→0.285 | 0.284→0.285 | no | no | no |
| ROA | -0.433 | -0.437 | -0.02 | 0.146→0.138 | 0.160→0.160 | no | no | no |

## 5. Other specifications (M0, M2, M3, M4s, M5) flagged material [comparison_regression.csv]

All terms are listed, including controls (ln_assets, trend, Tier1 in M0).

- ROA M3 trend: -0.177 → -0.176 (0.01 v1 SE); WCB p 0.057 → 0.049; CR1 p 0.113 → 0.108

## 6. Sensitivity runs whose WCB decision or sign changed [comparison_robustness.csv]

- none

## 7. Hypothesis decisions by objective [comparison_interpretation.csv]

- O1 Allowance / gross loans: v1 'H0 not rejected at 5% (WCB)' → v2 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O1 Impairment / average assets: v1 'H0 not rejected at 5% (WCB)' → v2 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O2 CAR: v1 'H0 not rejected at 5% (WCB)' → v2 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O3 Equity / assets: v1 'H0 rejected at 5% (WCB); CR1 t(G-1) p = 0.125 gives the opposite decision' → v2 'H0 rejected at 5% (WCB); CR1 t(G-1) p = 0.123 gives the opposite decision' (unchanged); robustness label unchanged ('robust: same sign in 4/4 sensitivities, WCB p < 0.05 in 4/4, jackknife sign changes 0')
- O3 Leverage: v1 'H0 rejected at 5% (WCB); CR1 t(G-1) p = 0.125 gives the opposite decision' → v2 'H0 rejected at 5% (WCB); CR1 t(G-1) p = 0.123 gives the opposite decision' (unchanged); robustness label unchanged ('robust: same sign in 4/4 sensitivities, WCB p < 0.05 in 4/4, jackknife sign changes 0')
- O3 OCF / average assets: v1 'H0 rejected at 5% (WCB)' → v2 'H0 rejected at 5% (WCB)' (unchanged); robustness label unchanged ('robust: same sign in 4/4 sensitivities, WCB p < 0.05 in 4/4, jackknife sign changes 0')
- O3 ROA: v1 'H0 not rejected at 5% (WCB)' → v2 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O4 Going-concern uncertainty: v1 'not tested (3 events in one bank; a model would be unidentified/separation-prone)' → v2 'not tested (3 events in one bank; a model would be unidentified/separation-prone)' (unchanged); robustness label unchanged ('not applicable')
- O5 Allowance / gross loans: v1 'H0 not rejected at 5% (WCB)' → v2 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O5 CAR: v1 'H0 not rejected at 5% (WCB)' → v2 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O5 Equity / assets: v1 'H0 not rejected at 5% (WCB)' → v2 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O5 Impairment / average assets: v1 'H0 not rejected at 5% (WCB)' → v2 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O5 Leverage: v1 'H0 not rejected at 5% (WCB)' → v2 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O5 OCF / average assets: v1 'H0 not rejected at 5% (WCB)' → v2 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O5 ROA: v1 'H0 not rejected at 5% (WCB)' → v2 'H0 not rejected at 5% (WCB)' (unchanged); robustness label unchanged ('primary not significant')
- O6 Allowance / gross loans: v1 'H0 not rejected (exploratory)' → v2 'H0 not rejected (exploratory)' (unchanged); robustness label unchanged ('exploratory')
- O6 CAR: v1 'H0 not rejected (exploratory)' → v2 'H0 not rejected (exploratory)' (unchanged); robustness label unchanged ('exploratory')
- O6 Impairment / average assets: v1 'H0 rejected (exploratory)' → v2 'H0 not rejected (exploratory)' (CHANGED); robustness label unchanged ('exploratory')
- O6 ROA: v1 'H0 not rejected (exploratory)' → v2 'H0 not rejected (exploratory)' (unchanged); robustness label unchanged ('exploratory')

## 8. Matched pre/post and volatility [comparison_matched_prepost.csv, comparison_volatility.csv]

- Matched Allowance / gross loans (All matched banks): banks 9→9; mean diff -0.911→-0.992; Wilcoxon p 0.496→0.570
- Matched Allowance / gross loans (Tier 1): banks 4→4; mean diff 1.837→1.654; Wilcoxon p n/a→n/a
- Matched Allowance / gross loans (Tier 2): banks 5→5; mean diff -3.109→-3.109; Wilcoxon p 0.625→0.625
- Matched CAR (All matched banks): banks 8→8; mean diff -3.881→-3.904; Wilcoxon p 0.195→0.195
- Matched CAR (Tier 1): banks 3→3; mean diff 0.038→-0.023; Wilcoxon p n/a→n/a
- Matched CAR (Tier 2): banks 5→5; mean diff -6.233→-6.233; Wilcoxon p 0.188→0.188
- Matched Equity / assets (All matched banks): banks 9→9; mean diff -10.128→-10.146; Wilcoxon p 0.008→0.008
- Matched Equity / assets (Tier 1): banks 4→4; mean diff -2.668→-2.708; Wilcoxon p n/a→n/a
- Matched Equity / assets (Tier 2): banks 5→5; mean diff -16.096→-16.096; Wilcoxon p 0.062→0.062
- Matched Impairment / average assets (All matched banks): banks 9→9; mean diff -0.977→-0.962; Wilcoxon p 0.074→0.074
- Matched Impairment / average assets (Tier 1): banks 4→4; mean diff -0.281→-0.248; Wilcoxon p n/a→n/a
- Matched Impairment / average assets (Tier 2): banks 5→5; mean diff -1.533→-1.533; Wilcoxon p 0.312→0.312
- Matched Leverage (All matched banks): banks 9→9; mean diff 10.128→10.146; Wilcoxon p 0.008→0.008
- Matched Leverage (Tier 1): banks 4→4; mean diff 2.668→2.708; Wilcoxon p n/a→n/a
- Matched Leverage (Tier 2): banks 5→5; mean diff 16.096→16.096; Wilcoxon p 0.062→0.062
- Matched OCF / average assets (All matched banks): banks 9→9; mean diff 6.332→6.264; Wilcoxon p 0.020→0.020
- Matched OCF / average assets (Tier 1): banks 4→4; mean diff 7.147→6.995; Wilcoxon p n/a→n/a
- Matched OCF / average assets (Tier 2): banks 5→5; mean diff 5.679→5.679; Wilcoxon p 0.125→0.125
- Matched ROA (All matched banks): banks 9→9; mean diff -0.002→0.004; Wilcoxon p 0.910→0.910
- Matched ROA (Tier 1): banks 4→4; mean diff -0.202→-0.189; Wilcoxon p n/a→n/a
- Matched ROA (Tier 2): banks 5→5; mean diff 0.158→0.158; Wilcoxon p 0.625→0.625
- Volatility Allowance / gross loans: banks 8→8; median SD ratio 1.19→1.19; Wilcoxon p 0.844→0.844
- Volatility CAR: banks 6→7; median SD ratio 0.74→0.77; Wilcoxon p 0.062→0.297
- Volatility Equity / assets: banks 9→9; median SD ratio 1.39→1.39; Wilcoxon p 0.359→0.359
- Volatility Impairment / average assets: banks 8→8; median SD ratio 0.34→0.34; Wilcoxon p 0.039→0.055 (crosses 0.05)
- Volatility Leverage: banks 9→9; median SD ratio 1.39→1.39; Wilcoxon p 0.359→0.359
- Volatility OCF / average assets: banks 7→7; median SD ratio 1.40→1.40; Wilcoxon p 0.578→0.688
- Volatility ROA: banks 8→8; median SD ratio 0.60→0.60; Wilcoxon p 0.383→0.383

## 9. Bank-level results for the banks with added rows [comparison_bank_level.csv]

- Access allr: n post 3→4; post-minus-pre 2.136→1.406
- Access car: n post 2→3; post-minus-pre -0.177→-0.360
- Access eqta: n post 4→5; post-minus-pre -4.714→-4.874
- Access impairment_assets: n post 3→4; post-minus-pre -0.143→-0.009
- Access leverage: n post 4→5; post-minus-pre 4.714→4.874
- Access ocf_ratio: n post 3→4; post-minus-pre 11.915→11.310
- Access roa: n post 3→4; post-minus-pre -0.908→-0.855

## 10. Summary

- Principal (M1) and tier (M4) estimates flagged material under the rule: 0 of 14 [comparison_regression.csv].
- Objective-level H0 decisions changed: 1 of 19 [comparison_interpretation.csv].
