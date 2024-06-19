.PHONY: up local migrations migrate
up:
	docker compose up --build

local:
	docker compose -f docker-compose.local.yml up -d --build

migrations:
	cd src; alembic revision --autogenerate

migrate:
	cd src; alembic upgrade head

.DEFAULT_GOAL := up
