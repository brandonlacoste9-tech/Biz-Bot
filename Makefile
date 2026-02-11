.PHONY: help up down restart logs seed test clean build

help:
	@echo "Biz-Bot Development Commands"
	@echo ""
	@echo "  make up       - Start all services with Docker Compose"
	@echo "  make down     - Stop all services"
	@echo "  make restart  - Restart all services"
	@echo "  make logs     - Show logs from all services"
	@echo "  make seed     - Initialize database with seed data"
	@echo "  make test     - Run all tests"
	@echo "  make clean    - Clean up containers, volumes, and cache"
	@echo "  make build    - Build Docker images"

up:
	docker-compose up -d
	@echo "✅ Services started!"
	@echo "Frontend: http://localhost:3000"
	@echo "Backend: http://localhost:8000"
	@echo "API Docs: http://localhost:8000/docs"

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

logs-backend:
	docker-compose logs -f backend

logs-frontend:
	docker-compose logs -f frontend

seed:
	docker-compose exec backend python -m app.utils.seed_data

test:
	@echo "Running backend tests..."
	cd backend && pytest app/tests/ -v
	@echo "Backend tests completed!"

test-backend:
	docker-compose exec backend pytest app/tests/ -v

clean:
	docker-compose down -v
	rm -rf backend/__pycache__
	rm -rf backend/.pytest_cache
	rm -rf frontend/.next
	rm -rf frontend/node_modules
	@echo "✅ Cleaned up!"

build:
	docker-compose build

install-backend:
	cd backend && pip install -r requirements.txt

install-frontend:
	cd frontend && npm install

dev-backend:
	cd backend && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

dev-frontend:
	cd frontend && npm run dev
