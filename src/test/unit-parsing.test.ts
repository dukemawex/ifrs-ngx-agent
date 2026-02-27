import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { detectUnit, applyScaling, validateExtractedContent, plausibilityCheck } from "../extract.js";

describe("detectUnit", () => {
  it("detects ₦'000", () => {
    const result = detectUnit("All amounts are in ₦'000");
    assert.equal(result.label, "₦'000");
    assert.equal(result.factor, 1_000);
  });

  it("detects ₦'million", () => {
    const result = detectUnit("Figures stated in ₦'million unless otherwise noted");
    assert.equal(result.label, "₦'million");
    assert.equal(result.factor, 1_000_000);
  });

  it("detects NGN'billion", () => {
    const result = detectUnit("Values in NGN billion");
    assert.equal(result.label, "NGN'billion");
    assert.equal(result.factor, 1_000_000_000);
  });

  it("detects in thousands", () => {
    const result = detectUnit("All figures in thousands of Naira");
    assert.equal(result.label, "thousands");
    assert.equal(result.factor, 1_000);
  });

  it("detects plain ₦ with factor 1", () => {
    const result = detectUnit("Revenue was ₦50,000,000");
    assert.equal(result.label, "₦");
    assert.equal(result.factor, 1);
  });

  it("detects plain NGN with factor 1", () => {
    const result = detectUnit("Revenue NGN 50000000");
    assert.equal(result.label, "NGN");
    assert.equal(result.factor, 1);
  });

  it("returns unknown for text without units", () => {
    const result = detectUnit("some random text without currency markers");
    assert.equal(result.label, "unknown");
    assert.equal(result.factor, 1);
  });

  it("detects in millions", () => {
    const result = detectUnit("Expressed in millions");
    assert.equal(result.label, "millions");
    assert.equal(result.factor, 1_000_000);
  });

  it("detects NGN'000", () => {
    const result = detectUnit("In NGN'000");
    assert.equal(result.label, "NGN'000");
    assert.equal(result.factor, 1_000);
  });
});

describe("applyScaling", () => {
  it("scales by factor 1000", () => {
    assert.equal(applyScaling(500, 1_000), 500_000);
  });

  it("scales by factor 1 million", () => {
    assert.equal(applyScaling(3.5, 1_000_000), 3_500_000);
  });

  it("returns null for null input", () => {
    assert.equal(applyScaling(null, 1_000), null);
  });

  it("scales negative values correctly", () => {
    assert.equal(applyScaling(-100, 1_000), -100_000);
  });
});

describe("validateExtractedContent", () => {
  it("passes when content has firm name, year, and unit", () => {
    const result = validateExtractedContent(
      "Oando Plc annual report 2020 ₦50,000,000",
      "Oando Plc", ["Oando"], "OANDO", 2020,
    );
    assert.equal(result.valid, true);
    assert.equal(result.reasons.length, 0);
  });

  it("fails when firm name not found", () => {
    const result = validateExtractedContent(
      "Some Company annual report 2020 ₦50,000",
      "Oando Plc", ["Oando"], "OANDO", 2020,
    );
    assert.equal(result.valid, false);
    assert.ok(result.reasons.includes("firm_name_not_found"));
  });

  it("matches on ticker", () => {
    const result = validateExtractedContent(
      "OANDO ticker results 2020 ₦1,000",
      "Oando Plc", ["Oando"], "OANDO", 2020,
    );
    assert.equal(result.valid, true);
  });

  it("matches on alias", () => {
    const result = validateExtractedContent(
      "Oando results for 2020 NGN amounts",
      "Oando Plc", ["Oando"], "OANDO", 2020,
    );
    assert.equal(result.valid, true);
  });

  it("fails when year not found", () => {
    const result = validateExtractedContent(
      "Oando Plc annual report ₦50,000",
      "Oando Plc", ["Oando"], "OANDO", 2020,
    );
    assert.equal(result.valid, false);
    assert.ok(result.reasons.includes("year_not_found"));
  });

  it("fails when unit marker not found", () => {
    const result = validateExtractedContent(
      "Oando Plc annual report 2020 revenue 50000",
      "Oando Plc", ["Oando"], "OANDO", 2020,
    );
    assert.equal(result.valid, false);
    assert.ok(result.reasons.includes("unit_marker_not_found"));
  });
});

describe("plausibilityCheck", () => {
  it("passes for reasonable values", () => {
    const result = plausibilityCheck({
      total_assets: 5_000_000_000,
      revenue: 1_000_000_000,
      equity: 2_000_000_000,
    });
    assert.equal(result.ok, true);
    assert.equal(result.flags.length, 0);
  });

  it("flags total_assets too small", () => {
    const result = plausibilityCheck({ total_assets: 500 });
    assert.equal(result.ok, false);
    assert.ok(result.flags.includes("total_assets_too_small"));
  });

  it("flags total_assets too large", () => {
    const result = plausibilityCheck({ total_assets: 100_000_000_000_000 });
    assert.equal(result.ok, false);
    assert.ok(result.flags.includes("total_assets_too_large"));
  });

  it("flags negative revenue", () => {
    const result = plausibilityCheck({ revenue: -1000 });
    assert.equal(result.ok, false);
    assert.ok(result.flags.includes("negative_revenue"));
  });
});
