from __future__ import annotations

import math
import random
from dataclasses import dataclass
from statistics import NormalDist


@dataclass(frozen=True)
class CreditParams:
    E: float = 100.0
    LGD: float = 0.6
    PD: float = 0.02
    rho: float = 0.2
    alpha: float = 0.999


def var_analytic(params: CreditParams) -> float:
    nd = NormalDist()
    q = nd.cdf(
        (nd.inv_cdf(params.PD) + math.sqrt(params.rho) * nd.inv_cdf(params.alpha))
        / math.sqrt(1 - params.rho)
    )
    return params.E * params.LGD * q


def var_mc(params: CreditParams, *, n_paths: int = 50_000, seed: int = 7) -> float:
    """Monte Carlo estimate of VaR for an *infinitely granular* Vasicek portfolio.

    We simulate only the systematic factor Z ~ N(0,1). Conditional on Z, the default rate is
    q(Z) = Phi((Phi^{-1}(PD) + sqrt(rho)*Z)/sqrt(1-rho)).
    Loss is then L = E*LGD*q(Z).
    """
    nd = NormalDist()
    rnd = random.Random(seed)
    pd_thresh = nd.inv_cdf(params.PD)

    losses = []
    for _ in range(n_paths):
        z = nd.inv_cdf(rnd.random())
        q = nd.cdf((pd_thresh + math.sqrt(params.rho) * z) / math.sqrt(1.0 - params.rho))
        losses.append(params.E * params.LGD * q)

    losses.sort()
    idx = int(params.alpha * (n_paths - 1))
    return float(losses[idx])


def var_with_sanity_check(
    params: CreditParams, *, mc_paths: int = 50_000, seed: int = 7, max_gap: float = 5.0
) -> float:
    analytic = var_analytic(params)
    mc = var_mc(params, n_paths=mc_paths, seed=seed)
    if abs(mc - analytic) > max_gap:
        raise RuntimeError("Monte Carlo sanity-check too far from analytic VaR.")
    return analytic
