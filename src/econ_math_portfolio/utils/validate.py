from __future__ import annotations

def result(task_id: str, expected: float, tol: float, answer: float) -> dict:
    ok = abs(answer - expected) <= tol
    return {
        "task_id": task_id,
        "expected": expected,
        "tolerance": tol,
        "answer": float(answer),
        "ok": bool(ok),
        "abs_error": float(abs(answer - expected)),
    }
