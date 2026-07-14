import pytest
from sqlalchemy import text

from kindred_api.config import Settings
from kindred_api.db.session import create_engine, create_session_factory


@pytest.mark.unit
async def test_session_executes_a_simple_query() -> None:
    engine = create_engine(Settings(environment="test"))
    session_factory = create_session_factory(engine)

    try:
        async with session_factory() as session:
            result = await session.execute(text("SELECT 1"))

        assert result.scalar_one() == 1
    finally:
        await engine.dispose()
