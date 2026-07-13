# Kindred API

The Kindred backend is a Python 3.13 FastAPI service.

## Setup

Install the locked development dependencies:

```sh
uv sync --all-groups
```

## Development

Start the local server:

```sh
uv run uvicorn kindred_api.main:app --reload
```

The health endpoint is available at `GET /health`. FastAPI serves the OpenAPI schema at
`GET /openapi.json`.

## Quality Checks

Run each check from this directory:

```sh
uv run ruff format --check .
uv run ruff check .
uv run ty check
uv run pytest tests/unit
uv run pytest tests/integration
```

Generate a deterministic OpenAPI document:

```sh
uv run python scripts/generate_openapi.py --output openapi.json
```

`openapi.json` is committed as the versioned API contract. CI regenerates and commits it back to
same-repository pull request branches when the application schema changes.
