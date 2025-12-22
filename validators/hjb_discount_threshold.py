from __future__ import annotations

from econ_math_portfolio.models.hjb_discount_threshold import (
    HjbParams,
    rho_critical,
)
from econ_math_portfolio.utils.validate import result

TASK_ID = "hjb_discount_threshold"
TOL = 1e-6


def reference_compute() -> float:
    return rho_critical(HjbParams())


EXPECTED = reference_compute()


def validate(answer: float) -> dict:
    return result(TASK_ID, EXPECTED, TOL, float(answer))