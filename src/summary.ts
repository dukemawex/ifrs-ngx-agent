import { tavilySearch } from "./tavily.js";
import { IFRS_BREAK } from "./years.js";
import type { TargetCompany } from "./targets.js";
import type {
  FinancialSummary,
  IFRSAdoption,
  PanelMetricRow,
  PeriodData,
  YearlyMetrics,
} from "./types.js";

// Nigeria mandated IFRS adoption for listed companies effective 1 Jan 2012.
const NIGERIA_DEFAULT_IFRS_YEAR = 2012;

/**
 * Attempt to determine the IFRS adoption year for a company via Tavily search.
 * Falls back to the Nigerian default (2012) if no credible source is found.
 */
export async function determineIFRSAdoptionYear(
  company: TargetCompany,
  apiKey: string,
): Promise<IFRSAdoption> {
  try {
    const query = `"${company.name}" IFRS adoption year Nigeria financial reporting standards`;
    const res = await tavilySearch(query, apiKey, {
      search_depth: "basic",
      max_results: 5,
      include_answer: true,
    });

    // Look for a 4-digit year near "IFRS" or "adopt" in the answer / results
    const texts = [res.answer ?? "", ...res.results.map((r) => r.content)];
    for (const text of texts) {
      const match = text.match(/(?:IFRS|adopt\w*)\D{0,40}(20[01]\d)/i);
      if (match) {
        const year = Number(match[1]);
        if (year >= 2010 && year <= 2015) {
          const sourceUrl = res.results[0]?.url ?? "";
          return {
            adoption_year: year,
            source_url: sourceUrl,
            notes: `Found adoption year ${year} via Tavily search`,
          };
        }
      }
    }

    return {
      adoption_year: NIGERIA_DEFAULT_IFRS_YEAR,
      source_url: res.results[0]?.url ?? "",
      notes: "Used Nigeria default IFRS adoption year (2012) – no company-specific year found",
    };
  } catch (err) {
    return {
      adoption_year: NIGERIA_DEFAULT_IFRS_YEAR,
      source_url: "",
      notes: `Defaulted to Nigeria IFRS year (2012) due to search error: ${String(err)}`,
    };
  }
}

function toYearlyMetrics(row: PanelMetricRow): YearlyMetrics {
  return {
    revenue: row.revenue,
    profit_before_tax: row.profit_before_tax ?? row.EBIT,
    net_income: row.net_income,
    total_assets: row.total_assets,
    total_liabilities: row.total_liabilities,
    equity: row.equity,
    eps: null,
    dividends: null,
  };
}

/**
 * Build a FinancialSummary object for a single company from its metric rows.
 */
export function buildFinancialSummary(
  company: TargetCompany,
  ifrs: IFRSAdoption,
  rows: PanelMetricRow[],
): FinancialSummary {
  const breakYear = ifrs.adoption_year ?? IFRS_BREAK;

  const preRows = rows.filter((r) => r.year < breakYear);
  const postRows = rows.filter((r) => r.year >= breakYear);

  const toPeriod = (subset: PanelMetricRow[]): PeriodData => ({
    years: subset.map((r) => r.year).sort((a, b) => a - b),
    metrics: Object.fromEntries(subset.map((r) => [r.year, toYearlyMetrics(r)])),
    sources: [...new Set(subset.map((r) => r.source_url).filter(Boolean) as string[])],
  });

  return {
    company: { name: company.name, ticker: company.ticker, exchange: "NGX" },
    ifrs,
    periods: { pre_ifrs: toPeriod(preRows), post_ifrs: toPeriod(postRows) },
    currency: "NGN",
    notes: "",
    generated_at: new Date().toISOString(),
  };
}
