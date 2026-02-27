import { readFile } from "node:fs/promises";
import { runTavilyAutomation } from "./tavily.js";
import type { ExtractedFinancials } from "./types.js";

function normalizeExtracted(input: unknown): ExtractedFinancials {
  const obj = (input && typeof input === "object" ? input : {}) as Record<string, unknown>;
  const num = (key: string): number | null => {
    const value = obj[key];
    if (value === null || value === undefined || value === "") return null;
    const n = Number(value);
    return Number.isFinite(n) ? n : null;
  };

  return {
    total_assets: num("total_assets"),
    total_liabilities: num("total_liabilities"),
    equity: num("equity"),
    revenue: num("revenue"),
    EBIT: num("EBIT"),
    EBIT_computed: Boolean(obj.EBIT_computed),
    interest_expense: num("interest_expense"),
    net_income: num("net_income"),
    current_assets: num("current_assets"),
    current_liabilities: num("current_liabilities"),
    total_debt: num("total_debt"),
    retained_earnings: num("retained_earnings"),
    evidence_hints:
      obj.evidence_hints && typeof obj.evidence_hints === "object"
        ? (obj.evidence_hints as Record<string, string>)
        : {},
    extraction_notes: String(obj.extraction_notes ?? ""),
  };
}

export async function extractFinancials(
  company: string,
  year: number,
  url: string,
  apiKey: string,
): Promise<ExtractedFinancials> {
  const template = await readFile("prompts/extract_financials.md", "utf8");
  const goal = template
    .replace("{{company}}", company)
    .replace("{{year}}", String(year))
    .replace("{{url}}", url);

  const result = await runTavilyAutomation({ goal, browser_profile: "stealth" }, apiKey);
  return normalizeExtracted(result.resultJson);
}
