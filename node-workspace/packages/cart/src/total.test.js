import { expect, test } from "vitest";
import { cartTotal } from "./total.js";

test("totals a cart", () => {
  expect(cartTotal([{ price: 2, qty: 2 }, { price: 1.5, qty: 1 }])).toBe(5.5);
});
