# Model readiness (no thesis regressions run)

Generated from `data/outcome_eligibility.csv` via `ifrs9_recovery.eligibility.sample()`.

## Collinearity warning

IFRS9_D = 1 for 2018-2022 is an exact linear combination of the year dummies. A specification with IFRS9_D and a full set of year fixed effects is not identified. Use bank fixed effects with time-varying macro controls, or identify a differential effect (e.g. Tier 1 x Post) with bank and year fixed effects.

With 12 banks the number of clusters is small: report wild-cluster-bootstrap inference.

## Recommended estimator by outcome

| Outcome | Eligible N | Banks | Status | Tier DiD feasible | Banks with volatility feasible | Recommended estimator |
|---|---|---|---|---|---|---|
| car | 74 | 11 | testable | True | 6 | bank fixed effects with IFRS9_D (no year FE: collinear) and macro controls instead; bank-clustered SEs with wild cluster bootstrap (few clusters); robustness: pooled OLS, drop fallback rows |
| car_computed | 54 | 11 | testable | True | 5 | bank fixed effects with IFRS9_D (no year FE: collinear) and macro controls instead; bank-clustered SEs with wild cluster bootstrap (few clusters); robustness: pooled OLS, drop fallback rows |
| roa | 77 | 12 | testable | True | 8 | bank fixed effects with IFRS9_D (no year FE: collinear) and macro controls instead; bank-clustered SEs with wild cluster bootstrap (few clusters); robustness: pooled OLS, drop fallback rows |
| eqta | 97 | 12 | testable | True | 9 | bank fixed effects with IFRS9_D (no year FE: collinear) and macro controls instead; bank-clustered SEs with wild cluster bootstrap (few clusters); robustness: pooled OLS, drop fallback rows |
| ocf_ratio | 71 | 11 | testable | True | 7 | bank fixed effects with IFRS9_D (no year FE: collinear) and macro controls instead; bank-clustered SEs with wild cluster bootstrap (few clusters); robustness: pooled OLS, drop fallback rows |
| allr | 81 | 11 | testable | True | 8 | bank fixed effects with IFRS9_D (no year FE: collinear) and macro controls instead; bank-clustered SEs with wild cluster bootstrap (few clusters); robustness: pooled OLS, drop fallback rows |
| impairment_assets | 72 | 12 | testable | True | 8 | bank fixed effects with IFRS9_D (no year FE: collinear) and macro controls instead; bank-clustered SEs with wild cluster bootstrap (few clusters); robustness: pooled OLS, drop fallback rows |
| npl_calc | 14 | 3 | descriptive | False | 1 | descriptive only (too few eligible observations / banks observed in both regimes) |
| broad_coverage | 13 | 3 | descriptive | False | 1 | descriptive only (too few eligible observations / banks observed in both regimes) |
| stage3_coverage | 5 | 2 | descriptive | False | 0 | descriptive only (too few eligible observations / banks observed in both regimes) |
| liquidity | 10 | 3 | descriptive | False | 1 | descriptive only (too few eligible observations / banks observed in both regimes) |
| leverage | 97 | 12 | testable | True | 9 | bank fixed effects with IFRS9_D (no year FE: collinear) and macro controls instead; bank-clustered SEs with wild cluster bootstrap (few clusters); robustness: pooled OLS, drop fallback rows |
| gcu | 46 | 10 | descriptive | True | 4 | descriptive only: event counts by regime and tier; exact (Fisher) comparison of event shares; no multivariable model |

## Objectives

| Objective | Testable outcomes | Descriptive only | Readiness |
|---|---|---|---|
| O1 Effect of IFRS 9 adoption on loan-loss provisioning | allr;impairment_assets | broad_coverage;npl_calc;stage3_coverage | testable |
| O2 Effect of IFRS 9 adoption on capital adequacy | car;car_computed | - | testable |
| O3 Effect of IFRS 9 adoption on profitability, cash generation and balance-sheet stability | roa;ocf_ratio;eqta;leverage | liquidity | testable |
| O4 Going-concern indicators before and after IFRS 9 | - | gcu | descriptive only |
| O5 Tier 1 versus Tier 2 differences in the IFRS 9 effect | allr;car;roa;eqta | - | testable |
| O6 Change in volatility of key indicators after IFRS 9 | roa;car;allr;impairment_assets | - | exploratory test only (bank-level SDs from >=3 observations per regime) |

Objective wording is inferred from the study title and dataset variables; map it onto the thesis's own objectives.

## Files

- trend_matched_pre_post.csv, tier_comparison.csv, volatility_feasibility.csv, within_bank_variation.csv,
  model_sample_sizes.csv, estimator_recommendations.csv, objective_readiness.csv
