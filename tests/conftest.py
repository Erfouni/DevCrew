import pytest


@pytest.fixture(autouse=True)
def fake_api_key(monkeypatch):
    """Building agents needs a key to be set; no test ever calls the API."""
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test-not-a-real-key")
