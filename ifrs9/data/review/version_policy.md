# Reporting-version selection policy

The rule is applied mechanically and recorded per value in `data/field_status.csv`
(`reporting_version`) and in `data/review/version_decisions.csv`.

1. **Primary rule.** Use the bank-year's own audited report, as originally published
   (the "original-year" report), for all inputs of that bank-year.
2. **Fallback.** If the original-year report has not been retrieved, use the next
   year's audited comparative column. Flag the value as `comparative`, and add
   `+restated_comparative` where the column is labelled Restated.
3. **No mixing within a bank-year.** PAT, assets, liabilities and equity of a new
   bank-year must come from one reporting version (enforced at admission).
4. **Opening assets.** Use the prior-period column of the *same* report as the
   bank-year's closing assets, so that average-asset denominators are version-matched.
   Where that differs from the panel's own prior-year closing assets, both are kept
   and the difference is listed in `data/denominator_compatibility.csv`.
5. **Later alternatives.** A later report's different figure never silently replaces
   the primary value. It is recorded as a source alternative and classified as one of:
   *labelled restatement*, *labelled reclassification*, or *unexplained difference*.
6. **Baseline rows.** The 47 inherited rows keep their inherited version. They change
   only through a logged, evidence-backed correction.
7. **Sensitivity.** Analyses that use a value with a recorded alternative should be
   repeated with the alternative (column `sensitivity_alternative` in the decisions file).
