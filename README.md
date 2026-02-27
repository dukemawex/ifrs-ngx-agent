# ifrs-ngx-agent

Node.js + TypeScript automation project for building a firm-year (2010-2023) panel dataset for seven Nigerian listed companies used in an IFRS thesis.

## Targets
- Nigerian Enamelware Plc
- Academy Press Plc
- Oando Plc
- Sterling Financial Holdings (Sterling HoldCo/Sterling Bank lineage)
- Aso Savings and Loans Plc
- Northern Nigeria Flour Mills Plc (NNFMN/NNFM)
- Beta Glass Plc

## What the pipeline does
1. Validates `TAVILY_API_KEY` at startup (fails fast with clear error if missing).
2. For each company, determines the IFRS adoption year via Tavily search (defaults to Nigeria's 2012 if not found).
3. Discovers annual report / audited financial statement URLs for each company-year via **Tavily Search API**.
4. Prioritizes sources in this order:
   - Official company IR/disclosure pages
   - NGX document library
   - AfricanFinancials
   - Credible archive/mirror fallbacks
5. Uses **Tavily Extract API** and supplemental search queries to extract financial line items.
6. Computes IFRS dummy and financial ratios.
7. Validates quality and missingness.
8. Generates per-company financial summaries (pre/post IFRS adoption periods).
9. Exports:
   - `data/processed/panel_raw.csv`
   - `data/processed/panel_metrics.csv`
   - `data/processed/audit_trail.jsonl`
   - `data/processed/financial_summaries.json`

## Financial Summary Schema

Each entry in `financial_summaries.json` follows this contract:

```json
{
  "company": { "name": "...", "ticker": "...", "exchange": "NGX" },
  "ifrs": { "adoption_year": 2012, "source_url": "...", "notes": "..." },
  "periods": {
    "pre_ifrs": {
      "years": [2010, 2011],
      "metrics": { "2010": { "revenue": null, "net_income": null, "..." : "..." } },
      "sources": ["https://..."]
    },
    "post_ifrs": {
      "years": [2012, 2013, "..."],
      "metrics": { "2012": { "revenue": null, "net_income": null, "..." : "..." } },
      "sources": ["https://..."]
    }
  },
  "currency": "NGN",
  "notes": "",
  "generated_at": "ISO8601"
}
```

Metrics per year: `revenue`, `profit_before_tax`, `net_income`, `total_assets`, `total_liabilities`, `equity`, `eps`, `dividends`.

## Tavily Client Features
- Uses Tavily **Search** (`/search`) and **Extract** (`/extract`) REST APIs.
- Retry logic with exponential backoff + jitter for 429/5xx and network errors.
- Request timeout (30 s) with `AbortController`.
- Concurrency cap (2 parallel requests) to avoid API throttling.
- API key validated once at startup; never logged.
- Robust logging of request status without exposing sensitive data.

## Setup
1. Install dependencies:
   ```bash
   npm install
   ```
2. Copy env template and set API key:
   ```bash
   cp .env.example .env
   ```
3. Edit `.env`:
   ```env
   TAVILY_API_KEY=your_key
   ```

## Run locally
```bash
npm run build-dataset
```

## GitHub Actions
Workflow file: `.github/workflows/build_dataset.yml`

### Add repository secret
1. Go to **Settings -> Secrets and variables -> Actions**.
2. Create secret:
   - Name: `TAVILY_API_KEY`
   - Value: your Tavily API key
3. Run workflow manually from **Actions -> Build IFRS NGX Dataset -> Run workflow**.

## Output interpretation
- `panel_raw.csv`: extracted statement fields and source metadata per firm-year.
- `panel_metrics.csv`: raw fields plus computed metrics:
  - `ifrs_dummy` (`1` if year >= adoption year, else `0`)
  - `roa` = net income / total assets
  - `current_ratio` = current assets / current liabilities
  - `leverage_ratio` = total liabilities / total assets
  - `interest_coverage` = EBIT / interest expense
  - `altman_z_modified` = `6.56X1 + 3.26X2 + 6.72X3 + 1.05X4`
- `audit_trail.jsonl`: one event per processing step for traceability and troubleshooting.
- `financial_summaries.json`: structured per-company summaries with pre/post IFRS adoption periods.

## Prompt files
- `prompts/discover_report_urls.md`
- `prompts/extract_financials.md`

These serve as documentation for the search/extraction strategy.
