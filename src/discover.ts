import { tavilySearch } from "./tavily.js";
import type { DiscoveryCandidate, SourceType } from "./types.js";
import type { TargetCompany } from "./targets.js";

const SOURCE_PRIORITY: Record<string, number> = {
  official_ir: 5,
  ngx_doclib: 4,
  africanfinancials: 3,
  archive: 2,
  mirror: 1,
};

const PREFERRED_DOMAINS = [
  "doclib.ngxgroup.com",
  "ngxgroup.com",
  "ngx.com.ng",
  "africanfinancials.com",
];

function hostMatches(hostname: string, domain: string): boolean {
  return hostname === domain || hostname.endsWith("." + domain);
}

function classifySource(url: string): SourceType {
  let hostname = "";
  try {
    hostname = new URL(url).hostname.toLowerCase();
  } catch {
    // If URL parsing fails, fall through to mirror.
  }

  if (hostMatches(hostname, "africanfinancials.com"))
    return "africanfinancials";
  if (hostMatches(hostname, "ngxgroup.com") || hostMatches(hostname, "ngx.com.ng"))
    return "ngx_doclib";
  if (hostMatches(hostname, "archive.org"))
    return "archive";

  const lower = url.toLowerCase();
  if (
    lower.includes("investor") ||
    lower.includes("annual-report") ||
    lower.includes("annualreport")
  )
    return "official_ir";
  return "mirror";
}

export function rankCandidates(candidates: DiscoveryCandidate[]): DiscoveryCandidate[] {
  return [...candidates].sort((a, b) => {
    const pdfA = a.url.toLowerCase().includes(".pdf") ? 1 : 0;
    const pdfB = b.url.toLowerCase().includes(".pdf") ? 1 : 0;
    const priorityA = SOURCE_PRIORITY[a.source_type] ?? 0;
    const priorityB = SOURCE_PRIORITY[b.source_type] ?? 0;

    return (
      pdfB - pdfA ||
      priorityB - priorityA ||
      b.confidence - a.confidence ||
      a.url.localeCompare(b.url)
    );
  });
}

/**
 * Build exclude_domains to prevent cross-company contamination.
 * Excludes domains containing other companies' names.
 */
function buildExcludeDomains(company: TargetCompany, allCompanies: TargetCompany[]): string[] {
  const excluded: string[] = [];
  for (const other of allCompanies) {
    if (other.id === company.id) continue;
    // Exclude domains that might host other companies' data
    const lowerName = other.name.toLowerCase().replace(/\s+plc$/i, "").trim();
    const slug = lowerName.replace(/\s+/g, "");
    if (slug.length > 3) {
      excluded.push(`${slug}.com`, `${slug}.com.ng`);
    }
  }
  return excluded;
}

export async function discoverReportUrls(
  company: TargetCompany,
  allCompanies: TargetCompany[],
  year: number,
  apiKey: string,
): Promise<DiscoveryCandidate[]> {
  const names = [company.name, ...company.aliases].slice(0, 3);
  const query = `${names.join(" OR ")} annual report ${year} financial statements Nigeria NGX filetype:pdf`;

  const excludeDomains = buildExcludeDomains(company, allCompanies);

  const response = await tavilySearch(query, apiKey, {
    search_depth: "advanced",
    max_results: 8,
    include_domains: PREFERRED_DOMAINS,
    exclude_domains: excludeDomains,
  });

  let candidates: DiscoveryCandidate[] = response.results.map((r) => ({
    url: r.url,
    source_type: classifySource(r.url),
    confidence: r.score,
    notes: r.title,
  }));

  // If preferred domains yielded few results, do a broader search without include_domains
  if (candidates.length < 3) {
    const broader = await tavilySearch(query, apiKey, {
      search_depth: "advanced",
      max_results: 5,
      exclude_domains: excludeDomains,
    });
    const existing = new Set(candidates.map((c) => c.url));
    for (const r of broader.results) {
      if (!existing.has(r.url)) {
        candidates.push({
          url: r.url,
          source_type: classifySource(r.url),
          confidence: r.score,
          notes: r.title,
        });
      }
    }
  }

  return rankCandidates(candidates);
}
