export type SourceType =
  | "official_ir"
  | "ngx_doclib"
  | "africanfinancials"
  | "archive"
  | "mirror";

export type DiscoveryCandidate = {
  url: string;
  source_type: SourceType;
  confidence: number;
  notes: string;
};

export type ExtractedFinancials = {
  total_assets: number | null;
  total_liabilities: number | null;
  equity: number | null;
  revenue: number | null;
  EBIT: number | null;
  EBIT_computed: boolean;
  interest_expense: number | null;
  net_income: number | null;
  current_assets: number | null;
  current_liabilities: number | null;
  total_debt: number | null;
  retained_earnings: number | null;
  evidence_hints: Record<string, string>;
  extraction_notes: string;
};

export type PanelRawRow = {
  company_id: string;
  company_name: string;
  year: number;
  ifrs_dummy: number;
  source_url: string | null;
  source_type: SourceType | null;
} & ExtractedFinancials;

export type PanelMetricRow = PanelRawRow & {
  roa: number | null;
  current_ratio: number | null;
  leverage_ratio: number | null;
  interest_coverage: number | null;
  altman_z_modified: number | null;
  validation_flags: string[];
};

export type AuditTrailEvent = {
  ts: string;
  company_id: string;
  year: number;
  step: string;
  ok: boolean;
  details: Record<string, unknown>;
};

// ---------- Financial summary data contract ----------

export type CompanyInfo = {
  name: string;
  ticker: string;
  exchange: string;
};

export type IFRSAdoption = {
  adoption_year: number;
  source_url: string;
  notes: string;
};

export type YearlyMetrics = {
  revenue: number | null;
  profit_before_tax: number | null;
  net_income: number | null;
  total_assets: number | null;
  total_liabilities: number | null;
  equity: number | null;
  eps: number | null;
  dividends: number | null;
};

export type PeriodData = {
  years: number[];
  metrics: Record<number, YearlyMetrics>;
  sources: string[];
};

export type FinancialSummary = {
  company: CompanyInfo;
  ifrs: IFRSAdoption;
  periods: {
    pre_ifrs: PeriodData;
    post_ifrs: PeriodData;
  };
  currency: string;
  notes: string;
  generated_at: string;
};
