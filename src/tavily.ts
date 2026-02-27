const TAVILY_SEARCH_URL = "https://api.tavily.com/search";
const TAVILY_EXTRACT_URL = "https://api.tavily.com/extract";

const DEFAULT_TIMEOUT_MS = 30_000;
const MAX_RETRIES = 3;
const BASE_BACKOFF_MS = 1_000;
const MAX_CONCURRENT = 2;

// ---------- public types ----------

export type TavilySearchOptions = {
  search_depth?: "basic" | "advanced";
  max_results?: number;
  include_answer?: boolean;
  include_raw_content?: boolean;
  include_domains?: string[];
  exclude_domains?: string[];
};

export type TavilySearchResult = {
  title: string;
  url: string;
  content: string;
  score: number;
  raw_content?: string | null;
};

export type TavilySearchResponse = {
  query: string;
  answer?: string;
  results: TavilySearchResult[];
  response_time: number;
};

export type TavilyExtractResult = {
  url: string;
  raw_content: string;
};

export type TavilyExtractResponse = {
  results: TavilyExtractResult[];
  failed_results?: { url: string; error: string }[];
};

export type TavilyExtractOptions = {
  extract_depth?: "basic" | "advanced";
};

// ---------- concurrency limiter ----------

let activeRequests = 0;
const waitQueue: Array<() => void> = [];

async function acquireConcurrency(): Promise<void> {
  if (activeRequests < MAX_CONCURRENT) {
    activeRequests++;
    return;
  }
  await new Promise<void>((resolve) => waitQueue.push(resolve));
  activeRequests++;
}

function releaseConcurrency(): void {
  activeRequests--;
  const next = waitQueue.shift();
  if (next) next();
}

// ---------- helpers ----------

function jitter(ms: number): number {
  return ms + Math.random() * ms * 0.5;
}

function isRetryable(status: number): boolean {
  return status === 429 || (status >= 500 && status <= 599);
}

async function tavilyFetch<T>(
  url: string,
  body: Record<string, unknown>,
  apiKey: string,
): Promise<T> {
  let lastErr: unknown;

  for (let attempt = 1; attempt <= MAX_RETRIES; attempt++) {
    await acquireConcurrency();
    try {
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), DEFAULT_TIMEOUT_MS);

      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ api_key: apiKey, ...body }),
        signal: controller.signal,
      });

      clearTimeout(timer);

      if (!response.ok) {
        const snippet = await response.text().catch(() => "");
        if (isRetryable(response.status) && attempt < MAX_RETRIES) {
          const wait = jitter(BASE_BACKOFF_MS * 2 ** (attempt - 1));
          console.warn(
            `[tavily] ${url} returned ${response.status}, retrying in ${Math.round(wait)}ms (attempt ${attempt}/${MAX_RETRIES})`,
          );
          await new Promise((r) => setTimeout(r, wait));
          continue;
        }
        throw new Error(
          `Tavily request failed: ${response.status} ${response.statusText} – ${snippet.slice(0, 200)}`,
        );
      }

      return (await response.json()) as T;
    } catch (err) {
      lastErr = err;
      if (
        attempt < MAX_RETRIES &&
        (err instanceof DOMException || (err instanceof TypeError && /fetch|network/i.test(String(err))))
      ) {
        const wait = jitter(BASE_BACKOFF_MS * 2 ** (attempt - 1));
        console.warn(`[tavily] network error, retrying in ${Math.round(wait)}ms (attempt ${attempt}/${MAX_RETRIES})`);
        await new Promise((r) => setTimeout(r, wait));
        continue;
      }
      throw err;
    } finally {
      releaseConcurrency();
    }
  }

  throw new Error(`Tavily request to ${url} failed after ${MAX_RETRIES} retries: ${String(lastErr)}`);
}

// ---------- public API ----------

/**
 * Validate the API key is present. Call once at startup; throws if missing.
 */
export function validateApiKey(apiKey: string | undefined): asserts apiKey is string {
  if (!apiKey || apiKey.trim().length === 0) {
    throw new Error(
      "TAVILY_API_KEY is not set. Provide it via environment variable. " +
        "See .env.example for details.",
    );
  }
  console.log("[tavily] API key validated (key not logged).");
}

/**
 * Tavily Search – returns ranked web results for a query.
 */
export async function tavilySearch(
  query: string,
  apiKey: string,
  options: TavilySearchOptions = {},
): Promise<TavilySearchResponse> {
  console.log(`[tavily:search] query="${query.slice(0, 120)}…"`);
  const body: Record<string, unknown> = {
    query,
    search_depth: options.search_depth ?? "advanced",
    max_results: options.max_results ?? 10,
    include_answer: options.include_answer ?? false,
    include_raw_content: options.include_raw_content ?? false,
  };
  if (options.include_domains?.length) body.include_domains = options.include_domains;
  if (options.exclude_domains?.length) body.exclude_domains = options.exclude_domains;

  const res = await tavilyFetch<TavilySearchResponse>(TAVILY_SEARCH_URL, body, apiKey);
  console.log(`[tavily:search] ${res.results.length} results in ${res.response_time}s`);
  return res;
}

/**
 * Tavily Extract – pull raw page content from one or more URLs.
 */
export async function tavilyExtract(
  urls: string[],
  apiKey: string,
  options: TavilyExtractOptions = {},
): Promise<TavilyExtractResponse> {
  console.log(`[tavily:extract] ${urls.length} URL(s)`);
  const body: Record<string, unknown> = { urls };
  if (options.extract_depth) body.extract_depth = options.extract_depth;
  const res = await tavilyFetch<TavilyExtractResponse>(TAVILY_EXTRACT_URL, body, apiKey);
  console.log(
    `[tavily:extract] ${res.results.length} succeeded, ${res.failed_results?.length ?? 0} failed`,
  );
  return res;
}
