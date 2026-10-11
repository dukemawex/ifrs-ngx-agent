**Table 11. Model diagnostics**

| outcome | model | N | banks | banks_observed_both_regimes | within_share_of_variance | max_vif | condition_number | max_cooks_d | max_cooks_obs | n_cooks_gt_4_over_N | jarque_bera_p | breusch_pagan_p | wooldridge_ar1_p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| allr | M1 | 93 | 12 | 11 | 0.756 | 1.000 | 1.000 | 0.599 | Unity 2016 | 2 | 0.000 | 0.156 | 0.000 |
| allr | M2 | 93 | 12 | 11 | 0.756 | 2.310 | 2.741 | 1.536 | Unity 2016 | 4 | 0.000 | 0.004 |  |
| allr | M4 | 93 | 12 | 11 | 0.756 | 2.622 | 4.856 | 0.385 | Unity 2016 | 3 | 0.000 | 0.237 |  |
| impairment_assets | M1 | 90 | 12 | 12 | 0.725 | 1.000 | 1.000 | 0.233 | Unity 2016 | 4 | 0.000 | 0.358 | 0.195 |
| impairment_assets | M2 | 90 | 12 | 12 | 0.725 | 2.333 | 2.819 | 0.385 | Unity 2016 | 6 | 0.000 | 0.366 |  |
| impairment_assets | M4 | 90 | 12 | 12 | 0.725 | 3.292 | 5.700 | 0.172 | Unity 2016 | 4 | 0.000 | 0.793 |  |
| car | M1 | 86 | 12 | 11 | 0.165 | 1.000 | 1.000 | 0.600 | Unity 2016 | 5 | 0.000 | 0.584 | 0.000 |
| car | M2 | 86 | 12 | 11 | 0.165 | 2.351 | 2.774 | 1.533 | Unity 2016 | 8 | 0.000 | 0.830 |  |
| car | M4 | 86 | 12 | 11 | 0.165 | 2.427 | 4.590 | 0.356 | Unity 2016 | 6 | 0.000 | 0.987 |  |
| roa | M1 | 97 | 12 | 12 | 0.291 | 1.000 | 1.000 | 0.301 | Unity 2017 | 4 | 0.000 | 0.409 | 0.034 |
| roa | M2 | 97 | 12 | 12 | 0.291 | 2.386 | 2.815 | 1.476 | Unity 2017 | 5 | 0.000 | 0.057 |  |
| roa | M4 | 97 | 12 | 12 | 0.291 | 3.306 | 5.865 | 0.343 | Unity 2017 | 3 | 0.000 | 0.632 |  |
| ocf_ratio | M1 | 86 | 12 | 11 | 0.753 | 1.000 | 1.000 | 0.061 | UBA 2019 | 5 | 0.575 | 0.674 | 0.646 |
| ocf_ratio | M2 | 86 | 12 | 11 | 0.753 | 2.278 | 2.758 | 0.144 | Unity 2017 | 3 | 0.671 | 0.334 |  |
| ocf_ratio | M4 | 86 | 12 | 11 | 0.753 | 3.541 | 6.349 | 0.090 | UBA 2019 | 4 | 0.721 | 0.021 |  |
| eqta | M1 | 118 | 12 | 12 | 0.521 | 1.000 | 1.000 | 0.341 | Unity 2017 | 7 | 0.000 | 0.248 | 0.000 |
| eqta | M2 | 118 | 12 | 12 | 0.521 | 2.228 | 2.665 | 0.832 | Unity 2017 | 8 | 0.000 | 0.202 |  |
| eqta | M4 | 118 | 12 | 12 | 0.521 | 2.061 | 4.175 | 0.316 | Unity 2017 | 7 | 0.000 | 0.717 |  |
| leverage | M1 | 118 | 12 | 12 | 0.521 | 1.000 | 1.000 | 0.341 | Unity 2017 | 7 | 0.000 | 0.248 | 0.000 |
| leverage | M2 | 118 | 12 | 12 | 0.521 | 2.228 | 2.665 | 0.832 | Unity 2017 | 8 | 0.000 | 0.202 |  |
| leverage | M4 | 118 | 12 | 12 | 0.521 | 2.061 | 4.175 | 0.316 | Unity 2017 | 7 | 0.000 | 0.717 |  |

*Note.* VIF/condition number on the within-transformed design. Cook's D threshold 4/N. Wooldridge AR(1) test on first-differenced residuals (H0 no serial correlation). Source: model_diagnostics.csv.
