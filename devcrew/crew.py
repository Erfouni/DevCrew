"""Assemble the crew and run the pipeline end-to-end."""

from crewai import Crew, Process

from . import agents, tasks


def build_crew(output_dir: str = "output", model: str | None = None) -> Crew:
    llm = agents.get_llm(model)

    pm = agents.project_manager(llm)
    dev = agents.developer(llm)
    qa = agents.qa_tester(llm)
    reviewer = agents.code_reviewer(llm)

    t_plan = tasks.plan_task(pm, output_dir=output_dir)
    t_code = tasks.code_task(dev, plan=t_plan, output_dir=output_dir)
    t_test = tasks.test_task(qa, code=t_code, output_dir=output_dir)
    t_review = tasks.review_task(reviewer, code=t_code, tests=t_test, output_dir=output_dir)

    return Crew(
        agents=[pm, dev, qa, reviewer],
        tasks=[t_plan, t_code, t_test, t_review],
        process=Process.sequential,  # strict order: plan -> code -> test -> review
        verbose=True,
    )


def run(idea: str, output_dir: str = "output", model: str | None = None) -> str:
    """Run the full pipeline for a one-line project idea."""
    crew = build_crew(output_dir=output_dir, model=model)
    result = crew.kickoff(inputs={"idea": idea})
    return str(result)
