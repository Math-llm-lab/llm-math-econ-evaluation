from __future__ import annotations

import math


def solve_contract() -> float:
    # --- Inputs ---
    delta = 0.95
    prob = 0.5  # equal probability for the two income states
    c_low = 0.95
    V0_target = 3.0

    # Autarky utilities (if consumption equals income)
    V_aut_high = math.log(1.1) / (1 - delta)

    # Expected lifetime utility under the contract (given c_high)
    def expected_value(c_high: float) -> float:
        if c_high <= 0:
            return -math.inf
        exp_u = prob * math.log(c_low) + prob * math.log(c_high)
        return exp_u / (1 - delta)

    # Participation / exit constraint in the high-income state:
    # log(c_high)/(1-delta) >= log(1.1)/(1-delta)  =>  c_high >= 1.1
    def exit_constraint(c_high: float) -> bool:
        return c_high >= 1.1

    # Solve expected_value(c_high) = V0_target via bisection on (0, 10)
    tol = 1e-8
    low, high = 1e-8, 10.0

    # Bracketing check (monotone in c_high)
    if expected_value(low) > V0_target:
        raise ValueError("Target too low for the chosen lower bound.")
    if expected_value(high) < V0_target:
        raise ValueError("Target too high for the chosen upper bound.")

    while high - low > tol:
        mid = (low + high) / 2
        val = expected_value(mid)
        if val < V0_target:
            low = mid
        else:
            high = mid

    solution = (low + high) / 2

    # Enforce exit constraint if needed
    if not exit_constraint(solution):
        print("Exit constraint not satisfied by the utility-matching solution.")
        print("Raising c_high to the minimum feasible value: 1.100000")
        solution = max(solution, 1.1)
    else:
        print("Solution satisfies both the target utility and the exit constraint.")

    print(f"c_high (income=1.1): {solution:.6f}")
    print(f"Contract lifetime utility: {expected_value(solution):.6f}")
    print(
        f"High-state lifetime utility: {math.log(solution)/(1 - delta):.6f} "
        f"(autarky minimum: {V_aut_high:.6f})"
    )
    return float(solution)


if __name__ == "__main__":
    solve_contract()
