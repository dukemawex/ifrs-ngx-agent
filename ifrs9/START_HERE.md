# IFRS 9: Nimble / Claude Code handoff

Baseline: 47 selected bank-years, 11 represented banks, 2013–2022.
This pack has NOT updated the analytical dataset. It contains a verified inventory of
the present gaps and source leads for the next extraction pass.

## Use
1. Extract this ZIP into a local project or Codespaces workspace.
2. Supply your existing Nimble API key privately as NIMBLE_API_KEY, or in a
   gitignored local .env copied from .env.example. Do not paste a key into chat.
3. Open Claude Code in this directory.
4. Ask it: "Read CLAUDE_PROMPT.md, inspect the supplied inputs and task files,
   and implement and run the requested verification pipeline. Preserve the
   original inputs. Start with the inventory and an end-to-end pilot, then
   continue through the tasks within the configured budget."

## Contents
- inputs/: unchanged master workbook, selected CSV, prior evidence/recomputation
  archive, and two raw candidate extracts.
- tasks/bank_year_gaps.csv: 83 unselected bank-year positions (72 candidate-only
  and 11 without the current master's core PAT/assets pair).
- tasks/field_gaps_selected.csv: 354 absent-field or exception requests in
  already selected observations. Counts do not imply the bank failed to disclose.
- tasks/cohort.csv: operating-entity search aliases, with historical-scope checks.
- tasks/coverage_before.csv: exact 130-position master snapshot.
- tasks/bank_summary.csv and field_availability.csv: compact summaries.
- seeds/report_sources.csv: 32 inherited or newly located source/archive URLs.
  Newly opened Stanbic 2021/2022 PDFs and Fidelity 2022 are leads, not newly
  admitted bank-year rows. Wema's mirror remains a download-size issue.
- checks/snapshot_manifest.json: SHA-256 hashes for original inputs.
- CLAUDE_PROMPT.md: full execution instructions and verified Nimble API references.

No Nimble API call was made to prepare this pack. The 100-call starter cap is an
application setting, not a currency spending guarantee. Do not increase it silently.
The full thesis is intentionally not included: recover/verify data before rewriting it.

Sources used for the gap inventory:
IFRS9_Master_Data_Updated_20261010.xlsx, Master_130 and Read_Me sheets;
IFRS9_Selected_Data_Updated_20261010.csv.
