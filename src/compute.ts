import { IFRS_BREAK } from "./years.js";
import type { PanelMetricRow, PanelRawRow } from "./types.js";

const safeDiv = (a: number | null, b: number | null): number | null => {
  if (a === null || b === null || b === 0) return null;
  return a / b;
};

export function computeMetrics(row: PanelRawRow): PanelMetricRow {
  const ifrs_dummy = row.year >= IFRS_BREAK ? 1 : 0;
  const roa = safeDiv(row.net_income, row.total_assets);
  const current_ratio = safeDiv(row.current_assets, row.current_liabilities);
  const leverage_ratio = safeDiv(row.total_liabilities, row.total_assets);
  const interest_coverage = safeDiv(row.EBIT, row.interest_expense);

  const x1 = safeDiv(
    row.current_assets !== null && row.current_liabilities !== null
      ? row.current_assets - row.current_liabilities
      : null,
    row.total_assets,
  );
  const x2 = safeDiv(row.retained_earnings, row.total_assets);
  const x3 = safeDiv(row.EBIT, row.total_assets);
  const x4 = safeDiv(row.equity, row.total_liabilities);

  const altman_z_modified =
    x1 === null || x2 === null || x3 === null || x4 === null
      ? null
      : 6.56 * x1 + 3.26 * x2 + 6.72 * x3 + 1.05 * x4;

  return {
    ...row,
    ifrs_dummy,
    roa,
    current_ratio,
    leverage_ratio,
    interest_coverage,
    altman_z_modified,
    validation_flags: [],
  };
}
