from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional, Tuple


@dataclass(frozen=True)
class ScoreBreakdown:
    total: float
    format_score: float
    numeric_score: float
    reasoning_score: float
    reasons: list[str]


def load_rubric(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _coerce_float(x: Any) -> Tuple[Optional[float], str | None]:
    try:
        if isinstance(x, bool):
            return None, "answer is boolean, expected float"
        return float(x), None
    except Exception:
        return None, "answer is not a number"


def score_submission(
    *,
    task_id: str,
    answer: Any,
    explanation: str | None,
    expected: float,
    rubric: dict,
) -> ScoreBreakdown:
    cfg = rubric["scoring"]["components"]
    w_format = float(cfg["format"])
    w_num = float(cfg["numeric_correctness"])
    w_reason = float(cfg["reasoning_quality"])

    task_cfg = rubric["tasks"].get(task_id)
    if task_cfg is None:
        return ScoreBreakdown(
            total=0.0,
            format_score=0.0,
            numeric_score=0.0,
            reasoning_score=0.0,
            reasons=[f"unknown task_id: {task_id}"],
        )

    reasons: list[str] = []

    val, err = _coerce_float(answer)
    if err:
        reasons.append(err)
        format_score = 0.0
        numeric_score = 0.0
    else:
        format_score = 1.0
        bounds = task_cfg.get("bounds")
        if bounds is not None and val is not None:
            lo = float(bounds.get("min", float("-inf")))
            hi = float(bounds.get("max", float("inf")))
            if not (lo <= val <= hi):
                reasons.append(f"answer out of bounds [{lo}, {hi}]")

        tol = float(task_cfg.get("tolerance", 0.0))
        abs_err = abs(val - expected) if val is not None else float("inf")
        if abs_err <= tol:
            numeric_score = 1.0
        else:
            numeric_score = 0.0
            reasons.append(f"abs_error={abs_err} exceeds tolerance={tol}")

    reasoning_score = 0.0
    req_exp = bool(task_cfg.get("require_explanation", False))
    if req_exp and (not explanation or not explanation.strip()):
        reasons.append("missing explanation")
        reasoning_score = 0.0
    else:
        if explanation and len(explanation.strip().split()) >= 8:
            reasoning_score = 1.0

    total = (w_format * format_score) + (w_num * numeric_score) + (w_reason * reasoning_score)
    return ScoreBreakdown(
        total=round(total, 6),
        format_score=round(format_score, 6),
        numeric_score=round(numeric_score, 6),
        reasoning_score=round(reasoning_score, 6),
        reasons=reasons,
    )


def load_submission_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def to_json_dict(sb: ScoreBreakdown) -> Dict[str, Any]:
    return {
        "total": sb.total,
        "format_score": sb.format_score,
        "numeric_score": sb.numeric_score,
        "reasoning_score": sb.reasoning_score,
        "reasons": sb.reasons,
    }
