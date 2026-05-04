# code-learner

Python backend for beginner programming learning app.

## Alembic Operations

Alembic is configured to use the Postgres database defined in the project setup:

`postgresql+psycopg2://devuser:devpassword@localhost:5432/fastapi_db`

You can override that by setting `DATABASE_URL` before running Alembic.

### Start the database

If you are using Docker Compose, start Postgres first:

```bash
make db-up
```

### Create a migration

Generate a new migration from your SQLAlchemy models:

```bash
uv run alembic revision --autogenerate -m "describe changes"
```

For autogenerate to detect tables, make sure the model modules are imported and that they use the shared `Base` from `src/model/db.py`.

### Apply migrations

Upgrade the database to the latest revision:

```bash
uv run alembic upgrade head
```

### Check the current revision

Show the revision currently applied to the database:

```bash
uv run alembic current
```

### Move backward

Downgrade by one migration step:

```bash
uv run alembic downgrade -1
```

### Useful notes

If `--autogenerate` creates an empty migration, it usually means no model metadata was imported before Alembic loaded `target_metadata`.

The shared SQLAlchemy base lives in `src/model/db.py` and Alembic reads `Base.metadata` from there.

## Commit Hooks

This repository includes a commit-msg hook that enforces conventional commit messages and requires a JIRA ticket key in the scope.

Install it once after cloning:

```bash
make hooks
```

The expected format is:

```text
type(ABC-123): short summary
```

Examples:

```text
feat(ABC-123): add course lookup
fix(PLAT-42): reject expired tokens
```
