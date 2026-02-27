import { mkdir, writeFile } from "node:fs/promises";
import type { AuditTrailEvent, FinancialSummary, PanelMetricRow, PanelRawRow } from "./types.js";

function escapeCsv(value: unknown): string {
  if (value === null || value === undefined) return "";
  const s = typeof value === "string" ? value : JSON.stringify(value);
  if (/[",\n]/.test(s)) {
    return `"${s.replace(/"/g, '""')}"`;
  }
  return s;
}

function toCsv<T extends Record<string, unknown>>(rows: T[]): string {
  if (rows.length === 0) return "";
  const headers = Object.keys(rows[0]);
  const body = rows.map((r) => headers.map((h) => escapeCsv(r[h])).join(",")).join("\n");
  return `${headers.join(",")}\n${body}\n`;
}

export async function exportOutputs(
  rawRows: PanelRawRow[],
  metricRows: PanelMetricRow[],
  auditTrail: AuditTrailEvent[],
  summaries?: FinancialSummary[],
): Promise<void> {
  await mkdir("data/processed", { recursive: true });

  await writeFile("data/processed/panel_raw.csv", toCsv(rawRows), "utf8");
  await writeFile("data/processed/panel_metrics.csv", toCsv(metricRows), "utf8");
  await writeFile(
    "data/processed/audit_trail.jsonl",
    auditTrail.map((x) => JSON.stringify(x)).join("\n") + (auditTrail.length ? "\n" : ""),
    "utf8",
  );

  if (summaries && summaries.length > 0) {
    await writeFile(
      "data/processed/financial_summaries.json",
      JSON.stringify(summaries, null, 2) + "\n",
      "utf8",
    );
  }
}
