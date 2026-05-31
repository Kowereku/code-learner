# 1. Match your local Windows Python version
FROM python:3.13-slim

# 2. Install uv directly into the container (Astral's official method)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# 3. Keep Python logs clean and real-time
ENV PYTHONUNBUFFERED=1

# 4. Set the working directory
WORKDIR /app

# 5. Copy requirements FIRST to cache the installation layer
COPY requirements.txt .

# 6. Use uv to install packages into the system environment (super fast!)
RUN uv pip install --system --no-cache -r requirements.txt

# 7. Copy the rest of your application code
COPY . .

# 8. Expose the port
EXPOSE 8000

# 9. Apply DB migrations, then start the server.
CMD ["sh", "-c", "alembic upgrade head && uvicorn src.main:app --host 0.0.0.0 --port 8000"]