from asyncio import run
from pathlib import Path

import pytest
from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine


def migration_config() -> Config:
    """Load the Alembic configuration committed with the backend."""
    backend_directory = Path(__file__).parent.parent.parent
    return Config(str(backend_directory / "alembic.ini"))


async def current_revision(database_url: str) -> str:
    """Read the revision Alembic recorded in the migrated database."""
    engine = create_async_engine(database_url)
    try:
        async with engine.connect() as connection:
            result = await connection.execute(text("SELECT version_num FROM alembic_version"))
        return result.scalar_one()
    finally:
        await engine.dispose()


@pytest.mark.integration
def test_migrations_upgrade_postgres(
    postgres_database_url: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Apply the complete migration history to a disposable PostgreSQL database."""
    monkeypatch.setenv("KINDRED_ENVIRONMENT", "test")
    monkeypatch.setenv("KINDRED_DATABASE_URL", postgres_database_url)
    config = migration_config()

    command.upgrade(config, "head")

    assert (
        run(current_revision(postgres_database_url))
        == ScriptDirectory.from_config(config).get_current_head()
    )
