# Tracked research material and exposure (inventory, 2026-10-10)

Repository metadata indicated **public** visibility at review time. Nothing here was moved, deleted or
history-rewritten; changing visibility or history needs the owner's explicit approval
(GitHub: Settings → General → Danger Zone → Change visibility).

## Credentials
- `NIMBLE_API_KEY` is read only from the environment or the gitignored `.env`. A scan of all commits on all
  branches found no committed `.env` file and no assignment of a key value; only `.env.example` files
  (placeholders) are tracked. Tracked data/outputs were also scanned for key-like assignments (see
  `tests/test_real_data.py::test_no_secret_in_tracked_outputs`).

## Research inputs tracked in git (publicly readable while the repo is public)
| Path | Bytes | Nature |
|---|---|---|
| inputs/IFRS9_Selected_Data_Updated_20261010.csv | 32,702 | frozen 47-row selected panel (thesis data) |
| inputs/IFRS9_Master_Data_Updated_20261010.xlsx | 143,304 | master workbook (thesis data) |
| inputs/IFRS9_Data_Update_Pack_20261010.zip | 61,044 | update pack |
| inputs/extract_nigerian_bank_ifrs_9_financial_data_6085ddb6.csv | 20,825 | earlier extraction |
| inputs/nigerian_banks_ifrs9_thesis_data.docx | 58,515 | thesis data document (unpublished research text) |

Also tracked: the derived registers in `data/`, `outputs/` (workbook, summary, handoff zip with page images of
public annual reports), `tasks/`, `state/` (download ledger with public URLs) and `checks/`.
Source PDFs (`reports/*`) are gitignored and not published.

## Owner decision needed
If the thesis data and draft should not be public before submission, make the repository private, or remove
`inputs/` in a new commit. Removing it from *history* requires a history rewrite, which has not been done.
