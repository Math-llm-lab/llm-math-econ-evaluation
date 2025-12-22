from econ_math_portfolio.models.cpi_target_discount import CpiParams, cpi, solve_t
from econ_math_portfolio.models.contract_stochastic_income import ContractParams, lifetime_utility, solve_c_high

def test_cpi_bisection_hits_target():
    p = CpiParams()
    t = solve_t(p)
    assert abs(cpi(t, p) - p.target_cpi) < 1e-6

def test_contract_solver_hits_target_or_constraint_binds():
    p = ContractParams()
    c_high = solve_c_high(p)
    v = lifetime_utility(p.delta, p.c_low, c_high)
    assert v >= p.V0 - 1e-6
    assert c_high >= p.autarky_high
