from __future__ import annotations

from econ_math_portfolio.models.cpi_target_discount import CpiParams, solve_t
from econ_math_portfolio.utils.validate import result

TASK_ID = "cpi_target_discount"
TOL = 1e-5


def reference_compute() -> float:
    return solve_t(CpiParams())


EXPECTED = reference_compute()


def validate(answer: float) -> dict:
    return result(TASK_ID, EXPECTED, TOL, float(answer))