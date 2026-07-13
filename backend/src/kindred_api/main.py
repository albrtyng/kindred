from fastapi import FastAPI

from kindred_api.routes.health import router as health_router


def create_app() -> FastAPI:
    """Create the API application without constructing infrastructure at import time."""
    app = FastAPI(
        title="Kindred API",
        description="API for sharing private albums and photos with the people who matter.",
        # TODO: Derive this from release metadata once release automation exists.
        # https://linear.app/albrtyng/issue/KIN-35/automate-release-versioning
        version="0.1.0",
    )
    app.include_router(health_router)
    return app


app = create_app()
