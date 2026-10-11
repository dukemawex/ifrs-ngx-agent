**Table 11. Model diagnostics**

| outcome | model | N | banks | banks_observed_both_regimes | within_share_of_variance | max_vif | condition_number | max_cooks_d | max_cooks_obs | n_cooks_gt_4_over_N | jarque_bera_p | breusch_pagan_p | wooldridge_ar1_p |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| allr | M1 | 81 | 11 | 9 | 0.794 | 1.000 | 1.000 | 0.672 | Unity 2016 | 2 | 0.000 | 0.156 | 0.000 |
| allr | M2 | 81 | 11 | 9 | 0.794 | 2.445 | 2.812 | 1.720 | Unity 2016 | 3 | 0.000 | 0.006 |  |
| allr | M4 | 81 | 11 | 9 | 0.794 | 2.793 | 4.844 | 0.400 | Unity 2016 | 3 | 0.000 | 0.261 |  |
| impairment_assets | M1 | 72 | 12 | 9 | 0.633 | 1.000 | 1.000 | 0.328 | Unity 2016 | 4 | 0.000 | 0.637 | 0.005 |
| impairment_assets | M2 | 72 | 12 | 9 | 0.633 | 2.314 | 2.778 | 0.530 | Unity 2016 | 5 | 0.000 | 0.509 |  |
| impairment_assets | M4 | 72 | 12 | 9 | 0.633 | 4.334 | 6.539 | 0.223 | Unity 2016 | 4 | 0.000 | 0.940 |  |
| car | M1 | 74 | 11 | 8 | 0.166 | 1.000 | 1.000 | 0.665 | Unity 2016 | 5 | 0.000 | 0.563 | 0.000 |
| car | M2 | 74 | 11 | 8 | 0.166 | 2.592 | 2.909 | 1.643 | Unity 2016 | 8 | 0.000 | 0.906 |  |
| car | M4 | 74 | 11 | 8 | 0.166 | 2.436 | 4.371 | 0.329 | Unity 2016 | 6 | 0.000 | 0.981 |  |
| roa | M1 | 77 | 12 | 9 | 0.271 | 1.000 | 1.000 | 0.438 | Unity 2017 | 2 | 0.000 | 0.264 | 0.066 |
| roa | M2 | 77 | 12 | 9 | 0.271 | 2.374 | 2.780 | 2.005 | Unity 2017 | 3 | 0.000 | 0.044 |  |
| roa | M4 | 77 | 12 | 9 | 0.271 | 4.319 | 6.638 | 0.408 | Unity 2017 | 3 | 0.000 | 0.655 |  |
| ocf_ratio | M1 | 71 | 11 | 9 | 0.776 | 1.000 | 1.000 | 0.080 | Access 2019 | 5 | 0.497 | 0.852 | 0.507 |
| ocf_ratio | M2 | 71 | 11 | 9 | 0.776 | 2.426 | 2.831 | 0.166 | Unity 2017 | 3 | 0.562 | 0.315 |  |
| ocf_ratio | M4 | 71 | 11 | 9 | 0.776 | 3.951 | 6.517 | 0.136 | UBA 2019 | 3 | 0.397 | 0.046 |  |
| eqta | M1 | 97 | 12 | 9 | 0.525 | 1.000 | 1.000 | 0.406 | Unity 2017 | 7 | 0.000 | 0.215 | 0.000 |
| eqta | M2 | 97 | 12 | 9 | 0.525 | 2.152 | 2.588 | 0.928 | Unity 2017 | 10 | 0.000 | 0.178 |  |
| eqta | M4 | 97 | 12 | 9 | 0.525 | 2.141 | 4.040 | 0.330 | Unity 2017 | 7 | 0.000 | 0.657 |  |
| leverage | M1 | 97 | 12 | 9 | 0.525 | 1.000 | 1.000 | 0.406 | Unity 2017 | 7 | 0.000 | 0.215 | 0.000 |
| leverage | M2 | 97 | 12 | 9 | 0.525 | 2.152 | 2.588 | 0.928 | Unity 2017 | 10 | 0.000 | 0.178 |  |
| leverage | M4 | 97 | 12 | 9 | 0.525 | 2.141 | 4.040 | 0.330 | Unity 2017 | 7 | 0.000 | 0.657 |  |

*Note.* VIF/condition number on the within-transformed design. Cook's D threshold 4/N. Wooldridge AR(1) test on first-differenced residuals (H0 no serial correlation). Source: model_diagnostics.csv.
