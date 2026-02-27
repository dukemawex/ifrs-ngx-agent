export type TargetCompany = {
  id: string;
  name: string;
  aliases: string[];
};

export const TARGETS: TargetCompany[] = [
  {
    id: "nigerian_enamelware",
    name: "Nigerian Enamelware Plc",
    aliases: ["Nigerian Enamelware", "Enamelware Plc"],
  },
  {
    id: "academy_press",
    name: "Academy Press Plc",
    aliases: ["Academy Press"],
  },
  {
    id: "oando",
    name: "Oando Plc",
    aliases: ["Oando"],
  },
  {
    id: "sterling_holdco",
    name: "Sterling Financial Holdings Plc",
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
    aliases: ["Aso Savings", "Aso Savings and Loans"],
  },
  {
    id: "nnfm",
    name: "Northern Nigeria Flour Mills Plc",
    aliases: ["NNFMN", "NNFM", "Northern Nigeria Flour Mills"],
  },
  {
    id: "beta_glass",
    name: "Beta Glass Plc",
    aliases: ["Beta Glass"],
  },
];
