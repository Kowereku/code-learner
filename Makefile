.PHONY: install req run-dev run migrate up down build logs db-up db-down hooks

install:
	uv sync

req:
	uv pip freeze > requirements.txt

run-dev:
	uv run uvicorn src.main:app --reload

run:
	uv run uvicorn src.main:app

migrate:
	uv run alembic upgrade head

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