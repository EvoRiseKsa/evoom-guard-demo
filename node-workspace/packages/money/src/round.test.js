import { expect, test } from "vitest";
import { roundPrice } from "./round.js";

test("rounds half-up to 2 decimals", () => {
  expect(roundPrice(1.005)).toBe(1.01);
  expect(roundPrice(2.675)).toBe(2.68);
});

test("keeps exact cents untouched", () => {
  expect(roundPrice(3.1)).toBe(3.1);
});
