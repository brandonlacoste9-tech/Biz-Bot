.PHONY: help dev prod build up down logs restart clean ssl secrets backup test

# Default target
help:
@echo "Biz-Bot Makefile Commands:"
@echo ""
@echo "Development:"
@echo "  make dev          - Start development environment"
@echo "  make logs         - View development logs"
@echo "  make down         - Stop development environment"
@echo ""
@echo "Production:"
@echo "  make prod         - Start production environment"
@echo "  make prod-logs    - View production logs"
@echo "  make prod-down    - Stop production environment"
@echo ""
@echo "Setup:"
@echo "  make secrets      - Run secrets setup wizard"
@echo "  make ssl          - Setup SSL certificates"
@echo ""
@echo "Maintenance:"
@echo "  make backup       - Backup database and secrets"
@echo "  make restart      - Restart all services"
@echo "  make clean        - Clean up containers and volumes"
@echo "  make test         - Run tests"
@echo ""
@echo "Docker:"
@echo "  make build        - Build Docker images"
@echo "  make ps           - Show running containers"
@echo "  make stats        - Show container resource usage"

# Development commands
dev:
@echo "Starting development environment..."
docker-compose up -d
@echo "Services started. Access at http://localhost:3000"

dev-build:
@echo "Building and starting development environment..."
docker-compose up -d --build

logs:
docker-compose logs -f

down:
@echo "Stopping development environment..."
docker-compose down

# Production commands
prod:
@echo "Starting production environment..."
docker-compose -f docker-compose.prod.yml up -d
@echo "Production services started"
@make prod-status

prod-build:
@echo "Building and starting production environment..."
docker-compose -f docker-compose.prod.yml up -d --build

prod-logs:
docker-compose -f docker-compose.prod.yml logs -f

prod-down:
@echo "Stopping production environment..."
docker-compose -f docker-compose.prod.yml down

prod-status:
@echo "Checking production service status..."
docker-compose -f docker-compose.prod.yml ps

# Setup commands
secrets:
@echo "Running secrets setup wizard..."
./scripts/setup-secrets.sh

ssl:
@echo "Setting up SSL certificates..."
./scripts/setup-ssl.sh

# Docker commands
build:
docker-compose build

ps:
docker-compose ps

stats:
docker stats --no-stream

# Maintenance commands
backup:
@echo "Creating backup..."
@mkdir -p backups
@DATE=$$(date +%Y%m%d_%H%M%S) && \
docker exec biz-bot-postgres pg_dump -U bizbot bizbot | gzip > backups/db_backup_$$DATE.sql.gz && \
tar czf backups/secrets_backup_$$DATE.tar.gz secrets/ && \
echo "Backup completed: backups/*_$$DATE.*"

restore:
@echo "Please specify backup file: make restore FILE=backups/db_backup_20240211_120000.sql.gz"
@if [ -n "$(FILE)" ]; then \
gunzip -c $(FILE) | docker exec -i biz-bot-postgres psql -U bizbot bizbot && \
echo "Database restored from $(FILE)"; \
fi

restart:
@echo "Restarting services..."
docker-compose restart

restart-prod:
@echo "Restarting production services..."
docker-compose -f docker-compose.prod.yml restart

clean:
@echo "Cleaning up containers, volumes, and images..."
docker-compose down -v
@echo "Clean complete"

clean-all:
@echo "WARNING: This will remove all containers, volumes, and images!"
@read -p "Are you sure? [y/N] " -n 1 -r; \
echo; \
if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
docker-compose down -v --rmi all; \
echo "All cleaned up"; \
fi

# Testing
test:
@echo "Running tests..."
npm test

lint:
@echo "Running linter..."
npm run lint

# Health checks
health:
@echo "Checking application health..."
@curl -s http://localhost:3000/health | json_pp || echo "Service not responding"

health-prod:
@echo "Checking production health..."
@curl -s https://$${DOMAIN:-localhost}/health | json_pp || echo "Service not responding"

# Monitoring
metrics:
@echo "Opening Prometheus..."
@open http://localhost:9090 || xdg-open http://localhost:9090 || echo "Prometheus: http://localhost:9090"

grafana:
@echo "Opening Grafana..."
@open http://localhost:3001 || xdg-open http://localhost:3001 || echo "Grafana: http://localhost:3001"

# Database operations
db-shell:
@echo "Connecting to database..."
docker exec -it biz-bot-postgres psql -U bizbot -d bizbot

db-migrate:
@echo "Running database migrations..."
docker exec -it biz-bot-postgres psql -U bizbot -d bizbot -f /docker-entrypoint-initdb.d/init.sql

# Redis operations
redis-shell:
@echo "Connecting to Redis..."
docker exec -it biz-bot-redis redis-cli

redis-flush:
@echo "WARNING: This will clear all Redis data!"
@read -p "Are you sure? [y/N] " -n 1 -r; \
echo; \
if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
docker exec -it biz-bot-redis redis-cli FLUSHALL; \
echo "Redis flushed"; \
fi

# Logs
logs-app:
docker-compose logs -f app

logs-nginx:
docker-compose logs -f nginx

logs-db:
docker-compose logs -f postgres

logs-redis:
docker-compose logs -f redis

# Deploy
deploy:
@echo "Deploying to production..."
./scripts/deploy.sh

# Version
version:
@echo "Biz-Bot Version: 1.0.0"
@echo "Docker Version:" && docker --version
@echo "Docker Compose Version:" && docker-compose --version
