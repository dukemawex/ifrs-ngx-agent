import { describe, it, mock, beforeEach } from "node:test";
import assert from "node:assert/strict";

// E2E test stub with mocked Tavily responses.
// This validates the overall pipeline flow without hitting the real API.

describe("end-to-end pipeline stub", () => {
  const MOCK_SEARCH_RESPONSE = {
    query: "Oando Plc annual report 2020",
    results: [
      {
        title: "Oando Plc Annual Report 2020",
        url: "https://doclib.ngxgroup.com/oando-2020-annual-report.pdf",
        content:
          "Oando Plc 2020 Annual Report. Total assets: 1,200,000 Total liabilities: 800,000 " +
          "Equity: 400,000 Revenue: 500,000 Net income: 50,000 EBIT: 70,000 " +
          "Interest expense: 20,000 Current assets: 600,000 Current liabilities: 300,000 " +
          "Total debt: 200,000 Retained earnings: 150,000 Profit before tax: 65,000 " +
          "All amounts in ₦'million",
        score: 0.95,
      },
    ],
    response_time: 0.5,
  };

  const MOCK_EXTRACT_RESPONSE = {
    results: [
      {
        url: "https://doclib.ngxgroup.com/oando-2020-annual-report.pdf",
        raw_content:
          "Oando Plc Financial Statements 2020\n" +
          "All amounts in ₦'million\n" +
          "Total assets: 1,200,000\n" +
          "Total liabilities: 800,000\n" +
          "Shareholders' equity: 400,000\n" +
          "Revenue: 500,000\n" +
          "Net income: 50,000\n" +
          "EBIT: 70,000\n" +
          "Profit before tax: 65,000\n" +
          "Interest expense: 20,000\n" +
          "Current assets: 600,000\n" +
          "Current liabilities: 300,000\n" +
          "Total debt: 200,000\n" +
          "Retained earnings: 150,000\n",
      },
    ],
    failed_results: [],
  };

  beforeEach(() => {
    // Reset mocks before each test
    mock.restoreAll();
  });

  it("should parse financial data from mocked extract content", async () => {
    // Import the extract module's internal parsing functions via the public API
    const { detectUnit, validateExtractedContent, plausibilityCheck } = await import("../extract.js");

    const content = MOCK_EXTRACT_RESPONSE.results[0].raw_content;

    // Validate unit detection
    const unit = detectUnit(content);
    assert.equal(unit.label, "₦'million");
    assert.equal(unit.factor, 1_000_000);

    // Validate content validation gates
    const validation = validateExtractedContent(
      content, "Oando Plc", ["Oando"], "OANDO", 2020,
    );
    assert.equal(validation.valid, true);
    assert.deepEqual(validation.reasons, []);
  });

  it("should compute metrics correctly from raw values", async () => {
    const { computeMetrics } = await import("../compute.js");

    const rawRow = {
      company_id: "oando",
      company_name: "Oando Plc",
      year: 2020,
      ifrs_dummy: 1,
      source_url: "https://example.com/report.pdf",
      source_type: "ngx_doclib" as const,
      total_assets: 1_200_000_000_000,
      total_liabilities: 800_000_000_000,
      equity: 400_000_000_000,
      revenue: 500_000_000_000,
      EBIT: 70_000_000_000,
      profit_before_tax: 65_000_000_000,
      EBIT_computed: false,
      interest_expense: 20_000_000_000,
      net_income: 50_000_000_000,
      current_assets: 600_000_000_000,
      current_liabilities: 300_000_000_000,
      total_debt: 200_000_000_000,
      retained_earnings: 150_000_000_000,
      scaling_factor: 1_000_000,
      detected_unit: "₦'million",
      evidence_hints: {},
      extraction_notes: "test",
    };

    const metrics = computeMetrics(rawRow);

    // ROA = net_income / total_assets
    assert.ok(metrics.roa !== null);
    assert.ok(Math.abs(metrics.roa! - 50 / 1200) < 0.001);

    // Current ratio = current_assets / current_liabilities
    assert.ok(metrics.current_ratio !== null);
    assert.ok(Math.abs(metrics.current_ratio! - 2.0) < 0.001);

    // Leverage ratio = total_liabilities / total_assets
    assert.ok(metrics.leverage_ratio !== null);
    assert.ok(Math.abs(metrics.leverage_ratio! - 800 / 1200) < 0.001);

    // Interest coverage = EBIT / interest_expense
    assert.ok(metrics.interest_coverage !== null);
    assert.ok(Math.abs(metrics.interest_coverage! - 3.5) < 0.001);

    // Altman Z should be computed
    assert.ok(metrics.altman_z_modified !== null);
  });

  it("should validate rows and flag missing fields", async () => {
    const { validateRow } = await import("../validate.js");

    const row = {
      company_id: "test",
      company_name: "Test Co",
      year: 2020,
      ifrs_dummy: 1,
      source_url: null,
      source_type: null,
      total_assets: null,
      total_liabilities: null,
      equity: null,
      revenue: null,
      EBIT: null,
      profit_before_tax: null,
      EBIT_computed: false,
      interest_expense: null,
      net_income: null,
      current_assets: null,
      current_liabilities: null,
      total_debt: null,
      retained_earnings: null,
      scaling_factor: 1,
      detected_unit: "unknown",
      evidence_hints: {},
      extraction_notes: "test",
      roa: null,
      current_ratio: null,
      leverage_ratio: null,
      interest_coverage: null,
      altman_z_modified: null,
      validation_flags: [] as string[],
    };

    const validated = validateRow(row);
    assert.ok(validated.validation_flags.length > 0);
    assert.ok(validated.validation_flags.includes("missing_total_assets"));
    assert.ok(validated.validation_flags.includes("missing_revenue"));
  });

  it("should generate year range from 2007 to 2024", async () => {
    const { YEARS, START_YEAR, END_YEAR } = await import("../years.js");
    assert.equal(START_YEAR, 2007);
    assert.equal(END_YEAR, 2024);
    assert.equal(YEARS.length, 18);
    assert.equal(YEARS[0], 2007);
    assert.equal(YEARS[YEARS.length - 1], 2024);
  });

  it("should have 7 target companies", async () => {
    const { TARGETS } = await import("../targets.js");
    assert.equal(TARGETS.length, 7);
  });

  it("should rank PDF candidates higher", async () => {
    const { rankCandidates } = await import("../discover.js");

    const candidates = [
      { url: "https://example.com/page.html", source_type: "mirror" as const, confidence: 0.9, notes: "HTML page" },
      { url: "https://ngxgroup.com/report.pdf", source_type: "ngx_doclib" as const, confidence: 0.8, notes: "PDF report" },
    ];

    const ranked = rankCandidates(candidates);
    assert.equal(ranked[0].url, "https://ngxgroup.com/report.pdf");
  });
});
