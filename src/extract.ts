import { tavilySearch, tavilyExtract } from "./tavily.js";
import type { ExtractedFinancials } from "./types.js";

// ---------- unit detection & scaling ----------

export type DetectedUnit = {
  label: string;
  factor: number;
};

const UNIT_PATTERNS: Array<{ pattern: RegExp; label: string; factor: number }> = [
  { pattern: /₦[''']?\s*billion/i, label: "₦'billion", factor: 1_000_000_000 },
  { pattern: /NGN[''']?\s*billion/i, label: "NGN'billion", factor: 1_000_000_000 },
  { pattern: /₦[''']?\s*million/i, label: "₦'million", factor: 1_000_000 },
  { pattern: /NGN[''']?\s*million/i, label: "NGN'million", factor: 1_000_000 },
  { pattern: /₦[''']?\s*000/i, label: "₦'000", factor: 1_000 },
  { pattern: /NGN[''']?\s*000/i, label: "NGN'000", factor: 1_000 },
  { pattern: /in\s*thousands/i, label: "thousands", factor: 1_000 },
  { pattern: /in\s*millions/i, label: "millions", factor: 1_000_000 },
  { pattern: /in\s*billions/i, label: "billions", factor: 1_000_000_000 },
  { pattern: /₦/i, label: "₦", factor: 1 },
  { pattern: /NGN/i, label: "NGN", factor: 1 },
];

export function detectUnit(content: string): DetectedUnit {
  for (const { pattern, label, factor } of UNIT_PATTERNS) {
    if (pattern.test(content)) {
      return { label, factor };
    }
  }
  return { label: "unknown", factor: 1 };
}

export function applyScaling(
  value: number | null,
  factor: number,
): number | null {
  if (value === null) return null;
  return value * factor;
}

// ---------- validation gates ----------

export function validateExtractedContent(
  content: string,
  companyName: string,
  aliases: string[],
  ticker: string,
  year: number,
): { valid: boolean; reasons: string[] } {
  const reasons: string[] = [];
  const lower = content.toLowerCase();

  // Must contain firm name or ticker
  const nameFound = [companyName, ticker, ...aliases].some(
    (n) => lower.includes(n.toLowerCase()),
  );
  if (!nameFound) reasons.push("firm_name_not_found");

  // Must contain the year
  if (!content.includes(String(year))) reasons.push("year_not_found");

  // Must contain a currency/unit marker
  const hasUnit = /₦|NGN|naira/i.test(content);
  if (!hasUnit) reasons.push("unit_marker_not_found");

  return { valid: reasons.length === 0, reasons };
}

// ---------- plausibility checks ----------

const MIN_ASSET_NGN = 1_000_000;         // ₦1 million
const MAX_ASSET_NGN = 50_000_000_000_000; // ₦50 trillion

export function plausibilityCheck(
  financials: Partial<ExtractedFinancials>,
): { ok: boolean; flags: string[] } {
  const flags: string[] = [];
  const assets = financials.total_assets;
  if (assets !== null && assets !== undefined) {
    if (assets < MIN_ASSET_NGN) flags.push("total_assets_too_small");
    if (assets > MAX_ASSET_NGN) flags.push("total_assets_too_large");
  }
  const revenue = financials.revenue;
  if (revenue !== null && revenue !== undefined) {
    if (revenue < 0) flags.push("negative_revenue");
    if (revenue > MAX_ASSET_NGN) flags.push("revenue_too_large");
  }
  const equity = financials.equity;
  if (equity !== null && equity !== undefined) {
    if (equity > MAX_ASSET_NGN) flags.push("equity_too_large");
  }
  return { ok: flags.length === 0, flags };
}

// ---------- text parsing helpers ----------

function parseNumberFromText(text: string): number | null {
  const cleaned = text.replace(/[,\s]/g, "").replace(/\((.+)\)/, "-$1");
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
  ]);
  result.profit_before_tax = extractFieldFromContent(content, [
    /profit\s*before\s*(?:interest\s*and\s*)?tax(?:ation)?[:\s]+([-\d,.()]+)/i,
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

function scaleFinancials(
  partial: Partial<ExtractedFinancials>,
  factor: number,
): Partial<ExtractedFinancials> {
  const numericKeys: Array<keyof ExtractedFinancials> = [
    "total_assets", "total_liabilities", "equity", "revenue",
    "EBIT", "profit_before_tax", "interest_expense", "net_income",
    "current_assets", "current_liabilities", "total_debt", "retained_earnings",
  ];
  const scaled = { ...partial };
  for (const key of numericKeys) {
    const val = scaled[key];
    if (typeof val === "number") {
      (scaled as Record<string, unknown>)[key] = val * factor;
    }
  }
  return scaled;
}

function normalizeExtracted(
  partial: Partial<ExtractedFinancials>,
  notes: string,
  unit: DetectedUnit,
): ExtractedFinancials {
  return {
    total_assets: partial.total_assets ?? null,
    total_liabilities: partial.total_liabilities ?? null,
    equity: partial.equity ?? null,
    revenue: partial.revenue ?? null,
    EBIT: partial.EBIT ?? null,
    profit_before_tax: partial.profit_before_tax ?? null,
    EBIT_computed: false,
    interest_expense: partial.interest_expense ?? null,
    net_income: partial.net_income ?? null,
    current_assets: partial.current_assets ?? null,
    current_liabilities: partial.current_liabilities ?? null,
    total_debt: partial.total_debt ?? null,
    retained_earnings: partial.retained_earnings ?? null,
    scaling_factor: unit.factor,
    detected_unit: unit.label,
    evidence_hints: {},
    extraction_notes: notes,
  };
}

export type ExtractionResult = {
  financials: ExtractedFinancials;
  validationResults: { valid: boolean; reasons: string[] };
  plausibilityFlags: string[];
  urlsConsidered: string[];
  chosenUrl: string | null;
  parseConfidence: number;
};

export async function extractFinancials(
  company: string,
  aliases: string[],
  ticker: string,
  year: number,
  url: string,
  apiKey: string,
): Promise<ExtractionResult> {
  const notes: string[] = [];
  const urlsConsidered: string[] = [url];
  let chosenUrl: string | null = url;
  let allContent = "";

  // Step 1: Try extracting content from the discovered URL with advanced depth.
  let merged: Partial<ExtractedFinancials> = {};

  try {
    const extracted = await tavilyExtract([url], apiKey, { extract_depth: "advanced" });
    if (extracted.results.length > 0) {
      const content = extracted.results[0].raw_content;
      allContent += content + "\n";
      merged = { ...merged, ...extractFromText(content) };
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

    const searchContent = [
      searchRes.answer ?? "",
      ...searchRes.results.map((r) => r.content),
    ].join("\n");
    allContent += searchContent + "\n";

    for (const r of searchRes.results) {
      if (!urlsConsidered.includes(r.url)) urlsConsidered.push(r.url);
    }

    const fromSearch = extractFromText(searchContent);

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

  // Step 3: Detect unit and apply scaling.
  const unit = detectUnit(allContent);
  merged = scaleFinancials(merged, unit.factor);
  notes.push(`Detected unit: ${unit.label} (factor=${unit.factor})`);

  // Step 4: Validate that content mentions firm, year, and unit.
  const validationResults = validateExtractedContent(
    allContent, company, aliases, ticker, year,
  );
  if (!validationResults.valid) {
    notes.push(`Validation warnings: ${validationResults.reasons.join(", ")}`);
  }

  // Step 5: Plausibility check on scaled values.
  const plausibility = plausibilityCheck(merged);
  if (!plausibility.ok) {
    notes.push(`Plausibility flags: ${plausibility.flags.join(", ")}`);
    // Discard implausible values
    for (const flag of plausibility.flags) {
      if (flag === "total_assets_too_small" || flag === "total_assets_too_large") merged.total_assets = null;
      if (flag === "negative_revenue" || flag === "revenue_too_large") merged.revenue = null;
      if (flag === "equity_too_large") merged.equity = null;
    }
  }

  // Compute parse confidence: ratio of non-null financial fields out of 11 key fields.
  const keyFields: Array<keyof ExtractedFinancials> = [
    "total_assets", "total_liabilities", "equity", "revenue", "EBIT",
    "profit_before_tax", "interest_expense", "net_income", "current_assets",
    "current_liabilities", "total_debt",
  ];
  const filled = keyFields.filter((k) => merged[k] != null).length;
  const parseConfidence = filled / keyFields.length;

  return {
    financials: normalizeExtracted(merged, notes.join("; "), unit),
    validationResults,
    plausibilityFlags: plausibility.flags,
    urlsConsidered,
    chosenUrl,
    parseConfidence,
  };
}
