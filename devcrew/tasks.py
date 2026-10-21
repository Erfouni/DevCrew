"""The pipeline: Plan -> Code -> Test -> Review.

The hand-off between agents happens through CrewAI's `context` parameter:
each task receives the *output* of the previous task(s) as input. That is
the "orchestrated hand-off" — no agent sees the whole conversation, only
what it needs.
"""

import os

from crewai import Agent, Task

from .schemas import ProjectPlan, ReviewReport, TestReport


def plan_task(agent: Agent, output_dir: str = "output") -> Task:
    return Task(
        description=(
            "The user wants to build: '{idea}'.\n"
            "Create a development plan with 3-6 concrete tasks. The whole "
            "project must fit in ONE Python file using only the standard "
            "library."
        ),
        expected_output="A structured project plan as JSON.",
        agent=agent,
        output_json=ProjectPlan,
        output_file=os.path.join(output_dir, "01_plan.json"),
    )


def code_task(agent: Agent, plan: Task, output_dir: str = "output") -> Task:
    return Task(
        description=(
            "Implement the project plan you received as ONE self-contained "
            "Python file. Include docstrings and a small demo under "
            "`if __name__ == '__main__':`. Output ONLY the raw Python code, "
            "no markdown fences, no explanations."
        ),
        expected_output="A single runnable Python file.",
        agent=agent,
        context=[plan],  # hand-off: developer only sees the plan
        output_file=os.path.join(output_dir, "02_code.py"),
    )


def test_task(agent: Agent, code: Task, output_dir: str = "output") -> Task:
    return Task(
        description=(
            "Read the Python code you received and design 5-8 test cases "
            "covering normal use and edge cases (empty input, invalid input, "
            "duplicates, boundaries). For each, decide honestly whether the "
            "CURRENT code would pass or fail, and list concrete bugs."
        ),
        expected_output="A structured QA test report as JSON.",
        agent=agent,
        context=[code],  # hand-off: tester only sees the code
        output_json=TestReport,
        output_file=os.path.join(output_dir, "03_test_report.json"),
    )


def review_task(agent: Agent, code: Task, tests: Task, output_dir: str = "output") -> Task:
    return Task(
        description=(
            "Review the code, taking the QA report into account. Score "
            "readability and correctness out of 10, leave specific comments "
            "with severity levels, and give a final verdict."
        ),
        expected_output="A structured code review as JSON.",
        agent=agent,
        context=[code, tests],  # hand-off: reviewer sees code + QA report
        output_json=ReviewReport,
        output_file=os.path.join(output_dir, "04_review.json"),
    )
