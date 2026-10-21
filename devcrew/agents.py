"""The four specialised agents.

Each agent gets a narrow role, goal and backstory ("role-scoped context").
This is deliberate: a focused prompt hallucinates less than one giant
prompt asking a single LLM to plan, code, test and review all at once.
"""

import os

from crewai import LLM, Agent

DEFAULT_MODEL = "gpt-4o-mini"


def get_llm(model: str | None = None) -> LLM:
    """One shared LLM config. Model comes from the argument, then the MODEL env var."""
    return LLM(
        model=model or os.getenv("MODEL", DEFAULT_MODEL),
        temperature=0.3,  # low temp = more deterministic, parseable output
    )


def project_manager(llm: LLM) -> Agent:
    return Agent(
        role="Project Manager",
        goal="Break the user's idea into a small, concrete development plan.",
        backstory=(
            "You are a pragmatic software project manager. You take vague "
            "one-line ideas and turn them into 3-6 unambiguous tasks a "
            "developer can implement in a single Python file. You never "
            "invent features the user did not ask for."
        ),
        llm=llm,
        verbose=True,
    )


def developer(llm: LLM) -> Agent:
    return Agent(
        role="Python Developer",
        goal="Implement the project plan as clean, working Python code.",
        backstory=(
            "You are a senior Python developer. You write a single, "
            "self-contained, runnable Python file with functions, docstrings "
            "and a __main__ demo block. You implement exactly the tasks in "
            "the plan — nothing more. You only use the standard library."
        ),
        llm=llm,
        verbose=True,
    )


def qa_tester(llm: LLM) -> Agent:
    return Agent(
        role="QA Tester",
        goal="Find bugs and untested edge cases in the developer's code.",
        backstory=(
            "You are a sceptical QA engineer. You read code line by line "
            "looking for edge cases: empty inputs, wrong types, negative "
            "numbers, duplicates. You design test cases and honestly mark "
            "which ones the current code would fail."
        ),
        llm=llm,
        verbose=True,
    )


def code_reviewer(llm: LLM) -> Agent:
    return Agent(
        role="Code Reviewer",
        goal="Judge the code on readability and correctness, using the QA report.",
        backstory=(
            "You are a strict but fair code reviewer. You consider both the "
            "code and the QA report, score readability and correctness out "
            "of 10, and give a final verdict: approved or changes_requested. "
            "You point at specific functions, never vague advice."
        ),
        llm=llm,
        verbose=True,
    )
