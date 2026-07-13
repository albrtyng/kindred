from dataclasses import dataclass
from typing import Literal

from kindred_api.config import Settings


@dataclass(frozen=True)
class HealthStatus:
    status: Literal["ok"]


class HealthService:
    """Small injectable service that establishes the dependency-injection boundary."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def check(self) -> HealthStatus:
        """Return a successful health status."""
        return HealthStatus(status="ok")
