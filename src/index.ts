import "dotenv/config";
import { TARGETS } from "./targets.js";
import { YEARS } from "./years.js";
import { discoverReportUrls } from "./discover.js";
import { extractFinancials } from "./extract.js";
import { computeMetrics } from "./compute.js";
import { exportOutputs } from "./export.js";
import { summarizeMissingness, validateRow } from "./validate.js";
import type { AuditTrailEvent, PanelMetricRow, PanelRawRow } from "./types.js";

const API_KEY = process.env.TAVILY_API_KEY;
const RETRIES = 3;
const BASE_BACKOFF_MS = 2000;
const POLITE_DELAY_MS = 1200;

const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

async function withRetry<T>(label: string, fn: () => Promise<T>): Promise<T> {
  let lastErr: unknown;
  for (let attempt = 1; attempt <= RETRIES; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastErr = error;
      const backoff = BASE_BACKOFF_MS * attempt;
      console.warn(`[retry ${attempt}/${RETRIES}] ${label}: ${String(error)}`);
      await sleep(backoff);
    }
  }
  throw new Error(`${label} failed after ${RETRIES} retries: ${String(lastErr)}`);
}

function audit(
  trail: AuditTrailEvent[],
  company_id: string,
  year: number,
  step: string,
  ok: boolean,
  details: Record<string, unknown>,
): void {
  trail.push({
    ts: new Date().toISOString(),
    company_id,
    year,
    step,
    ok,
    details,
  });
}

async function main(): Promise<void> {
  if (!API_KEY) {
    throw new Error("Missing TAVILY_API_KEY environment variable.");
  }

  const rawRows: PanelRawRow[] = [];
  const metricRows: PanelMetricRow[] = [];
  const auditTrail: AuditTrailEvent[] = [];

  for (const company of TARGETS) {
    for (const year of YEARS) {
      console.log(`\n=== ${company.name} (${year}) ===`);
      let sourceUrl: string | null = null;
      let sourceType: PanelRawRow["source_type"] = null;

      try {
        const candidates = await withRetry("discoverReportUrls", () =>
          discoverReportUrls(company.name, company.aliases, year, API_KEY),
        );
        audit(auditTrail, company.id, year, "discover", true, {
          candidate_count: candidates.length,
          top_candidate: candidates[0] ?? null,
        });

        if (candidates.length > 0) {
          sourceUrl = candidates[0].url;
          sourceType = candidates[0].source_type;
        }

        if (!sourceUrl) {
          throw new Error("No candidate URLs discovered");
        }

        await sleep(POLITE_DELAY_MS);

        const extracted = await withRetry("extractFinancials", () =>
          extractFinancials(company.name, year, sourceUrl as string, API_KEY),
        );

        const rawRow: PanelRawRow = {
          company_id: company.id,
          company_name: company.name,
          year,
          ifrs_dummy: 0,
          source_url: sourceUrl,
          source_type: sourceType,
          ...extracted,
        };

        const metricRow = validateRow(computeMetrics(rawRow));

        rawRows.push({ ...rawRow, ifrs_dummy: metricRow.ifrs_dummy });
        metricRows.push(metricRow);

        audit(auditTrail, company.id, year, "extract_compute_validate", true, {
          source_url: sourceUrl,
          source_type: sourceType,
          validation_flags: metricRow.validation_flags,
        });
      } catch (error) {
        audit(auditTrail, company.id, year, "pipeline", false, {
          error: String(error),
          source_url: sourceUrl,
          source_type: sourceType,
        });
      }

      await sleep(POLITE_DELAY_MS);
    }
  }

  const missingness = summarizeMissingness(metricRows);
  auditTrail.push({
    ts: new Date().toISOString(),
    company_id: "ALL",
    year: 0,
    step: "missingness_summary",
    ok: true,
    details: missingness,
  });

  await exportOutputs(rawRows, metricRows, auditTrail);
  console.log(`Exported ${rawRows.length} raw rows and ${metricRows.length} metric rows.`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
