# Interpretation by objective (no thesis prose)

Decision rule: H0 (no effect) rejected when the wild-cluster-bootstrap p < 0.05 for the principal model; CR1 and conventional p-values reported for transparency. Source: interpretation.csv.

## O1. IFRS 9 adoption and loan-loss provisioning

### Allowance / gross loans
- Usable sample: N = 82 bank-years, 11 banks (40 pre / 42 post)
- Estimator: Bank FE: y ~ IFRS9_D  [principal] (term IFRS9_D)
- Direction: decrease; magnitude: -0.91 pp vs pre-period mean 4.89 / median 3.10
- Significance: p conventional 0.301, p CR1 0.635, p WCB 0.880
- Robustness: primary not significant; same sign in 3/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 1
- Decision: H0 not rejected at 5% (WCB)
- Limitations: 11 bank clusters (few-cluster inference); IFRS9_D is a single common adoption date: without year FE it also absorbs 2018-2022 macro shocks (2020 pandemic, FX reforms)

### Impairment / average assets
- Usable sample: N = 73 bank-years, 12 banks (35 pre / 38 post)
- Estimator: Bank FE: y ~ IFRS9_D  [principal] (term IFRS9_D)
- Direction: decrease; magnitude: -0.88 pp vs pre-period mean 1.33 / median 0.76
- Significance: p conventional 0.001, p CR1 0.144, p WCB 0.080
- Robustness: primary not significant; same sign in 5/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 0
- Decision: H0 not rejected at 5% (WCB)
- Limitations: 12 bank clusters (few-cluster inference); IFRS9_D is a single common adoption date: without year FE it also absorbs 2018-2022 macro shocks (2020 pandemic, FX reforms)

## O2. IFRS 9 adoption and capital adequacy

### CAR
- Usable sample: N = 75 bank-years, 11 banks (37 pre / 38 post)
- Estimator: Bank FE: y ~ IFRS9_D  [principal] (term IFRS9_D)
- Direction: decrease; magnitude: -2.78 pp vs pre-period mean 10.53 / median 17.79
- Significance: p conventional 0.593, p CR1 0.247, p WCB 0.206
- Robustness: primary not significant; same sign in 5/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 0
- Decision: H0 not rejected at 5% (WCB)
- Limitations: 11 bank clusters (few-cluster inference); IFRS9_D is a single common adoption date: without year FE it also absorbs 2018-2022 macro shocks (2020 pandemic, FX reforms); Unity's negative-capital years dominate the variance (see S3/S5)

## O3. IFRS 9 adoption, profitability, cash generation and balance-sheet stability

### ROA
- Usable sample: N = 78 bank-years, 12 banks (39 pre / 39 post)
- Estimator: Bank FE: y ~ IFRS9_D  [principal] (term IFRS9_D)
- Direction: decrease; magnitude: -0.04 pp vs pre-period mean 1.58 / median 1.41
- Significance: p conventional 0.837, p CR1 0.798, p WCB 0.800
- Robustness: primary not significant; same sign in 3/4 sensitivities, WCB p < 0.05 in 0/4 (none); jackknife sign changes 3
- Decision: H0 not rejected at 5% (WCB)
- Limitations: 12 bank clusters (few-cluster inference); IFRS9_D is a single common adoption date: without year FE it also absorbs 2018-2022 macro shocks (2020 pandemic, FX reforms)

### OCF / average assets
- Usable sample: N = 72 bank-years, 11 banks (36 pre / 36 post)
- Estimator: Bank FE: y ~ IFRS9_D  [principal] (term IFRS9_D)
- Direction: increase; magnitude: +7.33 pp vs pre-period mean -1.54 / median -2.34
- Significance: p conventional 0.000, p CR1 0.002, p WCB 0.017
- Robustness: robust: same sign in 4/4 sensitivities, WCB p < 0.05 in 4/4, jackknife sign changes 0
- Decision: H0 rejected at 5% (WCB)
- Limitations: 11 bank clusters (few-cluster inference); IFRS9_D is a single common adoption date: without year FE it also absorbs 2018-2022 macro shocks (2020 pandemic, FX reforms)

### Equity / assets
- Usable sample: N = 98 bank-years, 12 banks (50 pre / 48 post)
- Estimator: Bank FE: y ~ IFRS9_D  [principal] (term IFRS9_D)
- Direction: decrease; magnitude: -10.63 pp vs pre-period mean 11.30 / median 14.39
- Significance: p conventional 0.018, p CR1 0.123, p WCB 0.013
- Robustness: robust: same sign in 4/4 sensitivities, WCB p < 0.05 in 4/4, jackknife sign changes 0
- Decision: H0 rejected at 5% (WCB); CR1 t(G-1) p = 0.123 gives the opposite decision
- Limitations: 12 bank clusters (few-cluster inference); IFRS9_D is a single common adoption date: without year FE it also absorbs 2018-2022 macro shocks (2020 pandemic, FX reforms); Unity's negative-capital years dominate the variance (see S3/S5)

### Leverage
- Usable sample: N = 98 bank-years, 12 banks (50 pre / 48 post)
- Estimator: Bank FE: y ~ IFRS9_D  [principal] (term IFRS9_D)
- Direction: increase; magnitude: +10.63 pp vs pre-period mean 88.70 / median 85.61
- Significance: p conventional 0.018, p CR1 0.123, p WCB 0.013
- Robustness: robust: same sign in 4/4 sensitivities, WCB p < 0.05 in 4/4, jackknife sign changes 0
- Decision: H0 rejected at 5% (WCB); CR1 t(G-1) p = 0.123 gives the opposite decision
- Limitations: 12 bank clusters (few-cluster inference); IFRS9_D is a single common adoption date: without year FE it also absorbs 2018-2022 macro shocks (2020 pandemic, FX reforms); Unity's negative-capital years dominate the variance (see S3/S5); leverage = 100 - equity/assets, so results mirror equity/assets

## O5. Tier 1 versus Tier 2 difference in the IFRS 9 effect

### Allowance / gross loans
- Usable sample: N = 82 bank-years, 11 banks (40 pre / 42 post)
- Estimator: Bank FE + year FE: y ~ Tier1 x IFRS9_D  [principal tier model; IFRS9_D absorbed by year FE] (term Tier1_x_IFRS9_D)
- Direction: increase; magnitude: +4.74 pp vs pre-period mean 4.89 / median 3.10
- Significance: p conventional 0.007, p CR1 0.130, p WCB 0.114
- Robustness: primary not significant; same sign in 5/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 0
- Decision: H0 not rejected at 5% (WCB)
- Limitations: 11 bank clusters (few-cluster inference); year FE absorb common shocks; identification rests on Tier 1 vs Tier 2 differences only; only 5 Tier 1 banks

### Impairment / average assets
- Usable sample: N = 73 bank-years, 12 banks (35 pre / 38 post)
- Estimator: Bank FE + year FE: y ~ Tier1 x IFRS9_D  [principal tier model; IFRS9_D absorbed by year FE] (term Tier1_x_IFRS9_D)
- Direction: increase; magnitude: +1.14 pp vs pre-period mean 1.33 / median 0.76
- Significance: p conventional 0.033, p CR1 0.246, p WCB 0.255
- Robustness: primary not significant; same sign in 5/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 0
- Decision: H0 not rejected at 5% (WCB)
- Limitations: 12 bank clusters (few-cluster inference); year FE absorb common shocks; identification rests on Tier 1 vs Tier 2 differences only; only 5 Tier 1 banks

### CAR
- Usable sample: N = 75 bank-years, 11 banks (37 pre / 38 post)
- Estimator: Bank FE + year FE: y ~ Tier1 x IFRS9_D  [principal tier model; IFRS9_D absorbed by year FE] (term Tier1_x_IFRS9_D)
- Direction: increase; magnitude: +5.13 pp vs pre-period mean 10.53 / median 17.79
- Significance: p conventional 0.632, p CR1 0.290, p WCB 0.307
- Robustness: primary not significant; same sign in 5/5 sensitivities, WCB p < 0.05 in 0/5 (none); jackknife sign changes 0
- Decision: H0 not rejected at 5% (WCB)
- Limitations: 11 bank clusters (few-cluster inference); year FE absorb common shocks; identification rests on Tier 1 vs Tier 2 differences only; Unity's negative-capital years dominate the variance (see S3/S5); only 5 Tier 1 banks

### ROA
- Usable sample: N = 78 bank-years, 12 banks (39 pre / 39 post)
- Estimator: Bank FE + year FE: y ~ Tier1 x IFRS9_D  [principal tier model; IFRS9_D absorbed by year FE] (term Tier1_x_IFRS9_D)
- Direction: decrease; magnitude: -0.44 pp vs pre-period mean 1.58 / median 1.41
- Significance: p conventional 0.278, p CR1 0.138, p WCB 0.160
- Robustness: primary not significant; same sign in 4/4 sensitivities, WCB p < 0.05 in 0/4 (none); jackknife sign changes 0
- Decision: H0 not rejected at 5% (WCB)
- Limitations: 12 bank clusters (few-cluster inference); year FE absorb common shocks; identification rests on Tier 1 vs Tier 2 differences only; only 5 Tier 1 banks

### OCF / average assets
- Usable sample: N = 72 bank-years, 11 banks (36 pre / 36 post)
- Estimator: Bank FE + year FE: y ~ Tier1 x IFRS9_D  [principal tier model; IFRS9_D absorbed by year FE] (term Tier1_x_IFRS9_D)
- Direction: increase; magnitude: +3.89 pp vs pre-period mean -1.54 / median -2.34
- Significance: p conventional 0.304, p CR1 0.285, p WCB 0.285
- Robustness: primary not significant; same sign in 4/4 sensitivities, WCB p < 0.05 in 0/4 (none); jackknife sign changes 0
- Decision: H0 not rejected at 5% (WCB)
- Limitations: 11 bank clusters (few-cluster inference); year FE absorb common shocks; identification rests on Tier 1 vs Tier 2 differences only; only 5 Tier 1 banks

### Equity / assets
- Usable sample: N = 98 bank-years, 12 banks (50 pre / 48 post)
- Estimator: Bank FE + year FE: y ~ Tier1 x IFRS9_D  [principal tier model; IFRS9_D absorbed by year FE] (term Tier1_x_IFRS9_D)
- Direction: increase; magnitude: +12.84 pp vs pre-period mean 11.30 / median 14.39
- Significance: p conventional 0.159, p CR1 0.256, p WCB 0.282
- Robustness: primary not significant; same sign in 4/4 sensitivities, WCB p < 0.05 in 0/4 (none); jackknife sign changes 0
- Decision: H0 not rejected at 5% (WCB)
- Limitations: 12 bank clusters (few-cluster inference); year FE absorb common shocks; identification rests on Tier 1 vs Tier 2 differences only; Unity's negative-capital years dominate the variance (see S3/S5); only 5 Tier 1 banks

### Leverage
- Usable sample: N = 98 bank-years, 12 banks (50 pre / 48 post)
- Estimator: Bank FE + year FE: y ~ Tier1 x IFRS9_D  [principal tier model; IFRS9_D absorbed by year FE] (term Tier1_x_IFRS9_D)
- Direction: decrease; magnitude: -12.84 pp vs pre-period mean 88.70 / median 85.61
- Significance: p conventional 0.159, p CR1 0.256, p WCB 0.282
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
- Usable sample: 7 banks with >= 3 comparable observations per regime
- Estimator: within-bank sample SD by regime; Wilcoxon signed-rank on log SD ratio
- Direction: lower after; magnitude: median SD ratio post/pre 0.77 (2 up, 5 down)
- Significance: p conventional , p CR1 , p WCB 0.297
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
- Direction: lower after; magnitude: median SD ratio post/pre 0.34 (2 up, 6 down)
- Significance: p conventional , p CR1 , p WCB 0.055
- Robustness: exploratory; SDs from 3-5 points
- Decision: H0 not rejected (exploratory)
- Limitations: few observations per regime; SD sensitive to single years; not definitive
