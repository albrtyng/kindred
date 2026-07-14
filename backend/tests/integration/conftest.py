from collections.abc import AsyncIterator, Iterator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient
from testcontainers.postgres import PostgresContainer

from kindred_api.config import Settings
from kindred_api.main import create_app


@pytest.fixture(scope="session")
def postgres_database_url() -> Iterator[str]:
    """Start one disposable PostgreSQL database for the integration test session."""
    with PostgresContainer("postgres:17-alpine", driver="asyncpg") as postgres:
        yield postgres.get_connection_url()


@pytest.fixture
def app(postgres_database_url: str) -> FastAPI:
    """Create an application connected to the disposable PostgreSQL database."""
    return create_app(Settings(environment="test", database_url=postgres_database_url))


@pytest.fixture
async def client(app: FastAPI) -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=app)
    async with (
        app.router.lifespan_context(app),
        AsyncClient(transport=transport, base_url="http://testserver") as test_client,
    ):
        yield test_client
