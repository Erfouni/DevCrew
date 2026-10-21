# Contributing to DevCrew

Thanks for helping out! Bug reports, prompt improvements, new agents and docs fixes are all welcome.

## Set up

```bash
git clone https://github.com/agrvasu05/DevCrew && cd DevCrew
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
```

## Before opening a PR

```bash
pytest                              # no API key or network needed
ruff check . && ruff format --check .
```

The unit tests never call an LLM. They check that the pipeline is wired correctly
(which agent sees which output) and that the committed `sample_output/` matches the
schemas in `devcrew/schemas.py`.

If you change a prompt in `agents.py`/`tasks.py` or a schema in `schemas.py`, also run
the pipeline once for real (`devcrew "some idea"`) and mention the result in your PR.
If the run is a good showcase, you can refresh `sample_output/` with it.

## Where things live

| File | What to change there |
|---|---|
| `devcrew/agents.py` | Agent roles, goals, backstories, LLM settings |
| `devcrew/tasks.py` | Task instructions and who hands off to whom |
| `devcrew/schemas.py` | The JSON each agent must return |
| `devcrew/crew.py` | Pipeline assembly |
| `devcrew/cli.py` | Command-line options |

## Good first issues

Look for the [`good first issue`](https://github.com/agrvasu05/DevCrew/labels/good%20first%20issue)
label. Comment on the issue before starting so work isn't duplicated.

## Releases

Maintainers bump `__version__` in `devcrew/__init__.py`, update `CHANGELOG.md`, and publish a
GitHub release; the release workflow publishes to PyPI.
