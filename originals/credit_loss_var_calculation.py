from __future__ import annotations

import math
from dataclasses import dataclass
from statistics import NormalDist


def harq_sigma_forecast(sigma_t: float, sigma_4: float, sigma_21: float, Q_t: float) -> float:
    """Simplified HARQ-F volatility forecast (demo).

    Uses illustrative weights (not calibrated).
    Inputs are decimals (e.g., 2.5% -> 0.025).
    """
    w1, w2, w3 = 0.6, 0.3, 0.1
    hat_sigma = w1 * sigma_t + w2 * sigma_4 + w3 * sigma_21

    # Simple quarticity adjustment (demo)
    adj_factor = 1.0 + 0.5 * Q_t
    return hat_sigma * adj_factor


def calculate_exposure(hat_sigma: float) -> float:
    """Exposure model: E = 15 + 40 * hat_sigma (million USD)."""
    return 15.0 + 40.0 * hat_sigma


def estimate_E_sigma(Q_t: float, multiplier: float = 40.0) -> float:
    """Approximate exposure std via quarticity: sigma(E) approx multiplier * sqrt(Q_t)."""
    return multiplier * math.sqrt(Q_t)


@dataclass(frozen=True)
class VasicekParams:
    PD: float = 0.058
    LGD: float = 0.6
    rho: float = 0.7
    alpha: float = 0.999


def var_999_vasicek_infinite_granular(E: float, params: VasicekParams) -> float:
    """99.9% VaR for an infinitely granular Vasicek portfolio.

    q_alpha = Phi((Phi^{-1}(PD) + sqrt(rho)*Phi^{-1}(alpha)) / sqrt(1-rho))
    VaR = E * LGD * q_alpha
    """
    nd = NormalDist()
    q = nd.cdf(
        (nd.inv_cdf(params.PD) + math.sqrt(params.rho) * nd.inv_cdf(params.alpha))
        / math.sqrt(1.0 - params.rho)
    )
    return params.LGD * E * q


if __name__ == "__main__":
    # Inputs (decimals)
    sigma_t = 0.025
    sigma_4 = 0.021
    sigma_21 = 0.018
    Q_t = 0.0003

    params = VasicekParams(PD=0.058, LGD=0.6, rho=0.7, alpha=0.999)

    # Step 1: forecast volatility
    hat_sigma = harq_sigma_forecast(sigma_t, sigma_4, sigma_21, Q_t)
    print(f"Forecast volatility hat_sigma: {hat_sigma:.6f}")

    # Step 2: exposure
    E_mu = calculate_exposure(hat_sigma)
    print(f"Mean exposure E_mu: {E_mu:.6f} million USD")

    # Step 3: exposure dispersion (kept for demo)
    E_sigma = estimate_E_sigma(Q_t)
    print(f"Exposure std estimate E_sigma: {E_sigma:.6f} million USD")

    # Step 4: compute VaR 99.9%
    VaR_999 = var_999_vasicek_infinite_granular(E_mu, params)
    print(f"99.9% VaR (Vasicek, infinite granular): {VaR_999:.6f} million USD")
