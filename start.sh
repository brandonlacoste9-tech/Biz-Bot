#!/bin/bash

# Biz-Bot Quick Start Script

echo "🤖 Starting Biz-Bot Multi-Tenant Platform..."
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Error: Docker is not running. Please start Docker and try again."
    exit 1
fi

# Check if .env exists, if not copy from example
if [ ! -f .env ]; then
    echo "📋 Creating .env file from .env.example..."
    cp .env.example .env
    echo "✓ .env file created. You can edit it to add your API keys."
else
    echo "✓ .env file already exists"
fi

echo ""
echo "🚀 Starting services with Docker Compose..."
docker-compose up -d postgres redis

echo ""
echo "⏳ Waiting for PostgreSQL to be ready..."
sleep 10

echo ""
echo "🔄 Building and starting backend..."
docker-compose up -d backend

echo ""
echo "⏳ Waiting for backend to be ready..."
sleep 5

echo ""
echo "📊 Running database migrations..."
docker-compose exec -T backend alembic upgrade head

echo ""
echo "🌱 Seeding demo data..."
docker-compose exec -T backend python seed_data.py

echo ""
echo "🎨 Starting frontend..."
docker-compose up -d frontend

echo ""
echo "✅ Biz-Bot is starting up!"
echo ""
echo "📍 Access points:"
echo "   Frontend:        http://localhost:3000"
echo "   Backend API:     http://localhost:8000"
echo "   API Docs:        http://localhost:8000/docs"
echo "   Health Check:    http://localhost:8000/health"
echo ""
echo "🔐 Demo accounts (use magic link authentication):"
echo "   - admin@cafe-quebecois.ca"
echo "   - admin@techsolutions.ca"
echo ""
echo "📝 Check backend logs for magic link URLs"
echo "   docker-compose logs -f backend"
echo ""
echo "🛑 To stop: docker-compose down"
echo "🗑️  To clean: docker-compose down -v (removes data)"
