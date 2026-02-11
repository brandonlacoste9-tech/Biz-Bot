#!/bin/bash

set -e

echo "🚀 Starting Biz-Bot Setup..."
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please update the .env file with your API keys (Twilio, ElevenLabs)"
fi

# Build and start services
echo "🏗️  Building Docker images..."
docker-compose build

echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 10

# Check if backend is ready
echo "🔍 Checking backend health..."
until curl -s http://localhost:8000/api/health/ > /dev/null; do
    echo "   Waiting for backend..."
    sleep 2
done

echo "✅ Backend is ready!"

# Initialize database with seed data
echo "🌱 Seeding database..."
docker-compose exec backend python -m app.utils.seed_data

echo ""
echo "✅ Setup complete!"
echo ""
echo "📱 Access the application:"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo ""
echo "🔐 Test Login Credentials:"
echo "   Email: admin@cafe-quebecois.ca (or any user from seed data)"
echo "   Use magic link authentication"
echo ""
echo "📚 Useful commands:"
echo "   make logs        - View logs"
echo "   make restart     - Restart services"
echo "   make down        - Stop services"
echo "   make clean       - Clean up everything"
echo ""
