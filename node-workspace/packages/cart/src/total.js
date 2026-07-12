import { roundPrice } from "../../money/src/round.js";

export function cartTotal(items) {
  return roundPrice(items.reduce((sum, it) => sum + it.price * it.qty, 0));
}
