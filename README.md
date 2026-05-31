# code-learner

Python backend for beginner programming learning app.

## Running with Docker

The full stack (FastAPI app + Postgres) runs via Docker Compose. The `app` service waits for `db` to pass its healthcheck, then applies `alembic upgrade head` before starting the server.

### Start the full stack

Build the image and start both services:

```bash
make up
```

### Verify it is running

The app is exposed on `localhost:8000`:

```bash
curl http://localhost:8000/
```

### Follow the logs

Tail the app container output:

```bash
make logs
```

### Stop the stack

Stop and remove the containers:

```bash
make down
```

## Local Development

Run Postgres in Docker and the app directly on your machine. Inside Compose the app reaches the database as host `db`; locally `src/model/db.py` falls back to `localhost`.

### Start Postgres only

```bash
make db-up
```

### Run the app with hot reload

```bash
make run-dev
```

### Stop Postgres

```bash
make db-down
```

## Alembic Operations

Alembic is configured to use the Postgres database defined in the project setup:

`postgresql+psycopg2://devuser:devpassword@localhost:5432/fastapi_db`

You can override that by setting `DATABASE_URL` before running Alembic. Start Postgres first with `make db-up` (see [Local Development](#local-development)).

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

## Branch Naming Convention

Branches must follow the format: `<type>/<TICKET>-<short-summary>`

Valid types: `feat`, `fix`, `chore`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`

Examples:

```text
feat/ABC-123-add-course-lookup
fix/PLAT-42-reject-expired-tokens
docs/ABC-100-update-api-docs
```

The branch name is validated by a GitHub Action on every pull request.
