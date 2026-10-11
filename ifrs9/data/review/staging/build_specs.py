"""Spec rows for the 2026-10-11 user-handoff sources (Ecobank Nigeria, GTBank 2015/2016).
Run: python data/review/staging/build_specs.py  -> replaces rows with these spec_id prefixes in data/review/specs.csv."""
import csv, pathlib
ROOT = pathlib.Path(__file__).resolve().parents[3]
P = ROOT / "data/review/specs.csv"
HDR = next(csv.reader(open(P)))
OUT = []

def doc(bank, year, job, title, version, doc_scope, col_scope, basis, units, offset, orig=None):
    """Return a function that adds one spec for this document."""
    def add(sid, var, page, rx, x0, x1, note, occ=1, sign=1, colhead=None, nn="", u=None, ori=None, cbasis=None,
            manual="", derive="", sign_reason="", opinion="", year_=None):
        d = dict.fromkeys(HDR, "")
        d.update(spec_id=sid, bank=bank, year=str(year_ or year), variable=var, job_id=job, page=page,
                 printed_page=(page - offset) if isinstance(page, int) and offset is not None else "",
                 row_regex=rx, x_min=x0, x_max=x1, row_occurrence=occ, sign=sign, raw_units=u or units,
                 scope="Bank (single-entity financial statements)" if col_scope == "bank_single_entity" else "Bank (separate financial statements)",
                 column_heading=colhead or f"31 December {year}", report_title=title, report_year=str(year),
                 original_or_comparative=ori or orig or f"original ({year} current year)", reporting_version=version,
                 note_number=nn, admit="yes", reviewer_note=note, manual_value=manual, derive_from=derive,
                 document_scope=doc_scope, column_scope=col_scope, column_scope_basis=cbasis or basis,
                 opinion_applicability=opinion, sign_reason=sign_reason)
        OUT.append(d)
    return add

EXP = "printed in parentheses as expense; panel stores positive"
ALW = "printed in parentheses; panel stores positive"

# ---------------- Ecobank Nigeria 2013 (xs-4668b73761) ----------------
B = ("Single-entity statements of Ecobank Nigeria Limited (no Group column; the bank had no consolidated subsidiaries); "
     "columns headed '31 December 2013' | '31 December 2012' ('All amounts in millions of Nigerian Naira'); 2013 column used")
a = doc("Ecobank Nigeria", 2013, "xs-4668b73761", "Ecobank Nigeria Limited Annual Report 2013 (issuer archive)",
        "2013 annual report, as originally reported", "single_entity", "bank_single_entity", B, "NGN million", 2)
a("ECO13-A", "assets", 38, r"^Total Assets", 345, 370, "SOFP Total Assets 1,460,811")
a("ECO13-L", "liabilities", 38, r"^Total Liabilities", 345, 370, "SOFP Total Liabilities 1,304,183")
a("ECO13-E", "equity", 38, r"^Total Equity [\d(]", 350, 370, "SOFP Total Equity 156,628; balance 1,304,183 + 156,628 = 1,460,811")
a("ECO13-PAT", "pat", 37, r"^Profit for the year", 372, 392, "Statement of profit or loss: Profit for the year 11,658 (after income tax credit)")
a("ECO13-PBT", "pbt", 37, r"^Profit before tax", 372, 392, "Profit before tax 10,533")
a("ECO13-OCF", "ocf", 41, r"^Net cash from operating activities", 370, 385, "Statement of cash flows: Net cash from operating activities 4,606")
a("ECO13-OA", "opening_assets", 38, r"^Total Assets", 455, 480, "Prior-year (31 December 2012) column of the 2013 SOFP: Total Assets 1,325,315; column not labelled restated",
  colhead="31 December 2012", ori="prior-year comparative in 2013 report (not restated)",
  cbasis=B.replace("2013 column used", "2012 (prior-year) column used"))
a("ECO13-TI", "total_impairment", 37, r"^Impairment charge for losses", 372, 392, "Impairment charge for losses (32,606) (IAS 39; credit losses)", nn="5", sign=-1, sign_reason=EXP)
a("ECO13-GL", "gross_loans", 59, r"^660,730 ", 320, 332, "Note 18.1 unlabelled 31 Dec 2013 total row: Gross amount 660,730 = specialised 243,454 + overdrafts 133,198 + term 271,298 + CP 100 + finance lease 12,680", nn="18.1")
a("ECO13-ALW", "loan_allowance", 59, r"^660,730 ", 438, 452, "Note 18.1 31 Dec 2013 total impairment (34,823) = specific (28,226) + collective (6,597); agrees with note 18.2 closing balance 34,823 (p60)", nn="18.1", sign=-1, sign_reason=ALW)
a("ECO13-NL", "net_loans", 38, r"^Loans And Advances To Customers", 352, 368, "SOFP Loans and advances to customers 625,907 = 660,730 - 34,823", nn="18")
a("ECO13-RC", "regulatory_capital", 97, r"^Total regulatory capital", 372, 392, "Capital management: Total regulatory capital 165,746 (Tier 1 149,293 + Tier 2 16,453) (printed page 95)")
a("ECO13-RWA", "rwa", 97, r"^Total risk-weighted assets", 372, 392, "Total risk-weighted assets 953,338")
a("ECO13-CAR", "car", 97, r"^Risk weighted Capital Adequacy Ratio", 383, 395, "Risk weighted Capital Adequacy Ratio (CAR) printed '17%' (whole-percent display; 165,746 / 953,338 = 17.39%)", u="percent")
a("GC-EcobankNigeria2013", "gcu", 36, r"Independent", "", "", "Independent Auditor's Report to the Members of Ecobank Nigeria Limited, PDF p36 (printed p34), single complete page: "
  "Akintola Williams Deloitte, David Achugamonu FRC/2013/ICAN/00000000840, dated 23 April 2014. Opinion: present fairly (unmodified). "
  "No material-uncertainty section, no emphasis-of-matter or other-matter paragraph; legal/regulatory section reports insider credits and BOFIA contraventions only.",
  u="indicator", manual="0", opinion="bank_single_entity", colhead="Auditor's report on the financial statements of Ecobank Nigeria Limited")

# ---------------- Ecobank Nigeria 2014 (xs-5bf40497d1) ----------------
B = ("Single-entity statements of Ecobank Nigeria Limited (no Group column); columns headed '31 December 2014' | '31 December 2013' "
     "('All amounts in millions of Naira'); 2014 column used")
a = doc("Ecobank Nigeria", 2014, "xs-5bf40497d1", "Ecobank Nigeria Limited Annual Report and Financial Statements 2014 (issuer archive)",
        "2014 annual report, as originally reported", "single_entity", "bank_single_entity", B, "NGN million", 2)
a("ECO14-A", "assets", 33, r"^Total assets", 412, 435, "SOFP Total assets 1,772,922")
a("ECO14-L", "liabilities", 33, r"^Total liabilities [\d(]", 412, 435, "SOFP Total liabilities 1,574,528")
a("ECO14-E", "equity", 33, r"^Total equity [\d(]", 420, 435, "SOFP Total equity 198,394; 1,574,528 + 198,394 = 1,772,922")
a("ECO14-PAT", "pat", 32, r"^PROFIT FOR THE YEAR", 425, 445, "PROFIT FOR THE YEAR 29,733")
a("ECO14-PBT", "pbt", 32, r"^Profit before tax from continuing operations", 425, 445, "Profit before tax from continuing operations 28,663 (no discontinued operations)")
a("ECO14-OCF", "ocf", 36, r"^Net cash generated from operating activities", 425, 445, "Statement of cash flows: Net cash generated from operating activities (110,701) (outflow; sign preserved)")
a("ECO14-OA", "opening_assets", 33, r"^Total assets", 482, 500, "Prior-year (31 December 2013) column: Total assets 1,460,811; not labelled restated; equals the 2013 original (xs-4668b73761 p38)",
  colhead="31 December 2013", ori="prior-year comparative in 2014 report (not restated)", cbasis=B.replace("2014 column used", "2013 (prior-year) column used"))
a("ECO14-TI", "total_impairment", 32, r"^Impairment charge for losses", 425, 445, "Impairment charge for losses (32,994) (IAS 39)", nn="8", sign=-1, sign_reason=EXP)
a("ECO14-GL", "gross_loans", 71, r"^930,956 ", 275, 290, "Note 18.1 unlabelled 31 Dec 2014 total row: Gross 930,956; carrying 892,721 (printed page 69)", nn="18.1")
a("ECO14-ALW", "loan_allowance", 71, r"^930,956 ", 455, 468, "Note 18.1 31 Dec 2014 total impairment (38,235) = specific (28,755) + collective (9,480); equals note 18.2 closing balance 38,235 (p72)", nn="18.1", sign=-1, sign_reason=ALW)
a("ECO14-NL", "net_loans", 33, r"^Loans and advances to customers", 420, 435, "SOFP Loans and advances to customers 892,721 = 930,956 - 38,235", nn="18")
a("ECO14-RC", "regulatory_capital", 128, r"^Total regulatory capital", 428, 440, "Capital management: Total regulatory capital 239,281 (Tier 1 183,136 + Tier 2 56,145) (printed page 126)")
a("ECO14-RWA", "rwa", 128, r"^Total risk-weighted assets", 420, 432, "Total risk-weighted assets 1,492,373 (credit 1,241,980 + operational 247,593 + market 2,800; Basel II from 2014, 2013 comparative credit-only)")
a("ECO14-CAR", "car", 128, r"^Risk weighted Capital Adequacy Ratio", 445, 455, "Risk weighted Capital Adequacy Ratio (CAR) printed '16%' (whole-percent display; 239,281 / 1,492,373 = 16.03%)", u="percent")
a("GC-EcobankNigeria2014", "gcu", 31, r"ECOBANK", "", "", "Report of the independent auditors to the members of Ecobank Nigeria Limited, PDF p31 (printed p29), single complete page, scanned image under a text header "
  "(transcribed from 110-dpi render). Heading misprints 'ECOBANK BANK LIMITED'; opinion names ECOBANK NIGERIA LIMITED. Akintola Williams Deloitte, Jelili Adebisi FRC/2013/ICAN/00000004247, dated 14 April 2015. "
  "Opinion: true and fair (unmodified). No material-uncertainty, emphasis-of-matter or other-matter paragraph; other reporting covers insider credits and CBN circular contraventions.",
  u="indicator", manual="0", opinion="bank_single_entity", colhead="Auditor's report on the financial statements of Ecobank Nigeria Limited")

# ---------------- Ecobank Nigeria 2015 (xs-a62824fb3d) ----------------
B = ("Single-entity statements of Ecobank Nigeria Limited (no Group column); columns headed '31 Dec. 2015' | '31 Dec. 2014' "
     "('All amounts in millions of Naira'); 2015 column used")
a = doc("Ecobank Nigeria", 2015, "xs-a62824fb3d", "2015 Ecobank Nigeria Annual Report (issuer archive)",
        "2015 annual report, as originally reported", "single_entity", "bank_single_entity", B, "NGN million", 2)
a("ECO15-A", "assets", 49, r"^Total assets", 398, 410, "SOFP Total assets 1,794,348")
a("ECO15-L", "liabilities", 49, r"^Total liabilities [\d(]", 398, 410, "SOFP Total liabilities 1,566,561")
a("ECO15-E", "equity", 49, r"^Total equity [\d(]", 403, 415, "SOFP Total equity 227,787; 1,566,561 + 227,787 = 1,794,348")
a("ECO15-PAT", "pat", 48, r"^Profit for the year", 392, 405, "Profit for the year 11,304")
a("ECO15-PBT", "pbt", 48, r"^Profit before tax from continuing operations", 392, 405, "Profit before tax from continuing operations 11,380")
a("ECO15-OCF", "ocf", 52, r"^Net cash from operating activities", 392, 405, "Statement of cash flows: Net cash from operating activities 24,229")
a("ECO15-OA", "opening_assets", 49, r"^Total assets", 474, 486, "Prior-year (31 Dec. 2014) column: Total assets 1,772,922; not labelled restated; equals the 2014 original (xs-5bf40497d1 p33)",
  colhead="31 Dec. 2014", ori="prior-year comparative in 2015 report (not restated)", cbasis=B.replace("2015 column used", "2014 (prior-year) column used"))
a("ECO15-TI", "total_impairment", 48, r"^Impairment charge for losses", 388, 400, "Impairment charge for losses (55,740) (IAS 39)", nn="8", sign=-1, sign_reason=EXP)
a("ECO15-GL", "gross_loans", 76, r"^885,701 \(", 182, 195, "Note 18 unlabelled 31 December 2015 total row: Gross 885,701; carrying 817,348 (printed page 74)", nn="18")
a("ECO15-ALW", "loan_allowance", 76, r"^885,701 \(", 393, 405, "Note 18 31 December 2015 total impairment (68,353) = specific (59,038) + collective (9,315); equals closing balance 68,353 (p77)", nn="18", sign=-1, sign_reason=ALW)
a("ECO15-NL", "net_loans", 49, r"^Loans and advances to customers", 404, 416, "SOFP Loans and advances to customers 817,348 = 885,701 - 68,353", nn="18")
a("ECO15-RC", "regulatory_capital", 120, r"^Total regulatory capital", 390, 400, "Capital management: Total regulatory capital 254,109 (Tier 1 202,017 + Tier 2 75,000 less deductions as printed) (printed page 118)")
a("ECO15-RWA", "rwa", 120, r"^Total risk-weighted assets", 384, 395, "Total risk-weighted assets 1,357,098 (credit 1,098,488 + operational 250,662 + market)")
a("ECO15-CAR", "car", 120, r"^Risk weighted Capital Adequacy Ratio", 400, 410, "Risk weighted Capital Adequacy Ratio (CAR) printed '19%' (whole-percent display; 254,109 / 1,357,098 = 18.72%)", u="percent")
a("GC-EcobankNigeria2015", "gcu", 46, r"Independent", "", "", "Independent Auditor's Report to the Members of Ecobank Nigeria Limited, PDF pp46-47 (printed 44-45), complete: "
  "Akintola Williams Deloitte, Joshua Ojo FRC/2013/ICAN/00000000849, dated 27 April 2016. Opinion: true and fair (unmodified). "
  "No material-uncertainty, emphasis-of-matter or other-matter paragraph; other reporting covers insider credits and BOFIA/CBN contraventions.",
  u="indicator", manual="0", opinion="bank_single_entity", colhead="Auditor's report on the financial statements of Ecobank Nigeria Limited")

# ---------------- Ecobank Nigeria 2018 (xs-29bf069fa6) ----------------
B = ("Single-entity statements of Ecobank Nigeria Limited (no Group column); columns headed '31-Dec 2018' | '31-Dec2017' "
     "(N'million); 2018 column used")
a = doc("Ecobank Nigeria", 2018, "xs-29bf069fa6", "Ecobank Nigeria Annual Report 2018 (issuer archive)",
        "2018 annual report, as originally reported", "single_entity", "bank_single_entity", B, "NGN million", 0)
a("ECO18-A", "assets", 65, r"^Total assets", 412, 425, "SOFP Total assets 1,956,830")
a("ECO18-L", "liabilities", 65, r"^Total liabilities [\d(]", 412, 425, "SOFP Total liabilities 1,709,348")
a("ECO18-E", "equity", 65, r"^Total equity [\d(]", 416, 428, "SOFP Total equity 247,482; 1,709,348 + 247,482 = 1,956,830")
a("ECO18-PAT", "pat", 64, r"^Pofit for the year", 415, 428, "Statement of profit or loss: 'Pofit for the year' (misprint) 27,155")
a("ECO18-PBT", "pbt", 64, r"^Profit before income tax", 415, 428, "Profit before income tax 27,521")
a("ECO18-OCF", "ocf", 67, r"^Net cash from operating activities", 420, 432, "Statement of cash flows: Net cash from operating activities 31,236")
a("ECO18-OA", "opening_assets", 65, r"^Total assets", 472, 484, "Prior-year (31-Dec 2017) column: Total assets 1,829,761; IAS 39 closing balance, not restated for IFRS 9 (bank applied the IFRS 9 exemption; transition adjustment in opening equity)",
  colhead="31-Dec 2017", ori="prior-year comparative in 2018 report (not restated)", cbasis=B.replace("2018 column used", "2017 (prior-year) column used"))
a("ECO18-TI", "total_impairment", 64, r"^Impairment charge for losses", 412, 424, "Impairment charge for losses (27,360) (IFRS 9 ECL)", nn="9", sign=-1, sign_reason=EXP)
a("ECO18-GL", "gross_loans", 110, r"^Gross loans", 458, 470, "Note 19.1 31 December 2018: Gross loans 926,546 (Stage 1 480,739 + Stage 2 318,962 + Stage 3 126,844)", nn="19.1")
a("ECO18-ALW", "loan_allowance", 110, r"^Expected credit loss allowance", 458, 470, "Note 19.1 Expected credit loss allowance (84,071) (Stage 1 4,921 + Stage 2 15,291 + Stage 3 63,859); equals closing balance p111", nn="19.1", sign=-1, sign_reason=ALW)
a("ECO18-NL", "net_loans", 65, r"^.oans and advances to cust", 418, 430, "SOFP Loans and advances to customers 842,475 = 926,546 - 84,071 (label glyph 'L' rendered '.' in text layer)", nn="19")
a("ECO18-NPL", "npl_amount", 110, r"^Non-Performing", 408, 420, "Note 19.1: Non-Performing loans 126,844 (equals Stage 3 gross)", nn="19.1")
a("ECO18-RC", "regulatory_capital", 170, r"^Total regulatory capital", 410, 422, "Capital: Total regulatory capital 205,312; Tier 1 includes 'IFRS 9 transitional adjustment' 8,509")
a("ECO18-RWA", "rwa", 170, r"^Total risk-weighted assets", 405, 416, "Total risk-weighted assets 1,433,545")
a("ECO18-CAR", "car", 170, r"^Risk weighted Capital Adequacy Ratio", 418, 428, "Risk weighted Capital Adequacy Ratio (CAR) 14.3%; only ratio printed; transitional basis (Tier 1 includes IFRS 9 transitional adjustment 8,509); full-impact CAR not printed", u="percent")
a("ECO18-CART", "car_transitional", 170, r"^Risk weighted Capital Adequacy Ratio", 418, 428, "Same printed ratio 14.3% recorded as the transitional-basis CAR (IFRS 9 transitional adjustment 8,509 in Tier 1); see ECO18-CAR", u="percent")
a("GC-EcobankNigeria2018", "gcu", 58, r"INDEPENDENT", "", "", "Independent auditor's report to the shareholders of Ecobank Nigeria Limited, PDF pp58-63, complete: Deloitte & Touche, Joshua Ojo FRC/2013/ICAN/00000000849, dated 29 March 2019. "
  "Opinion: present fairly (unmodified). KAMs: loan loss impairment incl. off-balance-sheet (IFRS 9 first adoption); valuation of derivatives. No material-uncertainty section, no emphasis-of-matter or other-matter paragraph; going concern appears only in responsibilities boilerplate.",
  u="indicator", manual="0", opinion="bank_single_entity", colhead="Auditor's report on the financial statements of Ecobank Nigeria Limited")

# ---------------- Ecobank Nigeria 2019 (xs-be6229d851) ----------------
B = ("Single-entity statements of Ecobank Nigeria Limited (no Group column); columns headed '31-Dec 2019' | 'Restated 31-Dec 2018' | '31-Dec 2018' "
     "(=N= million); 2019 column used")
a = doc("Ecobank Nigeria", 2019, "xs-be6229d851", "Ecobank Nigeria Annual Report 2019 (issuer archive)",
        "2019 annual report, as originally reported", "single_entity", "bank_single_entity", B, "NGN million", 0)
a("ECO19-A", "assets", 71, r"^Total assets", 390, 402, "SOFP Total assets 1,991,040")
a("ECO19-L", "liabilities", 71, r"^Total liabilities [\d(]", 390, 402, "SOFP Total liabilities 1,726,770")
a("ECO19-E", "equity", 71, r"^Total equity [\d(]", 394, 406, "SOFP Total equity 264,270; 1,726,770 + 264,270 = 1,991,040")
a("ECO19-PAT", "pat", 70, r"^PROFIT/\(LOSS\) FOR THE YEAR", 382, 394, "PROFIT/(LOSS) FOR THE YEAR 1,256")
a("ECO19-PBT", "pbt", 70, r"^Profit/\(loss\) before income tax", 382, 394, "Profit/(loss) before income tax 2,238")
a("ECO19-OCF", "ocf", 74, r"^Net cash from operating activities", 410, 420, "Statement of cash flows: Net cash from operating activities 49,052 (first occurrence)")
a("ECO19-OA", "opening_assets", 71, r"^Total assets", 434, 446, "Prior-year column headed 'Restated 31-Dec 2018': Total assets 1,927,889 (restated per Note 44, CBN haircut on petroleum-marketer interest); the panel's own 2018 closing assets are the original 1,956,830",
  colhead="Restated 31-Dec 2018", ori="prior-year comparative in 2019 report (labelled Restated)", cbasis=B.replace("2019 column used", "'Restated 31-Dec 2018' (prior-year) column used"))
a("ECO19-TI", "total_impairment", 70, r"^Impairment charge for losses", 378, 390, "Impairment charge for losses (2,704) (IFRS 9 ECL)", nn="9", sign=-1, sign_reason=EXP)
a("ECO19-GL", "gross_loans", 111, r"^Gross loans", 488, 500, "Note 19.1 31 Dec 2019: Gross loans 913,082 (Stage 1 428,380 + Stage 2 266,187 + Stage 3 218,515)", nn="19.1")
a("ECO19-ALW", "loan_allowance", 111, r"^Expected credit loss allowance", 486, 498, "Note 19.1 Expected credit loss allowance (101,476); equals closing balance p112", nn="19.1", sign=-1, sign_reason=ALW)
a("ECO19-NL", "net_loans", 71, r"^Loans and advances to customers", 397, 409, "SOFP Loans and advances to customers 811,606 = 913,082 - 101,476", nn="19")
a("ECO19-NPL", "npl_amount", 111, r"^Non-Performing", 440, 452, "Note 19.1: Non-Performing 218,515 (equals Stage 3 gross)", nn="19.1")
a("ECO19-RC", "regulatory_capital", 170, r"^Total regulatory capital", 372, 384, "Capital: Total regulatory capital 236,196; Tier 1 includes IFRS 9 transitional adjustment 5,672")
a("ECO19-RWA", "rwa", 170, r"^Total risk-weighted assets", 366, 378, "Total risk-weighted assets 1,447,830")
a("ECO19-CAR", "car", 170, r"^Risk weighted Capital Adequacy Ratio", 375, 387, "CAR 16.31%; only ratio printed; transitional basis (Tier 1 includes IFRS 9 transitional adjustment 5,672)", u="percent")
a("ECO19-CART", "car_transitional", 170, r"^Risk weighted Capital Adequacy Ratio", 375, 387, "Same printed ratio 16.31% recorded as transitional-basis CAR; see ECO19-CAR", u="percent")
a("GC-EcobankNigeria2019", "gcu", 64, r"INDEPENDENT", "", "", "Independent auditor's report to the shareholders of Ecobank Nigeria Limited, PDF pp64-69, complete: Deloitte & Touche, Joshua Ojo FRC/2013/ICAN/00000000849, dated 25 March 2020. "
  "Opinion: present fairly (unmodified). Emphasis of Matters: Note 44 restatement of certain balances (CBN haircut on petroleum-marketer interest) - not going-concern related. KAMs on ECL. "
  "No material-uncertainty section; going concern only in responsibilities boilerplate.",
  u="indicator", manual="0", opinion="bank_single_entity", colhead="Auditor's report on the financial statements of Ecobank Nigeria Limited")

# ---------------- Ecobank Nigeria 2020 (xs-0dd4c49a7f) ----------------
B = ("Single-entity statements of Ecobank Nigeria Limited (no Group column); columns headed '31 Dec 2020' | '31 Dec 2019' "
     "('All amounts in millions of Naira'); 2020 column used")
a = doc("Ecobank Nigeria", 2020, "xs-0dd4c49a7f", "Ecobank Nigeria Annual Report 2020 (issuer archive)",
        "2020 annual report, as originally reported", "single_entity", "bank_single_entity", B, "NGN million", 0)
a("ECO20-A", "assets", 81, r"^Total assets", 422, 434, "SOFP Total assets 2,186,712")
a("ECO20-L", "liabilities", 81, r"^Total liabilities [\d(]", 422, 434, "SOFP Total liabilities 1,887,991")
a("ECO20-E", "equity", 81, r"^Total equity [\d(]", 427, 439, "SOFP Total equity 298,721; 1,887,991 + 298,721 = 2,186,712")
a("ECO20-PAT", "pat", 80, r"^PROFIT FOR THE YEAR", 392, 404, "PROFIT FOR THE YEAR 8,087")
a("ECO20-PBT", "pbt", 80, r"^Profit before income tax", 392, 404, "Profit before income tax 8,639")
a("ECO20-OCF", "ocf", 84, r"^Net cash from operating activities", 374, 386, "Statement of cash flows: Net cash from operating activities (13,271) (outflow; first occurrence)")
a("ECO20-OA", "opening_assets", 81, r"^Total assets", 466, 478, "Prior-year (31 Dec 2019) column: Total assets 1,991,040; not labelled restated; equals the 2019 original (xs-be6229d851 p71)",
  colhead="31 Dec 2019", ori="prior-year comparative in 2020 report (not restated)", cbasis=B.replace("2020 column used", "2019 (prior-year) column used"))
a("ECO20-TI", "total_impairment", 80, r"^Impairment charge for losses", 390, 402, "Impairment charge for losses (9,164) (IFRS 9 ECL)", nn="9", sign=-1, sign_reason=EXP)
a("ECO20-GL", "gross_loans", 115, r"^Gross loans", 482, 494, "Note 19.1 31 Dec 2020: Gross loans 993,191 (Stage 1 537,673 + Stage 2 258,315 + Stage 3 197,204)", nn="19.1")
a("ECO20-ALW", "loan_allowance", 115, r"^Expected credit loss allowance", 479, 491, "Note 19.1 Expected credit loss allowance (111,609)", nn="19.1", sign=-1, sign_reason=ALW)
a("ECO20-NL", "net_loans", 81, r"^Loans and advances to customers", 428, 440, "SOFP Loans and advances to customers 881,582 = 993,191 - 111,609", nn="19")
a("ECO20-NPL", "npl_amount", 115, r"^Non-Performing", 430, 442, "Note 19.1: Non-Performing 197,204 (equals Stage 3 gross)", nn="19.1")
a("ECO20-RC", "regulatory_capital", 177, r"^Total regulatory capital", 419, 431, "Capital: Total regulatory capital 301,364; Tier 1 includes IFRS 9 transitional adjustment 2,836")
a("ECO20-RWA", "rwa", 177, r"^Total risk-weighted assets", 413, 425, "Total risk-weighted assets 1,405,676")
a("ECO20-CAR", "car", 177, r"^Risk weighted Capital Adequacy Ratio", 421, 433, "CAR 21.44%; only ratio printed; transitional basis (IFRS 9 transitional adjustment 2,836 in Tier 1)", u="percent")
a("ECO20-CART", "car_transitional", 177, r"^Risk weighted Capital Adequacy Ratio", 421, 433, "Same printed ratio 21.44% recorded as transitional-basis CAR; see ECO20-CAR", u="percent")
a("GC-EcobankNigeria2020", "gcu", 72, r"INDEPENDENT", "", "", "Independent auditor's report to the shareholders of Ecobank Nigeria Limited, PDF pp72-79, complete: Deloitte & Touche, Yetunde Odetayo FRC/2013/ICAN/00000000823, dated 30 March 2021. "
  "Opinion: true and fair (unmodified). KAMs on ECL and derivatives. No material-uncertainty section, no emphasis-of-matter or other-matter paragraph.",
  u="indicator", manual="0", opinion="bank_single_entity", colhead="Auditor's report on the financial statements of Ecobank Nigeria Limited")

# ---------------- Ecobank Nigeria 2021 (xs-cce620f771) ----------------
B = ("Single-entity statements of Ecobank Nigeria Limited (no Group column); columns headed '31 Dec 2021' | '31 Dec 2020' "
     "('In millions of Nigerian Naira'); 2021 column used")
a = doc("Ecobank Nigeria", 2021, "xs-cce620f771", "Ecobank Nigeria Annual Report 2021 (issuer archive)",
        "2021 annual report, as originally reported", "single_entity", "bank_single_entity", B, "NGN million", 0)
a("ECO21-A", "assets", 86, r"^Total assets", 397, 410, "SOFP Total assets 2,475,079")
a("ECO21-L", "liabilities", 86, r"^Total liabilities [\d(]", 397, 410, "SOFP Total liabilities 2,196,302")
a("ECO21-E", "equity", 86, r"^Total equity [\d(]", 403, 415, "SOFP Total equity 278,777; 2,196,302 + 278,777 = 2,475,079")
a("ECO21-PAT", "pat", 84, r"^Profit for the year", 345, 358, "Profit for the year 9,766")
a("ECO21-PBT", "pbt", 84, r"^Profit before income tax", 345, 358, "Profit before income tax 10,676")
a("ECO21-OCF", "ocf", 89, r"^Net cash flows used in operating activities", 418, 430, "Statement of cash flows: Net cash flows used in operating activities (86,740) (outflow)")
a("ECO21-OA", "opening_assets", 86, r"^Total assets", 456, 468, "Prior-year (31 Dec 2020) column: Total assets 2,186,711, not labelled restated; the 2020 original prints 2,186,712 (1 million rounding)",
  colhead="31 Dec 2020", ori="prior-year comparative in 2021 report (not restated)", cbasis=B.replace("2021 column used", "2020 (prior-year) column used"))
a("ECO21-TI", "total_impairment", 84, r"^Credit loss expense on financial assets", 345, 358, "Credit loss expense on financial assets (7,041) (IFRS 9 ECL; same line as 'Impairment charge for losses' in earlier years)", nn="14", sign=-1, sign_reason=EXP)
a("ECO21-GL", "gross_loans", 124, r"^1,113,022 ", 400, 412, "Note 24 unlabelled 31 Dec 2021 total of overdrafts 114,990 + term loans 991,688 + other lines: 1,113,022; also equals Performing 931,068 + Non-Performing 181,954 (printed page 124)", nn="24")
a("ECO21-ALW", "loan_allowance", 124, r"^Less: Allowance for ECL", 403, 415, "Note 24: Less: Allowance for ECL (97,419); 1,113,022 - 97,419 = 1,015,603", nn="24", sign=-1, sign_reason=ALW)
a("ECO21-NL", "net_loans", 86, r"^Loans and advances to customers", 400, 412, "SOFP Loans and advances to customers 1,015,603", nn="24")
a("ECO21-NPL", "npl_amount", 124, r"^Non-Performing", 404, 416, "Note 24 gross analysis: Non-Performing 181,954 (first occurrence; second block is net of ECL)", nn="24")
a("ECO21-RC", "regulatory_capital", 198, r"^Total eligible capital", 413, 425, "Capital: Total eligible capital 170,600 (IFRS 9 transitional adjustment nil in 2021)")
a("ECO21-RWA", "rwa", 198, r"^Total risk-weighted assets", 407, 419, "Total risk-weighted assets 1,486,056")
a("ECO21-CAR", "car", 198, r"^Risk weighted Capital Adequacy Ratio", 416, 428, "CAR 11.48% (no transitional add-back in 2021)", u="percent")
a("GC-EcobankNigeria2021", "gcu", 78, r"INDEPENDENT", "", "", "Independent auditor's report to the shareholders of Ecobank Nigeria Limited, PDF pp78-83, complete: Ernst & Young, Oluwasayo Elumaro FRC/2012/ICAN/000000139, dated 26 April 2022. "
  "Opinion: true and fair (unmodified). KAMs: ECL on loans; valuation of unquoted equity. No material-uncertainty section, no emphasis-of-matter or other-matter paragraph.",
  u="indicator", manual="0", opinion="bank_single_entity", colhead="Auditor's report on the financial statements of Ecobank Nigeria Limited")

# ---------------- Ecobank Nigeria 2022 (xs-932212298e) ----------------
B = ("Single-entity statements of Ecobank Nigeria Limited (no Group column); columns headed '31-Dec 2022' | '31-Dec 2021' "
     "('In millions of Nigerian Naira'); 2022 column used")
a = doc("Ecobank Nigeria", 2022, "xs-932212298e", "Ecobank Nigeria Annual Report 2022 (issuer archive)",
        "2022 annual report, as originally reported", "single_entity", "bank_single_entity", B, "NGN million", 0)
a("ECO22-A", "assets", 76, r"^Total assets", 398, 410, "SOFP Total assets 2,917,689")
a("ECO22-L", "liabilities", 76, r"^Total liabilities [\d(]", 397, 409, "SOFP Total liabilities 2,623,076")
a("ECO22-E", "equity", 76, r"^Total equity [\d(]", 403, 415, "SOFP Total equity 294,613; 2,623,076 + 294,613 = 2,917,689")
a("ECO22-PAT", "pat", 74, r"^Profit for the year", 418, 430, "Profit for the year 10,396")
a("ECO22-PBT", "pbt", 74, r"^Profit before income tax", 418, 430, "Profit before income tax 12,396")
a("ECO22-OCF", "ocf", 80, r"^Net cash flows used in operating activities", 394, 406, "Statement of cash flows: Net cash flows used in operating activities (75,642) (outflow). 2021 comparative (98,241) differs from the 2021 original (86,740): comparatives marked '*' (reclassified); original retained for 2021")
a("ECO22-OA", "opening_assets", 76, r"^Total assets", 454, 466, "Prior-year (31-Dec 2021) column: Total assets 2,475,079; equals the 2021 original (xs-cce620f771 p86)",
  colhead="31-Dec 2021", ori="prior-year comparative in 2022 report (balance sheet total not restated)", cbasis=B.replace("2022 column used", "2021 (prior-year) column used"))
a("ECO22-TI", "total_impairment", 74, r"^Credit loss expense on financial assets", 414, 426, "Credit loss expense on financial assets (12,377) (IFRS 9 ECL)", nn="14", sign=-1, sign_reason=EXP)
a("ECO22-GL", "gross_loans", 110, r"^1,190,306 ", 398, 410, "Note 24 unlabelled 31 Dec 2022 total: overdrafts 100,037 + term loans 1,087,616 + other = 1,190,306; equals Performing 1,107,957 + Non-Performing 82,348 (printed page 110)", nn="24")
a("ECO22-ALW", "loan_allowance", 110, r"^Less: Allowance for ECL", 402, 414, "Note 24: Less: Allowance for ECL (62,880); 1,190,306 - 62,880 = 1,127,426", nn="24", sign=-1, sign_reason=ALW)
a("ECO22-NL", "net_loans", 76, r"^Loans and advances to customers", 400, 412, "SOFP Loans and advances to customers 1,127,426", nn="24")
a("ECO22-NPL", "npl_amount", 110, r"^Non-Performing", 406, 418, "Note 24 gross analysis: Non-Performing 82,348 (first occurrence)", nn="24")
a("ECO22-RC", "regulatory_capital", 184, r"^Total eligible capital", 412, 424, "Capital management note 54: Total eligible capital 232,070 (Tier 1 179,319)")
a("ECO22-RWA", "rwa", 184, r"^Total risk-weighted assets", 408, 420, "Total risk-weighted assets 1,748,560")
a("ECO22-CAR", "car", 184, r"^Risk weighted Capital Adequacy Ratio", 416, 428, "CAR 13.27%", u="percent")
a("GC-EcobankNigeria2022", "gcu", 68, r"INDEPENDENT", "", "", "Independent auditor's report to the shareholders of Ecobank Nigeria Limited, PDF pp68-72, complete: Ernst & Young, Oluwasayo Elumaro FRC/2012/ICAN/000000139, dated 11 April 2023 (printed 'll April 2023'). "
  "Opinion: true and fair (unmodified). KAMs on ECL. No material-uncertainty section, no emphasis-of-matter or other-matter paragraph.",
  u="indicator", manual="0", opinion="bank_single_entity", colhead="Auditor's report on the financial statements of Ecobank Nigeria Limited")

# ---------------- GTBank 2015 (xs-ac933e7f2f, issuer site) ----------------
B = ("Columns 'Group' | 'Group1' | 'Group1' | 'Parent' | 'Parent1' | 'Parent1' over 'Dec-2015' | 'Dec-2014' | 'Jan-2014' "
     "('In thousands of Nigerian Naira'; 1 = Restated, note 49); Parent = Guaranty Trust Bank Plc, the operating bank (pre-GTCO); Parent Dec-2015 column used")
SC = "Bank (separate financial statements; 'Parent' = Guaranty Trust Bank Plc, the operating bank, pre-GTCO)"
a = doc("GTBank", 2015, "xs-ac933e7f2f", "Guaranty Trust Bank Plc 2015 Year End Audited Results (consolidated and separate; issuer site)",
        "2015 annual report, as originally reported", "consolidated_and_separate", "bank_separate", B, "NGN thousand", 4)
def g(*args, **kw):
    kw.setdefault("colhead", "Parent Dec-2015")
    a(*args, **kw); OUT[-1]["scope"] = SC
g("GTB15-A", "assets", 54, r"^Total assets", 385, 400, "SOFP Parent Total assets 2,277,629,224")
g("GTB15-L", "liabilities", 54, r"^Total liabilities", 385, 400, "SOFP Parent Total liabilities 1,872,020,876")
g("GTB15-E", "equity", 55, r"^Total equity [\d(]", 392, 405, "SOFP Parent Total equity 405,608,348; 1,872,020,876 + 405,608,348 = 2,277,629,224")
g("GTB15-PAT", "pat", 56, r"^Profit for the year", 445, 460, "Income statement Parent Profit for the year 94,308,123")
g("GTB15-PBT", "pbt", 56, r"^Profit before income tax", 442, 455, "Parent Profit before income tax 113,027,057")
g("GTB15-OCF", "ocf", 62, r"^Net cash/\(used in\) provided by operating activities", 445, 460, "Statement of cash flows Parent Net cash provided by operating activities 10,429,148")
g("GTB15-OA", "opening_assets", 54, r"^Total assets", 448, 462, "Prior-year column 'Parent1 Dec-2014' (1 = Restated, note 49 reporting changes): Total assets 2,126,608,312",
  colhead="Parent Dec-2014 (Restated)", ori="prior-year comparative in 2015 report (labelled Restated)", cbasis=B.replace("Parent Dec-2015 column used", "Parent Dec-2014 (Restated) column used"))
g("GTB15-TI", "total_impairment", 56, r"^Loan impairment charges", 445, 460, "Parent Loan impairment charges (11,769,374); Parent 'Net impairment on financial assets' printed '-' for Dec-2015, so total impairment equals the loan charge (same composition as GTB17-TI)", nn="11", sign=-1, sign_reason=EXP)
g("GTB15-GLI", "gross_loans_individuals", 255, r"^Gross loans", 548, 560, "Note 29 Parent Dec-2015 loans to individuals: Gross loans 78,456,917 (printed page 251)", nn="29")
g("GTB15-ALI", "loan_allowance_individuals", 255, r"^Total impairment", 557, 570, "Note 29 Parent individuals Total impairment (809,643) = specific 138,049 + collective 671,594", nn="29", sign=-1, sign_reason=ALW)
g("GTB15-GLN", "gross_loans_non-individuals", 255, r"^Gross loans", 538, 550, "Note 29 Parent Dec-2015 loans to non-individuals: Gross loans 1,213,059,311 (second occurrence)", nn="29", occ=2)
g("GTB15-ALN", "loan_allowance_non-individuals", 256, r"^Total impairment", 545, 558, "Note 29 Parent non-individuals Total impairment (25,499,142) = specific 18,781,373 + collective 6,717,769", nn="29", sign=-1, sign_reason=ALW)
g("GTB15-GL", "gross_loans", 255, "derived", "", "", "Individuals + non-individuals = 1,291,516,228", nn="29", derive="GTB15-GLI+GTB15-GLN")
g("GTB15-ALW", "loan_allowance", 256, "derived", "", "", "Individuals + non-individuals customer-loan allowance = 26,308,785; gross - allowance = 1,265,207,443 = printed total carrying amount", nn="29", derive="GTB15-ALI+GTB15-ALN")
g("GTB15-NL", "net_loans", 54, r"^Loans and advances to customers", 385, 400, "SOFP Parent Loans and advances to customers 1,265,207,443", nn="29")
g("GTB15-RC", "regulatory_capital", 201, r"^Total Qualifying Capital", 392, 405, "Capital adequacy ratio table headed 'Bank': Total Qualifying Capital (C=A+B) 333,426,139 (printed page 197)", nn="5")
g("GTB15-RWA", "rwa", 201, r"^Aggregate Risk-Weighted Assets", 384, 395, "Bank Aggregate Risk-Weighted Assets 1,835,072,113 (credit 1,505,103,910 + operational 325,137,398 + market 4,830,805)", nn="5")
g("GTB15-CAR", "car", 201, r"^Total Risk-Weighted Capital Ratio", 416, 428, "Bank Total Risk-Weighted Capital Ratio 18.17% (first occurrence; recomputes 333,426,139 / 1,835,072,113 = 18.17%). Narrative on p200 says 18.11%: internal inconsistency in the source, table value used", nn="5", u="percent")
g("GC-GTBank2015", "gcu", 51, r"REPORT", "", "", "Report of the independent auditor to the members of Guaranty Trust Bank Plc, PDF pp51-52 (image pages, transcribed from 110-dpi renders), complete: "
  "PricewaterhouseCoopers, Daniel Asapokhai FRC/2013/ICAN/00000000946, dated 25 February 2016. Opinion on the separate and consolidated financial statements: true and fair view of the bank and the group (unmodified). "
  "No material-uncertainty, emphasis-of-matter or other-matter paragraph; legal section notes CBN contraventions (Note 47).",
  u="indicator", manual="0", opinion="covers_bank_separate", colhead="Auditor's report on the separate and consolidated financial statements of Guaranty Trust Bank Plc")

# ---------------- GTBank 2016 (xs-b786ea3289, AnnualReports.com mirror) ----------------
B = ("Columns 'Group' | 'Group' | 'Parent' | 'Parent' over 'Dec-2016' | 'Dec-2015' ('In thousands of Nigerian Naira'); "
     "Parent = Guaranty Trust Bank Plc, the operating bank (pre-GTCO); Parent Dec-2016 column used")
a = doc("GTBank", 2016, "xs-b786ea3289", "Guaranty Trust Bank Plc 2016 Annual Report (public mirror: AnnualReports.com; issuer URL returns 404)",
        "2016 annual report, as originally reported (public mirror copy)", "consolidated_and_separate", "bank_separate", B, "NGN thousand", 1)
def g(*args, **kw):
    kw.setdefault("colhead", "Parent Dec-2016")
    a(*args, **kw); OUT[-1]["scope"] = SC
g("GTB16-A", "assets", 78, r"^Total assets", 428, 440, "SOFP Parent Total assets 2,613,340,074 (printed page 77)")
g("GTB16-L", "liabilities", 78, r"^Total liabilities", 428, 440, "SOFP Parent Total liabilities 2,136,422,221")
g("GTB16-E", "equity", 79, r"^Total equity [\d(]", 442, 452, "SOFP Parent Total equity 476,917,853; 2,136,422,221 + 476,917,853 = 2,613,340,074")
g("GTB16-PAT", "pat", 80, r"^Profit for the year", 452, 462, "Income statement Parent Profit for the year 126,836,792")
g("GTB16-PBT", "pbt", 80, r"^Profit before income tax", 452, 462, "Parent Profit before income tax 154,005,487")
g("GTB16-OCF", "ocf", 86, r"^Net cash/\(used in\) provided by operating activities", 430, 440, "Statement of cash flows Parent Net cash provided by operating activities 286,884,139")
g("GTB16-OA", "opening_assets", 78, r"^Total assets", 490, 500, "Prior-year (Parent Dec-2015) column: Total assets 2,277,629,224; not labelled restated; equals the 2015 original (xs-ac933e7f2f p54)",
  colhead="Parent Dec-2015", ori="prior-year comparative in 2016 report (not restated)", cbasis=B.replace("Parent Dec-2016 column used", "Parent Dec-2015 (prior-year) column used"))
g("GTB16-TI", "total_impairment", 80, r"^Loan impairment charges", 452, 462, "Parent Loan impairment charges (63,542,640); no separate impairment line on other financial assets printed in the 2016 income statement", nn="11", sign=-1, sign_reason=EXP)
g("GTB16-GLI", "gross_loans_individuals", 257, r"^Gross loans", 426, 436, "Note 29 Parent Dec-2016 individuals: Gross loans 113,567,868 (printed page 256)", nn="29")
g("GTB16-ALI", "loan_allowance_individuals", 257, r"^Total impairment", 429, 440, "Note 29 Parent individuals Total impairment (2,080,890)", nn="29", sign=-1, sign_reason=ALW)
g("GTB16-GLN", "gross_loans_non-individuals", 257, r"^Gross loans", 419, 430, "Note 29 Parent non-individuals: Gross loans 1,377,549,848 (second occurrence)", nn="29", occ=2)
g("GTB16-ALN", "loan_allowance_non-individuals", 257, r"^Total impairment", 425, 436, "Note 29 Parent non-individuals Total impairment (71,818,874) (second occurrence)", nn="29", occ=2, sign=-1, sign_reason=ALW)
g("GTB16-GL", "gross_loans", 257, "derived", "", "", "Individuals + non-individuals = 1,491,117,716", nn="29", derive="GTB16-GLI+GTB16-GLN")
g("GTB16-ALW", "loan_allowance", 257, "derived", "", "", "Individuals + non-individuals allowance = 73,899,764; gross - allowance = 1,417,217,952 = printed total carrying amount", nn="29", derive="GTB16-ALI+GTB16-ALN")
g("GTB16-NL", "net_loans", 78, r"^Loans and advances to customers", 428, 440, "SOFP Parent Loans and advances to customers 1,417,217,952", nn="29")
g("GTB16-RC", "regulatory_capital", 213, r"^Total Qualifying Capital", 429, 440, "Capital adequacy table headed 'Bank': Total Qualifying Capital (C=A+B) 405,526,626 (printed page 212)", nn="5")
g("GTB16-RWA", "rwa", 213, r"^Aggregate Risk-Weighted Assets", 423, 433, "Bank Aggregate Risk-Weighted Assets 2,049,087,592", nn="5")
g("GTB16-CAR", "car", 213, r"^Total Risk-Weighted Capital Ratio", 443, 453, "Bank Total Risk-Weighted Capital Ratio 19.79% (405,526,626 / 2,049,087,592 = 19.79%)", nn="5", u="percent")
g("GC-GTBank2016", "gcu", 71, r"Our opinion", "", "", "Independent auditor's report to the members of Guaranty Trust Bank Plc, PDF pp71-76 (printed 70-75), complete from 'Our opinion' to signature: "
  "PricewaterhouseCoopers, Obioma Ubah FRC/2013/ICAN/00000002002, dated 2 March 2017. Opinion on the consolidated and separate financial statements (unmodified). KAMs on loan impairment; "
  "no material-uncertainty section, no emphasis-of-matter or other-matter paragraph. Source is the AnnualReports.com mirror (issuer URL returns 404).",
  u="indicator", manual="0", opinion="covers_bank_separate", colhead="Auditor's report on the consolidated and separate financial statements of Guaranty Trust Bank Plc")

# ---------------- GTBank 2021-2022 from GTCO HoldCo packages (explicit operating-bank subsidiary disclosure) ----------------
SCG = "Operating bank (GT Bank Nigeria column of 'Condensed results of consolidated entities' in the audited GTCO HoldCo annual report)"
def gtco_basis(yr, inv, a20check):
    return ("Holding-company report of Guaranty Trust Holding Company Plc; note 'Condensed results of consolidated entities' (b): column headed "
            "'GT Bank Nigeria' beside separate columns for each foreign banking subsidiary (Ghana, Sierra Leone, Liberia, Gambia, Cote d'Ivoire, "
            f"Kenya Group, Tanzania, UK) and Habari Pay ('In thousands of Nigerian Naira'), Dec-{yr}. Entity-only scope: the column carries "
            f"'Investment in subsidiaries' {inv} (foreign subsidiaries held at cost, not consolidated); {a20check}. "
            "Basis: audited HoldCo package - explicit operating-bank subsidiary disclosure; Guaranty Trust Bank Ltd issued no standalone annual report in this set.")
CHK21 = ("the same report's Dec-2020 column (pp248-250) reproduces Guaranty Trust Bank Plc's own audited 2020 Parent statements exactly "
         "(PAT 178,188,398; PBT 205,130,559; total assets 4,061,543,605; net loans 1,410,577,734; OCF 327,793,446)")
CHK22 = "the 2022 report's Dec-2021 column (pp259-261) equals the 2021 report's GT Bank Nigeria figures (PAT 146,184,067; total assets 4,357,033,134)"
for yr, job, title, pg, inv, chk in ((2021, "xs-66a266c90d", "Guaranty Trust Holding Company Plc 2021 Annual Report (HoldCo; issuer site)", None, "56,903,032", CHK21),
                                     (2022, "xs-cf5faa1264", "Guaranty Trust Holding Company Plc 2022 Annual Report (HoldCo; issuer site)", None, "57,595,367", CHK22)):
    globals()["a"] = doc("GTBank", yr, job, title,
        f"GTCO {yr} annual report: audited HoldCo package - explicit operating-bank subsidiary disclosure (GT Bank Nigeria condensed results)",
        "holding_company_report", "bank_subsidiary_disclosure", gtco_basis(yr, inv, chk), "NGN thousand", 0)
    def h(*args, **kw):
        kw.setdefault("colhead", f"GT Bank Nigeria Dec-{yr}")
        a(*args, **kw); OUT[-1]["scope"] = SCG
    if yr == 2021:
        h("GTB21-PAT", "pat", 244, r"^Bank Nigeria 303,977,853", 256, 266, "Condensed full-year profit and loss, GT Bank Nigeria: Profit after tax 146,184,067")
        h("GTB21-PBT", "pbt", 244, r"^Bank Nigeria 303,977,853", 228, 238, "GT Bank Nigeria Profit before tax 176,121,448")
        h("GTB21-LI", "loan_impairment", 244, r"^Bank Nigeria 303,977,853", 200, 210, "GT Bank Nigeria Loan impairment charges (4,088,901). Loan charge only: not used as total impairment because the 2020 condensed loan charge (13,667,341) differs from the bank's 2020 audited total impairment (10,555,467)", sign=-1, sign_reason=EXP)
        h("GTB21-NL", "net_loans", 244, r"^Bank Nigeria 303,977,853", 490, 500, "Condensed financial position, GT Bank Nigeria: Loans and advances to customers 1,475,674,160")
        h("GTB21-A", "assets", 245, r"^162,911,719 ", 208, 218, "Condensed financial position (continued), first entity line = GT Bank Nigeria (column order as on p244, confirmed on 130-dpi render): Total assets 4,357,033,134")
        h("GTB21-L", "liabilities", 245, r"^162,911,719 ", 391, 401, "GT Bank Nigeria Total liabilities 3,610,197,551")
        h("GTB21-E", "equity", 245, r"^162,911,719 ", 405, 415, "GT Bank Nigeria Equity and reserve 746,835,583; 3,610,197,551 + 746,835,583 = 4,357,033,134")
        h("GTB21-OCF", "ocf", 246, r"^Bank Nigeria 364,670,769", 160, 170, "Condensed cash flow Dec-2021, GT Bank Nigeria: net cash from operating activities 364,670,769")
        h("GTB21-OA", "opening_assets", 249, r"^Bank Nigeria 493,209,016", 405, 415, "Same report, condensed financial position Dec-2020, GT Bank Nigeria Total assets 4,061,543,605 (= GTBank Plc 2020 audited Parent total assets)",
          colhead="GT Bank Nigeria Dec-2020", ori="prior-year condensed column in the 2021 HoldCo report")
    else:
        h("GTB22-PAT", "pat", 255, r"^Bank Nigeria 340,912,155", 255, 265, "Condensed full-year profit and loss, GT Bank Nigeria: Profit after tax 145,296,211")
        h("GTB22-PBT", "pbt", 255, r"^Bank Nigeria 340,912,155", 228, 238, "GT Bank Nigeria Profit before tax 180,628,262")
        h("GTB22-LI", "loan_impairment", 255, r"^Bank Nigeria 340,912,155", 200, 210, "GT Bank Nigeria Loan impairment charges (8,937,161); loan charge only, not used as total impairment (see GTB21-LI)", sign=-1, sign_reason=EXP)
        h("GTB22-NL", "net_loans", 255, r"^Bank Nigeria 340,912,155", 457, 467, "Condensed financial position, GT Bank Nigeria: Loans and advances to customers 1,577,191,692")
        h("GTB22-A", "assets", 256, r"^242,427,005 ", 249, 259, "Condensed financial position (continued), first entity line = GT Bank Nigeria (confirmed on 130-dpi render): Total assets 5,208,576,833")
        h("GTB22-L", "liabilities", 256, r"^242,427,005 ", 436, 446, "GT Bank Nigeria Total liabilities 4,412,624,546")
        h("GTB22-E", "equity", 256, r"^242,427,005 ", 450, 460, "GT Bank Nigeria Equity and reserve 795,952,287; 4,412,624,546 + 795,952,287 = 5,208,576,833")
        h("GTB22-OCF", "ocf", 257, r"^Bank Nigeria 671,361,457", 189, 199, "Condensed cash flow Dec-2022, GT Bank Nigeria: net cash from operating activities 671,361,457")
        h("GTB22-OA", "opening_assets", 260, r"^consolidated Bank Nigeria 588,572,038", 365, 375, "Same report, condensed financial position Dec-2021, GT Bank Nigeria Total assets 4,357,033,134 (= 2021 report figure)",
          colhead="GT Bank Nigeria Dec-2021", ori="prior-year condensed column in the 2022 HoldCo report")

# ---------------- Stanbic 2013, 2015-2017 from Stanbic IBTC Holdings HoldCo packages (note 13.4) ----------------
SCS = "Operating bank (Stanbic IBTC Bank PLC column of note 13.4 'Summarised financial statements of the consolidated entities' in the audited Stanbic IBTC Holdings HoldCo report)"
def stan_basis(yr, extra):
    return ("Holding-company report of Stanbic IBTC Holdings PLC; note 13.4 'Summarised financial statements/information of the consolidated entities': "
            "separate columns for Stanbic IBTC Holdings PLC (Company), Stanbic IBTC Bank PLC, Capital, Pension Managers, Asset Management, Ventures, Trustees, "
            f"Insurance Brokers, Investments, Stockbrokers and Eliminations (N million), {yr}. Column used: 'Stanbic IBTC Bank PLC'. Entity-only scope: "
            "'Equity investment in group companies' is nil in the Bank column (no consolidated subsidiaries); the bank operates only in Nigeria. "
            f"{extra} Basis: audited HoldCo package - explicit operating-bank subsidiary disclosure (summarised, not a standalone bank annual report).")
STAN = {
 2013: ("xs-c712bb5b6c", "Stanbic IBTC Holdings PLC Annual Report 2013 (HoldCo; The Vault archive)", 96, 97,
        "Total liabilities printed (654,520) + equity 70,580 = total assets 725,100.",
        dict(PAT=(96, r"^Profit for the year", 1, "10,129"), PBT=(96, r"^Profit before tax", 1, "9,474"), TI=(96, r"^Credit impairment charges", 1, "(2,667)"),
             NL=(96, r"^Loans and advances to customers", 1, "289,747"), A=(96, r"^Total assets", 1, "725,100"), OA=(96, r"^At 31 December 2012", 2, "650,470 (31 Dec 2012)"),
             E=(97, r"^Equity and reserves", 1, "70,580"), L=(97, r"^Total liabilities .Nmillion.", 1, "654,520")), []),
 2014: ("xs-f35c275cf6", "Stanbic IBTC Holdings PLC Annual report 2014 (HoldCo; The Vault archive)", 104, 105,
        "Total liabilities not printed: derived as the sum of the Bank's printed liability lines (829,231) = 911,052 - 81,821. "
        "Prior-year row (2013: PAT 10,129, total assets 725,100) equals the 2013 note.",
        dict(PAT=(104, r"^Profit for the year", 1, "19,456"), PBT=(104, r"^Profit before tax", 1, "21,610"), TI=(104, r"^Credit impairment charges", 1, "(3,217)"),
             NL=(104, r"^Loans and advances to customers", 1, "398,604"), A=(104, r"^Total assets", 1, "911,052"), OA=(104, r"^At 31 December 2013", 2, "725,100 (31 Dec 2013)"),
             E=(105, r"^Equity and reserves", 1, "81,821")),
        [("DL", r"^Derivative liabilities", "2,677"), ("TL", r"^Trading liabilities", "85,283"), ("DB", r"^Deposits from banks", "59,121"),
         ("DC", r"^Deposits from customers", "507,734"), ("OB", r"^Other borrowings", "70,151"), ("SD", r"^Subordinated debt", "22,973"),
         ("CT", r"^Current and deferred tax liabilities", "3,244"), ("PO", r"^Other liabilities", "78,048")]),
 2015: ("xs-40d24d09d3", "Stanbic IBTC Holdings PLC Annual report 2015 (HoldCo; The Vault archive)", 86, 87,
        "Total liabilities not printed: derived as the sum of the Bank's printed liability lines (795,663), which equals total liabilities and equity 890,580 less equity 94,917.",
        dict(PAT=(86, r"^Profit for the year", 1, "6,232"), PBT=(86, r"^Profit before tax", 1, "4,479"), TI=(86, r"^Credit impairment charges", 1, "(14,931)"),
             NL=(86, r"^Loans and advances to customers", 1, "353,513"), A=(86, r"^Total assets", 1, "890,580"), OA=(86, r"^At 31 December 2014", 1, "908,429 (31 Dec 2014)"),
             E=(87, r"^Equity and reserves", 1, "94,917")),
        [("DL", r"^Derivative liabilities", "383"), ("TL", r"^Trading liabilities", "24,101"), ("DB", r"^Deposits from banks", "95,446"),
         ("DC", r"^Deposits from customers", "497,580"), ("OB", r"^Other borrowings", "81,107"), ("SD", r"^Subordinated debt", "23,699"),
         ("CT", r"^Current tax liability", "1,883"), ("PO", r"^Provisions and other liabilities", "71,464")]),
 2016: ("xs-328f885a48", "Stanbic IBTC Holdings PLC 2016 Annual Report (HoldCo; The Vault archive)", 84, 85,
        "Total liabilities not printed: derived as the sum of the Bank's printed liability lines (884,443) = 993,759 - 109,316.",
        dict(PAT=(84, r"^Profit for the year", 1, "15,030"), PBT=(84, r"^Profit before tax", 1, "14,908"), TI=(84, r"^Credit impairment charges", 1, "(19,803)"),
             NL=(84, r"^Loans and advances to customers", 1, "352,965"), A=(84, r"^Total assets", 1, "993,759"), OA=(84, r"^At 31 December 2015", 1, "890,580 (31 Dec 2015)"),
             E=(85, r"^Equity and reserves", 1, "109,316")),
        [("DL", r"^Derivative liabilities", "11,788"), ("TL", r"^Trading liabilities", "5,325"), ("DB", r"^Deposits from banks", "53,766"),
         ("DC", r"^Deposits from customers", "568,675"), ("OB", r"^Other borrowings", "79,633"), ("SD", r"^Subordinated debt", "27,964"),
         ("CT", r"^Current tax liabilities", "1,865"), ("PO", r"^Provisions and other liabilities", "135,427")]),
 2017: ("xs-2d674ef14c", "Stanbic IBTC Holdings PLC 2017 Annual Report (HoldCo; The Vault archive)", 94, 95,
        "Total liabilities not printed: derived as the sum of the Bank's printed liability lines (1,193,969) = 1,332,669 - 138,700. "
        "Cross-check: Stanbic IBTC Bank's own 2018 audited statements give 2017 total assets 1,332,723 (54 million, 0.004%, higher).",
        dict(PAT=(94, r"^Profit for the year .2017.", 1, "28,842"), PBT=(94, r"^Profit before tax", 1, "30,345"), TI=(94, r"^Credit impairment charges", 1, "(25,577)"),
             NL=(94, r"^Loans and advances to customers", 1, "372,088"), A=(94, r"^Total assets .2017.", 1, "1,332,669"), OA=(94, r"^Total assets at 31 December 2016", 1, "993,759 (31 Dec 2016)"),
             E=(95, r"^Equity and reserves", 1, "138,700")),
        [("DL", r"^Derivative liabilities", "2,592"), ("TL", r"^Trading liabilities", "62,449"), ("DB", r"^Deposits from banks", "61,721"),
         ("DC", r"^Deposits from customers", "775,262"), ("OB", r"^Other borrowings", "74,892"), ("SD", r"^Subordinated debt", "29,046"),
         ("CT", r"^Current tax liabilities", "2,412"), ("PO", r"^Provisions and other liabilities", "185,595")]),
}
VAR = dict(PAT="pat", PBT="pbt", TI="total_impairment", NL="net_loans", A="assets", OA="opening_assets", E="equity", L="liabilities")
for yr, (job, title, p1, p2, extra, cells, comps) in STAN.items():
    globals()["a"] = doc("Stanbic", yr, job, title,
        f"Stanbic IBTC Holdings {yr} annual report: audited HoldCo package - explicit operating-bank subsidiary disclosure (note 13.4, Stanbic IBTC Bank PLC)",
        "holding_company_report", "bank_subsidiary_disclosure", stan_basis(yr, extra), "NGN million", None)
    tag = f"STANH{str(yr)[2:]}"
    for k, (pg, rx, occ, val) in cells.items():
        kw = dict(occ=occ, colhead=f"Stanbic IBTC Bank PLC {yr}")
        if k == "TI": kw.update(sign=-1, sign_reason=EXP)
        if k == "OA": kw.update(colhead=f"Stanbic IBTC Bank PLC {yr-1} (prior-year row)", ori=f"prior-year row of note 13.4 in the {yr} HoldCo report")
        a(f"{tag}-{k}", VAR[k], pg, rx, 288, 345, f"Note 13.4 Stanbic IBTC Bank PLC column: {VAR[k]} {val}", **kw)
        OUT[-1]["scope"] = SCS
    for c, rx, val in comps:
        a(f"{tag}-LC{c}", f"liabilities_component_{c.lower()}", p2, rx, 288, 345, f"Note 13.4 Bank liability line {rx[1:]} {val}", colhead=f"Stanbic IBTC Bank PLC {yr}")
        OUT[-1]["scope"] = SCS
    if comps:
        a(f"{tag}-L", "liabilities", p2, "derived", "", "", f"Sum of the Bank's printed liability lines; {extra.split(':')[1].strip() if ':' in extra else ''}",
          derive="+".join(f"{tag}-LC{c}" for c, _, _ in comps), colhead=f"Stanbic IBTC Bank PLC {yr}")
        OUT[-1]["scope"] = SCS

# Stanbic HoldCo PDFs place two printed pages on one PDF page; the Bank column sits on the left-hand printed page.
STAN_PRINTED = {("xs-f35c275cf6", 104): 204, ("xs-f35c275cf6", 105): 206, ("xs-c712bb5b6c", 96): 188, ("xs-c712bb5b6c", 97): 190, ("xs-40d24d09d3", 86): 168, ("xs-40d24d09d3", 87): 170,
                ("xs-328f885a48", 84): 164, ("xs-328f885a48", 85): 166, ("xs-2d674ef14c", 94): 186, ("xs-2d674ef14c", 95): 188}
for o in OUT:
    if o["spec_id"].startswith("STANH"):
        o["printed_page"] = STAN_PRINTED[(o["job_id"], int(o["page"]))]
        o["note_number"] = o["note_number"] or "13.4"

if __name__ == "__main__":
    prefixes = {o["spec_id"] for o in OUT}
    keep = [r for r in csv.DictReader(open(P)) if r["spec_id"] not in prefixes]
    with open(P, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=HDR); w.writeheader(); w.writerows(keep); w.writerows(OUT)
    print(len(OUT), "staged specs written")
