.PHONY: install run-dev run migrate seed up down build logs db-up db-down hooks

install:
	uv sync

run-dev:
	uv run uvicorn src.main:app --reload

run:
	uv run uvicorn src.main:app

migrate:
	uv run alembic upgrade head

seed:
	uv run python -m src.scripts.seed

up:
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