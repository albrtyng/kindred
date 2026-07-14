import pytest
from pydantic import ValidationError

from kindred_api.config import TEST_DATABASE_URL, Settings
from kindred_api.main import create_app


@pytest.mark.unit
def test_test_settings_default_to_an_isolated_sqlite_database() -> None:
    settings = Settings()

    assert settings.is_test
    assert settings.database_url == TEST_DATABASE_URL


@pytest.mark.unit
def test_settings_rejects_missing_database_url_outside_tests() -> None:
    with pytest.raises(ValidationError):
        Settings(environment="development", database_url=None)


@pytest.mark.unit
def test_settings_rejects_an_invalid_database_url() -> None:
    with pytest.raises(ValidationError):
        Settings(environment="production", database_url="not-a-url")


@pytest.mark.unit
def test_settings_requires_asyncpg_outside_tests() -> None:
    with pytest.raises(ValidationError):
        Settings(environment="production", database_url="postgresql://localhost/kindred")


@pytest.mark.unit
async def test_application_startup_reads_test_settings() -> None:
    app = create_app()

    async with app.router.lifespan_context(app):
        assert app.state.settings.is_test
