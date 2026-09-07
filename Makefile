.PHONY: up down build restart logs test migrate migrations superuser check shell

up:
	docker compose up -d

down:
	docker compose down

build:
	docker compose build

restart:
	docker compose restart

logs:
	docker compose logs -f

test:
	uv run python src/manage.py test jobs

migrate:
	docker compose exec web uv run python src/manage.py migrate

migrations:
	uv run python src/manage.py makemigrations

superuser:
	docker compose exec web uv run python src/manage.py createsuperuser

check:
	uv run python src/manage.py check

shell:
	docker compose exec web uv run python src/manage.py shell
