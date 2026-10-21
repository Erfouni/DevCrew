# DevCrew — Multi-Agent AI Orchestration System

[![CI](https://github.com/agrvasu05/DevCrew/actions/workflows/ci.yml/badge.svg)](https://github.com/agrvasu05/DevCrew/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
![Python 3.10–3.13](https://img.shields.io/badge/python-3.10%E2%80%933.13-blue.svg)

An AI software team in a pipeline. You give it a one-line project idea; four specialised LLM agents plan it, code it, test it, and review it — each handing structured output to the next.

Built with **CrewAI** on the OpenAI API.

## How it works

```
 idea ─→ ┌─────────────────┐      ┌─────────────────┐
         │ Project Manager │ ───→ │    Developer    │
         │  plan.json      │      │    code.py      │
         └─────────────────┘      └───────┬─────────┘
                                          │
                                          ▼
         ┌─────────────────┐      ┌─────────────────┐
         │  Code Reviewer  │ ←─── │    QA Tester    │
         │  review.json    │      │ test_report.json│
         └─────────────────┘      └─────────────────┘
          (sees code + QA report)
```

1. **Project Manager** turns the idea into a 3–6 task plan (JSON).
2. **Developer** implements the plan as one runnable Python file.
3. **QA Tester** designs edge-case tests against the code and honestly marks which would fail (JSON).
4. **Code Reviewer** reads the code *and* the QA report, scores it, and gives a verdict (JSON).

## Design decisions

- **Role-scoped context, not one giant prompt.** Each agent only receives what it needs (the developer sees the plan, not the user's raw message). Narrow prompts hallucinate less and stay on task.
- **Structured JSON outputs via Pydantic.** Every non-code output is bound to a schema (`devcrew/schemas.py`), so one agent's output is machine-parseable input for the next — no regex, no parsing failures.
- **Sequential process.** A software pipeline has a natural order; sequential orchestration keeps the run deterministic and debuggable. Every stage is written to `output/` so you can inspect exactly where a run went wrong.
- **Adversarial QA.** The tester is prompted to be sceptical and mark failures honestly, and the reviewer sees the QA report — so the review verdict is grounded in found bugs, not vibes.

## Run it

```bash
git clone https://github.com/agrvasu05/DevCrew && cd DevCrew
pip install -e .
cp .env.example .env   # add your OPENAI_API_KEY

devcrew "Build a CLI expense tracker with categories and monthly totals"
```

`python main.py "..."` still works if you'd rather not install the package.

| Option | Default | What it does |
|---|---|---|
| `-o`, `--output-dir` | `output` | Where results go (a path relative to the current directory) |
| `-m`, `--model` | `$MODEL` or `gpt-4o-mini` | Which LLM the agents use |
| `--version` | | Print the version |

Outputs land in the output directory:

| File | Agent | Contents |
|---|---|---|
| `01_plan.json` | Project Manager | Task breakdown |
| `02_code.py` | Developer | Runnable Python file |
| `03_test_report.json` | QA Tester | Test cases + bugs found |
| `04_review.json` | Code Reviewer | Scores, comments, verdict |

A full example run is committed in [`sample_output/`](sample_output/).

> DevCrew never runs the code it generates. Read `02_code.py` before you execute it.

## Development

```bash
pip install -e ".[dev]"
pytest          # no API key or network needed
ruff check .
```

The tests check how the pipeline is wired (which agent sees which output) and validate
`sample_output/` against the schemas, without calling an LLM. CI runs them on Python 3.10–3.13.

## Roadmap

- Feed the reviewer's verdict back to the Developer for a fix-up round when changes are requested
- Actually run the generated code against the QA test cases in a sandbox
- Support projects that span more than one file
- A small eval set of project ideas to catch prompt regressions in CI

Ideas and PRs are welcome — see [CONTRIBUTING.md](CONTRIBUTING.md).

## Stack

Python · CrewAI · OpenAI API · Pydantic

## Project structure

```
devcrew/
├── main.py              # thin wrapper around devcrew.cli
├── devcrew/
│   ├── cli.py           # `devcrew` command-line entry point
│   ├── agents.py        # 4 agents with role-scoped prompts
│   ├── tasks.py         # pipeline tasks + context hand-offs
│   ├── schemas.py       # Pydantic schemas for structured JSON
│   └── crew.py          # crew assembly (sequential process)
├── sample_output/       # committed example run
├── tests/               # offline unit tests
├── pyproject.toml
├── requirements.txt
└── .env.example
```

## License

[MIT](LICENSE) © Vasu Agrawal
