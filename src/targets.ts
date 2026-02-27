export type TargetCompany = {
  id: string;
  name: string;
  ticker: string;
  aliases: string[];
};

export const TARGETS: TargetCompany[] = [
  {
    id: "nigerian_enamelware",
    name: "Nigerian Enamelware Plc",
    ticker: "ENAMELWA",
    aliases: ["Nigerian Enamelware", "Enamelware Plc"],
  },
  {
    id: "academy_press",
    name: "Academy Press Plc",
    ticker: "ACADEMY",
    aliases: ["Academy Press"],
  },
  {
    id: "oando",
    name: "Oando Plc",
    ticker: "OANDO",
    aliases: ["Oando"],
  },
  {
    id: "sterling_holdco",
    name: "Sterling Financial Holdings Plc",
    ticker: "STERLNBANK",
    aliases: [
      "Sterling Financial Holdings",
      "Sterling HoldCo",
      "Sterling Bank",
      "Sterling Bank Plc",
    ],
  },
  {
    id: "aso_savings",
    name: "Aso Savings and Loans Plc",
    ticker: "ASOSAVINGS",
    aliases: ["Aso Savings", "Aso Savings and Loans"],
  },
  {
    id: "nnfm",
    name: "Northern Nigeria Flour Mills Plc",
    ticker: "NNFM",
    aliases: ["NNFMN", "NNFM", "Northern Nigeria Flour Mills"],
  },
  {
    id: "beta_glass",
    name: "Beta Glass Plc",
    ticker: "BETAGLAS",
    aliases: ["Beta Glass"],
  },
];
