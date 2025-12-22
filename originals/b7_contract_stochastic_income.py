from __future__ import annotations

import math


def solve_contract() -> float:
    """Solve for high-state consumption in a two-state stochastic contract.

    Uses bisection to match a target lifetime utility under log preferences,
    with a participation (exit) constraint in the high-income state.
    """
    delta = 0.95
    prob = 0.5
    c_low = 0.95
    v0_target = 3.0

    def expected_value(c_high: float) -> float:
        if c_high <= 0:
            return -math.inf
        eu = prob * math.log(c_low) + prob * math.log(c_high)
        return eu / (1.0 - delta)

    def exit_constraint(c_high: float) -> bool:
        # Participation constraint in the high-income state:
        # requires c_high >= 1.1 (autarky consumption).
        return c_high >= 1.1

    tol = 1e-8
    lo, hi = 1e-8, 10.0

    if expected_value(lo) > v0_target:
        raise ValueError("Target utility too low for lower bound.")
    if expected_value(hi) < v0_target:
        raise ValueError("Target utility too high for upper bound.")

    while hi - lo > tol:
        mid = 0.5 * (lo + hi)
        if expected_value(mid) < v0_target:
            lo = mid
        else:
            hi = mid

    sol = 0.5 * (lo + hi)

    # Enforce the exit constraint (minimal feasible c_high).
    if not exit_constraint(sol):
        sol = 1.1

    return float(sol)


if __name__ == "__main__":
    print(solve_contract())
