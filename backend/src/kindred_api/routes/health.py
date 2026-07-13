from typing import Annotated

from fastapi import APIRouter, Depends

from kindred_api.dependencies import get_health_service
from kindred_api.dtos.health import HealthResponse
from kindred_api.services.health import HealthService

router = APIRouter(tags=["health"])


@router.get("/health")
async def health_check(
    health_service: Annotated[HealthService, Depends(get_health_service)],
) -> HealthResponse:
    """Return the service health without exposing implementation details."""
    health_status = health_service.check()
    return HealthResponse(status=health_status.status)
