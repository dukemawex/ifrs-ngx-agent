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
1. Discovers annual report / audited financial statement URLs for each company-year.
2. Prioritizes sources in this order:
   - Official company IR/disclosure pages
   - NGX document library
   - AfricanFinancials
   - Credible archive/mirror fallbacks
3. Uses TinyFish Web Agent API to extract line items.
4. Computes IFRS and financial ratios.
5. Validates quality and missingness.
6. Exports:
   - `data/processed/panel_raw.csv`
   - `data/processed/panel_metrics.csv`
   - `data/processed/audit_trail.jsonl`

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
   TINYFISH_API_KEY=your_key
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
   - Name: `TINYFISH_API_KEY`
   - Value: your TinyFish API key
3. Run workflow manually from **Actions -> Build IFRS NGX Dataset -> Run workflow**.

## Output interpretation
- `panel_raw.csv`: extracted statement fields and source metadata per firm-year.
- `panel_metrics.csv`: raw fields plus computed metrics:
  - `ifrs_dummy` (`1` if year >= 2012, else `0`)
  - `roa` = net income / total assets
  - `current_ratio` = current assets / current liabilities
  - `leverage_ratio` = total liabilities / total assets
  - `interest_coverage` = EBIT / interest expense
  - `altman_z_modified` = `6.56X1 + 3.26X2 + 6.72X3 + 1.05X4`
- `audit_trail.jsonl`: one event per processing step for traceability and troubleshooting.

## Prompt files
- `prompts/discover_report_urls.md`
- `prompts/extract_financials.md`

These can be tuned without changing TypeScript code.
