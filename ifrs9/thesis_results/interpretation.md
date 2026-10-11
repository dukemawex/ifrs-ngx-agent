# Interpretation by objective (no thesis prose)

Decision rule: H0 (no effect) rejected when the wild-cluster-bootstrap p < 0.05 for the principal model; CR1 and conventional p-values reported for transparency. Source: interpretation.csv.

## O1. IFRS 9 adoption and loan-loss provisioning

### Allowance / gross loans
- Usable sample: N = 81 bank-years, 11 banks (40 pre / 41 post)
- Estimator: Bank FE: y ~ IFRS9_D  [principal] (term IFRS9_D)
- Direction: decrease; magnitude: -0.87 pp vs pre-period mean 4.89 / median 3.10
- Significance: p conventional 0.326, p CR1 0.652, p WCB 0.889
- Robustness: primary not significant; same sign in 3/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 1
- Decision: H0 not rejected at 5% (WCB)
- Limitations: 11 bank clusters (few-cluster inference); IFRS9_D is a single common adoption date: without year FE it also absorbs 2018-2022 macro shocks (2020 pandemic, FX reforms)

### Impairment / average assets
- Usable sample: N = 72 bank-years, 12 banks (35 pre / 37 post)
- Estimator: Bank FE: y ~ IFRS9_D  [principal] (term IFRS9_D)
- Direction: decrease; magnitude: -0.91 pp vs pre-period mean 1.33 / median 0.76
- Significance: p conventional 0.001, p CR1 0.135, p WCB 0.070
- Robustness: primary not significant; same sign in 5/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 0
- Decision: H0 not rejected at 5% (WCB)
- Limitations: 12 bank clusters (few-cluster inference); IFRS9_D is a single common adoption date: without year FE it also absorbs 2018-2022 macro shocks (2020 pandemic, FX reforms)

## O2. IFRS 9 adoption and capital adequacy

### CAR
- Usable sample: N = 74 bank-years, 11 banks (37 pre / 37 post)
- Estimator: Bank FE: y ~ IFRS9_D  [principal] (term IFRS9_D)
- Direction: decrease; magnitude: -2.82 pp vs pre-period mean 10.53 / median 17.79
- Significance: p conventional 0.596, p CR1 0.250, p WCB 0.213
- Robustness: primary not significant; same sign in 5/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 0
- Decision: H0 not rejected at 5% (WCB)
- Limitations: 11 bank clusters (few-cluster inference); IFRS9_D is a single common adoption date: without year FE it also absorbs 2018-2022 macro shocks (2020 pandemic, FX reforms); Unity's negative-capital years dominate the variance (see S3/S5)

## O3. IFRS 9 adoption, profitability, cash generation and balance-sheet stability

### ROA
- Usable sample: N = 77 bank-years, 12 banks (39 pre / 38 post)
- Estimator: Bank FE: y ~ IFRS9_D  [principal] (term IFRS9_D)
- Direction: decrease; magnitude: -0.03 pp vs pre-period mean 1.58 / median 1.41
- Significance: p conventional 0.871, p CR1 0.835, p WCB 0.837
- Robustness: primary not significant; same sign in 3/4 sensitivities, WCB p < 0.05 in 0/4 (none); jackknife sign changes 3
- Decision: H0 not rejected at 5% (WCB)
- Limitations: 12 bank clusters (few-cluster inference); IFRS9_D is a single common adoption date: without year FE it also absorbs 2018-2022 macro shocks (2020 pandemic, FX reforms)

### OCF / average assets
- Usable sample: N = 71 bank-years, 11 banks (36 pre / 35 post)
- Estimator: Bank FE: y ~ IFRS9_D  [principal] (term IFRS9_D)
- Direction: increase; magnitude: +7.34 pp vs pre-period mean -1.54 / median -2.34
- Significance: p conventional 0.000, p CR1 0.003, p WCB 0.017
- Robustness: robust: same sign in 4/4 sensitivities, WCB p < 0.05 in 4/4, jackknife sign changes 0
- Decision: H0 rejected at 5% (WCB)
- Limitations: 11 bank clusters (few-cluster inference); IFRS9_D is a single common adoption date: without year FE it also absorbs 2018-2022 macro shocks (2020 pandemic, FX reforms)

### Equity / assets
- Usable sample: N = 97 bank-years, 12 banks (50 pre / 47 post)
- Estimator: Bank FE: y ~ IFRS9_D  [principal] (term IFRS9_D)
- Direction: decrease; magnitude: -10.68 pp vs pre-period mean 11.30 / median 14.39
- Significance: p conventional 0.019, p CR1 0.125, p WCB 0.013
- Robustness: robust: same sign in 4/4 sensitivities, WCB p < 0.05 in 4/4, jackknife sign changes 0
- Decision: H0 rejected at 5% (WCB); CR1 t(G-1) p = 0.125 gives the opposite decision
- Limitations: 12 bank clusters (few-cluster inference); IFRS9_D is a single common adoption date: without year FE it also absorbs 2018-2022 macro shocks (2020 pandemic, FX reforms); Unity's negative-capital years dominate the variance (see S3/S5)

### Leverage
- Usable sample: N = 97 bank-years, 12 banks (50 pre / 47 post)
- Estimator: Bank FE: y ~ IFRS9_D  [principal] (term IFRS9_D)
- Direction: increase; magnitude: +10.68 pp vs pre-period mean 88.70 / median 85.61
- Significance: p conventional 0.019, p CR1 0.125, p WCB 0.013
- Robustness: robust: same sign in 4/4 sensitivities, WCB p < 0.05 in 4/4, jackknife sign changes 0
- Decision: H0 rejected at 5% (WCB); CR1 t(G-1) p = 0.125 gives the opposite decision
- Limitations: 12 bank clusters (few-cluster inference); IFRS9_D is a single common adoption date: without year FE it also absorbs 2018-2022 macro shocks (2020 pandemic, FX reforms); Unity's negative-capital years dominate the variance (see S3/S5); leverage = 100 - equity/assets, so results mirror equity/assets

## O5. Tier 1 versus Tier 2 difference in the IFRS 9 effect

### Allowance / gross loans
- Usable sample: N = 81 bank-years, 11 banks (40 pre / 41 post)
- Estimator: Bank FE + year FE: y ~ Tier1 x IFRS9_D  [principal tier model; IFRS9_D absorbed by year FE] (term Tier1_x_IFRS9_D)
- Direction: increase; magnitude: +4.83 pp vs pre-period mean 4.89 / median 3.10
- Significance: p conventional 0.007, p CR1 0.123, p WCB 0.110
- Robustness: primary not significant; same sign in 5/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 0
- Decision: H0 not rejected at 5% (WCB)
- Limitations: 11 bank clusters (few-cluster inference); year FE absorb common shocks; identification rests on Tier 1 vs Tier 2 differences only; only 5 Tier 1 banks

### Impairment / average assets
- Usable sample: N = 72 bank-years, 12 banks (35 pre / 37 post)
- Estimator: Bank FE + year FE: y ~ Tier1 x IFRS9_D  [principal tier model; IFRS9_D absorbed by year FE] (term Tier1_x_IFRS9_D)
- Direction: increase; magnitude: +1.08 pp vs pre-period mean 1.33 / median 0.76
- Significance: p conventional 0.047, p CR1 0.262, p WCB 0.286
- Robustness: primary not significant; same sign in 5/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 0
- Decision: H0 not rejected at 5% (WCB)
- Limitations: 12 bank clusters (few-cluster inference); year FE absorb common shocks; identification rests on Tier 1 vs Tier 2 differences only; only 5 Tier 1 banks

### CAR
- Usable sample: N = 74 bank-years, 11 banks (37 pre / 37 post)
- Estimator: Bank FE + year FE: y ~ Tier1 x IFRS9_D  [principal tier model; IFRS9_D absorbed by year FE] (term Tier1_x_IFRS9_D)
- Direction: increase; magnitude: +5.58 pp vs pre-period mean 10.53 / median 17.79
- Significance: p conventional 0.612, p CR1 0.273, p WCB 0.304
- Robustness: primary not significant; same sign in 5/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 0
- Decision: H0 not rejected at 5% (WCB)
- Limitations: 11 bank clusters (few-cluster inference); year FE absorb common shocks; identification rests on Tier 1 vs Tier 2 differences only; Unity's negative-capital years dominate the variance (see S3/S5); only 5 Tier 1 banks

### ROA
- Usable sample: N = 77 bank-years, 12 banks (39 pre / 38 post)
- Estimator: Bank FE + year FE: y ~ Tier1 x IFRS9_D  [principal tier model; IFRS9_D absorbed by year FE] (term Tier1_x_IFRS9_D)
- Direction: decrease; magnitude: -0.43 pp vs pre-period mean 1.58 / median 1.41
- Significance: p conventional 0.293, p CR1 0.146, p WCB 0.160
- Robustness: primary not significant; same sign in 4/4 sensitivities, WCB p < 0.05 in 0/4 (none); jackknife sign changes 0
- Decision: H0 not rejected at 5% (WCB)
- Limitations: 12 bank clusters (few-cluster inference); year FE absorb common shocks; identification rests on Tier 1 vs Tier 2 differences only; only 5 Tier 1 banks

### OCF / average assets
- Usable sample: N = 71 bank-years, 11 banks (36 pre / 35 post)
- Estimator: Bank FE + year FE: y ~ Tier1 x IFRS9_D  [principal tier model; IFRS9_D absorbed by year FE] (term Tier1_x_IFRS9_D)
- Direction: increase; magnitude: +4.08 pp vs pre-period mean -1.54 / median -2.34
- Significance: p conventional 0.290, p CR1 0.281, p WCB 0.284
- Robustness: primary not significant; same sign in 4/4 sensitivities, WCB p < 0.05 in 0/4 (none); jackknife sign changes 0
- Decision: H0 not rejected at 5% (WCB)
- Limitations: 11 bank clusters (few-cluster inference); year FE absorb common shocks; identification rests on Tier 1 vs Tier 2 differences only; only 5 Tier 1 banks

### Equity / assets
- Usable sample: N = 97 bank-years, 12 banks (50 pre / 47 post)
- Estimator: Bank FE + year FE: y ~ Tier1 x IFRS9_D  [principal tier model; IFRS9_D absorbed by year FE] (term Tier1_x_IFRS9_D)
- Direction: increase; magnitude: +13.06 pp vs pre-period mean 11.30 / median 14.39
- Significance: p conventional 0.160, p CR1 0.257, p WCB 0.284
- Robustness: primary not significant; same sign in 4/4 sensitivities, WCB p < 0.05 in 0/4 (none); jackknife sign changes 0
- Decision: H0 not rejected at 5% (WCB)
- Limitations: 12 bank clusters (few-cluster inference); year FE absorb common shocks; identification rests on Tier 1 vs Tier 2 differences only; Unity's negative-capital years dominate the variance (see S3/S5); only 5 Tier 1 banks

### Leverage
- Usable sample: N = 97 bank-years, 12 banks (50 pre / 47 post)
- Estimator: Bank FE + year FE: y ~ Tier1 x IFRS9_D  [principal tier model; IFRS9_D absorbed by year FE] (term Tier1_x_IFRS9_D)
- Direction: decrease; magnitude: -13.06 pp vs pre-period mean 88.70 / median 85.61
- Significance: p conventional 0.160, p CR1 0.257, p WCB 0.284
- Robustness: primary not significant; same sign in 4/4 sensitivities, WCB p < 0.05 in 0/4 (none); jackknife sign changes 0
- Decision: H0 not rejected at 5% (WCB)
- Limitations: 12 bank clusters (few-cluster inference); year FE absorb common shocks; identification rests on Tier 1 vs Tier 2 differences only; Unity's negative-capital years dominate the variance (see S3/S5); leverage = 100 - equity/assets, so results mirror equity/assets; only 5 Tier 1 banks

## O4. Going-concern indicators before and after IFRS 9

### Going-concern uncertainty
- Usable sample: 46 coded bank-years, 10 banks; 3 events
- Estimator: descriptive only (event table, coverage, Fisher exact share comparison)
- Direction: events only after adoption; magnitude: events: Unity 2019, Unity 2021, Unity 2022
- Significance: p conventional , p CR1 , p WCB 
- Robustness: not applicable
- Decision: not tested (3 events in one bank; a model would be unidentified/separation-prone)
- Limitations: events concentrated in Unity; 51 panel rows have unknown (not zero) codes; Unity 2020 uncoded

## O6. Volatility before and after IFRS 9 (exploratory)

### ROA
- Usable sample: 8 banks with >= 3 comparable observations per regime
- Estimator: within-bank sample SD by regime; Wilcoxon signed-rank on log SD ratio
- Direction: lower after; magnitude: median SD ratio post/pre 0.60 (3 up, 5 down)
- Significance: p conventional , p CR1 , p WCB 0.383
- Robustness: exploratory; SDs from 3-5 points
- Decision: H0 not rejected (exploratory)
- Limitations: few observations per regime; SD sensitive to single years; not definitive

### CAR
- Usable sample: 6 banks with >= 3 comparable observations per regime
- Estimator: within-bank sample SD by regime; Wilcoxon signed-rank on log SD ratio
- Direction: lower after; magnitude: median SD ratio post/pre 0.74 (1 up, 5 down)
- Significance: p conventional , p CR1 , p WCB 0.062
- Robustness: exploratory; SDs from 3-5 points
- Decision: H0 not rejected (exploratory)
- Limitations: few observations per regime; SD sensitive to single years; not definitive

### Allowance / gross loans
- Usable sample: 8 banks with >= 3 comparable observations per regime
- Estimator: within-bank sample SD by regime; Wilcoxon signed-rank on log SD ratio
- Direction: higher after; magnitude: median SD ratio post/pre 1.19 (5 up, 3 down)
- Significance: p conventional , p CR1 , p WCB 0.844
- Robustness: exploratory; SDs from 3-5 points
- Decision: H0 not rejected (exploratory)
- Limitations: few observations per regime; SD sensitive to single years; not definitive

### Impairment / average assets
- Usable sample: 8 banks with >= 3 comparable observations per regime
- Estimator: within-bank sample SD by regime; Wilcoxon signed-rank on log SD ratio
- Direction: lower after; magnitude: median SD ratio post/pre 0.34 (1 up, 7 down)
- Significance: p conventional , p CR1 , p WCB 0.039
- Robustness: exploratory; SDs from 3-5 points
- Decision: H0 rejected (exploratory)
- Limitations: few observations per regime; SD sensitive to single years; not definitive
