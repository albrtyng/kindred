from typing import Literal, Self

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import make_url
from sqlalchemy.exc import ArgumentError

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"


class Settings(BaseSettings):
    """Application settings supplied through KINDRED_ environment variables."""

    model_config = SettingsConfigDict(env_prefix="KINDRED_", case_sensitive=False)

    environment: Literal["development", "test", "production"] = "development"
    database_url: str | None = None

    @property
    def is_test(self) -> bool:
        """Whether these settings are configured for the test environment."""
        return self.environment == "test"

    @model_validator(mode="after")
    def validate_database_url(self) -> Self:
        """Require async PostgreSQL outside tests and isolated SQLite in tests."""
        if self.database_url is None and self.is_test:
            self.database_url = TEST_DATABASE_URL

        if self.database_url is None:
            msg = "KINDRED_DATABASE_URL is required outside the test environment."
            raise ValueError(msg)

        try:
            url = make_url(self.database_url)
        except ArgumentError as error:
            msg = "KINDRED_DATABASE_URL must be a valid SQLAlchemy URL."
            raise ValueError(msg) from error

        if self.is_test:
            if url.drivername not in {"postgresql+asyncpg", "sqlite+aiosqlite"}:
                msg = (
                    "KINDRED_DATABASE_URL must use sqlite+aiosqlite or postgresql+asyncpg "
                    "in the test environment."
                )
                raise ValueError(msg)
        elif url.drivername != "postgresql+asyncpg":
            msg = "KINDRED_DATABASE_URL must use postgresql+asyncpg outside the test environment."
            raise ValueError(msg)

        return self
