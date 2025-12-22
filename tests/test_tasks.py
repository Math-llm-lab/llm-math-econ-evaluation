import importlib
import math

import pytest

TASKS = [
    "contract_stochastic_income",
    "hjb_discount_threshold",
    "cpi_target_discount",
    "credit_var_quantile",
]


@pytest.mark.parametrize("task_id", TASKS)
def test_reference_is_finite(task_id):
    v = importlib.import_module(f"validators.{task_id}")
    ans = v.reference_compute()
    assert math.isfinite(ans)


@pytest.mark.parametrize("task_id", TASKS)
def test_validator_accepts_expected(task_id):
    v = importlib.import_module(f"validators.{task_id}")
    assert v.validate(v.EXPECTED)["ok"] is True


@pytest.mark.parametrize("task_id", TASKS)
def test_validator_rejects_wrong(task_id):
    v = importlib.import_module(f"validators.{task_id}")
    assert v.validate(v.EXPECTED + 100 * v.TOL)["ok"] is False
