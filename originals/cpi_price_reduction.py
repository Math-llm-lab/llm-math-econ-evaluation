from __future__ import annotations

import numpy as np

# Original-style script: expected CPI under availability + discount, solved by bisection.
#
# Notes:
# - This file is intentionally more verbose (input validation, richer model).
# - The portfolio's main CPI task is the simpler bisection version in:
#   `src/econ_math_portfolio/models/cpi_target_discount.py`

# --- Inputs ---
prices = {
    "a": {"x": 2, "y": 3, "z": 4, "g": 3},
    "b": {"x": 4, "y": 3, "z": 2, "g": 4},
    "c": {"x": 10, "y": 10, "z": 10, "g": 10},
}

P_base = {"a": 1, "b": 2, "c": 3.15}
weights = {"a": 1 / 3, "b": 1 / 3, "c": 1 / 3}

M = 2  # number of periods

# Availability transition (example)
p11 = 0.5
p01 = 0.15
p_A1_1 = 0.2

target_CPI = 200.00


def _check_prob(p: float) -> None:
    if not (0.0 <= p <= 1.0):
        raise ValueError(f"Probability {p} is outside [0, 1]")


for prob in [p11, p01, p_A1_1]:
    _check_prob(prob)

if target_CPI <= 0:
    raise ValueError("Target CPI must be positive.")

for prod in ["a", "b", "c"]:
    for brand in ["x", "y", "z", "g"]:
        price = prices[prod][brand]
        if price < 0:
            raise ValueError(f"Negative price for {prod}, {brand}.")

for w in weights.values():
    if not (0 <= w <= 1):
        raise ValueError("Product weight is outside [0,1].")

if not np.isclose(sum(weights.values()), 1.0):
    raise ValueError("Weights must sum to 1.")


def availability_probs() -> list[float]:
    # Availability probabilities for g in each period
    p_A1 = p_A1_1
    p_A2 = p11 * p_A1 + p01 * (1 - p_A1)
    return [p_A1, p_A2]


def expected_min_price(t: float, product: str) -> float:
    # Expected minimum price across brands (x,y,z) vs discounted g, averaged over periods
    p_A = availability_probs()
    alt_prices = [prices[product][b] for b in ["x", "y", "z"]]
    alt_min = min(alt_prices)

    g_price_discounted = prices[product]["g"] * (1 - t)

    exp_price_sum = 0.0
    for i in range(M):
        min_if_g = min(alt_min, g_price_discounted)
        exp_price_i = p_A[i] * min_if_g + (1 - p_A[i]) * alt_min
        exp_price_sum += exp_price_i
    return exp_price_sum / M


def compute_index(t: float) -> float:
    # Compute CPI index I(t) given discount t in [0,1]
    EI: dict[str, float] = {}
    for product in ["a", "b", "c"]:
        exp_price = expected_min_price(t, product)
        EI[product] = (exp_price / P_base[product]) * 100.0
    return sum(weights[p] * EI[p] for p in EI)


def find_t_bisect(eps: float = 1e-5) -> float:
    # Bisection on t in [0,1]. Assumes CPI(t) is monotone decreasing in t.
    low, high = 0.0, 1.0
    f_low = compute_index(low) - target_CPI
    f_high = compute_index(high) - target_CPI
    if f_low * f_high > 0:
        raise ValueError("Target not bracketed on [0,1].")

    while high - low > eps:
        mid = (low + high) / 2
        val = compute_index(mid)
        if val > target_CPI:
            # CPI too high -> increase discount
            low = mid
        else:
            high = mid
    return round((low + high) / 2, 5)


def verify_solution(t: float, tolerance: float = 1e-2) -> bool:
    computed_cpi = compute_index(t)
    diff = abs(computed_cpi - target_CPI)
    print(f"Check for t={t}: computed CPI={computed_cpi:.4f}, diff={diff:.4f}")
    ok = diff <= tolerance
    print("OK" if ok else "NOT OK")
    return ok


if __name__ == "__main__":
    t_optimal = find_t_bisect()
    print(f"Optimal discount t = {t_optimal}")
    verify_solution(t_optimal)
