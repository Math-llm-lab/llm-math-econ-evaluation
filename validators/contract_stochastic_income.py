from __future__ import annotations

from econ_math_portfolio.models.contract_stochastic_income import (
    ContractParams,
    solve_c_high,
)
from econ_math_portfolio.utils.validate import result

TASK_ID = "contract_stochastic_income"
TOL = 1e-6


def reference_compute() -> float:
    return solve_c_high(ContractParams())


EXPECTED = reference_compute()


def validate(answer: float) -> dict:
    return result(TASK_ID, EXPECTED, TOL, float(answer))
