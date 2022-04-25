build:
	docker compose build --no-cache
up:
	docker compose up
upd:
	docker compose up -d
down:
	docker compose down
destroy:
	docker compose down -v
test:
	docker compose exec device-data-ingestion-api su -c "pytest"
