#!/bin/bash

# Deployment script for Biz-Bot on VPS
# This script automates the deployment process

set -e

echo "🚀 Starting Biz-Bot deployment..."

# Configuration
VPS_IP="${VPS_IP:-155.138.139.53}"
VPS_USER="${VPS_USER:-root}"
DOMAIN="${DOMAIN:-yourdomain.com}"
DEPLOY_PATH="/opt/biz-bot"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if we're on the VPS or deploying remotely
if [ -f "/.dockerenv" ] || [ "$USER" = "$VPS_USER" ]; then
    echo -e "${GREEN}Running on VPS${NC}"
    ON_VPS=true
else
    echo -e "${YELLOW}Deploying to remote VPS${NC}"
    ON_VPS=false
fi

# Function to run command locally or via SSH
run_command() {
    if [ "$ON_VPS" = true ]; then
        eval "$1"
    else
        ssh "$VPS_USER@$VPS_IP" "$1"
    fi
}

# Step 1: Pull latest changes
echo -e "${GREEN}Step 1: Pulling latest changes...${NC}"
if [ "$ON_VPS" = true ]; then
    git pull origin main
else
    echo "Syncing files to VPS..."
    rsync -avz --exclude 'node_modules' --exclude '.git' --exclude 'secrets' \
        ./ "$VPS_USER@$VPS_IP:$DEPLOY_PATH/"
fi

# Step 2: Setup SSL certificates (if needed)
echo -e "${GREEN}Step 2: Checking SSL certificates...${NC}"
run_command "cd $DEPLOY_PATH && if [ ! -f nginx/ssl/fullchain.pem ]; then \
    echo 'SSL certificates not found. Please run setup-ssl.sh first'; \
fi"

# Step 3: Build Docker images
echo -e "${GREEN}Step 3: Building Docker images...${NC}"
run_command "cd $DEPLOY_PATH && docker-compose -f docker-compose.prod.yml build"

# Step 4: Start services
echo -e "${GREEN}Step 4: Starting services...${NC}"
run_command "cd $DEPLOY_PATH && docker-compose -f docker-compose.prod.yml up -d"

# Step 5: Wait for services to be healthy
echo -e "${GREEN}Step 5: Waiting for services to be healthy...${NC}"
sleep 10

# Step 6: Check health
echo -e "${GREEN}Step 6: Checking service health...${NC}"
run_command "cd $DEPLOY_PATH && docker-compose -f docker-compose.prod.yml ps"

# Step 7: Show logs
echo -e "${GREEN}Step 7: Showing recent logs...${NC}"
run_command "cd $DEPLOY_PATH && docker-compose -f docker-compose.prod.yml logs --tail=50"

echo -e "${GREEN}✓ Deployment complete!${NC}"
echo
echo "Access your application:"
echo "  - Application: https://$DOMAIN"
echo "  - Prometheus: http://$VPS_IP:9090"
echo "  - Grafana: http://$VPS_IP:3001"
echo
echo "To view logs: docker-compose -f docker-compose.prod.yml logs -f"
echo "To stop services: docker-compose -f docker-compose.prod.yml down"
