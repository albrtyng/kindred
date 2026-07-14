from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from kindred_api.config import Settings


def create_engine(settings: Settings) -> AsyncEngine:
    """Create an async database engine from validated application settings."""
    if settings.database_url is None:
        msg = "Database settings must be validated before creating an engine."
        raise RuntimeError(msg)

    return create_async_engine(settings.database_url)


def create_session_factory(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    """Create sessions that do not expire loaded values after commits."""
    return async_sessionmaker(engine, expire_on_commit=False)
