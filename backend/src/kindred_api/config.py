from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings supplied through KINDRED_ environment variables."""

    model_config = SettingsConfigDict(env_prefix="KINDRED_", case_sensitive=False)

    environment: Literal["development", "test", "production"] = "development"
