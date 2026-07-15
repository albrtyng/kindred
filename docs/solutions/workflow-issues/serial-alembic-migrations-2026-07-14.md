---
title: Serialize Alembic migrations before application rollout
date: 2026-07-14
category: workflow-issues
module: backend database migrations
problem_type: workflow_issue
component: database
severity: high
applies_when:
  - Deploying a backend that runs Alembic migrations against PostgreSQL
  - Rolling out multiple application instances or retrying deployment jobs
tags: [alembic, postgresql, migrations, deployment]
---

# Serialize Alembic migrations before application rollout

## Context

Two deployment jobs can both observe the same Alembic revision, then race to create or update
`alembic_version` and execute the same schema operations. One job may fail even if the other
successfully advances the database.

## Guidance

Run migrations once as a dedicated deployment step before application instances are started or
rolled out. Do not run `alembic upgrade head` from FastAPI startup or from every application
container.

```text
deploy:
  1. Run one migration job: alembic upgrade head
  2. Wait for the migration job to succeed
  3. Roll out application containers
```

For protection against accidentally overlapping deployment jobs, have the migration runner acquire
a PostgreSQL advisory lock before invoking Alembic. The deployment workflow remains the primary
serialization mechanism; the database lock is a safety net.

## Why This Matters

Alembic tracks only the revision history. It does not coordinate independent deployment processes.
Serializing the migration runner avoids duplicate DDL, conflicting revision writes, and partial
rollouts where a losing application deployment fails after the schema has already changed.

## When to Apply

- Before introducing the first production migration runner.
- When deployment tooling can retry jobs or run deployments concurrently.
- Before scaling an application deployment to multiple replicas.

## Examples

Pre-deploy, confirm the target schema and inspect the recorded migration history:

```sql
SELECT current_database(), current_user, current_schema();
SELECT to_regclass('alembic_version') AS alembic_version_table;
SELECT version_num FROM alembic_version;
```

Run exactly one migration process after the advisory lock is held:

```sh
uv run --env-file <production-env-file> alembic upgrade head
```

Afterward, verify that the database has reached the expected revision:

```sql
SELECT version_num FROM alembic_version;
```

## Related

- [KIN-18: Set up versioned database migrations](https://linear.app/albrtyng/issue/KIN-18)
