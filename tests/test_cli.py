import pytest

from devcrew import __version__, cli


def test_version(capsys):
    with pytest.raises(SystemExit) as exc:
        cli.main(["--version"])
    assert exc.value.code == 0
    assert __version__ in capsys.readouterr().out


def test_idea_is_required():
    with pytest.raises(SystemExit) as exc:
        cli.main([])
    assert exc.value.code == 2


def test_missing_api_key_exits_with_hint(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY")
    monkeypatch.setattr(cli, "load_dotenv", lambda: None)
    with pytest.raises(SystemExit) as exc:
        cli.main(["a todo app"])
    assert "OPENAI_API_KEY" in str(exc.value.code)


@pytest.mark.parametrize("bad", ["/tmp/out", "../out", "~/out"])
def test_output_dir_must_be_relative(bad):
    with pytest.raises(SystemExit) as exc:
        cli.main(["a todo app", "-o", bad])
    assert exc.value.code == 2


def test_runs_pipeline_with_options(monkeypatch, tmp_path):
    calls = {}

    def fake_run(idea, output_dir, model):
        calls.update(idea=idea, output_dir=output_dir, model=model)
        return "ok"

    monkeypatch.setattr("devcrew.crew.run", fake_run)
    monkeypatch.chdir(tmp_path)
    assert cli.main(["a todo app", "-o", "runs/todo", "-m", "gpt-4o"]) == 0
    assert calls == {"idea": "a todo app", "output_dir": "runs/todo", "model": "gpt-4o"}
    assert (tmp_path / "runs" / "todo").is_dir()
