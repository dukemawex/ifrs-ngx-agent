import { tavilySearch, tavilyExtract } from "./tavily.js";
import type { ExtractedFinancials } from "./types.js";

function num(obj: Record<string, unknown>, key: string): number | null {
  const value = obj[key];
  if (value === null || value === undefined || value === "") return null;
  const n = Number(value);
  return Number.isFinite(n) ? n : null;
}

function parseNumberFromText(text: string): number | null {
  const cleaned = text.replace(/[,\s]/g, "");
  const match = cleaned.match(/-?[\d.]+/);
  if (!match) return null;
  const n = Number(match[0]);
  return Number.isFinite(n) ? n : null;
}

function extractFieldFromContent(
  content: string,
  patterns: RegExp[],
): number | null {
  for (const pat of patterns) {
    const m = content.match(pat);
    if (m) {
      const v = parseNumberFromText(m[1] ?? m[0]);
      if (v !== null) return v;
    }
  }
  return null;
}

function extractFromText(content: string): Partial<ExtractedFinancials> {
  const result: Partial<ExtractedFinancials> = {};

  result.total_assets = extractFieldFromContent(content, [
    /total\s*assets[:\s]+([-\d,.()]+)/i,
  ]);
  result.total_liabilities = extractFieldFromContent(content, [
    /total\s*liabilities[:\s]+([-\d,.()]+)/i,
  ]);
  result.equity = extractFieldFromContent(content, [
    /(?:total\s*)?(?:shareholders[''']?\s*)?equity[:\s]+([-\d,.()]+)/i,
  ]);
  result.revenue = extractFieldFromContent(content, [
    /(?:total\s*)?revenue[:\s]+([-\d,.()]+)/i,
    /turnover[:\s]+([-\d,.()]+)/i,
  ]);
  result.net_income = extractFieldFromContent(content, [
    /net\s*(?:income|profit)[:\s]+([-\d,.()]+)/i,
    /profit\s*(?:for\s*the\s*year|after\s*tax)[:\s]+([-\d,.()]+)/i,
  ]);
  result.EBIT = extractFieldFromContent(content, [
    /(?:EBIT|operating\s*(?:profit|income))[:\s]+([-\d,.()]+)/i,
    /profit\s*before\s*(?:interest\s*and\s*)?tax[:\s]+([-\d,.()]+)/i,
  ]);
  result.interest_expense = extractFieldFromContent(content, [
    /(?:interest|finance)\s*(?:expense|cost)[:\s]+([-\d,.()]+)/i,
  ]);
  result.current_assets = extractFieldFromContent(content, [
    /current\s*assets[:\s]+([-\d,.()]+)/i,
  ]);
  result.current_liabilities = extractFieldFromContent(content, [
    /current\s*liabilities[:\s]+([-\d,.()]+)/i,
  ]);
  result.total_debt = extractFieldFromContent(content, [
    /total\s*(?:debt|borrowings)[:\s]+([-\d,.()]+)/i,
  ]);
  result.retained_earnings = extractFieldFromContent(content, [
    /retained\s*earnings[:\s]+([-\d,.()]+)/i,
  ]);

  return result;
}

function normalizeExtracted(partial: Partial<ExtractedFinancials>, notes: string): ExtractedFinancials {
  return {
    total_assets: partial.total_assets ?? null,
    total_liabilities: partial.total_liabilities ?? null,
    equity: partial.equity ?? null,
    revenue: partial.revenue ?? null,
    EBIT: partial.EBIT ?? null,
    EBIT_computed: false,
    interest_expense: partial.interest_expense ?? null,
    net_income: partial.net_income ?? null,
    current_assets: partial.current_assets ?? null,
    current_liabilities: partial.current_liabilities ?? null,
    total_debt: partial.total_debt ?? null,
    retained_earnings: partial.retained_earnings ?? null,
    evidence_hints: {},
    extraction_notes: notes,
  };
}

export async function extractFinancials(
  company: string,
  year: number,
  url: string,
  apiKey: string,
): Promise<ExtractedFinancials> {
  const notes: string[] = [];

  // Step 1: Try extracting content from the discovered URL.
  let merged: Partial<ExtractedFinancials> = {};

  try {
    const extracted = await tavilyExtract([url], apiKey);
    if (extracted.results.length > 0) {
      merged = { ...merged, ...extractFromText(extracted.results[0].raw_content) };
      notes.push(`Extracted content from ${url}`);
    }
  } catch (err) {
    notes.push(`Extract from URL failed: ${String(err)}`);
  }

  // Step 2: Supplement with a targeted Tavily search for financial data.
  try {
    const query = `"${company}" ${year} total assets revenue net income financial statements Nigeria`;
    const searchRes = await tavilySearch(query, apiKey, {
      search_depth: "advanced",
      max_results: 5,
      include_answer: true,
    });

    const allContent = [
      searchRes.answer ?? "",
      ...searchRes.results.map((r) => r.content),
    ].join("\n");

    const fromSearch = extractFromText(allContent);

    // Only fill fields that are still null.
    for (const [key, value] of Object.entries(fromSearch)) {
      if (value !== null && (merged as Record<string, unknown>)[key] == null) {
        (merged as Record<string, unknown>)[key] = value;
      }
    }
    notes.push(`Supplemented with Tavily search (${searchRes.results.length} results)`);
  } catch (err) {
    notes.push(`Supplemental search failed: ${String(err)}`);
  }

  return normalizeExtracted(merged, notes.join("; "));
}
