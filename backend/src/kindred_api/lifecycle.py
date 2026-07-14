from collections.abc import AsyncIterator, Callable
from contextlib import AbstractAsyncContextManager, asynccontextmanager

from fastapi import FastAPI

from kindred_api.config import Settings
from kindred_api.db.session import create_engine, create_session_factory

Lifespan = Callable[[FastAPI], AbstractAsyncContextManager[None]]


def create_lifespan(settings: Settings | None = None) -> Lifespan:
    """Create an application lifecycle with optional explicitly supplied settings."""

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        """Own process-scoped database resources for one application instance."""
        active_settings = settings if settings is not None else Settings()
        engine = create_engine(active_settings)
        app.state.settings = active_settings
        app.state.session_factory = create_session_factory(engine)

        try:
            yield
        finally:
            await engine.dispose()

    return lifespan
