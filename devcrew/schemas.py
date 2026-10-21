"""Pydantic schemas that force each agent to return structured JSON.

Why this matters: LLM agents tend to ramble. By binding each task to a
schema, the output of one agent becomes machine-parseable input for the
next agent in the pipeline — no regex, no guessing.
"""

from typing import Literal

from pydantic import BaseModel, Field

# ---------- Project Manager output ----------


class PlanItem(BaseModel):
    id: int = Field(description="Sequential task id, starting at 1")
    title: str = Field(description="Short task title")
    description: str = Field(description="What exactly needs to be built")


class ProjectPlan(BaseModel):
    project_name: str
    summary: str = Field(description="One-paragraph summary of the project")
    tasks: list[PlanItem] = Field(description="3-6 concrete development tasks")


# ---------- QA Tester output ----------


class TestCase(BaseModel):
    name: str
    scenario: str = Field(description="What is being tested")
    expected: str = Field(description="Expected behaviour")
    verdict: Literal["pass", "fail"] = Field(
        description="'pass' or 'fail' based on reading the code"
    )
    notes: str = Field(default="", description="Why it passes/fails")


class TestReport(BaseModel):
    total_cases: int
    passed: int
    failed: int
    test_cases: list[TestCase]
    bugs_found: list[str] = Field(description="Concrete bugs or edge cases the code misses")


# ---------- Code Reviewer output ----------


class ReviewComment(BaseModel):
    severity: Literal["critical", "major", "minor"] = Field(
        description="'critical', 'major' or 'minor'"
    )
    location: str = Field(description="Function or section of code")
    comment: str


class ReviewReport(BaseModel):
    verdict: Literal["approved", "changes_requested"] = Field(
        description="'approved' or 'changes_requested'"
    )
    readability_score: int = Field(ge=1, le=10, description="1-10")
    correctness_score: int = Field(ge=1, le=10, description="1-10")
    comments: list[ReviewComment]
    summary: str = Field(description="Final review summary in 2-3 sentences")
