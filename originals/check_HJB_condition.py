from __future__ import annotations

# Original-style script: HJB inequality check at a test state.
#
# Notes:
# - This script is kept in `originals/` for transparency.
# - The repo's main implementation lives in:
#   `src/econ_math_portfolio/models/hjb_discount_threshold.py`
#
# We check the inequality in the form used in the repo:
#   F(rho) = rho*w^gamma + b*p*gamma*y*w^(gamma-1) + 0.5*sigma^2*p^2*gamma*(gamma-1)*y^2*w^(gamma-2)
# and compute rho_critical (smallest rho with F(rho) >= 0) at x=0,y=1,p=1.

# Model parameters
b = 1.0
sigma = 0.2
gamma = 0.7


def F(rho: float, x: float, y: float, p: float) -> float:
    w = x + p * y
    if w <= 0:
        raise ValueError("Wealth must be positive.")
    return (
        rho * (w**gamma)
        + b * p * gamma * y * (w ** (gamma - 1))
        + 0.5 * (sigma**2) * (p**2) * gamma * (gamma - 1) * (y**2) * (w ** (gamma - 2))
    )


def rho_critical(x: float, y: float, p: float) -> float:
    w = x + p * y
    if w <= 0:
        raise ValueError("Wealth must be positive.")
    const = (
        b * p * gamma * y * (w ** (gamma - 1))
        + 0.5 * (sigma**2) * (p**2) * gamma * (gamma - 1) * (y**2) * (w ** (gamma - 2))
    )
    return (-const) / (w**gamma)


if __name__ == "__main__":
    p_test = 1.0
    x_test = 0.0
    y_test = 1.0

    rho_star = rho_critical(x_test, y_test, p_test)
    test_rhos = [rho_star - 0.01, rho_star, rho_star + 0.01]

    print(f"Critical rho (rho*): {rho_star:.6f}")
    print(f"Test state: x={x_test}, y={y_test}, p={p_test}")
    print("=" * 60)

    for rho in test_rhos:
        value = F(rho, x_test, y_test, p_test)
        status = "SATISFIED" if value >= 0 else "VIOLATED"
        print(f"rho = {rho:.6f}")
        print(f"delta vs critical: {rho - rho_star:+.6f}")
        print(f"F(rho) = {value:.6f}")
        print(f"Inequality status: {status}")
        print("-" * 60)
