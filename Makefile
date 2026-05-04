.PHONY: install req run-dev run db-up db-down

install:
	uv sync

req:
	uv pip freeze > requirements.txt

run-dev:
	uv run uvicorn src.main:app --reload

run:
	uv run uvicorn src.main:app

db-up:
	docker compose up -d

db-down:
	docker compose down