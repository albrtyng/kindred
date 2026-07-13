import pytest

from kindred_api.config import Settings


@pytest.mark.unit
def test_settings_reads_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("KINDRED_ENVIRONMENT", "test")

    settings = Settings()

    assert settings.environment == "test"
