from __future__ import annotations

import argparse
import json
from importlib import import_module
from pathlib import Path
from typing import Any

from econ_math_portfolio.scoring import load_submission_json, score_submission, to_json_dict, load_rubric

def _repo_root() -> Path:
    return Path(__file__).resolve().parents[2]

def _validators_dir() -> Path:
    return _repo_root() / "validators"

def _load_validator(task_id: str):
    return import_module(f"validators.{task_id}")

def _emit(obj: Any, *, as_json: bool) -> None:
    if as_json:
        print(json.dumps(obj, indent=2, sort_keys=True))
    else:
        if isinstance(obj, dict):
            print(obj)
        else:
            print(obj)

def cmd_list(*, as_json: bool) -> int:
    tasks = sorted([p.stem for p in _validators_dir().glob("*.py") if p.name != "__init__.py"])
    _emit({"tasks": tasks}, as_json=as_json)
    return 0

def cmd_reference(task_id: str, *, as_json: bool) -> int:
    v = _load_validator(task_id)
    value = float(v.reference_compute())
    _emit({"task_id": task_id, "reference": value}, as_json=as_json)
    return 0

def cmd_validate(task_id: str, answer: float, *, as_json: bool) -> int:
    v = _load_validator(task_id)
    res = v.validate(answer)
    _emit(res, as_json=as_json)
    return 0 if res["ok"] else 2

def cmd_score(submission_path: str, *, as_json: bool) -> int:
    sub_path = Path(submission_path)
    payload = load_submission_json(sub_path)
    task_id = str(payload.get("task_id", "")).strip()
    answer = payload.get("answer", None)
    explanation = payload.get("explanation", None)

    v = _load_validator(task_id)
    expected = float(v.EXPECTED)

    rubric_path = _repo_root() / "rubrics" / "rubric.json"
    rubric = load_rubric(rubric_path)

    sb = score_submission(
        task_id=task_id,
        answer=answer,
        explanation=explanation if isinstance(explanation, str) else None,
        expected=expected,
        rubric=rubric,
    )
    out = {"task_id": task_id, "score": to_json_dict(sb)}
    _emit(out, as_json=as_json)
    return 0 if sb.total >= 0.8 else 2

def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="econ-math-portfolio", description="Math/Econ reasoning tasks + validators.")
    p.add_argument("--json", action="store_true", help="Output machine-readable JSON.")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("list", help="List task IDs")

    r = sub.add_parser("reference", help="Compute the reference answer for a task")
    r.add_argument("task_id")

    v = sub.add_parser("validate", help="Validate an answer for a task")
    v.add_argument("task_id")
    v.add_argument("answer", type=float)

    s = sub.add_parser("score", help="Score a JSON submission using rubric + expected answer")
    s.add_argument("submission_path", help="Path to submission JSON")

    args = p.parse_args(argv)

    if args.cmd == "list":
        return cmd_list(as_json=args.json)
    if args.cmd == "reference":
        return cmd_reference(args.task_id, as_json=args.json)
    if args.cmd == "validate":
        return cmd_validate(args.task_id, args.answer, as_json=args.json)
    if args.cmd == "score":
        return cmd_score(args.submission_path, as_json=args.json)
    return 1
