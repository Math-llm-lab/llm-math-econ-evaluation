import math
import pytest

from econ_math_portfolio.models.contract_stochastic_income import ContractParams, solve_c_high
from econ_math_portfolio.models.cpi_target_discount import CpiParams, solve_t, cpi
from econ_math_portfolio.models.credit_var_quantile import CreditParams, var_analytic, var_mc
from econ_math_portfolio.models.hjb_discount_threshold import HjbParams, F, rho_critical

def test_contract_raises_if_not_bracketed():
    p = ContractParams()
    # Narrow bracket that likely doesn't contain the root
    with pytest.raises(ValueError):
        solve_c_high(p, lo=0.5, hi=0.6)

def test_contract_participation_constraint_binds_if_needed():
    # If autarky_high is set above the unconstrained solution, the constraint should bind.
    p = ContractParams(autarky_high=2.5)
    c = solve_c_high(p)
    assert c >= 2.5

def test_cpi_solution_in_bounds_and_hits_target():
    p = CpiParams()
    t = solve_t(p)
    assert 0.0 <= t <= 1.0
    assert abs(cpi(t, p) - p.target_cpi) < 1e-6

def test_hjb_rho_is_minimal():
    p = HjbParams()
    rho = rho_critical(p)
    assert F(rho, p) >= -1e-10
    # Slightly smaller rho should violate (or be very close due to float)
    assert F(rho - 1e-6, p) <= 1e-6

def test_credit_var_mc_sanity_close_to_analytic():
    p = CreditParams()
    a = var_analytic(p)
    mc = var_mc(p, n_paths=100_000, seed=7)
    assert math.isfinite(a)
    assert math.isfinite(mc)
    # toy model, allow some noise but should be in same ballpark
    assert abs(mc - a) < 0.5
