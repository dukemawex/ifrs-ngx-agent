export const START_YEAR = 2010;
export const END_YEAR = 2023;
export const IFRS_BREAK = 2012;

export const YEARS: number[] = Array.from(
  { length: END_YEAR - START_YEAR + 1 },
  (_, i) => START_YEAR + i,
);
