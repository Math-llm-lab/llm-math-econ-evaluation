from __future__ import annotations

import math
from dataclasses import dataclass


@dataclass(frozen=True)
class ContractParams:
    delta: float = 0.95
    V0: float = 3.0
    c_low: float = 0.95
    autarky_high: float = 1.1


def lifetime_utility(delta: float, c_low: float, c_high: float) -> float:
    return (0.5 * math.log(c_low) + 0.5 * math.log(c_high)) / (1.0 - delta)


def solve_c_high(
    params: ContractParams, *, lo: float = 1e-8, hi: float = 10.0, iters: int = 200
) -> float:
    def f(c_high: float) -> float:
        return lifetime_utility(params.delta, params.c_low, c_high) - params.V0

    f_lo = f(lo)
    f_hi = f(hi)
    if f_lo * f_hi > 0:
        raise ValueError("Root not bracketed: widen [lo, hi].")

    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        f_mid = f(mid)
        if abs(f_mid) < 1e-12:
            c_high = mid
            break
        if f_lo * f_mid <= 0:
            hi = mid
            f_hi = f_mid
        else:
            lo = mid
            f_lo = f_mid
    else:
        c_high = 0.5 * (lo + hi)

    return max(c_high, params.autarky_high)
