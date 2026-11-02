.PHONY: install run-dev run test migrate seed db-setup up down build logs db-up db-down hooks ai-up ai-pull

install:
	uv sync

test:
	uv run pytest -q

run-dev:
	uv run uvicorn src.main:app --reload

run:
	uv run uvicorn src.main:app

migrate:
	docker compose run --rm --build app alembic upgrade head

seed:
	docker compose run --rm --build app python -m src.scripts.seed

db-setup: migrate seed

up: db-setup
	docker compose up -d --build

down:
	docker compose down

build:
	docker compose build

logs:
	docker compose logs -f app

db-up:
	docker compose up -d db

db-down:
	docker compose stop db

hooks:
	git config core.hooksPath .githooks

ai-up:
	docker compose up -d ollama

ai-pull:
	docker compose exec ollama ollama pull qwen2.5-coder:7b
	docker compose exec ollama ollama pull gemma3:4b
