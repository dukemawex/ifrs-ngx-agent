**Table 2. Variable definitions and eligible sample sizes**

| variable | definition | units | available_N | eligible_N | excluded_N | banks | pre | post | tier1 | tier2 | fallback_rows_in_eligible | analysis_role | excluded_rows |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Allowance / gross loans | Loan-loss allowance / gross customer loans | % | 82 | 81 | 1 | 11 | 40 | 41 | 35 | 46 | 5 | inferential models | Union 2018 (AUTO-POOL;EL-UNION18-ALLOWANCE) |
| Impairment / average assets | Total impairment charge / average total assets | % | 74 | 72 | 2 | 12 | 35 | 37 | 30 | 42 | 2 | inferential models | Unity 2017 (EL-UNITY17-IMP); Wema 2021 (AUTO-FALLBACK;EL-WEMA21-IMP) |
| CAR | Reported capital adequacy ratio (full-impact basis where both printed) | % | 76 | 74 | 2 | 11 | 37 | 37 | 31 | 43 | 2 | inferential models | Fidelity 2016 (AUTO-FLAG;EL-FID16-CAR); Wema 2021 (AUTO-FALLBACK;AUTO-FLAG;EL-WEMA21-CAR) |
| ROA | Profit after tax / average total assets | % | 77 | 77 | 0 | 12 | 39 | 38 | 32 | 45 | 3 | inferential models |  |
| OCF / average assets | Operating cash flow / average total assets | % | 71 | 71 | 0 | 11 | 36 | 35 | 30 | 41 | 3 | inferential models |  |
| Equity / assets | Total equity / total assets | % | 97 | 97 | 0 | 12 | 50 | 47 | 40 | 57 | 7 | inferential models |  |
| Leverage | Total liabilities / total assets | % | 97 | 97 | 0 | 12 | 50 | 47 | 40 | 57 | 7 | inferential models |  |
| NPL ratio | NPL amount / gross loans | % | 14 | 14 | 0 | 3 | 7 | 7 | 6 | 8 | 1 | descriptive only (too sparse) |  |
| Broad NPL coverage | Total loan allowance / NPL amount | % | 14 | 13 | 1 | 3 | 7 | 6 | 6 | 7 | 1 | descriptive only (too sparse) | Union 2018 (AUTO-POOL;EL-UNION18-ALLOWANCE) |
| Stage 3 coverage | Stage 3 allowance / Stage 3 gross exposure | % | 6 | 5 | 1 | 2 | 0 | 5 | 0 | 5 | 0 | descriptive only (too sparse) | Unity 2021 (EL-UNITY21-S3) |
| Liquidity ratio | Liquidity ratio used | % | 10 | 10 | 0 | 3 | 5 | 5 | 7 | 3 | 0 | descriptive only (too sparse) |  |
| Going-concern uncertainty | Auditor material-uncertainty section or going-concern emphasis (1/0) | indicator | 46 | 46 | 0 | 10 | 18 | 28 | 13 | 33 | 0 | event description only |  |

*Note.* Eligible = inferential_use in the frozen outcome_eligibility.csv. Fallback rows are original-year-unavailable comparatives kept in the primary sample.
