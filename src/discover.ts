import { tavilySearch } from "./tavily.js";
import type { DiscoveryCandidate, SourceType } from "./types.js";

const SOURCE_PRIORITY: Record<string, number> = {
  official_ir: 5,
  ngx_doclib: 4,
  africanfinancials: 3,
  archive: 2,
  mirror: 1,
};

function classifySource(url: string): SourceType {
  const lower = url.toLowerCase();
  if (lower.includes("africanfinancials")) return "africanfinancials";
  if (lower.includes("ngxgroup.com") || lower.includes("ngx.com.ng")) return "ngx_doclib";
  if (lower.includes("archive.org")) return "archive";
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
