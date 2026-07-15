# Kindred API

The Kindred backend is a Python 3.13 FastAPI service.

## Setup

Install the locked development dependencies:

```sh
uv sync --all-groups
```

## Development

Copy the local configuration template, then start the server:

```sh
cp .env.example .env
uv run --env-file .env uvicorn kindred_api.main:app --reload
```

The health endpoint is available at `GET /health`. FastAPI serves the OpenAPI schema at
`GET /openapi.json`.

## Database Configuration

The API reads settings from `KINDRED_` environment variables. `.env.example` documents local
development values. Copy `.env.test.example` to the ignored `.env.test` file to customize test
settings. Development and production require an async PostgreSQL URL:

```sh
export KINDRED_ENVIRONMENT=development
export KINDRED_DATABASE_URL='postgresql+asyncpg://kindred:kindred@localhost:5432/kindred'
```

Pytest loads `.env.test` automatically when present and otherwise falls back to `.env.test.example`.
The profile configures an isolated in-memory SQLite database using `sqlite+aiosqlite`. Integration
tests start a disposable PostgreSQL Docker container and inject its connection URL into the FastAPI
application. Invalid URLs, unsupported drivers, and missing non-test URLs prevent the API from
starting.

## Database Migrations

Alembic tracks each applied schema revision in the database. Copy `.env.example` to `.env` and
create the local PostgreSQL database before running migration commands:

```sh
uv run --env-file .env alembic upgrade head
```

Create a revision, write and review its `upgrade()` and `downgrade()` operations, then apply it
locally:

```sh
uv run --env-file .env alembic revision -m "describe schema change"
uv run --env-file .env alembic upgrade head
```

Do not edit a migration after it has been applied outside your local database. Create a new revision
to correct or evolve an existing schema instead.

## Quality Checks

Run each check from this directory:

```sh
uv run ruff format --check .
uv run ruff check .
uv run ty check
uv run pytest tests/unit
uv run pytest tests/integration
```

`make python-test` requires a running Docker daemon because it includes the PostgreSQL integration
tests. The integration suite applies all Alembic migrations to its disposable PostgreSQL database.

Generate a deterministic OpenAPI document:

```sh
uv run python scripts/generate_openapi.py --output openapi.json
```

`openapi.json` is committed as the versioned API contract. CI regenerates and commits it back to
same-repository pull request branches when the application schema changes.
