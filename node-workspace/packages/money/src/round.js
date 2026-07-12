// Round a price to 2 decimals, half-up. BUG: truncates instead of rounding.
export function roundPrice(value) {
  return Math.trunc(value * 100) / 100;
}
