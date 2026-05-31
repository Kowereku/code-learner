# 1. Match your local Windows Python version
FROM python:3.13-slim

# 2. Install uv directly into the container (Astral's official method)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 3. Keep Python logs clean and real-time, and put the venv on PATH
ENV PYTHONUNBUFFERED=1
ENV PATH="/app/.venv/bin:$PATH"

# 4. Set the working directory
WORKDIR /app

# 5. Install dependencies first to leverage Docker caching.
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project --no-dev

# 6. Copy the rest of your application code and install the project
COPY . .
RUN uv sync --frozen --no-dev

# 7. Expose the port
EXPOSE 8000

# 8. Apply DB migrations, then start the server.
CMD ["sh", "-c", "alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 8000"]
