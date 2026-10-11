**Table 11. Model diagnostics**

| outcome | model | N | banks | banks_observed_both_regimes | within_share_of_variance | max_vif | condition_number | max_cooks_d | max_cooks_obs | n_cooks_gt_4_over_N | jarque_bera_p | breusch_pagan_p | wooldridge_ar1_p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| allr | M1 | 82 | 11 | 9 | 0.791 | 1.000 | 1.000 | 0.669 | Unity 2016 | 2 | 0.000 | 0.157 | 0.000 |
| allr | M2 | 82 | 11 | 9 | 0.791 | 2.438 | 2.794 | 1.695 | Unity 2016 | 3 | 0.000 | 0.006 |  |
| allr | M4 | 82 | 11 | 9 | 0.791 | 2.785 | 4.879 | 0.405 | Unity 2016 | 3 | 0.000 | 0.253 |  |
| impairment_assets | M1 | 73 | 12 | 9 | 0.634 | 1.000 | 1.000 | 0.324 | Unity 2016 | 4 | 0.000 | 0.635 | 0.005 |
| impairment_assets | M2 | 73 | 12 | 9 | 0.634 | 2.295 | 2.728 | 0.514 | Unity 2016 | 5 | 0.000 | 0.540 |  |
| impairment_assets | M4 | 73 | 12 | 9 | 0.634 | 4.326 | 6.604 | 0.225 | Unity 2016 | 4 | 0.000 | 0.938 |  |
| car | M1 | 75 | 11 | 8 | 0.165 | 1.000 | 1.000 | 0.661 | Unity 2016 | 5 | 0.000 | 0.563 | 0.000 |
| car | M2 | 75 | 11 | 8 | 0.165 | 2.608 | 2.908 | 1.646 | Unity 2016 | 8 | 0.000 | 0.903 |  |
| car | M4 | 75 | 11 | 8 | 0.165 | 2.592 | 4.471 | 0.333 | Unity 2016 | 6 | 0.000 | 0.980 |  |
| roa | M1 | 78 | 12 | 9 | 0.272 | 1.000 | 1.000 | 0.436 | Unity 2017 | 2 | 0.000 | 0.258 | 0.059 |
| roa | M2 | 78 | 12 | 9 | 0.272 | 2.364 | 2.751 | 1.813 | Unity 2017 | 3 | 0.000 | 0.053 |  |
| roa | M4 | 78 | 12 | 9 | 0.272 | 4.313 | 6.702 | 0.414 | Unity 2017 | 3 | 0.000 | 0.647 |  |
| ocf_ratio | M1 | 72 | 11 | 9 | 0.775 | 1.000 | 1.000 | 0.075 | UBA 2019 | 5 | 0.520 | 0.945 | 0.563 |
| ocf_ratio | M2 | 72 | 11 | 9 | 0.775 | 2.410 | 2.798 | 0.147 | Unity 2019 | 4 | 0.612 | 0.235 |  |
| ocf_ratio | M4 | 72 | 11 | 9 | 0.775 | 3.961 | 6.580 | 0.138 | UBA 2019 | 4 | 0.422 | 0.035 |  |
| eqta | M1 | 98 | 12 | 9 | 0.525 | 1.000 | 1.000 | 0.404 | Unity 2017 | 7 | 0.000 | 0.215 | 0.000 |
| eqta | M2 | 98 | 12 | 9 | 0.525 | 2.140 | 2.560 | 0.853 | Unity 2017 | 9 | 0.000 | 0.202 |  |
| eqta | M4 | 98 | 12 | 9 | 0.525 | 2.137 | 4.072 | 0.334 | Unity 2017 | 7 | 0.000 | 0.653 |  |
| leverage | M1 | 98 | 12 | 9 | 0.525 | 1.000 | 1.000 | 0.404 | Unity 2017 | 7 | 0.000 | 0.215 | 0.000 |
| leverage | M2 | 98 | 12 | 9 | 0.525 | 2.140 | 2.560 | 0.853 | Unity 2017 | 9 | 0.000 | 0.202 |  |
| leverage | M4 | 98 | 12 | 9 | 0.525 | 2.137 | 4.072 | 0.334 | Unity 2017 | 7 | 0.000 | 0.653 |  |

*Note.* VIF/condition number on the within-transformed design. Cook's D threshold 4/N. Wooldridge AR(1) test on first-differenced residuals (H0 no serial correlation). Source: model_diagnostics.csv.
