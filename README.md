# ifrs-ngx-agent

Node.js + TypeScript automation project for building a firm-year (2007-2024) panel dataset for seven Nigerian listed companies used in an IFRS thesis.

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
   - Uses `include_domains` (doclib.ngxgroup.com, ngxgroup.com, africanfinancials.com) to prefer official sources.
   - Uses `exclude_domains` to prevent cross-company contamination.
   - Requests 5–8 results per query; falls back to broader search if preferred domains yield few results.
4. Prioritizes sources in this order:
   - Official company IR/disclosure pages
   - NGX document library
   - AfricanFinancials
   - Credible archive/mirror fallbacks
5. Uses **Tavily Extract API** with `extract_depth="advanced"` and supplemental search queries to extract financial line items.
6. Applies **strict validation gates**: extracted text must contain the firm name (or ticker), the year, and a unit marker (₦, NGN, ₦'000, ₦'million). Detects the unit and normalizes all values into plain NGN.
7. Runs **plausibility checks**: assets/revenue/equity must be reasonable after scaling. If not, flags and discards the record.
8. Enforces **completeness thresholds**: if key fields are missing, writes the record but marks `validation_flags` and excludes from ratios that require those fields.
9. Computes IFRS dummy and financial ratios.
10. Validates quality and missingness.
11. Generates per-company financial summaries (pre/post IFRS adoption periods).
12. Exports:
    - `data/processed/panel_raw.csv`
    - `data/processed/panel_metrics.csv`
    - `data/processed/audit_trail.jsonl`
    - `data/processed/financial_summaries.json`

## Year Range & IFRS Split
- **Pre-IFRS**: 2007–2011
- **Post-IFRS**: 2012–2024
- Total: 18 firm-years per company (126 firm-years across 7 companies)

## Financial Summary Schema

Each entry in `financial_summaries.json` follows this contract:

```json
{
  "company": { "name": "...", "ticker": "...", "exchange": "NGX" },
  "ifrs": { "adoption_year": 2012, "source_url": "...", "notes": "..." },
  "periods": {
    "pre_ifrs": {
      "years": [2007, 2008, 2009, 2010, 2011],
      "metrics": { "2007": { "revenue": null, "net_income": null, "..." : "..." } },
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

## Audit Trail

The audit trail (`audit_trail.jsonl`) records every decision with detailed context:

```json
{
  "ts": "ISO8601",
  "company_id": "oando",
  "year": 2020,
  "step": "extract_compute_validate",
  "ok": true,
  "details": {
    "query": "...",
    "urls_considered": ["..."],
    "chosen_url": "...",
    "validation_results": { "valid": true, "reasons": [] },
    "detected_unit": "₦'million",
    "scaling_factor": 1000000,
    "parse_confidence": 0.82
  }
}
```

## panel_raw.csv Fields

`company_id`, `company_name`, `year`, `ifrs_dummy`, `source_url`, `source_type`, `total_assets`, `total_liabilities`, `equity`, `revenue`, `EBIT`, `profit_before_tax`, `interest_expense`, `net_income`, `current_assets`, `current_liabilities`, `total_debt`, `retained_earnings`, `scaling_factor`, `detected_unit`, `extraction_notes`.

## panel_metrics.csv Fields

All `panel_raw.csv` fields plus computed ratios:
- `roa` = net income / total assets
- `current_ratio` = current assets / current liabilities
- `leverage_ratio` = total liabilities / total assets
- `interest_coverage` = EBIT / interest expense (falls back to profit_before_tax)
- `altman_z_modified` = `6.56X1 + 3.26X2 + 6.72X3 + 1.05X4`
- `validation_flags`

## Tavily Client Features
- Uses Tavily **Search** (`/search`) and **Extract** (`/extract`) REST APIs.
- Extract uses `extract_depth="advanced"` for table capture from PDFs.
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
npm run build:data
```

Or equivalently:
```bash
npm run build-dataset
```

## Run tests
```bash
npm run build && npm test
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
- `panel_metrics.csv`: raw fields plus computed metrics and validation flags.
- `audit_trail.jsonl`: one event per processing step for traceability and troubleshooting.
- `financial_summaries.json`: structured per-company summaries with pre/post IFRS adoption periods.

## Prompt files
- `prompts/discover_report_urls.md`
- `prompts/extract_financials.md`

These serve as documentation for the search/extraction strategy.
