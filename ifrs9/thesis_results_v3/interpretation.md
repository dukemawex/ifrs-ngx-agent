# Interpretation by objective (no thesis prose)

Decision rule: H0 (no effect) rejected when the wild-cluster-bootstrap p < 0.05 for the principal model; CR1 and conventional p-values reported for transparency. Source: interpretation.csv.

## O1. IFRS 9 adoption and loan-loss provisioning

### Allowance / gross loans
- Usable sample: N = 92 bank-years, 12 banks (45 pre / 47 post)
- Estimator: Bank FE: y ~ IFRS9_D  [principal] (term IFRS9_D)
- Direction: decrease; magnitude: -0.40 pp vs pre-period mean 4.88 / median 3.16
- Significance: p conventional 0.619, p CR1 0.815, p WCB 0.951
- Robustness: primary not significant; same sign in 4/6 sensitivities, WCB p < 0.05 in 0/6 (none); jackknife sign changes 1
- Decision: H0 not rejected at 5% (WCB)
- Limitations: 12 bank clusters (few-cluster inference); IFRS9_D is a single common adoption date: without year FE it also absorbs 2018-2022 macro shocks (2020 pandemic, FX reforms)

### Impairment / average assets
- Usable sample: N = 87 bank-years, 12 banks (44 pre / 43 post)
- Estimator: Bank FE: y ~ IFRS9_D  [principal] (term IFRS9_D)
- Direction: decrease; magnitude: -1.11 pp vs pre-period mean 1.45 / median 0.92
- Significance: p conventional 0.000, p CR1 0.031, p WCB 0.011
- Robustness: robust: same sign in 6/6 sensitivities, WCB p < 0.05 in 6/6, jackknife sign changes 0
- Decision: H0 rejected at 5% (WCB)
- Limitations: 12 bank clusters (few-cluster inference); IFRS9_D is a single common adoption date: without year FE it also absorbs 2018-2022 macro shocks (2020 pandemic, FX reforms)

## O2. IFRS 9 adoption and capital adequacy

### CAR
- Usable sample: N = 84 bank-years, 12 banks (41 pre / 43 post)
- Estimator: Bank FE: y ~ IFRS9_D  [principal] (term IFRS9_D)
- Direction: decrease; magnitude: -2.59 pp vs pre-period mean 11.25 / median 17.79
- Significance: p conventional 0.570, p CR1 0.209, p WCB 0.150
- Robustness: primary not significant; same sign in 6/6 sensitivities, WCB p < 0.05 in 0/6 (none); jackknife sign changes 0
- Decision: H0 not rejected at 5% (WCB)
- Limitations: 12 bank clusters (few-cluster inference); IFRS9_D is a single common adoption date: without year FE it also absorbs 2018-2022 macro shocks (2020 pandemic, FX reforms); Unity's negative-capital years dominate the variance (see S3/S5)

## O3. IFRS 9 adoption, profitability, cash generation and balance-sheet stability

### ROA
- Usable sample: N = 94 bank-years, 12 banks (48 pre / 46 post)
- Estimator: Bank FE: y ~ IFRS9_D  [principal] (term IFRS9_D)
- Direction: decrease; magnitude: -0.06 pp vs pre-period mean 1.68 / median 1.48
- Significance: p conventional 0.730, p CR1 0.699, p WCB 0.699
- Robustness: primary not significant; same sign in 5/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 1
- Decision: H0 not rejected at 5% (WCB)
- Limitations: 12 bank clusters (few-cluster inference); IFRS9_D is a single common adoption date: without year FE it also absorbs 2018-2022 macro shocks (2020 pandemic, FX reforms)

### OCF / average assets
- Usable sample: N = 84 bank-years, 12 banks (41 pre / 43 post)
- Estimator: Bank FE: y ~ IFRS9_D  [principal] (term IFRS9_D)
- Direction: increase; magnitude: +6.58 pp vs pre-period mean -1.18 / median -0.10
- Significance: p conventional 0.000, p CR1 0.003, p WCB 0.010
- Robustness: robust: same sign in 5/5 sensitivities, WCB p < 0.05 in 5/5, jackknife sign changes 0
- Decision: H0 rejected at 5% (WCB)
- Limitations: 12 bank clusters (few-cluster inference); IFRS9_D is a single common adoption date: without year FE it also absorbs 2018-2022 macro shocks (2020 pandemic, FX reforms)

### Equity / assets
- Usable sample: N = 114 bank-years, 12 banks (59 pre / 55 post)
- Estimator: Bank FE: y ~ IFRS9_D  [principal] (term IFRS9_D)
- Direction: decrease; magnitude: -8.48 pp vs pre-period mean 11.49 / median 13.83
- Significance: p conventional 0.021, p CR1 0.132, p WCB 0.012
- Robustness: robust: same sign in 5/5 sensitivities, WCB p < 0.05 in 5/5, jackknife sign changes 0
- Decision: H0 rejected at 5% (WCB); CR1 t(G-1) p = 0.132 gives the opposite decision
- Limitations: 12 bank clusters (few-cluster inference); IFRS9_D is a single common adoption date: without year FE it also absorbs 2018-2022 macro shocks (2020 pandemic, FX reforms); Unity's negative-capital years dominate the variance (see S3/S5)

### Leverage
- Usable sample: N = 114 bank-years, 12 banks (59 pre / 55 post)
- Estimator: Bank FE: y ~ IFRS9_D  [principal] (term IFRS9_D)
- Direction: increase; magnitude: +8.48 pp vs pre-period mean 88.51 / median 86.17
- Significance: p conventional 0.021, p CR1 0.132, p WCB 0.012
- Robustness: robust: same sign in 5/5 sensitivities, WCB p < 0.05 in 5/5, jackknife sign changes 0
- Decision: H0 rejected at 5% (WCB); CR1 t(G-1) p = 0.132 gives the opposite decision
- Limitations: 12 bank clusters (few-cluster inference); IFRS9_D is a single common adoption date: without year FE it also absorbs 2018-2022 macro shocks (2020 pandemic, FX reforms); Unity's negative-capital years dominate the variance (see S3/S5); leverage = 100 - equity/assets, so results mirror equity/assets

## O5. Tier 1 versus Tier 2 difference in the IFRS 9 effect

### Allowance / gross loans
- Usable sample: N = 92 bank-years, 12 banks (45 pre / 47 post)
- Estimator: Bank FE + year FE: y ~ Tier1 x IFRS9_D  [principal tier model; IFRS9_D absorbed by year FE] (term Tier1_x_IFRS9_D)
- Direction: increase; magnitude: +4.11 pp vs pre-period mean 4.88 / median 3.16
- Significance: p conventional 0.010, p CR1 0.156, p WCB 0.135
- Robustness: primary not significant; same sign in 6/6 sensitivities, WCB p < 0.05 in 0/6 (none); jackknife sign changes 0
- Decision: H0 not rejected at 5% (WCB)
- Limitations: 12 bank clusters (few-cluster inference); year FE absorb common shocks; identification rests on Tier 1 vs Tier 2 differences only; only 5 Tier 1 banks

### Impairment / average assets
- Usable sample: N = 87 bank-years, 12 banks (44 pre / 43 post)
- Estimator: Bank FE + year FE: y ~ Tier1 x IFRS9_D  [principal tier model; IFRS9_D absorbed by year FE] (term Tier1_x_IFRS9_D)
- Direction: increase; magnitude: +1.18 pp vs pre-period mean 1.45 / median 0.92
- Significance: p conventional 0.009, p CR1 0.120, p WCB 0.111
- Robustness: primary not significant; same sign in 6/6 sensitivities, WCB p < 0.05 in 0/6 (none); jackknife sign changes 0
- Decision: H0 not rejected at 5% (WCB)
- Limitations: 12 bank clusters (few-cluster inference); year FE absorb common shocks; identification rests on Tier 1 vs Tier 2 differences only; only 5 Tier 1 banks

### CAR
- Usable sample: N = 84 bank-years, 12 banks (41 pre / 43 post)
- Estimator: Bank FE + year FE: y ~ Tier1 x IFRS9_D  [principal tier model; IFRS9_D absorbed by year FE] (term Tier1_x_IFRS9_D)
- Direction: increase; magnitude: +6.03 pp vs pre-period mean 11.25 / median 17.79
- Significance: p conventional 0.528, p CR1 0.271, p WCB 0.270
- Robustness: primary not significant; same sign in 6/6 sensitivities, WCB p < 0.05 in 0/6 (none); jackknife sign changes 0
- Decision: H0 not rejected at 5% (WCB)
- Limitations: 12 bank clusters (few-cluster inference); year FE absorb common shocks; identification rests on Tier 1 vs Tier 2 differences only; Unity's negative-capital years dominate the variance (see S3/S5); only 5 Tier 1 banks

### ROA
- Usable sample: N = 94 bank-years, 12 banks (48 pre / 46 post)
- Estimator: Bank FE + year FE: y ~ Tier1 x IFRS9_D  [principal tier model; IFRS9_D absorbed by year FE] (term Tier1_x_IFRS9_D)
- Direction: decrease; magnitude: -0.48 pp vs pre-period mean 1.68 / median 1.48
- Significance: p conventional 0.182, p CR1 0.055, p WCB 0.055
- Robustness: primary not significant; same sign in 5/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 0
- Decision: H0 not rejected at 5% (WCB)
- Limitations: 12 bank clusters (few-cluster inference); year FE absorb common shocks; identification rests on Tier 1 vs Tier 2 differences only; only 5 Tier 1 banks

### OCF / average assets
- Usable sample: N = 84 bank-years, 12 banks (41 pre / 43 post)
- Estimator: Bank FE + year FE: y ~ Tier1 x IFRS9_D  [principal tier model; IFRS9_D absorbed by year FE] (term Tier1_x_IFRS9_D)
- Direction: increase; magnitude: +3.61 pp vs pre-period mean -1.18 / median -0.10
- Significance: p conventional 0.274, p CR1 0.311, p WCB 0.320
- Robustness: primary not significant; same sign in 5/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 0
- Decision: H0 not rejected at 5% (WCB)
- Limitations: 12 bank clusters (few-cluster inference); year FE absorb common shocks; identification rests on Tier 1 vs Tier 2 differences only; only 5 Tier 1 banks

### Equity / assets
- Usable sample: N = 114 bank-years, 12 banks (59 pre / 55 post)
- Estimator: Bank FE + year FE: y ~ Tier1 x IFRS9_D  [principal tier model; IFRS9_D absorbed by year FE] (term Tier1_x_IFRS9_D)
- Direction: increase; magnitude: +8.91 pp vs pre-period mean 11.49 / median 13.83
- Significance: p conventional 0.243, p CR1 0.312, p WCB 0.362
- Robustness: primary not significant; same sign in 5/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 0
- Decision: H0 not rejected at 5% (WCB)
- Limitations: 12 bank clusters (few-cluster inference); year FE absorb common shocks; identification rests on Tier 1 vs Tier 2 differences only; Unity's negative-capital years dominate the variance (see S3/S5); only 5 Tier 1 banks

### Leverage
- Usable sample: N = 114 bank-years, 12 banks (59 pre / 55 post)
- Estimator: Bank FE + year FE: y ~ Tier1 x IFRS9_D  [principal tier model; IFRS9_D absorbed by year FE] (term Tier1_x_IFRS9_D)
- Direction: decrease; magnitude: -8.91 pp vs pre-period mean 88.51 / median 86.17
- Significance: p conventional 0.243, p CR1 0.312, p WCB 0.362
- Robustness: primary not significant; same sign in 5/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 0
- Decision: H0 not rejected at 5% (WCB)
- Limitations: 12 bank clusters (few-cluster inference); year FE absorb common shocks; identification rests on Tier 1 vs Tier 2 differences only; Unity's negative-capital years dominate the variance (see S3/S5); leverage = 100 - equity/assets, so results mirror equity/assets; only 5 Tier 1 banks

## O4. Going-concern indicators before and after IFRS 9

### Going-concern uncertainty
- Usable sample: 56 coded bank-years, 11 banks; 3 events
- Estimator: descriptive only (event table, coverage, Fisher exact share comparison)
- Direction: events only after adoption; magnitude: events: Unity 2019, Unity 2021, Unity 2022
- Significance: p conventional , p CR1 , p WCB 
- Robustness: not applicable
- Decision: not tested (3 events in one bank; a model would be unidentified/separation-prone)
- Limitations: events concentrated in Unity; 51 panel rows have unknown (not zero) codes; Unity 2020 uncoded

## O6. Volatility before and after IFRS 9 (exploratory)

### ROA
- Usable sample: 11 banks with >= 3 comparable observations per regime
- Estimator: within-bank sample SD by regime; Wilcoxon signed-rank on log SD ratio
- Direction: lower after; magnitude: median SD ratio post/pre 0.99 (5 up, 6 down)
- Significance: p conventional , p CR1 , p WCB 0.638
- Robustness: exploratory; SDs from 3-5 points
- Decision: H0 not rejected (exploratory)
- Limitations: few observations per regime; SD sensitive to single years; not definitive

### CAR
- Usable sample: 8 banks with >= 3 comparable observations per regime
- Estimator: within-bank sample SD by regime; Wilcoxon signed-rank on log SD ratio
- Direction: lower after; magnitude: median SD ratio post/pre 0.78 (3 up, 5 down)
- Significance: p conventional , p CR1 , p WCB 0.641
- Robustness: exploratory; SDs from 3-5 points
- Decision: H0 not rejected (exploratory)
- Limitations: few observations per regime; SD sensitive to single years; not definitive

### Allowance / gross loans
- Usable sample: 10 banks with >= 3 comparable observations per regime
- Estimator: within-bank sample SD by regime; Wilcoxon signed-rank on log SD ratio
- Direction: higher after; magnitude: median SD ratio post/pre 1.30 (7 up, 3 down)
- Significance: p conventional , p CR1 , p WCB 0.492
- Robustness: exploratory; SDs from 3-5 points
- Decision: H0 not rejected (exploratory)
- Limitations: few observations per regime; SD sensitive to single years; not definitive

### Impairment / average assets
- Usable sample: 11 banks with >= 3 comparable observations per regime
- Estimator: within-bank sample SD by regime; Wilcoxon signed-rank on log SD ratio
- Direction: lower after; magnitude: median SD ratio post/pre 0.33 (2 up, 9 down)
- Significance: p conventional , p CR1 , p WCB 0.014
- Robustness: exploratory; SDs from 3-5 points
- Decision: H0 rejected (exploratory)
- Limitations: few observations per regime; SD sensitive to single years; not definitive
