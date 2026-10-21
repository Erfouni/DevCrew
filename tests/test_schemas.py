"""The committed sample run must match the schemas agents are bound to."""

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from devcrew import schemas

SAMPLE = Path(__file__).resolve().parent.parent / "sample_output"


def load(name: str) -> dict:
    return json.loads((SAMPLE / name).read_text())


def test_sample_plan_is_valid():
    plan = schemas.ProjectPlan.model_validate(load("01_plan.json"))
    assert 3 <= len(plan.tasks) <= 6
    assert [t.id for t in plan.tasks] == list(range(1, len(plan.tasks) + 1))


def test_sample_test_report_is_valid():
    report = schemas.TestReport.model_validate(load("03_test_report.json"))
    assert report.total_cases == len(report.test_cases)
    assert report.passed + report.failed == report.total_cases


def test_sample_review_is_valid():
    schemas.ReviewReport.model_validate(load("04_review.json"))


def test_sample_code_compiles():
    compile((SAMPLE / "02_code.py").read_text(), "02_code.py", "exec")


@pytest.mark.parametrize("score", [0, 11])
def test_review_scores_are_bounded(score):
    review = load("04_review.json") | {"readability_score": score}
    with pytest.raises(ValidationError):
        schemas.ReviewReport.model_validate(review)


def test_unknown_verdict_is_rejected():
    review = load("04_review.json") | {"verdict": "looks fine"}
    with pytest.raises(ValidationError):
        schemas.ReviewReport.model_validate(review)


def test_unknown_severity_is_rejected():
    review = load("04_review.json")
    review["comments"][0]["severity"] = "blocker"
    with pytest.raises(ValidationError):
        schemas.ReviewReport.model_validate(review)
