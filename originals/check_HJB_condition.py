from __future__ import annotations

# Original-style script: HJB inequality check at a test state.
# Kept for transparency; main implementation lives in models/.

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
        + 0.5
        * sigma**2
        * p**2
        * gamma
        * (gamma - 1)
        * y**2
        * (w ** (gamma - 2))
    )


def rho_critical(x: float, y: float, p: float) -> float:
    w = x + p * y
    if w <= 0:
        raise ValueError("Wealth must be positive.")

    const = (
        b * p * gamma * y * (w ** (gamma - 1))
        + 0.5
        * sigma**2
        * p**2
        * gamma
        * (gamma - 1)
        * y**2
        * (w ** (gamma - 2))
    )
    return -const / (w**gamma)


if __name__ == "__main__":
    x0, y0, p0 = 0.0, 1.0, 1.0
    rho_star = rho_critical(x0, y0, p0)
    print(f"Critical rho: {rho_star:.6f}")