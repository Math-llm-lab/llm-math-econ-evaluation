from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class CpiParams:
    EI_a: float = 200.0
    EI_b: float = 100.0
    base_c: float = 3.15
    price_c: float = 10.0
    discount_coeff: float = 0.21
    target_cpi: float = 200.0


def ei_c(t: float, params: CpiParams) -> float:
    return (params.price_c * (1.0 - params.discount_coeff * t) / params.base_c) * 100.0


def cpi(t: float, params: CpiParams) -> float:
    return (params.EI_a + params.EI_b + ei_c(t, params)) / 3.0


def solve_t(params: CpiParams, *, lo: float = 0.0, hi: float = 1.0, iters: int = 200) -> float:
    def f(x: float) -> float:
        return cpi(x, params) - params.target_cpi

    f_lo = f(lo)
    f_hi = f(hi)
    if f_lo * f_hi > 0:
        raise ValueError("Target not bracketed on [0,1].")

    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        f_mid = f(mid)
        if abs(f_mid) < 1e-12:
            return mid
        if f_lo * f_mid <= 0:
            hi = mid
            f_hi = f_mid
        else:
            lo = mid
            f_lo = f_mid
    return 0.5 * (lo + hi)
