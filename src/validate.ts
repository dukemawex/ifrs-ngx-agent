import type { PanelMetricRow } from "./types.js";

const REQUIRED_NUMERIC_FIELDS: Array<keyof PanelMetricRow> = [
  "total_assets",
  "total_liabilities",
  "equity",
  "revenue",
  "EBIT",
  "interest_expense",
  "net_income",
  "current_assets",
  "current_liabilities",
  "total_debt",
];

export function validateRow(row: PanelMetricRow): PanelMetricRow {
  const flags: string[] = [];

  for (const field of REQUIRED_NUMERIC_FIELDS) {
    const value = row[field];
    if (value === null || value === undefined || Number.isNaN(Number(value))) {
      flags.push(`missing_${String(field)}`);
    }
  }

  if ((row.total_assets ?? 0) < 0) flags.push("negative_total_assets");
  if ((row.total_liabilities ?? 0) < 0) flags.push("negative_total_liabilities");

  if (
    row.total_assets !== null &&
    row.total_liabilities !== null &&
    row.equity !== null &&
    Math.abs(row.total_assets - (row.total_liabilities + row.equity)) > Math.max(1, row.total_assets * 0.05)
  ) {
    flags.push("balance_sheet_mismatch_gt_5pct");
  }

  return {
    ...row,
    validation_flags: flags,
  };
}

export function summarizeMissingness(rows: PanelMetricRow[]): Record<string, number> {
  const summary: Record<string, number> = {};
  for (const row of rows) {
    for (const field of REQUIRED_NUMERIC_FIELDS) {
      const value = row[field];
      if (value === null || value === undefined || Number.isNaN(Number(value))) {
        const key = `missing_${String(field)}`;
        summary[key] = (summary[key] ?? 0) + 1;
      }
    }
  }
  return summary;
}
