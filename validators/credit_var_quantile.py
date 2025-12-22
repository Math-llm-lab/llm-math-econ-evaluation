from __future__ import annotations

from econ_math_portfolio.models.credit_var_quantile import (
    CreditParams,
    var_with_sanity_check,
)
from econ_math_portfolio.utils.validate import result

TASK_ID = "credit_var_quantile"
TOL = 1e-6


def reference_compute() -> float:
    return var_with_sanity_check(
        CreditParams(),
        mc_paths=50_000,
        seed=7,
        max_gap=5.0,
    )


EXPECTED = reference_compute()


def validate(answer: float) -> dict:
    return result(TASK_ID, EXPECTED, TOL, float(answer))