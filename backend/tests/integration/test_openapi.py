import pytest
from httpx import AsyncClient


@pytest.mark.integration
async def test_openapi_schema_includes_api_metadata(client: AsyncClient) -> None:
    response = await client.get("/openapi.json")

    assert response.status_code == 200
    assert response.json()["info"] == {
        "description": "API for sharing private albums and photos with the people who matter.",
        "title": "Kindred API",
        "version": "0.1.0",
    }
