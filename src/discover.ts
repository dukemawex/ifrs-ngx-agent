import { tavilySearch } from "./tavily.js";
import type { DiscoveryCandidate, SourceType } from "./types.js";

const SOURCE_PRIORITY: Record<string, number> = {
  official_ir: 5,
  ngx_doclib: 4,
  africanfinancials: 3,
  archive: 2,
  mirror: 1,
};

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

export async function discoverReportUrls(
  company: string,
  aliases: string[],
  year: number,
  apiKey: string,
): Promise<DiscoveryCandidate[]> {
  const names = [company, ...aliases].slice(0, 3);
  const query = `${names.join(" OR ")} annual report ${year} financial statements Nigeria NGX filetype:pdf`;

  const response = await tavilySearch(query, apiKey, {
    search_depth: "advanced",
    max_results: 10,
  });

  const candidates: DiscoveryCandidate[] = response.results.map((r) => ({
    url: r.url,
    source_type: classifySource(r.url),
    confidence: r.score,
    notes: r.title,
  }));

  return rankCandidates(candidates);
}
