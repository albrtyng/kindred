from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from kindred_api.config import Settings
from kindred_api.services.health import HealthService


@lru_cache
def get_settings() -> Settings:
    """Provide one settings instance per process; tests can override this dependency."""
    return Settings()


def get_health_service(
    settings: Annotated[Settings, Depends(get_settings)],
) -> HealthService:
    """Construct the health service through FastAPI's dependency graph."""
    return HealthService(settings)
