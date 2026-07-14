from collections.abc import AsyncIterator
from typing import Annotated

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from kindred_api.config import Settings
from kindred_api.services.health import HealthService


def get_settings(request: Request) -> Settings:
    """Provide settings initialized by the application lifespan."""
    return request.app.state.settings


def get_session_factory(request: Request) -> async_sessionmaker[AsyncSession]:
    """Provide the session factory initialized by the application lifespan."""
    return request.app.state.session_factory


async def get_session(
    session_factory: Annotated[async_sessionmaker[AsyncSession], Depends(get_session_factory)],
) -> AsyncIterator[AsyncSession]:
    """Provide a request-scoped async database session."""
    async with session_factory() as session:
        yield session


def get_health_service(
    settings: Annotated[Settings, Depends(get_settings)],
) -> HealthService:
    """Construct the health service through FastAPI's dependency graph."""
    return HealthService(settings)
