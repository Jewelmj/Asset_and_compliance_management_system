.PHONY: help build up down restart logs clean init-db seed-db verify-db backup restore dev

help:
	@echo "Site-Steward MVP - Docker Commands"
	@echo ""
	@echo "  make build       - Build all Docker images"
	@echo "  make up          - Start all services"
	@echo "  make down        - Stop all services"
	@echo "  make restart     - Restart all services"
	@echo "  make logs        - View logs from all services"
	@echo "  make clean       - Remove all containers, volumes, and images"
	@echo "  make init-db     - Initialize database (create tables only)"
	@echo "  make seed-db     - Initialize database with seed data"
	@echo "  make verify-db   - Verify seed data was loaded correctly"
	@echo "  make backup      - Backup database"
	@echo "  make restore     - Restore database from backup"
	@echo "  make dev         - Start in development mode with hot-reload"

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "Services started!"
	@echo "Admin Portal: http://localhost:8501"
	@echo "Field App: http://localhost:8502"
	@echo "API: http://localhost:5000"

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

clean:
	docker-compose down -v --rmi all
	@echo "All containers, volumes, and images removed"

init-db:
	docker-compose exec api python database/init_db.py
	@echo "Database initialized (tables created)"

seed-db:
	docker-compose exec api python database/init_db.py --seed
	@echo "Database initialized with seed data"
	@echo ""
	@echo "Default credentials:"
	@echo "  Admin - username: admin, password: admin123"
	@echo "  Foreman - username: foreman, password: foreman123"

verify-db:
	docker-compose exec api python scripts/verify_seed_data.py

backup:
	@mkdir -p backups
	docker-compose exec db pg_dump -U admin sitesteward > backups/backup_$$(date +%Y%m%d_%H%M%S).sql
	@echo "Database backed up to backups/"

restore:
	@read -p "Enter backup file path: " backup_file; \
	docker-compose exec -T db psql -U admin sitesteward < $$backup_file
	@echo "Database restored"

dev:
	docker-compose -f docker-compose.yml -f docker-compose.dev.yml up
	@echo "Development mode started with hot-reload"
