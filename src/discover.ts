import { readFile } from "node:fs/promises";
import { runTinyFishAutomation } from "./tinyfish.js";
import type { DiscoveryCandidate } from "./types.js";

const SOURCE_PRIORITY: Record<string, number> = {
  official_ir: 5,
  ngx_doclib: 4,
  africanfinancials: 3,
  archive: 2,
  mirror: 1,
};

function toArray(value: unknown): DiscoveryCandidate[] {
  if (!Array.isArray(value)) return [];
  return value
    .map((v) => {
      if (!v || typeof v !== "object") return null;
      const x = v as Record<string, unknown>;
      return {
        url: String(x.url ?? ""),
        source_type: String(x.source_type ?? "mirror") as DiscoveryCandidate["source_type"],
        confidence: Number(x.confidence ?? 0),
        notes: String(x.notes ?? ""),
      };
    })
    .filter((x): x is DiscoveryCandidate => Boolean(x && x.url));
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
  const template = await readFile("prompts/discover_report_urls.md", "utf8");
  const goal = template
    .replace("{{company}}", company)
    .replace("{{aliases}}", aliases.join(", "))
    .replace(/{{year}}/g, String(year));

  const result = await runTinyFishAutomation({ goal, browser_profile: "stealth" }, apiKey);
  return rankCandidates(toArray(result.resultJson));
}
