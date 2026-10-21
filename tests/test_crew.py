"""The pipeline is wired as plan -> code -> test -> review, without calling an LLM."""

import os

from crewai import Process

from devcrew import schemas
from devcrew.crew import build_crew


def test_crew_has_four_agents_in_order():
    crew = build_crew()
    assert [a.role for a in crew.agents] == [
        "Project Manager",
        "Python Developer",
        "QA Tester",
        "Code Reviewer",
    ]
    assert crew.process == Process.sequential


def test_each_task_only_sees_what_it_needs():
    plan, code, test, review = build_crew().tasks
    assert not isinstance(plan.context, list)  # no upstream task
    assert code.context == [plan]
    assert test.context == [code]
    assert review.context == [code, test]


def test_structured_outputs_are_bound_to_schemas():
    plan, code, test, review = build_crew().tasks
    assert plan.output_json is schemas.ProjectPlan
    assert code.output_json is None
    assert test.output_json is schemas.TestReport
    assert review.output_json is schemas.ReviewReport


def test_output_dir_is_configurable():
    out = os.path.join("runs", "todo-app")
    tasks = build_crew(output_dir=out).tasks
    assert [os.path.basename(t.output_file) for t in tasks] == [
        "01_plan.json",
        "02_code.py",
        "03_test_report.json",
        "04_review.json",
    ]
    assert {os.path.dirname(t.output_file) for t in tasks} == {out}


def test_model_can_be_overridden(monkeypatch):
    monkeypatch.setenv("MODEL", "gpt-4o")
    assert build_crew().agents[0].llm.model == "gpt-4o"
    assert build_crew(model="gpt-4.1-mini").agents[0].llm.model == "gpt-4.1-mini"
