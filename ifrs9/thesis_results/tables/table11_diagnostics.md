**Table 11. Model diagnostics**

| outcome | model | N | banks | banks_observed_both_regimes | within_share_of_variance | max_vif | condition_number | max_cooks_d | max_cooks_obs | n_cooks_gt_4_over_N | jarque_bera_p | breusch_pagan_p | wooldridge_ar1_p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| allr | M1 | 92 | 12 | 10 | 0.750 | 1.000 | 1.000 | 0.627 | Unity 2016 | 2 | 0.000 | 0.166 | 0.000 |
| allr | M2 | 92 | 12 | 10 | 0.750 | 2.332 | 2.745 | 1.618 | Unity 2016 | 4 | 0.000 | 0.004 |  |
| allr | M4 | 92 | 12 | 10 | 0.750 | 2.622 | 4.665 | 0.393 | Unity 2016 | 3 | 0.000 | 0.278 |  |
| impairment_assets | M1 | 88 | 12 | 11 | 0.723 | 1.000 | 1.000 | 0.239 | Unity 2016 | 4 | 0.000 | 0.459 | 0.197 |
| impairment_assets | M2 | 88 | 12 | 11 | 0.723 | 2.378 | 2.834 | 0.398 | Unity 2016 | 5 | 0.000 | 0.521 |  |
| impairment_assets | M4 | 88 | 12 | 11 | 0.723 | 3.089 | 5.437 | 0.170 | Unity 2016 | 4 | 0.000 | 0.839 |  |
| car | M1 | 84 | 12 | 10 | 0.165 | 1.000 | 1.000 | 0.635 | Unity 2016 | 6 | 0.000 | 0.574 | 0.000 |
| car | M2 | 84 | 12 | 10 | 0.165 | 2.450 | 2.825 | 1.627 | Unity 2016 | 8 | 0.000 | 0.834 |  |
| car | M4 | 84 | 12 | 10 | 0.165 | 2.430 | 4.285 | 0.347 | Unity 2016 | 6 | 0.000 | 0.986 |  |
| roa | M1 | 95 | 12 | 11 | 0.291 | 1.000 | 1.000 | 0.311 | Unity 2017 | 4 | 0.000 | 0.454 | 0.038 |
| roa | M2 | 95 | 12 | 11 | 0.291 | 2.462 | 2.854 | 1.462 | Unity 2017 | 5 | 0.000 | 0.051 |  |
| roa | M4 | 95 | 12 | 11 | 0.291 | 3.123 | 5.556 | 0.336 | Unity 2017 | 3 | 0.000 | 0.650 |  |
| ocf_ratio | M1 | 84 | 12 | 10 | 0.747 | 1.000 | 1.000 | 0.066 | UBA 2019 | 5 | 0.592 | 0.900 | 0.643 |
| ocf_ratio | M2 | 84 | 12 | 10 | 0.747 | 2.352 | 2.791 | 0.149 | Unity 2017 | 3 | 0.724 | 0.253 |  |
| ocf_ratio | M4 | 84 | 12 | 10 | 0.747 | 3.451 | 6.022 | 0.127 | UBA 2019 | 6 | 0.457 | 0.040 |  |
| eqta | M1 | 115 | 12 | 11 | 0.521 | 1.000 | 1.000 | 0.357 | Unity 2017 | 7 | 0.000 | 0.237 | 0.000 |
| eqta | M2 | 115 | 12 | 11 | 0.521 | 2.246 | 2.669 | 0.841 | Unity 2017 | 8 | 0.000 | 0.202 |  |
| eqta | M4 | 115 | 12 | 11 | 0.521 | 1.946 | 3.898 | 0.307 | Unity 2017 | 7 | 0.000 | 0.719 |  |
| leverage | M1 | 115 | 12 | 11 | 0.521 | 1.000 | 1.000 | 0.357 | Unity 2017 | 7 | 0.000 | 0.237 | 0.000 |
| leverage | M2 | 115 | 12 | 11 | 0.521 | 2.246 | 2.669 | 0.841 | Unity 2017 | 8 | 0.000 | 0.202 |  |
| leverage | M4 | 115 | 12 | 11 | 0.521 | 1.946 | 3.898 | 0.307 | Unity 2017 | 7 | 0.000 | 0.719 |  |

*Note.* VIF/condition number on the within-transformed design. Cook's D threshold 4/N. Wooldridge AR(1) test on first-differenced residuals (H0 no serial correlation). Source: model_diagnostics.csv.
