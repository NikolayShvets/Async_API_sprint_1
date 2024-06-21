.PHONY: up down local down_local
up:
	docker compose up --build

down:
	docker compose down -v --remove-orphans

local:
	docker compose -f docker-compose.local.yml up -d --build

down_local:
	docker compose -f docker-compose.local.yml down -v --remove-orphans

.DEFAULT_GOAL := up
