from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HjbParams:
    b: float = 1.0
    sigma: float = 0.2
    gamma: float = 0.7
    x: float = 0.0
    y: float = 1.0
    p: float = 1.0


def F(rho: float, params: HjbParams) -> float:
    w = params.x + params.p * params.y
    return (
        rho * (w**params.gamma)
        + params.b * params.p * params.gamma * params.y * (w ** (params.gamma - 1))
        + 0.5
        * (params.sigma**2)
        * (params.p**2)
        * params.gamma
        * (params.gamma - 1)
        * (params.y**2)
        * (w ** (params.gamma - 2))
    )


def rho_critical(params: HjbParams) -> float:
    w = params.x + params.p * params.y
    const = params.b * params.p * params.gamma * params.y * (w ** (params.gamma - 1)) + 0.5 * (
        params.sigma**2
    ) * (params.p**2) * params.gamma * (params.gamma - 1) * (params.y**2) * (
        w ** (params.gamma - 2)
    )
    rho = (-const) / (w**params.gamma)
    if F(rho, params) < -1e-10:
        raise RuntimeError("Verification failed: F(rho_critical) < 0.")
    return rho
