import importlib
from pathlib import Path

from econ_math_portfolio.scoring import load_rubric, score_submission


def test_scoring_correct_answer_scores_high(tmp_path):
    rubric = load_rubric(Path("rubrics/rubric.json"))
    v = importlib.import_module("validators.contract_stochastic_income")
    sb = score_submission(
        task_id="contract_stochastic_income",
        answer=v.EXPECTED,
        explanation="Bisection root-finding; then constraint check.",
        expected=float(v.EXPECTED),
        rubric=rubric,
    )
    assert sb.total >= 0.9


def test_scoring_bad_format_scores_zeroish():
    rubric = load_rubric(Path("rubrics/rubric.json"))
    v = importlib.import_module("validators.contract_stochastic_income")
    sb = score_submission(
        task_id="contract_stochastic_income",
        answer="not-a-number",
        explanation=None,
        expected=float(v.EXPECTED),
        rubric=rubric,
    )
    assert sb.total <= 0.2


def test_bounds_note_does_not_crash():
    rubric = load_rubric(Path("rubrics/rubric.json"))
    v = importlib.import_module("validators.cpi_target_discount")
    sb = score_submission(
        task_id="cpi_target_discount",
        answer=2.0,
        explanation="",
        expected=float(v.EXPECTED),
        rubric=rubric,
    )
    # out of bounds should not get full numeric credit
    assert sb.total < 1.0
