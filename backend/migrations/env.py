from asyncio import run
from logging.config import fileConfig

from alembic import context
from sqlalchemy.engine import Connection

from kindred_api.config import Settings
from kindred_api.db.base import Base
from kindred_api.db.session import create_engine

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Import model modules here before using this metadata when introducing Alembic autogeneration.
target_metadata = Base.metadata


def database_url() -> str:
    """Return the validated application database URL for offline migrations."""
    url = Settings().database_url
    if url is None:
        msg = "Database settings must be validated before running migrations."
        raise RuntimeError(msg)
    return url


def run_migrations_offline() -> None:
    """Run migrations without a database connection."""
    context.configure(
        url=database_url(),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    """Configure Alembic with an active synchronous connection facade."""
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations through the application's asynchronous database engine."""
    engine = create_engine(Settings())
    try:
        async with engine.connect() as connection:
            await connection.run_sync(do_run_migrations)
    finally:
        await engine.dispose()


def run_migrations_online() -> None:
    """Run migrations against a live database."""
    run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
