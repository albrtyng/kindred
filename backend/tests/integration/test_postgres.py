import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine


@pytest.mark.integration
async def test_postgres_container_accepts_connections(postgres_database_url: str) -> None:
    engine = create_async_engine(postgres_database_url)

    try:
        async with engine.connect() as connection:
            result = await connection.execute(text("SELECT version()"))

        assert "PostgreSQL" in result.scalar_one()
    finally:
        await engine.dispose()
